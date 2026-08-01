# Copyright (C) 2026 Chris Malek.
"""Abstaining single-page merge orchestration and facade."""

from __future__ import annotations

from typing import Any, Callable, NamedTuple, TypeVar

from bochord.models import (
    AlternateCandidate,
    BaselineShift,
    BoundingBox,
    BundlePage,
    CoordinateSpace,
    FontSlant,
    FontWeight,
    LineRecord,
    MergeFlag,
    MergeFlagType,
    MergePageInput,
    MergePageResult,
    MergePolicy,
    NoteRecord,
    ObjectProvenance,
    PassWitnessPage,
    PreparedPage,
    RegionRecord,
    SpanRecord,
    TextRole,
    Typography,
)
from bochord.services.text_normalization import (
    DEFAULT_TEXT_NORMALIZATION_POLICY,
    TextNormalizer,
)

#: Fixed merge confidence when all witnesses agree on an object.
_MERGE_CONFIDENCE_AGREEMENT = 1.0
#: Fixed merge confidence when precedence resolves differing alternates.
_MERGE_CONFIDENCE_PRECEDENCE = 0.7
#: Fixed merge confidence for material disagreement or weak evidence.
_MERGE_CONFIDENCE_CONFLICT = 0.3

#: Type variable for region and line layout objects.
_LayoutObject = TypeVar("_LayoutObject", RegionRecord, LineRecord)


class _SpanCandidate(NamedTuple):
    """One matched witness span offered for merge resolution."""

    #: Witness artifact that supplied this span candidate.
    witness_id: str
    #: Runner that emitted the witness supplying this span candidate.
    runner_id: str
    #: Matched span record from the witness graph.
    span: SpanRecord
    #: Normalized diplomatic text used for equality comparison.
    normalized_text: str


class _NoteCandidate(NamedTuple):
    """One matched witness note offered for merge resolution."""

    #: Witness artifact that supplied this note candidate.
    witness_id: str
    #: Runner that emitted the witness supplying this note candidate.
    runner_id: str
    #: Matched note record from the witness graph.
    note: NoteRecord


class _MarkerMappingContext(NamedTuple):
    """Inputs required to map witness marker spans onto accepted spans."""

    #: Witness fragment supplying marker span identifiers.
    witness: PassWitnessPage
    #: Witness chosen as the structure scaffold.
    scaffold_witness: PassWitnessPage
    #: Accepted spans in the merged page graph.
    accepted_spans: list[SpanRecord]
    #: Minimum IoU required for geometry matching.
    iou_threshold: float


class _NoteLinkResolutionContext(NamedTuple):
    """Inputs required to resolve note text and marker linkage."""

    #: Accepted spans in the merged page graph.
    accepted_spans: list[SpanRecord]
    #: Witness chosen as the structure scaffold.
    scaffold_witness: PassWitnessPage
    #: Eligible witnesses aligned to the prepared page.
    witnesses: list[PassWitnessPage]
    #: Minimum IoU required for geometry matching.
    iou_threshold: float
    #: Normalizer used when emitting normalized note text.
    text_normalizer: TextNormalizer


class _SpanRoleMergeState(NamedTuple):
    """Confidence, alternates, and flag callback for span-role resolution."""

    #: Current merge confidence for the span.
    confidence: float
    #: Alternate candidates accumulated during resolution.
    alternates: list[AlternateCandidate]
    #: Callback that appends one merge flag to the run accumulator.
    add_flag: Callable[..., None]


class _NoteLinkMergeState(NamedTuple):
    """Confidence, alternates, and flag callback for note-link resolution."""

    #: Current merge confidence for the note.
    confidence: float
    #: Alternate candidates accumulated during resolution.
    alternates: list[AlternateCandidate]
    #: Callback that appends one merge flag to the run accumulator.
    add_flag: Callable[..., None]


def _box_iou(left: BoundingBox, right: BoundingBox) -> float:
    """
    Return intersection-over-union for two axis-aligned boxes.

    Args:
        left: First box.
        right: Second box.

    Returns:
        IoU in ``[0, 1]``.

    """
    x0 = max(left.x0, right.x0)
    y0 = max(left.y0, right.y0)
    x1 = min(left.x1, right.x1)
    y1 = min(left.y1, right.y1)
    if x1 <= x0 or y1 <= y0:
        return 0.0
    intersection = (x1 - x0) * (y1 - y0)
    left_area = (left.x1 - left.x0) * (left.y1 - left.y0)
    right_area = (right.x1 - right.x0) * (right.y1 - right.y0)
    return intersection / (left_area + right_area - intersection)


class MergeOrchestrator:
    """
    Per-page mutable merge state and step runner.

    Args:
        policy: Versioned merge precedence and thresholds.
        page_input: Competing witness fragments for one page.
        text_normalizer: Normalizer used when emitting accepted text.

    """

    def __init__(
        self,
        policy: MergePolicy,
        page_input: MergePageInput,
        text_normalizer: TextNormalizer,
    ) -> None:
        """
        Initialize merge orchestration for one page.

        Args:
            policy: Versioned merge precedence and thresholds.
            page_input: Competing witness fragments for one page.
            text_normalizer: Normalizer used when emitting accepted text.

        """
        #: Versioned merge precedence and thresholds.
        self._policy = policy
        #: Competing witness fragments for one page.
        self._page_input = page_input
        #: Normalizer used when emitting accepted text.
        self._text_normalizer = text_normalizer
        #: Accepted prepared page variant for this merge run.
        self._prepared_page: PreparedPage | None = None
        #: Witnesses aligned to the accepted prepared page variant.
        self._eligible_witnesses: list[PassWitnessPage] = []
        #: Cross-variant witnesses excluded from geometry merge.
        self._skipped_witnesses: list[PassWitnessPage] = []
        #: Witness chosen as the structure scaffold.
        self._scaffold_witness: PassWitnessPage | None = None
        #: Accepted region nodes under construction.
        self._regions: list[RegionRecord] = []
        #: Accepted line nodes under construction.
        self._lines: list[LineRecord] = []
        #: Accepted span nodes under construction.
        self._spans: list[SpanRecord] = []
        #: Accepted note nodes under construction.
        self._notes: list[NoteRecord] = []
        #: Material disagreement flags emitted during merge.
        self._flags: list[MergeFlag] = []
        #: Whether merge abstained from asserting full certainty.
        self._abstained = False
        #: Alternate geometry payloads collected from losing scaffolds.
        self._geometry_alternates: list[AlternateCandidate] = []
        #: Monotonic counter for generated flag identifiers.
        self._next_flag_id = 1
        #: Whether a material structure scaffold conflict was detected.
        self._structure_scaffold_conflict = False

    def run(self) -> MergePageResult:
        """
        Execute the Spec 0009 merge sequence for one page.

        Returns:
            Accepted page graph plus flags and abstention state.

        """
        self._select_prepared_variant()
        self._normalize_coordinates()
        self._choose_structure_scaffold()
        self._align_layout()
        self._merge_text()
        self._merge_typography()
        self._merge_notes()
        self._apply_confidence_floor()
        return self._emit_result()

    def _select_prepared_variant(self) -> None:
        """Choose the accepted prepared page variant for this merge."""
        self._prepared_page = self._page_input.prepared_page.model_copy(deep=True)

    def _normalize_coordinates(self) -> None:
        """Keep same-variant witnesses and record skipped cross-variant evidence."""
        if self._prepared_page is None:
            msg = (
                "Prepared page variant must be selected before "
                "coordinate normalization."
            )
            raise RuntimeError(msg)
        self._eligible_witnesses = []
        self._skipped_witnesses = []
        for witness in self._page_input.witnesses:
            if _witness_skip_reason(self._prepared_page, witness) is None:
                self._eligible_witnesses.append(witness)
            else:
                self._skipped_witnesses.append(witness)

    def _choose_structure_scaffold(self) -> None:
        """Pick one coordinate-rich structure scaffold and detect layout conflicts."""
        candidates = _region_bearing_witnesses(self._eligible_witnesses)
        if not candidates:
            self._abstain_without_scaffold()
            return

        self._scaffold_witness = self._pick_scaffold_witness(candidates)
        if self._scaffold_witness is not None:
            self._flag_scaffold_conflicts(self._scaffold_witness)

    def _abstain_without_scaffold(self) -> None:
        """Record insufficient evidence when no region scaffold is available."""
        self._scaffold_witness = None
        self._abstained = True
        self._add_flag(
            MergeFlagType.INSUFFICIENT_EVIDENCE,
            target_object_ids=[],
            message=(
                "No witness supplies region structure for scaffold selection."
            ),
        )

    def _pick_scaffold_witness(
        self,
        candidates: list[PassWitnessPage],
    ) -> PassWitnessPage:
        """
        Select one scaffold witness from region-bearing candidates.

        Args:
            candidates: Eligible witnesses that supply region structure.

        Returns:
            Chosen scaffold witness.

        """
        if self._policy.structure_scaffold_runner_ids:
            preferred = _first_witness_by_runner_preference(
                candidates,
                self._policy.structure_scaffold_runner_ids,
            )
            return preferred if preferred is not None else candidates[0]
        return max(
            candidates,
            key=lambda witness: (
                _coordinate_rich_line_count(witness),
                -self._eligible_witnesses.index(witness),
            ),
        )

    def _flag_scaffold_conflicts(self, scaffold_witness: PassWitnessPage) -> None:
        """
        Compare other witnesses against the chosen scaffold and flag conflicts.

        Args:
            scaffold_witness: Witness selected as the structure scaffold.

        """
        for witness in self._eligible_witnesses:
            if witness.witness_id == scaffold_witness.witness_id:
                continue
            if not witness.regions:
                continue
            conflict, alternates = _detect_structure_conflict(
                scaffold_witness.regions,
                witness.regions,
                self._policy.iou_match_threshold,
                witness_id=witness.witness_id,
                runner_id=witness.runner_id,
            )
            if conflict:
                self._geometry_alternates.extend(alternates)
                self._structure_scaffold_conflict = True
                self._add_flag(
                    MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT,
                    target_object_ids=[
                        region.region_id for region in scaffold_witness.regions
                    ]
                    + [line.line_id for line in scaffold_witness.lines],
                    message=(
                        f"Witness {witness.witness_id} structure disagrees with "
                        f"scaffold {scaffold_witness.witness_id}."
                    ),
                )
                self._abstained = True

    def _align_layout(self) -> None:
        """Copy scaffold layout into the accepted graph without mutating witnesses."""
        if self._scaffold_witness is None:
            return

        merge_provenance = ObjectProvenance(
            source_page_id=self._page_input.page_id,
            witness_ids=[self._scaffold_witness.witness_id],
            runner_ids=[self._scaffold_witness.runner_id],
            machine_confidence=self._scaffold_witness.machine_confidence,
        )
        self._regions, self._lines, self._spans, self._notes = _copy_scaffold_layout(
            self._scaffold_witness,
            merge_provenance,
        )
        layout_confidence = (
            _MERGE_CONFIDENCE_CONFLICT
            if self._structure_scaffold_conflict
            else _MERGE_CONFIDENCE_AGREEMENT
        )
        self._regions = _apply_layout_merge_confidence(self._regions, layout_confidence)
        self._lines = _apply_layout_merge_confidence(self._lines, layout_confidence)
        if self._regions:
            if self._prepared_page is None:
                msg = (
                    "Prepared page variant must be selected before "
                    "attaching region alternates."
                )
                raise RuntimeError(msg)
            self._regions = _attach_region_alternates(
                self._regions,
                self._skipped_witnesses,
                self._geometry_alternates,
                prepared_page=self._prepared_page,
            )

    def _merge_text(self) -> None:
        """Resolve diplomatic text for each accepted span from witness candidates."""
        if self._scaffold_witness is None:
            return
        self._spans = [
            self._resolve_span_text(span) for span in self._spans
        ]

    def _merge_typography(self) -> None:
        """Resolve typography facets and roles independently for each span."""
        if self._scaffold_witness is None:
            return
        self._spans = [
            self._resolve_typography(span) for span in self._spans
        ]

    def _merge_notes(self) -> None:
        """Resolve note text and marker linkage from witness candidates."""
        if self._scaffold_witness is None:
            return
        self._notes = [
            self._resolve_note_links(note) for note in self._notes
        ]

    def _apply_confidence_floor(self) -> None:
        """Abstain when any accepted object falls below the policy confidence floor."""
        minimum = self._policy.min_merge_confidence_to_accept
        flagged_ids = _flagged_object_ids(self._flags)
        for obj_id, obj in _iter_accepted_objects(
            self._regions,
            self._lines,
            self._spans,
            self._notes,
        ):
            confidence = obj.provenance.merge_confidence
            if confidence is None or confidence >= minimum:
                continue
            self._abstained = True
            if obj_id in flagged_ids:
                continue
            self._add_flag(
                MergeFlagType.INSUFFICIENT_EVIDENCE,
                target_object_ids=[obj_id],
                message=(
                    f"Object {obj_id} merge confidence {confidence} "
                    f"is below acceptance floor {minimum}."
                ),
            )
            flagged_ids.add(obj_id)

    def _resolve_span_text(self, span: SpanRecord) -> SpanRecord:
        """
        Choose diplomatic text for one accepted span from matched witnesses.

        Args:
            span: Accepted span copied from the structure scaffold.

        Returns:
            Span with resolved text, confidence, alternates, and flags applied.

        """
        if self._scaffold_witness is None:
            return span
        candidates = _collect_span_candidates(
            span,
            self._scaffold_witness,
            self._eligible_witnesses,
            self._policy.iou_match_threshold,
            self._text_normalizer,
        )
        if not candidates:
            return _span_with_insufficient_text_evidence(
                span,
                self._text_normalizer,
                self._add_flag,
            )
        return _apply_span_text_resolution(
            span,
            candidates,
            self._text_normalizer,
            self._policy.runner_text_precedence,
            self._add_flag,
        )

    def _resolve_typography(self, span: SpanRecord) -> SpanRecord:
        """
        Resolve typography facets and roles independently for one span.

        Args:
            span: Accepted span with text already resolved.

        Returns:
            Span with resolved typography, roles, confidence, and flags applied.

        """
        if self._scaffold_witness is None:
            return span
        candidates = _collect_span_candidates(
            span,
            self._scaffold_witness,
            self._eligible_witnesses,
            self._policy.iou_match_threshold,
            self._text_normalizer,
        )
        if not candidates:
            return span
        return _apply_span_typography_resolution(span, candidates, self._add_flag)

    def _resolve_note_links(self, note: NoteRecord) -> NoteRecord:
        """
        Resolve note text and marker linkage from matched witness notes.

        Args:
            note: Accepted note copied from the structure scaffold.

        Returns:
            Note with resolved text, links, confidence, alternates, and flags.

        """
        if self._scaffold_witness is None:
            return note
        candidates = _collect_note_candidates(
            note,
            self._scaffold_witness,
            self._eligible_witnesses,
            self._policy.iou_match_threshold,
        )
        return _apply_note_link_resolution(
            note,
            candidates,
            _NoteLinkResolutionContext(
                accepted_spans=self._spans,
                scaffold_witness=self._scaffold_witness,
                witnesses=self._eligible_witnesses,
                iou_threshold=self._policy.iou_match_threshold,
                text_normalizer=self._text_normalizer,
            ),
            self._add_flag,
        )

    def _emit_result(self) -> MergePageResult:
        """
        Build the accepted page graph result for this merge run.

        Returns:
            Merge result containing the accepted page graph and flags.

        """
        if self._prepared_page is None:
            msg = "Prepared page variant must be selected before emitting merge result."
            raise RuntimeError(msg)
        page = BundlePage(
            page_id=self._page_input.page_id,
            page_number=self._page_input.page_number,
            prepared_page=self._prepared_page,
            regions=self._regions,
            lines=self._lines,
            spans=self._spans,
            notes=self._notes,
        )
        return MergePageResult(
            page=page,
            flags=self._flags,
            abstained=self._abstained,
        )

    def _add_flag(
        self,
        flag_type: MergeFlagType,
        *,
        target_object_ids: list[str],
        message: str,
    ) -> None:
        """
        Append one merge flag to the run accumulator.

        Args:
            flag_type: Disagreement category for the flag.

        Keyword Args:
            target_object_ids: Derived object ids affected by the disagreement.
            message: Human-readable explanation of the disagreement.

        """
        flag_id = f"merge-flag-{self._next_flag_id}"
        self._next_flag_id += 1
        self._flags.append(
            MergeFlag(
                flag_id=flag_id,
                flag_type=flag_type,
                target_object_ids=target_object_ids,
                message=message,
            )
        )


class AbstainingMergeService:
    """
    Stateless facade: merge one page of competing witnesses.

    Args:
        text_normalizer: Optional normalizer; defaults to Spec 0008 v1 policy.

    """

    def __init__(self, text_normalizer: TextNormalizer | None = None) -> None:
        """
        Initialize the merge facade.

        Args:
            text_normalizer: Optional normalizer; defaults to Spec 0008 v1 policy.

        """
        #: Normalizer used when emitting accepted diplomatic and normalized text.
        self._text_normalizer = text_normalizer or TextNormalizer(
            DEFAULT_TEXT_NORMALIZATION_POLICY
        )

    def merge_page(
        self,
        page_input: MergePageInput,
        policy: MergePolicy,
    ) -> MergePageResult:
        """
        Merge competing witness fragments into one accepted page graph.

        Args:
            page_input: Competing witness fragments for one page.
            policy: Versioned merge precedence and thresholds.

        Returns:
            Accepted page graph plus flags and abstention state.

        """
        if (
            policy.text_normalization_policy_id
            != self._text_normalizer.policy.policy_id
        ):
            msg = (
                "MergePolicy text_normalization_policy_id "
                f"{policy.text_normalization_policy_id!r} does not match "
                "TextNormalizer policy_id "
                f"{self._text_normalizer.policy.policy_id!r}"
            )
            raise ValueError(msg)
        orchestrator = MergeOrchestrator(
            policy=policy,
            page_input=page_input,
            text_normalizer=self._text_normalizer,
        )
        return orchestrator.run()


def _region_bearing_witnesses(
    witnesses: list[PassWitnessPage],
) -> list[PassWitnessPage]:
    """
    Return witnesses that supply region structure for scaffold selection.

    Args:
        witnesses: Eligible witnesses aligned to the accepted prepared page.

    Returns:
        Witnesses with at least one region node.

    """
    return [witness for witness in witnesses if witness.regions]


def _first_witness_by_runner_preference(
    candidates: list[PassWitnessPage],
    runner_ids: list[str],
) -> PassWitnessPage | None:
    """
    Pick the first eligible witness for the earliest preferred runner id.

    Args:
        candidates: Region-bearing witnesses in input order.
        runner_ids: Preferred runner ids in precedence order.

    Returns:
        First matching witness, or ``None`` when no runner id matches.

    """
    by_runner: dict[str, PassWitnessPage] = {}
    for witness in candidates:
        if witness.runner_id not in by_runner:
            by_runner[witness.runner_id] = witness
    for runner_id in runner_ids:
        preferred = by_runner.get(runner_id)
        if preferred is not None:
            return preferred
    return None


def _copy_scaffold_layout(
    scaffold: PassWitnessPage,
    merge_provenance: ObjectProvenance,
) -> tuple[
    list[RegionRecord],
    list[LineRecord],
    list[SpanRecord],
    list[NoteRecord],
]:
    """
    Deep-copy scaffold layout nodes with merge provenance.

    Args:
        scaffold: Witness selected as the structure scaffold.
        merge_provenance: Provenance stamped onto accepted layout nodes.

    Returns:
        Accepted region, line, span, and note nodes copied from the scaffold.

    """
    provenance = merge_provenance.model_copy(deep=True)

    def _copy_node(node: RegionRecord | LineRecord | SpanRecord | NoteRecord) -> Any:
        return node.model_copy(
            update={"provenance": provenance.model_copy(deep=True)},
            deep=True,
        )

    regions = [_copy_node(region) for region in scaffold.regions]
    lines = [_copy_node(line) for line in scaffold.lines]
    spans = [_copy_node(span) for span in scaffold.spans]
    notes = [_copy_node(note) for note in scaffold.notes]
    return regions, lines, spans, notes


def _witness_coordinate_space_matches(
    expected: CoordinateSpace,
    witness_space: CoordinateSpace,
) -> bool:
    """
    Return whether a witness coordinate space aligns with the prepared page.

    Args:
        expected: Coordinate space from the accepted prepared page.
        witness_space: Coordinate space declared by one witness fragment.

    Returns:
        ``True`` when space identity and dimensions match.

    """
    return (
        witness_space.space_id == expected.space_id
        and witness_space.width_px == expected.width_px
        and witness_space.height_px == expected.height_px
    )


def _witness_bounding_box_spaces_match(
    expected_space_id: str,
    witness: PassWitnessPage,
) -> bool:
    """
    Return whether every present bounding box uses the expected coordinate space.

    Args:
        expected_space_id: Coordinate-space identifier from the prepared page.
        witness: Candidate witness fragment to evaluate.

    Returns:
        ``True`` when all non-null bounding boxes match ``expected_space_id``.

    """
    for region in witness.regions:
        if (
            region.bounding_box is not None
            and region.bounding_box.coordinate_space_id != expected_space_id
        ):
            return False
    for line in witness.lines:
        if (
            line.bounding_box is not None
            and line.bounding_box.coordinate_space_id != expected_space_id
        ):
            return False
    for span in witness.spans:
        if (
            span.bounding_box is not None
            and span.bounding_box.coordinate_space_id != expected_space_id
        ):
            return False
    for note in witness.notes:
        if (
            note.bounding_box is not None
            and note.bounding_box.coordinate_space_id != expected_space_id
        ):
            return False
    return True


def _witness_skip_reason(
    prepared_page: PreparedPage,
    witness: PassWitnessPage,
) -> str | None:
    """
    Return the skip reason for a witness excluded from merge eligibility.

    Args:
        prepared_page: Accepted prepared page variant for this merge run.
        witness: Candidate witness fragment to evaluate.

    Returns:
        Skip reason string, or ``None`` when the witness is eligible.

    """
    if witness.prepared_page_id != prepared_page.prepared_page_id:
        return "cross_variant_excluded"
    if not _witness_coordinate_space_matches(
        prepared_page.coordinate_space,
        witness.coordinate_space,
    ):
        return "coordinate_space_mismatch"
    if not _witness_bounding_box_spaces_match(
        prepared_page.coordinate_space.space_id,
        witness,
    ):
        return "coordinate_space_mismatch"
    return None


def _apply_layout_merge_confidence(
    objects: list[_LayoutObject],
    confidence: float,
) -> list[_LayoutObject]:
    """
    Stamp merge confidence onto accepted layout objects.

    Args:
        objects: Accepted region or line nodes copied from the scaffold.
        confidence: Merge confidence to record on each object.

    Returns:
        Layout objects with updated provenance merge confidence.

    """
    updated: list[_LayoutObject] = []
    for obj in objects:
        provenance = obj.provenance.model_copy(deep=True)
        provenance.merge_confidence = confidence
        updated.append(
            obj.model_copy(update={"provenance": provenance}, deep=True)
        )
    return updated


def _attach_region_alternates(
    regions: list[RegionRecord],
    skipped_witnesses: list[PassWitnessPage],
    geometry_alternates: list[AlternateCandidate],
    *,
    prepared_page: PreparedPage,
) -> list[RegionRecord]:
    """
    Attach skipped and geometry alternates to the first accepted region.

    Args:
        regions: Accepted region nodes copied from the scaffold.
        skipped_witnesses: Cross-variant witnesses excluded from merge.
        geometry_alternates: Losing geometry payloads from scaffold conflicts.

    Keyword Args:
        prepared_page: Accepted prepared page used to classify skip reasons.

    Returns:
        Region list with alternates attached to the first region.

    """
    alternates = [
        AlternateCandidate(
            witness_id=witness.witness_id,
            runner_id=witness.runner_id,
            value_kind="skipped_witness",
            value={
                "prepared_page_id": witness.prepared_page_id,
                "reason": _witness_skip_reason(prepared_page, witness),
            },
        )
        for witness in skipped_witnesses
    ]
    alternates.extend(geometry_alternates)
    if not alternates:
        return regions

    region = regions[0]
    provenance = region.provenance.model_copy(deep=True)
    provenance.alternate_candidates.extend(alternates)
    updated_regions = list(regions)
    updated_regions[0] = region.model_copy(update={"provenance": provenance}, deep=True)
    return updated_regions


def _coordinate_rich_line_count(witness: PassWitnessPage) -> int:
    """
    Count lines carrying bounding boxes or baseline geometry.

    Args:
        witness: One runner witness fragment.

    Returns:
        Number of coordinate-rich lines in the witness.

    """
    return sum(
        1
        for line in witness.lines
        if line.bounding_box is not None or line.baseline
    )


def _detect_structure_conflict(
    scaffold_regions: list[RegionRecord],
    witness_regions: list[RegionRecord],
    iou_threshold: float,
    *,
    witness_id: str,
    runner_id: str,
) -> tuple[bool, list[AlternateCandidate]]:
    """
    Decide whether witness regions disagree with the chosen scaffold.

    Args:
        scaffold_regions: Regions from the chosen scaffold witness.
        witness_regions: Regions from another eligible witness.
        iou_threshold: Minimum IoU required for a one-to-one region match.

    Keyword Args:
        witness_id: Witness identifier supplying alternate geometry.
        runner_id: Runner identifier supplying alternate geometry.

    Returns:
        Conflict flag plus alternate geometry payloads for losing regions.

    """
    scaffold_sorted = _regions_by_reading_order(scaffold_regions)
    witness_sorted = _regions_by_reading_order(witness_regions)
    if len(scaffold_sorted) != len(witness_sorted):
        return True, _geometry_alternates_for_regions(
            witness_sorted,
            witness_id=witness_id,
            runner_id=runner_id,
        )

    box_presence = _region_box_presence_mismatch(scaffold_sorted, witness_sorted)
    if box_presence is True:
        return True, _geometry_alternates_for_regions(
            witness_sorted,
            witness_id=witness_id,
            runner_id=runner_id,
        )
    if box_presence is None:
        return False, []

    if _regions_iou_conflict(scaffold_sorted, witness_sorted, iou_threshold):
        return True, _geometry_alternates_for_regions(
            witness_sorted,
            witness_id=witness_id,
            runner_id=runner_id,
        )
    return False, []


def _regions_by_reading_order(regions: list[RegionRecord]) -> list[RegionRecord]:
    """
    Sort regions by reading order index.

    Args:
        regions: Region nodes from one witness.

    Returns:
        Regions sorted by ``reading_order_index``.

    """
    return sorted(regions, key=lambda region: region.reading_order_index)


def _region_box_presence_mismatch(
    scaffold_sorted: list[RegionRecord],
    witness_sorted: list[RegionRecord],
) -> bool | None:
    """
    Decide whether region box presence disagrees between two witnesses.

    Args:
        scaffold_sorted: Scaffold regions sorted by reading order.
        witness_sorted: Witness regions sorted by reading order.

    Returns:
        ``True`` when box presence disagrees, ``False`` when both sides have
        boxes, and ``None`` when neither side supplies boxes.

    """
    scaffold_has_boxes = any(
        region.bounding_box is not None for region in scaffold_sorted
    )
    witness_has_boxes = any(
        region.bounding_box is not None for region in witness_sorted
    )
    if not scaffold_has_boxes and not witness_has_boxes:
        return None
    return scaffold_has_boxes != witness_has_boxes


def _regions_iou_conflict(
    scaffold_sorted: list[RegionRecord],
    witness_sorted: list[RegionRecord],
    iou_threshold: float,
) -> bool:
    """
    Return whether paired regions fail the IoU match threshold.

    Args:
        scaffold_sorted: Scaffold regions sorted by reading order.
        witness_sorted: Witness regions sorted by reading order.
        iou_threshold: Minimum IoU required for a one-to-one region match.

    Returns:
        ``True`` when any paired region boxes disagree beyond the threshold.

    """
    for scaffold_region, witness_region in zip(
        scaffold_sorted,
        witness_sorted,
        strict=True,
    ):
        scaffold_box = scaffold_region.bounding_box
        witness_box = witness_region.bounding_box
        if scaffold_box is None and witness_box is None:
            continue
        if scaffold_box is None or witness_box is None:
            return True
        if _box_iou(scaffold_box, witness_box) < iou_threshold:
            return True
    return False


def _geometry_alternates_for_regions(
    regions: list[RegionRecord],
    *,
    witness_id: str,
    runner_id: str,
) -> list[AlternateCandidate]:
    """
    Serialize losing witness regions as geometry alternate candidates.

    Args:
        regions: Region nodes from a non-scaffold witness.

    Keyword Args:
        witness_id: Witness identifier supplying the alternate geometry.
        runner_id: Runner identifier supplying the alternate geometry.

    Returns:
        Alternate candidate payloads for the supplied regions.

    """
    alternates: list[AlternateCandidate] = []
    for region in regions:
        value: dict[str, Any] = region.model_dump(mode="json")
        alternates.append(
            AlternateCandidate(
                witness_id=witness_id,
                runner_id=runner_id,
                value_kind="geometry",
                value=value,
                machine_confidence=region.provenance.machine_confidence,
            )
        )
    return alternates


def _min_merge_confidence(current: float | None, new: float) -> float:
    """
    Return the lower of two merge-confidence values.

    Args:
        current: Existing confidence, if any.
        new: Candidate confidence to compare.

    Returns:
        Minimum of the supplied confidence values.

    """
    if current is None:
        return new
    return min(current, new)


def _witness_ids_from_candidates(candidates: list[_SpanCandidate]) -> list[str]:
    """
    Collect unique witness ids from span candidates in input order.

    Args:
        candidates: Matched witness span candidates.

    Returns:
        Witness ids in first-seen order.

    """
    seen: set[str] = set()
    witness_ids: list[str] = []
    for candidate in candidates:
        if candidate.witness_id not in seen:
            seen.add(candidate.witness_id)
            witness_ids.append(candidate.witness_id)
    return witness_ids


def _runner_ids_from_candidates(candidates: list[_SpanCandidate]) -> list[str]:
    """
    Collect unique runner ids from span candidates in input order.

    Args:
        candidates: Matched witness span candidates.

    Returns:
        Runner ids in first-seen order.

    """
    seen: set[str] = set()
    runner_ids: list[str] = []
    for candidate in candidates:
        if candidate.runner_id not in seen:
            seen.add(candidate.runner_id)
            runner_ids.append(candidate.runner_id)
    return runner_ids


def _witness_ids_from_note_candidates(candidates: list[_NoteCandidate]) -> list[str]:
    """
    Collect unique witness ids from note candidates in input order.

    Args:
        candidates: Matched witness note candidates.

    Returns:
        Witness ids in first-seen order.

    """
    seen: set[str] = set()
    witness_ids: list[str] = []
    for candidate in candidates:
        if candidate.witness_id not in seen:
            seen.add(candidate.witness_id)
            witness_ids.append(candidate.witness_id)
    return witness_ids


def _runner_ids_from_note_candidates(candidates: list[_NoteCandidate]) -> list[str]:
    """
    Collect unique runner ids from note candidates in input order.

    Args:
        candidates: Matched witness note candidates.

    Returns:
        Runner ids in first-seen order.

    """
    seen: set[str] = set()
    runner_ids: list[str] = []
    for candidate in candidates:
        if candidate.runner_id not in seen:
            seen.add(candidate.runner_id)
            runner_ids.append(candidate.runner_id)
    return runner_ids


def _collect_span_candidates(
    accepted_span: SpanRecord,
    scaffold_witness: PassWitnessPage,
    witnesses: list[PassWitnessPage],
    iou_threshold: float,
    text_normalizer: TextNormalizer,
) -> list[_SpanCandidate]:
    """
    Gather matched span candidates from all eligible witnesses.

    Args:
        accepted_span: Accepted span copied from the scaffold layout.
        scaffold_witness: Witness chosen as the structure scaffold.
        witnesses: Eligible witnesses aligned to the prepared page.
        iou_threshold: Minimum IoU required for geometry matching.
        text_normalizer: Normalizer used when comparing diplomatic text.

    Returns:
        Matched span candidates with normalized text for comparison.

    """
    candidates: list[_SpanCandidate] = []
    for witness in witnesses:
        matched_spans = _matching_spans_for_witness(
            accepted_span,
            scaffold_witness,
            witness,
            iou_threshold,
        )
        candidates.extend(
            _SpanCandidate(
                witness_id=witness.witness_id,
                runner_id=witness.runner_id,
                span=matched_span,
                normalized_text=text_normalizer.normalize_span_text(
                    matched_span.text_diplomatic
                ),
            )
            for matched_span in matched_spans
        )
    return candidates


def _matching_spans_for_witness(
    accepted_span: SpanRecord,
    scaffold_witness: PassWitnessPage,
    witness: PassWitnessPage,
    iou_threshold: float,
) -> list[SpanRecord]:
    """
    Find witness spans that align to one accepted scaffold span.

    Args:
        accepted_span: Accepted span copied from the scaffold layout.
        scaffold_witness: Witness chosen as the structure scaffold.
        witness: Witness fragment to search for matching spans.
        iou_threshold: Minimum IoU required for geometry matching.

    Returns:
        Matching spans from the supplied witness.

    """
    if witness.witness_id == scaffold_witness.witness_id:
        original = _span_by_id(witness, accepted_span.span_id)
        return [original] if original is not None else []

    if accepted_span.bounding_box is not None:
        return [
            span
            for span in witness.spans
            if span.bounding_box is not None
            and _box_iou(accepted_span.bounding_box, span.bounding_box)
            >= iou_threshold
        ]

    return []


def _span_with_insufficient_text_evidence(
    span: SpanRecord,
    text_normalizer: TextNormalizer,
    add_flag: Callable[..., None],
) -> SpanRecord:
    """
    Return a span flagged for missing witness text evidence.

    Args:
        span: Accepted span copied from the structure scaffold.
        text_normalizer: Normalizer used when emitting normalized text.
        add_flag: Callback that appends one merge flag to the run accumulator.

    Returns:
        Span with insufficient-evidence confidence and flag applied.

    """
    add_flag(
        MergeFlagType.INSUFFICIENT_EVIDENCE,
        target_object_ids=[span.span_id],
        message=f"No witness span candidates matched {span.span_id}.",
    )
    provenance = span.provenance.model_copy(deep=True)
    provenance.merge_confidence = _MERGE_CONFIDENCE_CONFLICT
    return span.model_copy(
        update={
            "text_normalized": text_normalizer.normalize_span_text(
                span.text_diplomatic
            ),
            "provenance": provenance,
        },
        deep=True,
    )


def _apply_span_text_resolution(
    span: SpanRecord,
    candidates: list[_SpanCandidate],
    text_normalizer: TextNormalizer,
    runner_precedence: list[str],
    add_flag: Callable[..., None],
) -> SpanRecord:
    """
    Apply text agreement or disagreement resolution for one span.

    Args:
        span: Accepted span copied from the structure scaffold.
        candidates: Matched witness span candidates.
        text_normalizer: Normalizer used when emitting normalized text.
        runner_precedence: Preferred runner order for text acceptance.
        add_flag: Callback that appends one merge flag to the run accumulator.

    Returns:
        Span with resolved text, confidence, alternates, and flags applied.

    """
    provenance = span.provenance.model_copy(deep=True)
    alternates = list(provenance.alternate_candidates)
    confidence = _MERGE_CONFIDENCE_AGREEMENT
    diplomatic = span.text_diplomatic

    normalized_values = {candidate.normalized_text for candidate in candidates}
    if len(normalized_values) == 1:
        diplomatic = candidates[0].span.text_diplomatic
    else:
        diplomatic, confidence, text_alternates = _resolve_text_disagreement(
            span,
            candidates,
            runner_precedence,
        )
        alternates.extend(text_alternates)
        add_flag(
            MergeFlagType.TEXT_DISAGREEMENT,
            target_object_ids=[span.span_id],
            message=(
                f"Witnesses disagree on normalized text for span {span.span_id}."
            ),
        )

    provenance.merge_confidence = confidence
    provenance.alternate_candidates = alternates
    provenance.witness_ids = _witness_ids_from_candidates(candidates)
    provenance.runner_ids = _runner_ids_from_candidates(candidates)
    return span.model_copy(
        update={
            "text_diplomatic": diplomatic,
            "text_normalized": text_normalizer.normalize_span_text(diplomatic),
            "provenance": provenance,
        },
        deep=True,
    )


def _resolve_span_typography_conflicts(
    typography: Typography,
    candidates: list[_SpanCandidate],
    alternates: list[AlternateCandidate],
    confidence: float,
) -> tuple[Typography, list[AlternateCandidate], float, bool]:
    """
    Resolve typography facets from witness span candidates.

    Args:
        typography: Typography copied from the accepted span.
        candidates: Matched witness span candidates.
        alternates: Existing alternate candidates to extend.
        confidence: Current merge confidence for the span.

    Returns:
        Resolved typography, alternates, confidence, and typography conflict flag.

    """
    typography, facet_conflict, typo_alternates = _resolve_typography_facets(
        typography,
        candidates,
    )
    typo_conflict = False
    if facet_conflict:
        typo_conflict = True
        alternates = list(alternates)
        alternates.extend(typo_alternates)
        confidence = _min_merge_confidence(
            confidence,
            _MERGE_CONFIDENCE_CONFLICT,
        )
    return typography, alternates, confidence, typo_conflict


def _resolve_span_role_conflicts(
    candidates: list[_SpanCandidate],
    roles: list[TextRole],
    span_id: str,
    state: _SpanRoleMergeState,
) -> tuple[list[TextRole], _SpanRoleMergeState]:
    """
    Resolve span roles from witness candidates.

    Args:
        candidates: Matched witness span candidates.
        roles: Starting roles copied from the accepted span.
        span_id: Accepted span identifier for flag targeting.
        state: Confidence, alternates, and flag callback for role resolution.

    Returns:
        Resolved roles and updated merge state.

    """
    roles, role_conflict, role_alternates = _resolve_span_roles(candidates, roles)
    if not role_conflict:
        return roles, state

    alternates = list(state.alternates)
    alternates.extend(role_alternates)
    confidence = _min_merge_confidence(
        state.confidence,
        _MERGE_CONFIDENCE_CONFLICT,
    )
    state.add_flag(
        MergeFlagType.ROLE_CONFLICT,
        target_object_ids=[span_id],
        message=f"Witnesses disagree on roles for span {span_id}.",
    )
    return roles, state._replace(confidence=confidence, alternates=alternates)


def _apply_span_typography_resolution(
    span: SpanRecord,
    candidates: list[_SpanCandidate],
    add_flag: Callable[..., None],
) -> SpanRecord:
    """
    Apply typography and role resolution for one span.

    Args:
        span: Accepted span with text already resolved.
        candidates: Matched witness span candidates.
        add_flag: Callback that appends one merge flag to the run accumulator.

    Returns:
        Span with resolved typography, roles, confidence, and flags applied.

    """
    typography = span.typography.model_copy(deep=True)
    provenance = span.provenance.model_copy(deep=True)
    alternates = list(provenance.alternate_candidates)
    confidence = provenance.merge_confidence or _MERGE_CONFIDENCE_AGREEMENT
    roles = list(span.roles)

    typography, alternates, confidence, typo_conflict = (
        _resolve_span_typography_conflicts(
            typography,
            candidates,
            alternates,
            confidence,
        )
    )
    roles, role_state = _resolve_span_role_conflicts(
        candidates,
        roles,
        span.span_id,
        _SpanRoleMergeState(
            confidence=confidence,
            alternates=alternates,
            add_flag=add_flag,
        ),
    )
    if typo_conflict:
        add_flag(
            MergeFlagType.TYPOGRAPHY_CONFLICT,
            target_object_ids=[span.span_id],
            message=(
                f"Witnesses disagree on typography facets for span {span.span_id}."
            ),
        )

    provenance.merge_confidence = role_state.confidence
    provenance.alternate_candidates = role_state.alternates
    return span.model_copy(
        update={
            "typography": typography,
            "roles": roles,
            "provenance": provenance,
        },
        deep=True,
    )


def _resolve_span_roles(
    candidates: list[_SpanCandidate],
    default_roles: list[TextRole],
) -> tuple[list[TextRole], bool, list[AlternateCandidate]]:
    """
    Resolve span roles from matched witness candidates.

    Args:
        candidates: Matched witness span candidates.
        default_roles: Starting roles copied from the accepted span.

    Returns:
        Accepted roles, conflict flag, and role alternates.

    """
    role_sets = {frozenset(candidate.span.roles) for candidate in candidates}
    if len(role_sets) > 1:
        return (
            [TextRole.UNKNOWN],
            True,
            _role_alternates_from_candidates(candidates),
        )
    if candidates:
        return list(candidates[0].span.roles), False, []
    return default_roles, False, []


def _note_marker_links_when_mapping_ambiguous(
    note_id: str,
    candidates: list[_NoteCandidate],
    context: _NoteLinkResolutionContext,
    state: _NoteLinkMergeState,
) -> tuple[list[str], _NoteLinkMergeState]:
    """
    Return empty links when witness marker mapping is ambiguous.

    Args:
        note_id: Accepted note identifier for flag targeting.
        candidates: Matched witness note candidates.
        context: Witness, span, and threshold inputs for note-link resolution.
        state: Confidence, alternates, and flag callback for note-link resolution.

    Returns:
        Empty linked ids and updated merge state.

    """
    alternates = list(state.alternates)
    alternates.extend(_note_link_alternates(candidates, context))
    state.add_flag(
        MergeFlagType.NOTE_LINK_AMBIGUOUS,
        target_object_ids=[note_id],
        message=(
            f"Witness marker spans map ambiguously for note {note_id}."
        ),
    )
    return [], state._replace(
        confidence=_min_merge_confidence(
            state.confidence,
            _MERGE_CONFIDENCE_CONFLICT,
        ),
        alternates=alternates,
    )


def _note_marker_links_from_mapped_sets(
    note_id: str,
    mapped_sets: list[frozenset[str]],
    candidates: list[_NoteCandidate],
    context: _NoteLinkResolutionContext,
    state: _NoteLinkMergeState,
) -> tuple[list[str], _NoteLinkMergeState]:
    """
    Resolve linked marker ids when mapping succeeded for all candidates.

    Args:
        note_id: Accepted note identifier for flag targeting.
        mapped_sets: Mapped link-id sets per witness note candidate.
        candidates: Matched witness note candidates.
        context: Witness, span, and threshold inputs for note-link resolution.
        state: Confidence, alternates, and flag callback for note-link resolution.

    Returns:
        Linked marker span ids and updated merge state.

    """
    unique_sets = set(mapped_sets)
    if len(unique_sets) == 1:
        linked_ids = sorted(unique_sets.pop())
        return linked_ids, state._replace(
            confidence=_min_merge_confidence(
                state.confidence,
                _MERGE_CONFIDENCE_AGREEMENT,
            ),
        )

    alternates = list(state.alternates)
    alternates.extend(_note_link_alternates(candidates, context))
    state.add_flag(
        MergeFlagType.NOTE_LINK_AMBIGUOUS,
        target_object_ids=[note_id],
        message=(
            f"Witnesses supply conflicting note links for {note_id}."
        ),
    )
    return [], state._replace(
        confidence=_min_merge_confidence(
            state.confidence,
            _MERGE_CONFIDENCE_CONFLICT,
        ),
        alternates=alternates,
    )


def _resolve_note_marker_links(
    note_id: str,
    candidates: list[_NoteCandidate],
    context: _NoteLinkResolutionContext,
    state: _NoteLinkMergeState,
) -> tuple[list[str], _NoteLinkMergeState]:
    """
    Resolve linked marker span ids from matched witness notes.

    Args:
        note_id: Accepted note identifier for flag targeting.
        candidates: Matched witness note candidates.
        context: Witness, span, and threshold inputs for note-link resolution.
        state: Confidence, alternates, and flag callback for note-link resolution.

    Returns:
        Linked marker span ids and updated merge state.

    """
    mapped_sets, mapping_ambiguous = _mapped_note_link_sets(
        candidates,
        context,
    )
    if mapping_ambiguous:
        return _note_marker_links_when_mapping_ambiguous(
            note_id,
            candidates,
            context,
            state,
        )
    return _note_marker_links_from_mapped_sets(
        note_id,
        mapped_sets,
        candidates,
        context,
        state,
    )


def _apply_note_link_resolution(
    note: NoteRecord,
    candidates: list[_NoteCandidate],
    context: _NoteLinkResolutionContext,
    add_flag: Callable[..., None],
) -> NoteRecord:
    """
    Apply note text and marker-link resolution from matched witness notes.

    Args:
        note: Accepted note copied from the structure scaffold.
        candidates: Matched witness note candidates.
        context: Witness, span, and threshold inputs for note-link resolution.
        add_flag: Callback that appends one merge flag to the run accumulator.

    Returns:
        Note with resolved text, links, confidence, alternates, and flags.

    """
    provenance = note.provenance.model_copy(deep=True)
    alternates = list(provenance.alternate_candidates)
    confidence = provenance.merge_confidence or _MERGE_CONFIDENCE_AGREEMENT
    linked_ids = list(note.linked_marker_span_ids)
    diplomatic = note.text_diplomatic

    if candidates:
        diplomatic = candidates[0].note.text_diplomatic
        link_state = _NoteLinkMergeState(
            confidence=confidence,
            alternates=alternates,
            add_flag=add_flag,
        )
        linked_ids, link_state = _resolve_note_marker_links(
            note.note_id,
            candidates,
            context,
            link_state,
        )
        confidence = link_state.confidence
        alternates = link_state.alternates

    provenance.merge_confidence = confidence
    provenance.alternate_candidates = alternates
    if candidates:
        provenance.witness_ids = _witness_ids_from_note_candidates(candidates)
        provenance.runner_ids = _runner_ids_from_note_candidates(candidates)
    return note.model_copy(
        update={
            "text_diplomatic": diplomatic,
            "text_normalized": context.text_normalizer.normalize_note_text(
                diplomatic
            ),
            "linked_marker_span_ids": linked_ids,
            "provenance": provenance,
        },
        deep=True,
    )


def _mapped_note_link_sets(
    candidates: list[_NoteCandidate],
    context: _NoteLinkResolutionContext,
) -> tuple[list[frozenset[str]], bool]:
    """
    Map each witness note candidate's marker links onto accepted span ids.

    Args:
        candidates: Matched witness note candidates.
        context: Witness, span, and threshold inputs for note-link resolution.

    Returns:
        Mapped link-id sets per candidate and whether any mapping was ambiguous.

    """
    mapped_sets: list[frozenset[str]] = []
    mapping_ambiguous = False
    for candidate in candidates:
        witness = _witness_by_id(context.witnesses, candidate.witness_id)
        if witness is None:
            mapped_sets.append(frozenset())
            continue
        mapped_ids, candidate_ambiguous = _map_marker_span_ids(
            candidate.note.linked_marker_span_ids,
            _MarkerMappingContext(
                witness=witness,
                scaffold_witness=context.scaffold_witness,
                accepted_spans=context.accepted_spans,
                iou_threshold=context.iou_threshold,
            ),
        )
        if candidate_ambiguous:
            mapping_ambiguous = True
        mapped_sets.append(frozenset(mapped_ids))
    return mapped_sets, mapping_ambiguous


def _resolve_text_disagreement(
    span: SpanRecord,
    candidates: list[_SpanCandidate],
    runner_precedence: list[str],
) -> tuple[str, float, list[AlternateCandidate]]:
    """
    Resolve differing normalized text among span candidates.

    Args:
        span: Accepted scaffold-aligned span.
        candidates: Matched witness span candidates.
        runner_precedence: Preferred runner order for text acceptance.

    Returns:
        Chosen diplomatic text, merge confidence, and text alternates.

    """
    if runner_precedence:
        winner = _first_candidate_by_runner_precedence(candidates, runner_precedence)
        if winner is not None:
            alternates = _text_alternates_from_candidates(candidates, winner)
            return (
                winner.span.text_diplomatic,
                _MERGE_CONFIDENCE_PRECEDENCE,
                alternates,
            )
    alternates = _text_alternates_from_candidates(candidates)
    return span.text_diplomatic, _MERGE_CONFIDENCE_CONFLICT, alternates


def _first_candidate_by_runner_precedence(
    candidates: list[_SpanCandidate],
    runner_precedence: list[str],
) -> _SpanCandidate | None:
    """
    Pick the first candidate whose runner appears in precedence order.

    Args:
        candidates: Matched witness span candidates.
        runner_precedence: Preferred runner order for text acceptance.

    Returns:
        First precedence-matching candidate, if any.

    """
    by_runner: dict[str, _SpanCandidate] = {}
    for candidate in candidates:
        if candidate.runner_id not in by_runner:
            by_runner[candidate.runner_id] = candidate
    for runner_id in runner_precedence:
        preferred = by_runner.get(runner_id)
        if preferred is not None:
            return preferred
    return None


def _text_alternates_from_candidates(
    candidates: list[_SpanCandidate],
    winner: _SpanCandidate | None = None,
) -> list[AlternateCandidate]:
    """
    Serialize non-winning span text as alternate candidates.

    Args:
        candidates: Matched witness span candidates.
        winner: Accepted candidate to exclude from alternates.

    Returns:
        Alternate text payloads for losing candidates.

    """
    alternates: list[AlternateCandidate] = []
    for candidate in candidates:
        if winner is not None and (
            candidate.witness_id == winner.witness_id
            and candidate.span.span_id == winner.span.span_id
        ):
            continue
        alternates.append(
            AlternateCandidate(
                witness_id=candidate.witness_id,
                runner_id=candidate.runner_id,
                value_kind="text",
                value={
                    "text_diplomatic": candidate.span.text_diplomatic,
                    "text_normalized": candidate.normalized_text,
                },
                machine_confidence=candidate.span.provenance.machine_confidence,
            )
        )
    return alternates


def _resolve_typography_facets(
    typography: Typography,
    candidates: list[_SpanCandidate],
) -> tuple[Typography, bool, list[AlternateCandidate]]:
    """
    Resolve each typography facet independently from span candidates.

    Args:
        typography: Starting typography copied from the accepted span.
        candidates: Matched witness span candidates.

    Returns:
        Resolved typography, conflict flag, and typography alternates.

    """
    typography, enum_conflict, enum_alternates = _resolve_typography_enum_facets(
        typography,
        candidates,
    )
    typography, optional_conflict, optional_alternates = (
        _resolve_typography_optional_facets(
            typography,
            candidates,
        )
    )
    typography, family_conflict, family_alternates = _resolve_font_families_facet(
        typography,
        candidates,
    )
    conflict = enum_conflict or optional_conflict or family_conflict
    alternates = enum_alternates + optional_alternates + family_alternates
    return typography, conflict, alternates


def _resolve_font_families_facet(
    typography: Typography,
    candidates: list[_SpanCandidate],
) -> tuple[Typography, bool, list[AlternateCandidate]]:
    """
    Resolve font-family labels independently from span candidates.

    Args:
        typography: Starting typography copied from the accepted span.
        candidates: Matched witness span candidates.

    Returns:
        Updated typography, conflict flag, and font-family alternates.

    """
    family_lists = [
        list(candidate.span.typography.font_families) for candidate in candidates
    ]
    non_empty = [families for families in family_lists if families]
    if not non_empty:
        return typography, False, []

    name_sets = [
        frozenset(family.name for family in families) for families in non_empty
    ]
    if len(set(name_sets)) == 1:
        typography.font_families = list(non_empty[0])
        return typography, False, []

    typography.font_families = []
    return (
        typography,
        True,
        _typography_alternates_for_facet("font_families", candidates),
    )


def _flagged_object_ids(flags: list[MergeFlag]) -> set[str]:
    """
    Collect object ids already referenced by merge flags.

    Args:
        flags: Merge flags emitted during the current run.

    Returns:
        Object ids appearing in any flag target list.

    """
    return {
        object_id
        for flag in flags
        for object_id in flag.target_object_ids
    }


def _iter_accepted_objects(
    regions: list[RegionRecord],
    lines: list[LineRecord],
    spans: list[SpanRecord],
    notes: list[NoteRecord],
) -> list[tuple[str, RegionRecord | LineRecord | SpanRecord | NoteRecord]]:
    """
    Pair accepted graph objects with their stable identifiers.

    Args:
        regions: Accepted region nodes under construction.
        lines: Accepted line nodes under construction.
        spans: Accepted span nodes under construction.
        notes: Accepted note nodes under construction.

    Returns:
        Object id and record pairs for confidence-floor evaluation.

    """
    objects: list[tuple[str, RegionRecord | LineRecord | SpanRecord | NoteRecord]] = []
    objects.extend((region.region_id, region) for region in regions)
    objects.extend((line.line_id, line) for line in lines)
    objects.extend((span.span_id, span) for span in spans)
    objects.extend((note.note_id, note) for note in notes)
    return objects


def _resolve_typography_enum_facets(
    typography: Typography,
    candidates: list[_SpanCandidate],
) -> tuple[Typography, bool, list[AlternateCandidate]]:
    """
    Resolve enum-like typography facets from span candidates.

    Args:
        typography: Starting typography copied from the accepted span.
        candidates: Matched witness span candidates.

    Returns:
        Updated typography, conflict flag, and enum facet alternates.

    """
    alternates: list[AlternateCandidate] = []
    conflict = False

    weight, weight_conflict, weight_alternates = _resolve_enum_facet(
        [candidate.span.typography.weight for candidate in candidates],
        FontWeight.UNKNOWN,
        "weight",
        candidates,
    )
    typography.weight = weight
    conflict = conflict or weight_conflict
    alternates.extend(weight_alternates)

    slant, slant_conflict, slant_alternates = _resolve_enum_facet(
        [candidate.span.typography.slant for candidate in candidates],
        FontSlant.UNKNOWN,
        "slant",
        candidates,
    )
    typography.slant = slant
    conflict = conflict or slant_conflict
    alternates.extend(slant_alternates)

    baseline, baseline_conflict, baseline_alternates = _resolve_enum_facet(
        [candidate.span.typography.baseline_shift for candidate in candidates],
        BaselineShift.UNKNOWN,
        "baseline_shift",
        candidates,
    )
    typography.baseline_shift = baseline
    conflict = conflict or baseline_conflict
    alternates.extend(baseline_alternates)

    return typography, conflict, alternates


def _resolve_typography_optional_facets(
    typography: Typography,
    candidates: list[_SpanCandidate],
) -> tuple[Typography, bool, list[AlternateCandidate]]:
    """
    Resolve optional boolean and float typography facets from span candidates.

    Args:
        typography: Starting typography copied from the accepted span.
        candidates: Matched witness span candidates.

    Returns:
        Updated typography, conflict flag, and optional facet alternates.

    """
    alternates: list[AlternateCandidate] = []
    conflict = False

    small_caps, small_caps_conflict, small_caps_alternates = (
        _resolve_optional_bool_facet(
            [candidate.span.typography.small_caps for candidate in candidates],
            "small_caps",
            candidates,
        )
    )
    typography.small_caps = small_caps
    conflict = conflict or small_caps_conflict
    alternates.extend(small_caps_alternates)

    letter_spaced, letter_conflict, letter_alternates = _resolve_optional_bool_facet(
        [candidate.span.typography.letter_spaced for candidate in candidates],
        "letter_spaced",
        candidates,
    )
    typography.letter_spaced = letter_spaced
    conflict = conflict or letter_conflict
    alternates.extend(letter_alternates)

    font_size, size_conflict, size_alternates = _resolve_optional_float_facet(
        [candidate.span.typography.font_size_points for candidate in candidates],
        "font_size_points",
        candidates,
    )
    typography.font_size_points = font_size
    conflict = conflict or size_conflict
    alternates.extend(size_alternates)

    return typography, conflict, alternates


def _resolve_enum_facet(
    values: list[Any],
    unknown_value: Any,
    facet_name: str,
    candidates: list[_SpanCandidate],
) -> tuple[Any, bool, list[AlternateCandidate]]:
    """
    Resolve one enum-like typography facet from candidate values.

    Args:
        values: Facet values collected from matched spans.
        unknown_value: Sentinel value meaning missing evidence.
        facet_name: Facet key stored in alternate payloads.
        candidates: Matched witness span candidates.

    Returns:
        Accepted facet value, conflict flag, and facet alternates.

    """
    known_values = [value for value in values if value != unknown_value]
    unique_values = set(known_values)
    if not unique_values:
        return unknown_value, False, []
    if len(unique_values) == 1:
        return next(iter(unique_values)), False, []
    return (
        unknown_value,
        True,
        _typography_alternates_for_facet(facet_name, candidates),
    )


def _resolve_optional_bool_facet(
    values: list[bool | None],
    facet_name: str,
    candidates: list[_SpanCandidate],
) -> tuple[bool | None, bool, list[AlternateCandidate]]:
    """
    Resolve one optional boolean typography facet from candidate values.

    Args:
        values: Facet values collected from matched spans.
        facet_name: Facet key stored in alternate payloads.
        candidates: Matched witness span candidates.

    Returns:
        Accepted facet value, conflict flag, and facet alternates.

    """
    known_values = [value for value in values if value is not None]
    unique_values = set(known_values)
    if not unique_values:
        return None, False, []
    if len(unique_values) == 1:
        return next(iter(unique_values)), False, []
    return None, True, _typography_alternates_for_facet(facet_name, candidates)


def _resolve_optional_float_facet(
    values: list[float | None],
    facet_name: str,
    candidates: list[_SpanCandidate],
) -> tuple[float | None, bool, list[AlternateCandidate]]:
    """
    Resolve one optional float typography facet from candidate values.

    Args:
        values: Facet values collected from matched spans.
        facet_name: Facet key stored in alternate payloads.
        candidates: Matched witness span candidates.

    Returns:
        Accepted facet value, conflict flag, and facet alternates.

    """
    known_values = [value for value in values if value is not None]
    unique_values = set(known_values)
    if not unique_values:
        return None, False, []
    if len(unique_values) == 1:
        return next(iter(unique_values)), False, []
    return None, True, _typography_alternates_for_facet(facet_name, candidates)


def _role_alternates_from_candidates(
    candidates: list[_SpanCandidate],
) -> list[AlternateCandidate]:
    """
    Serialize competing role lists as alternate candidates.

    Args:
        candidates: Matched witness span candidates.

    Returns:
        Alternate role payloads for each candidate.

    """
    return [
        AlternateCandidate(
            witness_id=candidate.witness_id,
            runner_id=candidate.runner_id,
            value_kind="role",
            value={
                "roles": [role.value for role in candidate.span.roles],
            },
            machine_confidence=candidate.span.provenance.machine_confidence,
        )
        for candidate in candidates
    ]


def _typography_alternates_for_facet(
    facet_name: str,
    candidates: list[_SpanCandidate],
) -> list[AlternateCandidate]:
    """
    Serialize typography facet payloads as alternate candidates.

    Args:
        facet_name: Facet key stored in alternate payloads.
        candidates: Matched witness span candidates.

    Returns:
        Alternate typography payloads for the supplied facet.

    """
    alternates: list[AlternateCandidate] = []
    for candidate in candidates:
        typography = candidate.span.typography
        alternates.append(
            AlternateCandidate(
                witness_id=candidate.witness_id,
                runner_id=candidate.runner_id,
                value_kind="typography",
                value={
                    "facet": facet_name,
                    "typography": typography.model_dump(mode="json"),
                },
                machine_confidence=candidate.span.provenance.machine_confidence,
            )
        )
    return alternates


def _collect_note_candidates(
    accepted_note: NoteRecord,
    scaffold_witness: PassWitnessPage,
    witnesses: list[PassWitnessPage],
    iou_threshold: float,
) -> list[_NoteCandidate]:
    """
    Gather matched note candidates from all eligible witnesses.

    Args:
        accepted_note: Accepted note copied from the scaffold layout.
        scaffold_witness: Witness chosen as the structure scaffold.
        witnesses: Eligible witnesses aligned to the prepared page.
        iou_threshold: Minimum IoU required for geometry matching.

    Returns:
        Matched note candidates from eligible witnesses.

    """
    candidates: list[_NoteCandidate] = []
    for witness in witnesses:
        matched_notes = _matching_notes_for_witness(
            accepted_note,
            scaffold_witness,
            witness,
            iou_threshold,
        )
        candidates.extend(
            _NoteCandidate(
                witness_id=witness.witness_id,
                runner_id=witness.runner_id,
                note=matched_note,
            )
            for matched_note in matched_notes
        )
    return candidates


def _matching_notes_for_witness(
    accepted_note: NoteRecord,
    scaffold_witness: PassWitnessPage,
    witness: PassWitnessPage,
    iou_threshold: float,
) -> list[NoteRecord]:
    """
    Find witness notes that align to one accepted scaffold note.

    Args:
        accepted_note: Accepted note copied from the scaffold layout.
        scaffold_witness: Witness chosen as the structure scaffold.
        witness: Witness fragment to search for matching notes.
        iou_threshold: Minimum IoU required for geometry matching.

    Returns:
        Matching notes from the supplied witness.

    """
    if witness.witness_id == scaffold_witness.witness_id:
        original = _note_by_id(witness, accepted_note.note_id)
        return [original] if original is not None else []

    if accepted_note.bounding_box is not None:
        return [
            note
            for note in witness.notes
            if note.bounding_box is not None
            and note.note_kind == accepted_note.note_kind
            and _box_iou(accepted_note.bounding_box, note.bounding_box)
            >= iou_threshold
        ]

    return []


def _map_marker_span_ids(
    marker_span_ids: list[str],
    context: _MarkerMappingContext,
) -> tuple[list[str], bool]:
    """
    Map witness-local marker span ids onto accepted scaffold span ids.

    Args:
        marker_span_ids: Marker span ids from one witness note.
        context: Witness and accepted-span mapping inputs.

    Returns:
        Accepted scaffold span ids and whether any marker mapping was ambiguous.

    """
    witness = context.witness
    mapped_ids: list[str] = []
    ambiguous = False
    for marker_span_id in marker_span_ids:
        marker_span = _span_by_id(witness, marker_span_id)
        if marker_span is None:
            continue
        matching_accepted_ids: list[str] = []
        for accepted_span in context.accepted_spans:
            matched = _matching_spans_for_witness(
                accepted_span,
                context.scaffold_witness,
                witness,
                context.iou_threshold,
            )
            if any(span.span_id == marker_span_id for span in matched):
                matching_accepted_ids.append(accepted_span.span_id)
        if len(matching_accepted_ids) > 1:
            ambiguous = True
        elif len(matching_accepted_ids) == 1:
            mapped_ids.append(matching_accepted_ids[0])
    return mapped_ids, ambiguous


def _note_link_alternates(
    candidates: list[_NoteCandidate],
    context: _NoteLinkResolutionContext,
) -> list[AlternateCandidate]:
    """
    Serialize note-link candidate sets as alternate provenance payloads.

    Args:
        candidates: Matched witness note candidates.
        context: Witness, span, and threshold inputs for note-link resolution.

    Returns:
        Alternate note-link payloads for ambiguous linkage.

    """
    alternates: list[AlternateCandidate] = []
    for candidate in candidates:
        witness = _witness_by_id(context.witnesses, candidate.witness_id)
        if witness is None:
            continue
        mapped_ids, _ = _map_marker_span_ids(
            candidate.note.linked_marker_span_ids,
            _MarkerMappingContext(
                witness=witness,
                scaffold_witness=context.scaffold_witness,
                accepted_spans=context.accepted_spans,
                iou_threshold=context.iou_threshold,
            ),
        )
        alternates.append(
            AlternateCandidate(
                witness_id=candidate.witness_id,
                runner_id=candidate.runner_id,
                value_kind="note_link",
                value={
                    "linked_marker_span_ids": mapped_ids
                    or list(candidate.note.linked_marker_span_ids)
                },
                machine_confidence=candidate.note.provenance.machine_confidence,
            )
        )
    return alternates


def _witness_by_id(
    witnesses: list[PassWitnessPage],
    witness_id: str,
) -> PassWitnessPage | None:
    """
    Return one witness page by identifier.

    Args:
        witnesses: Eligible witness fragments to search.
        witness_id: Witness artifact identifier to locate.

    Returns:
        Matching witness page, if present.

    """
    for witness in witnesses:
        if witness.witness_id == witness_id:
            return witness
    return None


def _span_by_id(witness: PassWitnessPage, span_id: str) -> SpanRecord | None:
    """
    Return one span from a witness by identifier.

    Args:
        witness: Witness fragment to search.
        span_id: Span identifier to locate.

    Returns:
        Matching span record, if present.

    """
    for span in witness.spans:
        if span.span_id == span_id:
            return span
    return None


def _note_by_id(witness: PassWitnessPage, note_id: str) -> NoteRecord | None:
    """
    Return one note from a witness by identifier.

    Args:
        witness: Witness fragment to search.
        note_id: Note identifier to locate.

    Returns:
        Matching note record, if present.

    """
    for note in witness.notes:
        if note.note_id == note_id:
            return note
    return None
