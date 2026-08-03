# Copyright (C) 2026 Chris Malek.
"""Tests for deterministic review-overlay event replay."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

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
    RegionRevision,
    ResolveFlagReviewEvent,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    ReviewTask,
    ReviewTaskStatus,
    ReviewTaskType,
    SplitRegionReviewEvent,
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
    base_run_id: str = "run-1",
    base_graph_revision: str = "graph-1",
    prepared_image_checksum: str = "sha256:prepared",
    status: ReviewTaskStatus = ReviewTaskStatus.PENDING,
    related_object_ids: list[str] | None = None,
) -> ReviewTask:
    """Return a review task bound to the shared overlay evidence."""
    return ReviewTask(
        task_id=task_id,
        task_type=task_type,
        dimensions=dimensions,
        target_scope=target_scope,
        target_object_ids=target_object_ids,
        related_object_ids=related_object_ids or [],
        question="Inspect the target.",
        required_evidence=["prepared-page", "witness"],
        allowed_actions=allowed_actions,
        completion_criteria=["evidence inspected"],
        guideline_id="review",
        guideline_version="1.0.0",
        base_run_id=base_run_id,
        base_graph_revision=base_graph_revision,
        prepared_image_checksum=prepared_image_checksum,
        status=status,
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


def _successor_source_overlay() -> PageOverlay:
    """
    Build a compact predecessor with one copyable and two conflict events.

    Copyable: text correction whose task, target, and event ids all map.
    Conflicts: geometry whose coordinate space is outside the resolvable set,
    and a note link whose nested marker id is absent from the object map.
    """
    text_task = _task(
        task_id="task-text",
        task_type=ReviewTaskType.TEXT,
        dimensions=[ReviewDimension.TEXT],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        allowed_actions=[ReviewAction.CORRECT_TEXT],
    )
    geo_task = _task(
        task_id="task-geo",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        allowed_actions=[ReviewAction.CORRECT_GEOMETRY],
    )
    note_task = _task(
        task_id="task-note",
        task_type=ReviewTaskType.NOTE_LINKAGE,
        dimensions=[ReviewDimension.NOTE_LINKAGE],
        target_scope=ReviewScope.NOTE,
        target_object_ids=["note-1"],
        allowed_actions=[ReviewAction.LINK_NOTE],
    )
    events = [
        CorrectTextReviewEvent(
            **_event_base(
                event_id="evt-text",
                task_id="task-text",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.CORRECTED,
            ),
            text_diplomatic="emended",
        ),
        CorrectGeometryReviewEvent(
            **_event_base(
                event_id="evt-geo",
                task_id="task-geo",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.STRUCTURE],
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.CORRECTED,
            ),
            polygon=_polygon(),
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
            marker_span_ids=["marker-1", "marker-unmapped"],
            note_id="note-1",
        ),
    ]
    return PageOverlay(
        schema_version="1.0.0",
        overlay_id="overlay-old",
        page_id="page-1",
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
        review_tasks=[text_task, geo_task, note_task],
        review_events=events,
        current_state=[],
    )


def test_successor_rebases_only_resolved_events_and_queues_conflicts() -> None:
    """Successor copies resolvable events only and keeps conflict packets."""
    source = _successor_source_overlay()
    source_event_dump = [event.model_dump() for event in source.review_events]
    binding = {
        "base_run_id": "run-2",
        "base_graph_revision": "graph-2",
        "prepared_image_checksum": "sha256:prepared-v2",
    }
    successor_text = _task(
        task_id="task-text-v2",
        task_type=ReviewTaskType.TEXT,
        dimensions=[ReviewDimension.TEXT],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-2"],
        allowed_actions=[ReviewAction.CORRECT_TEXT],
        **binding,
    )
    successor_geo = _task(
        task_id="task-geo-v2",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-2"],
        allowed_actions=[ReviewAction.CORRECT_GEOMETRY],
        **binding,
    )
    successor_note = _task(
        task_id="task-note-v2",
        task_type=ReviewTaskType.NOTE_LINKAGE,
        dimensions=[ReviewDimension.NOTE_LINKAGE],
        target_scope=ReviewScope.NOTE,
        target_object_ids=["note-2"],
        allowed_actions=[ReviewAction.LINK_NOTE],
        **binding,
    )
    conflict_geo = _task(
        task_id="task-conflict-geo",
        task_type=ReviewTaskType.ADJUDICATION,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-2"],
        allowed_actions=[ReviewAction.FLAG],
        status=ReviewTaskStatus.PENDING,
        related_object_ids=["span-1"],
        **binding,
    )
    conflict_note = _task(
        task_id="task-conflict-note",
        task_type=ReviewTaskType.ADJUDICATION,
        dimensions=[ReviewDimension.NOTE_LINKAGE],
        target_scope=ReviewScope.NOTE,
        target_object_ids=["note-2"],
        allowed_actions=[ReviewAction.FLAG],
        status=ReviewTaskStatus.PENDING,
        related_object_ids=["marker-unmapped"],
        **binding,
    )
    service = ReviewOverlayService()

    successor = service.create_successor(
        source,
        new_overlay_id="overlay-new",
        successor_tasks={
            "task-text-v2": successor_text,
            "task-geo-v2": successor_geo,
            "task-note-v2": successor_note,
        },
        task_id_map={
            "task-text": "task-text-v2",
            "task-geo": "task-geo-v2",
            "task-note": "task-note-v2",
        },
        object_id_map={
            "span-1": "span-2",
            "note-1": "note-2",
            "marker-1": "marker-a",
        },
        resolvable_coordinate_space_ids={"prepared-page-2"},
        event_id_map={"evt-text": "evt-text-v2"},
        conflict_tasks=[conflict_geo, conflict_note],
    )

    assert successor.overlay_id == "overlay-new"
    assert successor.predecessor_overlay_id == "overlay-old"
    assert successor.source_run_id == "run-2"
    assert successor.base_graph_revision == "graph-2"
    assert successor.prepared_image_checksum == "sha256:prepared-v2"
    assert [event.event_id for event in successor.review_events] == ["evt-text-v2"]
    copied = successor.review_events[0]
    assert isinstance(copied, CorrectTextReviewEvent)
    assert copied.task_id == "task-text-v2"
    assert copied.target_object_id == "span-2"
    assert copied.base_run_id == "run-2"
    assert copied.base_graph_revision == "graph-2"
    assert copied.text_diplomatic == "emended"

    task_ids = {task.task_id for task in successor.review_tasks}
    assert task_ids == {
        "task-text-v2",
        "task-geo-v2",
        "task-note-v2",
        "task-conflict-geo",
        "task-conflict-note",
    }
    by_id = {task.task_id: task for task in successor.review_tasks}
    assert by_id["task-conflict-geo"].task_type == ReviewTaskType.ADJUDICATION
    assert by_id["task-conflict-geo"].status == ReviewTaskStatus.PENDING
    assert by_id["task-conflict-note"].task_type == ReviewTaskType.ADJUDICATION
    assert by_id["task-conflict-note"].status == ReviewTaskStatus.PENDING

    assert source.overlay_id == "overlay-old"
    assert [event.model_dump() for event in source.review_events] == source_event_dump

    assert len(successor.current_state) == 1
    state = successor.current_state[0]
    assert state.object_id == "span-2"
    assert state.scope == ReviewScope.SPAN
    assert state.text_diplomatic_override == "emended"
    assert state.applied_event_ids == ["evt-text-v2"]
    assert state.trust_state == TrustState.CORRECTED


def _region_revision(
    *,
    region_id: str,
    line_ids: list[str],
    reading_order_index: int,
) -> RegionRevision:
    """Return a resolvable region revision for structural rebase fixtures."""
    return RegionRevision(
        region_id=region_id,
        region_kind=RegionKind.BODY,
        reading_order_index=reading_order_index,
        polygon=_polygon(),
        line_ids=line_ids,
    )


def _split_source_overlay() -> PageOverlay:
    """Build a predecessor containing one fully remappable split event."""
    layout_task = _task(
        task_id="task-split",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.REGION,
        target_object_ids=["region-src"],
        allowed_actions=[ReviewAction.SPLIT_REGION],
    )
    event = SplitRegionReviewEvent(
        **_event_base(
            event_id="evt-split",
            task_id="task-split",
            target_object_id="region-src",
            target_scope=ReviewScope.REGION,
            review_dimensions=[ReviewDimension.STRUCTURE],
            prior_trust_state=TrustState.MACHINE,
            new_trust_state=TrustState.CORRECTED,
        ),
        source_region_id="region-src",
        replacement_regions=[
            _region_revision(
                region_id="region-a",
                line_ids=["line-1", "line-2"],
                reading_order_index=1,
            ),
            _region_revision(
                region_id="region-b",
                line_ids=["line-3"],
                reading_order_index=2,
            ),
        ],
    )
    return PageOverlay(
        schema_version="1.0.0",
        overlay_id="overlay-split-old",
        page_id="page-1",
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
        review_tasks=[layout_task],
        review_events=[event],
        current_state=[],
    )


def test_successor_rebases_split_region_nested_ids() -> None:
    """Successor remaps nested region and line ids on a copied split event."""
    source = _split_source_overlay()
    binding = {
        "base_run_id": "run-2",
        "base_graph_revision": "graph-2",
        "prepared_image_checksum": "sha256:prepared-v2",
    }
    successor_task = _task(
        task_id="task-split-v2",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.REGION,
        target_object_ids=["region-src-v2"],
        allowed_actions=[ReviewAction.SPLIT_REGION],
        **binding,
    )
    service = ReviewOverlayService()

    successor = service.create_successor(
        source,
        new_overlay_id="overlay-split-new",
        successor_tasks=[successor_task],
        task_id_map={"task-split": "task-split-v2"},
        object_id_map={
            "region-src": "region-src-v2",
            "region-a": "region-a-v2",
            "region-b": "region-b-v2",
            "line-1": "line-1-v2",
            "line-2": "line-2-v2",
            "line-3": "line-3-v2",
        },
        resolvable_coordinate_space_ids={"prepared-page-1"},
        event_id_map={"evt-split": "evt-split-v2"},
        conflict_tasks=[],
    )

    assert [event.event_id for event in successor.review_events] == ["evt-split-v2"]
    copied = successor.review_events[0]
    assert isinstance(copied, SplitRegionReviewEvent)
    assert copied.task_id == "task-split-v2"
    assert copied.target_object_id == "region-src-v2"
    assert copied.source_region_id == "region-src-v2"
    assert [region.region_id for region in copied.replacement_regions] == [
        "region-a-v2",
        "region-b-v2",
    ]
    assert copied.replacement_regions[0].line_ids == ["line-1-v2", "line-2-v2"]
    assert copied.replacement_regions[1].line_ids == ["line-3-v2"]
    assert len(copied.replacement_regions) == 2


def test_successor_rejects_missing_mapped_task_ids() -> None:
    """Missing mapped successor task ids are hard ValueError failures."""
    source = _successor_source_overlay()
    service = ReviewOverlayService()

    with pytest.raises(ValueError, match="successor_tasks missing mapped task ids"):
        service.create_successor(
            source,
            new_overlay_id="overlay-bad",
            successor_tasks={},
            task_id_map={"task-text": "task-text-missing"},
            object_id_map={"span-1": "span-2"},
            resolvable_coordinate_space_ids={"prepared-page-2"},
            event_id_map={"evt-text": "evt-text-v2"},
            conflict_tasks=[],
        )


def test_successor_split_rebind_rejects_non_mapping_region(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Corrupt split dump shapes must raise ValueError, not shrink regions."""
    source = _split_source_overlay()
    binding = {
        "base_run_id": "run-2",
        "base_graph_revision": "graph-2",
        "prepared_image_checksum": "sha256:prepared-v2",
    }
    successor_task = _task(
        task_id="task-split-v2",
        task_type=ReviewTaskType.LAYOUT,
        dimensions=[ReviewDimension.STRUCTURE],
        target_scope=ReviewScope.REGION,
        target_object_ids=["region-src-v2"],
        allowed_actions=[ReviewAction.SPLIT_REGION],
        **binding,
    )
    original_dump = SplitRegionReviewEvent.model_dump

    def corrupt_dump(
        self: SplitRegionReviewEvent,
        *args: object,
        **kwargs: object,
    ) -> dict[str, object]:
        data = original_dump(self, *args, **kwargs)
        regions = list(data["replacement_regions"])
        regions[1] = "not-a-mapping"
        data["replacement_regions"] = regions
        return data

    monkeypatch.setattr(SplitRegionReviewEvent, "model_dump", corrupt_dump)
    service = ReviewOverlayService()

    with pytest.raises(ValueError, match="replacement region must be a mapping") as err:
        service.create_successor(
            source,
            new_overlay_id="overlay-split-bad",
            successor_tasks=[successor_task],
            task_id_map={"task-split": "task-split-v2"},
            object_id_map={
                "region-src": "region-src-v2",
                "region-a": "region-a-v2",
                "region-b": "region-b-v2",
                "line-1": "line-1-v2",
                "line-2": "line-2-v2",
                "line-3": "line-3-v2",
            },
            resolvable_coordinate_space_ids={"prepared-page-1"},
            event_id_map={"evt-split": "evt-split-v2"},
            conflict_tasks=[],
        )
    # Pydantic ValidationError subclasses ValueError; require the explicit
    # dump-shape guard rather than a later shrunk-list validation failure.
    assert type(err.value) is ValueError
