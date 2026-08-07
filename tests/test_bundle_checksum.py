# Copyright (C) 2026 Chris Malek.
"""Tests for bundle checksum verification during inspect-bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tests.test_bundle_layout import (
    _write_minimal_inputs,
    load_minimal_bundle,
)
from wordwending.models import (
    ChecksumVerificationStatus,
    InputKind,
    PreparedArtifactRef,
    SourceDescriptor,
    SourceType,
)
from wordwending.services.bundle_checksum import BundleChecksumService
from wordwending.services.bundle_layout import BundleLayoutService


def _sha256_label(payload: bytes) -> str:
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _write_bundle_with_matching_checksums(tmp_path: Path) -> Path:
    """Materialize a minimal bundle whose recorded digests match on-disk bytes."""
    prepared_bytes = b"fake-prepared-bytes"
    source_pdf_bytes = b"%PDF-1.4 minimal"
    bundle = load_minimal_bundle()
    bundle = bundle.model_copy(
        update={
            "source": SourceDescriptor(
                source_id=bundle.source.source_id,
                source_type=SourceType.PDF,
                source_label="sample.pdf",
                original_path=bundle.source.original_path,
                page_count=bundle.source.page_count,
                checksum=_sha256_label(source_pdf_bytes),
            ),
        },
        deep=True,
    )
    bundle.pages[0].prepared_page = bundle.pages[0].prepared_page.model_copy(
        update={"image_checksum": _sha256_label(prepared_bytes)},
    )
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    BundleLayoutService().write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )
    return root


def test_verify_matching_checksums_ok(tmp_path: Path) -> None:
    """Recorded digests that match on-disk bytes report OK."""
    root = _write_bundle_with_matching_checksums(tmp_path)
    report = BundleChecksumService().verify(root)

    assert report.all_ok
    prepared = next(
        result
        for result in report.results
        if result.artifact_path == "pages/page-0001/image/prepared.jp2"
    )
    assert prepared.status == ChecksumVerificationStatus.OK
    assert prepared.recorded_checksum == prepared.computed_checksum

    source = next(
        result for result in report.results if result.artifact_path == "source/sample.pdf"
    )
    assert source.status == ChecksumVerificationStatus.OK


def test_verify_tampered_prepared_image_fails(tmp_path: Path) -> None:
    """Tampered prepared image bytes report FAIL against the recorded digest."""
    root = _write_bundle_with_matching_checksums(tmp_path)
    image_path = root / "pages" / "page-0001" / "image" / "prepared.jp2"
    image_path.write_bytes(b"tampered-bytes")

    report = BundleChecksumService().verify(root)

    assert not report.all_ok
    prepared = next(
        result
        for result in report.results
        if result.artifact_path == "pages/page-0001/image/prepared.jp2"
    )
    assert prepared.status == ChecksumVerificationStatus.FAIL
    assert prepared.recorded_checksum != prepared.computed_checksum


def test_verify_skips_source_when_checksum_not_recorded(tmp_path: Path) -> None:
    """Document source digests are omitted from verification when not recorded."""
    root = _write_bundle_with_matching_checksums(tmp_path)
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source"]["checksum"] = None
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    report = BundleChecksumService().verify(root)

    assert report.all_ok
    assert all(result.artifact_path != "source/sample.pdf" for result in report.results)


def test_verify_prepared_unit_without_recorded_checksum_is_skipped() -> None:
    """Prepared units without recorded digests are skipped honestly."""
    service = BundleChecksumService()
    unit = PreparedArtifactRef.model_construct(
        artifact_id="unit-1",
        kind=InputKind.PREPARED_UNIT,
        page_id="page-0001",
        prepared_unit_id="unit-1",
        artifact_path="pages/page-0001/image/unit.png",
        parent_prepared_page_id="prepared-page-1",
        checksum=None,
    )

    result = service._verify_prepared_unit(Path("/unused"), unit)

    assert result.status == ChecksumVerificationStatus.SKIPPED
    assert result.detail == "no recorded checksum"
