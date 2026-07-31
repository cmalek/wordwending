# Copyright (C) 2026 Chris Malek.
"""Package planned runner batches into hosted-input artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

from bochord.models.ocr import InputKind, PackagingStrategy
from bochord.models.runner_execution import PackagedRunnerInput, PlannedRunnerBatch


def _sha256_label(payload: bytes) -> str:
    """
    Return the canonical checksum label for ``payload``.

    Args:
        payload: Raw artifact bytes.

    Returns:
        ``sha256:<hex>`` digest label.

    """
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _page_numbers(batch: PlannedRunnerBatch) -> list[int]:
    """
    Derive one page number per batch item from artifact order metadata.

    Args:
        batch: Planned batch whose artifacts supply reading-order positions.

    Returns:
        One-based page numbers aligned with batch items.

    Raises:
        ValueError: If an artifact lacks ``order`` metadata.

    """
    page_numbers: list[int] = []
    for index, artifact in enumerate(batch.artifacts, start=1):
        if artifact.order is None:
            msg = f"artifact {artifact.artifact_id} is missing order metadata"
            raise ValueError(msg)
        page_numbers.append(artifact.order if artifact.order >= 1 else index)
    return page_numbers


def _write_pdf(images: list[Image.Image], destination: Path) -> None:
    """
    Persist ``images`` as one multi-page PDF at ``destination``.

    Args:
        images: Open Pillow images converted to RGB.
        destination: Final PDF output path.

    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = destination.with_suffix(destination.suffix + ".tmp")
    try:
        images[0].save(
            temp_path,
            "PDF",
            save_all=True,
            append_images=images[1:],
            resolution=300.0,
        )
        temp_path.replace(destination)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


class RunnerInputPackager:
    """Package one planned batch into a hosted-runner input artifact."""

    def package(
        self,
        batch: PlannedRunnerBatch,
        strategy: PackagingStrategy,
        bundle_root: Path,
        output_dir: Path,
    ) -> PackagedRunnerInput:
        """
        Package one batch using the requested strategy.

        Args:
            batch: Planned batch whose artifacts will be packaged.
            strategy: Packaging policy to apply.
            bundle_root: Bundle root containing source artifact bytes.
            output_dir: Directory where packaged runner inputs are written.

        Returns:
            Packaged runner input metadata and digest.

        Raises:
            ValueError: If direct packaging receives a multi-item batch.
            FileNotFoundError: If a source artifact path is missing.

        """
        if strategy is PackagingStrategy.DIRECT:
            return self._package_direct(batch)
        return self._package_pdf(batch, strategy, bundle_root, output_dir)

    def _package_direct(self, batch: PlannedRunnerBatch) -> PackagedRunnerInput:
        """
        Reference one prepared artifact without copying bytes.

        Args:
            batch: Single-item planned batch.

        Returns:
            Direct packaged runner input metadata.

        Raises:
            ValueError: If the batch contains more than one item.

        """
        if len(batch.items) != 1:
            msg = "direct packaging requires a one-item batch"
            raise ValueError(msg)
        artifact = batch.artifacts[0]
        item = batch.items[0]
        checksum = artifact.checksum or ""
        return PackagedRunnerInput(
            artifact_id=f"pkg-{batch.batch_id}",
            artifact_path=artifact.artifact_path,
            checksum=checksum,
            kind=artifact.kind,
            batch_item_ids=[item.item_id],
            page_numbers=_page_numbers(batch),
        )

    def _package_pdf(
        self,
        batch: PlannedRunnerBatch,
        strategy: PackagingStrategy,
        bundle_root: Path,
        output_dir: Path,
    ) -> PackagedRunnerInput:
        """
        Combine prepared images into one PDF runner input.

        Args:
            batch: Planned batch whose artifacts will be merged.
            strategy: PDF packaging strategy (image or unit batch).
            bundle_root: Bundle root containing source artifact bytes.
            output_dir: Directory where the PDF will be written.

        Returns:
            Packaged PDF runner input metadata and digest.

        """
        _ = strategy
        rel_path = Path("runner-inputs") / f"{batch.batch_id}.pdf"
        destination = output_dir / rel_path
        source_paths = [
            bundle_root / artifact.artifact_path for artifact in batch.artifacts
        ]
        for source_path in source_paths:
            if not source_path.is_file():
                msg = f"missing prepared artifact at {source_path}"
                raise FileNotFoundError(msg)

        images = [Image.open(path).convert("RGB") for path in source_paths]
        try:
            _write_pdf(images, destination)
        finally:
            for image in images:
                image.close()

        checksum = _sha256_label(destination.read_bytes())
        return PackagedRunnerInput(
            artifact_id=f"pkg-{batch.batch_id}",
            artifact_path=rel_path.as_posix(),
            checksum=checksum,
            kind=InputKind.PDF,
            batch_item_ids=[item.item_id for item in batch.items],
            page_numbers=_page_numbers(batch),
        )
