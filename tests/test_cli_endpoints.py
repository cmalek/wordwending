# Copyright (C) 2026 Chris Malek.
"""Tests for the endpoints CLI command group."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.test_cli_commands import _run_cli_args
from wordwending.cli.cli import cli
from wordwending.exc import EndpointLifecycleError
from wordwending.models.bakeoff import (
    BAKEOFF_MATRIX_FILENAME,
    BakeoffCandidate,
    BakeoffManifest,
    default_bakeoff_candidates,
)
from wordwending.models.endpoint_lifecycle import (
    EndpointDownResult,
    EndpointEnsureResult,
    EndpointStatusReport,
    EndpointStatusRow,
)
from wordwending.models.ocr import PageClass
from wordwending.models.runner_execution import RunnerThroughputSummary
from wordwending.settings import Settings


class FakeEndpointLifecycleService:
    """In-memory double for endpoint CLI tests."""

    def __init__(self) -> None:
        self.pause_idle_calls = 0
        self.ensure_up_calls: list[list[str]] = []
        self.down_calls: list[tuple[list[str], bool]] = []
        self.status_calls: list[list[str] | None] = []

    def pause_idle(self, *, now: datetime | None = None) -> EndpointDownResult:
        del now
        self.pause_idle_calls += 1
        return EndpointDownResult()

    def ensure_up(self, runner_ids: list[str]) -> EndpointEnsureResult:
        self.ensure_up_calls.append(list(runner_ids))
        urls = {
            runner_id: f"https://ww-{runner_id}.endpoints.huggingface.cloud"
            for runner_id in (runner_ids or ["olmocr", "kraken"])
        }
        selected = list(runner_ids) if runner_ids else ["olmocr", "kraken"]
        return EndpointEnsureResult(
            urls_by_runner_id={rid: urls[rid] for rid in selected},
            created_runner_ids=selected[:1],
            resumed_runner_ids=selected[1:],
        )

    def down(
        self,
        runner_ids: list[str],
        *,
        delete: bool = False,
    ) -> EndpointDownResult:
        self.down_calls.append((list(runner_ids), delete))
        selected = list(runner_ids) if runner_ids else ["olmocr", "kraken"]
        if delete:
            return EndpointDownResult(deleted_runner_ids=selected)
        return EndpointDownResult(paused_runner_ids=selected)

    def status(
        self,
        runner_ids: list[str] | None = None,
    ) -> EndpointStatusReport:
        self.status_calls.append(list(runner_ids) if runner_ids is not None else None)
        selected = runner_ids or ["olmocr", "kraken"]
        return EndpointStatusReport(
            rows=[
                EndpointStatusRow(
                    runner_id=runner_id,
                    endpoint_name=f"ww-{runner_id}",
                    hf_status="running",
                    endpoint_url=f"https://ww-{runner_id}.endpoints.huggingface.cloud",
                    last_used_at_utc=datetime(2026, 1, 1, tzinfo=UTC),
                )
                for runner_id in selected
            ]
        )


class ExplodingEndpointLifecycleService(FakeEndpointLifecycleService):
    """Service that raises on ensure_up for fail-closed CLI tests."""

    def ensure_up(self, runner_ids: list[str]) -> EndpointEnsureResult:
        del runner_ids
        msg = "unknown endpoint runner id(s): bogus; catalogued ids: kraken, olmocr"
        raise EndpointLifecycleError(msg)


@pytest.fixture
def configured_settings() -> Settings:
    return Settings(huggingface_api_key="hf_test_token")


@pytest.fixture
def fake_service() -> FakeEndpointLifecycleService:
    return FakeEndpointLifecycleService()


def test_endpoints_up_prints_urls(
    runner,
    configured_settings: Settings,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        result = runner.invoke(cli, ["endpoints", "up", "--runner", "olmocr"])

    assert result.exit_code == 0
    assert "https://" in result.output
    assert fake_service.pause_idle_calls == 1
    assert fake_service.ensure_up_calls == [["olmocr"]]


def test_endpoints_up_without_runner_targets_catalog(
    runner,
    configured_settings: Settings,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        result = runner.invoke(cli, ["endpoints", "up"])

    assert result.exit_code == 0
    assert "https://" in result.output
    assert fake_service.ensure_up_calls == [[]]


def test_endpoints_down_pauses_by_default(
    runner,
    configured_settings: Settings,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        result = runner.invoke(cli, ["endpoints", "down", "--runner", "olmocr"])

    assert result.exit_code == 0
    assert "paused: olmocr" in result.output
    assert fake_service.down_calls == [(["olmocr"], False)]


def test_endpoints_down_delete(
    runner,
    configured_settings: Settings,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        result = runner.invoke(
            cli,
            ["endpoints", "down", "--runner", "kraken", "--delete"],
        )

    assert result.exit_code == 0
    assert "deleted: kraken" in result.output
    assert fake_service.down_calls == [(["kraken"], True)]


def test_endpoints_status_prints_rows(
    runner,
    configured_settings: Settings,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        result = runner.invoke(cli, ["endpoints", "status", "--runner", "olmocr"])

    assert result.exit_code == 0
    assert "runner_id: olmocr" in result.output
    assert "hf_status: running" in result.output
    assert "https://" in result.output
    assert fake_service.pause_idle_calls == 1
    assert fake_service.status_calls == [["olmocr"]]


def test_endpoints_up_rejects_missing_huggingface_api_key(runner) -> None:
    with patch("wordwending.cli.cli.Settings") as mock_settings:
        mock_settings.return_value = Settings()
        result = runner.invoke(cli, ["endpoints", "up", "--runner", "olmocr"])

    assert result.exit_code != 0
    assert "huggingface_api_key" in result.output


def test_endpoints_unknown_runner_exits_nonzero(
    runner,
    configured_settings: Settings,
) -> None:
    exploding = ExplodingEndpointLifecycleService()
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=exploding,
        ),
    ):
        result = runner.invoke(cli, ["endpoints", "up", "--runner", "bogus"])

    assert result.exit_code != 0
    assert "unknown endpoint runner id" in result.output


@patch("wordwending.cli.cli.RunnerExecutionService.run")
@patch("wordwending.services.pass_runner_registry.HuggingFaceOlmocrRunner")
def test_run_ensure_endpoints_overlays_url_before_invoke(
    mock_olmocr_cls,
    mock_run,
    runner,
    tmp_path: Path,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    """``--ensure-endpoints`` overlays HTTPS URL before hosted runner construction."""
    overlay_url = "https://ww-olmocr.endpoints.huggingface.cloud"
    mock_run.return_value = (
        [],
        RunnerThroughputSummary(
            measured_item_count=0,
            failed_item_count=0,
            measured_duration_seconds=0.0,
            items_per_second=0.0,
        ),
    )
    mock_olmocr_cls.return_value = mock_olmocr_cls
    configured = Settings(huggingface_api_key="hf_test_token")
    with (
        patch("wordwending.cli.cli.Settings", return_value=configured),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        result = runner.invoke(
            cli,
            [*_run_cli_args(tmp_path, runner_id="olmocr"), "--ensure-endpoints"],
        )

    assert result.exit_code == 0, result.output
    assert fake_service.pause_idle_calls == 1
    assert fake_service.ensure_up_calls == [["olmocr"]]
    mock_olmocr_cls.assert_called_once()
    assert mock_olmocr_cls.call_args.kwargs["endpoint_url"] == overlay_url


def test_bakeoff_ensure_endpoints_fail_closed_on_lifecycle_error(
    runner,
    tmp_path: Path,
    configured_settings: Settings,
) -> None:
    """``bakeoff --ensure-endpoints`` aborts when lifecycle ensure fails."""
    profile_src = Path("tests/fixtures/evaluation/metric-profile-v1.json")
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(profile_src.read_text(encoding="utf-8"), encoding="utf-8")
    gold_path = tmp_path / "gold-page.json"
    gold_path.write_text("{}", encoding="utf-8")
    manifest = BakeoffManifest(
        candidates=default_bakeoff_candidates(),
        pages=[
            {
                "page_id": "page-1",
                "page_class": PageClass.ORDINARY_PROSE,
                "gold_path": gold_path.name,
            }
        ],
        predictions=[],
    )
    manifest_path = tmp_path / "bakeoff-manifest.json"
    manifest_path.write_text(manifest.model_dump_json(), encoding="utf-8")
    output_dir = tmp_path / "out"
    exploding = ExplodingEndpointLifecycleService()

    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=exploding,
        ),
    ):
        result = runner.invoke(
            cli,
            [
                "bakeoff",
                "--bundle-root",
                str(tmp_path),
                "--manifest",
                str(manifest_path),
                "--profile",
                str(profile_path),
                "--output-dir",
                str(output_dir),
                "--ensure-endpoints",
            ],
        )

    assert result.exit_code != 0
    assert "unknown endpoint runner id" in result.output
    assert not (output_dir / BAKEOFF_MATRIX_FILENAME).exists()


def test_bakeoff_ensure_endpoints_skips_when_no_catalog_candidates(
    runner,
    tmp_path: Path,
    configured_settings: Settings,
    fake_service: FakeEndpointLifecycleService,
) -> None:
    """Fake-only bakeoff must not expand empty filter into ensure-all catalog."""
    profile_src = Path("tests/fixtures/evaluation/metric-profile-v1.json")
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(profile_src.read_text(encoding="utf-8"), encoding="utf-8")
    gold_path = tmp_path / "gold-page.json"
    gold_path.write_text("{}", encoding="utf-8")
    manifest = BakeoffManifest(
        candidates=[
            BakeoffCandidate(
                runner_id="FakePassRunner",
                license_placeholder="harness",
                cost_placeholder="n/a",
                operability_placeholder="n/a",
            )
        ],
        pages=[
            {
                "page_id": "page-1",
                "page_class": PageClass.ORDINARY_PROSE,
                "gold_path": gold_path.name,
            }
        ],
        predictions=[],
    )
    manifest_path = tmp_path / "bakeoff-manifest.json"
    manifest_path.write_text(manifest.model_dump_json(), encoding="utf-8")
    output_dir = tmp_path / "out"

    with (
        patch("wordwending.cli.cli.Settings", return_value=configured_settings),
        patch(
            "wordwending.cli.endpoints.build_endpoint_lifecycle_service",
            return_value=fake_service,
        ),
    ):
        runner.invoke(
            cli,
            [
                "bakeoff",
                "--bundle-root",
                str(tmp_path),
                "--manifest",
                str(manifest_path),
                "--profile",
                str(profile_path),
                "--output-dir",
                str(output_dir),
                "--ensure-endpoints",
            ],
        )

    assert fake_service.pause_idle_calls == 0
    assert fake_service.ensure_up_calls == []
