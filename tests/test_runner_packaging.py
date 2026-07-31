# Copyright (C) 2026 Chris Malek.
"""Tests for runner input packaging."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image

from bochord.models.ocr import (
    BatchItemRef,
    InputKind,
    PackagingStrategy,
    PreparedArtifactRef,
)
from bochord.models.runner_execution import PlannedRunnerBatch
from bochord.services.runner_packaging import RunnerInputPackager

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "runner"
PREPARED_INPUTS_PATH = FIXTURE_ROOT / "prepared-inputs.json"


def fixture_root() -> Path:
    """Return the runner fixture directory."""
    return FIXTURE_ROOT


def _write_test_images(root: Path, artifacts: list[PreparedArtifactRef]) -> None:
    for artifact in artifacts:
        destination = root / artifact.artifact_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (8, 8), color=(128, 64, 32)).save(destination)


def planned_batch(item_count: int, *, batch_id: str = "batch-test") -> PlannedRunnerBatch:
    """Build a planned batch aligned with ``prepared-inputs.json``."""
    payload = json.loads(PREPARED_INPUTS_PATH.read_text())
    artifacts = [
        PreparedArtifactRef.model_validate(entry)
        for entry in payload["artifacts"][:item_count]
    ]
    items = [
        BatchItemRef(
            item_id=f"{batch_id}-item-{index:03d}",
            source_page_id=artifact.page_id,
            prepared_unit_id=artifact.prepared_unit_id,
            artifact_id=artifact.artifact_id,
        )
        for index, artifact in enumerate(artifacts, start=1)
    ]
    return PlannedRunnerBatch(
        batch_id=batch_id,
        items=items,
        artifacts=artifacts,
    )


@pytest.fixture
def bundle_root(tmp_path: Path) -> Path:
    """Create a bundle root with PNG inputs for packaging tests."""
    payload = json.loads(PREPARED_INPUTS_PATH.read_text())
    artifacts = [PreparedArtifactRef.model_validate(entry) for entry in payload["artifacts"]]
    _write_test_images(tmp_path, artifacts)
    return tmp_path


def test_pdf_batch_preserves_item_page_mapping(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    batch = planned_batch(3)
    packaged = RunnerInputPackager().package(
        batch,
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        bundle_root,
        tmp_path,
    )
    assert packaged.kind is InputKind.PDF
    assert packaged.page_numbers == [1, 2, 3]
    assert packaged.batch_item_ids == [item.item_id for item in batch.items]
    assert Path(tmp_path, packaged.artifact_path).exists()
    assert packaged.checksum


def test_direct_packaging_references_original_artifact(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "packaged"
    output_dir.mkdir()
    batch = planned_batch(1)
    packaged = RunnerInputPackager().package(
        batch,
        PackagingStrategy.DIRECT,
        bundle_root,
        output_dir,
    )
    assert packaged.kind is InputKind.PREPARED_UNIT
    assert packaged.artifact_path == batch.artifacts[0].artifact_path
    assert (bundle_root / packaged.artifact_path).exists()
    assert not (output_dir / packaged.artifact_path).exists()
    assert packaged.batch_item_ids == [batch.items[0].item_id]
    assert packaged.page_numbers == [1]


def test_image_to_pdf_writes_runner_input(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    batch = planned_batch(3)
    packaged = RunnerInputPackager().package(
        batch,
        PackagingStrategy.IMAGE_TO_PDF,
        bundle_root,
        tmp_path,
    )
    assert packaged.kind is InputKind.PDF
    assert packaged.artifact_path == f"runner-inputs/{batch.batch_id}.pdf"
    assert Path(tmp_path, packaged.artifact_path).exists()
    assert packaged.checksum.startswith("sha256:")


def test_direct_packaging_rejects_multi_item_batch(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    batch = planned_batch(2)
    with pytest.raises(ValueError, match="one-item"):
        RunnerInputPackager().package(
            batch,
            PackagingStrategy.DIRECT,
            bundle_root,
            tmp_path,
        )
