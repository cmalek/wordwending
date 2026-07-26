# Copyright (C) 2026 Chris Malek.
"""Tests for PAGE XML review-package interchange."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from bochord.models import BaselineShift, BundlePage, FontSlant
from bochord.services.page_interchange import PAGE_NS, PageXmlInterchangeService

FIXTURE_DIR = Path("tests/fixtures/interchange")
NOTE_FIXTURE = FIXTURE_DIR / "note-page.base.json"


def _parse_native_corrected(stem: str) -> ET.Element:
    """Return the root element of one recorded eScriptorium PAGE export."""
    return ET.parse(FIXTURE_DIR / f"{stem}.corrected.xml").getroot()  # noqa: S314


def _line_unicode(line_el: ET.Element) -> str:
    unicode_el = line_el.find(f"{{{PAGE_NS}}}TextEquiv/{{{PAGE_NS}}}Unicode")
    return "" if unicode_el is None or unicode_el.text is None else unicode_el.text


def _word_ids(root: ET.Element) -> list[str]:
    return [
        word.get("id", "")
        for word in root.findall(f".//{{{PAGE_NS}}}Word")
        if word.get("id")
    ]


def _export_note_page(tmp_path: Path) -> tuple[PageXmlInterchangeService, Path, Path]:
    """Export the note-page fixture and return paths for import tests."""
    base = BundlePage.model_validate_json(NOTE_FIXTURE.read_text())
    image = tmp_path / "note-page.png"
    image.write_bytes(b"fixture-image")
    service = PageXmlInterchangeService()
    service.export_review_package(base, image, tmp_path)
    return service, tmp_path / "page-0010.xml", tmp_path / "page-0010.bochord.json"


def test_page_xml_round_trip_keeps_page_contract(tmp_path: Path) -> None:
    """Round-trip export/import should preserve sidecar-only page evidence."""
    base = BundlePage.model_validate_json(NOTE_FIXTURE.read_text())
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
    returned_order = [
        region.reading_order_index
        for region in sorted(returned.regions, key=lambda item: item.region_id)
    ]
    base_order = [
        region.reading_order_index
        for region in sorted(base.regions, key=lambda item: item.region_id)
    ]
    assert returned_order == base_order == [1, 2]
    marker = next(
        span for span in returned.spans if span.span_id == "span-note-marker-10"
    )
    assert marker.typography.baseline_shift is BaselineShift.SUPERSCRIPT


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


def test_import_rejects_missing_region_id(tmp_path: Path) -> None:
    """Import should fail when PAGE XML drops a canonical region id."""
    service, page_xml, sidecar = _export_note_page(tmp_path)
    xml = page_xml.read_text().replace('id="region-0010-footnote"', 'id="region-0010-missing"')

    page_xml.write_text(xml, encoding="utf-8")

    with pytest.raises(ValueError, match="missing region ids: region-0010-footnote"):
        service.import_corrected_page(page_xml, sidecar)


def test_import_rejects_duplicate_line_id(tmp_path: Path) -> None:
    """Import should fail when PAGE XML repeats a canonical line id."""
    service, page_xml, sidecar = _export_note_page(tmp_path)
    xml = page_xml.read_text().replace(
        '<TextLine id="line-0010-footnote-1">',
        '<TextLine id="line-0010-body-1">',
        1,
    )

    page_xml.write_text(xml, encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate line id line-0010-body-1"):
        service.import_corrected_page(page_xml, sidecar)


def test_import_rejects_missing_word_id(tmp_path: Path) -> None:
    """Import should fail when PAGE XML drops a canonical word id."""
    service, page_xml, sidecar = _export_note_page(tmp_path)
    root = ET.parse(page_xml).getroot()  # noqa: S314
    page_el = root.find(f"{{{PAGE_NS}}}Page")
    assert page_el is not None
    for region_el in page_el.findall(f"{{{PAGE_NS}}}TextRegion"):
        for line_el in region_el.findall(f"{{{PAGE_NS}}}TextLine"):
            for word_el in list(line_el.findall(f"{{{PAGE_NS}}}Word")):
                if word_el.get("id") == "span-note-marker-10":
                    line_el.remove(word_el)
    ET.ElementTree(root).write(page_xml, encoding="utf-8", xml_declaration=True)

    with pytest.raises(ValueError, match="missing word ids: span-note-marker-10"):
        service.import_corrected_page(page_xml, sidecar)


@pytest.mark.parametrize(
    ("stem", "corrected_text", "region_ids", "line_ids"),
    [
        (
            "dictionary-page",
            "drēorig",
            ["region-0100-a", "region-0100-b"],
            ["line-0100-1", "line-0100-2"],
        ),
        (
            "note-page",
            "Deletion",
            ["region-0010-body", "region-0010-footnote"],
            ["line-0010-body-1", "line-0010-footnote-1"],
        ),
    ],
)
def test_native_escriptorium_export_preserves_region_line_ids_and_text(
    stem: str,
    corrected_text: str,
    region_ids: list[str],
    line_ids: list[str],
) -> None:
    """Recorded native exports keep region/line ids and line-level corrections."""
    root = _parse_native_corrected(stem)
    page_el = root.find(f"{{{PAGE_NS}}}Page")
    assert page_el is not None

    exported_region_ids = [
        region.get("id")
        for region in page_el.findall(f"{{{PAGE_NS}}}TextRegion")
        if region.get("id")
    ]
    exported_line_ids = [
        line.get("id")
        for region in page_el.findall(f"{{{PAGE_NS}}}TextRegion")
        for line in region.findall(f"{{{PAGE_NS}}}TextLine")
        if line.get("id")
    ]
    assert exported_region_ids == region_ids
    assert exported_line_ids == line_ids

    body_line = next(
        line
        for region in page_el.findall(f"{{{PAGE_NS}}}TextRegion")
        for line in region.findall(f"{{{PAGE_NS}}}TextLine")
        if line.get("id") == line_ids[0]
    )
    assert corrected_text in _line_unicode(body_line)


@pytest.mark.parametrize("stem", ["dictionary-page", "note-page"])
def test_native_escriptorium_export_lacks_stable_word_ids(stem: str) -> None:
    """Native eScriptorium PAGE export drops Word elements and span-* ids."""
    root = _parse_native_corrected(stem)
    assert root.findall(f".//{{{PAGE_NS}}}Word") == []
    assert _word_ids(root) == []
    assert "span-" not in ET.tostring(root, encoding="unicode")


@pytest.mark.parametrize(
    ("stem", "missing_word_ids"),
    [
        (
            "dictionary-page",
            ["span-0100-headword", "span-0100-sorrow"],
        ),
        (
            "note-page",
            ["span-0010-footnote-text", "span-0010-italic", "span-note-marker-10"],
        ),
    ],
)
def test_native_escriptorium_export_rejects_import(
    stem: str,
    missing_word_ids: list[str],
) -> None:
    """Import must fail when native export omits canonical Word/span ids."""
    service = PageXmlInterchangeService()
    sidecar = FIXTURE_DIR / f"{stem}.base.json"
    corrected = FIXTURE_DIR / f"{stem}.corrected.xml"

    with pytest.raises(ValueError, match="missing word ids:") as exc_info:
        service.import_corrected_page(corrected, sidecar)

    for word_id in missing_word_ids:
        assert word_id in str(exc_info.value)
