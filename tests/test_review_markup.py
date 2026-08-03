# Copyright (C) 2026 Chris Malek.
"""Tests for evidence-bound human-review task packet construction."""

from __future__ import annotations

import pytest

from bochord.models import (
    BundlePage,
    CoordinateSpace,
    LineRecord,
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


def _provenance() -> ObjectProvenance:
    """Return minimal provenance for graph fixtures."""
    return ObjectProvenance(
        source_page_id="page-1",
        witness_ids=["wit-1"],
        runner_ids=["runner-1"],
    )


@pytest.fixture
def page() -> BundlePage:
    """Return a page graph with two spans for text-task targeting."""
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
                provenance=provenance,
            )
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
    )


def test_text_packet_has_exact_scope_and_evidence_order(page: BundlePage) -> None:
    service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
    task = service.create_text_task(
        page, ["span-2"], run_id="run-1", graph_revision="graph-1"
    )
    assert task.target_scope is ReviewScope.SPAN
    assert task.target_object_ids == ["span-2"]
    assert task.dimensions == [ReviewDimension.TEXT]
    assert task.required_evidence == [
        "prepared-page-image",
        "scope-overlay",
        "raw-text-witnesses",
        "independent-witnesses",
        "accepted-page-graph",
        "evaluation-and-prior-review",
        "decision-controls-and-checklist",
    ]
    assert task.allowed_actions == [
        ReviewAction.ACCEPT,
        ReviewAction.CORRECT_TEXT,
        ReviewAction.MARK_ILLEGIBLE,
        ReviewAction.FLAG,
    ]


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
