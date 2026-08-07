# Copyright (C) 2026 Chris Malek.
"""Tests for BakeoffService harness and bakeoff-matrix-v1 schema."""

from __future__ import annotations

from pathlib import Path

import pytest

from wordwending.cli.cli import cli
from wordwending.models import (
    BoundingBox,
    BundlePage,
    CoordinateSpace,
    GoldCoverage,
    GoldPageAnnotation,
    GoldTextSpan,
    LineRecord,
    MetricProfile,
    ObjectProvenance,
    PageClass,
    PageEvaluationSummary,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewDimension,
    SpanRecord,
    WitnessReference,
)
from wordwending.models.bakeoff import (
    BAKEOFF_MATRIX_FILENAME,
    BAKEOFF_MATRIX_SCHEMA_VERSION,
    BakeoffCandidate,
    BakeoffInvocationOutcome,
    BakeoffManifest,
    BakeoffMatrix,
    BakeoffMatrixCell,
    BakeoffPageCase,
    BakeoffRequest,
    default_bakeoff_candidates,
)
from wordwending.services.bakeoff import BakeoffService, RecordedBakeoffInvoker
from wordwending.services.evaluation import EvaluationService

_PROFILE_PATH = Path(__file__).parent / "fixtures/evaluation/metric-profile-v1.json"
_PAGE_ID = "page-1"
_COORDINATE_SPACE_ID = "prepared-page"


def profile() -> MetricProfile:
    """Load the frozen v1 metric profile."""
    return MetricProfile.model_validate_json(_PROFILE_PATH.read_text(encoding="utf-8"))


def _provenance(*, runner_id: str = "olmocr") -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id=_PAGE_ID,
        witness_ids=["wit-1"],
        runner_ids=[runner_id],
    )


def _box(x0: float, y0: float, x1: float, y1: float) -> BoundingBox:
    """Build one axis-aligned box in the fixture prepared-page space."""
    return BoundingBox(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        coordinate_space_id=_COORDINATE_SPACE_ID,
    )


def _prediction(*, text: str, runner_id: str) -> BundlePage:
    """Build one minimal BundlePage prediction for bake-off scoring."""
    provenance = _provenance(runner_id=runner_id)
    return BundlePage(
        page_id=_PAGE_ID,
        page_number=1,
        prepared_page=PreparedPage(
            prepared_page_id="prepared-page-1",
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
            preparation_recipe_digest="digest-prep-v1",
            coordinate_space=CoordinateSpace(
                space_id=_COORDINATE_SPACE_ID,
                width_px=100,
                height_px=100,
            ),
        ),
        witnesses=[
            WitnessReference(
                witness_id="wit-1",
                runner_id=runner_id,
                witness_kind="text",
                artifact_path="witness.json",
                page_id=_PAGE_ID,
            )
        ],
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
                provenance=provenance,
            )
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic=text,
                text_normalized=text,
                bounding_box=_box(0, 0, 40, 10),
                provenance=provenance,
            )
        ],
    )


def _gold(*, reference: str) -> GoldPageAnnotation:
    """Build one gold page annotation matching the prediction span."""
    return GoldPageAnnotation(
        page_id=_PAGE_ID,
        page_number=1,
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:image",
        coverage=[
            GoldCoverage(
                coverage_id="coverage-1",
                dimensions=[ReviewDimension.TEXT],
                target_object_ids=["span-1"],
                exhaustive=True,
            )
        ],
        text_spans=[
            GoldTextSpan(
                annotation_id="gold-span-1",
                target_object_id="span-1",
                text_diplomatic=reference,
            )
        ],
    )


def test_default_candidates_target_olmocr_and_kraken() -> None:
    """Schema defaults name real ADR 0007 candidates, not FakePassRunner."""
    candidates = default_bakeoff_candidates()
    assert [c.runner_id for c in candidates] == ["olmocr", "kraken"]
    for candidate in candidates:
        assert candidate.license_placeholder is not None
        assert candidate.cost_placeholder is not None
        assert candidate.operability_placeholder is not None


def test_matrix_cell_schema_includes_required_fields() -> None:
    """Matrix cells carry runner, page class, scores, latency, failure, license."""
    summary = PageEvaluationSummary()
    cell = BakeoffMatrixCell(
        runner_id="olmocr",
        page_id=_PAGE_ID,
        page_class=PageClass.ORDINARY_PROSE,
        score_families=summary,
        latency_ms=12.5,
        failure=None,
        license_placeholder="TBD",
        cost_placeholder="deferred",
        operability_placeholder="deferred",
    )
    dumped = cell.model_dump()
    assert dumped["runner_id"] == "olmocr"
    assert dumped["page_class"] == PageClass.ORDINARY_PROSE
    assert dumped["score_families"] is not None
    assert dumped["latency_ms"] == 12.5
    assert dumped["failure"] is None
    assert dumped["license_placeholder"] == "TBD"


def test_run_scores_recorded_olmocr_and_kraken_predictions() -> None:
    """Harness scores recorded (mocked) responses for both real candidates."""
    gold = _gold(reference="þæt dream")
    olmocr_page = _prediction(text="þæt dream", runner_id="olmocr")
    kraken_page = _prediction(text="þæt drexm", runner_id="kraken")
    invoker = RecordedBakeoffInvoker(
        {
            ("olmocr", _PAGE_ID): BakeoffInvocationOutcome(
                prediction=olmocr_page,
                latency_ms=10.0,
            ),
            ("kraken", _PAGE_ID): BakeoffInvocationOutcome(
                prediction=kraken_page,
                latency_ms=20.0,
            ),
        }
    )
    service = BakeoffService(evaluation=EvaluationService(), invoker=invoker)
    request = BakeoffRequest(
        candidates=default_bakeoff_candidates(),
        pages=[
            BakeoffPageCase(
                page_id=_PAGE_ID,
                page_class=PageClass.ORDINARY_PROSE,
                gold=gold,
            )
        ],
    )

    matrix = service.run(request, profile())

    assert matrix.schema_version == BAKEOFF_MATRIX_SCHEMA_VERSION
    assert [c.runner_id for c in matrix.candidates] == ["olmocr", "kraken"]
    assert len(matrix.cells) == 2
    by_runner = {cell.runner_id: cell for cell in matrix.cells}
    assert by_runner["olmocr"].failure is None
    assert by_runner["kraken"].failure is None
    assert by_runner["olmocr"].latency_ms == 10.0
    assert by_runner["kraken"].latency_ms == 20.0
    assert by_runner["olmocr"].page_class == PageClass.ORDINARY_PROSE
    assert by_runner["olmocr"].score_families is not None
    assert by_runner["kraken"].score_families is not None
    olmocr_cer = {
        m.metric_id: m for m in by_runner["olmocr"].score_families.text.metrics
    }["character_error_rate"]
    kraken_cer = {
        m.metric_id: m for m in by_runner["kraken"].score_families.text.metrics
    }["character_error_rate"]
    assert olmocr_cer.value == 0
    assert kraken_cer.value > 0
    assert by_runner["olmocr"].license_placeholder is not None
    assert any("cost" in note.lower() for note in matrix.deferred)
    assert any("license" in note.lower() for note in matrix.deferred)
    assert any(
        "held-out" in note.lower() or "corpus" in note.lower()
        for note in matrix.deferred
    )


def test_run_records_failure_without_score_families() -> None:
    """Failed invocations populate failure and omit score families."""
    gold = _gold(reference="hello")
    invoker = RecordedBakeoffInvoker(
        {
            ("olmocr", _PAGE_ID): BakeoffInvocationOutcome(
                failure="endpoint timeout",
                latency_ms=5000.0,
            ),
        }
    )
    service = BakeoffService(evaluation=EvaluationService(), invoker=invoker)
    request = BakeoffRequest(
        candidates=[BakeoffCandidate(runner_id="olmocr", license_placeholder="TBD")],
        pages=[
            BakeoffPageCase(
                page_id=_PAGE_ID,
                page_class=PageClass.NOTE_HEAVY,
                gold=gold,
            )
        ],
    )

    matrix = service.run(request, profile())

    assert len(matrix.cells) == 1
    cell = matrix.cells[0]
    assert cell.failure == "endpoint timeout"
    assert cell.score_families is None
    assert cell.latency_ms == 5000.0
    assert cell.page_class == PageClass.NOTE_HEAVY


def test_write_matrix_writes_bakeoff_matrix_v1_json(tmp_path: Path) -> None:
    """Harness writes bakeoff-matrix-v1.json under the output directory."""
    matrix = BakeoffMatrix(
        candidates=default_bakeoff_candidates(),
        cells=[
            BakeoffMatrixCell(
                runner_id="olmocr",
                page_id=_PAGE_ID,
                page_class=PageClass.ORDINARY_PROSE,
                score_families=PageEvaluationSummary(),
                latency_ms=1.0,
                failure=None,
                license_placeholder="TBD",
            )
        ],
    )
    service = BakeoffService(
        evaluation=EvaluationService(),
        invoker=RecordedBakeoffInvoker({}),
    )

    path = service.write_matrix(matrix, tmp_path)

    assert path == tmp_path / BAKEOFF_MATRIX_FILENAME
    assert path.is_file()
    loaded = BakeoffMatrix.model_validate_json(path.read_text(encoding="utf-8"))
    assert loaded.schema_version == BAKEOFF_MATRIX_SCHEMA_VERSION
    assert loaded.cells[0].runner_id == "olmocr"


def test_fake_invoker_allowed_only_for_harness_plumbing() -> None:
    """Fake invoker exercises plumbing; must not appear as a matrix candidate id."""

    class _FakeInvoker:
        """Test-only double for harness plumbing (not a Phase 5 candidate)."""

        def invoke(self, *, runner_id: str, page_id: str) -> BakeoffInvocationOutcome:
            del runner_id, page_id
            return BakeoffInvocationOutcome(
                prediction=_prediction(text="hello", runner_id="olmocr"),
                latency_ms=1.0,
            )

    service = BakeoffService(evaluation=EvaluationService(), invoker=_FakeInvoker())
    request = BakeoffRequest(
        candidates=default_bakeoff_candidates(),
        pages=[
            BakeoffPageCase(
                page_id=_PAGE_ID,
                page_class=PageClass.ORDINARY_PROSE,
                gold=_gold(reference="hello"),
            )
        ],
    )

    matrix = service.run(request, profile())

    assert {c.runner_id for c in matrix.candidates} == {"olmocr", "kraken"}
    assert "fake" not in {c.runner_id for c in matrix.candidates}
    assert all(cell.failure is None for cell in matrix.cells)


def test_recorded_invoker_from_manifest_paths(tmp_path: Path) -> None:
    """CLI/offline path loads recorded BundlePage JSON via BakeoffManifest."""
    gold = _gold(reference="hello")
    olmocr_path = tmp_path / "olmocr-page.json"
    kraken_path = tmp_path / "kraken-page.json"
    olmocr_path.write_text(
        _prediction(text="hello", runner_id="olmocr").model_dump_json(),
        encoding="utf-8",
    )
    kraken_path.write_text(
        _prediction(text="hallo", runner_id="kraken").model_dump_json(),
        encoding="utf-8",
    )
    gold_path = tmp_path / "gold-page.json"
    gold_path.write_text(gold.model_dump_json(), encoding="utf-8")
    manifest = BakeoffManifest(
        candidates=default_bakeoff_candidates(),
        pages=[
            {
                "page_id": _PAGE_ID,
                "page_class": PageClass.ORDINARY_PROSE,
                "gold_path": gold_path.name,
            }
        ],
        predictions=[
            {
                "runner_id": "olmocr",
                "page_id": _PAGE_ID,
                "prediction_path": olmocr_path.name,
                "latency_ms": 11.0,
            },
            {
                "runner_id": "kraken",
                "page_id": _PAGE_ID,
                "prediction_path": kraken_path.name,
                "latency_ms": 22.0,
            },
        ],
    )
    request, invoker = BakeoffService.load_recorded_manifest(
        manifest, bundle_root=tmp_path
    )
    service = BakeoffService(evaluation=EvaluationService(), invoker=invoker)

    matrix = service.run(request, profile())
    path = service.write_matrix(matrix, tmp_path / "out")

    assert path.name == BAKEOFF_MATRIX_FILENAME
    by_runner = {cell.runner_id: cell for cell in matrix.cells}
    assert by_runner["olmocr"].latency_ms == 11.0
    assert by_runner["kraken"].latency_ms == 22.0
    assert by_runner["olmocr"].failure is None


@pytest.mark.integration
def test_live_hf_bakeoff_requires_integration_marker() -> None:
    """Live HF bake-off stays behind pytest.mark.integration (not default suite)."""
    pytest.skip(
        "live Hugging Face bake-off requires deployed endpoints and credentials"
    )


def test_cli_bakeoff_writes_matrix_and_phase_not_complete(
    runner, tmp_path: Path
) -> None:
    """Thin bakeoff CLI writes matrix JSON and echoes Phase 5 NOT COMPLETE."""
    gold = _gold(reference="hello")
    gold_path = tmp_path / "gold-page.json"
    gold_path.write_text(gold.model_dump_json(), encoding="utf-8")
    olmocr_path = tmp_path / "olmocr-page.json"
    kraken_path = tmp_path / "kraken-page.json"
    olmocr_path.write_text(
        _prediction(text="hello", runner_id="olmocr").model_dump_json(),
        encoding="utf-8",
    )
    kraken_path.write_text(
        _prediction(text="hallo", runner_id="kraken").model_dump_json(),
        encoding="utf-8",
    )
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(_PROFILE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    manifest = BakeoffManifest(
        candidates=default_bakeoff_candidates(),
        pages=[
            {
                "page_id": _PAGE_ID,
                "page_class": PageClass.ORDINARY_PROSE,
                "gold_path": gold_path.name,
            }
        ],
        predictions=[
            {
                "runner_id": "olmocr",
                "page_id": _PAGE_ID,
                "prediction_path": olmocr_path.name,
                "latency_ms": 11.0,
            },
            {
                "runner_id": "kraken",
                "page_id": _PAGE_ID,
                "prediction_path": kraken_path.name,
                "latency_ms": 22.0,
            },
        ],
    )
    manifest_path = tmp_path / "bakeoff-manifest.json"
    manifest_path.write_text(manifest.model_dump_json(), encoding="utf-8")
    output_dir = tmp_path / "out"

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
        ],
    )

    assert result.exit_code == 0, result.output
    assert "phase_5: NOT COMPLETE" in result.output
    matrix_path = output_dir / BAKEOFF_MATRIX_FILENAME
    assert matrix_path.is_file()
    loaded = BakeoffMatrix.model_validate_json(matrix_path.read_text(encoding="utf-8"))
    assert len(loaded.cells) == 2
