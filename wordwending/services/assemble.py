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
    PassWitnessPage,
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
from wordwending.services.merge_review import MergeFlagReviewService
from wordwending.services.witness_adaptation import (  # noqa: TC001
    WitnessAdaptationService,
)

#: Spec 0002 witness family used for olmOCR text artifacts under pages/.
_TEXT_WITNESS_KIND = "text"
#: Stable relative path for loadable DocumentBundle JSON at bundle root.
DOCUMENT_BUNDLE_JSON = "document-bundle.json"


class AssembleOrchestrator:
    """
    Sequence adapt → merge → document-bundle write for one assemble pass.

    Multi-witness pages are supported. Merge flags from ``MergePageResult``
    are projected into the matching ``BundlePage.evaluation_summary`` families
    (via ``MergeFlagReviewService``) so Spec 0002 ``evaluation/flags.json``
    remains the inspectable sidecar and Spec 0005 review packets can be built
    without a second flag schema.

    Args:
        adapter: Converts persisted raw witness artifacts into PassWitnessPage.
        merge: Abstaining merge of adapted witnesses into BundlePage graphs.
        bundles: Spec 0002 document-bundle tree writer.
        merge_flag_review: Projects merge flags into evaluation families and
            Spec 0005 review packets; defaults to a fresh service instance.

    """

    def __init__(
        self,
        *,
        adapter: WitnessAdaptationService,
        merge: AbstainingMergeService,
        bundles: BundleLayoutService,
        merge_flag_review: MergeFlagReviewService | None = None,
    ) -> None:
        """
        Initialize assemble collaborators.

        Keyword Args:
            adapter: Witness adaptation service (orchestrator owns adapt).
            merge: Abstaining merge service for single-page merge.
            bundles: Bundle layout service for document-bundle write.
            merge_flag_review: Merge-flag projection service; constructed when
                omitted.

        """
        #: Converts persisted raw witness artifacts into PassWitnessPage graphs.
        self._adapter = adapter
        #: Abstaining merge of adapted witnesses into accepted BundlePage graphs.
        self._merge = merge
        #: Spec 0002 document-bundle tree writer.
        self._bundles = bundles
        #: Projects Spec 0009 merge flags into evaluation families / Spec 0005 tasks.
        self._merge_flag_review = merge_flag_review or MergeFlagReviewService()

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
            ``BundleLayoutService.write_document_bundle``, and writes loadable
            ``DocumentBundle`` JSON at ``document-bundle.json`` under
            ``bundle_root``.

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
            ValueError: If any page has no raw witnesses, or if the same
                ``witness_id`` appears on more than one page.
            ValueError: Propagated from witness adaptation when artifact paths
                are empty or the payload is not a supported chat.completion
                format.
            FileNotFoundError: Propagated from witness adaptation when a
                resolved artifact path does not exist.

        """
        execution = _AssembleExecution(
            adapter=self._adapter,
            merge=self._merge,
            merge_flag_review=self._merge_flag_review,
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
        bundle_json_path = bundle_root / DOCUMENT_BUNDLE_JSON
        bundle_json_path.write_text(
            bundle.model_dump_json(indent=2),
            encoding="utf-8",
        )
        return bundle


class _AssembleExecution:
    """
    Per-run mutable assemble state and page loop.

    Args:
        adapter: Witness adaptation service for this assemble run.
        merge: Abstaining merge service for this assemble run.
        merge_flag_review: Merge-flag projection service for this run.
        bundle_root: Filesystem root for relative path resolution.
        merge_policy: Versioned merge precedence and thresholds.

    """

    def __init__(
        self,
        *,
        adapter: WitnessAdaptationService,
        merge: AbstainingMergeService,
        merge_flag_review: MergeFlagReviewService,
        bundle_root: Path,
        merge_policy: MergePolicy,
    ) -> None:
        """
        Initialize per-run assemble accumulators.

        Keyword Args:
            adapter: Witness adaptation service for this assemble run.
            merge: Abstaining merge service for this assemble run.
            merge_flag_review: Merge-flag projection service for this run.
            bundle_root: Filesystem root for relative path resolution.
            merge_policy: Versioned merge precedence and thresholds.

        """
        #: Witness adaptation service for this assemble run.
        self._adapter = adapter
        #: Abstaining merge service for this assemble run.
        self._merge = merge
        #: Merge-flag projection service for this assemble run.
        self._merge_flag_review = merge_flag_review
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
            ValueError: If the page has no raw witnesses, if ``witness_id`` was
                already used on a prior page, or if witness adaptation rejects
                the artifact.
            FileNotFoundError: If a resolved witness artifact path does not
                exist.

        """
        if not page_request.raw_witnesses:
            msg = (
                "Assemble requires at least one raw witness per page; "
                f"page {page_request.page_id!r} has 0"
            )
            raise ValueError(msg)

        adapted, resolved_by_id, raw_refs_by_id = self._adapt_page_witnesses(
            page_request
        )
        merge_result = self._merge.merge_page(
            MergePageInput(
                page_id=page_request.page_id,
                page_number=page_request.page_number,
                prepared_page=page_request.prepared_page,
                witnesses=adapted,
            ),
            self._merge_policy,
        )
        page = _bundle_ready_page(
            merge_result.page,
            raw_refs_by_id=raw_refs_by_id,
            resolved_artifacts=resolved_by_id,
        )
        page = self._merge_flag_review.project_onto_page(page, merge_result.flags)
        self._accumulate_page(
            page_request=page_request,
            page=page,
            resolved_by_id=resolved_by_id,
            raw_refs_by_id=raw_refs_by_id,
        )

    def _adapt_page_witnesses(
        self,
        page_request: AssemblePageRequest,
    ) -> tuple[list[PassWitnessPage], dict[str, Path], dict[str, RawWitnessRef]]:
        """
        Adapt every raw witness on one page with unique-id checks.

        Args:
            page_request: Prepared page plus raw witness refs.

        Returns:
            Adapted witnesses, resolved primary artifact paths, and raw refs
            keyed by ``witness_id``.

        Raises:
            ValueError: If a ``witness_id`` collides within or across pages.
            FileNotFoundError: If a resolved witness artifact path does not
                exist.

        """
        adapted_witnesses: list[PassWitnessPage] = []
        resolved_by_witness_id: dict[str, Path] = {}
        raw_refs_by_id: dict[str, RawWitnessRef] = {}
        for raw_ref in page_request.raw_witnesses:
            self._assert_unique_witness_id(
                page_id=page_request.page_id,
                witness_id=raw_ref.witness_id,
                seen_on_page=resolved_by_witness_id,
            )
            resolved_paths = [
                _resolve_against_bundle_root(self._bundle_root, path_str)
                for path_str in raw_ref.artifact_paths
            ]
            adapted_witnesses.append(
                self._adapter.adapt_page(
                    prepared_page=page_request.prepared_page,
                    witness_id=raw_ref.witness_id,
                    runner_id=raw_ref.runner_id,
                    artifact_paths=[path.as_posix() for path in resolved_paths],
                    coordinate_space=raw_ref.coordinate_space,
                )
            )
            resolved_by_witness_id[raw_ref.witness_id] = resolved_paths[0]
            raw_refs_by_id[raw_ref.witness_id] = raw_ref
        return adapted_witnesses, resolved_by_witness_id, raw_refs_by_id

    def _assert_unique_witness_id(
        self,
        *,
        page_id: str,
        witness_id: str,
        seen_on_page: dict[str, Path],
    ) -> None:
        """
        Reject duplicate ``witness_id`` within a page or across pages.

        Keyword Args:
            page_id: Page being assembled (for error context).
            witness_id: Candidate witness identifier.
            seen_on_page: Witness ids already resolved on this page.

        Raises:
            ValueError: If ``witness_id`` was already used.

        """
        if witness_id in self.witness_files:
            msg = (
                "Assemble requires unique witness_id across pages; "
                f"witness_id {witness_id!r} already used"
            )
            raise ValueError(msg)
        if witness_id in seen_on_page:
            msg = (
                "Assemble requires unique witness_id within a page; "
                f"witness_id {witness_id!r} duplicated on page {page_id!r}"
            )
            raise ValueError(msg)

    def _accumulate_page(
        self,
        *,
        page_request: AssemblePageRequest,
        page: BundlePage,
        resolved_by_id: dict[str, Path],
        raw_refs_by_id: dict[str, RawWitnessRef],
    ) -> None:
        """
        Record one merged page and its witness/image paths into run state.

        Keyword Args:
            page_request: Original assemble page request.
            page: Bundle-ready page graph with persisted merge flags.
            resolved_by_id: Resolved primary artifact paths by witness id.
            raw_refs_by_id: Raw witness refs by witness id.

        """
        if not self.bundle_pages:
            self.preparation_recipe_id = (
                page_request.prepared_page.preparation_recipe_id
            )
        self.bundle_pages.append(page)
        for witness_id, resolved_path in resolved_by_id.items():
            self.witness_files[witness_id] = resolved_path
            runner_id = raw_refs_by_id[witness_id].runner_id
            if runner_id not in self.runner_ids:
                self.runner_ids.append(runner_id)
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
    raw_refs_by_id: dict[str, RawWitnessRef],
    resolved_artifacts: dict[str, Path],
) -> BundlePage:
    """
    Rewrite merge witnesses to Spec 0002 text-family references for write.

    Merge emits ``witness_kind=pass-witness``; bundle layout requires a Spec
    0002 family (``text`` / ``layout`` / ``style`` / ``table``).

    Args:
        page: Accepted page graph from merge.

    Keyword Args:
        raw_refs_by_id: Raw witness refs keyed by ``witness_id``.
        resolved_artifacts: Resolved primary artifact paths keyed by
            ``witness_id``.

    Returns:
        Bundle page with ``witness_kind=text`` and basename artifact paths.

    """
    rewritten: list[WitnessReference] = []
    for witness in page.witnesses:
        raw_ref = raw_refs_by_id.get(witness.witness_id)
        resolved_artifact = resolved_artifacts.get(witness.witness_id)
        if raw_ref is not None and resolved_artifact is not None:
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
