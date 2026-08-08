# Copyright (C) 2026 Chris Malek.
"""Review overlay CLI commands."""

from __future__ import annotations

from pathlib import Path

import click
from pydantic import ValidationError

from wordwending.models import PageOverlay
from wordwending.services.bundle_layout import BundleLayoutService
from wordwending.services.review_cli import ReviewCliService
from wordwending.services.review_overlay import ReviewOverlayService


@click.group()
def review() -> None:
    """Apply, materialize, issue, and rebase human review overlays on bundles."""


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
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    try:
        page_overlay = PageOverlay.model_validate_json(
            overlay.read_text(encoding="utf-8")
        )
        result = service.apply(bundle_root, page_overlay, page_id)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"page_id: {result.page_id}")
    click.echo(f"events_appended: {result.events_appended}")
    click.echo(f"states: {len(result.states)}")


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
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    try:
        result = service.materialize(bundle_root, page_id)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"page_id: {result.page_id}")
    click.echo(f"states: {len(result.states)}")


@review.command("issue")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Filesystem root for one assembled document bundle tree.",
)
@click.option("--page-id", required=True, help="Stable page identifier to update.")
@click.option(
    "--run-id",
    default=None,
    help=(
        "Execution run identifier stamped onto regenerated tasks; defaults to "
        "document-bundle.json run id when present, else run-review-issue."
    ),
)
def review_issue(bundle_root: Path, page_id: str, run_id: str | None) -> None:
    """
    Regenerate pending review tasks from one page's evaluation flags.

    Args:
        bundle_root: Filesystem root for one document bundle tree.
        page_id: Stable page identifier whose evaluation flags drive the queue.
        run_id: Optional run id stamped onto each regenerated task.

    Side Effects:
        Overwrites ``overlays/pending_tasks.json`` for the page.

    Raises:
        click.ClickException: When the page is missing or I/O fails.

    """
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    try:
        result = service.issue(bundle_root, page_id, run_id=run_id)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"page_id: {result.page_id}")
    click.echo(f"tasks: {result.task_count}")


@review.command("rebase")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Filesystem root for one assembled document bundle tree.",
)
@click.option("--page-id", required=True, help="Stable page identifier to rebase.")
@click.option(
    "--graph-revision",
    default=None,
    help=(
        "Explicit successor graph revision; defaults to bumping a trailing "
        "integer on the current page graph_revision."
    ),
)
def review_rebase(
    bundle_root: Path,
    page_id: str,
    graph_revision: str | None,
) -> None:
    """
    Apply overlay corrections onto the page graph and write a successor overlay.

    Args:
        bundle_root: Filesystem root for one document bundle tree.
        page_id: Stable page identifier whose graph is rebased.
        graph_revision: Optional explicit successor graph revision.

    Side Effects:
        Overwrites page graph, document-bundle page entry when present,
        ``overlays/page_overlay.json``, ``overlays/current_state.json``, and
        ``overlays/pending_tasks.json``. Does not rewrite
        ``overlays/review_events.jsonl``.

    Raises:
        click.ClickException: When the page is missing or rebase fails.

    """
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    try:
        result = service.rebase(
            bundle_root,
            page_id,
            graph_revision=graph_revision,
        )
    except (OSError, ValidationError, ValueError, FileNotFoundError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"page_id: {result.page_id}")
    click.echo(
        "graph_revision: "
        f"{result.old_graph_revision} -> {result.new_graph_revision}"
    )
