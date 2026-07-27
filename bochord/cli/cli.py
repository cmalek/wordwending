# Copyright (C) 2026 Chris Malek.
"""bochord command-line interface."""

from __future__ import annotations

import json
import os
import sys
from importlib.metadata import Distribution
from pathlib import Path

import click
from pydantic import ValidationError
from rich.table import Table

import bochord

from ..models import (
    BundlePage,
    GoldDocument,
    MetricProfile,
    PageClass,
    PreparationMode,
    PreparationRecipe,
)
from ..services.evaluation import EvaluationService
from ..services.preparation import (
    PageClassifier,
    PagePreparationService,
    PageQualityAssessor,
    PreparationBundleService,
)
from ..services.source_acquisition import SourceAcquisitionService
from ..settings import Settings
from .utils import console, print_error, print_info


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress all output except errors")
@click.option(
    "--config-file", type=click.Path(exists=True), help="Custom configuration file path"
)
@click.option(
    "--output",
    type=click.Choice(["json", "table", "text"]),
    default="table",
    help="Output format",
)
@click.pass_context
def cli(
    ctx: click.Context, verbose: bool, quiet: bool, config_file: str | None, output: str
):
    """
    bochord command line interface.

    Args:
        ctx: Click context object.
        verbose: Enable verbose output.
        quiet: Suppress all output except errors.
        config_file: Optional custom configuration file path.
        output: Selected output format for subcommands.

    """  # noqa: D403
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Store global options in context
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["output"] = output
    ctx.obj["config_file"] = config_file

    if config_file:
        # Picked up by Settings.settings_customise_sources.
        os.environ["BOCHORD_CONFIG_FILE"] = config_file

    # Load settings
    try:
        settings = Settings()
        ctx.obj["settings"] = settings
    except Exception as e:  # noqa: BLE001
        print_error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Configure console based on quiet mode
    if quiet:
        console.quiet = True


@cli.command(name="version", help="Print some version info.")
def version() -> None:
    """
    Print the some version info of this package,
    """
    table = Table(title="bochord Version Info")
    table.add_column("Package", justify="left", style="cyan", no_wrap=True)
    table.add_column("Version", justify="left", style="yellow", no_wrap=True)

    table.add_row("bochord", str(bochord.__version__))
    table.add_row("click", str(Distribution.from_name("click").version))
    table.add_row("rich", str(Distribution.from_name("rich").version))
    table.add_row("pydantic", str(Distribution.from_name("pydantic").version))

    console.print(table)


@cli.command("settings")
@click.pass_context
def show_settings(ctx: click.Context):
    """
    Settings-related commands.

    Args:
        ctx: Click context object.

    """
    output_format = ctx.obj.get("output", "table")
    verbose = ctx.obj.get("verbose", False)
    settings = ctx.obj.get("settings")

    if output_format == "json":
        click.echo(json.dumps(settings.model_dump()))
    elif output_format == "table":
        table = Table(
            title="Settings", show_header=True, header_style="bold magenta"
        )
        table.add_column("Setting Name", style="cyan")
        table.add_column("Value", style="green")

        for setting_name, setting_value in settings.model_dump().items():
            table.add_row(setting_name, str(setting_value))

        console.print(table)
    else:  # text format
        for setting_name, setting_value in settings.model_dump().items():
            click.echo(f"{setting_name}: {setting_value}")
            click.echo()

    if verbose:
        print_info(f"Found {len(settings.model_dump())} settings")


@cli.command("eval")
@click.option(
    "--prediction",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Predicted BundlePage JSON file.",
)
@click.option(
    "--gold",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="GoldDocument JSON file.",
)
@click.option(
    "--profile",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="MetricProfile JSON file.",
)
@click.option(
    "--output-json",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Destination path for PageEvaluationSummary JSON.",
)
def eval_page(
    prediction: Path,
    gold: Path,
    profile: Path,
    output_json: Path,
) -> None:
    """
    Score one predicted page against gold annotations.

    Args:
        prediction: Predicted BundlePage JSON file path.
        gold: GoldDocument JSON file path.
        profile: MetricProfile JSON file path.
        output_json: Destination path for PageEvaluationSummary JSON.

    Returns:
        Writes JSON with three top-level families: ``text``, ``structure``,
        and ``style`` (typography and note linkage nested under ``style``).

    Side Effects:
        Writes evaluation summary JSON to ``output_json``.

    Raises:
        click.ClickException: When inputs fail validation or I/O fails.

    """
    try:
        page = BundlePage.model_validate_json(prediction.read_text(encoding="utf-8"))
        gold_document = GoldDocument.model_validate_json(
            gold.read_text(encoding="utf-8")
        )
        metric_profile = MetricProfile.model_validate_json(
            profile.read_text(encoding="utf-8")
        )
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    gold_page = next(
        (item for item in gold_document.pages if item.page_id == page.page_id),
        None,
    )
    if gold_page is None:
        msg = f"gold document has no page matching page_id {page.page_id!r}"
        raise click.ClickException(msg)

    summary = EvaluationService().evaluate_page(page, gold_page, metric_profile)

    try:
        output_json.write_text(summary.model_dump_json(indent=2), encoding="utf-8")
    except OSError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command("prepare")
@click.argument(
    "source",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--recipe",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="PreparationRecipe JSON file.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Destination directory for acquired and prepared pages.",
)
@click.option(
    "--mode",
    type=click.Choice([mode.value for mode in PreparationMode]),
    default=None,
    help="Operator override for preparation subdivision mode.",
)
@click.option(
    "--page-class",
    type=click.Choice([page_class.value for page_class in PageClass]),
    default=None,
    help="Operator override for page-class cohort.",
)
@click.option(
    "--override-reason",
    default=None,
    help="Required reason when --mode or --page-class is set.",
)
def prepare_pages(  # noqa: PLR0913, PLR0917
    source: Path,
    recipe: Path,
    output_dir: Path,
    mode: str | None,
    page_class: str | None,
    override_reason: str | None,
) -> None:
    """
    Acquire and prepare source pages into a reproducible output bundle.

    Args:
        source: PDF, image, image folder, or ZIP of images.
        recipe: PreparationRecipe JSON file path.
        output_dir: Destination root for source and prepared artifacts.
        mode: Optional operator preparation-mode override.
        page_class: Optional operator page-class override.
        override_reason: Required reason when any override is set.

    Side Effects:
        Writes acquired pages under ``output_dir/source`` and prepared page
        artifacts plus ``preparation.json`` under ``output_dir/pages``.

    Raises:
        click.ClickException: When inputs fail validation or I/O fails.

    """
    try:
        preparation_recipe = _load_preparation_recipe(recipe)
        mode_override, page_class_override = _prepare_overrides(
            mode,
            page_class,
            override_reason,
        )
        results = PreparationBundleService(
            SourceAcquisitionService(),
            PagePreparationService(PageQualityAssessor(), PageClassifier()),
        ).prepare_bundle(
            source,
            preparation_recipe,
            output_dir,
            mode_override=mode_override,
            page_class_override=page_class_override,
            override_reason=override_reason,
        )
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    warning_count = sum(len(result.assessment.warnings) for result in results)
    click.echo(f"pages: {len(results)}")
    click.echo(f"warnings: {warning_count}")
    click.echo(f"output: {output_dir}")

def _load_preparation_recipe(recipe: Path) -> PreparationRecipe:
    """
    Load and validate a preparation recipe JSON file.

    Args:
        recipe: PreparationRecipe JSON file path.

    Returns:
        Validated preparation recipe model.

    """
    return PreparationRecipe.model_validate_json(recipe.read_text(encoding="utf-8"))


def _prepare_overrides(
    mode: str | None,
    page_class: str | None,
    override_reason: str | None,
) -> tuple[PreparationMode | None, PageClass | None]:
    """
    Validate and convert optional CLI override values.

    Args:
        mode: Optional preparation-mode override from Click.
        page_class: Optional page-class override from Click.
        override_reason: Required reason when any override is set.

    Returns:
        Parsed preparation-mode and page-class overrides.

    Raises:
        ValueError: If an override is supplied without a non-empty reason.

    """
    if (mode is not None or page_class is not None) and not (
        override_reason and override_reason.strip()
    ):
        msg = "--override-reason is required when --mode or --page-class is set"
        raise ValueError(msg)
    mode_override = PreparationMode(mode) if mode is not None else None
    page_class_override = PageClass(page_class) if page_class is not None else None
    return mode_override, page_class_override
