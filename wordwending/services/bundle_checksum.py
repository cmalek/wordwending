# Copyright (C) 2026 Chris Malek.
"""Verify recorded bundle-layout checksums against on-disk artifact bytes."""

from __future__ import annotations

import hashlib
from pathlib import Path  # noqa: TC003

from wordwending.models import (
    BundleChecksumReport,
    ChecksumVerificationResult,
    ChecksumVerificationStatus,
    DocumentBundleManifest,
    PreparedArtifactRef,
    PreparedPage,
)
from wordwending.services.bundle_layout import BundleLayoutService


def _sha256_label(payload: bytes) -> str:
    """
    Return the canonical digest label for ``payload``.

    Args:
        payload: Raw artifact bytes.

    Returns:
        ``sha256:<hex>`` digest label.

    """
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _recorded_checksum(value: str | None) -> str | None:
    """
    Normalize optional recorded digest labels.

    Args:
        value: Recorded digest label from bundle metadata.

    Returns:
        Stripped label, or ``None`` when absent or blank.

    """
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class BundleChecksumService:
    """
    Compare bundle-layout recorded digests to on-disk artifact bytes.

    Args:
        layout: Bundle reader used to load manifests and page graphs.

    """

    def __init__(self, *, layout: BundleLayoutService | None = None) -> None:
        """
        Initialize checksum verification collaborators.

        Keyword Args:
            layout: Bundle layout reader; defaults to a fresh service instance.

        """
        #: Bundle layout reader for manifests and page graphs.
        self._layout = layout or BundleLayoutService()

    def verify(self, bundle_root: Path) -> BundleChecksumReport:
        """
        Verify checksums recorded by bundle layout metadata.

        Args:
            bundle_root: Filesystem root for one document bundle tree.

        Returns:
            Per-artifact verification results in stable inspection order.

        """
        document_manifest = self._layout.read_document_manifest(bundle_root)
        results: list[ChecksumVerificationResult] = []
        results.extend(self._verify_source_checksum(bundle_root, document_manifest))
        for page_number in range(1, document_manifest.page_count + 1):
            page_graph = self._layout.read_page_graph(bundle_root, page_number)
            results.extend(
                self._verify_prepared_page(bundle_root, page_graph.prepared_page)
            )
        return BundleChecksumReport(results=results)

    def _verify_source_checksum(
        self,
        bundle_root: Path,
        document_manifest: DocumentBundleManifest,
    ) -> list[ChecksumVerificationResult]:
        """
        Verify the document source digest when recorded on the manifest.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            document_manifest: Parsed document manifest.

        Returns:
            Zero or one verification result for the primary source artifact.

        """
        recorded = _recorded_checksum(document_manifest.source.checksum)
        if recorded is None:
            return []
        artifact_path = f"source/{document_manifest.source.source_label}"
        return [
            self._verify_file(
                bundle_root,
                artifact_path=artifact_path,
                recorded_checksum=recorded,
            )
        ]

    def _verify_prepared_page(
        self,
        bundle_root: Path,
        prepared_page: PreparedPage,
    ) -> list[ChecksumVerificationResult]:
        """
        Verify prepared-page and prepared-unit digests from one page graph.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            prepared_page: Prepared-page metadata from the page graph.

        Returns:
            Verification results for the page image and any prepared units.

        """
        results = [
            self._verify_file(
                bundle_root,
                artifact_path=prepared_page.image_path,
                recorded_checksum=prepared_page.image_checksum,
            )
        ]
        results.extend(
            self._verify_prepared_unit(bundle_root, unit)
            for unit in prepared_page.prepared_units
        )
        return results

    def _verify_prepared_unit(
        self,
        bundle_root: Path,
        unit: PreparedArtifactRef,
    ) -> ChecksumVerificationResult:
        """
        Verify one prepared-unit digest when recorded on the page graph.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            unit: Prepared-unit metadata from the page graph.

        Returns:
            Verification result, including honest skips when no digest exists.

        """
        recorded = _recorded_checksum(unit.checksum)
        if recorded is None:
            return ChecksumVerificationResult(
                artifact_path=unit.artifact_path,
                status=ChecksumVerificationStatus.SKIPPED,
                detail="no recorded checksum",
            )
        return self._verify_file(
            bundle_root,
            artifact_path=unit.artifact_path,
            recorded_checksum=recorded,
        )

    def _verify_file(
        self,
        bundle_root: Path,
        *,
        artifact_path: str,
        recorded_checksum: str,
    ) -> ChecksumVerificationResult:
        """
        Compare one on-disk artifact against a recorded digest label.

        Args:
            bundle_root: Filesystem root for one document bundle tree.

        Keyword Args:
            artifact_path: Bundle-relative artifact path.
            recorded_checksum: Digest label recorded in bundle metadata.

        Returns:
            OK when bytes match; FAIL when missing or mismatched.

        """
        path = bundle_root / artifact_path
        if not path.is_file():
            return ChecksumVerificationResult(
                artifact_path=artifact_path,
                recorded_checksum=recorded_checksum,
                status=ChecksumVerificationStatus.FAIL,
                detail="missing file",
            )
        computed = _sha256_label(path.read_bytes())
        if computed == recorded_checksum:
            return ChecksumVerificationResult(
                artifact_path=artifact_path,
                recorded_checksum=recorded_checksum,
                computed_checksum=computed,
                status=ChecksumVerificationStatus.OK,
            )
        return ChecksumVerificationResult(
            artifact_path=artifact_path,
            recorded_checksum=recorded_checksum,
            computed_checksum=computed,
            status=ChecksumVerificationStatus.FAIL,
            detail="checksum mismatch",
        )
