# Copyright (C) 2026 Chris Malek.
"""Map Spec 0009 merge flags onto Spec 0005 review task packets."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: TC003
from enum import Enum
from typing import TYPE_CHECKING

from wordwending.models import (
    BundlePage,
    EvaluationFlag,
    FlagSeverity,
    MergeFlag,
    MergeFlagType,
    PageEvaluationSummary,
    ReviewDimension,
    ReviewTask,
    StyleEvaluationSummary,
)

if TYPE_CHECKING:
    from wordwending.services.review_markup import HumanMarkupService

class _AdjudicationOnly(Enum):
    """Sentinel: merge flag type has no Spec 0005 dimension packet."""

    #: Marker value for adjudication-only merge flag types.
    MARKER = "adjudication-only"


#: Sentinel meaning force page-scoped adjudication (no dimension packet).
ADJUDICATION_ONLY = _AdjudicationOnly.MARKER

#: Spec 0009 merge flag types → Spec 0005 review dimensions (or adjudication).
_MERGE_FLAG_DIMENSION: dict[MergeFlagType, ReviewDimension | _AdjudicationOnly] = {
    MergeFlagType.TEXT_DISAGREEMENT: ReviewDimension.TEXT,
    MergeFlagType.ROLE_CONFLICT: ReviewDimension.TEXT,
    MergeFlagType.TYPOGRAPHY_CONFLICT: ReviewDimension.TYPOGRAPHY,
    MergeFlagType.NOTE_LINK_AMBIGUOUS: ReviewDimension.NOTE_LINKAGE,
    MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT: ReviewDimension.STRUCTURE,
    MergeFlagType.INSUFFICIENT_EVIDENCE: ADJUDICATION_ONLY,
}


def merge_flag_review_dimension(
    flag_type: str,
    *,
    family_dimension: ReviewDimension,
) -> ReviewDimension | _AdjudicationOnly:
    """
    Resolve the Spec 0005 dimension for one evaluation/merge flag type.

    Known Spec 0009 ``MergeFlagType`` values override the evaluation-family
    bucket so misplaced flags (for example all merge flags in ``text``) still
    build the correct packet. Unknown ``flag_type`` values keep the family
    dimension.

    Args:
        flag_type: Machine-readable evaluation or merge flag type.

    Keyword Args:
        family_dimension: Dimension implied by the evaluation-summary family
            that currently holds the flag.

    Returns:
        A review dimension, or ``ADJUDICATION_ONLY`` when no Spec 0005
        dimension packet exists for the flag type.

    """
    try:
        merge_type = MergeFlagType(flag_type)
    except ValueError:
        return family_dimension
    mapped = _MERGE_FLAG_DIMENSION.get(merge_type)
    if mapped is None:
        return family_dimension
    return mapped


def _evaluation_flags_from_merge(flags: Sequence[MergeFlag]) -> list[EvaluationFlag]:
    """
    Project Spec 0009 merge flags into Spec 0002 evaluation flag payloads.

    Args:
        flags: Merge flags emitted for one page.

    Returns:
        Evaluation flags suitable for ``evaluation/flags.json`` via
        ``PageEvaluationSummary``.

    """
    return [
        EvaluationFlag(
            flag_id=flag.flag_id,
            flag_type=str(flag.flag_type),
            severity=FlagSeverity.WARNING,
            message=flag.message,
            target_object_ids=list(flag.target_object_ids),
        )
        for flag in flags
    ]


def _family_key_for_dimension(
    dimension: ReviewDimension | _AdjudicationOnly,
) -> str:
    """
    Map a review dimension to a ``PageEvaluationSummary`` family key.

    Args:
        dimension: Spec 0005 dimension or adjudication-only sentinel.

    Returns:
        One of ``text``, ``structure``, ``typography``, or ``note_linkage``.

    """
    if dimension is ADJUDICATION_ONLY or dimension is ReviewDimension.TEXT:
        return "text"
    if dimension is ReviewDimension.STRUCTURE:
        return "structure"
    if dimension is ReviewDimension.TYPOGRAPHY:
        return "typography"
    if dimension is ReviewDimension.NOTE_LINKAGE:
        return "note_linkage"
    return "text"


class MergeFlagReviewService:
    """
    Project merge flags into evaluation families and Spec 0005 review packets.

    Uses existing ``ReviewTask`` models only (no shadow schema). Types without
    a Spec 0005 dimension packet (``insufficient_evidence``) collapse to
    adjudication via ``HumanMarkupService``.

    """

    def project_onto_page(
        self, page: BundlePage, flags: Sequence[MergeFlag]
    ) -> BundlePage:
        """
        Attach merge flags onto the correct page evaluation families.

        Args:
            page: Accepted page graph after witness rewrite.
            flags: Merge flags from ``MergePageResult``.

        Returns:
            Page whose evaluation summary families include projected flags
            (unchanged when ``flags`` is empty).

        """
        if not flags:
            return page
        buckets: dict[str, list[EvaluationFlag]] = {
            "text": [],
            "structure": [],
            "typography": [],
            "note_linkage": [],
        }
        for flag, evaluation_flag in zip(
            flags, _evaluation_flags_from_merge(flags), strict=True
        ):
            mapped = _MERGE_FLAG_DIMENSION[flag.flag_type]
            buckets[_family_key_for_dimension(mapped)].append(evaluation_flag)

        summary = page.evaluation_summary
        text = summary.text.model_copy(
            update={"flags": [*summary.text.flags, *buckets["text"]]}
        )
        structure = summary.structure.model_copy(
            update={"flags": [*summary.structure.flags, *buckets["structure"]]}
        )
        typography = summary.style.typography.model_copy(
            update={
                "flags": [
                    *summary.style.typography.flags,
                    *buckets["typography"],
                ]
            }
        )
        note_linkage = summary.style.note_linkage.model_copy(
            update={
                "flags": [
                    *summary.style.note_linkage.flags,
                    *buckets["note_linkage"],
                ]
            }
        )
        evaluation_summary = PageEvaluationSummary(
            text=text,
            structure=structure,
            style=StyleEvaluationSummary(
                typography=typography,
                note_linkage=note_linkage,
            ),
        )
        return page.model_copy(update={"evaluation_summary": evaluation_summary})

    def build_review_tasks(
        self,
        page: BundlePage,
        flags: Sequence[MergeFlag],
        *,
        markup: HumanMarkupService,
        run_id: str,
        graph_revision: str,
    ) -> list[ReviewTask]:
        """
        Build Spec 0005 review task packets from merge flags.

        Args:
            page: Accepted page graph supplying ids and image binding.
            flags: Merge flags to project and convert into review packets.

        Keyword Args:
            markup: Spec 0005 packet factory / queue builder.
            run_id: Machine run against which tasks were prepared.
            graph_revision: Accepted graph revision for the tasks.

        Returns:
            Sorted review tasks covering flagged merge disagreements.

        """
        projected = self.project_onto_page(page, flags)
        return markup.build_review_tasks(
            projected, run_id=run_id, graph_revision=graph_revision
        )
