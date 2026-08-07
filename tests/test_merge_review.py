# Copyright (C) 2026 Chris Malek.
"""Tests mapping Spec 0009 merge flags to Spec 0005 review task packets."""

from __future__ import annotations

import pytest

from wordwending.models import (
    BundlePage,
    CoordinateSpace,
    EvaluationFamilySummary,
    EvaluationFlag,
    FlagSeverity,
    LineRecord,
    MergeFlag,
    MergeFlagType,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PageEvaluationSummary,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewDimension,
    ReviewTaskType,
    SpanRecord,
    WitnessReference,
)
from wordwending.services.merge_review import (
    _MERGE_FLAG_DIMENSION,
    MergeFlagReviewService,
)
from wordwending.services.review_markup import HumanMarkupService


def _provenance() -> ObjectProvenance:
    """Return minimal provenance for graph fixtures."""
    return ObjectProvenance(
        source_page_id="page-1",
        witness_ids=["wit-1"],
        runner_ids=["runner-1"],
    )


@pytest.fixture
def page() -> BundlePage:
    """Return a page graph with regions, spans, and a note for packet targeting."""
    provenance = _provenance()
    return BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=PreparedPage(
            prepared_page_id="prepared-page-1",
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
            preparation_recipe_digest="digest-prep-v1",
            coordinate_space=CoordinateSpace(
                space_id="prepared-page-1",
                width_px=100,
                height_px=100,
            ),
        ),
        witnesses=[
            WitnessReference(
                witness_id="wit-1",
                witness_kind="text",
                artifact_path="pages/page-1/witnesses/text/runner-1.json",
                runner_id="runner-1",
                page_id="page-1",
            )
        ],
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                note_ids=["note-1"],
                provenance=provenance,
            ),
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
                provenance=provenance,
            ),
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic="a",
                text_normalized="a",
                provenance=provenance,
            ),
        ],
        notes=[
            NoteRecord(
                note_id="note-1",
                note_kind=NoteKind.FOOTNOTE_BLOCK,
                region_id="region-1",
                text_diplomatic="note body",
                linked_marker_span_ids=["span-1"],
                provenance=provenance,
            )
        ],
    )


def _merge_flag(
    flag_type: MergeFlagType,
    target_object_ids: list[str],
    *,
    flag_id: str = "merge-flag-1",
) -> MergeFlag:
    """Return one merge flag fixture."""
    return MergeFlag(
        flag_id=flag_id,
        flag_type=flag_type,
        target_object_ids=target_object_ids,
        message=f"{flag_type} on {target_object_ids}",
    )


def _eval_flag(
    flag_type: str,
    target_object_ids: list[str],
    *,
    flag_id: str = "eval-1",
) -> EvaluationFlag:
    """Return one evaluation flag with an explicit merge flag_type."""
    return EvaluationFlag(
        flag_id=flag_id,
        flag_type=flag_type,
        severity=FlagSeverity.WARNING,
        message=f"{flag_type} on {target_object_ids}",
        target_object_ids=target_object_ids,
    )


def _page_with_text_flags(
    page: BundlePage, flags: list[EvaluationFlag]
) -> BundlePage:
    """Attach evaluation flags onto the text family only (legacy C3 shape)."""
    return page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(flags=flags)
            )
        }
    )


@pytest.mark.parametrize(
    ("flag_type", "targets", "expected_task_type", "expected_dimension"),
    [
        (
            MergeFlagType.TEXT_DISAGREEMENT,
            ["span-1"],
            ReviewTaskType.TEXT,
            ReviewDimension.TEXT,
        ),
        (
            MergeFlagType.TYPOGRAPHY_CONFLICT,
            ["span-1"],
            ReviewTaskType.TYPOGRAPHY,
            ReviewDimension.TYPOGRAPHY,
        ),
        (
            MergeFlagType.ROLE_CONFLICT,
            ["span-1"],
            ReviewTaskType.TEXT,
            ReviewDimension.TEXT,
        ),
        (
            MergeFlagType.NOTE_LINK_AMBIGUOUS,
            ["note-1"],
            ReviewTaskType.NOTE_LINKAGE,
            ReviewDimension.NOTE_LINKAGE,
        ),
        (
            MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT,
            ["region-1"],
            ReviewTaskType.LAYOUT,
            ReviewDimension.STRUCTURE,
        ),
    ],
)
def test_merge_flag_types_map_to_dimension_packets(
    page: BundlePage,
    flag_type: MergeFlagType,
    targets: list[str],
    expected_task_type: ReviewTaskType,
    expected_dimension: ReviewDimension,
) -> None:
    """Known merge flag types become Spec 0005 dimension packets even if mis-bucketed."""
    flagged = _page_with_text_flags(
        page, [_eval_flag(str(flag_type), targets)]
    )
    markup = HumanMarkupService("review-v1", "1.0.0")
    tasks = markup.build_review_tasks(
        flagged, run_id="run-1", graph_revision="graph-1"
    )
    by_type = {task.task_type: task for task in tasks}
    assert expected_task_type in by_type
    task = by_type[expected_task_type]
    assert task.dimensions == [expected_dimension]
    assert task.target_object_ids == targets


def test_merge_flag_dimension_map_is_exhaustive() -> None:
    """Every MergeFlagType has a Spec 0005 dimension mapping entry."""
    assert set(_MERGE_FLAG_DIMENSION) == set(MergeFlagType)


def test_text_disagreement_on_note_routes_to_adjudication(page: BundlePage) -> None:
    """Note-scoped text disagreement has no Spec 0005 text packet; use adjudication."""
    flagged = _page_with_text_flags(
        page,
        [_eval_flag(str(MergeFlagType.TEXT_DISAGREEMENT), ["note-1"])],
    )
    markup = HumanMarkupService("review-v1", "1.0.0")
    tasks = markup.build_review_tasks(
        flagged, run_id="run-1", graph_revision="graph-1"
    )
    assert len(tasks) == 1
    assert tasks[0].task_type is ReviewTaskType.ADJUDICATION
    assert tasks[0].related_object_ids == ["note-1"]
    assert ReviewDimension.TEXT in tasks[0].dimensions


def test_insufficient_evidence_forces_adjudication(page: BundlePage) -> None:
    """insufficient_evidence has no dedicated Spec 0005 packet type."""
    flagged = _page_with_text_flags(
        page,
        [_eval_flag(str(MergeFlagType.INSUFFICIENT_EVIDENCE), ["span-1"])],
    )
    markup = HumanMarkupService("review-v1", "1.0.0")
    tasks = markup.build_review_tasks(
        flagged, run_id="run-1", graph_revision="graph-1"
    )
    assert len(tasks) == 1
    assert tasks[0].task_type is ReviewTaskType.ADJUDICATION
    assert tasks[0].related_object_ids == ["span-1"]


def test_project_merge_flags_routes_into_evaluation_families(page: BundlePage) -> None:
    """Assemble projection places each merge flag into its Spec 0005 family."""
    service = MergeFlagReviewService()
    flags = [
        _merge_flag(MergeFlagType.TEXT_DISAGREEMENT, ["span-1"], flag_id="m-text"),
        _merge_flag(
            MergeFlagType.TYPOGRAPHY_CONFLICT, ["span-1"], flag_id="m-typo"
        ),
        _merge_flag(
            MergeFlagType.NOTE_LINK_AMBIGUOUS, ["note-1"], flag_id="m-note"
        ),
        _merge_flag(
            MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT,
            ["region-1"],
            flag_id="m-struct",
        ),
        _merge_flag(
            MergeFlagType.INSUFFICIENT_EVIDENCE, ["span-1"], flag_id="m-insuff"
        ),
        _merge_flag(MergeFlagType.ROLE_CONFLICT, ["span-1"], flag_id="m-role"),
    ]
    projected = service.project_onto_page(page, flags)
    summary = projected.evaluation_summary
    text_types = {flag.flag_type for flag in summary.text.flags}
    assert text_types == {
        str(MergeFlagType.TEXT_DISAGREEMENT),
        str(MergeFlagType.ROLE_CONFLICT),
        str(MergeFlagType.INSUFFICIENT_EVIDENCE),
    }
    assert {flag.flag_type for flag in summary.structure.flags} == {
        str(MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT)
    }
    assert {
        flag.flag_type for flag in summary.style.typography.flags
    } == {str(MergeFlagType.TYPOGRAPHY_CONFLICT)}
    assert {
        flag.flag_type for flag in summary.style.note_linkage.flags
    } == {str(MergeFlagType.NOTE_LINK_AMBIGUOUS)}


def test_tasks_from_merge_flags_builds_spec_0005_packets(page: BundlePage) -> None:
    """Service API: MergeFlag list → ReviewTask packets via HumanMarkupService."""
    service = MergeFlagReviewService()
    markup = HumanMarkupService("review-v1", "1.0.0")
    tasks = service.build_review_tasks(
        page,
        [
            _merge_flag(MergeFlagType.TEXT_DISAGREEMENT, ["span-1"]),
            _merge_flag(
                MergeFlagType.TYPOGRAPHY_CONFLICT, ["span-1"], flag_id="m-typo"
            ),
        ],
        markup=markup,
        run_id="run-1",
        graph_revision="graph-1",
    )
    by_type = {task.task_type: task for task in tasks}
    assert set(by_type) == {ReviewTaskType.TEXT, ReviewTaskType.TYPOGRAPHY}
    assert by_type[ReviewTaskType.TEXT].target_object_ids == ["span-1"]
    assert by_type[ReviewTaskType.TYPOGRAPHY].target_object_ids == ["span-1"]
