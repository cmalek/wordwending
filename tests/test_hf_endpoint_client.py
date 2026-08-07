# Copyright (C) 2026 Chris Malek.
"""Tests for Hugging Face Inference Endpoint client wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import Mock

import pytest
from huggingface_hub.errors import InferenceEndpointError, InferenceEndpointTimeoutError
from huggingface_hub.utils import HfHubHTTPError

from wordwending.exc import ConfigurationError, EndpointLifecycleError
from wordwending.models.endpoint_lifecycle import (
    EndpointRemoteState,
    default_endpoint_catalog,
)
from wordwending.services.hf_endpoint_client import HfEndpointClient

TOKEN = "hf_test"  # noqa: S105


@dataclass
class _FakeInferenceEndpoint:
    name: str
    namespace: str
    repository: str
    status: str
    url: str | None = None

    def wait(
        self,
        timeout: int | None = None,
        refresh_every: int = 5,
    ) -> _FakeInferenceEndpoint:
        del refresh_every
        if timeout == 0:
            msg = "timed out"
            raise InferenceEndpointTimeoutError(msg)
        return _FakeInferenceEndpoint(
            name=self.name,
            namespace=self.namespace,
            repository=self.repository,
            status="running",
            url=self.url or "https://example.endpoints.huggingface.cloud",
        )


def test_constructor_requires_token() -> None:
    with pytest.raises(ConfigurationError, match="token"):
        HfEndpointClient("")


def test_describe_maps_remote_state(monkeypatch: pytest.MonkeyPatch) -> None:
    endpoint = _FakeInferenceEndpoint(
        name="ww-olmocr",
        namespace="ns",
        repository="org/model",
        status="running",
        url="https://example.endpoints.huggingface.cloud",
    )

    def fake_get(
        _self: Any,
        name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        assert name == "ww-olmocr"
        assert namespace == "ns"
        assert token == TOKEN
        return endpoint

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.get_inference_endpoint",
        fake_get,
    )
    client = HfEndpointClient(TOKEN)
    state = client.describe("ww-olmocr", namespace="ns")
    assert state == EndpointRemoteState(
        name="ww-olmocr",
        status="running",
        url="https://example.endpoints.huggingface.cloud",
    )


def test_create_passes_catalog_fields_and_scale_to_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    entry = default_endpoint_catalog()[0]

    def fake_create(
        _self: Any,
        name: str,
        **kwargs: Any,
    ) -> _FakeInferenceEndpoint:
        captured["name"] = name
        captured.update(kwargs)
        return _FakeInferenceEndpoint(
            name=name,
            namespace=entry.namespace,
            repository=entry.repository,
            status="pending",
            url=None,
        )

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.create_inference_endpoint",
        fake_create,
    )
    client = HfEndpointClient(TOKEN)
    state = client.create(entry)
    assert captured["name"] == entry.endpoint_name
    assert captured["repository"] == entry.repository
    assert captured["revision"] == entry.revision
    assert captured["namespace"] == entry.namespace
    assert captured["scale_to_zero_timeout"] is not None
    assert state.status == "pending"
    assert state.url is None


def test_create_omits_scale_to_zero_when_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    entry = default_endpoint_catalog()[0].model_copy(update={"scale_to_zero": False})

    def fake_create(
        _self: Any,
        name: str,
        **kwargs: Any,
    ) -> _FakeInferenceEndpoint:
        captured.update(kwargs)
        return _FakeInferenceEndpoint(
            name=name,
            namespace=entry.namespace,
            repository=entry.repository,
            status="pending",
        )

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.create_inference_endpoint",
        fake_create,
    )
    client = HfEndpointClient(TOKEN)
    client.create(entry)
    assert "scale_to_zero_timeout" not in captured


def test_wait_ready_returns_running_state(monkeypatch: pytest.MonkeyPatch) -> None:
    pending = _FakeInferenceEndpoint(
        name="ww-olmocr",
        namespace="ns",
        repository="org/model",
        status="pending",
        url=None,
    )

    def fake_get(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        del namespace, token
        return pending

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.get_inference_endpoint",
        fake_get,
    )
    client = HfEndpointClient(TOKEN)
    state = client.wait_ready("ww-olmocr", namespace="ns", timeout_seconds=60)
    assert state.status == "running"
    assert state.url is not None
    assert state.url.startswith("https://")


def test_hub_errors_map_to_endpoint_lifecycle_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        del namespace, token
        response = Mock()
        response.headers = {}
        msg = "boom"
        raise HfHubHTTPError(msg, response=response)

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.get_inference_endpoint",
        fake_get,
    )
    client = HfEndpointClient(TOKEN)
    with pytest.raises(EndpointLifecycleError):
        client.describe("ww-olmocr")


def test_wait_ready_timeout_maps_to_endpoint_lifecycle_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pending = _FakeInferenceEndpoint(
        name="ww-olmocr",
        namespace="ns",
        repository="org/model",
        status="pending",
    )

    def fake_get(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        del namespace, token
        return pending

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.get_inference_endpoint",
        fake_get,
    )
    client = HfEndpointClient(TOKEN)
    with pytest.raises(EndpointLifecycleError):
        client.wait_ready("ww-olmocr", timeout_seconds=0)


def test_lifecycle_mutators_delegate_to_hub(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def make_endpoint(status: str) -> _FakeInferenceEndpoint:
        return _FakeInferenceEndpoint(
            name="ww-olmocr",
            namespace="ns",
            repository="org/model",
            status=status,
        )

    def fake_pause(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        del namespace, token
        calls.append("pause")
        return make_endpoint("paused")

    def fake_resume(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
        running_ok: bool = True,
    ) -> _FakeInferenceEndpoint:
        del namespace, token, running_ok
        calls.append("resume")
        return make_endpoint("pending")

    def fake_scale(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        del namespace, token
        calls.append("scale")
        return make_endpoint("scaledToZero")

    def fake_delete(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> None:
        del namespace, token
        calls.append("delete")

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.pause_inference_endpoint",
        fake_pause,
    )
    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.resume_inference_endpoint",
        fake_resume,
    )
    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.scale_to_zero_inference_endpoint",
        fake_scale,
    )
    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.delete_inference_endpoint",
        fake_delete,
    )

    client = HfEndpointClient(TOKEN)
    assert client.pause("ww-olmocr", namespace="ns").status == "paused"
    assert client.resume("ww-olmocr", namespace="ns").status == "pending"
    assert client.scale_to_zero("ww-olmocr", namespace="ns").status == "scaledToZero"
    client.delete("ww-olmocr", namespace="ns")
    assert calls == ["pause", "resume", "scale", "delete"]


def test_inference_endpoint_error_maps_to_lifecycle_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_pause(
        _self: Any,
        _name: str,
        *,
        namespace: str | None = None,
        token: str | None = None,
    ) -> _FakeInferenceEndpoint:
        del namespace, token
        msg = "failed"
        raise InferenceEndpointError(msg)

    monkeypatch.setattr(
        "wordwending.services.hf_endpoint_client.HfApi.pause_inference_endpoint",
        fake_pause,
    )
    client = HfEndpointClient(TOKEN)
    with pytest.raises(EndpointLifecycleError, match="failed"):
        client.pause("ww-olmocr")
