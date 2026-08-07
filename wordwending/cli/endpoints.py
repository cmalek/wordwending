# Copyright (C) 2026 Chris Malek.
"""Hugging Face Inference Endpoint lifecycle CLI commands."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from wordwending.exc import ConfigurationError, EndpointLifecycleError
from wordwending.services.endpoint_lifecycle import EndpointLifecycleService
from wordwending.services.endpoint_session_ledger import EndpointSessionLedgerStore
from wordwending.services.hf_endpoint_client import HfEndpointClient

if TYPE_CHECKING:
    from wordwending.settings import Settings


def build_endpoint_lifecycle_service(settings: Settings) -> EndpointLifecycleService:
    """
    Construct an ``EndpointLifecycleService`` from effective settings.

    Args:
        settings: Loaded application settings with HF token and catalog.

    Returns:
        Service bound to the resolved ledger path and endpoint catalog.

    Raises:
        ConfigurationError: When ``huggingface_api_key`` is missing.

    """
    api_key = settings.huggingface_api_key
    token = api_key.get_secret_value() if api_key is not None else None
    if not token:
        msg = "missing settings value huggingface_api_key"
        raise ConfigurationError(msg)
    client = HfEndpointClient(token)
    ledger = EndpointSessionLedgerStore(settings.resolved_endpoint_ledger_path())
    return EndpointLifecycleService(
        client=client,
        ledger=ledger,
        settings=settings,
    )


def _service_from_context(ctx: click.Context) -> EndpointLifecycleService:
    """
    Build the endpoint lifecycle service from Click context settings.

    Args:
        ctx: Click context carrying loaded settings.

    Returns:
        Endpoint lifecycle service for the current invocation.

    Raises:
        click.ClickException: When settings cannot produce a service.

    """
    settings: Settings = ctx.obj["settings"]
    try:
        return build_endpoint_lifecycle_service(settings)
    except ConfigurationError as exc:
        raise click.ClickException(str(exc)) from exc


def _handle_lifecycle_errors(func):
    """
    Wrap an endpoints subcommand to map lifecycle errors to Click failures.

    Args:
        func: Click command callable to wrap.

    Returns:
        Wrapped command that raises ``click.ClickException`` on lifecycle errors.

    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConfigurationError, EndpointLifecycleError) as exc:
            raise click.ClickException(str(exc)) from exc

    return wrapper


@click.group()
def endpoints() -> None:
    """Ensure, pause, or inspect Hugging Face Inference Endpoints."""


@endpoints.command("up")
@click.option(
    "--runner",
    "runner_ids",
    multiple=True,
    help="Catalogued runner id (repeatable). Defaults to all catalogued runners.",
)
@click.pass_context
@_handle_lifecycle_errors
def endpoints_up(ctx: click.Context, runner_ids: tuple[str, ...]) -> None:
    """
    Ensure catalogued endpoints are ready and print HTTPS URLs.

    Calls ``pause_idle`` first as a safety net for stale sessions, then
    creates or resumes endpoints until ready.

    Args:
        ctx: Click context object.
        runner_ids: Optional catalogued runner identifiers to ensure.

    Side Effects:
        May pause idle endpoints, create/resume remote endpoints, and rewrite
        the session ledger.

    Raises:
        click.ClickException: When configuration or lifecycle operations fail.

    """
    service = _service_from_context(ctx)
    service.pause_idle()
    result = service.ensure_up(list(runner_ids))
    for runner_id in sorted(result.urls_by_runner_id):
        click.echo(f"{runner_id}: {result.urls_by_runner_id[runner_id]}")
    for runner_id in result.created_runner_ids:
        click.echo(f"created: {runner_id}")
    for runner_id in result.resumed_runner_ids:
        click.echo(f"resumed: {runner_id}")
    for runner_id in result.already_ready_runner_ids:
        click.echo(f"already_ready: {runner_id}")


@endpoints.command("down")
@click.option(
    "--runner",
    "runner_ids",
    multiple=True,
    help="Catalogued runner id (repeatable). Defaults to all catalogued runners.",
)
@click.option(
    "--delete",
    is_flag=True,
    help="Destroy endpoints instead of pausing them.",
)
@click.pass_context
@_handle_lifecycle_errors
def endpoints_down(
    ctx: click.Context,
    runner_ids: tuple[str, ...],
    delete: bool,
) -> None:
    """
    Pause or delete catalogued endpoints.

    Args:
        ctx: Click context object.
        runner_ids: Optional catalogued runner identifiers to take down.
        delete: When set, destroy endpoints instead of pausing.

    Side Effects:
        Pauses or deletes remote endpoints and rewrites the session ledger.

    Raises:
        click.ClickException: When configuration or lifecycle operations fail.

    """
    service = _service_from_context(ctx)
    result = service.down(list(runner_ids), delete=delete)
    for runner_id in result.paused_runner_ids:
        click.echo(f"paused: {runner_id}")
    for runner_id in result.deleted_runner_ids:
        click.echo(f"deleted: {runner_id}")


@endpoints.command("status")
@click.option(
    "--runner",
    "runner_ids",
    multiple=True,
    help="Catalogued runner id (repeatable). Defaults to all catalogued runners.",
)
@click.pass_context
@_handle_lifecycle_errors
def endpoints_status(ctx: click.Context, runner_ids: tuple[str, ...]) -> None:
    """
    Report Hugging Face endpoint status plus session ledger last-used times.

    Calls ``pause_idle`` first as a safety net for stale sessions.

    Args:
        ctx: Click context object.
        runner_ids: Optional catalogued runner identifiers to report.

    Side Effects:
        May pause idle endpoints before reporting status.

    Raises:
        click.ClickException: When configuration or lifecycle operations fail.

    """
    service = _service_from_context(ctx)
    service.pause_idle()
    selected = list(runner_ids) if runner_ids else None
    report = service.status(selected)
    for row in report.rows:
        click.echo(f"runner_id: {row.runner_id}")
        click.echo(f"endpoint_name: {row.endpoint_name}")
        click.echo(f"hf_status: {row.hf_status}")
        if row.endpoint_url is not None:
            click.echo(f"endpoint_url: {row.endpoint_url}")
        if row.last_used_at_utc is not None:
            click.echo(f"last_used_at_utc: {row.last_used_at_utc.isoformat()}")
