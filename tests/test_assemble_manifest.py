# Copyright (C) 2026 Chris Malek.
"""Tests for AssembleManifestBuilder and BundlePage.graph_revision."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from wordwending.models.merge import MergePolicy
from wordwending.models.ocr import (
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePage,
    CoordinateSpace,
    PageClass,
    PreparationMode,
    PreparedPage,
    SourceDescriptor,
)
from wordwending.models.preparation import PreparationResult
from wordwending.services.assemble_manifest import (
    AssembleManifestBuilder,
    _raw_witness_ref,
)

_FIXTURES = Path(__file__).parent / "fixtures" / "hands_off"


def _source() -> SourceDescriptor:
    """Return source descriptor from hands-off fixtures."""
    return SourceDescriptor.model_validate_json(
        (_FIXTURES / "source.json").read_text(encoding="utf-8")
    )


def _bibliographic() -> BibliographicProvenance:
    """Return bibliographic provenance from hands-off fixtures."""
    return BibliographicProvenance.model_validate_json(
        (_FIXTURES / "bibliographic.json").read_text(encoding="utf-8")
    )


def _acquisition() -> AcquisitionProvenance:
    """Return acquisition provenance from hands-off fixtures."""
    return AcquisitionProvenance.model_validate_json(
        (_FIXTURES / "acquisition.json").read_text(encoding="utf-8")
    )


def _merge_policy() -> MergePolicy:
    """Return merge policy from hands-off fixtures."""
    return MergePolicy.model_validate_json(
        (_FIXTURES / "merge-policy.json").read_text(encoding="utf-8")
    )


def _stage_prepare(bundle_root: Path) -> None:
    """Copy prepare-tree fixtures under ``bundle_root``."""
    shutil.copytree(_FIXTURES / "prepare" / "pages", bundle_root / "pages")


def _stage_run(dest: Path, fixture_name: str) -> Path:
    """
    Copy one run fixture tree to ``dest``.

    Returns:
        Destination run directory path.

    """
    shutil.copytree(_FIXTURES / fixture_name, dest)
    return dest


def _load_batch(run_dir: Path) -> tuple[Path, dict]:
    """
    Load the sole batch JSON under ``run_dir/batches``.

    Returns:
        Batch path and parsed JSON dict.

    """
    batch_path = next((run_dir / "batches").glob("*.json"))
    return batch_path, json.loads(batch_path.read_text(encoding="utf-8"))


def _write_batch(batch_path: Path, payload: dict) -> None:
    """Overwrite batch JSON at ``batch_path``."""
    batch_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _build(
    *,
    bundle_root: Path,
    run_dirs: list[Path],
):
    """Invoke AssembleManifestBuilder.build with fixture provenance."""
    return AssembleManifestBuilder().build(
        bundle_root=bundle_root,
        run_dirs=run_dirs,
        source=_source(),
        bibliographic=_bibliographic(),
        acquisition=_acquisition(),
        merge_policy=_merge_policy(),
    )


def test_bundle_page_defaults_graph_revision() -> None:
    """BundlePage carries graph-v0 by default for overlay binding."""
    page = BundlePage(
        page_id="page-1",
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
                space_id="prepared-page-1",
                width_px=100,
                height_px=100,
            ),
        ),
    )
    assert page.graph_revision == "graph-v0"


def test_build_single_run_one_page(tmp_path: Path) -> None:
    """Single succeeded run yields one page with one copied witness."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    run_dir = _stage_run(tmp_path / "run-olmocr", "run-olmocr")

    manifest = _build(bundle_root=bundle_root, run_dirs=[run_dir])

    assert len(manifest.pages) == 1
    page = manifest.pages[0]
    assert page.page_id == "page-0001"
    assert page.page_number == 1
    assert page.prepared_page.prepared_page_id == "prepared-page-1"
    assert len(page.raw_witnesses) == 1
    witness = page.raw_witnesses[0]
    assert witness.witness_id == "wit-olmocr-page-0001"
    assert witness.runner_id == "olmocr"
    assert witness.artifact_paths == [
        "runs/run-olmocr/witnesses/batch-olmocr-1/item-1.json"
    ]
    copied = bundle_root.joinpath(*witness.artifact_paths[0].split("/"))
    assert copied.is_file()
    assert (
        copied.read_bytes()
        == (run_dir / "witnesses" / "batch-olmocr-1" / "item-1.json").read_bytes()
    )


def test_build_two_runs_same_page(tmp_path: Path) -> None:
    """Two runner runs merge into one page with two witnesses."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    olmocr_run = _stage_run(tmp_path / "run-olmocr", "run-olmocr")
    kraken_run = _stage_run(tmp_path / "run-kraken", "run-kraken")

    manifest = _build(
        bundle_root=bundle_root,
        run_dirs=[olmocr_run, kraken_run],
    )

    assert len(manifest.pages) == 1
    page = manifest.pages[0]
    runners = {w.runner_id: w for w in page.raw_witnesses}
    assert set(runners) == {"olmocr", "kraken"}
    assert runners["olmocr"].witness_id == "wit-olmocr-page-0001"
    assert runners["kraken"].witness_id == "wit-kraken-page-0001"
    assert runners["olmocr"].artifact_paths == [
        "runs/run-olmocr/witnesses/batch-olmocr-1/item-1.json"
    ]
    assert runners["kraken"].artifact_paths == [
        "runs/run-kraken/witnesses/batch-kraken-1/item-1.json"
    ]
    for witness in page.raw_witnesses:
        assert bundle_root.joinpath(*witness.artifact_paths[0].split("/")).is_file()


def test_build_missing_batches_errors(tmp_path: Path) -> None:
    """Run directory without batches fails clearly."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    empty_run = tmp_path / "run-empty"
    empty_run.mkdir()
    (empty_run / "batches").mkdir()

    with pytest.raises(ValueError, match="batch"):
        _build(bundle_root=bundle_root, run_dirs=[empty_run])


def test_build_empty_run_dir_among_valid_errors(tmp_path: Path) -> None:
    """Typo/empty run_dir fails even when another run_dir has batches."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    good_run = _stage_run(tmp_path / "run-olmocr", "run-olmocr")
    empty_run = tmp_path / "run-typo"
    empty_run.mkdir()
    (empty_run / "batches").mkdir()

    with pytest.raises(ValueError, match="run_dir"):
        _build(bundle_root=bundle_root, run_dirs=[good_run, empty_run])


def test_build_missing_preparation_errors(tmp_path: Path) -> None:
    """Succeeded batch without preparation.json fails clearly."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    # No prepare tree staged — only the run.
    run_dir = _stage_run(tmp_path / "run-olmocr", "run-olmocr")

    with pytest.raises(ValueError, match="preparation"):
        _build(bundle_root=bundle_root, run_dirs=[run_dir])


def test_build_partial_batch_skips_failed_items(tmp_path: Path) -> None:
    """Partial batch skips failure_item_ids and still ingests survivors."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    run_dir = _stage_run(tmp_path / "run-olmocr", "run-olmocr")
    batch_path, batch = _load_batch(run_dir)
    failed_witness = run_dir / "witnesses" / "batch-olmocr-1" / "item-failed.json"
    failed_witness.write_text('{"failed": true}\n', encoding="utf-8")
    batch["items"].append(
        {
            "item_id": "item-failed",
            "source_page_id": "page-0001",
            "prepared_unit_id": None,
            "artifact_id": "prepared-page-1",
        }
    )
    batch["batch_size"] = 2
    batch["result_status"] = "partial"
    batch["failure_item_ids"] = ["item-failed"]
    batch["output_artifacts"].append(
        {
            "artifact_id": "wit-olmocr-failed",
            "artifact_kind": "text",
            "artifact_path": "witnesses/batch-olmocr-1/item-failed.json",
            "media_type": "application/json",
            "batch_item_ids": ["item-failed"],
        }
    )
    _write_batch(batch_path, batch)

    manifest = _build(bundle_root=bundle_root, run_dirs=[run_dir])

    assert len(manifest.pages) == 1
    page = manifest.pages[0]
    assert len(page.raw_witnesses) == 1
    witness = page.raw_witnesses[0]
    assert witness.witness_id == "wit-olmocr-page-0001"
    assert witness.artifact_paths == [
        "runs/run-olmocr/witnesses/batch-olmocr-1/item-1.json"
    ]
    assert all("item-failed" not in path for path in witness.artifact_paths)


def test_build_unresolvable_artifact_path_errors(tmp_path: Path) -> None:
    """Missing artifact bytes under run_dir raise ValueError."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    run_dir = _stage_run(tmp_path / "run-olmocr", "run-olmocr")
    batch_path, batch = _load_batch(run_dir)
    batch["output_artifacts"][0]["artifact_path"] = "witnesses/missing.json"
    _write_batch(batch_path, batch)

    with pytest.raises(ValueError, match="unresolvable artifact path"):
        _build(bundle_root=bundle_root, run_dirs=[run_dir])


def test_build_unknown_batch_item_id_errors(tmp_path: Path) -> None:
    """output_artifacts.batch_item_ids must resolve to batch.items."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    run_dir = _stage_run(tmp_path / "run-olmocr", "run-olmocr")
    batch_path, batch = _load_batch(run_dir)
    batch["output_artifacts"][0]["batch_item_ids"] = ["item-missing"]
    _write_batch(batch_path, batch)

    with pytest.raises(
        ValueError,
        match="output artifacts must identify submitted batch items",
    ):
        _build(bundle_root=bundle_root, run_dirs=[run_dir])


def test_build_ambiguous_preparation_errors(tmp_path: Path) -> None:
    """Multiple preparation.json under one page fail clearly."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_prepare(bundle_root)
    prepared_root = bundle_root / "pages" / "page-0001" / "prepared"
    alt = prepared_root / "prepared-page-alt"
    alt.mkdir()
    shutil.copy2(
        prepared_root / "prepared-page-1" / "preparation.json",
        alt / "preparation.json",
    )
    run_dir = _stage_run(tmp_path / "run-olmocr", "run-olmocr")

    with pytest.raises(ValueError, match="ambiguous preparation"):
        _build(bundle_root=bundle_root, run_dirs=[run_dir])


def test_raw_witness_ref_zero_artifacts_errors() -> None:
    """Empty artifact group for a page/runner raises zero-witnesses error."""
    preparation = PreparationResult.model_validate_json(
        (
            _FIXTURES
            / "prepare"
            / "pages"
            / "page-0001"
            / "prepared"
            / "prepared-page-1"
            / "preparation.json"
        ).read_text(encoding="utf-8")
    )
    with pytest.raises(ValueError, match="zero witnesses"):
        _raw_witness_ref(
            page_id="page-0001",
            runner_id="olmocr",
            artifacts=[],
            preparation=preparation,
        )
