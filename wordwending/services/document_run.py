# Copyright (C) 2026 Chris Malek.
"""DocumentRunOrchestrator: thin facade sequencing one document run."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from wordwending.models.document_run import (
    DocumentRunConfig,
    DocumentRunStage,
)
from wordwending.models.evaluation import MetricProfile
from wordwending.models.merge import MergePolicy
from wordwending.models.ocr import (
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePage,
    DocumentBundle,
    GoldPageAnnotation,
    InputKind,
    PreparedArtifactRef,
    RunnerReference,
    SourceDescriptor,
)
from wordwending.models.preparation import PreparationRecipe, PreparationResult
from wordwending.models.runner_execution import RunnerExecutionPolicy
from wordwending.services.assemble import DOCUMENT_BUNDLE_JSON

if TYPE_CHECKING:
    from collections.abc import Callable

    from wordwending.services.assemble import AssembleOrchestrator
    from wordwending.services.assemble_manifest import AssembleManifestBuilder
    from wordwending.services.bundle_layout import BundleLayoutService
    from wordwending.services.evaluation import EvaluationService
    from wordwending.services.pass_runner_registry import PassRunnerRegistry
    from wordwending.services.preparation import PreparationBundleService
    from wordwending.services.review_cli import ReviewCliService
    from wordwending.services.runner_execution import RunnerExecutionService


@dataclass(frozen=True)
class DocumentRunResult:
    """Outcome summary for one orchestrated document run."""

    #: Logical run identifier from the config.
    run_id: str
    #: Document identifier from the config.
    document_id: str
    #: Resolved bundle root used for prepare and subsequent stages.
    bundle_root: Path
    #: Stages that completed successfully in order.
    stages_completed: list[DocumentRunStage]
    #: Path to written ``document-bundle.json`` when assemble ran.
    document_bundle_path: Path | None
    #: Export root when export ran.
    export_root: Path | None
    #: Page ids with pending review tasks after issue, when issued.
    pending_task_pages: list[str]


@dataclass
class _DocumentRunState:
    """Mutable per-run accumulator for orchestrator stage outputs."""

    #: Path to written ``document-bundle.json`` after assemble.
    document_bundle_path: Path | None = None
    #: In-memory assembled bundle kept for eval/issue/export.
    document_bundle: DocumentBundle | None = None
    #: Export directory after export stage.
    export_root: Path | None = None
    #: Page ids with non-empty pending task queues after issue.
    pending_task_pages: list[str] | None = None


def prepared_artifacts_from_bundle(bundle_root: Path) -> list[PreparedArtifactRef]:
    """
    Derive runner input artifacts from prepare-tree ``preparation.json`` files.

    Walks ``bundle_root/pages/**/preparation.json``. When a page has
    ``prepared_units``, those refs are used as-is. Otherwise a full-page
    ``InputKind.IMAGE`` artifact is synthesized from the prepared page image.

    Args:
        bundle_root: Bundle root containing prepare-tree pages.

    Returns:
        Ordered prepared artifact references for runner execution.

    """
    artifacts: list[PreparedArtifactRef] = []
    for prep_path in sorted(bundle_root.glob("pages/*/prepared/*/preparation.json")):
        result = PreparationResult.model_validate_json(
            prep_path.read_text(encoding="utf-8")
        )
        artifacts.extend(_artifacts_from_preparation_result(result))
    return artifacts


def _artifacts_from_preparation_result(
    result: PreparationResult,
) -> list[PreparedArtifactRef]:
    """
    Map one ``PreparationResult`` to runner artifact refs.

    Args:
        result: Persisted preparation outcome for one page.

    Returns:
        Prepared-unit refs when present; otherwise one full-page image ref.

    """
    page = result.prepared_page
    if page.prepared_units:
        return list(page.prepared_units)
    page_id = result.source_page.source_page_id
    return [
        PreparedArtifactRef(
            artifact_id=f"artifact-{page.prepared_page_id}",
            kind=InputKind.IMAGE,
            page_id=page_id,
            artifact_path=page.image_path,
            checksum=page.image_checksum,
        )
    ]


def _resolve_path(raw: str, *, config_dir: Path | None) -> Path:
    """
    Resolve a config path string to an absolute ``Path``.

    Args:
        raw: Absolute or relative path string from the config.

    Keyword Args:
        config_dir: Base directory for relative paths; required when ``raw``
            is relative.

    Returns:
        Absolute filesystem path.

    Raises:
        ValueError: If ``raw`` is relative and ``config_dir`` is unset.

    """
    path = Path(raw)
    if path.is_absolute():
        return path
    if config_dir is None:
        msg = f"relative path {raw!r} requires config_dir"
        raise ValueError(msg)
    return (config_dir / path).resolve()


def _load_json_model(path: Path, model: type[Any]) -> Any:
    """
    Load and validate one JSON model from ``path``.

    Args:
        path: Filesystem path to JSON.
        model: Pydantic model type with ``model_validate_json``.

    Returns:
        Validated model instance.

    """
    return model.model_validate_json(path.read_text(encoding="utf-8"))


class DocumentRunOrchestrator:
    """
    Thin facade: sequence existing stage modules for one document run.

    Args:
        preparation: Bundle preparation service for the prepare stage.
        runner_registry: Registry mapping runner ids to PassRunner classes.
        manifest_builder: Assemble-from-run manifest builder.
        assemble: Document assemble orchestrator.
        bundles: Bundle layout / export writer.
        runner_service_factory: Builds one ``RunnerExecutionService`` per
            runner invocation (mirrors CLI ``_invoke_hosted_run``).
        evaluation: Optional evaluation service for the eval stage.
        review_cli: Optional review issue collaborator.
        endpoint_ensurer: Optional ensure/overlay callable invoked when
            ``config.ensure_endpoints`` is true.

    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        preparation: PreparationBundleService,
        runner_registry: PassRunnerRegistry,
        manifest_builder: AssembleManifestBuilder,
        assemble: AssembleOrchestrator,
        bundles: BundleLayoutService,
        runner_service_factory: Callable[..., RunnerExecutionService],
        evaluation: EvaluationService | None = None,
        review_cli: ReviewCliService | None = None,
        endpoint_ensurer: Callable[..., None] | None = None,
    ) -> None:
        """
        Bind stage collaborators for one orchestrator instance.

        Keyword Args:
            preparation: Bundle preparation service for the prepare stage.
            runner_registry: Registry mapping runner ids to PassRunner classes.
            manifest_builder: Assemble-from-run manifest builder.
            assemble: Document assemble orchestrator.
            bundles: Bundle layout / export writer.
            runner_service_factory: Builds one ``RunnerExecutionService`` per
                runner invocation.
            evaluation: Optional evaluation service for the eval stage.
            review_cli: Optional review issue collaborator.
            endpoint_ensurer: Optional ensure/overlay callable for endpoints.

        """
        #: Bundle preparation service for the prepare stage.
        self._preparation = preparation
        #: Registry mapping runner ids to PassRunner classes.
        self._runner_registry = runner_registry
        #: Assemble-from-run manifest builder.
        self._manifest_builder = manifest_builder
        #: Document assemble orchestrator.
        self._assemble = assemble
        #: Bundle layout / export writer.
        self._bundles = bundles
        #: Factory producing one RunnerExecutionService per runner invocation.
        self._runner_service_factory = runner_service_factory
        #: Optional evaluation service for the eval stage.
        self._evaluation = evaluation
        #: Optional review CLI service for issuing pending tasks.
        self._review_cli = review_cli
        #: Optional endpoint ensure/overlay hook.
        self._endpoint_ensurer = endpoint_ensurer

    def run(
        self,
        config: DocumentRunConfig,
        *,
        config_dir: Path | None = None,
    ) -> DocumentRunResult:
        """
        Execute configured stages for one document run.

        Keyword Args:
            config_dir: Base directory for resolving relative config paths.
                Required when any path on ``config`` is relative. Paths are
                never resolved relative to ``bundle_root``.

        Args:
            config: Document run configuration.

        Returns:
            Summary of completed stages and output locations.

        Raises:
            ValueError: When relative paths lack ``config_dir``, runner ids
                mismatch references, required collaborators are missing, or
                ``ensure_endpoints`` lacks an ensurer.

        """
        bundle_root = _resolve_path(config.bundle_root, config_dir=config_dir)
        state = _DocumentRunState()
        stages_completed: list[DocumentRunStage] = []
        for stage in config.resolved_stages():
            self._dispatch_stage(
                stage,
                config,
                bundle_root=bundle_root,
                config_dir=config_dir,
                state=state,
            )
            stages_completed.append(stage)
        return DocumentRunResult(
            run_id=config.run_id,
            document_id=config.document_id,
            bundle_root=bundle_root,
            stages_completed=stages_completed,
            document_bundle_path=state.document_bundle_path,
            export_root=state.export_root,
            pending_task_pages=list(state.pending_task_pages or []),
        )

    def _dispatch_stage(
        self,
        stage: DocumentRunStage,
        config: DocumentRunConfig,
        *,
        bundle_root: Path,
        config_dir: Path | None,
        state: _DocumentRunState,
    ) -> None:
        """
        Run one stage, updating ``state`` as needed.

        Args:
            stage: Stage to execute.
            config: Document run configuration.

        Keyword Args:
            bundle_root: Resolved bundle root.
            config_dir: Base for relative config paths.
            state: Mutable per-run accumulator.

        Raises:
            ValueError: When a required collaborator is missing.

        """
        if stage is DocumentRunStage.PREPARE:
            self._run_prepare(
                config, bundle_root=bundle_root, config_dir=config_dir
            )
            return
        if stage is DocumentRunStage.RUN:
            self._run_runners(
                config, bundle_root=bundle_root, config_dir=config_dir
            )
            return
        if stage is DocumentRunStage.ASSEMBLE:
            self._run_assemble(
                config,
                bundle_root=bundle_root,
                config_dir=config_dir,
                state=state,
            )
            return
        if stage is DocumentRunStage.EVAL:
            self._run_eval(
                config,
                bundle_root=bundle_root,
                config_dir=config_dir,
                state=state,
            )
            return
        if stage is DocumentRunStage.ISSUE_REVIEW_TASKS:
            self._run_issue_review_tasks(config, bundle_root=bundle_root, state=state)
            return
        if stage is DocumentRunStage.EXPORT:
            self._run_export(bundle_root=bundle_root, state=state)
            return
        msg = f"unsupported document run stage: {stage!r}"
        raise ValueError(msg)

    def _run_prepare(
        self,
        config: DocumentRunConfig,
        *,
        bundle_root: Path,
        config_dir: Path | None,
    ) -> None:
        """
        Run the prepare stage into ``bundle_root``.

        Side Effects:
            Writes prepare-tree artifacts under ``bundle_root`` via the
            preparation collaborator.

        Args:
            config: Document run configuration.

        Keyword Args:
            bundle_root: Resolved prepare output directory.
            config_dir: Base for relative source/recipe paths.

        """
        source = _resolve_path(config.source_path, config_dir=config_dir)
        recipes = [
            PreparationRecipe.model_validate_json(
                _resolve_path(path, config_dir=config_dir).read_text(encoding="utf-8")
            )
            for path in config.recipe_paths
        ]
        if len(recipes) == 1:
            self._preparation.prepare_bundle(source, recipes[0], bundle_root)
        else:
            self._preparation.prepare_variants(source, recipes, bundle_root)

    def _run_runners(
        self,
        config: DocumentRunConfig,
        *,
        bundle_root: Path,
        config_dir: Path | None,
    ) -> None:
        """
        Execute each configured runner against derived prepared artifacts.

        Side Effects:
            Invokes ``endpoint_ensurer`` when configured, constructs one
            ``RunnerExecutionService`` per runner via the factory, and writes
            runner outputs under ``bundle_root/runs/<run_id>-<runner_id>/``.

        Args:
            config: Document run configuration.

        Keyword Args:
            bundle_root: Bundle root containing prepare outputs.
            config_dir: Base for relative runner reference/policy paths.

        Raises:
            ValueError: When runner reference ids mismatch or endpoints are
                requested without an ensurer.

        """
        artifacts = prepared_artifacts_from_bundle(bundle_root)
        for spec in config.runners:
            runner = RunnerReference.model_validate_json(
                _resolve_path(
                    spec.runner_reference_path,
                    config_dir=config_dir,
                ).read_text(encoding="utf-8")
            )
            if runner.runner_id != spec.runner_id:
                msg = (
                    f"runner reference id {runner.runner_id!r} does not match "
                    f"spec runner_id {spec.runner_id!r}"
                )
                raise ValueError(msg)
            policy = RunnerExecutionPolicy.model_validate_json(
                _resolve_path(spec.policy_path, config_dir=config_dir).read_text(
                    encoding="utf-8"
                )
            )
            runner_cls = self._runner_registry.resolve(spec.runner_id)
            if config.ensure_endpoints:
                if self._endpoint_ensurer is None:
                    msg = "ensure_endpoints requires endpoint_ensurer"
                    raise ValueError(msg)
                self._endpoint_ensurer(runner_ids=[spec.runner_id])
            execution_run_id = f"{config.run_id}-{spec.runner_id}"
            output_dir = bundle_root / "runs" / execution_run_id
            service = self._runner_service_factory(
                runner_cls=runner_cls,
                runner=runner,
                policy=policy,
                bundle_root=bundle_root,
                output_dir=output_dir,
            )
            service.run(
                execution_run_id,
                config.document_id,
                artifacts,
                bundle_root,
                output_dir,
                force=config.force_rerun,
            )

    def _run_assemble(
        self,
        config: DocumentRunConfig,
        *,
        bundle_root: Path,
        config_dir: Path | None,
        state: _DocumentRunState,
    ) -> None:
        """
        Build assemble manifest from run dirs and write the document bundle.

        Side Effects:
            Copies witnesses via the manifest builder and writes the Spec 0002
            document bundle under ``bundle_root``.

        Args:
            config: Document run configuration.

        Keyword Args:
            bundle_root: Bundle root owning prepare/run trees and assemble output.
            config_dir: Base for relative provenance/policy paths.
            state: Mutable per-run accumulator receiving the written bundle.

        """
        source, bibliographic, acquisition, merge_policy = self._load_assemble_inputs(
            config, config_dir=config_dir
        )
        run_dirs = [
            bundle_root / "runs" / f"{config.run_id}-{spec.runner_id}"
            for spec in config.runners
        ]
        manifest = self._manifest_builder.build(
            bundle_root=bundle_root,
            run_dirs=run_dirs,
            source=source,
            bibliographic=bibliographic,
            acquisition=acquisition,
            merge_policy=merge_policy,
        )
        bundle = self._assemble.assemble_document(
            bundle_root=bundle_root,
            source=manifest.source,
            bibliographic=manifest.bibliographic,
            acquisition=manifest.acquisition,
            pages=manifest.pages,
            merge_policy=manifest.merge_policy,
            document_id=config.document_id,
        )
        state.document_bundle = bundle
        state.document_bundle_path = bundle_root / DOCUMENT_BUNDLE_JSON

    def _load_assemble_inputs(
        self,
        config: DocumentRunConfig,
        *,
        config_dir: Path | None,
    ) -> tuple[
        SourceDescriptor,
        BibliographicProvenance,
        AcquisitionProvenance,
        MergePolicy,
    ]:
        """
        Load provenance and merge policy JSON for the assemble stage.

        Args:
            config: Document run configuration.

        Keyword Args:
            config_dir: Base for relative provenance/policy paths.

        Returns:
            Source, bibliographic, acquisition, and merge policy models.

        """
        source = _load_json_model(
            _resolve_path(config.source_json, config_dir=config_dir),
            SourceDescriptor,
        )
        bibliographic = _load_json_model(
            _resolve_path(config.bibliographic_json, config_dir=config_dir),
            BibliographicProvenance,
        )
        acquisition = _load_json_model(
            _resolve_path(config.acquisition_json, config_dir=config_dir),
            AcquisitionProvenance,
        )
        merge_policy = _load_json_model(
            _resolve_path(config.merge_policy_path, config_dir=config_dir),
            MergePolicy,
        )
        return source, bibliographic, acquisition, merge_policy

    def _run_eval(
        self,
        config: DocumentRunConfig,
        *,
        bundle_root: Path,
        config_dir: Path | None,
        state: _DocumentRunState,
    ) -> None:
        """
        Score gold pages and write evaluation summaries onto page graphs.

        Side Effects:
            Overwrites page graphs and ``document-bundle.json`` page entries
            with ``evaluation_summary`` write-back so issue sees eval flags.

        Args:
            config: Document run configuration.

        Keyword Args:
            bundle_root: Bundle root containing the assembled document.
            config_dir: Base for relative gold/metric paths.
            state: Mutable per-run accumulator holding the assembled bundle.

        Raises:
            ValueError: When evaluation is requested without a service, metric
                profile, assembled bundle, or matching page id.

        """
        if self._evaluation is None:
            msg = "eval stage requires evaluation service"
            raise ValueError(msg)
        if config.metric_profile_path is None:
            msg = "eval stage requires metric_profile_path"
            raise ValueError(msg)
        bundle = self._require_document_bundle(bundle_root=bundle_root, state=state)
        profile = _load_json_model(
            _resolve_path(config.metric_profile_path, config_dir=config_dir),
            MetricProfile,
        )
        updated_pages = list(bundle.pages)
        for page_id, gold_path in config.gold_page_paths.items():
            gold = _load_json_model(
                _resolve_path(gold_path, config_dir=config_dir),
                GoldPageAnnotation,
            )
            page = self._page_by_id(bundle, page_id)
            summary = self._evaluation.evaluate_page(page, gold, profile)
            updated = page.model_copy(update={"evaluation_summary": summary})
            self._bundles.write_page_graph(bundle_root, updated.page_number, updated)
            self._bundles.update_document_bundle_page(bundle_root, updated)
            updated_pages = [
                updated if existing.page_id == page_id else existing
                for existing in updated_pages
            ]
        state.document_bundle = bundle.model_copy(update={"pages": updated_pages})

    def _run_issue_review_tasks(
        self,
        config: DocumentRunConfig,
        *,
        bundle_root: Path,
        state: _DocumentRunState,
    ) -> None:
        """
        Rebuild pending review tasks from current page evaluation flags.

        Side Effects:
            Calls ``ReviewCliService.issue`` per page, rewriting pending task
            queues under each page tree.

        Args:
            config: Document run configuration.

        Keyword Args:
            bundle_root: Bundle root containing the assembled document.
            state: Mutable per-run accumulator receiving pending page ids.

        Raises:
            ValueError: When issue is requested without ``review_cli`` or an
                assembled bundle.

        """
        if self._review_cli is None:
            msg = "issue_review_tasks stage requires review_cli"
            raise ValueError(msg)
        bundle = self._require_document_bundle(bundle_root=bundle_root, state=state)
        pending: list[str] = []
        for page in bundle.pages:
            result = self._review_cli.issue(
                bundle_root,
                page.page_id,
                run_id=config.run_id,
            )
            if result.task_count > 0:
                pending.append(page.page_id)
        state.pending_task_pages = pending

    def _run_export(
        self,
        *,
        bundle_root: Path,
        state: _DocumentRunState,
    ) -> None:
        """
        Write derived document exports from ``document-bundle.json``.

        Side Effects:
            Writes export artifacts under ``bundle_root/exports/``.

        Keyword Args:
            bundle_root: Bundle root containing ``document-bundle.json``.
            state: Mutable per-run accumulator receiving ``export_root``.

        Raises:
            ValueError: When export is requested without an assembled bundle
                path on disk.

        """
        bundle = self._require_document_bundle(bundle_root=bundle_root, state=state)
        self._bundles.write_document_exports(bundle, bundle_root)
        state.export_root = bundle_root / "exports"

    def _require_document_bundle(
        self,
        *,
        bundle_root: Path,
        state: _DocumentRunState,
    ) -> DocumentBundle:
        """
        Return the in-memory or on-disk assembled document bundle.

        Keyword Args:
            bundle_root: Bundle root containing ``document-bundle.json``.
            state: Mutable per-run accumulator that may already hold the bundle.

        Returns:
            Assembled document bundle.

        Raises:
            ValueError: When neither state nor on-disk bundle is available.

        """
        if state.document_bundle is not None:
            return state.document_bundle
        bundle_path = bundle_root / DOCUMENT_BUNDLE_JSON
        if not bundle_path.is_file():
            msg = f"document bundle missing at {bundle_path}"
            raise ValueError(msg)
        bundle = DocumentBundle.model_validate_json(
            bundle_path.read_text(encoding="utf-8")
        )
        state.document_bundle = bundle
        state.document_bundle_path = bundle_path
        return bundle

    @staticmethod
    def _page_by_id(bundle: DocumentBundle, page_id: str) -> BundlePage:
        """
        Locate one page in ``bundle`` by ``page_id``.

        Args:
            bundle: Assembled document bundle.
            page_id: Stable page identifier to find.

        Returns:
            Matching bundle page.

        Raises:
            ValueError: When no page matches ``page_id``.

        """
        for page in bundle.pages:
            if page.page_id == page_id:
                return page
        msg = f"assembled bundle has no page with page_id {page_id!r}"
        raise ValueError(msg)
