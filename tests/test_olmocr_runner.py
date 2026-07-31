# Copyright (C) 2026 Chris Malek.
"""Tests for hosted olmOCR batch execution."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import patch

import httpx
import pytest
from PIL import Image

from bochord.exc import ConfigurationError, RunnerEndpointUnavailable
from bochord.models.ocr import (
    InputKind,
    RunnerReference,
)
from bochord.models.runner_execution import (
    PackagedRunnerInput,
    PlannedRunnerBatch,
    RunnerExecutionPolicy,
)
from bochord.services.olmocr_runner import HuggingFaceOlmocrRunner
from tests.test_ocr_models import model_runner_payload, runner_policy_payload
from tests.test_runner_packaging import planned_batch as packaging_planned_batch

ENDPOINT_URL = "https://example.endpoints.huggingface.cloud/v1"
TOKEN = "hf_test_token"  # noqa: S105


def olmocr_response(text: str) -> dict[str, Any]:
    """Return an OpenAI-compatible chat completion payload."""
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
    }


class MockHttpxClient:
    """Minimal httpx client stand-in for hosted runner tests."""

    def __init__(
        self,
        *,
        get_status: int = 200,
        get_json: dict[str, Any] | None = None,
        post_responses: list[httpx.Response | BaseException] | None = None,
    ) -> None:
        self.get_status = get_status
        self.get_json = get_json if get_json is not None else {"data": [{"id": "model"}]}
        self.post_responses = list(post_responses or [])
        self.get_calls: list[tuple[str, dict[str, Any]]] = []
        self.post_calls: list[tuple[str, dict[str, Any]]] = []

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        self.get_calls.append((url, kwargs))
        return httpx.Response(self.get_status, json=self.get_json)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        self.post_calls.append((url, kwargs))
        if not self.post_responses:
            msg = "no post response configured"
            raise RuntimeError(msg)
        response = self.post_responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def mock_client(**kwargs: Any) -> MockHttpxClient:
    """Build a mock httpx client with optional response overrides."""
    return MockHttpxClient(**kwargs)


def policy(**overrides: object) -> RunnerExecutionPolicy:
    """Return a default runner execution policy with optional overrides."""
    return RunnerExecutionPolicy.model_validate(runner_policy_payload(**overrides))


def runner_reference(**overrides: object) -> RunnerReference:
    """Return a default olmOCR runner reference with optional overrides."""
    return RunnerReference.model_validate(model_runner_payload(**overrides))


def hosted_runner(
    client: MockHttpxClient,
    *,
    token: str = TOKEN,
    endpoint_url: str = ENDPOINT_URL,
) -> HuggingFaceOlmocrRunner:
    """Construct a hosted olmOCR runner backed by ``client``."""
    return HuggingFaceOlmocrRunner(
        runner=runner_reference(),
        policy=policy(),
        endpoint_url=endpoint_url,
        token=token,
        client=client,  # type: ignore[arg-type]
    )


def planned_batch(item_count: int, *, batch_id: str = "batch-test") -> PlannedRunnerBatch:
    """Build a planned batch for hosted runner tests."""
    return packaging_planned_batch(item_count, batch_id=batch_id)


def _write_direct_image(output_dir: Path, batch: PlannedRunnerBatch) -> PackagedRunnerInput:
    artifact = batch.artifacts[0]
    destination = output_dir / artifact.artifact_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (64, 32), color=(200, 100, 50)).save(destination)
    return PackagedRunnerInput(
        artifact_id=f"pkg-{batch.batch_id}",
        artifact_path=artifact.artifact_path,
        checksum=artifact.checksum or "sha256:test",
        kind=InputKind.PREPARED_UNIT,
        batch_item_ids=[batch.items[0].item_id],
        page_numbers=[1],
    )


def _write_pdf_image(output_dir: Path, batch: PlannedRunnerBatch) -> PackagedRunnerInput:
    from bochord.models.ocr import PackagingStrategy
    from bochord.services.runner_packaging import RunnerInputPackager

    bundle_root = output_dir / "bundle"
    bundle_root.mkdir()
    for artifact in batch.artifacts:
        destination = bundle_root / artifact.artifact_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (64, 32), color=(200, 100, 50)).save(destination)
    return RunnerInputPackager().package(
        batch,
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        bundle_root,
        output_dir,
    )


def packaged_input(item_count: int, output_dir: Path) -> PackagedRunnerInput:
    """Create a packaged input artifact under ``output_dir``."""
    batch = planned_batch(item_count)
    if item_count == 1:
        return _write_direct_image(output_dir, batch)
    return _write_pdf_image(output_dir, batch)


def test_health_check_requires_models_readiness(tmp_path: Path) -> None:
    client = mock_client(get_status=503)
    with pytest.raises(RunnerEndpointUnavailable):
        hosted_runner(client).health_check()


def test_raw_response_is_saved_and_mapped_before_parsing(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(
        post_responses=[httpx.Response(200, json=olmocr_response("þā"))]
    )
    result = hosted_runner(client).invoke(
        batch,
        _write_direct_image(tmp_path, batch),
        tmp_path,
    )
    assert result.failure_item_ids == []
    artifact = result.output_artifacts[0]
    assert artifact.batch_item_ids == [batch.items[0].item_id]
    saved = Path(tmp_path, artifact.artifact_path).read_text(encoding="utf-8")
    assert "þā" in saved


def test_retryable_status_codes_capture_failure(tmp_path: Path) -> None:
    batch = planned_batch(1)
    for status_code in (429, 502):
        client = mock_client(
            post_responses=[httpx.Response(status_code, json={"error": "busy"})]
        )
        result = hosted_runner(client).invoke(
            batch,
            _write_direct_image(tmp_path, batch),
            tmp_path,
        )
        assert result.failure_item_ids == [batch.items[0].item_id]
        assert result.output_artifacts == []
        assert any(str(status_code) in warning for warning in result.warnings)


def test_timeout_captures_failure(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(post_responses=[httpx.TimeoutException("timed out")])
    result = hosted_runner(client).invoke(
        batch,
        _write_direct_image(tmp_path, batch),
        tmp_path,
    )
    assert result.failure_item_ids == [batch.items[0].item_id]
    assert result.output_artifacts == []
    assert result.warnings


def test_missing_token_raises() -> None:
    client = mock_client()
    with pytest.raises(ConfigurationError, match="token"):
        HuggingFaceOlmocrRunner(
            runner=runner_reference(),
            policy=policy(),
            endpoint_url=ENDPOINT_URL,
            token="",
            client=client,  # type: ignore[arg-type]
        )


def test_idempotency_header_is_sent(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(
        post_responses=[httpx.Response(200, json=olmocr_response("ok"))]
    )
    hosted_runner(client).invoke(
        batch,
        _write_direct_image(tmp_path, batch),
        tmp_path,
    )
    headers = client.post_calls[0][1]["headers"]
    assert headers["Idempotency-Key"] == f"{batch.batch_id}:{batch.items[0].item_id}"


def test_no_local_fallback_or_subprocess_call(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(
        post_responses=[httpx.Response(200, json=olmocr_response("ok"))]
    )
    with (
        patch.object(subprocess, "run") as mock_run,
        patch.object(subprocess, "Popen") as mock_popen,
        patch.object(subprocess, "call") as mock_call,
    ):
        hosted_runner(client).invoke(
            batch,
            _write_direct_image(tmp_path, batch),
            tmp_path,
        )
    mock_run.assert_not_called()
    mock_popen.assert_not_called()
    mock_call.assert_not_called()


def test_partial_batch_preserves_successful_item_artifacts(tmp_path: Path) -> None:
    batch = planned_batch(2, batch_id="batch-partial")
    client = mock_client(
        post_responses=[
            httpx.Response(
                200,
                json=olmocr_response("first"),
                headers={"x-request-id": "req-1"},
            ),
            httpx.Response(502, json={"error": "upstream"}),
        ]
    )
    result = hosted_runner(client).invoke(
        batch,
        _write_pdf_image(tmp_path, batch),
        tmp_path,
    )
    assert result.failure_item_ids == [batch.items[1].item_id]
    assert len(result.output_artifacts) == 1
    assert result.output_artifacts[0].batch_item_ids == [batch.items[0].item_id]
    assert result.request_ids == ["req-1"]
    witness_root = tmp_path / "witnesses" / batch.batch_id
    assert (witness_root / f"{batch.items[0].item_id}.json").exists()
    assert not (witness_root / f"{batch.items[1].item_id}.json").exists()


def test_health_check_uses_models_endpoint() -> None:
    client = mock_client()
    hosted_runner(client).health_check()
    assert client.get_calls[0][0] == f"{ENDPOINT_URL}/models"


def test_scale_up_timeout_header_uses_policy_value(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(
        post_responses=[httpx.Response(200, json=olmocr_response("ok"))]
    )
    runner = HuggingFaceOlmocrRunner(
        runner=runner_reference(),
        policy=policy(
            endpoint={
                **runner_policy_payload()["endpoint"],  # type: ignore[index]
                "cold_start_timeout_seconds": 600,
            },
        ),
        endpoint_url=ENDPOINT_URL,
        token=TOKEN,
        client=client,  # type: ignore[arg-type]
    )
    runner.invoke(batch, _write_direct_image(tmp_path, batch), tmp_path)
    headers = client.post_calls[0][1]["headers"]
    assert headers["X-Scale-Up-Timeout"] == "600"


def test_olmocr_capability_matches_spec() -> None:
    from bochord.models.ocr import BatchUnitKind, PackagingStrategy
    from bochord.services.olmocr_runner import OLMOCR_CAPABILITY

    assert OLMOCR_CAPABILITY.preferred_input_kind is InputKind.PDF
    assert OLMOCR_CAPABILITY.supports_multi_item_batching is True
    assert OLMOCR_CAPABILITY.batch_unit_kind is BatchUnitKind.PREPARED_UNIT
    assert OLMOCR_CAPABILITY.packaging_strategy is PackagingStrategy.UNIT_TO_PDF_BATCH
    assert set(OLMOCR_CAPABILITY.accepted_input_kinds) == {
        InputKind.IMAGE,
        InputKind.PREPARED_UNIT,
        InputKind.PDF,
    }
