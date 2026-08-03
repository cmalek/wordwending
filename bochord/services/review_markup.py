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

#: Fixed evidence presentation order for every text-review packet.
_TEXT_REQUIRED_EVIDENCE: list[str] = [
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

#: Concrete question the operator must answer for text review.
_TEXT_QUESTION = (
    "Does the diplomatic text for the target spans match the prepared "
    "page image character by character?"
)

#: Observable completion check for diplomatic-text review.
_TEXT_COMPLETION_CRITERIA: list[str] = [
    "every grapheme in scope was inspected against the prepared image",
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
        if not target_object_ids:
            msg = "target_object_ids must not be empty"
            raise ValueError(msg)
        span_ids = {span.span_id for span in page.spans}
        unknown = [
            object_id
            for object_id in target_object_ids
            if object_id not in span_ids
        ]
        if unknown:
            msg = f"text review targets must be span ids; unknown: {unknown}"
            raise ValueError(msg)
        task_type = ReviewTaskType.TEXT
        task_id = self._task_id(page.page_id, task_type, target_object_ids)
        return ReviewTask(
            task_id=task_id,
            task_type=task_type,
            dimensions=[ReviewDimension.TEXT],
            target_scope=ReviewScope.SPAN,
            target_object_ids=list(target_object_ids),
            question=_TEXT_QUESTION,
            required_evidence=list(_TEXT_REQUIRED_EVIDENCE),
            allowed_actions=list(_TEXT_ALLOWED_ACTIONS),
            completion_criteria=list(_TEXT_COMPLETION_CRITERIA),
            guideline_id=self.guideline_id,
            guideline_version=self.guideline_version,
            calibration_example_ids=list(self.calibration_example_ids),
            base_run_id=run_id,
            base_graph_revision=graph_revision,
            prepared_image_checksum=page.prepared_page.image_checksum,
        )

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
