# Copyright (C) 2026 Chris Malek.
"""Tests for PassRunnerRegistry resolution by runner_id."""

from __future__ import annotations

import pytest

from tests.test_kraken_runner import hosted_runner as kraken_hosted_runner
from tests.test_kraken_runner import mock_client as kraken_mock_client
from tests.test_olmocr_runner import hosted_runner as olmocr_hosted_runner
from tests.test_olmocr_runner import mock_client as olmocr_mock_client
from wordwending.services.kraken_runner import HuggingFaceKrakenRunner
from wordwending.services.olmocr_runner import HuggingFaceOlmocrRunner
from wordwending.services.pass_runner import PassRunner
from wordwending.services.pass_runner_registry import (
    PassRunnerRegistry,
    UnknownPassRunnerError,
)


def test_default_registry_resolves_olmocr_adapter() -> None:
    registry = PassRunnerRegistry()
    runner_cls = registry.resolve("olmocr")

    assert runner_cls is HuggingFaceOlmocrRunner
    runner = olmocr_hosted_runner(olmocr_mock_client())
    assert isinstance(runner, PassRunner)
    assert runner.runner_ref.runner_id == "olmocr"


def test_default_registry_resolves_kraken_adapter() -> None:
    registry = PassRunnerRegistry()
    runner_cls = registry.resolve("kraken")

    assert runner_cls is HuggingFaceKrakenRunner
    runner = kraken_hosted_runner(kraken_mock_client())
    assert isinstance(runner, PassRunner)
    assert runner.runner_ref.runner_id == "kraken"


def test_resolve_unknown_runner_id_fails_clearly() -> None:
    registry = PassRunnerRegistry()

    with pytest.raises(UnknownPassRunnerError, match=r"unsupported runner_id"):
        registry.resolve("unknown-engine")


def test_register_overrides_or_adds_runner_id() -> None:
    registry = PassRunnerRegistry(runners={})
    registry.register("olmocr", HuggingFaceOlmocrRunner)

    assert registry.resolve("olmocr") is HuggingFaceOlmocrRunner
    assert "olmocr" in registry.known_ids
