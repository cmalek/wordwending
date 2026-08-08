# Copyright (C) 2026 Chris Malek.
"""Build AssembleManifest by scanning prepare/run artifacts."""

from __future__ import annotations

import shutil
from collections import defaultdict
from pathlib import Path

from wordwending.models.assemble import (
    AssembleManifest,
    AssemblePageRequest,
    RawWitnessRef,
)
from wordwending.models.merge import MergePolicy  # noqa: TC001
from wordwending.models.ocr import (
    AcquisitionProvenance,
    BatchResultStatus,
    BibliographicProvenance,
    RunnerExecutionBatch,
    SourceDescriptor,
)
from wordwending.models.preparation import PreparationResult


class AssembleManifestBuilder:
    """
    Build AssembleManifest by scanning prepare/run artifacts.

    Copies witness bytes into ``bundle_root`` under ``runs/<run_id>/``.
    """

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
        """
        Scan run batches and prepare trees into an assemble manifest.

        Keyword Args:
            bundle_root: Destination bundle root receiving copied witnesses and
                owning ``pages/.../preparation.json``.
            run_dirs: One or more runner ``--output-dir`` trees to scan.
            source: Source identity for the assembled document.
            bibliographic: Bibliographic provenance for the document.
            acquisition: Acquisition provenance for the document.
            merge_policy: Merge policy embedded in the manifest.

        Returns:
            Assemble manifest with bundle-root-relative witness paths.

        Raises:
            ValueError: When batches, preparation, or witness artifacts are missing
                or unresolvable.

        Side Effects:
            Copies witness artifact bytes into ``bundle_root/runs/<run_id>/...``.

        """
        page_runner_artifacts: dict[str, dict[str, list[tuple[str, str]]]] = (
            defaultdict(lambda: defaultdict(list))
        )
        for run_dir in run_dirs:
            batches_dir = run_dir / "batches"
            if batches_dir.is_dir():
                batch_paths = sorted(batches_dir.glob("*.json"))
            else:
                batch_paths = []
            if not batch_paths:
                msg = f"no runner batch JSON found under run_dir {run_dir}/batches/"
                raise ValueError(msg)
            for batch_path in batch_paths:
                batch = RunnerExecutionBatch.model_validate_json(
                    batch_path.read_text(encoding="utf-8")
                )
                if batch.result_status is BatchResultStatus.FAILED:
                    continue
                self._ingest_batch(
                    batch=batch,
                    run_dir=run_dir,
                    bundle_root=bundle_root,
                    page_runner_artifacts=page_runner_artifacts,
                )

        if not page_runner_artifacts:
            msg = "no succeeded or partial batches produced page witnesses"
            raise ValueError(msg)

        pages: list[AssemblePageRequest] = []
        for page_id in sorted(page_runner_artifacts):
            preparation = _load_preparation(bundle_root, page_id)
            runner_map = page_runner_artifacts[page_id]
            if not runner_map:
                msg = f"page {page_id} has zero witnesses"
                raise ValueError(msg)
            raw_witnesses = [
                _raw_witness_ref(
                    page_id=page_id,
                    runner_id=runner_id,
                    artifacts=artifacts,
                    preparation=preparation,
                )
                for runner_id, artifacts in sorted(runner_map.items())
            ]
            pages.append(
                AssemblePageRequest(
                    page_id=page_id,
                    page_number=preparation.source_page.page_number,
                    prepared_page=preparation.prepared_page,
                    raw_witnesses=raw_witnesses,
                )
            )
        pages.sort(key=lambda page: (page.page_number, page.page_id))
        return AssembleManifest(
            source=source,
            bibliographic=bibliographic,
            acquisition=acquisition,
            merge_policy=merge_policy,
            pages=pages,
        )

    def _ingest_batch(
        self,
        *,
        batch: RunnerExecutionBatch,
        run_dir: Path,
        bundle_root: Path,
        page_runner_artifacts: dict[str, dict[str, list[tuple[str, str]]]],
    ) -> None:
        """
        Copy usable batch witnesses into ``bundle_root`` and record page refs.

        Keyword Args:
            batch: Succeeded or partial runner execution batch.
            run_dir: Runner output directory containing artifact bytes.
            bundle_root: Assemble destination root for copied witnesses.
            page_runner_artifacts: Accumulator of page → runner → artifact refs.

        Raises:
            ValueError: When an artifact path cannot be resolved under ``run_dir``,
                or when ``batch_item_ids`` reference an unknown ``item_id``.

        Side Effects:
            Copies witness files under ``bundle_root/runs/<run_id>/``.

        """
        items_by_id = {item.item_id: item for item in batch.items}
        failed_ids = set(batch.failure_item_ids)
        runner_id = batch.runner.runner_id
        for artifact in batch.output_artifacts:
            source_path = run_dir / artifact.artifact_path
            if not source_path.is_file():
                msg = (
                    f"unresolvable artifact path {artifact.artifact_path!r} "
                    f"under run_dir {run_dir}"
                )
                raise ValueError(msg)
            dest_rel = Path("runs") / batch.run_id / artifact.artifact_path
            dest_path = bundle_root / dest_rel
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            dest_posix = dest_rel.as_posix()
            for item_id in artifact.batch_item_ids:
                if item_id in failed_ids:
                    continue
                item = items_by_id.get(item_id)
                if item is None:
                    msg = (
                        f"unknown batch_item_id {item_id!r} in output_artifacts "
                        f"for batch {batch.batch_id}"
                    )
                    raise ValueError(msg)
                page_runner_artifacts[item.source_page_id][runner_id].append(
                    (artifact.artifact_id, dest_posix)
                )


def _load_preparation(bundle_root: Path, page_id: str) -> PreparationResult:
    """
    Load the sole ``PreparationResult`` for ``page_id`` under ``bundle_root``.

    Args:
        bundle_root: Bundle root containing prepare-tree pages.
        page_id: Source page identifier to load.

    Returns:
        Validated preparation result for the page.

    Raises:
        ValueError: When preparation.json is missing or ambiguous.

    """
    prepared_root = bundle_root / "pages" / page_id / "prepared"
    if not prepared_root.is_dir():
        msg = f"missing preparation directory for page {page_id}"
        raise ValueError(msg)
    candidates = sorted(prepared_root.glob("*/preparation.json"))
    if not candidates:
        msg = f"missing preparation.json for page {page_id}"
        raise ValueError(msg)
    if len(candidates) > 1:
        msg = (
            f"ambiguous preparation variants for page {page_id}: "
            f"{len(candidates)} preparation.json files"
        )
        raise ValueError(msg)
    return PreparationResult.model_validate_json(
        candidates[0].read_text(encoding="utf-8")
    )


def _raw_witness_ref(
    *,
    page_id: str,
    runner_id: str,
    artifacts: list[tuple[str, str]],
    preparation: PreparationResult,
) -> RawWitnessRef:
    """
    Build one ``RawWitnessRef`` for a page/runner artifact group.

    Keyword Args:
        page_id: Owning page identifier.
        runner_id: Runner that produced the artifacts.
        artifacts: Ordered ``(artifact_id, bundle_root-relative path)`` pairs.
        preparation: Preparation result supplying coordinate space.

    Returns:
        Raw witness reference with posix relative artifact paths.

    Raises:
        ValueError: When the runner produced no artifact paths for the page.

    """
    if not artifacts:
        msg = f"page {page_id} has zero witnesses for runner {runner_id}"
        raise ValueError(msg)
    # Single artifact → use its artifact_id; multiple → "{runner_id}-{page_id}".
    witness_id = artifacts[0][0] if len(artifacts) == 1 else f"{runner_id}-{page_id}"
    return RawWitnessRef(
        witness_id=witness_id,
        runner_id=runner_id,
        artifact_paths=[path for _, path in artifacts],
        coordinate_space=preparation.prepared_page.coordinate_space,
    )
