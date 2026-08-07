# Copyright (C) 2026 Chris Malek.
"""Tests for CLI commands with low coverage."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

from wordwending.cli.cli import cli
from wordwending.models import (
    DocumentBundle,
    EvaluationCohortReport,
    PageOverlay,
    PreparationResult,
    ReviewTaskType,
)
from wordwending.models.runner_execution import RunnerThroughputSummary
from wordwending.services.bundle_layout import BundleLayoutService
from wordwending.services.review_overlay import ReviewOverlayService
from wordwending.settings import Settings


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
        monkeypatch.setenv("WORDWENDING_HUGGINGFACE_API_KEY", secret)
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

    def test_prepare_command_writes_reproducible_metadata(
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
        binary_recipe.write_text(json.dumps(binary_payload, indent=2), encoding="utf-8")

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
        binary_recipe.write_text(json.dumps(binary_payload, indent=2), encoding="utf-8")

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

    def test_prepare_rejects_overrides_with_global_mode(self, runner, tmp_path) -> None:
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


def _runner_reference_json(*, runner_id: str = "olmocr") -> str:
    model_names = {
        "olmocr": "allenai/olmOCR",
        "kraken": "mittagessen/kraken",
    }
    return json.dumps(
        {
            "runner_id": runner_id,
            "runner_version": "0.4.27",
            "model_name": model_names.get(runner_id, f"example/{runner_id}"),
            "model_revision": "model-revision",
            "hardware_class": "nvidia-l40s",
            "runtime_name": "huggingface-endpoint",
            "runtime_revision": "container-digest",
            "config_digest": "sha256:runner-config",
            "prompt_digest": "sha256:prompt",
        }
    )


def _run_cli_args(tmp_path: Path, *, runner_id: str = "olmocr") -> list[str]:
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
    runner_ref.write_text(_runner_reference_json(runner_id=runner_id), encoding="utf-8")
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
        with patch("wordwending.cli.cli.Settings") as mock_settings:
            mock_settings.return_value = Settings()
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code != 0
        assert "huggingface_api_key" in result.output

    def test_run_rejects_missing_endpoint_mapping(self, runner, tmp_path) -> None:
        with patch("wordwending.cli.cli.Settings") as mock_settings:
            mock_settings.return_value = Settings(huggingface_api_key="hf_test_token")
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code != 0
        assert "missing Hugging Face endpoint" in result.output

    @patch("wordwending.cli.cli.RunnerExecutionService.run")
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
        with patch("wordwending.cli.cli.Settings", return_value=configured):
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code == 0
        assert "batches: 0" in result.output
        assert "failed_items: 0" in result.output
        assert "items_per_second: 2.0000" in result.output
        assert "hf_test_token" not in result.output

    @patch("wordwending.cli.cli.RunnerExecutionService.run")
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
        with patch("wordwending.cli.cli.Settings", return_value=configured):
            result = runner.invoke(cli, _run_cli_args(tmp_path))

        assert result.exit_code != 0
        assert "failed_items: 1" in result.output
        assert "failed item" in result.output.lower()

    @patch("wordwending.cli.cli.RunnerExecutionService.run")
    @patch("wordwending.cli.cli.HuggingFaceKrakenRunner")
    def test_run_selects_kraken_runner_by_runner_id(
        self,
        mock_kraken_cls,
        mock_run,
        runner,
        tmp_path,
    ) -> None:
        mock_run.return_value = (
            [],
            RunnerThroughputSummary(
                measured_item_count=0,
                failed_item_count=0,
                measured_duration_seconds=0.0,
                items_per_second=0.0,
            ),
        )
        mock_kraken_cls.return_value = mock_kraken_cls
        configured = Settings(
            huggingface_api_key="hf_test_token",
            huggingface_model_endpoints={
                "olmocr-production": "https://example.endpoints.huggingface.cloud/v1",
            },
        )
        with patch("wordwending.cli.cli.Settings", return_value=configured):
            result = runner.invoke(
                cli,
                _run_cli_args(tmp_path, runner_id="kraken"),
            )

        assert result.exit_code == 0
        mock_kraken_cls.assert_called_once()
        assert mock_kraken_cls.call_args.kwargs["runner"].runner_id == "kraken"

    @patch("wordwending.cli.cli.RunnerExecutionService.run")
    @patch("wordwending.cli.cli.HuggingFaceOlmocrRunner")
    def test_run_selects_olmocr_runner_by_runner_id(
        self,
        mock_olmocr_cls,
        mock_run,
        runner,
        tmp_path,
    ) -> None:
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
        configured = Settings(
            huggingface_api_key="hf_test_token",
            huggingface_model_endpoints={
                "olmocr-production": "https://example.endpoints.huggingface.cloud/v1",
            },
        )
        with patch("wordwending.cli.cli.Settings", return_value=configured):
            result = runner.invoke(cli, _run_cli_args(tmp_path, runner_id="olmocr"))

        assert result.exit_code == 0
        mock_olmocr_cls.assert_called_once()
        assert mock_olmocr_cls.call_args.kwargs["runner"].runner_id == "olmocr"

    def test_run_rejects_unsupported_runner_id(self, runner, tmp_path) -> None:
        configured = Settings(
            huggingface_api_key="hf_test_token",
            huggingface_model_endpoints={
                "olmocr-production": "https://example.endpoints.huggingface.cloud/v1",
            },
        )
        with patch("wordwending.cli.cli.Settings", return_value=configured):
            result = runner.invoke(
                cli,
                _run_cli_args(tmp_path, runner_id="unknown-engine"),
            )

        assert result.exit_code != 0
        assert "unsupported runner_id" in result.output


class TestCLIExport:
    """Test the export command."""

    def test_export_writes_document_markdown(self, runner, tmp_path: Path) -> None:
        """Export writes Spec 0006 derived artifacts under exports/."""
        fixture = Path("tests/fixtures/export_models/document-bundle-v1.json")
        bundle_json = tmp_path / "document-bundle.json"
        bundle_json.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
        root = tmp_path / "bundle-root"
        root.mkdir()

        result = runner.invoke(
            cli,
            ["export", str(bundle_json), "--bundle-root", str(root)],
        )

        assert result.exit_code == 0
        assert (root / "exports" / "document.md").exists()
        assert (root / "exports" / "bundle.json").exists()
        assert (root / "exports" / "rag.jsonl").exists()
        assert (root / "exports" / "stitched_chunks.jsonl").exists()

    def test_export_rejects_invalid_bundle_json(self, runner, tmp_path: Path) -> None:
        """Export aborts when DocumentBundle JSON fails validation."""
        bundle_json = tmp_path / "invalid-bundle.json"
        bundle_json.write_text("{not valid json", encoding="utf-8")
        root = tmp_path / "bundle-root"
        root.mkdir()

        result = runner.invoke(
            cli,
            ["export", str(bundle_json), "--bundle-root", str(root)],
        )

        assert result.exit_code != 0
        output = result.output.lower()
        assert "validation error" in output or "invalid json" in output
        assert "no such command" not in output
        assert not (root / "exports").exists()

    def test_export_requires_bundle_root(self, runner, tmp_path: Path) -> None:
        """Export requires --bundle-root."""
        fixture = Path("tests/fixtures/export_models/document-bundle-v1.json")
        bundle_json = tmp_path / "document-bundle.json"
        bundle_json.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

        result = runner.invoke(cli, ["export", str(bundle_json)])

        assert result.exit_code == 2
        output = result.output.lower()
        assert "bundle-root" in output
        assert "missing option" in output
        assert "no such command" not in output


class TestCLIAssemble:
    """Test assemble and inspect-bundle commands."""

    _WITNESS_FIXTURE = Path("tests/fixtures/assemble/olmocr-chat-completion-v1.json")
    _KRAKEN_FIXTURE = Path("tests/fixtures/assemble/kraken-chat-completion-v1.json")
    _MANIFEST_FIXTURE = Path("tests/fixtures/assemble/manifest-v1.json")
    _MULTI_WITNESS_MANIFEST = Path(
        "tests/fixtures/assemble/manifest-multi-witness-v1.json"
    )

    def _stage_bundle_inputs(self, bundle_root: Path) -> None:
        """Copy witness fixture and prepared image under bundle_root."""
        witnesses_dir = bundle_root / "raw" / "witnesses"
        witnesses_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(
            self._WITNESS_FIXTURE, witnesses_dir / "olmocr-chat-completion-v1.json"
        )

        image_dir = bundle_root / "prepared"
        image_dir.mkdir(parents=True, exist_ok=True)
        (image_dir / "page.png").write_bytes(b"fake-png-bytes")

    def _stage_multi_witness_bundle_inputs(self, bundle_root: Path) -> None:
        """Copy olmOCR + kraken fixtures and prepared image under bundle_root."""
        self._stage_bundle_inputs(bundle_root)
        witnesses_dir = bundle_root / "raw" / "witnesses"
        shutil.copy(
            self._KRAKEN_FIXTURE, witnesses_dir / "kraken-chat-completion-v1.json"
        )

    def test_assemble_writes_bundle_tree(self, runner, tmp_path: Path) -> None:
        """Assemble materializes Spec 0002 bundle tree from manifest."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_bundle_inputs(bundle_root)

        result = runner.invoke(
            cli,
            [
                "assemble",
                "--bundle-root",
                str(bundle_root),
                "--manifest",
                str(self._MANIFEST_FIXTURE),
            ],
        )

        assert result.exit_code == 0
        assert (bundle_root / "manifest.json").exists()
        assert (bundle_root / "document-bundle.json").exists()
        assert (
            bundle_root / "pages" / "page-0001" / "graph" / "page_graph.json"
        ).exists()
        assert "doc-src-1" in result.output
        assert "pages: 1" in result.output
        assert (
            f"document_bundle: {bundle_root / 'document-bundle.json'}" in result.output
        )

    def test_assemble_then_export_writes_document_markdown(
        self, runner, tmp_path: Path
    ) -> None:
        """Assemble followed by export produces exports/document.md."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_bundle_inputs(bundle_root)

        assemble_result = runner.invoke(
            cli,
            [
                "assemble",
                "--bundle-root",
                str(bundle_root),
                "--manifest",
                str(self._MANIFEST_FIXTURE),
            ],
        )
        assert assemble_result.exit_code == 0

        bundle_json = bundle_root / "document-bundle.json"
        assert bundle_json.exists()
        export_result = runner.invoke(
            cli,
            ["export", str(bundle_json), "--bundle-root", str(bundle_root)],
        )

        assert export_result.exit_code == 0
        assert (bundle_root / "exports" / "document.md").exists()

    def test_inspect_bundle_shows_page_info(self, runner, tmp_path: Path) -> None:
        """inspect-bundle prints document and page summary."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_bundle_inputs(bundle_root)
        assemble_result = runner.invoke(
            cli,
            [
                "assemble",
                "--bundle-root",
                str(bundle_root),
                "--manifest",
                str(self._MANIFEST_FIXTURE),
            ],
        )
        assert assemble_result.exit_code == 0

        result = runner.invoke(
            cli,
            ["inspect-bundle", "--bundle-root", str(bundle_root)],
        )

        assert result.exit_code == 0
        assert "doc-src-1" in result.output
        assert "page-0001" in result.output
        assert "page_number: 1" in result.output
        assert "olmocr" in result.output

    def test_inspect_bundle_surfaces_multi_witness_merge_flags(
        self, runner, tmp_path: Path
    ) -> None:
        """inspect-bundle prints merge flags after multi-witness disagreement."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_multi_witness_bundle_inputs(bundle_root)
        assemble_result = runner.invoke(
            cli,
            [
                "assemble",
                "--bundle-root",
                str(bundle_root),
                "--manifest",
                str(self._MULTI_WITNESS_MANIFEST),
            ],
        )
        assert assemble_result.exit_code == 0

        result = runner.invoke(
            cli,
            ["inspect-bundle", "--bundle-root", str(bundle_root)],
        )

        assert result.exit_code == 0
        assert "wit-olmocr" in result.output
        assert "wit-kraken" in result.output
        assert "text_disagreement" in result.output
        assert "flag:" in result.output

    def test_assemble_fails_when_witness_artifacts_missing(
        self, runner, tmp_path: Path
    ) -> None:
        """Assemble fails when manifest witness paths are absent under bundle_root."""
        bundle_root = tmp_path / "empty-bundle"
        result = runner.invoke(
            cli,
            [
                "assemble",
                "--bundle-root",
                str(bundle_root),
                "--manifest",
                str(self._MANIFEST_FIXTURE),
            ],
        )
        assert result.exit_code != 0
        assert "olmocr-chat-completion-v1.json" in result.output
        assert "no such file" in result.output.lower()

    def test_assemble_rejects_invalid_manifest(self, runner, tmp_path: Path) -> None:
        """Assemble fails when manifest JSON is invalid."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        bad_manifest = tmp_path / "bad-manifest.json"
        bad_manifest.write_text("{not valid", encoding="utf-8")

        result = runner.invoke(
            cli,
            [
                "assemble",
                "--bundle-root",
                str(bundle_root),
                "--manifest",
                str(bad_manifest),
            ],
        )
        assert result.exit_code != 0

    def test_inspect_bundle_rejects_missing_root(self, runner, tmp_path: Path) -> None:
        """inspect-bundle fails when bundle root is missing."""
        missing_root = tmp_path / "missing"
        result = runner.invoke(
            cli,
            ["inspect-bundle", "--bundle-root", str(missing_root)],
        )
        assert result.exit_code != 0


class TestCLIReview:
    """Test review apply and materialize commands."""

    _OVERLAY_FIXTURE = Path("tests/fixtures/review_overlay/page-overlay-v1.json")
    _MINIMAL_BUNDLE_FIXTURE = Path(
        "tests/fixtures/bundle_layout/minimal_document.json"
    )

    def _stage_minimal_bundle(self, bundle_root: Path, tmp_path: Path) -> None:
        """Write a minimal Spec 0002 bundle tree under ``bundle_root``."""
        inputs = tmp_path / "inputs"
        inputs.mkdir(parents=True, exist_ok=True)
        source_pdf = inputs / "sample.pdf"
        source_pdf.write_bytes(b"%PDF-1.4 minimal")
        source_page = inputs / "page1.jp2"
        source_page.write_bytes(b"fake-jp2-bytes")
        prepared_image = inputs / "prepared.jp2"
        prepared_image.write_bytes(b"fake-prepared-bytes")
        witness_src = inputs / "olmocr-response.json"
        witness_src.write_text('{"text": "hello"}', encoding="utf-8")

        bundle = json.loads(
            self._MINIMAL_BUNDLE_FIXTURE.read_text(encoding="utf-8")
        )
        service = BundleLayoutService()
        service.write_document_bundle(
            DocumentBundle.model_validate(bundle),
            bundle_root,
            source_files={"sample.pdf": source_pdf},
            source_page_images={1: source_page},
            page_images={"page-0001": prepared_image},
            witness_files={"wit-1": witness_src},
        )

    def test_review_apply_appends_events_and_writes_state(
        self, runner, tmp_path: Path
    ) -> None:
        """Apply appends overlay events and materializes current_state.json."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_minimal_bundle(bundle_root, tmp_path)
        overlay = PageOverlay.model_validate_json(
            self._OVERLAY_FIXTURE.read_text(encoding="utf-8")
        )

        result = runner.invoke(
            cli,
            [
                "review",
                "apply",
                "--bundle-root",
                str(bundle_root),
                "--overlay",
                str(self._OVERLAY_FIXTURE),
                "--page-id",
                "page-0001",
            ],
        )

        assert result.exit_code == 0, result.output
        review_path = (
            bundle_root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
        )
        state_path = (
            bundle_root / "pages" / "page-0001" / "overlays" / "current_state.json"
        )
        assert review_path.exists()
        assert state_path.exists()
        assert f"events_appended: {len(overlay.review_events)}" in result.output
        replayed = ReviewOverlayService().materialize(overlay)
        written = json.loads(state_path.read_text(encoding="utf-8"))
        assert written == [state.model_dump(mode="json") for state in replayed]

    def test_review_apply_is_append_only(self, runner, tmp_path: Path) -> None:
        """Re-applying the same overlay must not rewrite prior JSONL bytes."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_minimal_bundle(bundle_root, tmp_path)
        args = [
            "review",
            "apply",
            "--bundle-root",
            str(bundle_root),
            "--overlay",
            str(self._OVERLAY_FIXTURE),
            "--page-id",
            "page-0001",
        ]
        first = runner.invoke(cli, args)
        assert first.exit_code == 0, first.output
        review_path = (
            bundle_root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
        )
        bytes_after_first = review_path.read_bytes()

        second = runner.invoke(cli, args)
        assert second.exit_code == 0, second.output
        assert "events_appended: 0" in second.output
        assert review_path.read_bytes() == bytes_after_first

    def test_review_materialize_recomputes_state(self, runner, tmp_path: Path) -> None:
        """Materialize replays JSONL history into current_state.json."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_minimal_bundle(bundle_root, tmp_path)
        apply_result = runner.invoke(
            cli,
            [
                "review",
                "apply",
                "--bundle-root",
                str(bundle_root),
                "--overlay",
                str(self._OVERLAY_FIXTURE),
                "--page-id",
                "page-0001",
            ],
        )
        assert apply_result.exit_code == 0, apply_result.output
        state_path = (
            bundle_root / "pages" / "page-0001" / "overlays" / "current_state.json"
        )
        state_path.unlink()

        result = runner.invoke(
            cli,
            [
                "review",
                "materialize",
                "--bundle-root",
                str(bundle_root),
                "--page-id",
                "page-0001",
            ],
        )

        assert result.exit_code == 0, result.output
        overlay = PageOverlay.model_validate_json(
            self._OVERLAY_FIXTURE.read_text(encoding="utf-8")
        )
        replayed = ReviewOverlayService().materialize(overlay)
        written = json.loads(state_path.read_text(encoding="utf-8"))
        assert written == [state.model_dump(mode="json") for state in replayed]
        assert "states:" in result.output

    def test_review_apply_rejects_page_id_mismatch(
        self, runner, tmp_path: Path
    ) -> None:
        """Apply fails when --page-id does not match the overlay file."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_minimal_bundle(bundle_root, tmp_path)

        result = runner.invoke(
            cli,
            [
                "review",
                "apply",
                "--bundle-root",
                str(bundle_root),
                "--overlay",
                str(self._OVERLAY_FIXTURE),
                "--page-id",
                "page-9999",
            ],
        )

        assert result.exit_code != 0
        assert "does not match" in result.output

    def test_review_apply_rejects_unknown_task_object_ids(
        self, runner, tmp_path: Path
    ) -> None:
        """Apply fails when overlay tasks reference ids absent from the page."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_minimal_bundle(bundle_root, tmp_path)
        overlay = PageOverlay.model_validate_json(
            self._OVERLAY_FIXTURE.read_text(encoding="utf-8")
        )
        text_task = next(
            task
            for task in overlay.review_tasks
            if task.task_type == ReviewTaskType.TEXT
        )
        bad_task = text_task.model_copy(
            update={"target_object_ids": ["span-does-not-exist"]}
        )
        # Drop events so PageOverlay binding checks do not fire first; the
        # apply path must still reject unknown task targets against the page.
        bad_overlay = overlay.model_copy(
            update={
                "review_tasks": [bad_task],
                "review_events": [],
                "current_state": [],
            }
        )
        overlay_path = tmp_path / "bad-overlay.json"
        overlay_path.write_text(
            bad_overlay.model_dump_json(),
            encoding="utf-8",
        )

        result = runner.invoke(
            cli,
            [
                "review",
                "apply",
                "--bundle-root",
                str(bundle_root),
                "--overlay",
                str(overlay_path),
                "--page-id",
                "page-0001",
            ],
        )

        assert result.exit_code != 0
        assert "unknown" in result.output

    def test_review_materialize_rejects_unknown_page_id(
        self, runner, tmp_path: Path
    ) -> None:
        """Materialize fails when the bundle has no matching page id."""
        bundle_root = tmp_path / "bundle"
        bundle_root.mkdir()
        self._stage_minimal_bundle(bundle_root, tmp_path)

        result = runner.invoke(
            cli,
            [
                "review",
                "materialize",
                "--bundle-root",
                str(bundle_root),
                "--page-id",
                "page-9999",
            ],
        )

        assert result.exit_code != 0
        assert "page-9999" in result.output


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
