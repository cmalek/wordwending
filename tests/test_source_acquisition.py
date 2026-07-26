# Copyright (C) 2026 Chris Malek.
"""Tests for source page materialization."""

from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

import pypdfium2 as pdfium
import pytest
from PIL import Image

from bochord.models import PdfPageImageMode, PreparationRecipe
from bochord.services.source_acquisition import SourceAcquisitionService

#: Canonical preparation recipe fixture used by acquisition tests.
_RECIPE_PATH = Path("tests/fixtures/preparation/recipe-v1.json")


def recipe(**overrides: object) -> PreparationRecipe:
    """
    Load the Phase 3 recipe fixture with optional field overrides.

    Keyword Args:
        overrides: Recipe fields to replace in the fixture payload.

    Returns:
        Validated preparation recipe.

    """
    payload = json.loads(_RECIPE_PATH.read_text(encoding="utf-8"))
    payload.update(overrides)
    return PreparationRecipe.model_validate(payload)


def write_image(path: Path) -> None:
    """
    Write a tiny RGB PNG/JPEG/TIFF image to ``path``.

    Args:
        path: Destination image path; format follows the suffix.

    """
    Image.new("RGB", (10, 10), "white").save(path)


def test_image_folder_uses_natural_page_order(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    write_image(source / "page-10.png")
    write_image(source / "page-2.jpg")

    pages = SourceAcquisitionService().materialize(
        source,
        tmp_path / "out",
        recipe(),
    )

    assert [page.source_filename for page in pages] == ["page-2.jpg", "page-10.png"]
    assert all(page.checksum.startswith("sha256:") for page in pages)


def test_zip_rejects_parent_path_member(tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with ZipFile(archive, "w") as output:
        output.writestr("../escape.png", b"bad")
    with pytest.raises(ValueError, match="unsafe archive member"):
        SourceAcquisitionService().materialize(archive, tmp_path / "out", recipe())


def test_pdf_auto_extracts_single_page_raster(tmp_path: Path) -> None:
    pdf = tmp_path / "one-page.pdf"
    Image.new("RGB", (200, 300), "white").save(pdf, "PDF", resolution=400)

    pages = SourceAcquisitionService().materialize(
        pdf,
        tmp_path / "out",
        recipe(pdf_page_image_mode="auto"),
    )

    assert len(pages) == 1
    assert pages[0].acquisition_mode in {
        PdfPageImageMode.EXTRACT_EMBEDDED,
        PdfPageImageMode.RENDER_PAGE,
    }


def test_pdf_forced_render_matches_render_dpi(tmp_path: Path) -> None:
    render_dpi = 400
    width_pt = 612.0
    height_pt = 792.0
    pdf_path = tmp_path / "blank.pdf"
    document = pdfium.PdfDocument.new()
    document.new_page(width_pt, height_pt)
    document.save(pdf_path)
    document.close()

    pages = SourceAcquisitionService().materialize(
        pdf_path,
        tmp_path / "out",
        recipe(pdf_page_image_mode="render-page", render_dpi=render_dpi),
    )

    assert len(pages) == 1
    assert pages[0].acquisition_mode == PdfPageImageMode.RENDER_PAGE
    assert pages[0].coordinate_space.width_px == round(width_pt / 72 * render_dpi)
    assert pages[0].coordinate_space.height_px == round(height_pt / 72 * render_dpi)
    assert pages[0].coordinate_space.dpi == float(render_dpi)
