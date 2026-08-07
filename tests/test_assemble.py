# Copyright (C) 2026 Chris Malek.
"""Tests for assemble models and AssembleOrchestrator (adapt → merge → write)."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from wordwending.models import (
    AcquisitionProvenance,
    BibliographicProvenance,
    CoordinateSpace,
    MergeFlag,
    MergeFlagType,
    MergePageInput,
    MergePageResult,
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

_FIXTURES = Path(__file__).parent / "fixtures" / "assemble"
_FIXTURE = _FIXTURES / "olmocr-chat-completion-v1.json"
_KRAKEN_FIXTURE = _FIXTURES / "kraken-chat-completion-v1.json"


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


def _merge_policy(*, runners: list[str] | None = None) -> MergePolicy:
    """Return a merge policy with optional multi-runner precedence."""
    ordered = runners or ["olmocr"]
    return MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        runner_text_precedence=list(ordered),
        structure_scaffold_runner_ids=[ordered[0]],
    )


def _orchestrator(*, merge: AbstainingMergeService | None = None) -> AssembleOrchestrator:
    """Build AssembleOrchestrator with real assemble collaborators."""
    return AssembleOrchestrator(
        adapter=WitnessAdaptationService(),
        merge=merge or AbstainingMergeService(),
        bundles=BundleLayoutService(),
    )


class _MergeWithExtraFlags:
    """Wrap merge and append synthetic flags for assemble projection tests."""

    def __init__(
        self,
        inner: AbstainingMergeService,
        extra_flags: list[MergeFlag],
    ) -> None:
        self._inner = inner
        self._extra_flags = extra_flags

    def merge_page(
        self,
        page_input: MergePageInput,
        policy: MergePolicy,
    ) -> MergePageResult:
        result = self._inner.merge_page(page_input, policy)
        return result.model_copy(
            update={"flags": [*result.flags, *self._extra_flags]}
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


def _stage_multi_witness_bundle_inputs(bundle_root: Path) -> None:
    """Stage olmOCR + kraken fixtures and prepared image under ``bundle_root``."""
    witnesses_dir = bundle_root / "raw" / "witnesses"
    witnesses_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(_FIXTURE, witnesses_dir / "olmocr-chat-completion-v1.json")
    shutil.copy(_KRAKEN_FIXTURE, witnesses_dir / "kraken-chat-completion-v1.json")
    image_dir = bundle_root / "prepared"
    image_dir.mkdir(parents=True, exist_ok=True)
    (image_dir / "page.png").write_bytes(b"fake-png-bytes")


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


def test_assemble_document_multi_witness_disagreement_persists_flags(
    tmp_path: Path,
) -> None:
    """Multi-witness text disagreement writes non-empty evaluation/flags.json."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_multi_witness_bundle_inputs(bundle_root)
    page = AssemblePageRequest(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        raw_witnesses=[
            RawWitnessRef(
                witness_id="wit-olmocr",
                runner_id="olmocr",
                artifact_paths=["raw/witnesses/olmocr-chat-completion-v1.json"],
                coordinate_space=_coordinate_space(),
            ),
            RawWitnessRef(
                witness_id="wit-kraken",
                runner_id="kraken",
                artifact_paths=["raw/witnesses/kraken-chat-completion-v1.json"],
                coordinate_space=_coordinate_space(),
            ),
        ],
    )

    bundle = _orchestrator().assemble_document(
        bundle_root=bundle_root,
        source=_source(),
        bibliographic=_bibliographic(),
        acquisition=_acquisition(),
        pages=[page],
        merge_policy=_merge_policy(runners=["olmocr", "kraken"]),
    )

    assert len(bundle.pages) == 1
    assert {w.runner_id for w in bundle.pages[0].witnesses} == {"olmocr", "kraken"}
    flags_path = (
        bundle_root / "pages" / "page-0001" / "evaluation" / "flags.json"
    )
    assert flags_path.is_file()
    flags_payload = json.loads(flags_path.read_text(encoding="utf-8"))
    assert flags_payload["flags"]
    assert any(
        flag["flag_type"] == "text_disagreement" for flag in flags_payload["flags"]
    )
    assert any(
        flag.flag_type == "text_disagreement"
        for flag in bundle.pages[0].evaluation_summary.text.flags
    )


def test_assemble_document_projects_non_text_merge_flags(
    tmp_path: Path,
) -> None:
    """Assemble routes typography/structure merge flags into non-text families."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    witness_path, _image_path = _stage_bundle_inputs(bundle_root)
    page = AssemblePageRequest(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        raw_witnesses=[
            RawWitnessRef(
                witness_id="wit-1",
                runner_id="olmocr",
                artifact_paths=[witness_path.relative_to(bundle_root).as_posix()],
                coordinate_space=_coordinate_space(),
            )
        ],
    )
    merge = _MergeWithExtraFlags(
        AbstainingMergeService(),
        extra_flags=[
            MergeFlag(
                flag_id="m-typo",
                flag_type=MergeFlagType.TYPOGRAPHY_CONFLICT,
                target_object_ids=["span-1"],
                message="typography conflict on span-1",
            ),
            MergeFlag(
                flag_id="m-struct",
                flag_type=MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT,
                target_object_ids=["region-1"],
                message="structure conflict on region-1",
            ),
        ],
    )

    bundle = _orchestrator(merge=merge).assemble_document(
        bundle_root=bundle_root,
        source=_source(),
        bibliographic=_bibliographic(),
        acquisition=_acquisition(),
        pages=[page],
        merge_policy=_merge_policy(),
    )

    summary = bundle.pages[0].evaluation_summary
    assert any(
        flag.flag_type == str(MergeFlagType.TYPOGRAPHY_CONFLICT)
        for flag in summary.style.typography.flags
    )
    assert any(
        flag.flag_type == str(MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT)
        for flag in summary.structure.flags
    )


def test_assemble_document_rejects_duplicate_witness_id_across_pages(
    tmp_path: Path,
) -> None:
    """Assemble requires unique witness_id across all pages."""
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
