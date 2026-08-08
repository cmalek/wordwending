# Copyright (C) 2026 Chris Malek.
"""Tests for hosted kraken batch execution (provisional HF adapter)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

import httpx
import pytest
from PIL import Image

from tests.test_runner_packaging import planned_batch as packaging_planned_batch
from wordwending.exc import ConfigurationError, RunnerEndpointUnavailable
from wordwending.models.ocr import (
    InputKind,
    RunnerReference,
)
from wordwending.models.runner_execution import (
    PackagedRunnerInput,
    PlannedRunnerBatch,
    RunnerExecutionPolicy,
)
from wordwending.services.kraken_runner import (
    KRAKEN_TRANSCRIPTION_PROMPT,
    HuggingFaceKrakenRunner,
)
from wordwending.services.witness_adaptation import KRAKEN_SEGMENTATION_SCHEMA

ENDPOINT_URL = "https://example.endpoints.huggingface.cloud/v1"
TOKEN = "hf_test_token"  # noqa: S105
POLICY_FIXTURE = Path(__file__).parent / "fixtures" / "runner" / "olmocr-policy-v1.json"


def kraken_response(text: str) -> dict[str, Any]:
    """
    Return an OpenAI-compatible chat.completion payload for kraken mocks.

    Provisional HF kraken request shape is OpenAI-compatible chat.completions;
    raw witnesses are exact response bytes (ADR 0004), runner_id=kraken.
    """
    return {
        "id": "chatcmpl-kraken-test",
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
        get_error: BaseException | None = None,
        post_responses: list[httpx.Response | BaseException] | None = None,
    ) -> None:
        self.get_status = get_status
        self.get_json = (
            get_json if get_json is not None else {"data": [{"id": "model"}]}
        )
        self.get_error = get_error
        self.post_responses = list(post_responses or [])
        self.get_calls: list[tuple[str, dict[str, Any]]] = []
        self.post_calls: list[tuple[str, dict[str, Any]]] = []

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        self.get_calls.append((url, kwargs))
        if self.get_error is not None:
            raise self.get_error
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
    payload = json.loads(POLICY_FIXTURE.read_text())
    payload.update(overrides)
    return RunnerExecutionPolicy.model_validate(payload)


def runner_reference(**overrides: object) -> RunnerReference:
    """Return a default kraken runner reference with optional overrides."""
    payload: dict[str, object] = {
        "runner_id": "kraken",
        "runner_version": "5.2.5",
        "model_name": "mittagessen/kraken",
        "model_revision": "model-revision",
        "hardware_class": "nvidia-l40s",
        "runtime_name": "huggingface-endpoint",
        "runtime_revision": "container-digest",
        "config_digest": "sha256:runner-config",
        "prompt_digest": "sha256:prompt",
    }
    payload.update(overrides)
    return RunnerReference.model_validate(payload)


def policy_with_endpoint(**endpoint_overrides: object) -> RunnerExecutionPolicy:
    """Return a policy whose endpoint block includes ``endpoint_overrides``."""
    payload = json.loads(POLICY_FIXTURE.read_text())
    endpoint = dict(cast("dict[str, object]", payload["endpoint"]))
    endpoint.update(endpoint_overrides)
    payload["endpoint"] = endpoint
    return RunnerExecutionPolicy.model_validate(payload)


def hosted_runner(
    client: MockHttpxClient,
    *,
    token: str = TOKEN,
    endpoint_url: str = ENDPOINT_URL,
) -> HuggingFaceKrakenRunner:
    """Construct a hosted kraken runner backed by ``client``."""
    return HuggingFaceKrakenRunner(
        runner=runner_reference(),
        policy=policy(),
        endpoint_url=endpoint_url,
        token=token,
        client=client,  # type: ignore[arg-type]
    )


def planned_batch(
    item_count: int,
    *,
    batch_id: str = "batch-test",
    orders: list[int] | None = None,
) -> PlannedRunnerBatch:
    """Build a planned batch for hosted runner tests."""
    return packaging_planned_batch(item_count, batch_id=batch_id, orders=orders)


def _write_direct_image(
    output_dir: Path, batch: PlannedRunnerBatch
) -> PackagedRunnerInput:
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


def _write_pdf_image(
    output_dir: Path, batch: PlannedRunnerBatch
) -> PackagedRunnerInput:
    from tests.test_runner_batching import artifacts as batching_artifacts
    from wordwending.models.ocr import PackagingStrategy
    from wordwending.services.runner_packaging import RunnerInputPackager

    bundle_root = output_dir / "bundle"
    bundle_root.mkdir()
    for artifact in batch.artifacts:
        destination = bundle_root / artifact.artifact_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (64, 32), color=(200, 100, 50)).save(destination)
    for artifact in batching_artifacts(8):
        destination = bundle_root / artifact.artifact_path
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (64, 32), color=(200, 100, 50)).save(destination)
    return RunnerInputPackager().package(
        batch,
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        bundle_root,
        output_dir,
    )


def test_health_check_requires_models_readiness() -> None:
    client = mock_client(get_status=503)
    with pytest.raises(RunnerEndpointUnavailable):
        hosted_runner(client).health_check()


def test_health_check_network_failure_raises_unavailable() -> None:
    client = mock_client(get_error=httpx.ConnectError("connection refused"))
    with pytest.raises(RunnerEndpointUnavailable, match="connection refused"):
        hosted_runner(client).health_check()


def test_raw_response_is_saved_exact_bytes(tmp_path: Path) -> None:
    batch = planned_batch(1)
    payload = kraken_response("þā")
    raw_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    client = mock_client(
        post_responses=[
            httpx.Response(
                200,
                content=raw_bytes,
                headers={"content-type": "application/json"},
            )
        ]
    )
    result = hosted_runner(client).invoke(
        batch,
        _write_direct_image(tmp_path, batch),
        tmp_path,
    )
    assert result.failure_item_ids == []
    artifact = result.output_artifacts[0]
    assert artifact.batch_item_ids == [batch.items[0].item_id]
    saved = Path(tmp_path, artifact.artifact_path).read_bytes()
    assert saved == raw_bytes
    assert "þā" in saved.decode("utf-8")


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
        HuggingFaceKrakenRunner(
            runner=runner_reference(),
            policy=policy(),
            endpoint_url=ENDPOINT_URL,
            token="",
            client=client,  # type: ignore[arg-type]
        )


def test_idempotency_header_is_sent(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(
        post_responses=[httpx.Response(200, json=kraken_response("ok"))]
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
        post_responses=[httpx.Response(200, json=kraken_response("ok"))]
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


def test_connection_error_on_second_item_preserves_first_artifact(
    tmp_path: Path,
) -> None:
    batch = planned_batch(2, batch_id="batch-connect")
    client = mock_client(
        post_responses=[
            httpx.Response(
                200,
                json=kraken_response("first"),
                headers={"x-request-id": "req-1"},
            ),
            httpx.ConnectError("connection refused"),
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
    assert any("connection refused" in warning for warning in result.warnings)
    witness_root = tmp_path / "witnesses" / batch.batch_id
    assert (witness_root / f"{batch.items[0].item_id}.json").exists()
    assert not (witness_root / f"{batch.items[1].item_id}.json").exists()


def test_partial_batch_preserves_successful_item_artifacts(tmp_path: Path) -> None:
    batch = planned_batch(2, batch_id="batch-partial")
    client = mock_client(
        post_responses=[
            httpx.Response(
                200,
                json=kraken_response("first"),
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
        post_responses=[httpx.Response(200, json=kraken_response("ok"))]
    )
    runner = HuggingFaceKrakenRunner(
        runner=runner_reference(),
        policy=policy_with_endpoint(cold_start_timeout_seconds=600),
        endpoint_url=ENDPOINT_URL,
        token=TOKEN,
        client=client,  # type: ignore[arg-type]
    )
    runner.invoke(batch, _write_direct_image(tmp_path, batch), tmp_path)
    headers = client.post_calls[0][1]["headers"]
    assert headers["X-Scale-Up-Timeout"] == "600"


def test_runner_exposes_execution_contract() -> None:
    """Hosted kraken runner public properties match orchestrator expectations."""
    client = mock_client()
    runner = hosted_runner(client)
    assert runner.policy.policy_id == "olmocr-hf-fixed-v1"
    assert runner.runner_ref.runner_id == "kraken"
    assert runner.capability.supports_multi_item_batching is True


def test_kraken_transcription_prompt_requests_v1_json_only() -> None:
    """Runner prompt must demand wordwending.kraken_segmentation/v1 JSON only."""
    assert KRAKEN_SEGMENTATION_SCHEMA in KRAKEN_TRANSCRIPTION_PROMPT
    lowered = KRAKEN_TRANSCRIPTION_PROMPT.lower()
    assert "json" in lowered
    assert "bbox" in lowered or "bounding" in lowered
    assert "baseline" in lowered
    assert "markdown" in lowered or "fence" in lowered or "commentary" in lowered


def test_kraken_capability_matches_spine_packaging() -> None:
    from wordwending.models.ocr import BatchUnitKind, PackagingStrategy
    from wordwending.services.kraken_runner import KRAKEN_CAPABILITY

    assert KRAKEN_CAPABILITY.preferred_input_kind is InputKind.PDF
    assert KRAKEN_CAPABILITY.supports_multi_item_batching is True
    assert KRAKEN_CAPABILITY.batch_unit_kind is BatchUnitKind.PREPARED_UNIT
    assert KRAKEN_CAPABILITY.packaging_strategy is PackagingStrategy.UNIT_TO_PDF_BATCH
    assert set(KRAKEN_CAPABILITY.accepted_input_kinds) == {
        InputKind.IMAGE,
        InputKind.PREPARED_UNIT,
        InputKind.PDF,
    }


def test_completion_posts_openai_compatible_chat_completions(tmp_path: Path) -> None:
    batch = planned_batch(1)
    client = mock_client(
        post_responses=[httpx.Response(200, json=kraken_response("ok"))]
    )
    hosted_runner(client).invoke(
        batch,
        _write_direct_image(tmp_path, batch),
        tmp_path,
    )
    url, kwargs = client.post_calls[0]
    assert url == f"{ENDPOINT_URL}/chat/completions"
    payload = kwargs["json"]
    assert payload["model"] == "mittagessen/kraken"
    assert payload["messages"][0]["role"] == "user"
    content = payload["messages"][0]["content"]
    assert any(part.get("type") == "image_url" for part in content)
    assert any(part.get("type") == "text" for part in content)


def test_packaged_pdf_invoke_uses_positional_page_numbers(tmp_path: Path) -> None:
    batch = planned_batch(4, orders=[5, 6, 7, 8])
    client = mock_client(
        post_responses=[
            httpx.Response(200, json=kraken_response(f"page-{index}"))
            for index in range(1, 5)
        ]
    )
    result = hosted_runner(client).invoke(
        batch,
        _write_pdf_image(tmp_path, batch),
        tmp_path,
    )
    assert result.failure_item_ids == []
    assert len(result.output_artifacts) == 4


def test_missing_packaged_input_captures_failed_item(tmp_path: Path) -> None:
    batch = planned_batch(1)
    packaged = _write_direct_image(tmp_path, batch)
    missing_path = tmp_path / packaged.artifact_path
    missing_path.unlink()
    client = mock_client(
        post_responses=[httpx.Response(200, json=kraken_response("ok"))]
    )
    result = hosted_runner(client).invoke(batch, packaged, tmp_path)
    assert result.failure_item_ids == [batch.items[0].item_id]
    assert result.output_artifacts == []
    assert any("missing packaged input" in warning for warning in result.warnings)
