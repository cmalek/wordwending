# Copyright (C) 2026 Chris Malek.
"""AssembleOrchestrator: adapt raw witnesses → merge → write document bundle."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from wordwending.models import (
    BUNDLE_SCHEMA_VERSION,
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePage,
    DocumentBundle,
    DocumentEvaluationSummary,
    ExportSummary,
    MergePageInput,
    MergePolicy,
    RunMetadata,
    RunnerReference,
    SourceDescriptor,
    WitnessReference,
)
from wordwending.models.assemble import (  # noqa: TC001
    AssemblePageRequest,
    RawWitnessRef,
)
from wordwending.services.bundle_layout import BundleLayoutService  # noqa: TC001
from wordwending.services.merge import AbstainingMergeService  # noqa: TC001
from wordwending.services.witness_adaptation import (  # noqa: TC001
    WitnessAdaptationService,
)

#: Spec 0002 witness family used for olmOCR text artifacts under pages/.
_TEXT_WITNESS_KIND = "text"


class AssembleOrchestrator:
    """
    Sequence adapt → merge → document-bundle write for one assemble pass.

    Args:
        adapter: Converts persisted raw witness artifacts into PassWitnessPage.
        merge: Abstaining merge of adapted witnesses into BundlePage graphs.
        bundles: Spec 0002 document-bundle tree writer.

    """

    def __init__(
        self,
        *,
        adapter: WitnessAdaptationService,
        merge: AbstainingMergeService,
        bundles: BundleLayoutService,
    ) -> None:
        """
        Initialize assemble collaborators.

        Keyword Args:
            adapter: Witness adaptation service (orchestrator owns adapt).
            merge: Abstaining merge service for single-page merge.
            bundles: Bundle layout service for document-bundle write.

        """
        #: Converts persisted raw witness artifacts into PassWitnessPage graphs.
        self._adapter = adapter
        #: Abstaining merge of adapted witnesses into accepted BundlePage graphs.
        self._merge = merge
        #: Spec 0002 document-bundle tree writer.
        self._bundles = bundles

    def assemble_document(  # noqa: PLR0913
        self,
        *,
        bundle_root: Path,
        source: SourceDescriptor,
        bibliographic: BibliographicProvenance,
        acquisition: AcquisitionProvenance,
        pages: list[AssemblePageRequest],
        merge_policy: MergePolicy,
    ) -> DocumentBundle:
        """
        Adapt, merge, and write one document bundle under ``bundle_root``.

        Side Effects:
            Writes Spec 0002 document-bundle tree under ``bundle_root`` via
            ``BundleLayoutService.write_document_bundle``.

        Keyword Args:
            bundle_root: Filesystem root for relative witness/image paths and
                the written bundle tree.
            source: Source identity for the input artifact(s).
            bibliographic: Bibliographic metadata kept with the document.
            acquisition: Acquisition metadata kept with the document.
            pages: Per-page prepared inputs and raw witness refs.
            merge_policy: Versioned merge precedence and thresholds.

        Returns:
            Assembled ``DocumentBundle`` after successful on-disk write.

        Raises:
            ValueError: If any page has more than one raw witness (Wave A
                single-witness only).

        """
        execution = _AssembleExecution(
            adapter=self._adapter,
            merge=self._merge,
            bundle_root=bundle_root,
            merge_policy=merge_policy,
        )
        for page_request in pages:
            execution.assemble_page(page_request)
        bundle = execution.build_document_bundle(
            source=source,
            bibliographic=bibliographic,
            acquisition=acquisition,
        )
        self._bundles.write_document_bundle(
            bundle,
            bundle_root,
            page_images=execution.page_images or None,
            witness_files=execution.witness_files or None,
        )
        return bundle


class _AssembleExecution:
    """
    Per-run mutable assemble state and page loop.

    Args:
        adapter: Witness adaptation service for this assemble run.
        merge: Abstaining merge service for this assemble run.
        bundle_root: Filesystem root for relative path resolution.
        merge_policy: Versioned merge precedence and thresholds.

    """

    def __init__(
        self,
        *,
        adapter: WitnessAdaptationService,
        merge: AbstainingMergeService,
        bundle_root: Path,
        merge_policy: MergePolicy,
    ) -> None:
        """
        Initialize per-run assemble accumulators.

        Keyword Args:
            adapter: Witness adaptation service for this assemble run.
            merge: Abstaining merge service for this assemble run.
            bundle_root: Filesystem root for relative path resolution.
            merge_policy: Versioned merge precedence and thresholds.

        """
        #: Witness adaptation service for this assemble run.
        self._adapter = adapter
        #: Abstaining merge service for this assemble run.
        self._merge = merge
        #: Filesystem root for relative path resolution and write inputs.
        self._bundle_root = bundle_root
        #: Versioned merge precedence and thresholds for this run.
        self._merge_policy = merge_policy
        #: Accepted page graphs accumulated during the run.
        self.bundle_pages: list[BundlePage] = []
        #: Witness artifact paths keyed by witness id for bundle write.
        self.witness_files: dict[str, Path] = {}
        #: Prepared image paths keyed by page id for bundle write.
        self.page_images: dict[str, Path] = {}
        #: Ordered unique runner ids discovered from raw witness refs.
        self.runner_ids: list[str] = []
        #: Preparation recipe id from the first assembled page when present.
        self.preparation_recipe_id: str = "prep-v1"

    def assemble_page(self, page_request: AssemblePageRequest) -> None:
        """
        Adapt, merge, and accumulate one page into run state.

        Args:
            page_request: Prepared page plus raw witness refs for one page.

        Raises:
            ValueError: If the page has more than one raw witness.

        """
        if len(page_request.raw_witnesses) != 1:
            msg = (
                "Wave A assemble requires exactly one raw witness per page; "
                f"page {page_request.page_id!r} has "
                f"{len(page_request.raw_witnesses)}"
            )
            raise ValueError(msg)

        raw_ref = page_request.raw_witnesses[0]
        resolved_paths = [
            _resolve_against_bundle_root(self._bundle_root, path_str)
            for path_str in raw_ref.artifact_paths
        ]
        adapted = self._adapter.adapt_page(
            prepared_page=page_request.prepared_page,
            witness_id=raw_ref.witness_id,
            runner_id=raw_ref.runner_id,
            artifact_paths=[path.as_posix() for path in resolved_paths],
            coordinate_space=raw_ref.coordinate_space,
        )
        merge_result = self._merge.merge_page(
            MergePageInput(
                page_id=page_request.page_id,
                page_number=page_request.page_number,
                prepared_page=page_request.prepared_page,
                witnesses=[adapted],
            ),
            self._merge_policy,
        )
        page = _bundle_ready_page(
            merge_result.page,
            raw_ref=raw_ref,
            resolved_artifact=resolved_paths[0],
        )
        if not self.bundle_pages:
            self.preparation_recipe_id = (
                page_request.prepared_page.preparation_recipe_id
            )
        self.bundle_pages.append(page)
        self.witness_files[raw_ref.witness_id] = resolved_paths[0]
        if raw_ref.runner_id not in self.runner_ids:
            self.runner_ids.append(raw_ref.runner_id)
        image_path = _resolve_prepared_image(
            self._bundle_root,
            page_request.prepared_page.image_path,
        )
        if image_path is not None:
            self.page_images[page_request.page_id] = image_path

    def build_document_bundle(
        self,
        *,
        source: SourceDescriptor,
        bibliographic: BibliographicProvenance,
        acquisition: AcquisitionProvenance,
    ) -> DocumentBundle:
        """
        Build the in-memory document bundle from accumulated page results.

        Keyword Args:
            source: Source identity for the input artifact(s).
            bibliographic: Bibliographic metadata kept with the document.
            acquisition: Acquisition metadata kept with the document.

        Returns:
            Document bundle with coherent schema versions and runner set.

        """
        schema_version = BUNDLE_SCHEMA_VERSION
        return DocumentBundle(
            document_id=f"doc-{source.source_id}",
            bundle_schema_version=schema_version,
            source=source,
            bibliographic_provenance=bibliographic,
            acquisition_provenance=acquisition,
            run=RunMetadata(
                run_id=f"run-assemble-{source.source_id}",
                run_timestamp_utc=datetime.now(UTC),
                preparation_recipe_id=self.preparation_recipe_id,
                config_digest=(
                    "sha256:assemble:"
                    f"{self._merge_policy.policy_id}:{self._merge_policy.version}"
                ),
                runner_set=[
                    RunnerReference(runner_id=runner_id)
                    for runner_id in self.runner_ids
                ],
                bundle_schema_version=schema_version,
            ),
            pages=self.bundle_pages,
            evaluation_summary=DocumentEvaluationSummary(),
            exports=ExportSummary(bundle_json_path="exports/bundle.json"),
        )


def _resolve_against_bundle_root(bundle_root: Path, path_str: str) -> Path:
    """
    Resolve one path string against ``bundle_root`` when relative.

    Args:
        bundle_root: Assemble bundle root used as the relative base.
        path_str: Absolute or bundle-relative posix path string.

    Returns:
        Absolute filesystem path for reading the artifact.

    """
    path = Path(path_str)
    if path.is_absolute():
        return path
    return (bundle_root / path).resolve()


def _resolve_prepared_image(bundle_root: Path, image_path: str) -> Path | None:
    """
    Resolve a prepared page image path when the file exists.

    Args:
        bundle_root: Assemble bundle root used as the relative base.
        image_path: Prepared image path from ``PreparedPage.image_path``.

    Returns:
        Resolved path when the file exists; otherwise ``None``.

    """
    if not image_path:
        return None
    resolved = _resolve_against_bundle_root(bundle_root, image_path)
    if resolved.is_file():
        return resolved
    return None


def _bundle_ready_page(
    page: BundlePage,
    *,
    raw_ref: RawWitnessRef,
    resolved_artifact: Path,
) -> BundlePage:
    """
    Rewrite merge witnesses to Spec 0002 text-family references for write.

    Merge emits ``witness_kind=pass-witness``; bundle layout requires a Spec
    0002 family (``text`` / ``layout`` / ``style`` / ``table``).

    Args:
        page: Accepted page graph from merge.

    Keyword Args:
        raw_ref: Raw witness ref that produced the adapted pass witness.
        resolved_artifact: Resolved filesystem path of the primary artifact.

    Returns:
        Bundle page with ``witness_kind=text`` and basename artifact paths.

    """
    rewritten: list[WitnessReference] = []
    for witness in page.witnesses:
        if witness.witness_id == raw_ref.witness_id:
            rewritten.append(
                witness.model_copy(
                    update={
                        "witness_kind": _TEXT_WITNESS_KIND,
                        "artifact_path": resolved_artifact.name,
                        "runner_id": raw_ref.runner_id,
                    }
                )
            )
        else:
            rewritten.append(
                witness.model_copy(update={"witness_kind": _TEXT_WITNESS_KIND})
            )
    return page.model_copy(update={"witnesses": rewritten})
