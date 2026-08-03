# Copyright (C) 2026 Chris Malek.
"""Tests for deterministic review-overlay event replay."""

from __future__ import annotations

from datetime import UTC, datetime

from bochord.models import (
    AcceptReviewEvent,
    BaselineShift,
    CorrectGeometryReviewEvent,
    CorrectStyleReviewEvent,
    CorrectTextReviewEvent,
    FlagReviewEvent,
    FlagSeverity,
    FontSlant,
    FontWeight,
    LinkNoteReviewEvent,
    MarkIllegibleReviewEvent,
    PageOverlay,
    Point,
    Polygon,
    ReclassifyRegionReviewEvent,
    RegionKind,
    ResolveFlagReviewEvent,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
    TextRole,
    TrustState,
    Typography,
    UnlinkNoteReviewEvent,
)
from bochord.services.review_overlay import ReviewOverlayService


def _ts() -> datetime:
    """Return a fixed operator timestamp."""
    return datetime(2026, 8, 3, tzinfo=UTC)


def _event_base(  # noqa: PLR0913
    *,
    event_id: str,
    task_id: str,
    target_object_id: str,
    target_scope: ReviewScope,
    review_dimensions: list[ReviewDimension],
    prior_trust_state: TrustState,
    new_trust_state: TrustState,
) -> dict[str, object]:
    """Return shared review-event fields for the replay fixture."""
    return {
        "event_id": event_id,
        "task_id": task_id,
        "target_object_id": target_object_id,
        "target_scope": target_scope,
        "review_dimensions": review_dimensions,
        "base_run_id": "run-1",
        "base_graph_revision": "graph-1",
        "guideline_version": "1.0.0",
        "prior_trust_state": prior_trust_state,
        "new_trust_state": new_trust_state,
        "operator_id": "editor-1",
        "timestamp_utc": _ts(),
    }


def _task(  # noqa: PLR0913
    *,
    task_id: str,
    task_type: ReviewTaskType,
    dimensions: list[ReviewDimension],
    target_scope: ReviewScope,
    target_object_ids: list[str],
    allowed_actions: list[ReviewAction],
) -> ReviewTask:
    """Return a review task bound to the shared overlay evidence."""
    return ReviewTask(
        task_id=task_id,
        task_type=task_type,
        dimensions=dimensions,
        target_scope=target_scope,
        target_object_ids=target_object_ids,
        question="Inspect the target.",
        required_evidence=["prepared-page", "witness"],
        allowed_actions=allowed_actions,
        completion_criteria=["evidence inspected"],
        guideline_id="review",
        guideline_version="1.0.0",
        base_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
    )


def _polygon() -> Polygon:
    """Return polygon-only replacement geometry."""
    return Polygon(
        coordinate_space_id="prepared-page-1",
        points=[
            Point(x=0, y=0),
            Point(x=12, y=0),
            Point(x=12, y=8),
        ],
    )


def _typography() -> Typography:
    """Return orthogonal typography facets for style correction."""
    return Typography(
        weight=FontWeight.BOLD,
        slant=FontSlant.ITALIC,
        baseline_shift=BaselineShift.SUPERSCRIPT,
    )


def _replay_overlay() -> PageOverlay:
    """
    Build one overlay covering every replay assertion path.

    current_state is intentionally stale so materialize must ignore it.
    """
    text_task = _task(
        task_id="task-text",
        task_type=ReviewTaskType.TEXT,
        dimensions=[ReviewDimension.TEXT],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        allowed_actions=[
            ReviewAction.ACCEPT,
            ReviewAction.CORRECT_TEXT,
            ReviewAction.MARK_ILLEGIBLE,
            ReviewAction.FLAG,
            ReviewAction.RESOLVE_FLAG,
        ],
    )
    style_task = _task(
        task_id="task-style",
        task_type=ReviewTaskType.TYPOGRAPHY,
        dimensions=[ReviewDimension.TYPOGRAPHY],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        allowed_actions=[ReviewAction.CORRECT_STYLE],
    )
    layout_span_task = _task(
        task_id="task-geo",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        allowed_actions=[ReviewAction.CORRECT_GEOMETRY],
    )
    layout_region_task = _task(
        task_id="task-region",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.REGION,
        target_object_ids=["region-1"],
        allowed_actions=[ReviewAction.RECLASSIFY_REGION],
    )
    note_task = _task(
        task_id="task-note",
        task_type=ReviewTaskType.NOTE_LINKAGE,
        dimensions=[ReviewDimension.NOTE_LINKAGE],
        target_scope=ReviewScope.NOTE,
        target_object_ids=["note-1"],
        allowed_actions=[ReviewAction.LINK_NOTE, ReviewAction.UNLINK_NOTE],
    )
    polygon = _polygon()
    events = [
        AcceptReviewEvent(
            **_event_base(
                event_id="evt-accept",
                task_id="task-text",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.REVIEWED,
            )
        ),
        CorrectTextReviewEvent(
            **_event_base(
                event_id="evt-text",
                task_id="task-text",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                prior_trust_state=TrustState.REVIEWED,
                new_trust_state=TrustState.CORRECTED,
            ),
            text_diplomatic="emended",
        ),
        CorrectStyleReviewEvent(
            **_event_base(
                event_id="evt-style",
                task_id="task-style",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TYPOGRAPHY],
                prior_trust_state=TrustState.CORRECTED,
                new_trust_state=TrustState.CORRECTED,
            ),
            new_typography=_typography(),
            new_roles=[TextRole.FOOTNOTE_MARKER],
        ),
        CorrectGeometryReviewEvent(
            **_event_base(
                event_id="evt-geo",
                task_id="task-geo",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.STRUCTURE],
                prior_trust_state=TrustState.CORRECTED,
                new_trust_state=TrustState.CORRECTED,
            ),
            polygon=polygon,
        ),
        ReclassifyRegionReviewEvent(
            **_event_base(
                event_id="evt-reclass",
                task_id="task-region",
                target_object_id="region-1",
                target_scope=ReviewScope.REGION,
                review_dimensions=[ReviewDimension.STRUCTURE],
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.CORRECTED,
            ),
            new_region_kind=RegionKind.FOOTNOTE,
        ),
        LinkNoteReviewEvent(
            **_event_base(
                event_id="evt-link",
                task_id="task-note",
                target_object_id="note-1",
                target_scope=ReviewScope.NOTE,
                review_dimensions=[ReviewDimension.NOTE_LINKAGE],
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.CORRECTED,
            ),
            marker_span_ids=["marker-1", "marker-2"],
            note_id="note-1",
        ),
        UnlinkNoteReviewEvent(
            **_event_base(
                event_id="evt-unlink",
                task_id="task-note",
                target_object_id="note-1",
                target_scope=ReviewScope.NOTE,
                review_dimensions=[ReviewDimension.NOTE_LINKAGE],
                prior_trust_state=TrustState.CORRECTED,
                new_trust_state=TrustState.CORRECTED,
            ),
            marker_span_ids=["marker-1"],
            note_id="note-1",
        ),
        MarkIllegibleReviewEvent(
            **_event_base(
                event_id="evt-illegible",
                task_id="task-text",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                prior_trust_state=TrustState.CORRECTED,
                new_trust_state=TrustState.CORRECTED,
            ),
            reason="ink lost at gutter",
        ),
        FlagReviewEvent(
            **_event_base(
                event_id="evt-flag",
                task_id="task-text",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                prior_trust_state=TrustState.CORRECTED,
                new_trust_state=TrustState.CORRECTED,
            ),
            flag_id="flag-1",
            flag_type="uncertain-glyph",
            severity=FlagSeverity.WARNING,
            message="possible long-s confusion",
        ),
        ResolveFlagReviewEvent(
            **_event_base(
                event_id="evt-resolve",
                task_id="task-text",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                prior_trust_state=TrustState.CORRECTED,
                new_trust_state=TrustState.CORRECTED,
            ),
            flag_id="flag-1",
            resolution="confirmed long-s",
        ),
    ]
    return PageOverlay(
        schema_version="1.0.0",
        overlay_id="overlay-1",
        page_id="page-1",
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
        review_tasks=[
            text_task,
            style_task,
            layout_span_task,
            layout_region_task,
            note_task,
        ],
        review_events=events,
        current_state=[],
    )


def test_replay_materializes_only_append_only_event_effects() -> None:
    """Replay builds OverlayState solely from ordered append-only events."""
    overlay = _replay_overlay()
    service = ReviewOverlayService()

    states = service.materialize(overlay)
    by_key = {(state.object_id, state.scope): state for state in states}

    span = by_key[("span-1", ReviewScope.SPAN)]
    region = by_key[("region-1", ReviewScope.REGION)]
    note = by_key[("note-1", ReviewScope.NOTE)]

    assert span.applied_event_ids == [
        "evt-accept",
        "evt-text",
        "evt-style",
        "evt-geo",
        "evt-illegible",
        "evt-flag",
        "evt-resolve",
    ]
    assert span.text_diplomatic_override == "emended"
    assert not hasattr(span, "text_normalized_override")
    assert "text_normalized_override" not in type(span).model_fields
    assert span.typography_override == _typography()
    assert span.role_overrides == [TextRole.FOOTNOTE_MARKER]
    assert span.bounding_box_override is None
    assert span.polygon_override == _polygon()
    assert span.illegible is True
    assert span.active_flag_ids == []
    assert span.trust_state == TrustState.CORRECTED
    assert ReviewDimension.TEXT in span.reviewed_dimensions
    assert ReviewDimension.TYPOGRAPHY in span.reviewed_dimensions
    assert ReviewDimension.STRUCTURE in span.reviewed_dimensions
    assert ReviewDimension.TEXT in span.corrected_dimensions
    assert ReviewDimension.TYPOGRAPHY in span.corrected_dimensions

    assert region.region_kind_override == RegionKind.FOOTNOTE
    assert region.applied_event_ids == ["evt-reclass"]
    assert region.trust_state == TrustState.CORRECTED

    assert note.linked_marker_span_ids == ["marker-2"]
    assert note.applied_event_ids == ["evt-link", "evt-unlink"]
    assert note.trust_state == TrustState.CORRECTED

    # Flag then resolve must leave trust unchanged while clearing the flag.
    assert span.trust_state == TrustState.CORRECTED
    assert "flag-1" not in span.active_flag_ids
