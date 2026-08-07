# Copyright (C) 2026 Chris Malek.
"""Tests for assemble models and AssembleOrchestrator (adapt → merge → write)."""

from __future__ import annotations

import shutil
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from wordwending.models import (
    AcquisitionProvenance,
    BibliographicProvenance,
    CoordinateSpace,
    MergePolicy,
    PageClass,
    PreparationMode,
    PreparedPage,
    SourceDescriptor,
    SourceType,
)
from wordwending.models.assemble import AssemblePageRequest, RawWitnessRef
from wordwending.services.assemble import AssembleOrchestrator
from wordwending.services.bundle_layout import BundleLayoutService
from wordwending.services.merge import AbstainingMergeService
from wordwending.services.witness_adaptation import WitnessAdaptationService

_FIXTURE = (
    Path(__file__).parent / "fixtures" / "assemble" / "olmocr-chat-completion-v1.json"
)


def _prepared_page(
    *,
    prepared_page_id: str = "prepared-page-1",
    image_path: str = "prepared/page.png",
) -> PreparedPage:
    """Return a minimal prepared page for assemble tests."""
    return PreparedPage(
        prepared_page_id=prepared_page_id,
        preparation_mode=PreparationMode.FULL_PAGE,
        page_class=PageClass.ORDINARY_PROSE,
        image_path=image_path,
        source_artifact_id="source-1",
        image_checksum="sha256:image",
        preparation_recipe_id="prep-v1",
        preparation_recipe_digest="digest-prep-v1",
        coordinate_space=CoordinateSpace(
            space_id=prepared_page_id,
            width_px=200,
            height_px=300,
        ),
    )


def _coordinate_space(*, prepared_page_id: str = "prepared-page-1") -> CoordinateSpace:
    """Return coordinate space matching the test prepared page."""
    return CoordinateSpace(space_id=prepared_page_id, width_px=200, height_px=300)


def _source() -> SourceDescriptor:
    """Return a single-page source descriptor for assemble tests."""
    return SourceDescriptor(
        source_id="src-1",
        source_type=SourceType.SINGLE_IMAGE,
        source_label="page.png",
        original_path="sources/page.png",
        page_count=1,
    )


def _bibliographic() -> BibliographicProvenance:
    """Return bibliographic provenance for assemble tests."""
    return BibliographicProvenance(title="Assemble Sample", authors=["Author"])


def _acquisition() -> AcquisitionProvenance:
    """Return acquisition provenance for assemble tests."""
    return AcquisitionProvenance(
        acquisition_kind="local-scan",
        acquired_from="local",
    )


def _merge_policy() -> MergePolicy:
    """Return a single-witness merge policy for Wave A assemble."""
    return MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        runner_text_precedence=["olmocr"],
        structure_scaffold_runner_ids=["olmocr"],
    )


def _orchestrator() -> AssembleOrchestrator:
    """Build AssembleOrchestrator with real Wave A collaborators."""
    return AssembleOrchestrator(
        adapter=WitnessAdaptationService(),
        merge=AbstainingMergeService(),
        bundles=BundleLayoutService(),
    )


def _stage_bundle_inputs(bundle_root: Path) -> tuple[Path, Path]:
    """
    Stage witness fixture and prepared image under ``bundle_root``.

    Returns:
        ``(witness_path, image_path)`` absolute paths under the bundle root.

    """
    witnesses_dir = bundle_root / "raw" / "witnesses"
    witnesses_dir.mkdir(parents=True, exist_ok=True)
    witness_path = witnesses_dir / "olmocr-chat-completion-v1.json"
    shutil.copy(_FIXTURE, witness_path)

    image_dir = bundle_root / "prepared"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / "page.png"
    image_path.write_bytes(b"fake-png-bytes")
    return witness_path, image_path


def test_raw_witness_ref_paths_are_relative_posix_strings() -> None:
    """RawWitnessRef.artifact_paths are relative posix str, not Path objects."""
    ref = RawWitnessRef(
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
        coordinate_space=_coordinate_space(),
    )
    assert all(isinstance(path, str) for path in ref.artifact_paths)
    assert not any(isinstance(path, Path) for path in ref.artifact_paths)
    dumped = ref.model_dump(mode="json")
    assert dumped["artifact_paths"] == [
        "raw/witnesses/olmocr-chat-completion-v1.json"
    ]


def test_raw_witness_ref_rejects_empty_artifact_paths() -> None:
    """RawWitnessRef requires at least one artifact path."""
    with pytest.raises(ValidationError):
        RawWitnessRef(
            witness_id="wit-1",
            runner_id="olmocr",
            artifact_paths=[],
            coordinate_space=_coordinate_space(),
        )


def test_assemble_document_rejects_multi_witness_page(tmp_path: Path) -> None:
    """Wave A assemble requires exactly one raw witness per page."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_bundle_inputs(bundle_root)
    page = AssemblePageRequest(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        raw_witnesses=[
            RawWitnessRef(
                witness_id="wit-1",
                runner_id="olmocr",
                artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
                coordinate_space=_coordinate_space(),
            ),
            RawWitnessRef(
                witness_id="wit-2",
                runner_id="olmocr",
                artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
                coordinate_space=_coordinate_space(),
            ),
        ],
    )
    with pytest.raises(ValueError, match=r"Wave A assemble requires exactly one"):
        _orchestrator().assemble_document(
            bundle_root=bundle_root,
            source=_source(),
            bibliographic=_bibliographic(),
            acquisition=_acquisition(),
            pages=[page],
            merge_policy=_merge_policy(),
        )


def test_assemble_document_rejects_duplicate_witness_id_across_pages(
    tmp_path: Path,
) -> None:
    """Wave A assemble requires unique witness_id across all pages."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_bundle_inputs(bundle_root)
    pages = [
        AssemblePageRequest(
            page_id="page-0001",
            page_number=1,
            prepared_page=_prepared_page(prepared_page_id="prepared-page-1"),
            raw_witnesses=[
                RawWitnessRef(
                    witness_id="wit-1",
                    runner_id="olmocr",
                    artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
                    coordinate_space=_coordinate_space(prepared_page_id="prepared-page-1"),
                )
            ],
        ),
        AssemblePageRequest(
            page_id="page-0002",
            page_number=2,
            prepared_page=_prepared_page(
                prepared_page_id="prepared-page-2",
                image_path="prepared/page-2.png",
            ),
            raw_witnesses=[
                RawWitnessRef(
                    witness_id="wit-1",
                    runner_id="olmocr",
                    artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
                    coordinate_space=_coordinate_space(prepared_page_id="prepared-page-2"),
                )
            ],
        ),
    ]
    image_dir = bundle_root / "prepared"
    (image_dir / "page-2.png").write_bytes(b"fake-png-bytes-2")

    with pytest.raises(ValueError, match=r"unique witness_id"):
        _orchestrator().assemble_document(
            bundle_root=bundle_root,
            source=SourceDescriptor(
                source_id="src-1",
                source_type=SourceType.SINGLE_IMAGE,
                source_label="pages.png",
                original_path="sources/pages.png",
                page_count=2,
            ),
            bibliographic=_bibliographic(),
            acquisition=_acquisition(),
            pages=pages,
            merge_policy=_merge_policy(),
        )


def test_assemble_document_happy_path_writes_bundle_tree(tmp_path: Path) -> None:
    """One page + olmOCR fixture: adapt → merge → write returns DocumentBundle."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_bundle_inputs(bundle_root)
    page = AssemblePageRequest(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        raw_witnesses=[
            RawWitnessRef(
                witness_id="wit-1",
                runner_id="olmocr",
                artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
                coordinate_space=_coordinate_space(),
            )
        ],
    )

    before = datetime.now(UTC)
    bundle = _orchestrator().assemble_document(
        bundle_root=bundle_root,
        source=_source(),
        bibliographic=_bibliographic(),
        acquisition=_acquisition(),
        pages=[page],
        merge_policy=_merge_policy(),
    )
    after = datetime.now(UTC)

    assert bundle.source == _source()
    assert bundle.bibliographic_provenance == _bibliographic()
    assert bundle.acquisition_provenance == _acquisition()
    assert bundle.bundle_schema_version == bundle.run.bundle_schema_version
    assert before <= bundle.run.run_timestamp_utc <= after
    assert len(bundle.pages) == 1
    assert bundle.pages[0].page_id == "page-0001"
    assert bundle.pages[0].page_number == 1
    assert len(bundle.pages[0].spans) == 2
    assert bundle.pages[0].spans[0].text_diplomatic == "Line one of diplomatic text."
    assert bundle.pages[0].spans[1].text_diplomatic == "Line two of diplomatic text."
    assert any(ref.runner_id == "olmocr" for ref in bundle.run.runner_set)

    assert (bundle_root / "manifest.json").exists()
    assert (bundle_root / "document-bundle.json").exists()
    assert (bundle_root / "pages" / "page-0001" / "graph" / "page_graph.json").exists()
    assert (bundle_root / "pages" / "page-0001" / "manifest.json").exists()
    witness_dir = bundle_root / "pages" / "page-0001" / "witnesses" / "text"
    assert witness_dir.is_dir()
    assert any(witness_dir.iterdir())
    assert (bundle_root / "pages" / "page-0001" / "image" / "page.png").exists()
