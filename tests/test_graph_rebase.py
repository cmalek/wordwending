# Copyright (C) 2026 Chris Malek.
"""Tests for GraphRebaseService overlay→graph leaf application."""

from __future__ import annotations

import pytest

from wordwending.models import (
    BaselineShift,
    BoundingBox,
    BundlePage,
    CoordinateSpace,
    FontSlant,
    FontWeight,
    LineRecord,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    OverlayState,
    PageClass,
    Point,
    Polygon,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewDimension,
    ReviewScope,
    ReviewSummary,
    SpanRecord,
    TextRole,
    TrustState,
    Typography,
    WitnessReference,
)
from wordwending.services.graph_rebase import GraphRebaseService


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-1",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
    )


def _page() -> BundlePage:
    """Return a minimal page with one region, line, span, and note."""
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
                artifact_path="pages/page-1/witnesses/text/olmocr.json",
                runner_id="olmocr",
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
                bounding_box=BoundingBox(
                    x0=0,
                    y0=0,
                    x1=50,
                    y1=50,
                    coordinate_space_id="prepared-page-1",
                ),
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
            )
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic="machine-text",
                text_normalized="machine-text",
                typography=Typography(),
                roles=[TextRole.TEXT],
                bounding_box=BoundingBox(
                    x0=1,
                    y0=1,
                    x1=10,
                    y1=10,
                    coordinate_space_id="prepared-page-1",
                ),
                provenance=provenance,
            )
        ],
        notes=[
            NoteRecord(
                note_id="note-1",
                note_kind=NoteKind.FOOTNOTE_BLOCK,
                region_id="region-1",
                text_diplomatic="note-body",
                linked_marker_span_ids=[],
                provenance=provenance,
            )
        ],
        graph_revision="graph-v0",
    )


def test_rebase_applies_text_diplomatic_override() -> None:
    """Text overrides rewrite span diplomatic text by object_id + scope."""
    page = _page()
    states = [
        OverlayState(
            object_id="span-1",
            scope=ReviewScope.SPAN,
            trust_state=TrustState.CORRECTED,
            text_diplomatic_override="emended",
            corrected_dimensions=[ReviewDimension.TEXT],
            applied_event_ids=["evt-text"],
        )
    ]

    result = GraphRebaseService().rebase_page(
        page, states, new_graph_revision="graph-v1"
    )

    assert result.spans[0].text_diplomatic == "emended"
    assert result.spans[0].trust_state == TrustState.CORRECTED
    assert result.notes[0].text_diplomatic == "note-body"


def test_rebase_applies_note_text_diplomatic_override() -> None:
    """Text overrides rewrite note diplomatic text by object_id + scope."""
    page = _page()
    states = [
        OverlayState(
            object_id="note-1",
            scope=ReviewScope.NOTE,
            trust_state=TrustState.CORRECTED,
            text_diplomatic_override="emended-note",
            corrected_dimensions=[ReviewDimension.TEXT],
            applied_event_ids=["evt-note-text"],
        )
    ]

    result = GraphRebaseService().rebase_page(
        page, states, new_graph_revision="graph-v1"
    )

    assert result.notes[0].text_diplomatic == "emended-note"
    assert result.notes[0].trust_state == TrustState.CORRECTED
    assert result.spans[0].text_diplomatic == "machine-text"


def test_rebase_applies_typography_and_roles() -> None:
    """Typography and role overrides update the matching span."""
    page = _page()
    typography = Typography(
        weight=FontWeight.BOLD,
        slant=FontSlant.ITALIC,
        baseline_shift=BaselineShift.SUPERSCRIPT,
    )
    states = [
        OverlayState(
            object_id="span-1",
            scope=ReviewScope.SPAN,
            trust_state=TrustState.CORRECTED,
            typography_override=typography,
            role_overrides=[TextRole.FOOTNOTE_MARKER],
            corrected_dimensions=[ReviewDimension.TYPOGRAPHY],
            applied_event_ids=["evt-style"],
        )
    ]

    result = GraphRebaseService().rebase_page(
        page, states, new_graph_revision="graph-v1"
    )

    assert result.spans[0].typography == typography
    assert result.spans[0].roles == [TextRole.FOOTNOTE_MARKER]


def test_rebase_raises_on_unknown_object_id() -> None:
    """Unknown object_id raises ValueError naming the id."""
    page = _page()
    states = [
        OverlayState(
            object_id="span-missing",
            scope=ReviewScope.SPAN,
            trust_state=TrustState.CORRECTED,
            text_diplomatic_override="gone",
        )
    ]

    with pytest.raises(ValueError, match="span-missing"):
        GraphRebaseService().rebase_page(page, states, new_graph_revision="graph-v1")


def test_rebase_bumps_graph_revision() -> None:
    """Returned page carries the caller-supplied graph_revision."""
    page = _page()
    assert page.graph_revision == "graph-v0"

    result = GraphRebaseService().rebase_page(page, [], new_graph_revision="graph-v1")

    assert result.graph_revision == "graph-v1"
    assert page.graph_revision == "graph-v0"


def test_rebase_preserves_unrelated_page_fields() -> None:
    """Aside from applied overrides and revision, the page graph is equal."""
    page = _page()
    states = [
        OverlayState(
            object_id="span-1",
            scope=ReviewScope.SPAN,
            trust_state=TrustState.CORRECTED,
            text_diplomatic_override="emended",
            reviewed_dimensions=[ReviewDimension.TEXT],
            corrected_dimensions=[ReviewDimension.TEXT],
            applied_event_ids=["evt-text"],
        )
    ]

    result = GraphRebaseService().rebase_page(
        page, states, new_graph_revision="graph-v1"
    )

    expected = page.model_copy(deep=True)
    expected.spans[0].text_diplomatic = "emended"
    expected.spans[0].trust_state = TrustState.CORRECTED
    expected.spans[0].review = ReviewSummary(
        reviewed_dimensions=[ReviewDimension.TEXT],
        corrected_dimensions=[ReviewDimension.TEXT],
        last_event_id="evt-text",
        event_ids=["evt-text"],
    )
    expected.graph_revision = "graph-v1"
    assert result == expected


def test_rebase_applies_geometry_region_kind_and_note_links() -> None:
    """Geometry, region_kind, and note linkage overrides update targets."""
    page = _page()
    box = BoundingBox(
        x0=2,
        y0=2,
        x1=20,
        y1=20,
        coordinate_space_id="prepared-page-1",
    )
    polygon = Polygon(
        coordinate_space_id="prepared-page-1",
        points=[Point(x=0, y=0), Point(x=12, y=0), Point(x=12, y=8)],
    )
    states = [
        OverlayState(
            object_id="span-1",
            scope=ReviewScope.SPAN,
            trust_state=TrustState.CORRECTED,
            bounding_box_override=box,
            applied_event_ids=["evt-geo"],
        ),
        OverlayState(
            object_id="region-1",
            scope=ReviewScope.REGION,
            trust_state=TrustState.CORRECTED,
            region_kind_override=RegionKind.FOOTNOTE,
            polygon_override=polygon,
            applied_event_ids=["evt-kind"],
        ),
        OverlayState(
            object_id="note-1",
            scope=ReviewScope.NOTE,
            trust_state=TrustState.CORRECTED,
            linked_marker_span_ids=["span-1"],
            corrected_dimensions=[ReviewDimension.NOTE_LINKAGE],
            applied_event_ids=["evt-link"],
        ),
    ]

    result = GraphRebaseService().rebase_page(
        page, states, new_graph_revision="graph-v1"
    )

    assert result.spans[0].bounding_box == box
    assert result.regions[0].region_kind == RegionKind.FOOTNOTE
    assert result.regions[0].polygon == polygon
    assert result.notes[0].linked_marker_span_ids == ["span-1"]


def test_rebase_illegible_updates_trust_without_new_graph_field() -> None:
    """Illegible applies trust/review only; text and BundlePage stay field-stable."""
    page = _page()
    states = [
        OverlayState(
            object_id="span-1",
            scope=ReviewScope.SPAN,
            trust_state=TrustState.REVIEWED,
            illegible=True,
            reviewed_dimensions=[ReviewDimension.TEXT],
            applied_event_ids=["evt-illegible"],
        )
    ]

    result = GraphRebaseService().rebase_page(
        page, states, new_graph_revision="graph-v1"
    )

    assert result.spans[0].text_diplomatic == "machine-text"
    assert result.spans[0].trust_state == TrustState.REVIEWED
    assert result.spans[0].review.last_event_id == "evt-illegible"
    assert not hasattr(result, "illegible")
    assert "illegible" not in type(result).model_fields
