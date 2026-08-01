# Copyright (C) 2026 Chris Malek.
"""Abstaining single-page merge orchestration and facade."""

from __future__ import annotations

from typing import Any

from bochord.models import (
    AlternateCandidate,
    BoundingBox,
    BundlePage,
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
)
from bochord.services.text_normalization import (
    DEFAULT_TEXT_NORMALIZATION_POLICY,
    TextNormalizer,
)


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
        expected_id = self._prepared_page.prepared_page_id
        self._eligible_witnesses = []
        self._skipped_witnesses = []
        for witness in self._page_input.witnesses:
            if witness.prepared_page_id == expected_id:
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
                self._add_flag(
                    MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT,
                    target_object_ids=[
                        region.region_id for region in scaffold_witness.regions
                    ],
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
        if self._regions:
            self._regions = _attach_region_alternates(
                self._regions,
                self._skipped_witnesses,
                self._geometry_alternates,
            )

    def _merge_text(self) -> None:
        """Stub text merge: scaffold spans remain accepted until Task 3."""

    def _merge_typography(self) -> None:
        """Stub typography merge until Task 3."""

    def _merge_notes(self) -> None:
        """Stub note linkage merge until Task 3."""

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


def _attach_region_alternates(
    regions: list[RegionRecord],
    skipped_witnesses: list[PassWitnessPage],
    geometry_alternates: list[AlternateCandidate],
) -> list[RegionRecord]:
    """
    Attach skipped and geometry alternates to the first accepted region.

    Args:
        regions: Accepted region nodes copied from the scaffold.
        skipped_witnesses: Cross-variant witnesses excluded from merge.
        geometry_alternates: Losing geometry payloads from scaffold conflicts.

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
                "reason": "cross_variant_excluded",
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
