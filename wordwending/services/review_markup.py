# Copyright (C) 2026 Chris Malek.
"""Evidence-bound human-review task packet construction."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from wordwending.models import (
    BundlePage,
    EvaluationFlag,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
)
from wordwending.services.merge_review import (
    ADJUDICATION_ONLY,
    merge_flag_review_dimension,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

#: Shared evidence slots after the dimension-specific raw witness (Spec 0005 items 4-7).
_EVIDENCE_TAIL: list[str] = [
    "independent-witnesses",
    "accepted-page-graph",
    "evaluation-and-prior-review",
    "decision-controls-and-checklist",
]


def _evidence_with_witness(dimension_witness: str) -> list[str]:
    """
    Build Spec 0005 evidence order with a dimension-specific item 3.

    Args:
        dimension_witness: Raw witness label for the dimension under review.

    Returns:
        Ordered required-evidence labels for a review packet.

    """
    return [
        "prepared-page-image",
        "scope-overlay",
        dimension_witness,
        *_EVIDENCE_TAIL,
    ]


#: Evidence sequence for diplomatic-text review.
_TEXT_REQUIRED_EVIDENCE: list[str] = _evidence_with_witness("raw-text-witnesses")

#: Evidence sequence for layout/structure review.
_LAYOUT_REQUIRED_EVIDENCE: list[str] = _evidence_with_witness(
    "raw-structure-witnesses"
)

#: Evidence sequence for typography review.
_TYPOGRAPHY_REQUIRED_EVIDENCE: list[str] = _evidence_with_witness(
    "raw-typography-witnesses"
)

#: Evidence sequence for note-linkage review.
_NOTE_LINKAGE_REQUIRED_EVIDENCE: list[str] = _evidence_with_witness(
    "raw-note-linkage-witnesses"
)

#: Evidence sequence for page-scoped source triage.
_SOURCE_TRIAGE_REQUIRED_EVIDENCE: list[str] = _evidence_with_witness(
    "raw-source-quality-evidence"
)

#: Evidence sequence for preparation review (source-vs-prepared + transforms).
_PREPARATION_REQUIRED_EVIDENCE: list[str] = [
    "source-vs-prepared-images",
    "scope-overlay",
    "checksum-and-transform-overlays",
    *_EVIDENCE_TAIL,
]

#: Evidence sequence for unknown-target adjudication.
_ADJUDICATION_REQUIRED_EVIDENCE: list[str] = _evidence_with_witness(
    "raw-flagged-dimension-witnesses"
)

#: Required evidence keyed by review task type.
_REQUIRED_EVIDENCE_BY_TYPE: dict[ReviewTaskType, list[str]] = {
    ReviewTaskType.TEXT: _TEXT_REQUIRED_EVIDENCE,
    ReviewTaskType.LAYOUT: _LAYOUT_REQUIRED_EVIDENCE,
    ReviewTaskType.TYPOGRAPHY: _TYPOGRAPHY_REQUIRED_EVIDENCE,
    ReviewTaskType.NOTE_LINKAGE: _NOTE_LINKAGE_REQUIRED_EVIDENCE,
    ReviewTaskType.SOURCE_TRIAGE: _SOURCE_TRIAGE_REQUIRED_EVIDENCE,
    ReviewTaskType.PREPARATION: _PREPARATION_REQUIRED_EVIDENCE,
    ReviewTaskType.ADJUDICATION: _ADJUDICATION_REQUIRED_EVIDENCE,
}

#: Actions permitted for diplomatic-text review.
_TEXT_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.ACCEPT,
    ReviewAction.CORRECT_TEXT,
    ReviewAction.MARK_ILLEGIBLE,
    ReviewAction.FLAG,
]

#: Actions permitted for layout/structure review.
_LAYOUT_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.ACCEPT,
    ReviewAction.CORRECT_GEOMETRY,
    ReviewAction.RECLASSIFY_REGION,
    ReviewAction.REORDER,
    ReviewAction.SPLIT_REGION,
    ReviewAction.MERGE_REGION,
    ReviewAction.FLAG,
]

#: Actions permitted for typography review.
_TYPOGRAPHY_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.ACCEPT,
    ReviewAction.CORRECT_STYLE,
    ReviewAction.FLAG,
]

#: Actions permitted for note-linkage review.
_NOTE_LINKAGE_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.ACCEPT,
    ReviewAction.LINK_NOTE,
    ReviewAction.UNLINK_NOTE,
    ReviewAction.FLAG,
]

#: Actions permitted for page-scoped source triage.
_SOURCE_TRIAGE_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.ACCEPT,
    ReviewAction.DECIDE_SOURCE_TRIAGE,
    ReviewAction.FLAG,
]

#: Actions permitted for page-scoped preparation review.
_PREPARATION_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.ACCEPT,
    ReviewAction.DECIDE_PREPARATION,
    ReviewAction.FLAG,
]

#: Actions permitted for page-scoped adjudication of unknown flag targets.
#: ACCEPT is intentionally omitted: unknown/empty targets cannot be accepted
#: without inventing object ids or upgrading trust across dimensions/scopes.
_ADJUDICATION_ALLOWED_ACTIONS: list[ReviewAction] = [
    ReviewAction.FLAG,
]

#: Concrete question the operator must answer for text review.
_TEXT_QUESTION = (
    "Does the diplomatic text for the target spans match the prepared "
    "page image character by character?"
)

#: Concrete question the operator must answer for layout review.
_LAYOUT_QUESTION = (
    "Do the target regions have correct boundaries, classification, "
    "containment, and reading order against the prepared page image?"
)

#: Concrete question the operator must answer for typography review.
_TYPOGRAPHY_QUESTION = (
    "Do the typography facets for the target spans match the prepared "
    "page image?"
)

#: Concrete question the operator must answer for note-linkage review.
_NOTE_LINKAGE_QUESTION = (
    "Does the marker-to-note linkage for the target note match the "
    "prepared page image?"
)

#: Concrete question the operator must answer for source triage.
_SOURCE_TRIAGE_QUESTION = (
    "After whole-page and small-font inspection with the prepared-image "
    "checksum visible, is this acquired page usable, usable-with-warning, "
    "needing reprepare, or requiring reacquire?"
)

#: Concrete question the operator must answer for preparation review.
_PREPARATION_QUESTION = (
    "With transform overlays and the prepared-image checksum visible, "
    "and after whole-page plus small-font inspection, should this page "
    "use full-page preparation or subdivide?"
)

#: Concrete question for adjudication of empty or unknown flag targets.
_ADJUDICATION_QUESTION = (
    "After re-inspecting the prepared page image with checksum evidence "
    "visible, should each empty or unknown flagged target be flagged or "
    "abstained without inventing missing object ids?"
)

#: Observable completion check for diplomatic-text review.
_TEXT_COMPLETION_CRITERIA: list[str] = [
    "every grapheme in scope was inspected against the prepared image",
]

#: Observable completion check for layout review.
_LAYOUT_COMPLETION_CRITERIA: list[str] = [
    (
        "every region in scope has resolved containment, geometry, and order "
        "or an explicit unresolved flag"
    ),
]

#: Observable completion check for typography review.
_TYPOGRAPHY_COMPLETION_CRITERIA: list[str] = [
    (
        "each required typography facet is selected, explicitly unknown, "
        "or covered by an abstention"
    ),
]

#: Observable completion check for note-linkage review.
_NOTE_LINKAGE_COMPLETION_CRITERIA: list[str] = [
    (
        "marker and note body were reviewed separately and every asserted "
        "link resolves to existing object ids"
    ),
]

#: Observable completion check for source triage.
_SOURCE_TRIAGE_COMPLETION_CRITERIA: list[str] = [
    (
        "whole-page and at least one small-font area were inspected with "
        "checksum evidence visible, and a disposition or abstention recorded"
    ),
]

#: Observable completion check for preparation review.
_PREPARATION_COMPLETION_CRITERIA: list[str] = [
    (
        "transform chain and image checksum remained visible while choosing "
        "full-page or subdivision, or an abstention was recorded"
    ),
]

#: Observable completion check for unknown-target adjudication.
_ADJUDICATION_COMPLETION_CRITERIA: list[str] = [
    (
        "every empty or unknown flagged target was flagged or abstained with "
        "prepared-image checksum evidence visible"
    ),
]


class _FlagTargetBuckets:
    """Mutable accumulator for flag-driven queue grouping."""

    def __init__(self) -> None:
        """Initialize empty primary, related, and adjudication buckets."""
        #: Compatible primary targets keyed by evaluation family dimension.
        self.primary: dict[ReviewDimension, set[str]] = defaultdict(set)
        #: Marker span ids related to note-linkage primary targets.
        self.note_related: set[str] = set()
        #: Unknown or incompatible flagged object ids.
        self.unknown: set[str] = set()
        #: Dimensions whose flags required page-scoped adjudication.
        self.adjudication_dimensions: set[ReviewDimension] = set()
        #: Whether at least one empty or unknown flag target was seen.
        self.needs_adjudication: bool = False


class HumanMarkupService:
    """
    Build evidence-bound, dimension-specific review task packets.

    Constructor receives current guideline identity and calibration examples
    from orchestration; this service never invents review guidance.

    Args:
        guideline_id: Review guideline family governing constructed tasks.
        guideline_version: Exact guideline revision shown to the operator.
        calibration_example_ids: Calibration examples available for comparison.

    """

    def __init__(
        self,
        guideline_id: str,
        guideline_version: str,
        calibration_example_ids: Sequence[str] = (),
    ) -> None:
        """
        Bind immutable review guidance used for every constructed packet.

        Args:
            guideline_id: Review guideline family governing constructed tasks.
            guideline_version: Exact guideline revision shown to the operator.
            calibration_example_ids: Calibration examples available for comparison.

        Raises:
            ValueError: If guideline id or version is missing or blank.

        """
        if not guideline_id or not guideline_id.strip():
            msg = "guideline_id must be a non-blank string"
            raise ValueError(msg)
        if not guideline_version or not guideline_version.strip():
            msg = "guideline_version must be a non-blank string"
            raise ValueError(msg)
        #: Review guideline family governing constructed tasks.
        self.guideline_id = guideline_id
        #: Exact guideline revision shown to the operator.
        self.guideline_version = guideline_version
        #: Calibration examples available for comparison.
        self.calibration_example_ids = list(calibration_example_ids)

    def create_text_task(
        self,
        page: BundlePage,
        target_object_ids: list[str],
        *,
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a span-scoped diplomatic-text review task packet.

        Task identity is scoped to ``(page, task_type, targets)`` only and is
        independent of ``run_id`` / ``graph_revision``.

        Args:
            page: Accepted page graph supplying span ids and image binding.
            target_object_ids: Span ids the operator must inspect.

        Keyword Args:
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A self-contained text review task bound to the prepared image.

        Raises:
            ValueError: If targets are empty or any target id is not a page span.

        """
        self._require_known_ids(
            target_object_ids,
            {span.span_id for span in page.spans},
            "text review targets must be span ids",
        )
        return self._build_task(
            page,
            task_type=ReviewTaskType.TEXT,
            dimensions=[ReviewDimension.TEXT],
            target_scope=ReviewScope.SPAN,
            target_object_ids=target_object_ids,
            question=_TEXT_QUESTION,
            allowed_actions=_TEXT_ALLOWED_ACTIONS,
            completion_criteria=_TEXT_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def create_layout_task(
        self,
        page: BundlePage,
        target_object_ids: list[str],
        *,
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a region-scoped layout/structure review task packet.

        Split and merge work requires every source region id in task scope.

        Args:
            page: Accepted page graph supplying region ids and image binding.
            target_object_ids: Region ids the operator must inspect.

        Keyword Args:
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A self-contained layout review task bound to the prepared image.

        Raises:
            ValueError: If targets are empty or any target id is not a page region.

        """
        self._require_known_ids(
            target_object_ids,
            {region.region_id for region in page.regions},
            "layout review targets must be region ids",
        )
        return self._build_task(
            page,
            task_type=ReviewTaskType.LAYOUT,
            dimensions=[ReviewDimension.STRUCTURE],
            target_scope=ReviewScope.REGION,
            target_object_ids=target_object_ids,
            question=_LAYOUT_QUESTION,
            allowed_actions=_LAYOUT_ALLOWED_ACTIONS,
            completion_criteria=_LAYOUT_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def create_typography_task(
        self,
        page: BundlePage,
        target_object_ids: list[str],
        *,
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a span-scoped typography review task packet.

        Typography certification is independent of diplomatic-text review.

        Args:
            page: Accepted page graph supplying span ids and image binding.
            target_object_ids: Span ids the operator must inspect.

        Keyword Args:
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A self-contained typography review task bound to the prepared image.

        Raises:
            ValueError: If targets are empty or any target id is not a page span.

        """
        self._require_known_ids(
            target_object_ids,
            {span.span_id for span in page.spans},
            "typography review targets must be span ids",
        )
        return self._build_task(
            page,
            task_type=ReviewTaskType.TYPOGRAPHY,
            dimensions=[ReviewDimension.TYPOGRAPHY],
            target_scope=ReviewScope.SPAN,
            target_object_ids=target_object_ids,
            question=_TYPOGRAPHY_QUESTION,
            allowed_actions=_TYPOGRAPHY_ALLOWED_ACTIONS,
            completion_criteria=_TYPOGRAPHY_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def create_note_linkage_task(
        self,
        page: BundlePage,
        target_object_ids: list[str],
        *,
        related_object_ids: Sequence[str] = (),
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a note-scoped linkage review task packet.

        Primary targets are note ids. Marker span ids belong in
        ``related_object_ids`` and do not become primary trust targets.

        Args:
            page: Accepted page graph supplying note and span ids.
            target_object_ids: Note ids the operator must inspect.

        Keyword Args:
            related_object_ids: Marker span ids linked or candidate for linking.
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A self-contained note-linkage review task bound to the prepared image.

        Raises:
            ValueError: If note or related marker ids are missing or unknown.

        """
        self._require_known_ids(
            target_object_ids,
            {note.note_id for note in page.notes},
            "note-linkage review targets must be note ids",
        )
        related = list(related_object_ids)
        if related:
            self._require_known_ids(
                related,
                {span.span_id for span in page.spans},
                "note-linkage related_object_ids must be span ids",
            )
        return self._build_task(
            page,
            task_type=ReviewTaskType.NOTE_LINKAGE,
            dimensions=[ReviewDimension.NOTE_LINKAGE],
            target_scope=ReviewScope.NOTE,
            target_object_ids=target_object_ids,
            related_object_ids=related,
            question=_NOTE_LINKAGE_QUESTION,
            allowed_actions=_NOTE_LINKAGE_ALLOWED_ACTIONS,
            completion_criteria=_NOTE_LINKAGE_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def create_source_triage_task(
        self,
        page: BundlePage,
        *,
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a page-scoped source-quality triage task packet.

        Args:
            page: Accepted page graph supplying page id and image binding.

        Keyword Args:
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A self-contained source-triage task bound to the prepared image.

        """
        return self._build_task(
            page,
            task_type=ReviewTaskType.SOURCE_TRIAGE,
            dimensions=[ReviewDimension.SOURCE_QUALITY],
            target_scope=ReviewScope.PAGE,
            target_object_ids=[page.page_id],
            question=_SOURCE_TRIAGE_QUESTION,
            allowed_actions=_SOURCE_TRIAGE_ALLOWED_ACTIONS,
            completion_criteria=_SOURCE_TRIAGE_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def create_preparation_task(
        self,
        page: BundlePage,
        *,
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a page-scoped preparation / subdivision task packet.

        Args:
            page: Accepted page graph supplying page id and image binding.

        Keyword Args:
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A self-contained preparation task bound to the prepared image.

        """
        return self._build_task(
            page,
            task_type=ReviewTaskType.PREPARATION,
            dimensions=[ReviewDimension.PREPARATION],
            target_scope=ReviewScope.PAGE,
            target_object_ids=[page.page_id],
            question=_PREPARATION_QUESTION,
            allowed_actions=_PREPARATION_ALLOWED_ACTIONS,
            completion_criteria=_PREPARATION_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def create_adjudication_flag_task(
        self,
        page: BundlePage,
        *,
        dimensions: Sequence[ReviewDimension],
        related_object_ids: Sequence[str] = (),
        run_id: str,
        graph_revision: str,
    ) -> ReviewTask:
        """
        Build a page-scoped adjudication task for empty or unknown flag targets.

        Args:
            page: Accepted page graph supplying page id and image binding.

        Keyword Args:
            dimensions: Evaluation families whose flags could not be targeted.
            related_object_ids: Unknown flagged ids preserved for the operator.
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.

        Returns:
            A page-scoped adjudication packet allowing only flag (plus abstention).

        Raises:
            ValueError: If ``dimensions`` is empty.

        """
        if not dimensions:
            msg = "adjudication flag tasks require at least one dimension"
            raise ValueError(msg)
        # Page id is already the primary target; overlapping related ids
        # would fail ReviewTask related/target validation.
        safe_related = sorted(
            {
                object_id
                for object_id in related_object_ids
                if object_id and object_id != page.page_id
            }
        )
        return self._build_task(
            page,
            task_type=ReviewTaskType.ADJUDICATION,
            dimensions=sorted(dimensions, key=lambda item: item.value),
            target_scope=ReviewScope.PAGE,
            target_object_ids=[page.page_id],
            related_object_ids=safe_related,
            question=_ADJUDICATION_QUESTION,
            allowed_actions=_ADJUDICATION_ALLOWED_ACTIONS,
            completion_criteria=_ADJUDICATION_COMPLETION_CRITERIA,
            run_id=run_id,
            graph_revision=graph_revision,
        )

    def build_review_tasks(
        self,
        page: BundlePage,
        *,
        run_id: str,
        graph_revision: str,
    ) -> list[ReviewTask]:
        """
        Derive a deterministic review queue from page evaluation flags.

        Flags are flattened from ``PageEvaluationSummary`` families. Compatible
        targets of one dimension and scope are grouped into one factory packet;
        empty or unknown targets collapse into one page-scoped adjudication
        task. Nothing is persisted.

        Args:
            page: Accepted page graph whose evaluation flags drive the queue.

        Keyword Args:
            run_id: Machine run against which tasks were prepared.
            graph_revision: Accepted graph revision for the tasks.

        Returns:
            Sorted review tasks covering every flagged object id.

        """
        buckets = self._flag_target_buckets(page)
        tasks = self._tasks_from_buckets(
            page, buckets, run_id=run_id, graph_revision=graph_revision
        )
        tasks.sort(
            key=lambda task: (
                [dimension.value for dimension in task.dimensions],
                task.target_scope.value,
                list(task.target_object_ids),
            )
        )
        return tasks

    def _tasks_from_buckets(
        self,
        page: BundlePage,
        buckets: _FlagTargetBuckets,
        *,
        run_id: str,
        graph_revision: str,
    ) -> list[ReviewTask]:
        """
        Build unsorted packets from classified flag-target buckets.

        Args:
            page: Accepted page graph supplying ids and image binding.
            buckets: Compatible targets and adjudication inputs.

        Keyword Args:
            run_id: Machine run against which tasks were prepared.
            graph_revision: Accepted graph revision for the tasks.

        Returns:
            Review tasks for non-empty dimension buckets plus adjudication.

        """
        tasks = self._dimension_tasks_from_buckets(
            page, buckets, run_id=run_id, graph_revision=graph_revision
        )
        if not buckets.primary[ReviewDimension.NOTE_LINKAGE] and buckets.note_related:
            buckets.unknown.update(buckets.note_related)
            buckets.adjudication_dimensions.add(ReviewDimension.NOTE_LINKAGE)
            buckets.needs_adjudication = True
        if buckets.needs_adjudication:
            tasks.append(
                self.create_adjudication_flag_task(
                    page,
                    dimensions=sorted(
                        buckets.adjudication_dimensions,
                        key=lambda item: item.value,
                    ),
                    related_object_ids=sorted(buckets.unknown),
                    run_id=run_id,
                    graph_revision=graph_revision,
                )
            )
        return tasks

    def _dimension_tasks_from_buckets(
        self,
        page: BundlePage,
        buckets: _FlagTargetBuckets,
        *,
        run_id: str,
        graph_revision: str,
    ) -> list[ReviewTask]:
        """
        Emit dimension-specific packets for non-empty compatible target sets.

        Args:
            page: Accepted page graph supplying ids and image binding.
            buckets: Compatible primary and note-related targets.

        Keyword Args:
            run_id: Machine run against which tasks were prepared.
            graph_revision: Accepted graph revision for the tasks.

        Returns:
            Dimension factory packets for text, layout, typography, and notes.

        """
        tasks: list[ReviewTask] = []
        text_ids = sorted(buckets.primary[ReviewDimension.TEXT])
        if text_ids:
            tasks.append(
                self.create_text_task(
                    page, text_ids, run_id=run_id, graph_revision=graph_revision
                )
            )
        region_ids = sorted(buckets.primary[ReviewDimension.STRUCTURE])
        if region_ids:
            tasks.append(
                self.create_layout_task(
                    page, region_ids, run_id=run_id, graph_revision=graph_revision
                )
            )
        typography_ids = sorted(buckets.primary[ReviewDimension.TYPOGRAPHY])
        if typography_ids:
            tasks.append(
                self.create_typography_task(
                    page,
                    typography_ids,
                    run_id=run_id,
                    graph_revision=graph_revision,
                )
            )
        note_ids = sorted(buckets.primary[ReviewDimension.NOTE_LINKAGE])
        if note_ids:
            tasks.append(
                self.create_note_linkage_task(
                    page,
                    note_ids,
                    related_object_ids=sorted(buckets.note_related),
                    run_id=run_id,
                    graph_revision=graph_revision,
                )
            )
        return tasks

    def _flag_target_buckets(self, page: BundlePage) -> _FlagTargetBuckets:
        """
        Classify evaluation-flag targets into dimension buckets.

        Args:
            page: Accepted page graph supplying ids and evaluation flags.

        Returns:
            Compatible primary targets, note-related spans, and adjudication
            inputs for empty or unknown ids.

        """
        span_ids = {span.span_id for span in page.spans}
        region_ids = {region.region_id for region in page.regions}
        note_ids = {note.note_id for note in page.notes}
        buckets = _FlagTargetBuckets()
        summary = page.evaluation_summary
        families: list[tuple[ReviewDimension, list[EvaluationFlag]]] = [
            (ReviewDimension.TEXT, summary.text.flags),
            (ReviewDimension.STRUCTURE, summary.structure.flags),
            (ReviewDimension.TYPOGRAPHY, summary.style.typography.flags),
            (ReviewDimension.NOTE_LINKAGE, summary.style.note_linkage.flags),
        ]
        for dimension, flags in families:
            for flag in flags:
                self._classify_flag_targets(
                    flag,
                    dimension,
                    span_ids=span_ids,
                    region_ids=region_ids,
                    note_ids=note_ids,
                    buckets=buckets,
                )
        return buckets

    @staticmethod
    def _classify_flag_targets(  # noqa: PLR0913
        flag: EvaluationFlag,
        dimension: ReviewDimension,
        *,
        span_ids: set[str],
        region_ids: set[str],
        note_ids: set[str],
        buckets: _FlagTargetBuckets,
    ) -> None:
        """
        Route one flag's target ids into compatible or adjudication buckets.

        Known Spec 0009 merge ``flag_type`` values override the evaluation
        family dimension so misplaced merge flags still map to the correct
        Spec 0005 packet. Types without a dimension packet collapse to
        adjudication.

        Args:
            flag: Evaluation flag whose targets are classified.
            dimension: Family dimension that emitted the flag.

        Keyword Args:
            span_ids: Known span identifiers on the page.
            region_ids: Known region identifiers on the page.
            note_ids: Known note identifiers on the page.
            buckets: Mutable accumulator for grouped queue inputs.

        """
        resolved = merge_flag_review_dimension(
            flag.flag_type, family_dimension=dimension
        )
        if resolved is ADJUDICATION_ONLY:
            buckets.needs_adjudication = True
            buckets.adjudication_dimensions.add(dimension)
            for object_id in flag.target_object_ids:
                if object_id and object_id.strip():
                    buckets.unknown.add(object_id)
            return
        dimension = resolved
        if not flag.target_object_ids:
            buckets.needs_adjudication = True
            buckets.adjudication_dimensions.add(dimension)
            return
        for object_id in flag.target_object_ids:
            if not object_id or not object_id.strip():
                buckets.needs_adjudication = True
                buckets.adjudication_dimensions.add(dimension)
                continue
            if dimension is ReviewDimension.NOTE_LINKAGE:
                if object_id in note_ids:
                    buckets.primary[dimension].add(object_id)
                elif object_id in span_ids:
                    buckets.note_related.add(object_id)
                else:
                    buckets.needs_adjudication = True
                    buckets.unknown.add(object_id)
                    buckets.adjudication_dimensions.add(dimension)
                continue
            known = (
                span_ids
                if dimension
                in {ReviewDimension.TEXT, ReviewDimension.TYPOGRAPHY}
                else region_ids
            )
            if object_id in known:
                buckets.primary[dimension].add(object_id)
            else:
                buckets.needs_adjudication = True
                buckets.unknown.add(object_id)
                buckets.adjudication_dimensions.add(dimension)

    def _build_task(  # noqa: PLR0913
        self,
        page: BundlePage,
        *,
        task_type: ReviewTaskType,
        dimensions: list[ReviewDimension],
        target_scope: ReviewScope,
        target_object_ids: list[str],
        question: str,
        allowed_actions: list[ReviewAction],
        completion_criteria: list[str],
        run_id: str,
        graph_revision: str,
        related_object_ids: Sequence[str] = (),
    ) -> ReviewTask:
        """
        Assemble a dimension-specific packet with typed evidence binding.

        Args:
            page: Accepted page graph supplying the prepared-image checksum.

        Keyword Args:
            task_type: Review workflow represented by the task.
            dimensions: Exclusive trust dimensions certified by the task.
            target_scope: Scope shared by the primary targets.
            target_object_ids: Primary graph object ids in scope.
            question: Concrete question the operator must answer.
            allowed_actions: Actions the review interface may offer.
            completion_criteria: Observable checks required for completion.
            run_id: Machine run against which the task was prepared.
            graph_revision: Accepted graph revision for the task.
            related_object_ids: Related ids that contextualize targets.

        Returns:
            A self-contained review task bound to the prepared image.

        """
        task_id = self._task_id(page.page_id, task_type, target_object_ids)
        required_evidence = _REQUIRED_EVIDENCE_BY_TYPE[task_type]
        return ReviewTask(
            task_id=task_id,
            task_type=task_type,
            dimensions=list(dimensions),
            target_scope=target_scope,
            target_object_ids=list(target_object_ids),
            related_object_ids=list(related_object_ids),
            question=question,
            required_evidence=list(required_evidence),
            allowed_actions=list(allowed_actions),
            completion_criteria=list(completion_criteria),
            guideline_id=self.guideline_id,
            guideline_version=self.guideline_version,
            calibration_example_ids=list(self.calibration_example_ids),
            base_run_id=run_id,
            base_graph_revision=graph_revision,
            prepared_image_checksum=page.prepared_page.image_checksum,
            supports_abstention=True,
        )

    @staticmethod
    def _require_known_ids(
        object_ids: Sequence[str],
        known_ids: set[str],
        message_prefix: str,
    ) -> None:
        """
        Reject empty or unknown object identifiers for a packet factory.

        Args:
            object_ids: Candidate identifiers supplied by the caller.
            known_ids: Identifiers present on the accepted page graph.
            message_prefix: Human-readable prefix for validation errors.

        Raises:
            ValueError: If the id list is empty or contains unknown ids.

        """
        if not object_ids:
            msg = f"{message_prefix}; must not be empty"
            raise ValueError(msg)
        unknown = [
            object_id for object_id in object_ids if object_id not in known_ids
        ]
        if unknown:
            msg = f"{message_prefix}; unknown: {unknown}"
            raise ValueError(msg)

    @staticmethod
    def _task_id(
        page_id: str,
        task_type: ReviewTaskType,
        target_object_ids: Sequence[str],
    ) -> str:
        """
        Build a deterministic task id from page, type, and target ids.

        Identity is scoped to ``(page, task_type, targets)`` only; run and
        graph revision do not participate.

        Args:
            page_id: Owning page identifier.
            task_type: Review workflow represented by the task.
            target_object_ids: Ordered target object identifiers.

        Returns:
            Stable task id derived only from supplied identifiers.

        """
        targets = ",".join(target_object_ids)
        return f"{page_id}:{task_type.value}:{targets}"
