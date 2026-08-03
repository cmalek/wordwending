# Copyright (C) 2026 Chris Malek.
"""Deterministic replay and successor construction for review overlays."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from bochord.models import (
    CorrectGeometryReviewEvent,
    CorrectStyleReviewEvent,
    CorrectTextReviewEvent,
    FlagReviewEvent,
    LinkNoteReviewEvent,
    MarkIllegibleReviewEvent,
    MergeRegionReviewEvent,
    OverlayState,
    PageOverlay,
    ReclassifyRegionReviewEvent,
    RegionRevision,
    ReorderReviewEvent,
    ResolveFlagReviewEvent,
    ReviewAction,
    ReviewDimension,
    SplitRegionReviewEvent,
    UnlinkNoteReviewEvent,
)

if TYPE_CHECKING:
    from bochord.models import ReviewEvent, ReviewScope, ReviewTask


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

    def create_successor(  # noqa: PLR0913
        self,
        overlay: PageOverlay,
        *,
        new_overlay_id: str,
        successor_tasks: Mapping[str, ReviewTask] | Sequence[ReviewTask],
        task_id_map: Mapping[str, str],
        object_id_map: Mapping[str, str],
        resolvable_coordinate_space_ids: set[str],
        event_id_map: Mapping[str, str],
        conflict_tasks: Sequence[ReviewTask],
    ) -> PageOverlay:
        """
        Build a rebased successor overlay without mutating the predecessor.

        Copies only events whose task, target, nested payload ids, coordinate
        spaces, and caller-supplied event ids all resolve explicitly. Conflict
        packets are retained exactly as supplied; the service never invents
        adjudication tasks.

        Args:
            overlay: Predecessor overlay whose events may be rebased.

        Keyword Args:
            new_overlay_id: Stable identity for the successor overlay.
            successor_tasks: New-run tasks already bound to the successor
                evidence; may be a task-id map or a list.
            task_id_map: Explicit old→new task id map; every value must exist
                in ``successor_tasks``.
            object_id_map: Explicit old→new object id map for targets and
                nested marker/region/line/note ids.
            resolvable_coordinate_space_ids: Coordinate spaces still valid on
                the successor evidence; geometry outside this set is skipped.
            event_id_map: Caller-supplied old→new event ids for copied events.
            conflict_tasks: Caller-supplied PENDING ADJUDICATION packets for
                unresolved predecessor events.

        Returns:
            A distinct successor ``PageOverlay`` with materialized state.

        Raises:
            ValueError: If a mapped successor task is missing or successor
                evidence bindings cannot be derived.

        """
        tasks = _normalize_tasks(successor_tasks)
        _require_mapped_tasks(task_id_map, tasks)
        run_id, graph_revision, checksum = _successor_bindings(tasks, conflict_tasks)
        copied: list[ReviewEvent] = []
        for event in overlay.review_events:
            rebound = self._try_rebind_event(
                event,
                tasks=tasks,
                task_id_map=task_id_map,
                object_id_map=object_id_map,
                resolvable_coordinate_space_ids=resolvable_coordinate_space_ids,
                event_id_map=event_id_map,
                run_id=run_id,
                graph_revision=graph_revision,
            )
            if rebound is not None:
                copied.append(rebound)
        successor = PageOverlay(
            schema_version=overlay.schema_version,
            overlay_id=new_overlay_id,
            page_id=overlay.page_id,
            source_run_id=run_id,
            base_graph_revision=graph_revision,
            prepared_image_checksum=checksum,
            predecessor_overlay_id=overlay.overlay_id,
            review_tasks=[*tasks.values(), *conflict_tasks],
            review_events=copied,
            current_state=[],
        )
        states = self.materialize(successor)
        return successor.model_copy(update={"current_state": states})

    def _try_rebind_event(  # noqa: PLR0913
        self,
        event: ReviewEvent,
        *,
        tasks: Mapping[str, ReviewTask],
        task_id_map: Mapping[str, str],
        object_id_map: Mapping[str, str],
        resolvable_coordinate_space_ids: set[str],
        event_id_map: Mapping[str, str],
        run_id: str,
        graph_revision: str,
    ) -> ReviewEvent | None:
        """
        Rebind one event when every required id resolves; otherwise skip it.

        Keyword Args:
            tasks: Successor task map keyed by new task id.
            task_id_map: Explicit old→new task id map.
            object_id_map: Explicit old→new object id map.
            resolvable_coordinate_space_ids: Valid geometry spaces.
            event_id_map: Caller-supplied old→new event ids.
            run_id: Successor machine run id.
            graph_revision: Successor graph revision.

        Args:
            event: Predecessor event considered for copy.

        Returns:
            A distinct remapped event, or ``None`` when the event conflicts.

        """
        new_task_id = task_id_map.get(event.task_id)
        new_event_id = event_id_map.get(event.event_id)
        if new_task_id is None or new_event_id is None:
            return None
        if new_task_id not in tasks:
            return None
        if event.target_object_id not in object_id_map:
            return None
        nested = _nested_object_ids(event)
        if any(object_id not in object_id_map for object_id in nested):
            return None
        spaces = _coordinate_space_ids(event)
        if any(space_id not in resolvable_coordinate_space_ids for space_id in spaces):
            return None
        return _rebind_event(
            event,
            new_event_id=new_event_id,
            new_task_id=new_task_id,
            object_id_map=object_id_map,
            run_id=run_id,
            graph_revision=graph_revision,
        )

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


def _normalize_tasks(
    successor_tasks: Mapping[str, ReviewTask] | Sequence[ReviewTask],
) -> dict[str, ReviewTask]:
    """
    Normalize a successor task map or list into a task-id dictionary.

    Args:
        successor_tasks: Caller-supplied successor tasks.

    Returns:
        Tasks keyed by ``task_id``.

    Raises:
        ValueError: If a list contains duplicate task ids.

    """
    if isinstance(successor_tasks, Mapping):
        return dict(successor_tasks)
    tasks = {task.task_id: task for task in successor_tasks}
    if len(tasks) != len(successor_tasks):
        msg = "successor_tasks must have unique task ids"
        raise ValueError(msg)
    return tasks


def _require_mapped_tasks(
    task_id_map: Mapping[str, str],
    tasks: Mapping[str, ReviewTask],
) -> None:
    """
    Reject task maps that point at missing successor tasks.

    Args:
        task_id_map: Explicit old→new task id map.
        tasks: Normalized successor task map.

    Raises:
        ValueError: If any mapped new task id is absent from ``tasks``.

    """
    missing = sorted({new_id for new_id in task_id_map.values() if new_id not in tasks})
    if missing:
        msg = f"successor_tasks missing mapped task ids: {missing}"
        raise ValueError(msg)


def _successor_bindings(
    tasks: Mapping[str, ReviewTask],
    conflict_tasks: Sequence[ReviewTask],
) -> tuple[str, str, str]:
    """
    Derive successor run, graph, and checksum from caller-supplied tasks.

    Args:
        tasks: Normalized successor task map.
        conflict_tasks: Caller-supplied conflict adjudication packets.

    Returns:
        ``(run_id, graph_revision, prepared_image_checksum)``.

    Raises:
        ValueError: If no tasks are supplied to derive bindings from.

    """
    probe = next(iter(tasks.values()), None)
    if probe is None and conflict_tasks:
        probe = conflict_tasks[0]
    if probe is None:
        msg = "successor requires successor_tasks or conflict_tasks"
        raise ValueError(msg)
    return probe.base_run_id, probe.base_graph_revision, probe.prepared_image_checksum


def _nested_object_ids(event: ReviewEvent) -> list[str]:
    """
    Collect nested marker/region/line/note ids that must remap.

    Args:
        event: Predecessor event under consideration.

    Returns:
        Nested object ids referenced by the event payload.

    """
    if isinstance(event, (LinkNoteReviewEvent, UnlinkNoteReviewEvent)):
        return [*event.marker_span_ids, event.note_id]
    if isinstance(event, SplitRegionReviewEvent):
        ids = [event.source_region_id]
        for region in event.replacement_regions:
            ids.append(region.region_id)
            ids.extend(region.line_ids)
        return ids
    if isinstance(event, MergeRegionReviewEvent):
        ids = list(event.source_region_ids)
        ids.append(event.replacement_region.region_id)
        ids.extend(event.replacement_region.line_ids)
        return ids
    if isinstance(event, ReorderReviewEvent):
        return list(event.ordered_object_ids)
    return []


def _coordinate_space_ids(event: ReviewEvent) -> list[str]:
    """
    Collect coordinate-space ids named by event geometry payloads.

    Args:
        event: Predecessor event under consideration.

    Returns:
        Coordinate-space ids that must remain resolvable.

    """
    spaces: list[str] = []
    if isinstance(event, CorrectGeometryReviewEvent):
        if event.bounding_box is not None:
            spaces.append(event.bounding_box.coordinate_space_id)
        if event.polygon is not None:
            spaces.append(event.polygon.coordinate_space_id)
        return spaces
    if isinstance(event, SplitRegionReviewEvent):
        for region in event.replacement_regions:
            spaces.extend(_region_coordinate_space_ids(region))
        return spaces
    if isinstance(event, MergeRegionReviewEvent):
        return _region_coordinate_space_ids(event.replacement_region)
    return spaces


def _region_coordinate_space_ids(region: RegionRevision) -> list[str]:
    """
    Collect coordinate-space ids from one region revision.

    Args:
        region: Region revision carrying optional box/polygon geometry.

    Returns:
        Named coordinate-space ids on the revision.

    """
    spaces: list[str] = []
    if region.bounding_box is not None:
        spaces.append(region.bounding_box.coordinate_space_id)
    if region.polygon is not None:
        spaces.append(region.polygon.coordinate_space_id)
    return spaces


def _rebind_event(  # noqa: PLR0913
    event: ReviewEvent,
    *,
    new_event_id: str,
    new_task_id: str,
    object_id_map: Mapping[str, str],
    run_id: str,
    graph_revision: str,
) -> ReviewEvent:
    """
    Build a distinct remapped copy of one resolvable predecessor event.

    Keyword Args:
        new_event_id: Caller-supplied successor event id.
        new_task_id: Mapped successor task id.
        object_id_map: Explicit old→new object id map.
        run_id: Successor machine run id.
        graph_revision: Successor graph revision.

    Args:
        event: Predecessor event that fully resolved.

    Returns:
        Remapped event instance of the same concrete type.

    """
    data = event.model_dump(mode="python")
    data["event_id"] = new_event_id
    data["task_id"] = new_task_id
    data["target_object_id"] = object_id_map[event.target_object_id]
    data["base_run_id"] = run_id
    data["base_graph_revision"] = graph_revision
    if isinstance(event, (LinkNoteReviewEvent, UnlinkNoteReviewEvent)):
        data["marker_span_ids"] = [
            object_id_map[item] for item in event.marker_span_ids
        ]
        data["note_id"] = object_id_map[event.note_id]
    elif isinstance(event, SplitRegionReviewEvent):
        data["source_region_id"] = object_id_map[event.source_region_id]
        regions = data["replacement_regions"]
        if not isinstance(regions, list):
            msg = "replacement_regions must be a list"
            raise TypeError(msg)
        data["replacement_regions"] = [
            _rebind_region(region, object_id_map)
            for region in regions
            if isinstance(region, Mapping)
        ]
    elif isinstance(event, MergeRegionReviewEvent):
        data["source_region_ids"] = [
            object_id_map[item] for item in event.source_region_ids
        ]
        replacement = data["replacement_region"]
        if not isinstance(replacement, Mapping):
            msg = "replacement_region must be a mapping"
            raise TypeError(msg)
        data["replacement_region"] = _rebind_region(replacement, object_id_map)
    elif isinstance(event, ReorderReviewEvent):
        data["ordered_object_ids"] = [
            object_id_map[item] for item in event.ordered_object_ids
        ]
    return type(event).model_validate(data)


def _rebind_region(
    region: Mapping[str, object],
    object_id_map: Mapping[str, str],
) -> dict[str, object]:
    """
    Remap region and line ids inside one region revision payload.

    Args:
        region: Region revision mapping from ``model_dump``.
        object_id_map: Explicit old→new object id map.

    Returns:
        Remapped region revision dictionary.

    """
    payload = dict(region)
    payload["region_id"] = object_id_map[str(payload["region_id"])]
    raw_lines = payload.get("line_ids", [])
    if not isinstance(raw_lines, list):
        msg = "region line_ids must be a list"
        raise TypeError(msg)
    payload["line_ids"] = [object_id_map[str(item)] for item in raw_lines]
    return payload


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
