# Copyright (C) 2026 Chris Malek.
"""Tests for runner resume ledger load, record, and safe-corrupt handling."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path  # noqa: TC003

from wordwending.models.resume_ledger import (
    RESUME_LEDGER_FILENAME,
    ResumeLedger,
)
from wordwending.services.resume_ledger import ResumeLedgerService


def test_missing_ledger_is_empty(tmp_path: Path) -> None:
    service = ResumeLedgerService(tmp_path)
    assert service.completed_batch_ids() == frozenset()
    assert not service.contains("batch-missing")
    assert not (tmp_path / RESUME_LEDGER_FILENAME).exists()


def test_corrupt_ledger_is_treated_as_empty(tmp_path: Path) -> None:
    path = tmp_path / RESUME_LEDGER_FILENAME
    path.write_text("{not-valid-json", encoding="utf-8")
    service = ResumeLedgerService(tmp_path)
    assert service.completed_batch_ids() == frozenset()
    assert not service.contains("batch-1")


def test_record_completed_persists_and_reloads(tmp_path: Path) -> None:
    service = ResumeLedgerService(tmp_path)
    stamp = datetime(2026, 8, 7, 12, 0, tzinfo=UTC)
    service.record_completed(
        batch_id="batch-abc",
        run_id="run-1",
        document_id="doc-1",
        source_page_ids=["page-1", "page-2"],
        completed_at_utc=stamp,
    )
    path = tmp_path / RESUME_LEDGER_FILENAME
    assert path.exists()
    loaded = ResumeLedger.model_validate_json(path.read_text(encoding="utf-8"))
    assert len(loaded.completed_batches) == 1
    entry = loaded.completed_batches[0]
    assert entry.batch_id == "batch-abc"
    assert entry.run_id == "run-1"
    assert entry.document_id == "doc-1"
    assert entry.source_page_ids == ["page-1", "page-2"]
    assert entry.completed_at_utc == stamp

    reloaded = ResumeLedgerService(tmp_path)
    assert reloaded.contains("batch-abc")
    assert reloaded.completed_batch_ids() == frozenset({"batch-abc"})


def test_record_completed_replaces_same_batch_id(tmp_path: Path) -> None:
    service = ResumeLedgerService(tmp_path)
    service.record_completed(
        batch_id="batch-abc",
        run_id="run-1",
        document_id="doc-1",
        source_page_ids=["page-1"],
    )
    service.record_completed(
        batch_id="batch-abc",
        run_id="run-2",
        document_id="doc-1",
        source_page_ids=["page-1"],
    )
    assert len(service.completed_batch_ids()) == 1
    ledger = ResumeLedger.model_validate_json(
        (tmp_path / RESUME_LEDGER_FILENAME).read_text(encoding="utf-8")
    )
    assert ledger.completed_batches[0].run_id == "run-2"
