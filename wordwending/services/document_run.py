# Copyright (C) 2026 Chris Malek.
"""DocumentRunOrchestrator: thin facade sequencing one document run."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from wordwending.models.document_run import (
    DocumentRunConfig,
    DocumentRunStage,
)
from wordwending.models.ocr import InputKind, PreparedArtifactRef, RunnerReference
from wordwending.models.preparation import PreparationRecipe, PreparationResult
from wordwending.models.runner_execution import RunnerExecutionPolicy

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


class DocumentRunOrchestrator:
    """
    Thin facade: sequence existing stage modules for one document run.

    Args:
        preparation: Bundle preparation service for the prepare stage.
        runner_registry: Registry mapping runner ids to PassRunner classes.
        manifest_builder: Assemble-from-run manifest builder (Task 3).
        assemble: Document assemble orchestrator (Task 3).
        bundles: Bundle layout / export writer (Task 3).
        runner_service_factory: Builds one ``RunnerExecutionService`` per
            runner invocation (mirrors CLI ``_invoke_hosted_run``).
        evaluation: Optional evaluation service (Task 3).
        review_cli: Optional review issue collaborator (Task 3).
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
            manifest_builder: Assemble-from-run manifest builder (Task 3).
            assemble: Document assemble orchestrator (Task 3).
            bundles: Bundle layout / export writer (Task 3).
            runner_service_factory: Builds one ``RunnerExecutionService`` per
                runner invocation.
            evaluation: Optional evaluation service (Task 3).
            review_cli: Optional review issue collaborator (Task 3).
            endpoint_ensurer: Optional ensure/overlay callable for endpoints.

        """
        #: Bundle preparation service for the prepare stage.
        self._preparation = preparation
        #: Registry mapping runner ids to PassRunner classes.
        self._runner_registry = runner_registry
        #: Assemble-from-run manifest builder (filled in later stages).
        self._manifest_builder = manifest_builder
        #: Document assemble orchestrator (filled in later stages).
        self._assemble = assemble
        #: Bundle layout / export writer (filled in later stages).
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
            NotImplementedError: When a stage beyond prepare/run is requested.
            ValueError: When relative paths lack ``config_dir``, runner ids
                mismatch references, or ``ensure_endpoints`` lacks an ensurer.

        """
        bundle_root = _resolve_path(config.bundle_root, config_dir=config_dir)
        stages_completed: list[DocumentRunStage] = []
        for stage in config.resolved_stages():
            if stage is DocumentRunStage.PREPARE:
                self._run_prepare(
                    config,
                    bundle_root=bundle_root,
                    config_dir=config_dir,
                )
            elif stage is DocumentRunStage.RUN:
                self._run_runners(
                    config,
                    bundle_root=bundle_root,
                    config_dir=config_dir,
                )
            else:
                msg = f"stage {stage.value!r} is not implemented yet"
                raise NotImplementedError(msg)
            stages_completed.append(stage)
        return DocumentRunResult(
            run_id=config.run_id,
            document_id=config.document_id,
            bundle_root=bundle_root,
            stages_completed=stages_completed,
            document_bundle_path=None,
            export_root=None,
            pending_task_pages=[],
        )

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
