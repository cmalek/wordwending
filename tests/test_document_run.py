# Copyright (C) 2026 Chris Malek.
"""Tests for document run configuration and orchestrator stages."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from wordwending.models.assemble import (
    AssembleManifest,
    AssemblePageRequest,
    RawWitnessRef,
)
from wordwending.models.document_run import (
    DocumentRunConfig,
    DocumentRunnerSpec,
    DocumentRunStage,
)
from wordwending.models.evaluation import MetricProfile  # noqa: TC001
from wordwending.models.merge import MergePolicy  # noqa: TC001
from wordwending.models.ocr import (
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePage,
    CoordinateSpace,
    DocumentBundle,
    EvaluationFamilySummary,
    EvaluationFlag,
    ExportSummary,
    FlagSeverity,
    GoldPageAnnotation,
    InputKind,
    PageClass,
    PageEvaluationSummary,
    PreparationMode,
    PreparedArtifactRef,
    PreparedPage,
    SourceDescriptor,
)
from wordwending.models.preparation import PreparationRecipe, PreparationResult
from wordwending.services.document_run import (
    DocumentRunOrchestrator,
    prepared_artifacts_from_bundle,
)
from wordwending.services.review_cli import ReviewIssueResult

FIXTURE_ROOT = Path(__file__).parent / "fixtures"
DOCUMENT_RUN_FIXTURES = FIXTURE_ROOT / "document_run"
HANDS_OFF_PREP = (
    FIXTURE_ROOT
    / "hands_off"
    / "prepare"
    / "pages"
    / "page-0001"
    / "prepared"
    / "prepared-page-1"
    / "preparation.json"
)
RUNNER_POLICY = FIXTURE_ROOT / "runner" / "olmocr-policy-v1.json"
PREP_RECIPE = FIXTURE_ROOT / "preparation" / "recipe-v1.json"
MINIMAL_BUNDLE = FIXTURE_ROOT / "exports" / "minimal-bundle.json"


def _runner_reference_payload(runner_id: str = "olmocr") -> dict[str, object]:
    return {
        "runner_id": runner_id,
        "runner_version": "0.4.27",
        "model_name": "allenai/olmOCR",
        "model_revision": "model-revision",
        "hardware_class": "nvidia-l40s",
        "runtime_name": "huggingface-endpoint",
        "runtime_revision": "container-digest",
        "config_digest": "sha256:runner-config",
        "prompt_digest": "sha256:prompt",
    }


def _write_runner_files(
    directory: Path, *, runner_id: str = "olmocr"
) -> tuple[Path, Path]:
    """Write RunnerReference + policy JSON; return (ref_path, policy_path)."""
    directory.mkdir(parents=True, exist_ok=True)
    ref_path = directory / f"{runner_id}-ref.json"
    policy_path = directory / f"{runner_id}-policy.json"
    ref_path.write_text(
        json.dumps(_runner_reference_payload(runner_id)), encoding="utf-8"
    )
    policy_path.write_text(RUNNER_POLICY.read_text(encoding="utf-8"), encoding="utf-8")
    return ref_path, policy_path


def _full_page_preparation_json() -> str:
    return HANDS_OFF_PREP.read_text(encoding="utf-8")


def _units_preparation_json() -> str:
    payload = json.loads(_full_page_preparation_json())
    payload["prepared_page"]["preparation_mode"] = "columns"
    payload["prepared_page"]["prepared_units"] = [
        {
            "artifact_id": "artifact-page-0001-column-001",
            "kind": "prepared-unit",
            "page_id": "page-0001",
            "prepared_unit_id": "page-0001-column-001",
            "artifact_path": (
                "pages/page-0001/prepared/prepared-page-1/units/"
                "page-0001-column-001.png"
            ),
            "parent_prepared_page_id": "prepared-page-1",
            "checksum": "sha256:unit-1",
            "order": 1,
            "bounding_box": {
                "x0": 0,
                "y0": 0,
                "x1": 100,
                "y1": 300,
                "coordinate_space_id": "prepared-page-1",
            },
        },
        {
            "artifact_id": "artifact-page-0001-column-002",
            "kind": "prepared-unit",
            "page_id": "page-0001",
            "prepared_unit_id": "page-0001-column-002",
            "artifact_path": (
                "pages/page-0001/prepared/prepared-page-1/units/"
                "page-0001-column-002.png"
            ),
            "parent_prepared_page_id": "prepared-page-1",
            "checksum": "sha256:unit-2",
            "order": 2,
            "bounding_box": {
                "x0": 100,
                "y0": 0,
                "x1": 200,
                "y1": 300,
                "coordinate_space_id": "prepared-page-1",
            },
        },
    ]
    return json.dumps(payload)


def _seed_preparation(
    bundle_root: Path,
    *,
    page_id: str = "page-0001",
    body: str | None = None,
) -> Path:
    """Write preparation.json under the prepare-tree layout."""
    dest = (
        bundle_root
        / "pages"
        / page_id
        / "prepared"
        / "prepared-page-1"
        / "preparation.json"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body or _full_page_preparation_json(), encoding="utf-8")
    return dest


@dataclass
class _FakePreparation:
    """Records prepare calls and seeds preparation.json under output_dir."""

    calls: list[Any] = field(default_factory=list)
    seed_body: str = field(default_factory=_full_page_preparation_json)

    def prepare_bundle(
        self,
        source: Path,
        recipe: PreparationRecipe,
        output_dir: Path,
        **kwargs: object,
    ) -> list[PreparationResult]:
        self.calls.append(("prepare_bundle", source, recipe, output_dir, kwargs))
        _seed_preparation(output_dir, body=self.seed_body)
        return [
            PreparationResult.model_validate_json(self.seed_body),
        ]

    def prepare_variants(
        self,
        source: Path,
        recipes: list[PreparationRecipe],
        output_dir: Path,
        **kwargs: object,
    ) -> list[PreparationResult]:
        self.calls.append(("prepare_variants", source, recipes, output_dir, kwargs))
        _seed_preparation(output_dir, body=self.seed_body)
        return [
            PreparationResult.model_validate_json(self.seed_body),
        ]


@dataclass
class _RecordingRunnerService:
    """Records RunnerExecutionService.run invocations."""

    calls: list[dict[str, object]] = field(default_factory=list)

    def run(  # noqa: PLR0913
        self,
        run_id: str,
        document_id: str,
        artifacts: list[PreparedArtifactRef],
        bundle_root: Path,
        output_dir: Path,
        *,
        force: bool = False,
    ) -> tuple[list[object], object]:
        self.calls.append(
            {
                "run_id": run_id,
                "document_id": document_id,
                "artifacts": artifacts,
                "bundle_root": bundle_root,
                "output_dir": output_dir,
                "force": force,
            }
        )
        return [], object()


@dataclass
class _FakeRegistry:
    """PassRunnerRegistry stand-in returning a sentinel class."""

    resolved: list[str] = field(default_factory=list)

    def resolve(self, runner_id: str) -> type:
        self.resolved.append(runner_id)
        return type(f"FakeRunner_{runner_id}", (), {})


def _minimal_document_bundle(
    *,
    document_id: str = "doc-source-001",
    page_id: str = "page-0001",
) -> DocumentBundle:
    """Return a tiny DocumentBundle for stubbed assemble/export stages."""
    base = DocumentBundle.model_validate_json(
        MINIMAL_BUNDLE.read_text(encoding="utf-8")
    )
    page = base.pages[0].model_copy(update={"page_id": page_id, "page_number": 1})
    return base.model_copy(
        update={
            "document_id": document_id,
            "pages": [page],
            "source": base.source.model_copy(update={"page_count": 1}),
        }
    )


def _seed_assemble_inputs(directory: Path) -> None:
    """Copy provenance, merge policy, gold, and metric fixtures into directory."""
    directory.mkdir(parents=True, exist_ok=True)
    for name in (
        "source.json",
        "bibliographic.json",
        "acquisition.json",
        "merge-policy.json",
        "gold-page-0001.json",
        "metric-profile-v1.json",
    ):
        shutil.copy(DOCUMENT_RUN_FIXTURES / name, directory / name)


@dataclass
class _RecordingManifestBuilder:
    """Records AssembleManifestBuilder.build calls."""

    calls: list[dict[str, object]] = field(default_factory=list)

    def build(  # noqa: PLR0913
        self,
        *,
        bundle_root: Path,
        run_dirs: list[Path],
        source: SourceDescriptor,
        bibliographic: BibliographicProvenance,
        acquisition: AcquisitionProvenance,
        merge_policy: MergePolicy,
    ) -> AssembleManifest:
        self.calls.append(
            {
                "bundle_root": bundle_root,
                "run_dirs": list(run_dirs),
                "source": source,
                "bibliographic": bibliographic,
                "acquisition": acquisition,
                "merge_policy": merge_policy,
            }
        )
        prepared = PreparedPage(
            prepared_page_id="prepared-page-1",
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="prepared/page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
            preparation_recipe_digest="digest-prep-v1",
            coordinate_space=CoordinateSpace(
                space_id="prepared-page-1",
                width_px=200,
                height_px=300,
            ),
        )
        return AssembleManifest(
            source=source,
            bibliographic=bibliographic,
            acquisition=acquisition,
            merge_policy=merge_policy,
            pages=[
                AssemblePageRequest(
                    page_id="page-0001",
                    page_number=1,
                    prepared_page=prepared,
                    raw_witnesses=[
                        RawWitnessRef(
                            witness_id="wit-1",
                            runner_id="olmocr",
                            artifact_paths=["raw/witnesses/stub.json"],
                            coordinate_space=prepared.coordinate_space,
                        )
                    ],
                )
            ],
        )


@dataclass
class _RecordingAssemble:
    """Records assemble_document calls and writes document-bundle.json."""

    calls: list[dict[str, object]] = field(default_factory=list)

    def assemble_document(self, **kwargs: object) -> DocumentBundle:
        self.calls.append(dict(kwargs))
        document_id = kwargs.get("document_id")
        if not isinstance(document_id, str) or not document_id:
            source = kwargs["source"]
            assert isinstance(source, SourceDescriptor)
            document_id = f"doc-{source.source_id}"
        bundle = _minimal_document_bundle(document_id=document_id)
        bundle_root = kwargs["bundle_root"]
        assert isinstance(bundle_root, Path)
        bundle_root.mkdir(parents=True, exist_ok=True)
        (bundle_root / "document-bundle.json").write_text(
            bundle.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
        )
        return bundle


@dataclass
class _RecordingBundles:
    """Records BundleLayoutService write-backs used by eval/export."""

    write_page_graph_calls: list[dict[str, object]] = field(default_factory=list)
    update_document_bundle_page_calls: list[BundlePage] = field(default_factory=list)
    write_document_exports_calls: list[dict[str, object]] = field(default_factory=list)

    def write_page_graph(
        self,
        root: Path,
        page_number: int,
        page: BundlePage,
    ) -> None:
        self.write_page_graph_calls.append(
            {"root": root, "page_number": page_number, "page": page}
        )

    def update_document_bundle_page(self, root: Path, page: BundlePage) -> None:
        self.update_document_bundle_page_calls.append(page)
        bundle_path = root / "document-bundle.json"
        if bundle_path.is_file():
            bundle = DocumentBundle.model_validate_json(
                bundle_path.read_text(encoding="utf-8")
            )
            pages = [
                page if existing.page_id == page.page_id else existing
                for existing in bundle.pages
            ]
            updated = bundle.model_copy(update={"pages": pages})
            bundle_path.write_text(
                updated.model_dump_json(indent=2) + "\n",
                encoding="utf-8",
            )

    def write_document_exports(
        self,
        bundle: DocumentBundle,
        root: Path,
    ) -> DocumentBundle:
        self.write_document_exports_calls.append({"bundle": bundle, "root": root})
        export_root = root / "exports"
        export_root.mkdir(parents=True, exist_ok=True)
        (export_root / "document.md").write_text("export", encoding="utf-8")
        return bundle.model_copy(
            update={
                "exports": ExportSummary(
                    bundle_json_path="exports/bundle.json",
                    rag_jsonl_path="exports/rag.jsonl",
                    stitched_chunks_jsonl_path="exports/stitched_chunks.jsonl",
                    document_markdown_path="exports/document.md",
                )
            }
        )


@dataclass
class _RecordingEvaluation:
    """Records EvaluationService.evaluate_page calls."""

    calls: list[dict[str, object]] = field(default_factory=list)

    def evaluate_page(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> PageEvaluationSummary:
        self.calls.append(
            {"prediction": prediction, "gold": gold, "profile": profile}
        )
        return PageEvaluationSummary(
            text=EvaluationFamilySummary(
                flags=[
                    EvaluationFlag(
                        flag_id="eval-flag-1",
                        flag_type="stub_eval",
                        severity=FlagSeverity.WARNING,
                        message="stub eval flag",
                    )
                ]
            )
        )


@dataclass
class _RecordingReviewCli:
    """Records ReviewCliService.issue calls."""

    calls: list[dict[str, object]] = field(default_factory=list)

    def issue(
        self,
        bundle_root: Path,
        page_id: str,
        *,
        run_id: str | None = None,
    ) -> ReviewIssueResult:
        self.calls.append(
            {"bundle_root": bundle_root, "page_id": page_id, "run_id": run_id}
        )
        return ReviewIssueResult(page_id=page_id, task_count=1)


def _make_orchestrator(  # noqa: PLR0913
    *,
    preparation: _FakePreparation | None = None,
    registry: _FakeRegistry | None = None,
    factory_calls: list[dict[str, object]] | None = None,
    runner_service: _RecordingRunnerService | None = None,
    endpoint_ensurer: Any = None,
    manifest_builder: _RecordingManifestBuilder | None = None,
    assemble: _RecordingAssemble | None = None,
    bundles: _RecordingBundles | None = None,
    evaluation: _RecordingEvaluation | None = None,
    review_cli: _RecordingReviewCli | None = None,
) -> tuple[
    DocumentRunOrchestrator,
    _FakePreparation,
    _RecordingRunnerService,
    list,
    _RecordingManifestBuilder,
    _RecordingAssemble,
    _RecordingBundles,
    _RecordingEvaluation,
    _RecordingReviewCli,
]:
    prep = preparation or _FakePreparation()
    reg = registry or _FakeRegistry()
    service = runner_service or _RecordingRunnerService()
    calls = factory_calls if factory_calls is not None else []
    manifest = manifest_builder or _RecordingManifestBuilder()
    assemble_svc = assemble or _RecordingAssemble()
    bundles_svc = bundles or _RecordingBundles()
    evaluation_svc = evaluation or _RecordingEvaluation()
    review = review_cli or _RecordingReviewCli()

    def factory(**kwargs: object) -> _RecordingRunnerService:
        calls.append(kwargs)
        return service

    orchestrator = DocumentRunOrchestrator(
        preparation=prep,  # type: ignore[arg-type]
        runner_registry=reg,  # type: ignore[arg-type]
        manifest_builder=manifest,  # type: ignore[arg-type]
        assemble=assemble_svc,  # type: ignore[arg-type]
        bundles=bundles_svc,  # type: ignore[arg-type]
        runner_service_factory=factory,  # type: ignore[arg-type]
        evaluation=evaluation_svc,  # type: ignore[arg-type]
        review_cli=review,  # type: ignore[arg-type]
        endpoint_ensurer=endpoint_ensurer,
    )
    return (
        orchestrator,
        prep,
        service,
        calls,
        manifest,
        assemble_svc,
        bundles_svc,
        evaluation_svc,
        review,
    )


def _relative_prepare_run_config(
    config_dir: Path,
    *,
    runners: list[DocumentRunnerSpec] | None = None,
    **overrides: object,
) -> DocumentRunConfig:
    """Build a prepare+run config with paths relative to ``config_dir``."""
    source = config_dir / "sources" / "source.pdf"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(b"%PDF-1.4")
    recipe = config_dir / "recipes" / "recipe.json"
    recipe.parent.mkdir(parents=True, exist_ok=True)
    recipe.write_text(PREP_RECIPE.read_text(encoding="utf-8"), encoding="utf-8")
    if runners is None:
        _write_runner_files(config_dir / "runners")
        runners = [
            DocumentRunnerSpec(
                runner_id="olmocr",
                runner_reference_path="runners/olmocr-ref.json",
                policy_path="runners/olmocr-policy.json",
            )
        ]
    payload: dict[str, object] = {
        "run_id": "run-001",
        "document_id": "doc-source-001",
        "bundle_root": "output/bundle",
        "source_path": "sources/source.pdf",
        "recipe_paths": ["recipes/recipe.json"],
        "source_json": "provenance/source.json",
        "bibliographic_json": "provenance/bib.json",
        "acquisition_json": "provenance/acq.json",
        "merge_policy_path": "policies/merge.json",
        "runners": [spec.model_dump() for spec in runners],
        "stages": [DocumentRunStage.PREPARE, DocumentRunStage.RUN],
    }
    payload.update(overrides)
    return DocumentRunConfig.model_validate(payload)


def _absolute_prepare_run_config(
    tmp_path: Path,
    *,
    runners: list[DocumentRunnerSpec] | None = None,
    **overrides: object,
) -> DocumentRunConfig:
    """Build a prepare+run config with absolute paths under tmp_path."""
    bundle_root = tmp_path / "bundle"
    source = tmp_path / "source.pdf"
    source.write_bytes(b"%PDF-1.4")
    recipe = tmp_path / "recipe.json"
    recipe.write_text(PREP_RECIPE.read_text(encoding="utf-8"), encoding="utf-8")
    if runners is None:
        ref_path, policy_path = _write_runner_files(tmp_path / "runners")
        runners = [
            DocumentRunnerSpec(
                runner_id="olmocr",
                runner_reference_path=str(ref_path),
                policy_path=str(policy_path),
            )
        ]
    payload: dict[str, object] = {
        "run_id": "run-001",
        "document_id": "doc-source-001",
        "bundle_root": str(bundle_root),
        "source_path": str(source),
        "recipe_paths": [str(recipe)],
        "source_json": str(tmp_path / "source.json"),
        "bibliographic_json": str(tmp_path / "bib.json"),
        "acquisition_json": str(tmp_path / "acq.json"),
        "merge_policy_path": str(tmp_path / "merge.json"),
        "runners": [spec.model_dump() for spec in runners],
        "stages": [DocumentRunStage.PREPARE, DocumentRunStage.RUN],
    }
    payload.update(overrides)
    return DocumentRunConfig.model_validate(payload)


def runner_spec() -> DocumentRunnerSpec:
    """Return a minimal runner spec for config validation tests."""
    return DocumentRunnerSpec(
        runner_id="olmocr",
        runner_reference_path="runners/olmocr-ref.json",
        policy_path="runners/olmocr-policy.json",
    )


def valid_config(**overrides: object) -> DocumentRunConfig:
    """Return a minimal valid document run config with optional overrides."""
    payload: dict[str, object] = {
        "run_id": "run-001",
        "document_id": "doc-source-001",
        "bundle_root": "bundles/doc-source-001",
        "source_path": "sources/source.pdf",
        "recipe_paths": ["recipes/default.json"],
        "source_json": "provenance/source.json",
        "bibliographic_json": "provenance/bibliographic.json",
        "acquisition_json": "provenance/acquisition.json",
        "merge_policy_path": "policies/merge.json",
        "runners": [runner_spec().model_dump()],
    }
    payload.update(overrides)
    return DocumentRunConfig.model_validate(payload)


def test_document_run_config_rejects_empty_runners() -> None:
    with pytest.raises(ValidationError, match="runners"):
        valid_config(runners=[])


def test_document_run_config_rejects_empty_recipe_paths() -> None:
    with pytest.raises(ValidationError, match="recipe_paths"):
        valid_config(recipe_paths=[])


def test_document_run_config_rejects_unknown_stage_strings() -> None:
    with pytest.raises(ValidationError, match="stages"):
        valid_config(stages=["prepare", "not-a-stage"])


def test_default_stages_without_gold() -> None:
    config = valid_config()
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
        DocumentRunStage.EXPORT,
    ]


def test_default_stages_with_gold_and_metric_profile() -> None:
    config = valid_config(
        gold_page_paths={"page-001": "gold/page-001.json"},
        metric_profile_path="metrics/default.json",
    )
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.EVAL,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
        DocumentRunStage.EXPORT,
    ]


def test_default_stages_without_eval_when_only_gold_paths() -> None:
    config = valid_config(gold_page_paths={"page-001": "gold/page-001.json"})
    assert DocumentRunStage.EVAL not in config.resolved_stages()


def test_default_stages_without_eval_when_only_metric_profile() -> None:
    config = valid_config(metric_profile_path="metrics/default.json")
    assert DocumentRunStage.EVAL not in config.resolved_stages()


def test_default_stages_skip_export_when_stages_none() -> None:
    config = valid_config(skip_export=True)
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
    ]


def test_explicit_stages_ignore_skip_export() -> None:
    config = valid_config(
        stages=[DocumentRunStage.PREPARE, DocumentRunStage.EXPORT],
        skip_export=True,
    )
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.EXPORT,
    ]


def test_prepared_artifacts_from_bundle_full_page(tmp_path: Path) -> None:
    bundle_root = tmp_path / "bundle"
    _seed_preparation(bundle_root, body=_full_page_preparation_json())
    artifacts = prepared_artifacts_from_bundle(bundle_root)
    assert len(artifacts) == 1
    artifact = artifacts[0]
    assert artifact.kind is InputKind.IMAGE
    assert artifact.page_id == "page-0001"
    assert artifact.artifact_path.endswith("image.png")
    assert artifact.checksum == "sha256:image"
    assert artifact.prepared_unit_id is None


def test_prepared_artifacts_from_bundle_prepared_units(tmp_path: Path) -> None:
    bundle_root = tmp_path / "bundle"
    _seed_preparation(bundle_root, body=_units_preparation_json())
    artifacts = prepared_artifacts_from_bundle(bundle_root)
    assert len(artifacts) == 2
    assert all(a.kind is InputKind.PREPARED_UNIT for a in artifacts)
    assert [a.order for a in artifacts] == [1, 2]
    assert artifacts[0].parent_prepared_page_id == "prepared-page-1"
    assert artifacts[0].checksum == "sha256:unit-1"
    assert artifacts[0].bounding_box is not None


def test_orchestrator_prepare_then_run_sequencing(tmp_path: Path) -> None:
    config = _absolute_prepare_run_config(tmp_path)
    orchestrator, prep, service, factory_calls, *_ = _make_orchestrator()
    result = orchestrator.run(config)

    assert [call[0] for call in prep.calls] == ["prepare_bundle"]
    assert prep.calls[0][3] == Path(config.bundle_root)
    assert len(factory_calls) == 1
    assert len(service.calls) == 1
    run_call = service.calls[0]
    assert run_call["run_id"] == "run-001-olmocr"
    assert run_call["document_id"] == "doc-source-001"
    assert run_call["bundle_root"] == Path(config.bundle_root)
    assert (
        run_call["output_dir"] == Path(config.bundle_root) / "runs" / "run-001-olmocr"
    )
    assert run_call["force"] is False
    artifacts = run_call["artifacts"]
    assert isinstance(artifacts, list)
    assert len(artifacts) == 1
    first = artifacts[0]
    assert isinstance(first, PreparedArtifactRef)
    assert first.kind is InputKind.IMAGE
    assert result.stages_completed == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
    ]
    assert result.bundle_root == Path(config.bundle_root)
    assert result.document_bundle_path is None
    assert result.export_root is None
    assert result.pending_task_pages == []


def test_orchestrator_multi_runner_distinct_execution_dirs(tmp_path: Path) -> None:
    olmocr_ref, olmocr_policy = _write_runner_files(
        tmp_path / "runners", runner_id="olmocr"
    )
    kraken_ref, kraken_policy = _write_runner_files(
        tmp_path / "runners",
        runner_id="kraken",
    )
    config = _absolute_prepare_run_config(
        tmp_path,
        runners=[
            DocumentRunnerSpec(
                runner_id="olmocr",
                runner_reference_path=str(olmocr_ref),
                policy_path=str(olmocr_policy),
            ),
            DocumentRunnerSpec(
                runner_id="kraken",
                runner_reference_path=str(kraken_ref),
                policy_path=str(kraken_policy),
            ),
        ],
    )
    orchestrator, prep, service, factory_calls, *_ = _make_orchestrator()
    orchestrator.run(config)

    assert len(prep.calls) == 1
    assert len(factory_calls) == 2
    assert [call["run_id"] for call in service.calls] == [
        "run-001-olmocr",
        "run-001-kraken",
    ]
    bundle = Path(config.bundle_root)
    assert [call["output_dir"] for call in service.calls] == [
        bundle / "runs" / "run-001-olmocr",
        bundle / "runs" / "run-001-kraken",
    ]


def test_orchestrator_ensure_endpoints_calls_ensurer(tmp_path: Path) -> None:
    config = _absolute_prepare_run_config(tmp_path, ensure_endpoints=True)
    ensured: list[list[str]] = []

    def ensurer(*, runner_ids: list[str]) -> None:
        ensured.append(list(runner_ids))

    orchestrator, _, service, *_ = _make_orchestrator(endpoint_ensurer=ensurer)
    orchestrator.run(config)

    assert ensured == [["olmocr"]]
    assert len(service.calls) == 1


def test_orchestrator_force_rerun_passed_through(tmp_path: Path) -> None:
    config = _absolute_prepare_run_config(tmp_path, force_rerun=True)
    orchestrator, _, service, *_ = _make_orchestrator()
    orchestrator.run(config)
    assert service.calls[0]["force"] is True


def test_orchestrator_multi_recipe_uses_prepare_variants(tmp_path: Path) -> None:
    recipe_a = tmp_path / "recipe-a.json"
    recipe_b = tmp_path / "recipe-b.json"
    recipe_a.write_text(PREP_RECIPE.read_text(encoding="utf-8"), encoding="utf-8")
    recipe_b.write_text(PREP_RECIPE.read_text(encoding="utf-8"), encoding="utf-8")
    config = _absolute_prepare_run_config(
        tmp_path,
        recipe_paths=[str(recipe_a), str(recipe_b)],
    )
    orchestrator, prep, *_ = _make_orchestrator()
    orchestrator.run(config)
    assert [call[0] for call in prep.calls] == ["prepare_variants"]
    assert len(prep.calls[0][2]) == 2


def test_orchestrator_resolves_relative_paths_from_config_dir(
    tmp_path: Path,
) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config = _relative_prepare_run_config(config_dir)
    expected_bundle = (config_dir / "output" / "bundle").resolve()
    expected_source = (config_dir / "sources" / "source.pdf").resolve()
    wrong_source_under_bundle = expected_bundle / "sources" / "source.pdf"

    orchestrator, prep, service, factory_calls, *_ = _make_orchestrator()
    result = orchestrator.run(config, config_dir=config_dir)

    assert [call[0] for call in prep.calls] == ["prepare_bundle"]
    _, source, _recipe, output_dir, _kwargs = prep.calls[0]
    assert source == expected_source
    assert source.is_absolute()
    assert source != wrong_source_under_bundle
    assert output_dir == expected_bundle
    assert len(factory_calls) == 1
    factory_kwargs = factory_calls[0]
    assert factory_kwargs["runner"].runner_id == "olmocr"
    assert factory_kwargs["policy"].policy_id == "olmocr-hf-fixed-v1"
    assert len(service.calls) == 1
    assert result.bundle_root == expected_bundle


def test_orchestrator_runner_id_mismatch_raises(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    ref_path, policy_path = _write_runner_files(
        config_dir / "runners",
        runner_id="kraken",
    )
    config = _relative_prepare_run_config(
        config_dir,
        runners=[
            DocumentRunnerSpec(
                runner_id="olmocr",
                runner_reference_path="runners/kraken-ref.json",
                policy_path="runners/kraken-policy.json",
            )
        ],
    )
    orchestrator, *_ = _make_orchestrator()
    with pytest.raises(ValueError, match="does not match"):
        orchestrator.run(config, config_dir=config_dir)
    assert ref_path.exists()
    assert policy_path.exists()


def test_orchestrator_ensure_endpoints_without_ensurer_raises(
    tmp_path: Path,
) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config = _relative_prepare_run_config(config_dir, ensure_endpoints=True)
    orchestrator, *_ = _make_orchestrator(endpoint_ensurer=None)
    with pytest.raises(ValueError, match="ensure_endpoints requires endpoint_ensurer"):
        orchestrator.run(config, config_dir=config_dir)


def test_orchestrator_full_machine_path_assemble_issue_export(
    tmp_path: Path,
) -> None:
    """Default path without gold: assemble → issue → export with stubbed stages."""
    _seed_assemble_inputs(tmp_path)
    config = _absolute_prepare_run_config(
        tmp_path,
        source_json=str(tmp_path / "source.json"),
        bibliographic_json=str(tmp_path / "bibliographic.json"),
        acquisition_json=str(tmp_path / "acquisition.json"),
        merge_policy_path=str(tmp_path / "merge-policy.json"),
        stages=[
            DocumentRunStage.PREPARE,
            DocumentRunStage.RUN,
            DocumentRunStage.ASSEMBLE,
            DocumentRunStage.ISSUE_REVIEW_TASKS,
            DocumentRunStage.EXPORT,
        ],
    )
    (
        orchestrator,
        prep,
        service,
        _,
        manifest,
        assemble,
        bundles,
        evaluation,
        review,
    ) = _make_orchestrator()
    result = orchestrator.run(config)

    assert [call[0] for call in prep.calls] == ["prepare_bundle"]
    assert len(service.calls) == 1
    assert DocumentRunStage.EVAL not in result.stages_completed
    assert evaluation.calls == []
    assert len(manifest.calls) == 1
    assert manifest.calls[0]["run_dirs"] == [
        Path(config.bundle_root) / "runs" / "run-001-olmocr"
    ]
    assert len(assemble.calls) == 1
    assert assemble.calls[0]["document_id"] == "doc-source-001"
    assert len(review.calls) == 1
    assert review.calls[0]["run_id"] == "run-001"
    assert review.calls[0]["page_id"] == "page-0001"
    assert len(bundles.write_document_exports_calls) == 1
    assert result.stages_completed == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
        DocumentRunStage.EXPORT,
    ]
    assert result.document_bundle_path == Path(config.bundle_root) / "document-bundle.json"
    assert result.export_root == Path(config.bundle_root) / "exports"
    assert result.pending_task_pages == ["page-0001"]


def test_orchestrator_skips_eval_when_no_gold(tmp_path: Path) -> None:
    _seed_assemble_inputs(tmp_path)
    config = _absolute_prepare_run_config(
        tmp_path,
        source_json=str(tmp_path / "source.json"),
        bibliographic_json=str(tmp_path / "bibliographic.json"),
        acquisition_json=str(tmp_path / "acquisition.json"),
        merge_policy_path=str(tmp_path / "merge-policy.json"),
        stages=None,
    )
    assert DocumentRunStage.EVAL not in config.resolved_stages()
    (
        orchestrator,
        _,
        _,
        _,
        _,
        _,
        _,
        evaluation,
        review,
    ) = _make_orchestrator()
    result = orchestrator.run(config)
    assert DocumentRunStage.EVAL not in result.stages_completed
    assert evaluation.calls == []
    assert [call["run_id"] for call in review.calls] == ["run-001"]


def test_orchestrator_eval_before_issue_writes_page_graph(
    tmp_path: Path,
) -> None:
    _seed_assemble_inputs(tmp_path)
    config = _absolute_prepare_run_config(
        tmp_path,
        source_json=str(tmp_path / "source.json"),
        bibliographic_json=str(tmp_path / "bibliographic.json"),
        acquisition_json=str(tmp_path / "acquisition.json"),
        merge_policy_path=str(tmp_path / "merge-policy.json"),
        gold_page_paths={"page-0001": str(tmp_path / "gold-page-0001.json")},
        metric_profile_path=str(tmp_path / "metric-profile-v1.json"),
        stages=[
            DocumentRunStage.ASSEMBLE,
            DocumentRunStage.EVAL,
            DocumentRunStage.ISSUE_REVIEW_TASKS,
        ],
    )
    call_order: list[str] = []

    class _OrderedEvaluation(_RecordingEvaluation):
        def evaluate_page(self, prediction, gold, profile):  # type: ignore[no-untyped-def]
            call_order.append("eval")
            return super().evaluate_page(prediction, gold, profile)

    class _OrderedReview(_RecordingReviewCli):
        def issue(self, bundle_root, page_id, *, run_id=None):  # type: ignore[no-untyped-def]
            call_order.append("issue")
            return super().issue(bundle_root, page_id, run_id=run_id)

    evaluation = _OrderedEvaluation()
    review = _OrderedReview()
    (
        orchestrator,
        _,
        _,
        _,
        _,
        _,
        bundles,
        _,
        _,
    ) = _make_orchestrator(evaluation=evaluation, review_cli=review)
    result = orchestrator.run(config)

    assert call_order == ["eval", "issue"]
    assert len(evaluation.calls) == 1
    assert evaluation.calls[0]["gold"].page_id == "page-0001"
    assert len(bundles.write_page_graph_calls) == 1
    written_page = bundles.write_page_graph_calls[0]["page"]
    assert isinstance(written_page, BundlePage)
    assert written_page.evaluation_summary.text is not None
    assert written_page.evaluation_summary.text.flags
    assert written_page.evaluation_summary.text.flags[0].flag_id == "eval-flag-1"
    assert len(bundles.update_document_bundle_page_calls) == 1
    assert review.calls[0]["run_id"] == "run-001"
    assert result.stages_completed == [
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.EVAL,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
    ]


def test_orchestrator_multi_runner_passes_two_run_dirs_to_manifest(
    tmp_path: Path,
) -> None:
    _seed_assemble_inputs(tmp_path)
    olmocr_ref, olmocr_policy = _write_runner_files(
        tmp_path / "runners", runner_id="olmocr"
    )
    kraken_ref, kraken_policy = _write_runner_files(
        tmp_path / "runners",
        runner_id="kraken",
    )
    config = _absolute_prepare_run_config(
        tmp_path,
        source_json=str(tmp_path / "source.json"),
        bibliographic_json=str(tmp_path / "bibliographic.json"),
        acquisition_json=str(tmp_path / "acquisition.json"),
        merge_policy_path=str(tmp_path / "merge-policy.json"),
        runners=[
            DocumentRunnerSpec(
                runner_id="olmocr",
                runner_reference_path=str(olmocr_ref),
                policy_path=str(olmocr_policy),
            ),
            DocumentRunnerSpec(
                runner_id="kraken",
                runner_reference_path=str(kraken_ref),
                policy_path=str(kraken_policy),
            ),
        ],
        stages=[DocumentRunStage.ASSEMBLE],
    )
    orchestrator, _, _, _, manifest, *_ = _make_orchestrator()
    orchestrator.run(config)
    bundle = Path(config.bundle_root)
    assert manifest.calls[0]["run_dirs"] == [
        bundle / "runs" / "run-001-olmocr",
        bundle / "runs" / "run-001-kraken",
    ]


def test_orchestrator_assemble_passes_config_document_id(tmp_path: Path) -> None:
    _seed_assemble_inputs(tmp_path)
    config = _absolute_prepare_run_config(
        tmp_path,
        document_id="doc-config-authoritative",
        source_json=str(tmp_path / "source.json"),
        bibliographic_json=str(tmp_path / "bibliographic.json"),
        acquisition_json=str(tmp_path / "acquisition.json"),
        merge_policy_path=str(tmp_path / "merge-policy.json"),
        stages=[DocumentRunStage.ASSEMBLE],
    )
    orchestrator, _, _, _, _, assemble, *_ = _make_orchestrator()
    result = orchestrator.run(config)
    assert assemble.calls[0]["document_id"] == "doc-config-authoritative"
    assert result.document_bundle_path == Path(config.bundle_root) / "document-bundle.json"
