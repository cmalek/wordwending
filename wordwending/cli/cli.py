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

from ..exc import ConfigurationError, EndpointLifecycleError
from ..models import (
    BundlePage,
    ChecksumVerificationStatus,
    DocumentBundle,
    ExportSummary,
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
from ..models.bakeoff import BAKEOFF_MATRIX_FILENAME, BakeoffManifest
from ..models.runner_execution import RunnerExecutionPolicy
from ..services.assemble import DOCUMENT_BUNDLE_JSON, AssembleOrchestrator
from ..services.bakeoff import BakeoffService
from ..services.bundle_checksum import BundleChecksumService
from ..services.bundle_layout import BundleLayoutService
from ..services.evaluation import EvaluationService
from ..services.evaluation_cohorts import EvaluationCohortService
from ..services.merge import AbstainingMergeService
from ..services.pass_runner_registry import PassRunnerRegistry, UnknownPassRunnerError
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
from .endpoints import endpoints, ensure_and_overlay_settings
from .review import review
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


cli.add_command(review)
cli.add_command(endpoints)


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
@click.option(
    "--force",
    is_flag=True,
    help="Bypass the resume ledger and re-run completed batches.",
)
@click.option(
    "--ensure-endpoints",
    is_flag=True,
    help=(
        "Ensure the hosted Inference Endpoint for this runner is ready and "
        "overlay its HTTPS URL onto in-process settings."
    ),
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
    force: bool,
    ensure_endpoints: bool,
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
        force: When ``True``, bypass the resume ledger and re-run batches.
        ensure_endpoints: When ``True``, ensure the runner endpoint is ready
            and overlay its HTTPS URL onto in-process settings.

    Side Effects:
        Writes runner inputs, batch records, witnesses, throughput JSON, and
        updates ``bundle_root/runner-resume-ledger.json`` for completed batches.
        When ``ensure_endpoints`` is set, may create/resume remote endpoints and
        rewrite the session ledger.

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

    try:
        runner_cls = PassRunnerRegistry().resolve(runner.runner_id)
    except UnknownPassRunnerError as exc:
        raise click.ClickException(str(exc)) from exc

    settings: Settings = ctx.obj["settings"]
    if ensure_endpoints:
        settings = _overlay_ensure_endpoints(ctx, settings, [runner.runner_id])
    token = _huggingface_token(settings)
    endpoint_url = _resolve_hosted_endpoint_url(
        settings,
        runner_id=runner.runner_id,
        endpoint_key=execution_policy.endpoint.endpoint_key,
    )
    batches, summary = _invoke_hosted_run(
        runner_cls=runner_cls,
        runner=runner,
        execution_policy=execution_policy,
        endpoint_url=endpoint_url,
        token=token,
        run_id=run_id,
        document_id=document_id,
        artifacts=manifest.artifacts,
        bundle_root=bundle_root,
        output_dir=output_dir,
        force=force,
    )
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
    _echo_checksum_results(bundle_root)
    _echo_export_paths(bundle_root)


@cli.command("bakeoff")
@click.option(
    "--bundle-root",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Filesystem root for relative gold and prediction paths.",
)
@click.option(
    "--manifest",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="BakeoffManifest JSON with recorded predictions (offline harness).",
)
@click.option(
    "--profile",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="MetricProfile JSON for EvaluationService scoring.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory that will receive bakeoff-matrix-v1.json.",
)
@click.option(
    "--ensure-endpoints",
    is_flag=True,
    help=(
        "Ensure catalogued real bakeoff candidates (olmocr/kraken) are ready "
        "and overlay HTTPS URLs onto in-process settings."
    ),
)
@click.pass_context
def bakeoff_matrix(  # noqa: PLR0913, PLR0917
    ctx: click.Context,
    bundle_root: Path,
    manifest: Path,
    profile: Path,
    output_dir: Path,
    ensure_endpoints: bool,
) -> None:
    """
    Score recorded candidate predictions into bakeoff-matrix-v1.json.

    Thin offline CLI over :class:`~wordwending.services.bakeoff.BakeoffService`.
    Spec 0004 Phase 5 remains **NOT COMPLETE** (cost/license/operability
    scoring and full held-out corpus deferred).

    Args:
        ctx: Click context object.
        bundle_root: Root for relative gold and prediction paths.
        manifest: BakeoffManifest JSON describing candidates and recordings.
        profile: MetricProfile JSON for EvaluationService.
        output_dir: Directory for the written matrix artifact.
        ensure_endpoints: When ``True``, ensure catalogued real candidates and
            overlay HTTPS URLs onto in-process settings before scoring.

    Side Effects:
        Writes ``bakeoff-matrix-v1.json`` under ``output_dir``. When
        ``ensure_endpoints`` is set, may create/resume remote endpoints and
        rewrite the session ledger.

    Raises:
        click.ClickException: When inputs fail validation or I/O fails.

    """
    try:
        bakeoff_manifest = BakeoffManifest.model_validate_json(
            manifest.read_text(encoding="utf-8")
        )
        if ensure_endpoints:
            _ensure_catalogued_bakeoff_endpoints(ctx, bakeoff_manifest)
        metric_profile = MetricProfile.model_validate_json(
            profile.read_text(encoding="utf-8")
        )
        request, invoker = BakeoffService.load_recorded_manifest(
            bakeoff_manifest, bundle_root=bundle_root
        )
        service = BakeoffService(
            evaluation=EvaluationService(),
            invoker=invoker,
        )
        matrix = service.run(request, metric_profile)
        matrix_path = service.write_matrix(matrix, output_dir)
    except (
        OSError,
        ValidationError,
        ValueError,
        FileNotFoundError,
        ConfigurationError,
        EndpointLifecycleError,
    ) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"matrix: {matrix_path}")
    click.echo(f"cells: {len(matrix.cells)}")
    click.echo(f"filename: {BAKEOFF_MATRIX_FILENAME}")
    click.echo("phase_5: NOT COMPLETE")


def _overlay_ensure_endpoints(
    ctx: click.Context,
    settings: Settings,
    runner_ids: list[str],
) -> Settings:
    """
    Ensure runners and store an in-process Settings URL overlay on ``ctx``.

    Args:
        ctx: Click context carrying settings.
        settings: Effective settings before overlay.
        runner_ids: Catalogued runner identifiers to ensure.

    Returns:
        Settings copy with overlaid HTTPS endpoint URLs.

    Raises:
        click.ClickException: When configuration or lifecycle ensure fails.

    """
    try:
        overlaid = ensure_and_overlay_settings(settings, runner_ids)
    except (ConfigurationError, EndpointLifecycleError) as exc:
        raise click.ClickException(str(exc)) from exc
    ctx.obj["settings"] = overlaid
    return overlaid


def _ensure_catalogued_bakeoff_endpoints(
    ctx: click.Context,
    bakeoff_manifest: BakeoffManifest,
) -> None:
    """
    Ensure catalogued real bakeoff candidates and overlay HTTPS URLs.

    Fake / non-catalog runners in the manifest are skipped. When the
    intersection of manifest candidates with the catalog is empty, skip
    ensure/overlay entirely (do not call ``ensure_up([])``, which means
    all catalogued runners for the ``endpoints up`` CLI).

    Args:
        ctx: Click context carrying settings.
        bakeoff_manifest: Parsed bakeoff manifest with candidate runner ids.

    Raises:
        click.ClickException: When configuration or lifecycle ensure fails.

    """
    settings: Settings = ctx.obj["settings"]
    catalog = {entry.runner_id for entry in settings.effective_endpoint_catalog()}
    runner_ids = [
        candidate.runner_id
        for candidate in bakeoff_manifest.candidates
        if candidate.runner_id in catalog
    ]
    if not runner_ids:
        return
    _overlay_ensure_endpoints(ctx, settings, runner_ids)


def _huggingface_token(settings: Settings) -> str:
    """
    Return the Hugging Face API token from settings.

    Args:
        settings: Effective application settings.

    Returns:
        Secret token string for hosted inference.

    Raises:
        click.ClickException: When ``huggingface_api_key`` is missing.

    """
    api_key = settings.huggingface_api_key
    token = api_key.get_secret_value() if api_key is not None else None
    if not token:
        msg = "missing settings value huggingface_api_key"
        raise click.ClickException(msg)
    return token


def _resolve_hosted_endpoint_url(
    settings: Settings,
    *,
    runner_id: str,
    endpoint_key: str,
) -> str:
    """
    Resolve a hosted endpoint URL from overlay or configured endpoint key.

    Prefers an in-process overlay keyed by ``runner_id``, then falls back to
    the policy ``endpoint_key``.

    Args:
        settings: Effective settings possibly carrying a URL overlay.

    Keyword Args:
        runner_id: Stable hosted runner identifier.
        endpoint_key: Policy endpoint key into ``huggingface_model_endpoints``.

    Returns:
        HTTPS endpoint URL string.

    Raises:
        click.ClickException: When neither key is present in settings.

    """
    endpoint_url = settings.huggingface_model_endpoints.get(runner_id)
    if endpoint_url is None:
        endpoint_url = settings.huggingface_model_endpoints.get(endpoint_key)
    if endpoint_url is None:
        msg = f"missing Hugging Face endpoint for {endpoint_key}"
        raise click.ClickException(msg)
    return str(endpoint_url)


def _invoke_hosted_run(  # noqa: PLR0913
    *,
    runner_cls: type,
    runner: RunnerReference,
    execution_policy: RunnerExecutionPolicy,
    endpoint_url: str,
    token: str,
    run_id: str,
    document_id: str,
    artifacts: list[PreparedArtifactRef],
    bundle_root: Path,
    output_dir: Path,
    force: bool,
) -> tuple:
    """
    Construct a hosted runner and execute one run.

    Keyword Args:
        runner_cls: Constructable hosted PassRunner class.
        runner: Runner reference for the invocation.
        execution_policy: Batching and endpoint policy.
        endpoint_url: Ready HTTPS endpoint URL.
        token: Hugging Face API token.
        run_id: Execution run identifier.
        document_id: Document identifier under processing.
        artifacts: Prepared artifact refs to execute.
        bundle_root: Bundle root containing prepared bytes.
        output_dir: Destination directory for runner outputs.
        force: When ``True``, bypass the resume ledger.

    Returns:
        Tuple of ``(batches, summary)`` from ``RunnerExecutionService.run``.

    Raises:
        click.ClickException: When execution fails validation or I/O.

    """
    output_dir.mkdir(parents=True, exist_ok=True)
    client = httpx.Client()
    try:
        hosted_runner = runner_cls(
            runner=runner,
            policy=execution_policy,
            endpoint_url=endpoint_url,
            token=token,
            client=client,
        )
        service = RunnerExecutionService(
            RunnerBatchPlanner(),
            RunnerInputPackager(),
            hosted_runner,
        )
        return service.run(
            run_id,
            document_id,
            artifacts,
            bundle_root,
            output_dir,
            force=force,
        )
    except (OSError, ValidationError, ValueError, ConfigurationError) as exc:
        raise click.ClickException(str(exc)) from exc
    finally:
        client.close()


def _resolve_export_summary(bundle_root: Path) -> ExportSummary | None:
    """
    Load export path hints from the best available bundle JSON on disk.

    Args:
        bundle_root: Filesystem root for one document bundle tree.

    Returns:
        ``ExportSummary`` from ``exports/bundle.json`` when present, otherwise
        from ``document-bundle.json``; ``None`` when neither file is readable.

    """
    exported_bundle = bundle_root / "exports" / "bundle.json"
    if exported_bundle.is_file():
        try:
            bundle = DocumentBundle.model_validate_json(
                exported_bundle.read_text(encoding="utf-8")
            )
        except (OSError, ValidationError, ValueError):
            pass
        else:
            return bundle.exports
    doc_bundle = bundle_root / DOCUMENT_BUNDLE_JSON
    if doc_bundle.is_file():
        try:
            bundle = DocumentBundle.model_validate_json(
                doc_bundle.read_text(encoding="utf-8")
            )
        except (OSError, ValidationError, ValueError):
            pass
        else:
            return bundle.exports
    return None


def _echo_checksum_results(bundle_root: Path) -> None:
    """
    Print OK/FAIL/SKIPPED lines for bundle-layout recorded checksums.

    Args:
        bundle_root: Filesystem root for the document bundle tree.

    """
    report = BundleChecksumService().verify(bundle_root)
    for result in report.results:
        if result.status == ChecksumVerificationStatus.OK:
            click.echo(f"checksum: {result.artifact_path} OK")
            continue
        if result.status == ChecksumVerificationStatus.SKIPPED:
            detail = result.detail or "skipped"
            click.echo(f"checksum: {result.artifact_path} SKIPPED {detail}")
            continue
        line = f"checksum: {result.artifact_path} FAIL"
        if result.recorded_checksum:
            line += f" recorded={result.recorded_checksum}"
        if result.computed_checksum:
            line += f" computed={result.computed_checksum}"
        if result.detail:
            line += f" ({result.detail})"
        click.echo(line)


def _echo_export_paths(bundle_root: Path) -> None:
    """
    Print bundle-relative export artifact paths that exist on disk.

    Args:
        bundle_root: Filesystem root for the document bundle tree.

    """
    summary = _resolve_export_summary(bundle_root)
    if summary is None:
        return
    for rel_path in (
        summary.bundle_json_path,
        summary.rag_jsonl_path,
        summary.stitched_chunks_jsonl_path,
        summary.document_markdown_path,
    ):
        if rel_path and (bundle_root / rel_path).is_file():
            click.echo(f"export: {rel_path}")


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
