# Copyright (C) 2026 Chris Malek.
"""Tests for evidence-bound human-review task packet construction."""

from __future__ import annotations

import pytest

from bochord.models import (
    BundlePage,
    CoordinateSpace,
    LineRecord,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    SpanRecord,
)
from bochord.services.review_markup import HumanMarkupService

_EXPECTED_EVIDENCE = [
    "prepared-page-image",
    "scope-overlay",
    "raw-text-witnesses",
    "independent-witnesses",
    "accepted-page-graph",
    "evaluation-and-prior-review",
    "decision-controls-and-checklist",
]


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
    assert task.required_evidence == _EXPECTED_EVIDENCE
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
    assert task.required_evidence == _EXPECTED_EVIDENCE
    assert task.prepared_image_checksum == "sha256:image"
    text_task = service.create_text_task(
        page, ["span-2"], run_id="run-1", graph_revision="graph-1"
    )
    assert ReviewDimension.TYPOGRAPHY not in text_task.dimensions


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
    with pytest.raises(ValueError, match="target_object_ids"):
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
