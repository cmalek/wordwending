# Copyright (C) 2026 Chris Malek.
"""Apply materialized OverlayState rows onto an accepted BundlePage graph."""

from __future__ import annotations

from typing import Any

from wordwending.models import (
    BundlePage,
    LineRecord,
    NoteRecord,
    OverlayState,
    RegionRecord,
    ReviewDimension,
    ReviewScope,
    ReviewSummary,
    SpanRecord,
)

#: Graph node types that carry trust/review and optional leaf overrides.
_GraphNode = SpanRecord | NoteRecord | RegionRecord | LineRecord


class GraphRebaseService:
    """Apply materialized OverlayState rows onto an accepted BundlePage graph."""

    def rebase_page(
        self,
        page: BundlePage,
        states: list[OverlayState],
        *,
        new_graph_revision: str,
    ) -> BundlePage:
        """
        Return a new page with leaf overlay overrides and a bumped revision.

        Structural split/merge/reorder remain audit/trust-only in v1: no graph
        surgery. ``illegible`` updates trust/review via existing node fields
        only; the flag itself stays on overlay state (no ``BundlePage.illegible``).

        Args:
            page: Accepted page graph to rebase.
            states: Materialized overlay states to apply in order.

        Keyword Args:
            new_graph_revision: Revision id written onto the returned page.

        Returns:
            A distinct ``BundlePage`` with overrides applied and
            ``graph_revision=new_graph_revision``.

        Raises:
            ValueError: If an overlay ``object_id`` cannot be resolved for its
                scope (message includes the missing id).

        """
        result = page.model_copy(deep=True)
        indexes = _indexes(result)
        for state in states:
            target = _resolve(indexes, state)
            _apply_trust_and_review(target, state)
            _apply_leaf_overrides(target, state)
        return result.model_copy(update={"graph_revision": new_graph_revision})


def _indexes(page: BundlePage) -> dict[ReviewScope, dict[str, _GraphNode]]:
    """
    Index page graph nodes by scope and stable object id.

    Args:
        page: Page whose children are indexed.

    Returns:
        Scope → object-id → mutable node mapping.

    """
    return {
        ReviewScope.SPAN: {span.span_id: span for span in page.spans},
        ReviewScope.NOTE: {note.note_id: note for note in page.notes},
        ReviewScope.REGION: {region.region_id: region for region in page.regions},
        ReviewScope.LINE: {line.line_id: line for line in page.lines},
    }


def _resolve(
    indexes: dict[ReviewScope, dict[str, _GraphNode]],
    state: OverlayState,
) -> _GraphNode:
    """
    Resolve the graph node matching ``state.object_id`` and ``state.scope``.

    Args:
        indexes: Scope → object-id → node maps for the working page copy.
        state: Overlay state naming the target.

    Returns:
        The mutable target node.

    Raises:
        ValueError: If the object id is unknown for the given scope.

    """
    by_scope = indexes.get(state.scope)
    if by_scope is None:
        msg = f"unsupported overlay scope for rebase: {state.scope}"
        raise ValueError(msg)
    target = by_scope.get(state.object_id)
    if target is None:
        msg = f"unknown object_id for overlay rebase: {state.object_id}"
        raise ValueError(msg)
    return target


def _apply_trust_and_review(target: _GraphNode, state: OverlayState) -> None:
    """
    Copy overlay trust and review audit fields onto the target node.

    Args:
        target: Graph node receiving trust/review updates.
        state: Materialized overlay state for the target.

    """
    target.trust_state = state.trust_state
    last_event_id = state.applied_event_ids[-1] if state.applied_event_ids else None
    target.review = ReviewSummary(
        reviewed_dimensions=list(state.reviewed_dimensions),
        corrected_dimensions=list(state.corrected_dimensions),
        last_event_id=last_event_id,
        event_ids=list(state.applied_event_ids),
    )


def _apply_leaf_overrides(target: _GraphNode, state: OverlayState) -> None:
    """
    Apply leaf override fields present on ``state`` onto ``target``.

    Illegible does not invent a graph field: trust/review already updated.
    Structural split/merge/reorder produce no graph surgery here.

    Args:
        target: Graph node receiving leaf overrides.
        state: Materialized overlay state for the target.

    """
    updates: dict[str, Any] = {}
    if state.text_diplomatic_override is not None and isinstance(
        target, (SpanRecord, NoteRecord)
    ):
        updates["text_diplomatic"] = state.text_diplomatic_override
    if isinstance(target, SpanRecord):
        if state.typography_override is not None:
            updates["typography"] = state.typography_override
        if state.role_overrides:
            updates["roles"] = list(state.role_overrides)
    if state.bounding_box_override is not None and hasattr(target, "bounding_box"):
        updates["bounding_box"] = state.bounding_box_override
    if state.polygon_override is not None and hasattr(target, "polygon"):
        updates["polygon"] = state.polygon_override
    if state.region_kind_override is not None and isinstance(target, RegionRecord):
        updates["region_kind"] = state.region_kind_override
    if isinstance(target, NoteRecord) and (
        state.linked_marker_span_ids
        or ReviewDimension.NOTE_LINKAGE in state.corrected_dimensions
    ):
        updates["linked_marker_span_ids"] = list(state.linked_marker_span_ids)
    # ponytail: illegible stays on OverlayState; ReviewSummary has no field for it
    for key, value in updates.items():
        setattr(target, key, value)
