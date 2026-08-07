# Copyright (C) 2026 Chris Malek.
"""Tests for Hugging Face endpoint lifecycle catalog and settings contracts."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from wordwending.models.endpoint_lifecycle import (
    EndpointCatalogEntry,
    default_endpoint_catalog,
    mutable_revision_rejected,
)
from wordwending.settings import Settings


def test_default_catalog_includes_olmocr_and_kraken() -> None:
    ids = {entry.runner_id for entry in default_endpoint_catalog()}
    assert ids == {"olmocr", "kraken"}


def test_catalog_entry_rejects_mutable_revision() -> None:
    with pytest.raises(ValidationError):
        EndpointCatalogEntry(
            runner_id="olmocr",
            repository="org/model",
            revision="main",
            endpoint_name="ww-olmocr",
            namespace="ns",
            accelerator="gpu",
            vendor="aws",
            region="us-east-1",
            instance_type="nvidia-a10g",
            instance_size="x1",
            framework="pytorch",
            task="image-text-to-text",
            endpoint_type="protected",
            scale_to_zero=True,
        )


def test_mutable_revision_rejected() -> None:
    assert mutable_revision_rejected("main") is True
    assert mutable_revision_rejected("MASTER") is True
    assert mutable_revision_rejected("latest") is True
    assert mutable_revision_rejected("head") is True
    assert mutable_revision_rejected("deadbeef") is False


def test_default_catalog_revisions_are_immutable() -> None:
    for entry in default_endpoint_catalog():
        assert mutable_revision_rejected(entry.revision) is False


def test_settings_idle_and_ledger_defaults(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("WORDWENDING_HUGGINGFACE_ENDPOINT_IDLE_MINUTES", raising=False)
    settings = Settings()
    assert settings.huggingface_endpoint_idle_minutes == 30
    assert settings.huggingface_endpoint_wait_timeout_seconds == 900
