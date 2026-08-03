# Copyright (C) 2026 Chris Malek.
"""Deterministic replay of append-only review overlay events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bochord.models import (
    CorrectGeometryReviewEvent,
    CorrectStyleReviewEvent,
    CorrectTextReviewEvent,
    FlagReviewEvent,
    LinkNoteReviewEvent,
    MarkIllegibleReviewEvent,
    OverlayState,
    ReclassifyRegionReviewEvent,
    ResolveFlagReviewEvent,
    ReviewAction,
    ReviewDimension,
    UnlinkNoteReviewEvent,
)

if TYPE_CHECKING:
    from bochord.models import PageOverlay, ReviewEvent, ReviewScope


#: Actions that record a corrected dimension without graph mutation here.
_CORRECTIVE_ACTIONS: frozenset[ReviewAction] = frozenset(
    {
        ReviewAction.CORRECT_TEXT,
        ReviewAction.CORRECT_STYLE,
        ReviewAction.CORRECT_GEOMETRY,
        ReviewAction.RECLASSIFY_REGION,
        ReviewAction.MARK_ILLEGIBLE,
        ReviewAction.LINK_NOTE,
        ReviewAction.UNLINK_NOTE,
        ReviewAction.SPLIT_REGION,
        ReviewAction.MERGE_REGION,
        ReviewAction.REORDER,
    }
)


class ReviewOverlayService:
    """Rebuild overlay state by replaying append-only review events in order."""

    def materialize(self, overlay: PageOverlay) -> list[OverlayState]:
        """
        Replay ``overlay.review_events`` into per-object overlay state.

        Ignores any cached ``current_state`` on the overlay. Structural
        split/merge/reorder events update audit/trust fields only; they do not
        mutate a ``BundlePage``.

        Args:
            overlay: Validated page overlay whose event log is truth.

        Returns:
            Materialized states keyed by recorded ``(object_id, scope)`` order.

        """
        states: dict[tuple[str, ReviewScope], OverlayState] = {}
        order: list[tuple[str, ReviewScope]] = []
        for event in overlay.review_events:
            key = (event.target_object_id, event.target_scope)
            state = states.get(key)
            if state is None:
                state = OverlayState(
                    object_id=event.target_object_id,
                    scope=event.target_scope,
                    trust_state=event.new_trust_state,
                )
                states[key] = state
                order.append(key)
            self._apply_event(state, event)
        return [states[key] for key in order]

    def _apply_event(self, state: OverlayState, event: ReviewEvent) -> None:
        """
        Apply one append-only event onto a mutable overlay state.

        Args:
            state: Accumulator for ``(target_object_id, target_scope)``.
            event: Next event in recorded order.

        """
        self._apply_audit_fields(state, event)
        self._apply_payload(state, event)

    def _apply_audit_fields(self, state: OverlayState, event: ReviewEvent) -> None:
        """
        Record trust, applied event id, and reviewed/corrected dimensions.

        Args:
            state: Accumulator for ``(target_object_id, target_scope)``.
            event: Next event in recorded order.

        """
        state.trust_state = event.new_trust_state
        state.applied_event_ids = [*state.applied_event_ids, event.event_id]
        state.reviewed_dimensions = _union_dimensions(
            state.reviewed_dimensions,
            event.review_dimensions,
        )
        if event.action in _CORRECTIVE_ACTIONS:
            state.corrected_dimensions = _union_dimensions(
                state.corrected_dimensions,
                event.review_dimensions,
            )

    def _apply_payload(self, state: OverlayState, event: ReviewEvent) -> None:
        """
        Apply event-specific override fields named by the event contract.

        Structural split/merge/reorder retain audit fields only.

        Args:
            state: Accumulator for ``(target_object_id, target_scope)``.
            event: Next event in recorded order.

        """
        if isinstance(event, CorrectTextReviewEvent):
            state.text_diplomatic_override = event.text_diplomatic
        elif isinstance(event, CorrectStyleReviewEvent):
            state.typography_override = event.new_typography
            state.role_overrides = list(event.new_roles)
        elif isinstance(event, CorrectGeometryReviewEvent):
            if event.bounding_box is not None:
                state.bounding_box_override = event.bounding_box
            if event.polygon is not None:
                state.polygon_override = event.polygon
        elif isinstance(event, ReclassifyRegionReviewEvent):
            state.region_kind_override = event.new_region_kind
        elif isinstance(event, LinkNoteReviewEvent):
            state.linked_marker_span_ids = _union_ids(
                state.linked_marker_span_ids,
                event.marker_span_ids,
            )
        elif isinstance(event, UnlinkNoteReviewEvent):
            remove = set(event.marker_span_ids)
            state.linked_marker_span_ids = [
                marker_id
                for marker_id in state.linked_marker_span_ids
                if marker_id not in remove
            ]
        elif isinstance(event, MarkIllegibleReviewEvent):
            state.illegible = True
        elif isinstance(event, FlagReviewEvent):
            state.active_flag_ids = [*state.active_flag_ids, event.flag_id]
        elif isinstance(event, ResolveFlagReviewEvent):
            state.active_flag_ids = [
                flag_id
                for flag_id in state.active_flag_ids
                if flag_id != event.flag_id
            ]


def _union_dimensions(
    existing: list[ReviewDimension],
    incoming: list[ReviewDimension],
) -> list[ReviewDimension]:
    """
    Append novel review dimensions while preserving first-seen order.

    Args:
        existing: Dimensions already recorded on the state.
        incoming: Dimensions inspected or corrected by the event.

    Returns:
        Ordered unique dimension list.

    """
    seen = set(existing)
    merged = list(existing)
    for dimension in incoming:
        if dimension not in seen:
            merged.append(dimension)
            seen.add(dimension)
    return merged


def _union_ids(existing: list[str], incoming: list[str]) -> list[str]:
    """
    Append novel string ids while preserving first-seen order.

    Args:
        existing: Ids already recorded on the state.
        incoming: Ids contributed by the event.

    Returns:
        Ordered unique id list.

    """
    seen = set(existing)
    merged = list(existing)
    for item in incoming:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged
