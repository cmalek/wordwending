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
        candidates = [
            witness
            for witness in self._eligible_witnesses
            if witness.regions or witness.lines
        ]
        if not candidates:
            self._scaffold_witness = None
            return

        if self._policy.structure_scaffold_runner_ids:
            by_runner = {witness.runner_id: witness for witness in candidates}
            for runner_id in self._policy.structure_scaffold_runner_ids:
                witness = by_runner.get(runner_id)
                if witness is not None:
                    self._scaffold_witness = witness
                    break
            else:
                self._scaffold_witness = candidates[0]
        else:
            self._scaffold_witness = max(
                candidates,
                key=lambda witness: (
                    _coordinate_rich_line_count(witness),
                    -self._eligible_witnesses.index(witness),
                ),
            )

        scaffold_witness = self._scaffold_witness
        if scaffold_witness is None:
            return
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

        scaffold = self._scaffold_witness
        merge_provenance = ObjectProvenance(
            source_page_id=self._page_input.page_id,
            witness_ids=[scaffold.witness_id],
            runner_ids=[scaffold.runner_id],
            machine_confidence=scaffold.machine_confidence,
        )
        self._regions = [
            region.model_copy(
                update={"provenance": merge_provenance.model_copy(deep=True)},
                deep=True,
            )
            for region in scaffold.regions
        ]
        self._lines = [
            line.model_copy(
                update={"provenance": merge_provenance.model_copy(deep=True)},
                deep=True,
            )
            for line in scaffold.lines
        ]
        self._spans = [
            span.model_copy(
                update={"provenance": merge_provenance.model_copy(deep=True)},
                deep=True,
            )
            for span in scaffold.spans
        ]
        self._notes = [
            note.model_copy(
                update={"provenance": merge_provenance.model_copy(deep=True)},
                deep=True,
            )
            for note in scaffold.notes
        ]
        if self._regions:
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
                for witness in self._skipped_witnesses
            ]
            alternates.extend(self._geometry_alternates)
            if alternates:
                region = self._regions[0]
                provenance = region.provenance.model_copy(deep=True)
                provenance.alternate_candidates.extend(alternates)
                self._regions[0] = region.model_copy(
                    update={"provenance": provenance},
                    deep=True,
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
    scaffold_sorted = sorted(
        scaffold_regions,
        key=lambda region: region.reading_order_index,
    )
    witness_sorted = sorted(
        witness_regions,
        key=lambda region: region.reading_order_index,
    )
    if len(scaffold_sorted) != len(witness_sorted):
        return True, _geometry_alternates_for_regions(
            witness_sorted,
            witness_id=witness_id,
            runner_id=runner_id,
        )

    scaffold_has_boxes = any(
        region.bounding_box is not None for region in scaffold_sorted
    )
    witness_has_boxes = any(
        region.bounding_box is not None for region in witness_sorted
    )
    if not scaffold_has_boxes and not witness_has_boxes:
        return False, []
    if scaffold_has_boxes != witness_has_boxes:
        return True, _geometry_alternates_for_regions(
            witness_sorted,
            witness_id=witness_id,
            runner_id=runner_id,
        )

    used: set[int] = set()
    for scaffold_region in scaffold_sorted:
        if scaffold_region.bounding_box is None:
            continue
        best_index: int | None = None
        best_iou = 0.0
        for index, witness_region in enumerate(witness_sorted):
            if index in used or witness_region.bounding_box is None:
                continue
            iou = _box_iou(scaffold_region.bounding_box, witness_region.bounding_box)
            if iou >= iou_threshold and iou > best_iou:
                best_iou = iou
                best_index = index
        if best_index is None:
            return True, _geometry_alternates_for_regions(
                witness_sorted,
                witness_id=witness_id,
                runner_id=runner_id,
            )
        used.add(best_index)
    return False, []


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
