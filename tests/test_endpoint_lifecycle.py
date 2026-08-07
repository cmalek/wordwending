# Copyright (C) 2026 Chris Malek.
"""Tests for EndpointLifecycleService orchestration."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path  # noqa: TC003

import pytest

from wordwending.exc import ConfigurationError, EndpointLifecycleError
from wordwending.models.endpoint_lifecycle import (
    EndpointCatalogEntry,
    EndpointLastAction,
    EndpointLedgerEntry,
    EndpointRemoteState,
    EndpointSessionLedger,
    default_endpoint_catalog,
)
from wordwending.services.endpoint_lifecycle import EndpointLifecycleService
from wordwending.services.endpoint_session_ledger import EndpointSessionLedgerStore
from wordwending.services.hf_endpoint_client import EndpointClient
from wordwending.settings import Settings


class FakeHfEndpointClient:
    """In-memory ``EndpointClient`` double for lifecycle unit tests."""

    def __init__(self) -> None:
        self.states: dict[str, EndpointRemoteState] = {}
        self.created: list[str] = []
        self.resumed: list[str] = []
        self.paused: list[str] = []
        self.deleted: list[str] = []
        self.waited: list[str] = []
        self.create_entries: list[EndpointCatalogEntry] = []
        self.raise_on_describe: Exception | None = None

    def describe(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        del namespace
        if self.raise_on_describe is not None:
            raise self.raise_on_describe
        state = self.states.get(name)
        if state is None:
            msg = f"endpoint {name!r} not found"
            raise EndpointLifecycleError(msg)
        return state

    def create(self, entry: EndpointCatalogEntry) -> EndpointRemoteState:
        self.created.append(entry.endpoint_name)
        self.create_entries.append(entry)
        state = EndpointRemoteState(
            name=entry.endpoint_name,
            status="pending",
            url=None,
        )
        self.states[entry.endpoint_name] = state
        return state

    def resume(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        del namespace
        self.resumed.append(name)
        state = EndpointRemoteState(
            name=name,
            status="pending",
            url=self.states.get(
                name, EndpointRemoteState(name=name, status="pending")
            ).url,
        )
        self.states[name] = state
        return state

    def pause(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        del namespace
        self.paused.append(name)
        prior = self.states.get(name)
        state = EndpointRemoteState(
            name=name,
            status="paused",
            url=prior.url if prior is not None else None,
        )
        self.states[name] = state
        return state

    def scale_to_zero(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        del namespace
        prior = self.states.get(name)
        state = EndpointRemoteState(
            name=name,
            status="scaledToZero",
            url=prior.url if prior is not None else f"https://{name}.example.cloud",
        )
        self.states[name] = state
        return state

    def delete(self, name: str, *, namespace: str | None) -> None:
        del namespace
        self.deleted.append(name)
        self.states.pop(name, None)

    def wait_ready(
        self,
        name: str,
        *,
        namespace: str | None,
        timeout_seconds: int,
    ) -> EndpointRemoteState:
        del namespace, timeout_seconds
        self.waited.append(name)
        prior = self.states.get(name)
        url = (
            prior.url
            if prior is not None and prior.url is not None
            else f"https://{name}.endpoints.huggingface.cloud"
        )
        state = EndpointRemoteState(name=name, status="running", url=url)
        self.states[name] = state
        return state


def _assert_is_endpoint_client(client: FakeHfEndpointClient) -> EndpointClient:
    assert isinstance(client, EndpointClient)
    return client


def _catalog() -> list[EndpointCatalogEntry]:
    return default_endpoint_catalog()


def _settings(*, idle_minutes: int = 30, wait_timeout: int = 900) -> Settings:
    return Settings(
        huggingface_endpoint_idle_minutes=idle_minutes,
        huggingface_endpoint_wait_timeout_seconds=wait_timeout,
    )


def _service(
    tmp_path: Path,
    client: FakeHfEndpointClient | None = None,
    *,
    settings: Settings | None = None,
    catalog: list[EndpointCatalogEntry] | None = None,
) -> tuple[EndpointLifecycleService, FakeHfEndpointClient, EndpointSessionLedgerStore]:
    fake = client or FakeHfEndpointClient()
    _assert_is_endpoint_client(fake)
    ledger = EndpointSessionLedgerStore(tmp_path / "ledger.json")
    service = EndpointLifecycleService(
        client=fake,
        ledger=ledger,
        settings=settings or _settings(),
        catalog=catalog or _catalog(),
    )
    return service, fake, ledger


def test_ensure_up_creates_missing_and_returns_https_url(tmp_path: Path) -> None:
    service, client, ledger = _service(tmp_path)
    result = service.ensure_up(["olmocr"])
    assert "olmocr" in result.urls_by_runner_id
    assert result.urls_by_runner_id["olmocr"].startswith("https://")
    assert client.created == ["ww-olmocr"]
    assert "olmocr" in result.created_runner_ids
    assert client.waited == ["ww-olmocr"]
    loaded = ledger.load()
    assert loaded.entries["olmocr"].last_action == EndpointLastAction.UP
    assert loaded.entries["olmocr"].url.startswith("https://")


def test_ensure_up_resumes_paused_and_scaled_to_zero(tmp_path: Path) -> None:
    service, client, _ledger = _service(tmp_path)
    client.states["ww-olmocr"] = EndpointRemoteState(
        name="ww-olmocr",
        status="paused",
        url="https://ww-olmocr.endpoints.huggingface.cloud",
    )
    client.states["ww-kraken"] = EndpointRemoteState(
        name="ww-kraken",
        status="scaledToZero",
        url="https://ww-kraken.endpoints.huggingface.cloud",
    )
    result = service.ensure_up(["olmocr", "kraken"])
    assert set(client.resumed) == {"ww-olmocr", "ww-kraken"}
    assert set(result.resumed_runner_ids) == {"olmocr", "kraken"}
    assert client.created == []
    assert set(result.urls_by_runner_id) == {"olmocr", "kraken"}


def test_ensure_up_already_running_skips_create_and_resume(tmp_path: Path) -> None:
    service, client, _ledger = _service(tmp_path)
    client.states["ww-olmocr"] = EndpointRemoteState(
        name="ww-olmocr",
        status="running",
        url="https://ww-olmocr.endpoints.huggingface.cloud",
    )
    result = service.ensure_up(["olmocr"])
    assert client.created == []
    assert client.resumed == []
    assert client.waited == ["ww-olmocr"]
    assert result.already_ready_runner_ids == ["olmocr"]
    assert result.urls_by_runner_id["olmocr"].startswith("https://")


def test_ensure_up_passes_scale_to_zero_catalog_entry(tmp_path: Path) -> None:
    catalog = _catalog()
    catalog[0] = catalog[0].model_copy(update={"scale_to_zero": True})
    service, client, _ledger = _service(tmp_path, catalog=catalog)
    service.ensure_up(["olmocr"])
    assert client.create_entries[0].scale_to_zero is True


def test_ensure_up_empty_runner_ids_means_all_catalogued(tmp_path: Path) -> None:
    service, client, _ledger = _service(tmp_path)
    result = service.ensure_up([])
    assert set(result.urls_by_runner_id) == {"olmocr", "kraken"}
    assert set(client.created) == {"ww-olmocr", "ww-kraken"}


def test_ensure_up_unknown_runner_fails_closed(tmp_path: Path) -> None:
    service, _client, _ledger = _service(tmp_path)
    with pytest.raises(EndpointLifecycleError, match="nope") as exc_info:
        service.ensure_up(["nope"])
    message = str(exc_info.value)
    assert "olmocr" in message
    assert "kraken" in message


def test_ensure_up_partial_failure_fails_closed(tmp_path: Path) -> None:
    service, client, _ledger = _service(tmp_path)

    def flaky_wait(
        name: str,
        *,
        namespace: str | None,
        timeout_seconds: int,
    ) -> EndpointRemoteState:
        del namespace, timeout_seconds
        if name == "ww-kraken":
            msg = "kraken cold start failed"
            raise EndpointLifecycleError(msg)
        return FakeHfEndpointClient.wait_ready(
            client,
            name,
            namespace=None,
            timeout_seconds=1,
        )

    client.wait_ready = flaky_wait  # type: ignore[method-assign]
    with pytest.raises(EndpointLifecycleError, match="kraken") as exc_info:
        service.ensure_up(["olmocr", "kraken"])
    assert "failed" in str(exc_info.value).lower()


def test_ensure_up_propagates_configuration_error(tmp_path: Path) -> None:
    service, client, _ledger = _service(tmp_path)
    client.raise_on_describe = ConfigurationError("missing huggingface API token")
    with pytest.raises(ConfigurationError, match="token"):
        service.ensure_up(["olmocr"])


def test_down_pauses_by_default_delete_flag_destroys(tmp_path: Path) -> None:
    service, client, ledger = _service(tmp_path)
    client.states["ww-olmocr"] = EndpointRemoteState(
        name="ww-olmocr",
        status="running",
        url="https://ww-olmocr.endpoints.huggingface.cloud",
    )
    client.states["ww-kraken"] = EndpointRemoteState(
        name="ww-kraken",
        status="running",
        url="https://ww-kraken.endpoints.huggingface.cloud",
    )
    paused = service.down(["olmocr"])
    assert paused.paused_runner_ids == ["olmocr"]
    assert paused.deleted_runner_ids == []
    assert client.paused == ["ww-olmocr"]
    assert client.deleted == []
    assert ledger.load().entries["olmocr"].last_action == EndpointLastAction.PAUSE

    deleted = service.down(["kraken"], delete=True)
    assert deleted.deleted_runner_ids == ["kraken"]
    assert deleted.paused_runner_ids == []
    assert client.deleted == ["ww-kraken"]
    assert ledger.load().entries["kraken"].last_action == EndpointLastAction.DOWN


def test_pause_idle_pauses_only_stale_entries(tmp_path: Path) -> None:
    now = datetime(2026, 8, 7, 15, 0, tzinfo=UTC)
    service, client, ledger = _service(tmp_path, settings=_settings(idle_minutes=30))
    for name in ("ww-olmocr", "ww-kraken"):
        client.states[name] = EndpointRemoteState(
            name=name,
            status="running",
            url=f"https://{name}.endpoints.huggingface.cloud",
        )
    ledger.save(
        EndpointSessionLedger(
            entries={
                "olmocr": EndpointLedgerEntry(
                    runner_id="olmocr",
                    endpoint_name="ww-olmocr",
                    namespace="operator-namespace-required",
                    endpoint_url="https://ww-olmocr.endpoints.huggingface.cloud",
                    last_used_at_utc=now - timedelta(minutes=45),
                    last_action=EndpointLastAction.UP,
                ),
                "kraken": EndpointLedgerEntry(
                    runner_id="kraken",
                    endpoint_name="ww-kraken",
                    namespace="operator-namespace-required",
                    endpoint_url="https://ww-kraken.endpoints.huggingface.cloud",
                    last_used_at_utc=now - timedelta(minutes=5),
                    last_action=EndpointLastAction.UP,
                ),
            }
        )
    )
    result = service.pause_idle(now=now)
    assert result.paused_runner_ids == ["olmocr"]
    assert result.deleted_runner_ids == []
    assert client.paused == ["ww-olmocr"]
    assert client.deleted == []


def test_status_combines_hf_and_ledger(tmp_path: Path) -> None:
    stamp = datetime(2026, 8, 7, 12, 0, tzinfo=UTC)
    service, client, ledger = _service(tmp_path)
    client.states["ww-olmocr"] = EndpointRemoteState(
        name="ww-olmocr",
        status="running",
        url="https://ww-olmocr.endpoints.huggingface.cloud",
    )
    ledger.save(
        EndpointSessionLedger(
            entries={
                "olmocr": EndpointLedgerEntry(
                    runner_id="olmocr",
                    endpoint_name="ww-olmocr",
                    namespace="operator-namespace-required",
                    endpoint_url="https://ww-olmocr.endpoints.huggingface.cloud",
                    last_used_at_utc=stamp,
                    last_action=EndpointLastAction.UP,
                )
            }
        )
    )
    report = service.status(["olmocr"])
    assert len(report.rows) == 1
    row = report.rows[0]
    assert row.runner_id == "olmocr"
    assert row.hf_status == "running"
    assert row.endpoint_url == "https://ww-olmocr.endpoints.huggingface.cloud"
    assert row.last_used_at_utc == stamp


def test_status_none_means_all_catalogued(tmp_path: Path) -> None:
    service, client, _ledger = _service(tmp_path)
    for name in ("ww-olmocr", "ww-kraken"):
        client.states[name] = EndpointRemoteState(
            name=name,
            status="paused",
            url=None,
        )
    report = service.status()
    assert [row.runner_id for row in report.rows] == ["olmocr", "kraken"]


def test_fake_satisfies_endpoint_client_protocol() -> None:
    assert isinstance(FakeHfEndpointClient(), EndpointClient)
