# Copyright (C) 2026 Chris Malek.
"""Tests for evidence-bound human-review task packet construction."""

from __future__ import annotations

import pytest

from wordwending.models import (
    BundlePage,
    CoordinateSpace,
    EvaluationFamilySummary,
    EvaluationFlag,
    FlagSeverity,
    LineRecord,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PageEvaluationSummary,
    PreparationDecision,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    ReviewTaskType,
    SourceTriageDecision,
    SpanRecord,
    StyleEvaluationSummary,
    WitnessReference,
)
from wordwending.services.review_markup import HumanMarkupService


def _flag(
    flag_id: str,
    target_object_ids: list[str],
    *,
    flag_type: str = "test-flag",
) -> EvaluationFlag:
    """Return a minimal evaluation flag for queue fixtures."""
    return EvaluationFlag(
        flag_id=flag_id,
        flag_type=flag_type,
        severity=FlagSeverity.WARNING,
        message=f"flag {flag_id}",
        target_object_ids=target_object_ids,
    )

_EVIDENCE_TAIL = [
    "independent-witnesses",
    "accepted-page-graph",
    "evaluation-and-prior-review",
    "decision-controls-and-checklist",
]


def _expected_evidence(dimension_witness: str) -> list[str]:
    """Return Spec 0005 evidence order with a dimension-specific item 3."""
    return [
        "prepared-page-image",
        "scope-overlay",
        dimension_witness,
        *_EVIDENCE_TAIL,
    ]


_TEXT_EVIDENCE = _expected_evidence("raw-text-witnesses")
_LAYOUT_EVIDENCE = _expected_evidence("raw-structure-witnesses")
_TYPOGRAPHY_EVIDENCE = _expected_evidence("raw-typography-witnesses")
_NOTE_LINKAGE_EVIDENCE = _expected_evidence("raw-note-linkage-witnesses")
_SOURCE_TRIAGE_EVIDENCE = _expected_evidence("raw-source-quality-evidence")
_PREPARATION_EVIDENCE = [
    "source-vs-prepared-images",
    "scope-overlay",
    "checksum-and-transform-overlays",
    *_EVIDENCE_TAIL,
]
_ADJUDICATION_EVIDENCE = _expected_evidence("raw-flagged-dimension-witnesses")


def _provenance() -> ObjectProvenance:
    """Return minimal provenance for graph fixtures."""
    return ObjectProvenance(
        source_page_id="page-1",
        witness_ids=["wit-1"],
        runner_ids=["runner-1"],
    )


def _page_witnesses() -> list[WitnessReference]:
    """Return page-local witnesses matching fixture provenance."""
    return [
        WitnessReference(
            witness_id="wit-1",
            witness_kind="text",
            artifact_path="pages/page-1/witnesses/text/runner-1.json",
            runner_id="runner-1",
            page_id="page-1",
        )
    ]


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
        witnesses=_page_witnesses(),
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1", "line-2"],
                note_ids=["note-1"],
                provenance=provenance,
            ),
            RegionRecord(
                region_id="region-2",
                region_kind=RegionKind.FOOTNOTE,
                reading_order_index=2,
                line_ids=[],
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
            LineRecord(
                line_id="line-2",
                region_id="region-1",
                line_order=2,
                span_ids=["span-2"],
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
            SpanRecord(
                span_id="span-2",
                line_id="line-2",
                text_diplomatic="b",
                text_normalized="b",
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


def test_text_packet_has_exact_scope_and_evidence_order(page: BundlePage) -> None:
    service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
    task = service.create_text_task(
        page, ["span-2"], run_id="run-1", graph_revision="graph-1"
    )
    assert task.target_scope is ReviewScope.SPAN
    assert task.target_object_ids == ["span-2"]
    assert task.dimensions == [ReviewDimension.TEXT]
    assert ReviewDimension.TYPOGRAPHY not in task.dimensions
    assert task.required_evidence == _TEXT_EVIDENCE
    assert task.allowed_actions == [
        ReviewAction.ACCEPT,
        ReviewAction.CORRECT_TEXT,
        ReviewAction.MARK_ILLEGIBLE,
        ReviewAction.FLAG,
    ]


@pytest.mark.parametrize(
    (
        "factory_name",
        "target_object_ids",
        "related_object_ids",
        "expected_scope",
        "expected_dimension",
        "expected_actions",
        "expected_evidence",
        "question_fragment",
    ),
    [
        (
            "create_layout_task",
            ["region-1"],
            None,
            ReviewScope.REGION,
            ReviewDimension.STRUCTURE,
            [
                ReviewAction.ACCEPT,
                ReviewAction.CORRECT_GEOMETRY,
                ReviewAction.RECLASSIFY_REGION,
                ReviewAction.REORDER,
                ReviewAction.SPLIT_REGION,
                ReviewAction.MERGE_REGION,
                ReviewAction.FLAG,
            ],
            _LAYOUT_EVIDENCE,
            "region",
        ),
        (
            "create_typography_task",
            ["span-1"],
            None,
            ReviewScope.SPAN,
            ReviewDimension.TYPOGRAPHY,
            [
                ReviewAction.ACCEPT,
                ReviewAction.CORRECT_STYLE,
                ReviewAction.FLAG,
            ],
            _TYPOGRAPHY_EVIDENCE,
            "typography",
        ),
        (
            "create_note_linkage_task",
            ["note-1"],
            ["span-1"],
            ReviewScope.NOTE,
            ReviewDimension.NOTE_LINKAGE,
            [
                ReviewAction.ACCEPT,
                ReviewAction.LINK_NOTE,
                ReviewAction.UNLINK_NOTE,
                ReviewAction.FLAG,
            ],
            _NOTE_LINKAGE_EVIDENCE,
            "note",
        ),
    ],
    ids=["layout", "typography", "note_linkage"],
)
def test_dimension_specific_packets(  # noqa: PLR0913, PLR0917
    page: BundlePage,
    factory_name: str,
    target_object_ids: list[str],
    related_object_ids: list[str] | None,
    expected_scope: ReviewScope,
    expected_dimension: ReviewDimension,
    expected_actions: list[ReviewAction],
    expected_evidence: list[str],
    question_fragment: str,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
    factory = getattr(service, factory_name)
    if related_object_ids is None:
        task = factory(
            page,
            target_object_ids,
            run_id="run-1",
            graph_revision="graph-1",
        )
        assert task.related_object_ids == []
    else:
        task = factory(
            page,
            target_object_ids,
            related_object_ids=related_object_ids,
            run_id="run-1",
            graph_revision="graph-1",
        )
        assert task.related_object_ids == related_object_ids
    assert task.question
    assert question_fragment in task.question.lower()
    assert task.dimensions == [expected_dimension]
    assert len(task.dimensions) == 1
    assert task.target_scope is expected_scope
    assert task.target_object_ids == target_object_ids
    assert task.supports_abstention is True
    assert task.allowed_actions == expected_actions
    assert task.required_evidence == expected_evidence
    assert task.prepared_image_checksum == "sha256:image"
    text_task = service.create_text_task(
        page, ["span-2"], run_id="run-1", graph_revision="graph-1"
    )
    assert ReviewDimension.TYPOGRAPHY not in text_task.dimensions
    assert text_task.required_evidence == _TEXT_EVIDENCE
    assert text_task.required_evidence != expected_evidence


def test_layout_split_merge_scope_includes_every_source_region(
    page: BundlePage,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    task = service.create_layout_task(
        page,
        ["region-1", "region-2"],
        run_id="run-1",
        graph_revision="graph-1",
    )
    assert task.target_object_ids == ["region-1", "region-2"]
    assert task.target_scope is ReviewScope.REGION
    assert task.dimensions == [ReviewDimension.STRUCTURE]


@pytest.mark.parametrize("guideline_id", ["", "   "])
def test_rejects_blank_guideline_id(guideline_id: str) -> None:
    with pytest.raises(ValueError, match="guideline_id"):
        HumanMarkupService(guideline_id, "1.0.0")


@pytest.mark.parametrize("guideline_version", ["", "   "])
def test_rejects_blank_guideline_version(guideline_version: str) -> None:
    with pytest.raises(ValueError, match="guideline_version"):
        HumanMarkupService("review-v1", guideline_version)


def test_create_text_task_rejects_empty_target_object_ids(page: BundlePage) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    with pytest.raises(ValueError, match="must not be empty"):
        service.create_text_task(
            page, [], run_id="run-1", graph_revision="graph-1"
        )


def test_create_text_task_rejects_unknown_non_span_targets(page: BundlePage) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    with pytest.raises(ValueError, match="span ids"):
        service.create_text_task(
            page,
            ["region-1"],
            run_id="run-1",
            graph_revision="graph-1",
        )


@pytest.mark.parametrize(
    ("factory_name", "match"),
    [
        ("create_layout_task", "region"),
        ("create_typography_task", "span"),
        ("create_note_linkage_task", "note"),
    ],
)
def test_dimension_factories_reject_empty_targets(
    page: BundlePage,
    factory_name: str,
    match: str,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    factory = getattr(service, factory_name)
    with pytest.raises(ValueError, match=match) as exc_info:
        factory(page, [], run_id="run-1", graph_revision="graph-1")
    assert "must not be empty" in str(exc_info.value)


@pytest.mark.parametrize(
    ("factory_name", "bad_ids", "match"),
    [
        ("create_layout_task", ["span-1"], "region"),
        ("create_typography_task", ["region-1"], "span"),
        ("create_note_linkage_task", ["span-1"], "note"),
    ],
)
def test_dimension_factories_reject_unknown_wrong_kind_targets(
    page: BundlePage,
    factory_name: str,
    bad_ids: list[str],
    match: str,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    factory = getattr(service, factory_name)
    with pytest.raises(ValueError, match=match):
        factory(page, bad_ids, run_id="run-1", graph_revision="graph-1")


def test_create_note_linkage_task_rejects_unknown_related_span_ids(
    page: BundlePage,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    with pytest.raises(ValueError, match="span ids"):
        service.create_note_linkage_task(
            page,
            ["note-1"],
            related_object_ids=["region-1"],
            run_id="run-1",
            graph_revision="graph-1",
        )


def test_source_triage_packet_is_page_scoped_with_disposition_controls(
    page: BundlePage,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
    task = service.create_source_triage_task(
        page, run_id="run-1", graph_revision="graph-1"
    )
    assert task.target_scope is ReviewScope.PAGE
    assert task.target_object_ids == ["page-1"]
    assert task.dimensions == [ReviewDimension.SOURCE_QUALITY]
    assert task.supports_abstention is True
    assert task.allowed_actions == [
        ReviewAction.ACCEPT,
        ReviewAction.DECIDE_SOURCE_TRIAGE,
        ReviewAction.FLAG,
    ]
    assert "whole-page" in task.question.lower()
    assert "small-font" in task.question.lower()
    assert "checksum" in task.question.lower()
    assert task.required_evidence == _SOURCE_TRIAGE_EVIDENCE
    assert task.prepared_image_checksum == "sha256:image"
    assert {decision.value for decision in SourceTriageDecision} == {
        "usable",
        "usable-with-warning",
        "reprepare",
        "reacquire",
    }


def test_preparation_packet_is_page_scoped_with_decision_controls(
    page: BundlePage,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
    task = service.create_preparation_task(
        page, run_id="run-1", graph_revision="graph-1"
    )
    assert task.target_scope is ReviewScope.PAGE
    assert task.target_object_ids == ["page-1"]
    assert task.dimensions == [ReviewDimension.PREPARATION]
    assert task.supports_abstention is True
    assert task.allowed_actions == [
        ReviewAction.ACCEPT,
        ReviewAction.DECIDE_PREPARATION,
        ReviewAction.FLAG,
    ]
    assert "whole-page" in task.question.lower() or "full-page" in task.question.lower()
    assert "small-font" in task.question.lower()
    assert "checksum" in task.question.lower()
    assert "transform" in task.question.lower()
    assert task.required_evidence == _PREPARATION_EVIDENCE
    assert "source-vs-prepared-images" in task.required_evidence
    assert "checksum-and-transform-overlays" in task.required_evidence
    assert task.prepared_image_checksum == "sha256:image"
    assert {decision.value for decision in PreparationDecision} == {
        "full-page",
        "subdivide",
    }


def test_build_review_tasks_preserves_dimension_specific_coverage(
    page: BundlePage,
) -> None:
    flagged_page = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[
                        _flag("text-1", ["span-1"]),
                        _flag("text-empty", []),
                        _flag("text-unknown", ["missing-span"]),
                    ]
                ),
                structure=EvaluationFamilySummary(
                    flags=[_flag("structure-1", ["region-2", "region-1"])]
                ),
                style=StyleEvaluationSummary(
                    typography=EvaluationFamilySummary(
                        flags=[_flag("typo-1", ["span-2"])]
                    ),
                    note_linkage=EvaluationFamilySummary(
                        flags=[_flag("note-1", ["span-1", "note-1"])]
                    ),
                ),
            )
        }
    )
    service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
    tasks = service.build_review_tasks(
        flagged_page, run_id="run-1", graph_revision="graph-1"
    )

    flagged_ids = {
        "span-1",
        "span-2",
        "region-1",
        "region-2",
        "note-1",
        "missing-span",
    }
    covered_ids: set[str] = set()
    for task in tasks:
        covered_ids.update(task.target_object_ids)
        covered_ids.update(task.related_object_ids)
    assert flagged_ids <= covered_ids

    by_type = {task.task_type: task for task in tasks}
    assert set(by_type) == {
        ReviewTaskType.TEXT,
        ReviewTaskType.LAYOUT,
        ReviewTaskType.TYPOGRAPHY,
        ReviewTaskType.NOTE_LINKAGE,
        ReviewTaskType.ADJUDICATION,
    }

    assert by_type[ReviewTaskType.TEXT].target_scope is ReviewScope.SPAN
    assert by_type[ReviewTaskType.TEXT].target_object_ids == ["span-1"]
    assert by_type[ReviewTaskType.TEXT].dimensions == [ReviewDimension.TEXT]

    assert by_type[ReviewTaskType.LAYOUT].target_scope is ReviewScope.REGION
    assert by_type[ReviewTaskType.LAYOUT].target_object_ids == [
        "region-1",
        "region-2",
    ]
    assert by_type[ReviewTaskType.LAYOUT].dimensions == [ReviewDimension.STRUCTURE]

    assert by_type[ReviewTaskType.TYPOGRAPHY].target_scope is ReviewScope.SPAN
    assert by_type[ReviewTaskType.TYPOGRAPHY].target_object_ids == ["span-2"]
    assert by_type[ReviewTaskType.TYPOGRAPHY].dimensions == [
        ReviewDimension.TYPOGRAPHY
    ]

    note_task = by_type[ReviewTaskType.NOTE_LINKAGE]
    assert note_task.target_scope is ReviewScope.NOTE
    assert note_task.target_object_ids == ["note-1"]
    assert note_task.related_object_ids == ["span-1"]
    assert note_task.dimensions == [ReviewDimension.NOTE_LINKAGE]

    adjudication = by_type[ReviewTaskType.ADJUDICATION]
    assert adjudication.target_scope is ReviewScope.PAGE
    assert adjudication.target_object_ids == ["page-1"]
    assert adjudication.related_object_ids == ["missing-span"]
    assert adjudication.allowed_actions == [
        ReviewAction.FLAG,
    ]
    assert ReviewAction.ACCEPT not in adjudication.allowed_actions
    assert adjudication.supports_abstention is True
    assert adjudication.prepared_image_checksum == "sha256:image"
    assert adjudication.required_evidence == _ADJUDICATION_EVIDENCE
    assert ReviewDimension.TEXT in adjudication.dimensions

    sort_keys = [
        (
            [dimension.value for dimension in task.dimensions],
            task.target_scope.value,
            list(task.target_object_ids),
        )
        for task in tasks
    ]
    assert sort_keys == sorted(sort_keys)

    for task in tasks:
        assert task.certified_coverage_ids == []
        if task.task_type is not ReviewTaskType.ADJUDICATION:
            assert task.target_scope is not ReviewScope.PAGE


def test_note_linkage_marker_only_flags_collapse_to_adjudication(
    page: BundlePage,
) -> None:
    flagged_page = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                style=StyleEvaluationSummary(
                    note_linkage=EvaluationFamilySummary(
                        flags=[_flag("marker-only", ["span-2"])]
                    )
                )
            )
        }
    )
    service = HumanMarkupService("review-v1", "1.0.0")
    tasks = service.build_review_tasks(
        flagged_page, run_id="run-1", graph_revision="graph-1"
    )
    assert len(tasks) == 1
    task = tasks[0]
    assert task.task_type is ReviewTaskType.ADJUDICATION
    assert task.target_object_ids == ["page-1"]
    assert task.related_object_ids == ["span-2"]
    assert task.dimensions == [ReviewDimension.NOTE_LINKAGE]


def test_blank_target_object_id_routes_to_adjudication(page: BundlePage) -> None:
    flagged_page = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[_flag("blank-target", ["span-1", "   "])]
                )
            )
        }
    )
    service = HumanMarkupService("review-v1", "1.0.0")
    tasks = service.build_review_tasks(
        flagged_page, run_id="run-1", graph_revision="graph-1"
    )
    by_type = {task.task_type: task for task in tasks}
    assert set(by_type) == {ReviewTaskType.TEXT, ReviewTaskType.ADJUDICATION}
    assert by_type[ReviewTaskType.TEXT].target_object_ids == ["span-1"]
    adjudication = by_type[ReviewTaskType.ADJUDICATION]
    assert adjudication.target_object_ids == ["page-1"]
    assert adjudication.related_object_ids == []
    assert adjudication.dimensions == [ReviewDimension.TEXT]


def test_create_adjudication_flag_task_rejects_empty_dimensions(
    page: BundlePage,
) -> None:
    service = HumanMarkupService("review-v1", "1.0.0")
    with pytest.raises(ValueError, match="at least one dimension"):
        service.create_adjudication_flag_task(
            page,
            dimensions=[],
            run_id="run-1",
            graph_revision="graph-1",
        )


def test_adjudication_excludes_page_id_from_related_object_ids(
    page: BundlePage,
) -> None:
    flagged_page = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[_flag("page-as-target", ["page-1", "missing-span"])]
                )
            )
        }
    )
    service = HumanMarkupService("review-v1", "1.0.0")
    tasks = service.build_review_tasks(
        flagged_page, run_id="run-1", graph_revision="graph-1"
    )
    assert len(tasks) == 1
    task = tasks[0]
    assert task.task_type is ReviewTaskType.ADJUDICATION
    assert task.target_object_ids == ["page-1"]
    assert task.related_object_ids == ["missing-span"]
    assert "page-1" not in task.related_object_ids
