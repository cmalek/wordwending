# Copyright (C) 2026 Chris Malek.
"""Tests for endpoint session ledger persistence."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path  # noqa: TC003

import pytest
from pydantic import ValidationError

from wordwending.models.endpoint_lifecycle import (
    ENDPOINT_SESSION_LEDGER_SCHEMA_VERSION,
    EndpointLastAction,
    EndpointLedgerEntry,
    EndpointSessionLedger,
)
from wordwending.services.endpoint_session_ledger import EndpointSessionLedgerStore


def test_ledger_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    store = EndpointSessionLedgerStore(path)
    store.touch(
        runner_id="olmocr",
        endpoint_name="ww-olmocr",
        namespace="ns",
        url="https://example.huggingface.cloud",
        action="up",
    )
    loaded = store.load()
    assert loaded.entries["olmocr"].url.startswith("https://")


def test_missing_ledger_loads_empty(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    store = EndpointSessionLedgerStore(path)
    loaded = store.load()
    assert loaded.entries == {}
    assert loaded.schema_version == ENDPOINT_SESSION_LEDGER_SCHEMA_VERSION


def test_corrupt_ledger_loads_empty(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    path.write_text("{not-valid-json", encoding="utf-8")
    store = EndpointSessionLedgerStore(path)
    loaded = store.load()
    assert loaded.entries == {}


def test_touch_replaces_same_runner_id(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    store = EndpointSessionLedgerStore(path)
    store.touch(
        runner_id="olmocr",
        endpoint_name="ww-olmocr",
        namespace="ns",
        url="https://old.example.cloud",
        action="up",
    )
    store.touch(
        runner_id="olmocr",
        endpoint_name="ww-olmocr",
        namespace="ns",
        url="https://new.example.cloud",
        action="up",
    )
    loaded = store.load()
    assert loaded.entries["olmocr"].url == "https://new.example.cloud"


def test_mark_down_records_pause_action(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    store = EndpointSessionLedgerStore(path)
    store.touch(
        runner_id="olmocr",
        endpoint_name="ww-olmocr",
        namespace="ns",
        url="https://example.huggingface.cloud",
        action="up",
    )
    store.mark_down(
        runner_id="olmocr",
        endpoint_name="ww-olmocr",
        namespace="ns",
        action="pause",
    )
    loaded = store.load()
    assert loaded.entries["olmocr"].last_action == EndpointLastAction.PAUSE


def test_save_persists_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    store = EndpointSessionLedgerStore(path)
    stamp = datetime(2026, 8, 7, 12, 0, tzinfo=UTC)
    ledger = EndpointSessionLedger(
        entries={
            "olmocr": EndpointLedgerEntry(
                runner_id="olmocr",
                endpoint_name="ww-olmocr",
                namespace="ns",
                endpoint_url="https://example.huggingface.cloud",
                last_used_at_utc=stamp,
                last_action=EndpointLastAction.UP,
            )
        }
    )
    store.save(ledger)
    reloaded = EndpointSessionLedgerStore(path).load()
    assert reloaded.entries["olmocr"].url == "https://example.huggingface.cloud"


def test_touch_rejects_invalid_action(tmp_path: Path) -> None:
    store = EndpointSessionLedgerStore(tmp_path / "ledger.json")
    with pytest.raises((ValueError, ValidationError)):
        store.touch(
            runner_id="olmocr",
            endpoint_name="ww-olmocr",
            namespace="ns",
            url="https://example.huggingface.cloud",
            action="invalid",
        )
