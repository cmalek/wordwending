# Copyright (C) 2026 Chris Malek.
"""Tests for runner execution persistence, retries, and throughput."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import httpx
import pytest
from PIL import Image
from pydantic import ValidationError

from tests.test_olmocr_runner import hosted_runner, mock_client, olmocr_response
from tests.test_runner_batching import artifacts as batching_artifacts
from wordwending.exc import ConfigurationError, RunnerEndpointUnavailable
from wordwending.models.ocr import (
    BatchResultStatus,
    PreparedArtifactRef,
    RunnerCapability,
    RunnerReference,
)
from wordwending.models.runner_execution import (
    HostedInvocationResult,
    PackagedRunnerInput,
    PlannedRunnerBatch,
    RetryMode,
    RunnerExecutionPolicy,
    RunnerThroughputSummary,
)
from wordwending.services.olmocr_runner import OLMOCR_CAPABILITY
from wordwending.services.runner_batching import RunnerBatchPlanner
from wordwending.services.runner_execution import RunnerExecutionService
from wordwending.services.runner_packaging import RunnerInputPackager

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "runner"
PREPARED_INPUTS_PATH = FIXTURE_ROOT / "prepared-inputs.json"
POLICY_FIXTURE = FIXTURE_ROOT / "olmocr-policy-v1.json"
SCHEMA_VERSION = "1.0.0"


def policy(**overrides: object) -> RunnerExecutionPolicy:
    """Return a runner execution policy with optional overrides."""
    payload = json.loads(POLICY_FIXTURE.read_text())
    payload.update(overrides)
    return RunnerExecutionPolicy.model_validate(payload)


def runner_reference(**overrides: object) -> RunnerReference:
    """Return a default olmOCR runner reference with optional overrides."""
    payload: dict[str, object] = {
        "runner_id": "olmocr",
        "runner_version": "0.4.27",
        "model_name": "allenai/olmOCR",
        "model_revision": "model-revision",
        "hardware_class": "nvidia-l40s",
        "runtime_name": "huggingface-endpoint",
        "runtime_revision": "container-digest",
        "config_digest": "sha256:runner-config",
        "prompt_digest": "sha256:prompt",
    }
    payload.update(overrides)
    return RunnerReference.model_validate(payload)


def prepared_artifacts(count: int) -> list[PreparedArtifactRef]:
    """Build ``count`` prepared artifacts for execution tests."""
    if count <= 3:
        payload = json.loads(PREPARED_INPUTS_PATH.read_text())
        return [
            PreparedArtifactRef.model_validate(entry)
            for entry in payload["artifacts"][:count]
        ]
    return batching_artifacts(count)


def fixture_root(tmp_path: Path) -> Path:
    """Create a bundle root with PNG inputs for execution tests."""
    root = tmp_path
    if (FIXTURE_ROOT / "prepared-inputs.json").exists():
        payload = json.loads(PREPARED_INPUTS_PATH.read_text())
        refs = [
            PreparedArtifactRef.model_validate(entry) for entry in payload["artifacts"]
        ]
    else:
        refs = []
    for artifact in refs:
        destination = root / artifact.artifact_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (8, 8), color=(128, 64, 32)).save(destination)
    for artifact in batching_artifacts(8):
        destination = root / artifact.artifact_path
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (8, 8), color=(128, 64, 32)).save(destination)
    return root


def hosted_result(
    *,
    failed: list[str] | None = None,
    warnings: list[str] | None = None,
) -> HostedInvocationResult:
    """Build a hosted invocation result with optional per-item failures."""
    return HostedInvocationResult(
        failure_item_ids=list(failed or []),
        output_artifacts=[],
        request_ids=["req-1"],
        warnings=list(warnings or []),
    )


InvokeResult = HostedInvocationResult | Callable[[PlannedRunnerBatch], HostedInvocationResult]


class FakeOlmocrRunner:
    """Stub hosted runner for offline execution orchestration tests."""

    def __init__(
        self,
        *,
        execution_policy: RunnerExecutionPolicy,
        runner_ref: RunnerReference,
        capability: RunnerCapability = OLMOCR_CAPABILITY,
        health_error: BaseException | None = None,
        invoke_results: list[InvokeResult] | None = None,
    ) -> None:
        self.policy = execution_policy
        self.runner_ref = runner_ref
        self.capability = capability
        self._health_error = health_error
        self._invoke_results = list(invoke_results or [])
        self._invoke_index = 0
        self.health_check_calls = 0
        self.invoke_calls = 0

    def health_check(self) -> None:
        self.health_check_calls += 1
        if self._health_error is not None:
            raise self._health_error

    def invoke(
        self,
        batch: PlannedRunnerBatch,
        packaged: PackagedRunnerInput,
        output_dir: Path,
    ) -> HostedInvocationResult:
        _ = packaged, output_dir
        self.invoke_calls += 1
        if self._invoke_index >= len(self._invoke_results):
            return hosted_result(failed=[])
        configured = self._invoke_results[self._invoke_index]
        self._invoke_index += 1
        if callable(configured):
            return configured(batch)
        return configured


def execution_service(  # noqa: PLR0913
    *,
    warmup_batch_count: int | None = None,
    retry_mode: RetryMode | None = None,
    max_retries: int | None = None,
    health_error: BaseException | None = None,
    first_result: InvokeResult | None = None,
    retry_result: InvokeResult | None = None,
    invoke_results: list[InvokeResult] | None = None,
) -> RunnerExecutionService:
    """Construct an execution service backed by ``FakeOlmocrRunner``."""
    overrides: dict[str, object] = {}
    if warmup_batch_count is not None:
        overrides["warmup_batch_count"] = warmup_batch_count
    if retry_mode is not None:
        overrides["retry_mode"] = retry_mode.value
    if max_retries is not None:
        overrides["max_retries"] = max_retries
    execution_policy = policy(**overrides)
    results: list[InvokeResult] = list(invoke_results or [])
    if first_result is not None:
        results.append(first_result)
    if retry_result is not None:
        results.append(retry_result)
    fake = FakeOlmocrRunner(
        execution_policy=execution_policy,
        runner_ref=runner_reference(),
        health_error=health_error,
        invoke_results=results,
    )
    return RunnerExecutionService(
        RunnerBatchPlanner(),
        RunnerInputPackager(),
        fake,
    )


def _fail_second_item(batch: PlannedRunnerBatch) -> HostedInvocationResult:
    return hosted_result(failed=[batch.items[1].item_id])


def _fail_all_items(batch: PlannedRunnerBatch) -> HostedInvocationResult:
    return hosted_result(failed=[item.item_id for item in batch.items])


def test_execution_service_accepts_real_runner_public_contract() -> None:
    runner = hosted_runner(mock_client())
    service = RunnerExecutionService(
        RunnerBatchPlanner(),
        RunnerInputPackager(),
        runner,
    )
    assert service._runner.policy is runner.policy
    assert service._runner.runner_ref is runner.runner_ref
    assert service._runner.capability is runner.capability


def test_hosted_runner_across_two_batches_with_high_source_orders(
    tmp_path: Path,
) -> None:
    artifacts = [
        artifact.model_copy(update={"order": index + 5})
        for index, artifact in enumerate(prepared_artifacts(8))
    ]
    bundle = fixture_root(tmp_path / "bundle")
    post_responses = [
        httpx.Response(
            200,
            json=olmocr_response(f"item-{index}"),
            headers={"x-request-id": f"req-{index}"},
        )
        for index in range(1, 9)
    ]
    service = RunnerExecutionService(
        RunnerBatchPlanner(),
        RunnerInputPackager(),
        hosted_runner(mock_client(post_responses=post_responses)),
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        artifacts,
        bundle,
        tmp_path,
    )
    assert summary.failed_item_count == 0
    assert summary.measured_item_count == 4
    assert len(batches) == 2
    assert batches[0].warmup is True
    assert batches[1].warmup is False
    assert all("out of range" not in " ".join(batch.warnings) for batch in batches)


def test_partial_batch_persists_before_failed_item_retry(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(
        warmup_batch_count=0,
        first_result=_fail_second_item,
        retry_result=hosted_result(failed=[]),
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    assert [batch.result_status for batch in batches] == [
        BatchResultStatus.PARTIAL,
        BatchResultStatus.SUCCEEDED,
    ]
    assert batches[1].retry_of_batch_id == batches[0].batch_id
    assert batches[1].retry_strategy == "failed-items"
    assert len(list((tmp_path / "batches").glob("*.json"))) == 2
    assert summary.failed_item_count == 0


def test_warmup_batch_is_excluded_from_throughput(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    _, summary = execution_service(warmup_batch_count=1).run(
        "run-1",
        "bt",
        prepared_artifacts(8),
        bundle,
        tmp_path,
    )
    assert summary.measured_item_count == 4


def test_health_failure_persists_all_batches_without_invoke(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(
        warmup_batch_count=0,
        health_error=RunnerEndpointUnavailable("endpoint down"),
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    assert len(batches) == 1
    assert batches[0].result_status is BatchResultStatus.FAILED
    assert len(batches[0].failure_item_ids) == 2
    assert batches[0].warnings == ["endpoint down"]
    assert service._runner.health_check_calls == 1  # type: ignore[attr-defined]
    assert service._runner.invoke_calls == 0  # type: ignore[attr-defined]
    assert summary.failed_item_count == 2
    assert (tmp_path / "throughput.json").exists()


def test_all_failed_batch_status(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")

    def fail_all(batch: PlannedRunnerBatch) -> HostedInvocationResult:
        return hosted_result(failed=[item.item_id for item in batch.items])

    service = execution_service(
        warmup_batch_count=0,
        retry_mode=RetryMode.NONE,
        invoke_results=[fail_all],
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    assert len(batches) == 1
    assert batches[0].result_status is BatchResultStatus.FAILED
    assert summary.failed_item_count == 2


def test_no_retry_when_policy_disables_retries(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(
        warmup_batch_count=0,
        retry_mode=RetryMode.NONE,
        first_result=_fail_second_item,
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    assert len(batches) == 1
    assert batches[0].result_status is BatchResultStatus.PARTIAL
    assert summary.failed_item_count == 1


def test_max_retries_above_one_rejected_by_policy_model() -> None:
    with pytest.raises(ValidationError, match="max_retries"):
        policy(max_retries=3)


def test_whole_batch_retry_mode_is_rejected(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(
        warmup_batch_count=0,
        retry_mode=RetryMode.WHOLE_BATCH,
    )
    with pytest.raises(ConfigurationError, match="whole-batch retry"):
        service.run(
            "run-1",
            "bt",
            prepared_artifacts(2),
            bundle,
            tmp_path,
        )


def test_retry_failure_keeps_final_failed_item_count(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(
        warmup_batch_count=0,
        first_result=_fail_second_item,
        retry_result=_fail_all_items,
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    assert batches[0].result_status is BatchResultStatus.PARTIAL
    assert batches[1].result_status is BatchResultStatus.FAILED
    assert summary.failed_item_count == 1
    assert len(list((tmp_path / "batches").glob("*.json"))) == 2


def test_batch_timestamps_are_monotonic(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(warmup_batch_count=0)
    batches, _summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(8),
        bundle,
        tmp_path,
    )
    timestamps = [batch.started_at_utc for batch in batches]
    assert timestamps == sorted(timestamps)


def test_persisted_batch_matches_schema_version(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(warmup_batch_count=0)
    batches, _summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(1),
        bundle,
        tmp_path,
    )
    payload = json.loads((tmp_path / "batches" / f"{batches[0].batch_id}.json").read_text())
    assert payload["schema_version"] == SCHEMA_VERSION


def test_throughput_json_is_written(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(warmup_batch_count=0)
    _batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    persisted = RunnerThroughputSummary.model_validate_json(
        (tmp_path / "throughput.json").read_text()
    )
    assert persisted == summary


def test_resume_skips_completed_batches(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    artifacts = prepared_artifacts(8)
    first = execution_service(warmup_batch_count=0)
    first_batches, _ = first.run(
        "run-1",
        "bt",
        artifacts,
        bundle,
        tmp_path / "out-1",
    )
    assert len(first_batches) == 2
    assert (bundle / "runner-resume-ledger.json").exists()

    second_fake_runner = FakeOlmocrRunner(
        execution_policy=policy(warmup_batch_count=0),
        runner_ref=runner_reference(),
    )
    second = RunnerExecutionService(
        RunnerBatchPlanner(),
        RunnerInputPackager(),
        second_fake_runner,
    )
    second_batches, summary = second.run(
        "run-2",
        "bt",
        artifacts,
        bundle,
        tmp_path / "out-2",
    )
    assert second_fake_runner.invoke_calls == 0
    assert second_batches == []
    assert summary.measured_item_count == 0


def test_force_reruns_completed_batches(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    artifacts = prepared_artifacts(2)
    first = execution_service(warmup_batch_count=0)
    first.run("run-1", "bt", artifacts, bundle, tmp_path / "out-1")

    forced_runner = FakeOlmocrRunner(
        execution_policy=policy(warmup_batch_count=0),
        runner_ref=runner_reference(),
    )
    forced = RunnerExecutionService(
        RunnerBatchPlanner(),
        RunnerInputPackager(),
        forced_runner,
    )
    batches, summary = forced.run(
        "run-2",
        "bt",
        artifacts,
        bundle,
        tmp_path / "out-2",
        force=True,
    )
    assert forced_runner.invoke_calls == 1
    assert len(batches) == 1
    assert summary.measured_item_count == 2
    assert summary.failed_item_count == 0


def test_failed_batches_are_not_recorded_in_resume_ledger(tmp_path: Path) -> None:
    bundle = fixture_root(tmp_path / "bundle")
    service = execution_service(
        warmup_batch_count=0,
        retry_mode=RetryMode.NONE,
        first_result=_fail_all_items,
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        bundle,
        tmp_path,
    )
    assert summary.failed_item_count == 2
    assert batches[0].result_status is BatchResultStatus.FAILED
    ledger_path = bundle / "runner-resume-ledger.json"
    assert not ledger_path.exists()
