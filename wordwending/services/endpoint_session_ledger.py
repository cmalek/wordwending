# Copyright (C) 2026 Chris Malek.
"""Persist endpoint session rows without secrets."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path  # noqa: TC003

from pydantic import ValidationError

from wordwending.models.endpoint_lifecycle import (
    EndpointLastAction,
    EndpointLedgerEntry,
    EndpointSessionLedger,
)


def _atomic_write_text(path: Path, payload: str) -> None:
    """
    Atomically write ``payload`` to ``path`` via a sibling temporary file.

    Side Effects:
        Creates parent directories and replaces ``path`` on success.

    Args:
        path: Destination file path.
        payload: UTF-8 text to persist.

    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def _coerce_action(action: str | EndpointLastAction) -> EndpointLastAction:
    """
    Normalize a lifecycle action value for ledger rows.

    Args:
        action: Raw action string or enum value.

    Returns:
        Validated ``EndpointLastAction``.

    Raises:
        ValueError: When the action is not a supported lifecycle label.

    """
    if isinstance(action, EndpointLastAction):
        return action
    normalized = action.strip().lower()
    for candidate in EndpointLastAction:
        if candidate.value == normalized:
            return candidate
    msg = f"unsupported endpoint session action: {action!r}"
    raise ValueError(msg)


class EndpointSessionLedgerStore:
    """
    Load and persist the endpoint session ledger at a fixed path.

    Missing or corrupt ledger files are treated as empty so lifecycle
    operations can always proceed safely.

    Args:
        path: Absolute path to the on-disk ledger JSON document.

    """

    def __init__(self, path: Path) -> None:
        """
        Bind the ledger path for subsequent load and update operations.

        Args:
            path: Absolute path to the on-disk ledger JSON document.

        """
        #: Absolute path to the on-disk ledger JSON document.
        self._path = path

    @property
    def path(self) -> Path:
        """
        Return the configured on-disk ledger path.

        Returns:
            Absolute path to the ledger JSON document.

        """
        return self._path

    def load(self) -> EndpointSessionLedger:
        """
        Load the on-disk ledger, returning empty on missing or corrupt data.

        Returns:
            Validated ledger document, or an empty ledger when unsafe to trust.

        """
        if not self._path.exists():
            return EndpointSessionLedger()
        try:
            return EndpointSessionLedger.model_validate_json(
                self._path.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeDecodeError, ValidationError, ValueError):
            return EndpointSessionLedger()

    def save(self, ledger: EndpointSessionLedger) -> None:
        """
        Atomically persist the supplied ledger document.

        Side Effects:
            Replaces the configured ledger JSON file.

        Args:
            ledger: Ledger document to write to disk.

        """
        _atomic_write_text(self._path, ledger.model_dump_json(indent=2))

    def touch(
        self,
        *,
        runner_id: str,
        endpoint_name: str,
        namespace: str,
        url: str,
        action: str | EndpointLastAction,
    ) -> None:
        """
        Record one active endpoint session row and persist the ledger.

        Side Effects:
            Writes the configured ledger JSON file.

        Keyword Args:
            runner_id: Stable runner identifier for the session row.
            endpoint_name: Inference Endpoint name in the hosting provider.
            namespace: Hugging Face namespace for the endpoint.
            url: Last known HTTPS endpoint URL.
            action: Lifecycle action label, typically ``up``.

        """
        ledger = self.load()
        entry = EndpointLedgerEntry(
            runner_id=runner_id,
            endpoint_name=endpoint_name,
            namespace=namespace,
            endpoint_url=url,
            last_used_at_utc=datetime.now(tz=UTC),
            last_action=_coerce_action(action),
        )
        ledger.entries[runner_id] = entry
        self.save(ledger)

    def mark_down(
        self,
        *,
        runner_id: str,
        endpoint_name: str,
        namespace: str,
        action: str | EndpointLastAction,
    ) -> None:
        """
        Record one paused or scaled-down endpoint session row.

        Side Effects:
            Writes the configured ledger JSON file.

        Keyword Args:
            runner_id: Stable runner identifier for the session row.
            endpoint_name: Inference Endpoint name in the hosting provider.
            namespace: Hugging Face namespace for the endpoint.
            action: Lifecycle action label, typically ``down`` or ``pause``.

        """
        ledger = self.load()
        existing = ledger.entries.get(runner_id)
        endpoint_url = existing.endpoint_url if existing is not None else ""
        timestamp = (
            existing.last_used_at_utc
            if existing is not None
            else datetime.now(tz=UTC)
        )
        entry = EndpointLedgerEntry(
            runner_id=runner_id,
            endpoint_name=endpoint_name,
            namespace=namespace,
            endpoint_url=endpoint_url,
            last_used_at_utc=timestamp,
            last_action=_coerce_action(action),
        )
        ledger.entries[runner_id] = entry
        self.save(ledger)
