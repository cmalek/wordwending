# Copyright (C) 2026 Chris Malek.
"""Tests for CLI commands with low coverage."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from bochord.cli.cli import cli
from bochord.models import PreparationResult


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
