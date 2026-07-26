# Copyright (C) 2026 Chris Malek.
"""Tests for PAGE XML review-package interchange."""

from __future__ import annotations

from pathlib import Path

from bochord.models import BundlePage, FontSlant
from bochord.services.page_interchange import PageXmlInterchangeService


def test_page_xml_round_trip_keeps_page_contract(tmp_path: Path) -> None:
    """Round-trip export/import should preserve sidecar-only page evidence."""
    base = BundlePage.model_validate_json(
        Path("tests/fixtures/interchange/note-page.base.json").read_text()
    )
    image = tmp_path / "note-page.png"
    image.write_bytes(b"fixture-image")
    service = PageXmlInterchangeService()

    package = service.export_review_package(base, image, tmp_path)
    returned = service.import_corrected_page(
        tmp_path / "page-0010.xml",
        tmp_path / "page-0010.bochord.json",
    )

    assert package.name == "page-0010.review.zip"
    assert returned.page_id == base.page_id
    assert returned.prepared_page == base.prepared_page
    assert returned.notes[0].linked_marker_span_ids == ["span-note-marker-10"]
    assert returned.spans[0].typography.slant is FontSlant.ITALIC


def test_corrected_page_xml_updates_only_page_fields(tmp_path: Path) -> None:
    """PAGE corrections should update text while sidecar evidence stays intact."""
    base = BundlePage.model_validate_json(
        Path("tests/fixtures/interchange/dictionary-page.base.json").read_text()
    )
    service = PageXmlInterchangeService()
    image = tmp_path / "page.png"
    image.write_bytes(b"fixture-image")
    service.export_review_package(base, image, tmp_path)
    page_xml = tmp_path / "page-0100.xml"
    xml = page_xml.read_text().replace("dreorig", "drēorig")
    page_xml.write_text(xml, encoding="utf-8")

    returned = service.import_corrected_page(
        page_xml,
        tmp_path / "page-0100.bochord.json",
    )

    assert returned.spans[0].text_diplomatic == "drēorig"
    assert returned.spans[0].provenance == base.spans[0].provenance
    assert returned.prepared_page.transforms == base.prepared_page.transforms
