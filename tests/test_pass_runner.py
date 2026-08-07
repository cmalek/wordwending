# Copyright (C) 2026 Chris Malek.
"""Tests that real hosted adapters satisfy the PassRunner Protocol."""

from __future__ import annotations

from tests.test_kraken_runner import hosted_runner as kraken_hosted_runner
from tests.test_kraken_runner import mock_client as kraken_mock_client
from tests.test_olmocr_runner import hosted_runner as olmocr_hosted_runner
from tests.test_olmocr_runner import mock_client as olmocr_mock_client
from wordwending.services.pass_runner import PassRunner


def test_olmocr_runner_satisfies_pass_runner_protocol() -> None:
    runner = olmocr_hosted_runner(olmocr_mock_client())
    assert isinstance(runner, PassRunner)
    assert runner.runner_ref.runner_id == "olmocr"
    assert runner.capability.supports_multi_item_batching is True
    assert runner.policy.policy_id == "olmocr-hf-fixed-v1"


def test_kraken_runner_satisfies_pass_runner_protocol() -> None:
    runner = kraken_hosted_runner(kraken_mock_client())
    assert isinstance(runner, PassRunner)
    assert runner.runner_ref.runner_id == "kraken"
    assert runner.capability.supports_multi_item_batching is True
    assert runner.policy.policy_id == "olmocr-hf-fixed-v1"
