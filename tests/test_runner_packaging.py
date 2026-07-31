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
from tests.test_runner_batching import artifacts as batching_artifacts

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "runner"
PREPARED_INPUTS_PATH = FIXTURE_ROOT / "prepared-inputs.json"


def _write_test_images(root: Path, artifacts: list[PreparedArtifactRef]) -> None:
    for artifact in artifacts:
        destination = root / artifact.artifact_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (8, 8), color=(128, 64, 32)).save(destination)


def planned_batch(
    item_count: int,
    *,
    batch_id: str = "batch-test",
    orders: list[int] | None = None,
) -> PlannedRunnerBatch:
    """Build a planned batch aligned with ``prepared-inputs.json``."""
    payload = json.loads(PREPARED_INPUTS_PATH.read_text())
    fixture_artifacts = [
        PreparedArtifactRef.model_validate(entry) for entry in payload["artifacts"]
    ]
    if item_count <= len(fixture_artifacts):
        artifacts = fixture_artifacts[:item_count]
    else:
        artifacts = batching_artifacts(item_count)
    if orders is not None:
        if len(orders) != item_count:
            msg = "orders length must match item_count"
            raise ValueError(msg)
        artifacts = [
            artifact.model_copy(update={"order": order})
            for artifact, order in zip(artifacts, orders, strict=True)
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
    _write_test_images(tmp_path, batching_artifacts(8))
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


def test_pdf_packaging_raises_when_source_image_missing(tmp_path: Path) -> None:
    batch = planned_batch(3)
    with pytest.raises(FileNotFoundError, match="missing prepared artifact"):
        RunnerInputPackager().package(
            batch,
            PackagingStrategy.UNIT_TO_PDF_BATCH,
            tmp_path,
            tmp_path / "output",
        )


def test_pdf_packaging_uses_positional_page_numbers_not_source_order(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    batch = planned_batch(4, orders=[5, 6, 7, 8])
    packaged = RunnerInputPackager().package(
        batch,
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        bundle_root,
        tmp_path,
    )
    assert packaged.page_numbers == [1, 2, 3, 4]
    assert packaged.batch_item_ids == [item.item_id for item in batch.items]


def test_retry_packaging_uses_page_one_for_single_failed_item(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    batch = planned_batch(1, batch_id="batch-retry", orders=[8])
    packaged = RunnerInputPackager().package(
        batch,
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        bundle_root,
        tmp_path,
    )
    assert packaged.page_numbers == [1]
    assert len(packaged.batch_item_ids) == 1


def test_retry_packaging_for_non_first_failed_item_uses_page_one(
    bundle_root: Path,
    tmp_path: Path,
) -> None:
    original = planned_batch(4, batch_id="batch-original", orders=[5, 6, 7, 8])
    failed_index = 2
    retry_batch = PlannedRunnerBatch(
        batch_id="batch-retry",
        items=[original.items[failed_index]],
        artifacts=[original.artifacts[failed_index]],
    )
    packaged = RunnerInputPackager().package(
        retry_batch,
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        bundle_root,
        tmp_path,
    )
    assert packaged.page_numbers == [1]
    assert packaged.batch_item_ids == [original.items[failed_index].item_id]
