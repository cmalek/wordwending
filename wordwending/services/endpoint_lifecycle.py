# Copyright (C) 2026 Chris Malek.
"""Orchestrate Hugging Face endpoint ensure / down / status / idle pause."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: TC003
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from wordwending.exc import ConfigurationError, EndpointLifecycleError
from wordwending.models.endpoint_lifecycle import (
    EndpointCatalogEntry,
    EndpointDownResult,
    EndpointEnsureResult,
    EndpointLastAction,
    EndpointLedgerEntry,
    EndpointStatusReport,
    EndpointStatusRow,
)

if TYPE_CHECKING:
    from wordwending.services.endpoint_session_ledger import EndpointSessionLedgerStore
    from wordwending.services.hf_endpoint_client import EndpointClient
    from wordwending.settings import Settings

#: Remote HF statuses that require resume before wait-ready.
_RESUME_STATUSES = frozenset({"paused", "scaledToZero"})
#: Remote HF status treated as already ready before wait-ready.
_RUNNING_STATUS = "running"


class EndpointLifecycleService:
    """
    Orchestrate catalogued Inference Endpoint lifecycle operations.

    Coordinates an injected ``EndpointClient``, session ledger store, and
    Settings timeouts/idle policy. Unknown runner ids and partial ensure
    failures fail closed.

    Args:
        client: Hugging Face endpoint client (or Protocol-compatible fake).
        ledger: On-disk session ledger store without secrets.
        settings: Settings providing wait timeout and idle minutes.
        catalog: Optional catalog override; defaults to
            ``settings.effective_endpoint_catalog()``.

    """

    def __init__(
        self,
        *,
        client: EndpointClient,
        ledger: EndpointSessionLedgerStore,
        settings: Settings,
        catalog: Sequence[EndpointCatalogEntry] | None = None,
    ) -> None:
        """
        Bind collaborators for subsequent lifecycle operations.

        Keyword Args:
            client: Hugging Face endpoint client (or Protocol-compatible fake).
            ledger: On-disk session ledger store without secrets.
            settings: Settings providing wait timeout and idle minutes.
            catalog: Optional catalog override; defaults to effective catalog.

        """
        #: Injected endpoint client used for Hub lifecycle calls.
        self._client = client
        #: Injected session ledger store for last-used / action rows.
        self._ledger = ledger
        #: Injected settings for wait timeout and idle minutes.
        self._settings = settings
        resolved = (
            list(catalog)
            if catalog is not None
            else list(settings.effective_endpoint_catalog())
        )
        #: Catalog entries keyed by runner_id for this service instance.
        self._catalog_by_id = {entry.runner_id: entry for entry in resolved}

    def ensure_up(self, runner_ids: Sequence[str]) -> EndpointEnsureResult:
        """
        Create or resume catalogued endpoints until ready for inference.

        Side Effects:
            May create/resume remote endpoints and rewrite the session ledger.

        Args:
            runner_ids: Runner identifiers to ensure; empty means all catalogued.

        Returns:
            Ready HTTPS URLs and per-action runner id lists.

        Raises:
            EndpointLifecycleError: When a runner id is unknown or any ensure
                step fails (fail-closed; no silent partial success).

        """
        selected = self._resolve_runner_ids(runner_ids)
        urls: dict[str, str] = {}
        already_ready: list[str] = []
        resumed: list[str] = []
        created: list[str] = []
        failures: list[str] = []
        for runner_id in selected:
            try:
                url, action = self._ensure_one(runner_id)
            except ConfigurationError:
                raise
            except EndpointLifecycleError as exc:
                failures.append(f"{runner_id}: {exc}")
                continue
            urls[runner_id] = url
            if action == "created":
                created.append(runner_id)
            elif action == "resumed":
                resumed.append(runner_id)
            else:
                already_ready.append(runner_id)
        if failures:
            joined = "; ".join(failures)
            msg = f"endpoint ensure failed for: {joined}"
            raise EndpointLifecycleError(msg)
        return EndpointEnsureResult(
            urls_by_runner_id=urls,
            already_ready_runner_ids=already_ready,
            resumed_runner_ids=resumed,
            created_runner_ids=created,
        )

    def down(
        self,
        runner_ids: Sequence[str],
        *,
        delete: bool = False,
    ) -> EndpointDownResult:
        """
        Pause or delete catalogued endpoints and mark the session ledger.

        Side Effects:
            Pauses or deletes remote endpoints and rewrites ledger rows.

        Args:
            runner_ids: Runner identifiers to take down; empty means all catalogued.

        Keyword Args:
            delete: When ``True``, destroy endpoints instead of pausing.

        Returns:
            Runner ids that were paused or deleted.

        Raises:
            EndpointLifecycleError: When a runner id is unknown or a down
                operation fails.

        """
        selected = self._resolve_runner_ids(runner_ids)
        paused: list[str] = []
        deleted: list[str] = []
        failures: list[str] = []
        for runner_id in selected:
            entry = self._catalog_by_id[runner_id]
            namespace = self._namespace_for(entry)
            try:
                if delete:
                    self._client.delete(entry.endpoint_name, namespace=namespace)
                    action = EndpointLastAction.DOWN
                    deleted.append(runner_id)
                else:
                    self._client.pause(entry.endpoint_name, namespace=namespace)
                    action = EndpointLastAction.PAUSE
                    paused.append(runner_id)
                self._ledger.mark_down(
                    runner_id=runner_id,
                    endpoint_name=entry.endpoint_name,
                    namespace=entry.namespace,
                    action=action,
                )
            except ConfigurationError:
                raise
            except EndpointLifecycleError as exc:
                failures.append(f"{runner_id}: {exc}")
        if failures:
            joined = "; ".join(failures)
            msg = f"endpoint down failed for: {joined}"
            raise EndpointLifecycleError(msg)
        return EndpointDownResult(
            paused_runner_ids=paused,
            deleted_runner_ids=deleted,
        )

    def status(
        self,
        runner_ids: Sequence[str] | None = None,
    ) -> EndpointStatusReport:
        """
        Report Hugging Face status plus ledger last-used for runners.

        Args:
            runner_ids: Runner identifiers to report; ``None`` or empty means
                all catalogued runners.

        Returns:
            Aggregated per-runner status rows in request/catalog order.

        Raises:
            EndpointLifecycleError: When a runner id is unknown.

        """
        selected = self._resolve_runner_ids([] if runner_ids is None else runner_ids)
        ledger = self._ledger.load()
        rows = [
            self._status_row(runner_id, ledger.entries.get(runner_id))
            for runner_id in selected
        ]
        return EndpointStatusReport(rows=rows)

    def pause_idle(self, *, now: datetime | None = None) -> EndpointDownResult:
        """
        Pause catalogued runners idle longer than the configured threshold.

        Never deletes remote endpoints. Only runners present in both the
        catalog and the session ledger are considered.

        Side Effects:
            May pause remote endpoints and rewrite ledger rows.

        Keyword Args:
            now: Reference UTC time for idle comparison; defaults to now.

        Returns:
            Runner ids paused by the idle watchdog.

        """
        reference = now if now is not None else datetime.now(tz=UTC)
        if reference.tzinfo is None:
            reference = reference.replace(tzinfo=UTC)
        threshold = timedelta(minutes=self._settings.huggingface_endpoint_idle_minutes)
        ledger = self._ledger.load()
        stale: list[str] = []
        for runner_id, row in ledger.entries.items():
            if runner_id not in self._catalog_by_id:
                continue
            last_used = row.last_used_at_utc
            if last_used.tzinfo is None:
                last_used = last_used.replace(tzinfo=UTC)
            if reference - last_used >= threshold:
                stale.append(runner_id)
        if not stale:
            return EndpointDownResult()
        return self.down(stale, delete=False)

    def _ensure_one(self, runner_id: str) -> tuple[str, str]:
        """
        Ensure one catalogued runner is ready and return URL plus action label.

        Side Effects:
            May create/resume a remote endpoint and touch the session ledger.

        Args:
            runner_id: Catalogued runner identifier.

        Returns:
            Pair of ready HTTPS URL and action label
            (``created``, ``resumed``, or ``already_ready``).

        Raises:
            ConfigurationError: When the client reports missing configuration.
            EndpointLifecycleError: When the endpoint cannot be made ready.

        """
        entry = self._catalog_by_id[runner_id]
        namespace = self._namespace_for(entry)
        action = "already_ready"
        try:
            remote = self._client.describe(entry.endpoint_name, namespace=namespace)
        except ConfigurationError:
            raise
        except EndpointLifecycleError:
            self._client.create(entry)
            action = "created"
        else:
            if remote.status in _RESUME_STATUSES:
                self._client.resume(entry.endpoint_name, namespace=namespace)
                action = "resumed"
        ready = self._client.wait_ready(
            entry.endpoint_name,
            namespace=namespace,
            timeout_seconds=self._settings.huggingface_endpoint_wait_timeout_seconds,
        )
        if not ready.url or not str(ready.url).startswith("https://"):
            msg = f"endpoint {entry.endpoint_name!r} ready without HTTPS URL"
            raise EndpointLifecycleError(msg)
        self._ledger.touch(
            runner_id=runner_id,
            endpoint_name=entry.endpoint_name,
            namespace=entry.namespace,
            url=str(ready.url),
            action=EndpointLastAction.UP,
        )
        return str(ready.url), action

    def _status_row(
        self,
        runner_id: str,
        ledger_entry: EndpointLedgerEntry | None,
    ) -> EndpointStatusRow:
        """
        Build one status row from HF describe plus optional ledger data.

        Args:
            runner_id: Catalogued runner identifier.
            ledger_entry: Matching ledger entry when present.

        Returns:
            Combined HF and ledger status row.

        """
        entry = self._catalog_by_id[runner_id]
        namespace = self._namespace_for(entry)
        try:
            remote = self._client.describe(entry.endpoint_name, namespace=namespace)
            hf_status = remote.status
            endpoint_url = remote.url
        except ConfigurationError:
            raise
        except EndpointLifecycleError:
            hf_status = "missing"
            endpoint_url = None
        return EndpointStatusRow(
            runner_id=runner_id,
            endpoint_name=entry.endpoint_name,
            hf_status=hf_status,
            endpoint_url=endpoint_url
            or (ledger_entry.endpoint_url if ledger_entry is not None else None),
            last_used_at_utc=(
                ledger_entry.last_used_at_utc if ledger_entry is not None else None
            ),
        )

    def _resolve_runner_ids(self, runner_ids: Sequence[str]) -> list[str]:
        """
        Resolve requested runner ids against the catalog, fail-closed.

        Args:
            runner_ids: Requested runner identifiers; empty means all catalogued.

        Returns:
            Ordered list of known runner identifiers.

        Raises:
            EndpointLifecycleError: When any requested id is not catalogued.

        """
        if not runner_ids:
            return list(self._catalog_by_id)
        unknown = [
            runner_id
            for runner_id in runner_ids
            if runner_id not in self._catalog_by_id
        ]
        if unknown:
            known = ", ".join(sorted(self._catalog_by_id))
            joined = ", ".join(unknown)
            msg = f"unknown endpoint runner id(s): {joined}; catalogued ids: {known}"
            raise EndpointLifecycleError(msg)
        return list(runner_ids)

    def _namespace_for(self, entry: EndpointCatalogEntry) -> str | None:
        """
        Resolve the Hugging Face namespace for one catalog entry.

        Args:
            entry: Catalog pin for the runner.

        Returns:
            Settings namespace override when set, otherwise the catalog namespace.

        """
        override = self._settings.huggingface_endpoint_namespace
        if override:
            return override
        return entry.namespace
