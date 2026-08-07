# Copyright (C) 2026 Chris Malek.
"""wordwending command-line interface."""

from __future__ import annotations

import json
import os
import sys
from importlib.metadata import Distribution
from pathlib import Path

import click
import httpx
from pydantic import BaseModel, TypeAdapter, ValidationError
from rich.table import Table

import wordwending

from ..exc import ConfigurationError
from ..models import (
    BundlePage,
    DocumentBundle,
    GoldDocument,
    MetricProfile,
    PageClass,
    PageEvaluationRecord,
    PagePreparationOverride,
    PreparationMode,
    PreparationRecipe,
    PreparedArtifactRef,
    RunnerReference,
)
from ..models.assemble import AssembleManifest
from ..models.runner_execution import RunnerExecutionPolicy
from ..services.assemble import DOCUMENT_BUNDLE_JSON, AssembleOrchestrator
from ..services.bundle_layout import BundleLayoutService
from ..services.evaluation import EvaluationService
from ..services.evaluation_cohorts import EvaluationCohortService
from ..services.kraken_runner import HuggingFaceKrakenRunner
from ..services.merge import AbstainingMergeService
from ..services.olmocr_runner import HuggingFaceOlmocrRunner
from ..services.preparation import (
    PageClassifier,
    PagePreparationService,
    PageQualityAssessor,
    PreparationBundleService,
)
from ..services.runner_batching import RunnerBatchPlanner
from ..services.runner_execution import RunnerExecutionService
from ..services.runner_packaging import RunnerInputPackager
from ..services.source_acquisition import SourceAcquisitionService
from ..services.witness_adaptation import WitnessAdaptationService
from ..settings import Settings
from .utils import console, print_error, print_info


def _hosted_runner_class(runner_id: str) -> type:
    """
    Resolve one hosted runner class from ``runner_id`` without a registry.

    Args:
        runner_id: Stable logical runner id from ``RunnerReference``.

    Returns:
        Hosted runner class for ``runner_id``.

    Raises:
        click.ClickException: If ``runner_id`` is not supported.

    """
    # Built at call time so tests can patch the module-level class names.
    hosted_runner_by_id = {
        "olmocr": HuggingFaceOlmocrRunner,
        "kraken": HuggingFaceKrakenRunner,
    }
    runner_cls = hosted_runner_by_id.get(runner_id)
    if runner_cls is None:
        supported = ", ".join(sorted(hosted_runner_by_id))
        msg = f"unsupported runner_id {runner_id!r}; supported: {supported}"
        raise click.ClickException(msg)
    return runner_cls


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
    wordwending command line interface.

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
        os.environ["WORDWENDING_CONFIG_FILE"] = config_file

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
    table = Table(title="wordwending Version Info")
    table.add_column("Package", justify="left", style="cyan", no_wrap=True)
    table.add_column("Version", justify="left", style="yellow", no_wrap=True)

    table.add_row("wordwending", str(wordwending.__version__))
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

    settings_dump = settings.model_dump(mode="json")
    if output_format == "json":
        click.echo(json.dumps(settings_dump))
    elif output_format == "table":
        table = Table(title="Settings", show_header=True, header_style="bold magenta")
        table.add_column("Setting Name", style="cyan")
        table.add_column("Value", style="green")

        for setting_name, setting_value in settings_dump.items():
            table.add_row(setting_name, str(setting_value))

        console.print(table)
    else:  # text format
        for setting_name, setting_value in settings_dump.items():
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

    Side Effects:
        Writes evaluation summary JSON to ``output_json`` with three top-level
        families: ``text``, ``structure``, and ``style`` (typography and note
        linkage nested under ``style``).

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


@cli.command("eval-cohorts")
@click.argument(
    "records",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--output-json",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Destination path for EvaluationCohortReport JSON.",
)
def eval_cohorts(records: Path, output_json: Path) -> None:
    """
    Summarize page evaluation records into fixed cohort views.

    Args:
        records: JSON array of PageEvaluationRecord objects.
        output_json: Destination path for EvaluationCohortReport JSON.

    Side Effects:
        Writes cohort summary JSON to ``output_json``.

    Raises:
        click.ClickException: When inputs fail validation or I/O fails.

    """
    try:
        payload = json.loads(records.read_text(encoding="utf-8"))
        page_records = TypeAdapter(list[PageEvaluationRecord]).validate_python(payload)
    except (OSError, ValidationError, ValueError, json.JSONDecodeError) as exc:
        raise click.ClickException(str(exc)) from exc

    report = EvaluationCohortService().summarize(page_records)

    try:
        output_json.write_text(report.model_dump_json(indent=2), encoding="utf-8")
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
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="PreparationRecipe JSON file. Repeat for competing variants.",
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
@click.option(
    "--overrides",
    default=None,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="JSON manifest of per-page operator overrides.",
)
def prepare_pages(  # noqa: PLR0913, PLR0917
    source: Path,
    recipe: tuple[Path, ...],
    output_dir: Path,
    mode: str | None,
    page_class: str | None,
    override_reason: str | None,
    overrides: Path | None,
) -> None:
    """
    Acquire and prepare source pages into a reproducible output bundle.

    Args:
        source: PDF, image, image folder, or ZIP of images.
        recipe: One or more PreparationRecipe JSON file paths.
        output_dir: Destination root for source and prepared artifacts.
        mode: Optional operator preparation-mode override.
        page_class: Optional operator page-class override.
        override_reason: Required reason when any override is set.
        overrides: Optional JSON manifest of per-page operator overrides.

    Side Effects:
        Writes acquired pages under ``output_dir/source``, recipe artifacts
        under ``output_dir/recipes``, and prepared page artifacts plus
        ``preparation.json`` under ``output_dir/pages``.

    Raises:
        click.ClickException: When inputs fail validation or I/O fails.

    """
    try:
        preparation_recipes = [_load_preparation_recipe(path) for path in recipe]
        page_overrides = _load_page_overrides(overrides)
        _reject_conflicting_overrides(
            page_overrides=page_overrides,
            mode=mode,
            page_class=page_class,
            override_reason=override_reason,
        )
        _reject_multi_recipe_global_overrides(
            len(preparation_recipes),
            mode=mode,
            page_class=page_class,
            override_reason=override_reason,
        )
        mode_override, page_class_override = _prepare_overrides(
            mode,
            page_class,
            override_reason,
        )
        service = PreparationBundleService(
            SourceAcquisitionService(),
            PagePreparationService(PageQualityAssessor(), PageClassifier()),
        )
        if page_overrides is not None:
            results = service.prepare_variants(
                source,
                preparation_recipes,
                output_dir,
                page_overrides=page_overrides,
            )
        elif len(preparation_recipes) == 1:
            results = service.prepare_bundle(
                source,
                preparation_recipes[0],
                output_dir,
                mode_override=mode_override,
                page_class_override=page_class_override,
                override_reason=override_reason,
            )
        else:
            results = service.prepare_variants(
                source,
                preparation_recipes,
                output_dir,
            )
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    warning_count = sum(len(result.assessment.warnings) for result in results)
    page_count = len({result.source_page.source_page_id for result in results})
    click.echo(f"pages: {page_count}")
    if len(preparation_recipes) > 1:
        click.echo(f"variants: {len(preparation_recipes)}")
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


def _load_page_overrides(
    overrides: Path | None,
) -> list[PagePreparationOverride] | None:
    """
    Load and validate a per-page override manifest.

    Args:
        overrides: Optional JSON manifest path.

    Returns:
        Validated override records, or ``None`` when unset.

    """
    if overrides is None:
        return None
    return [
        PagePreparationOverride.model_validate(item)
        for item in json.loads(overrides.read_text(encoding="utf-8"))
    ]


def _reject_conflicting_overrides(
    *,
    page_overrides: list[PagePreparationOverride] | None,
    mode: str | None,
    page_class: str | None,
    override_reason: str | None,
) -> None:
    """
    Reject mixing per-page overrides with legacy global CLI overrides.

    Keyword Args:
        page_overrides: Optional per-page override manifest.
        mode: Optional preparation-mode override from Click.
        page_class: Optional page-class override from Click.
        override_reason: Optional override reason from Click.

    Raises:
        ValueError: If per-page and global overrides are both supplied.

    """
    if page_overrides is None:
        return
    if mode is not None or page_class is not None or override_reason is not None:
        msg = (
            "--overrides cannot be used together with --mode, --page-class, "
            "or --override-reason"
        )
        raise ValueError(msg)


def _reject_multi_recipe_global_overrides(
    recipe_count: int,
    *,
    mode: str | None,
    page_class: str | None,
    override_reason: str | None,
) -> None:
    """
    Reject global CLI overrides when multiple recipes are requested.

    Args:
        recipe_count: Number of ``--recipe`` values supplied.

    Keyword Args:
        mode: Optional preparation-mode override from Click.
        page_class: Optional page-class override from Click.
        override_reason: Optional override reason from Click.

    Raises:
        ValueError: If any global override is set with multiple recipes.

    """
    if recipe_count <= 1:
        return
    if mode is not None or page_class is not None or override_reason is not None:
        msg = (
            "--mode, --page-class, and --override-reason are not supported "
            "with multiple --recipe values"
        )
        raise ValueError(msg)


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


class _PreparedInputsManifest(BaseModel):
    """Prepared artifact manifest accepted by ``wordwending run``."""

    #: Ordered prepared artifacts ready for runner execution.
    artifacts: list[PreparedArtifactRef]


@cli.command("run")
@click.argument(
    "prepared_inputs",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--policy",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="RunnerExecutionPolicy JSON file.",
)
@click.option(
    "--runner",
    "runner_reference",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="RunnerReference JSON file.",
)
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Bundle root containing prepared artifact bytes.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Destination directory for runner outputs.",
)
@click.option("--run-id", required=True, help="Execution run identifier.")
@click.option(
    "--document-id",
    required=True,
    help="Document identifier under processing.",
)
@click.pass_context
def run_runner(  # noqa: PLR0913, PLR0917
    ctx: click.Context,
    prepared_inputs: Path,
    policy: Path,
    runner_reference: Path,
    bundle_root: Path,
    output_dir: Path,
    run_id: str,
    document_id: str,
) -> None:
    """
    Execute prepared artifacts against one hosted runner (olmOCR or kraken).

    Args:
        ctx: Click context object.
        prepared_inputs: JSON manifest of prepared artifact references.
        policy: RunnerExecutionPolicy JSON file path.
        runner_reference: RunnerReference JSON file path.
        bundle_root: Bundle root containing prepared artifact bytes.
        output_dir: Destination root for runner outputs.
        run_id: Execution run identifier.
        document_id: Document identifier under processing.

    Side Effects:
        Writes runner inputs, batch records, witnesses, and throughput JSON.

    Raises:
        click.ClickException: When inputs or settings fail validation.

    """
    try:
        manifest = _PreparedInputsManifest.model_validate_json(
            prepared_inputs.read_text(encoding="utf-8")
        )
        execution_policy = RunnerExecutionPolicy.model_validate_json(
            policy.read_text(encoding="utf-8")
        )
        runner = RunnerReference.model_validate_json(
            runner_reference.read_text(encoding="utf-8")
        )
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    runner_cls = _hosted_runner_class(runner.runner_id)

    settings: Settings = ctx.obj["settings"]
    api_key = settings.huggingface_api_key
    token = api_key.get_secret_value() if api_key is not None else None
    if not token:
        msg = "missing settings value huggingface_api_key"
        raise click.ClickException(msg)
    endpoint_url = settings.huggingface_model_endpoints.get(
        execution_policy.endpoint.endpoint_key
    )
    if endpoint_url is None:
        msg = (
            "missing Hugging Face endpoint for "
            f"{execution_policy.endpoint.endpoint_key}"
        )
        raise click.ClickException(msg)

    output_dir.mkdir(parents=True, exist_ok=True)
    client = httpx.Client()
    try:
        hosted_runner = runner_cls(
            runner=runner,
            policy=execution_policy,
            endpoint_url=str(endpoint_url),
            token=token,
            client=client,
        )
        service = RunnerExecutionService(
            RunnerBatchPlanner(),
            RunnerInputPackager(),
            hosted_runner,
        )
        batches, summary = service.run(
            run_id,
            document_id,
            manifest.artifacts,
            bundle_root,
            output_dir,
        )
    except (OSError, ValidationError, ValueError, ConfigurationError) as exc:
        raise click.ClickException(str(exc)) from exc
    finally:
        client.close()

    click.echo(f"batches: {len(batches)}")
    click.echo(f"failed_items: {summary.failed_item_count}")
    click.echo(f"items_per_second: {summary.items_per_second:.4f}")
    click.echo(f"output: {output_dir}")
    if summary.failed_item_count > 0:
        count = summary.failed_item_count
        msg = f"runner execution finished with {count} failed item(s)"
        raise click.ClickException(msg)


@cli.command("export")
@click.argument(
    "document_bundle",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Filesystem root that receives exports/ artifacts.",
)
def export_document(document_bundle: Path, bundle_root: Path) -> None:
    """
    Write derived bundle/RAG/Markdown exports from a DocumentBundle JSON.

    Args:
        document_bundle: DocumentBundle JSON file path.
        bundle_root: Filesystem root that receives exports/ artifacts.

    Side Effects:
        Writes exports/bundle.json, exports/rag.jsonl,
        exports/stitched_chunks.jsonl, and exports/document.md.

    Raises:
        click.ClickException: When bundle JSON or export writes fail validation.

    """
    try:
        bundle = DocumentBundle.model_validate_json(
            document_bundle.read_text(encoding="utf-8")
        )
        exported = BundleLayoutService().write_document_exports(bundle, bundle_root)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    exports = exported.exports
    if exports.document_markdown_path is not None:
        click.echo(f"markdown: {bundle_root / exports.document_markdown_path}")
    click.echo(f"bundle_json: {bundle_root / exports.bundle_json_path}")


@cli.command("assemble")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Filesystem root for witness paths and the written bundle tree.",
)
@click.option(
    "--manifest",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="AssembleManifest JSON with relative witness and image paths.",
)
def assemble_document(bundle_root: Path, manifest: Path) -> None:
    """
    Adapt raw witnesses, merge, and write a Spec 0002 document bundle.

    Args:
        bundle_root: Filesystem root for relative paths and bundle output.
        manifest: AssembleManifest JSON describing pages and witness refs.

    Side Effects:
        Writes document and page manifests, graphs, witnesses, images, and
        ``document-bundle.json`` under ``bundle_root``.

    Raises:
        click.ClickException: When manifest validation or assemble fails.

    """
    try:
        assemble_manifest = AssembleManifest.model_validate_json(
            manifest.read_text(encoding="utf-8")
        )
        orchestrator = AssembleOrchestrator(
            adapter=WitnessAdaptationService(),
            merge=AbstainingMergeService(),
            bundles=BundleLayoutService(),
        )
        bundle = orchestrator.assemble_document(
            bundle_root=bundle_root,
            source=assemble_manifest.source,
            bibliographic=assemble_manifest.bibliographic,
            acquisition=assemble_manifest.acquisition,
            pages=assemble_manifest.pages,
            merge_policy=assemble_manifest.merge_policy,
        )
    except (OSError, ValidationError, ValueError, FileNotFoundError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"document_id: {bundle.document_id}")
    click.echo(f"pages: {len(bundle.pages)}")
    click.echo(f"manifest: {bundle_root / 'manifest.json'}")
    click.echo(f"document_bundle: {bundle_root / DOCUMENT_BUNDLE_JSON}")


@cli.command("inspect-bundle")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Filesystem root for one assembled document bundle tree.",
)
def inspect_bundle(bundle_root: Path) -> None:
    """
    Print an honest summary of one assembled document bundle.

    Args:
        bundle_root: Filesystem root for one document bundle tree.

    Raises:
        click.ClickException: When the bundle root is missing or corrupt.

    """
    layout = BundleLayoutService()
    try:
        doc_manifest = layout.read_document_manifest(bundle_root)
    except (OSError, ValidationError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"document_id: {doc_manifest.document_id}")
    click.echo(f"page_count: {doc_manifest.page_count}")
    click.echo(f"bundle_schema_version: {doc_manifest.bundle_schema_version}")
    for page_number in range(1, doc_manifest.page_count + 1):
        try:
            page_manifest = layout.read_page_manifest(bundle_root, page_number)
        except (OSError, ValidationError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(f"page_id: {page_manifest.page_id}")
        click.echo(f"page_number: {page_manifest.page_number}")
        click.echo(f"graph: {page_manifest.graph_artifact_path}")
        for witness in page_manifest.witness_artifacts:
            click.echo(
                f"witness: {witness.witness_id} runner={witness.runner_id} "
                f"path={witness.artifact_path}"
            )
        _echo_page_flags(bundle_root, page_manifest.evaluation_flags_path)


def _echo_page_flags(bundle_root: Path, evaluation_flags_path: str | None) -> None:
    """
    Print evaluation/merge flags from one page ``flags.json`` sidecar.

    Args:
        bundle_root: Filesystem root for the document bundle tree.
        evaluation_flags_path: Bundle-relative path to ``evaluation/flags.json``.

    """
    if not evaluation_flags_path:
        return
    flags_path = bundle_root / evaluation_flags_path
    if not flags_path.is_file():
        return
    try:
        payload = json.loads(flags_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    flags = payload.get("flags", [])
    if not isinstance(flags, list):
        return
    for flag in flags:
        if not isinstance(flag, dict):
            continue
        flag_id = flag.get("flag_id", "")
        flag_type = flag.get("flag_type", "")
        message = flag.get("message", "")
        click.echo(f"flag: {flag_id} type={flag_type} message={message}")
