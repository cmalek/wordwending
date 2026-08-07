# Copyright (C) 2026 Chris Malek.
"""Review overlay CLI commands."""

from __future__ import annotations

from pathlib import Path

import click
from pydantic import TypeAdapter, ValidationError

from wordwending.models import (
    BundlePage,
    OverlayState,
    PageOverlay,
    ReviewEvent,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
)
from wordwending.services.bundle_layout import BundleLayoutService
from wordwending.services.review_markup import HumanMarkupService
from wordwending.services.review_overlay import ReviewOverlayService

#: Parses one JSONL review-event payload into a validated event model.
_REVIEW_EVENT_ADAPTER: TypeAdapter[ReviewEvent] = TypeAdapter(ReviewEvent)


@click.group()
def review() -> None:
    """Apply and materialize human review overlays on document bundles."""


@review.command("apply")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Filesystem root for one assembled document bundle tree.",
)
@click.option(
    "--overlay",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="PageOverlay JSON file whose review events are appended.",
)
@click.option("--page-id", required=True, help="Stable page identifier to update.")
def review_apply(bundle_root: Path, overlay: Path, page_id: str) -> None:
    """
    Append overlay review events and write materialized overlay state.

    Args:
        bundle_root: Filesystem root for one document bundle tree.
        overlay: PageOverlay JSON file whose review events are appended.
        page_id: Stable page identifier that must match the overlay.

    Side Effects:
        Appends new events to ``overlays/review_events.jsonl`` and overwrites
        ``overlays/current_state.json`` from the full append-only history.

    Raises:
        click.ClickException: When inputs fail validation or I/O fails.

    """
    layout = BundleLayoutService()
    replay = ReviewOverlayService()
    try:
        page_overlay = PageOverlay.model_validate_json(
            overlay.read_text(encoding="utf-8")
        )
        _ensure_overlay_page_id(page_overlay, page_id)
        page_number = _resolve_page_number(layout, bundle_root, page_id)
        page = layout.read_page_graph(bundle_root, page_number)
        _validate_overlay_tasks_on_page(page, page_overlay)
        appended = _append_new_review_events(
            layout,
            bundle_root,
            page_number,
            page_overlay.review_events,
        )
        states = _materialize_review_states(
            replay,
            layout,
            bundle_root,
            page_number,
            page_id,
        )
        layout.write_overlay_state(bundle_root, page_number, states)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"page_id: {page_id}")
    click.echo(f"events_appended: {appended}")
    click.echo(f"states: {len(states)}")


@review.command("materialize")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Filesystem root for one assembled document bundle tree.",
)
@click.option("--page-id", required=True, help="Stable page identifier to update.")
def review_materialize(bundle_root: Path, page_id: str) -> None:
    """
    Replay append-only review history into ``overlays/current_state.json``.

    Args:
        bundle_root: Filesystem root for one document bundle tree.
        page_id: Stable page identifier whose review history is replayed.

    Side Effects:
        Overwrites ``overlays/current_state.json`` from ``review_events.jsonl``.

    Raises:
        click.ClickException: When the page is missing or replay fails.

    """
    layout = BundleLayoutService()
    replay = ReviewOverlayService()
    try:
        page_number = _resolve_page_number(layout, bundle_root, page_id)
        states = _materialize_review_states(
            replay,
            layout,
            bundle_root,
            page_number,
            page_id,
        )
        layout.write_overlay_state(bundle_root, page_number, states)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"page_id: {page_id}")
    click.echo(f"states: {len(states)}")


def _ensure_overlay_page_id(overlay: PageOverlay, page_id: str) -> None:
    """
    Reject overlay submissions whose page id does not match the CLI flag.

    Args:
        overlay: Overlay loaded from the operator submission file.
        page_id: Page id supplied on the command line.

    Raises:
        ValueError: If ``overlay.page_id`` differs from ``page_id``.

    """
    if overlay.page_id != page_id:
        msg = (
            f"overlay page_id {overlay.page_id!r} "
            f"does not match --page-id {page_id!r}"
        )
        raise ValueError(msg)


def _resolve_page_number(
    layout: BundleLayoutService,
    bundle_root: Path,
    page_id: str,
) -> int:
    """
    Resolve one bundle page number from its stable page id.

    Args:
        layout: Bundle layout reader.
        bundle_root: Filesystem root for one document bundle tree.
        page_id: Stable page identifier to locate.

    Returns:
        1-based page index within the document bundle.

    Raises:
        ValueError: If no page manifest matches ``page_id``.

    """
    document = layout.read_document_manifest(bundle_root)
    for page_number in range(1, document.page_count + 1):
        manifest = layout.read_page_manifest(bundle_root, page_number)
        if manifest.page_id == page_id:
            return page_number
    msg = f"bundle has no page with page_id {page_id!r}"
    raise ValueError(msg)


def _parse_review_events(raw_events: list[dict[str, object]]) -> list[ReviewEvent]:
    """
    Parse JSONL review-event payloads into validated event models.

    Args:
        raw_events: Parsed JSON objects from ``read_review_events``.

    Returns:
        Validated review events in recorded order.

    """
    return [_REVIEW_EVENT_ADAPTER.validate_python(item) for item in raw_events]


def _append_new_review_events(
    layout: BundleLayoutService,
    bundle_root: Path,
    page_number: int,
    events: list[ReviewEvent],
) -> int:
    """
    Append only review events whose ids are not already recorded.

    Args:
        layout: Bundle layout writer.
        bundle_root: Filesystem root for one document bundle tree.
        page_number: 1-based page index within the document bundle.
        events: Candidate review events from one overlay submission.

    Returns:
        Count of events appended to ``review_events.jsonl``.

    """
    existing_ids = {
        event["event_id"]
        for event in layout.read_review_events(bundle_root, page_number)
        if "event_id" in event
    }
    new_events = [event for event in events if event.event_id not in existing_ids]
    layout.append_review_events(bundle_root, page_number, new_events)
    return len(new_events)


def _materialize_review_states(
    replay: ReviewOverlayService,
    layout: BundleLayoutService,
    bundle_root: Path,
    page_number: int,
    page_id: str,
) -> list[OverlayState]:
    """
    Replay append-only review history for one page.

    Args:
        replay: Overlay replay service.
        layout: Bundle layout reader.
        bundle_root: Filesystem root for one document bundle tree.
        page_number: 1-based page index within the document bundle.
        page_id: Stable page identifier used for replay scaffolding.

    Returns:
        Materialized overlay states for reviewed objects.

    """
    events = _parse_review_events(
        layout.read_review_events(bundle_root, page_number)
    )
    overlay = PageOverlay.model_construct(
        schema_version="1.0.0",
        overlay_id="cli-replay",
        page_id=page_id,
        source_run_id="cli-replay",
        base_graph_revision="cli-replay",
        prepared_image_checksum="cli-replay",
        review_events=events,
        review_tasks=[],
        current_state=[],
    )
    return replay.materialize(overlay)


def _validate_overlay_tasks_on_page(
    page: BundlePage,
    overlay: PageOverlay,
) -> None:
    """
    Ensure overlay task targets exist on the accepted page graph.

    Args:
        page: Accepted page graph for the bundle page.
        overlay: Overlay whose task packets are being applied.

    Raises:
        ValueError: If a task target id is absent from ``page``.

    """
    if not overlay.review_tasks:
        return
    first_task = overlay.review_tasks[0]
    markup = HumanMarkupService(
        first_task.guideline_id,
        first_task.guideline_version,
        first_task.calibration_example_ids,
    )
    for task in overlay.review_tasks:
        if (
            task.task_type == ReviewTaskType.LAYOUT
            and task.target_scope != ReviewScope.REGION
        ):
            _validate_object_ids_for_scope(page, task)
        else:
            _validate_task_targets(markup, page, task)


def _validate_object_ids_for_scope(page: BundlePage, task: ReviewTask) -> None:
    """
    Validate task target ids against the page graph for one review scope.

    Args:
        page: Accepted page graph for the bundle page.
        task: Review task whose target ids must resolve on ``page``.

    Raises:
        ValueError: If any target id is absent from ``page``.

    """
    if task.target_scope == ReviewScope.SPAN:
        known = {span.span_id for span in page.spans}
        label = "span ids"
    elif task.target_scope == ReviewScope.REGION:
        known = {region.region_id for region in page.regions}
        label = "region ids"
    elif task.target_scope == ReviewScope.NOTE:
        known = {note.note_id for note in page.notes}
        label = "note ids"
    elif task.target_scope == ReviewScope.PAGE:
        known = {page.page_id}
        label = "page ids"
    else:
        msg = f"unsupported review target scope {task.target_scope.value!r}"
        raise ValueError(msg)
    unknown = sorted(set(task.target_object_ids) - known)
    if unknown:
        msg = f"{label}; unknown: {unknown}"
        raise ValueError(msg)


def _validate_task_targets(
    markup: HumanMarkupService,
    page: BundlePage,
    task: ReviewTask,
) -> None:
    """
    Validate one review task's targets against the page graph.

    Args:
        markup: Human markup service bound to overlay guidance.
        page: Accepted page graph for the bundle page.
        task: Review task whose target ids must resolve on ``page``.

    Raises:
        ValueError: If ``task`` references unknown page object ids.

    """
    kwargs = {
        "run_id": task.base_run_id,
        "graph_revision": task.base_graph_revision,
    }
    target_ids = list(task.target_object_ids)
    if task.task_type == ReviewTaskType.TEXT:
        markup.create_text_task(page, target_ids, **kwargs)
    elif task.task_type == ReviewTaskType.LAYOUT:
        markup.create_layout_task(page, target_ids, **kwargs)
    elif task.task_type == ReviewTaskType.TYPOGRAPHY:
        markup.create_typography_task(page, target_ids, **kwargs)
    elif task.task_type == ReviewTaskType.NOTE_LINKAGE:
        markup.create_note_linkage_task(
            page,
            target_ids,
            related_object_ids=list(task.related_object_ids),
            **kwargs,
        )
    elif task.task_type == ReviewTaskType.SOURCE_TRIAGE:
        markup.create_source_triage_task(page, **kwargs)
    elif task.task_type == ReviewTaskType.PREPARATION:
        markup.create_preparation_task(page, **kwargs)
    elif task.task_type == ReviewTaskType.ADJUDICATION:
        markup.create_adjudication_flag_task(
            page,
            dimensions=list(task.dimensions),
            related_object_ids=list(task.related_object_ids),
            **kwargs,
        )
