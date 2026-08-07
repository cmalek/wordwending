# Copyright (C) 2026 Chris Malek.
"""Load and persist the runner resume ledger under a bundle root."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path  # noqa: TC003

from pydantic import ValidationError

from wordwending.models.resume_ledger import (
    RESUME_LEDGER_FILENAME,
    ResumeLedger,
    ResumeLedgerEntry,
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


class ResumeLedgerService:
    """
    Read and update the resume ledger stored under ``bundle_root``.

    Missing or corrupt ledger files are treated as empty so interrupted runs
    can always start safely.

    Args:
        bundle_root: Bundle root that owns ``runner-resume-ledger.json``.

    """

    def __init__(self, bundle_root: Path) -> None:
        """
        Bind the ledger path and load any existing on-disk document.

        Args:
            bundle_root: Bundle root that owns ``runner-resume-ledger.json``.

        """
        #: Absolute path to the on-disk ledger JSON document.
        self._path = bundle_root / RESUME_LEDGER_FILENAME
        #: In-memory ledger document loaded or created for this service.
        self._ledger = self._load_safe()

    @property
    def path(self) -> Path:
        """
        Return the on-disk ledger path under the bundle root.

        Returns:
            Absolute path to ``runner-resume-ledger.json``.

        """
        return self._path

    def completed_batch_ids(self) -> frozenset[str]:
        """
        Return the set of successfully completed batch ids.

        Returns:
            Frozen set of recorded ``batch_id`` values.

        """
        return frozenset(entry.batch_id for entry in self._ledger.completed_batches)

    def contains(self, batch_id: str) -> bool:
        """
        Return whether ``batch_id`` is already recorded as complete.

        Args:
            batch_id: Stable planned batch identifier.

        Returns:
            ``True`` when the ledger already records the batch.

        """
        return batch_id in self.completed_batch_ids()

    def record_completed(
        self,
        *,
        batch_id: str,
        run_id: str,
        document_id: str,
        source_page_ids: list[str],
        completed_at_utc: datetime | None = None,
    ) -> None:
        """
        Record one successfully completed batch and persist the ledger.

        Side Effects:
            Writes ``bundle_root/runner-resume-ledger.json``.

        Keyword Args:
            batch_id: Stable planned batch identifier.
            run_id: Execution run identifier that completed the batch.
            document_id: Document identifier under processing.
            source_page_ids: Source page ids included in the batch.
            completed_at_utc: Completion timestamp; defaults to UTC now.

        """
        timestamp = completed_at_utc or datetime.now(tz=UTC)
        entry = ResumeLedgerEntry(
            batch_id=batch_id,
            run_id=run_id,
            document_id=document_id,
            source_page_ids=list(source_page_ids),
            completed_at_utc=timestamp,
        )
        remaining = [
            existing
            for existing in self._ledger.completed_batches
            if existing.batch_id != batch_id
        ]
        remaining.append(entry)
        self._ledger = ResumeLedger(completed_batches=remaining)
        self._persist()

    def _load_safe(self) -> ResumeLedger:
        """
        Load the on-disk ledger, returning empty on missing or corrupt data.

        Returns:
            Validated ledger document, or an empty ledger when unsafe to trust.

        """
        if not self._path.exists():
            return ResumeLedger()
        try:
            return ResumeLedger.model_validate_json(
                self._path.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeDecodeError, ValidationError, ValueError):
            return ResumeLedger()

    def _persist(self) -> None:
        """
        Atomically write the in-memory ledger to disk.

        Side Effects:
            Replaces ``bundle_root/runner-resume-ledger.json``.

        """
        _atomic_write_text(self._path, self._ledger.model_dump_json(indent=2))
