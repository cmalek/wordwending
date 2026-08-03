# Copyright (C) 2026 Chris Malek.
"""Evidence-bound human-review task packet construction."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bochord.models import (
    BundlePage,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

#: Fixed evidence presentation order for every review packet.
_REQUIRED_EVIDENCE: list[str] = [
    "prepared-page-image",
    "scope-overlay",
    "raw-text-witnesses",
    "independent-witnesses",
    "accepted-page-graph",
    "evaluation-and-prior-review",
    "decision-controls-and-checklist",
]

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
        Assemble a dimension-specific packet with shared evidence binding.

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
        return ReviewTask(
            task_id=task_id,
            task_type=task_type,
            dimensions=list(dimensions),
            target_scope=target_scope,
            target_object_ids=list(target_object_ids),
            related_object_ids=list(related_object_ids),
            question=question,
            required_evidence=list(_REQUIRED_EVIDENCE),
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
