# Copyright (C) 2026 Chris Malek.
"""Tests for CLI commands with low coverage."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

from bochord.cli.cli import cli
from bochord.models import EvaluationCohortReport, PreparationResult
from bochord.models.runner_execution import RunnerThroughputSummary
from bochord.settings import Settings


def _dense_two_column_image() -> Image.Image:
    width, height = 1000, 1400
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    text_height = 12
    left_x0, left_x1 = 60, 440
    right_x0, right_x1 = 560, 940
    y = 80
    while y + text_height < height - 80:
        draw.rectangle((left_x0, y, left_x1, y + text_height - 1), fill=(20, 20, 20))
        draw.rectangle((right_x0, y, right_x1, y + text_height - 1), fill=(20, 20, 20))
        y += text_height + 10
    return image


class TestCLIVersion:
    """Test the version command."""

    def test_version_command(self, runner):
        """Test the version command displays version information."""
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        # The command should run successfully without errors
        # Rich console output may not be captured in test environment

    def test_version_command_with_verbose(self, runner):
        """Test the version command with verbose flag."""
        result = runner.invoke(cli, ["--verbose", "version"])
        assert result.exit_code == 0

    def test_version_command_with_quiet(self, runner):
        """Test the version command with quiet flag."""
        result = runner.invoke(cli, ["--quiet", "version"])
        assert result.exit_code == 0


class TestCLISettings:
    """Test the settings command."""

    def test_settings_command_table_output(self, runner):
        """Test the settings command with table output."""
        result = runner.invoke(cli, ["settings"])
        assert result.exit_code == 0

    def test_settings_command_json_output(self, runner):
        """Test the settings command with JSON output."""
        result = runner.invoke(cli, ["--output", "json", "settings"])
        assert result.exit_code == 0
        # Should be valid JSON
        data = json.loads(result.output)
        assert isinstance(data, dict)

    def test_settings_command_text_output(self, runner):
        """Test the settings command with text output."""
        result = runner.invoke(cli, ["--output", "text", "settings"])
        assert result.exit_code == 0

    def test_settings_command_with_verbose(self, runner):
        """Test the settings command with verbose flag."""
        result = runner.invoke(cli, ["--verbose", "settings"])
        assert result.exit_code == 0

    def test_settings_command_with_config_file(self, runner, temp_dir):
        """Test the settings command with custom config file."""
        config_file = temp_dir / "test_config.toml"
        config_file.write_text('default_output_format = "json"', encoding="utf-8")

        result = runner.invoke(cli, ["--config-file", str(config_file), "settings"])
        assert result.exit_code == 0

    def test_settings_command_redacts_huggingface_api_key(self, runner, monkeypatch):
        """Settings output must not expose the raw Hugging Face token."""
        secret = "hf_secret_token_xyz"
        monkeypatch.setenv("BOCHORD_HUGGINGFACE_API_KEY", secret)
        for output_format in ("json", "text", "table"):
            result = runner.invoke(cli, ["--output", output_format, "settings"])
            assert result.exit_code == 0
            assert secret not in result.output
        data = json.loads(runner.invoke(cli, ["--output", "json", "settings"]).output)
        assert data["huggingface_api_key"] == "**********"


class TestCLIGlobalOptions:
    """Test global CLI options."""

    def test_verbose_flag(self, runner):
        """Test verbose flag is properly set."""
        result = runner.invoke(cli, ["--verbose", "version"])
        assert result.exit_code == 0

    def test_quiet_flag(self, runner):
        """Test quiet flag is properly set."""
        result = runner.invoke(cli, ["--quiet", "version"])
        assert result.exit_code == 0

    def test_output_format_default(self, runner):
        """Test default output format is table."""
        result = runner.invoke(cli, ["settings"])
        assert result.exit_code == 0

    def test_output_format_json(self, runner):
        """Test JSON output format."""
        result = runner.invoke(cli, ["--output", "json", "settings"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, dict)

    def test_output_format_text(self, runner):
        """Test text output format."""
        result = runner.invoke(cli, ["--output", "text", "settings"])
        assert result.exit_code == 0

    def test_invalid_output_format(self, runner):
        """Test invalid output format."""
        result = runner.invoke(cli, ["--output", "invalid", "settings"])
        assert result.exit_code != 0


class TestCLIEval:
    """Test the eval command."""

    def test_eval_command_writes_reproducible_scores(self, runner, tmp_path) -> None:
        """Test eval writes deterministic PageEvaluationSummary JSON."""
        output = tmp_path / "scores.json"
        result = runner.invoke(
            cli,
            [
                "eval",
                "--prediction",
                "tests/fixtures/evaluation/page.json",
                "--gold",
                "tests/fixtures/evaluation/gold.json",
                "--profile",
                "tests/fixtures/evaluation/metric-profile-v1.json",
                "--output-json",
                str(output),
            ],
        )
        assert result.exit_code == 0
        payload = json.loads(output.read_text(encoding="utf-8"))
        assert set(payload) == {"text", "structure", "style"}
        assert "watchlist_exact_match_rate" in {
            item["metric_id"] for item in payload["text"]["metrics"]
        }


class TestCLIPrepare:
    """Test the prepare command."""

    def test_prepare_command_writes_reproducible_metadata(self, runner, tmp_path) -> None:
        source = tmp_path / "page.png"
        Image.new("L", (600, 800), "white").save(source)
        output = tmp_path / "bundle"

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                "tests/fixtures/preparation/recipe-v1.json",
                "--output-dir",
                str(output),
            ],
        )

        assert result.exit_code == 0
        preparation_files = list(
            (output / "pages/page-0001/prepared").glob("*/preparation.json")
        )
        assert len(preparation_files) == 1
        payload = json.loads(preparation_files[0].read_text(encoding="utf-8"))
        assert PreparationResult.model_validate(payload)
        source_path = payload["source_page"]["source_path"]
        assert not Path(source_path).is_absolute()
        assert source_path == "source/pages/1.png"

    def test_prepare_command_preserves_competing_variants(
        self, runner, tmp_path
    ) -> None:
        source = tmp_path / "page.png"
        Image.new("L", (600, 800), "white").save(source)
        output = tmp_path / "bundle"
        gray_recipe = tmp_path / "gray.json"
        binary_recipe = tmp_path / "binary.json"
        gray_payload = json.loads(
            Path("tests/fixtures/preparation/recipe-v1.json").read_text(
                encoding="utf-8"
            )
        )
        gray_payload["recipe_id"] = "gray"
        binary_payload = {
            **gray_payload,
            "recipe_id": "binary",
            "color_mode": "binary",
            "binarize_mode": "otsu",
        }
        gray_recipe.write_text(json.dumps(gray_payload, indent=2), encoding="utf-8")
        binary_recipe.write_text(
            json.dumps(binary_payload, indent=2), encoding="utf-8"
        )

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                str(gray_recipe),
                "--recipe",
                str(binary_recipe),
                "--output-dir",
                str(output),
            ],
        )

        assert result.exit_code == 0
        assert "variants: 2" in result.output
        assert len(list((output / "recipes").glob("*.json"))) == 2
        assert len(list((output / "pages/page-0001/prepared").iterdir())) == 2

    def test_prepare_rejects_global_overrides_with_multiple_recipes(
        self, runner, tmp_path
    ) -> None:
        source = tmp_path / "page.png"
        Image.new("L", (600, 800), "white").save(source)
        output = tmp_path / "bundle"
        gray_recipe = tmp_path / "gray.json"
        binary_recipe = tmp_path / "binary.json"
        gray_payload = json.loads(
            Path("tests/fixtures/preparation/recipe-v1.json").read_text(
                encoding="utf-8"
            )
        )
        gray_payload["recipe_id"] = "gray"
        binary_payload = {
            **gray_payload,
            "recipe_id": "binary",
            "color_mode": "binary",
            "binarize_mode": "otsu",
        }
        gray_recipe.write_text(json.dumps(gray_payload, indent=2), encoding="utf-8")
        binary_recipe.write_text(
            json.dumps(binary_payload, indent=2), encoding="utf-8"
        )

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                str(gray_recipe),
                "--recipe",
                str(binary_recipe),
                "--output-dir",
                str(output),
                "--mode",
                "full-page",
                "--override-reason",
                "force full page",
            ],
        )

        assert result.exit_code != 0
        assert "multiple --recipe" in result.output.lower()
        if output.exists():
            assert not (output / "pages").exists()
            assert not (output / "source").exists()

    def test_prepare_rejects_mode_override_without_reason(
        self, runner, tmp_path
    ) -> None:
        """Test prepare aborts before writes when override lacks a reason."""
        source = tmp_path / "page.png"
        Image.new("L", (600, 800), "white").save(source)
        output = tmp_path / "bundle"

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                "tests/fixtures/preparation/recipe-v1.json",
                "--output-dir",
                str(output),
                "--mode",
                "full-page",
            ],
        )

        assert result.exit_code != 0
        assert "override-reason" in result.output.lower()
        if output.exists():
            assert not (output / "pages").exists()
            assert not (output / "source").exists()

    def test_prepare_accepts_page_overrides_manifest(self, runner, tmp_path) -> None:
        source = tmp_path / "pages"
        source.mkdir()
        Image.new("L", (600, 800), "white").save(source / "page-1.png")
        _dense_two_column_image().save(source / "page-2.png")
        output = tmp_path / "bundle"

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                "tests/fixtures/preparation/recipe-v1.json",
                "--output-dir",
                str(output),
                "--overrides",
                "tests/fixtures/preparation/page-overrides.json",
            ],
        )

        assert result.exit_code == 0
        first_path = next(
            (output / "pages/page-0001/prepared").glob("*/preparation.json")
        )
        second_path = next(
            (output / "pages/page-0002/prepared").glob("*/preparation.json")
        )
        first = json.loads(first_path.read_text(encoding="utf-8"))
        second = json.loads(second_path.read_text(encoding="utf-8"))
        assert first["preparation_choice_source"] == "auto"
        assert second["preparation_choice_source"] == "operator"
        assert second["assessment"]["page_class_source"] == "operator"

    def test_prepare_rejects_overrides_with_global_mode(
        self, runner, tmp_path
    ) -> None:
        source = tmp_path / "page.png"
        Image.new("L", (600, 800), "white").save(source)
        output = tmp_path / "bundle"

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                "tests/fixtures/preparation/recipe-v1.json",
                "--output-dir",
                str(output),
                "--overrides",
                "tests/fixtures/preparation/page-overrides.json",
                "--mode",
                "full-page",
                "--override-reason",
                "conflicting global override",
            ],
        )

        assert result.exit_code != 0
        assert "override" in result.output.lower()
        if output.exists():
            assert not (output / "pages").exists()
            assert not (output / "source").exists()

    def test_prepare_rejects_invalid_overrides_before_acquisition(
        self, runner, tmp_path
    ) -> None:
        source = tmp_path / "page.png"
        Image.new("L", (600, 800), "white").save(source)
        output = tmp_path / "bundle"
        overrides = tmp_path / "overrides.json"
        overrides.write_text(
            json.dumps(
                [
                    {
                        "source_page_id": "page-0001",
                        "reason": "missing choice",
                    }
                ]
            ),
            encoding="utf-8",
        )

        result = runner.invoke(
            cli,
            [
                "prepare",
                str(source),
                "--recipe",
                "tests/fixtures/preparation/recipe-v1.json",
                "--output-dir",
                str(output),
                "--overrides",
                str(overrides),
            ],
        )

        assert result.exit_code != 0
        if output.exists():
            assert not (output / "pages").exists()
            assert not (output / "source").exists()


def test_eval_cohorts_writes_all_fixed_views(runner, tmp_path: Path) -> None:
    output = tmp_path / "cohorts.json"
    result = runner.invoke(
        cli,
        [
            "eval-cohorts",
            "tests/fixtures/evaluation/cohort-records.json",
            "--output-json",
            str(output),
        ],
    )
    assert result.exit_code == 0
    report = EvaluationCohortReport.model_validate_json(output.read_text())
    assert report.by_page_class
    assert report.by_page_class_and_preparation_mode
    assert report.by_page_class_and_runner


def _runner_reference_json() -> str:
    return json.dumps(
        {
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
    )


def _run_cli_args(tmp_path: Path) -> list[str]:
    prepared = tmp_path / "prepared.json"
    prepared.write_text(
        Path("tests/fixtures/runner/prepared-inputs.json").read_text(),
        encoding="utf-8",
    )
    policy = tmp_path / "policy.json"
    policy.write_text(
        Path("tests/fixtures/runner/olmocr-policy-v1.json").read_text(),
        encoding="utf-8",
    )
    runner_ref = tmp_path / "runner.json"
    runner_ref.write_text(_runner_reference_json(), encoding="utf-8")
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    output = tmp_path / "output"
    return [
        "run",
        str(prepared),
        "--policy",
        str(policy),
        "--runner",
        str(runner_ref),
        "--bundle-root",
        str(bundle),
        "--output-dir",
        str(output),
        "--run-id",
        "run-1",
        "--document-id",
        "doc-1",
    ]


class TestCLIRun:
    """Test the run command."""

    def test_run_rejects_missing_huggingface_api_key(self, runner, tmp_path) -> None:
        with patch("bochord.cli.cli.Settings") as mock_settings:
            mock_settings.return_value = Settings()
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code != 0
        assert "huggingface_api_key" in result.output

    def test_run_rejects_missing_endpoint_mapping(self, runner, tmp_path) -> None:
        with patch("bochord.cli.cli.Settings") as mock_settings:
            mock_settings.return_value = Settings(huggingface_api_key="hf_test_token")
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code != 0
        assert "missing Hugging Face endpoint" in result.output

    @patch("bochord.cli.cli.RunnerExecutionService.run")
    def test_run_command_reports_summary(
        self,
        mock_run,
        runner,
        tmp_path,
    ) -> None:
        mock_run.return_value = (
            [],
            RunnerThroughputSummary(
                measured_item_count=2,
                failed_item_count=0,
                measured_duration_seconds=1.0,
                items_per_second=2.0,
            ),
        )
        configured = Settings(
            huggingface_api_key="hf_test_token",
            huggingface_model_endpoints={
                "olmocr-production": "https://example.endpoints.huggingface.cloud/v1",
            },
        )
        with patch("bochord.cli.cli.Settings", return_value=configured):
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code == 0
        assert "batches: 0" in result.output
        assert "failed_items: 0" in result.output
        assert "items_per_second: 2.0000" in result.output
        assert "hf_test_token" not in result.output

    @patch("bochord.cli.cli.RunnerExecutionService.run")
    def test_run_command_exits_nonzero_when_items_failed(
        self,
        mock_run,
        runner,
        tmp_path,
    ) -> None:
        mock_run.return_value = (
            [],
            RunnerThroughputSummary(
                measured_item_count=2,
                failed_item_count=1,
                measured_duration_seconds=1.0,
                items_per_second=2.0,
            ),
        )
        configured = Settings(
            huggingface_api_key="hf_test_token",
            huggingface_model_endpoints={
                "olmocr-production": "https://example.endpoints.huggingface.cloud/v1",
            },
        )
        with patch("bochord.cli.cli.Settings", return_value=configured):
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code != 0
        assert "failed_items: 1" in result.output
        assert "failed item" in result.output.lower()


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_cli_without_arguments(self, runner):
        """Test CLI without arguments shows help."""
        result = runner.invoke(cli, [])
        # Click expects a command, so exit code 2 is correct for missing command
        assert result.exit_code == 2
        assert "Usage:" in result.output

    def test_invalid_command(self, runner):
        """Test invalid command shows error."""
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.output
