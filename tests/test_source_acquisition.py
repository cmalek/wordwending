# Copyright (C) 2026 Chris Malek.
"""Tests for source page materialization."""

from __future__ import annotations

import json
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile

import pypdfium2 as pdfium
import pytest
from PIL import Image

from wordwending.models import PdfPageImageMode, PreparationRecipe, SourceType
from wordwending.services.source_acquisition import (
    SourceAcquisitionService,
    _image_bounds_cover_page,
)

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


def pdf_fixture(tmp_path: Path | None = None) -> Path:
    """
    Build a one-page blank PDF for acquisition tests.

    Args:
        tmp_path: Optional pytest temp directory; uses a sibling path when omitted.

    Returns:
        Path to a saved one-page PDF.

    """
    base = tmp_path if tmp_path is not None else Path(".")
    pdf_path = base / "blank.pdf"
    document = pdfium.PdfDocument.new()
    document.new_page(612.0, 792.0)
    document.save(pdf_path)
    document.close()
    return pdf_path


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
    assert [page.source_page_id for page in pages] == ["page-0001", "page-0002"]
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


def test_image_bounds_must_overlap_most_of_page_area() -> None:
    assert _image_bounds_cover_page(0.0, 0.0, 95.0, 95.0, 100.0, 100.0)
    assert not _image_bounds_cover_page(10.0, 10.0, 110.0, 110.0, 100.0, 100.0)


def test_pdf_page_records_acquisition_backend(tmp_path: Path) -> None:
    page = SourceAcquisitionService().materialize(
        pdf_fixture(tmp_path),
        tmp_path / "out",
        recipe(),
    )[0]
    assert page.source_type is SourceType.PDF
    assert page.acquisition_backend == "pypdfium2"
    assert page.acquisition_backend_version == version("pypdfium2")


def test_single_image_records_source_type(tmp_path: Path) -> None:
    image = tmp_path / "page.png"
    write_image(image)
    page = SourceAcquisitionService().materialize(
        image,
        tmp_path / "out",
        recipe(),
    )[0]
    assert page.source_type is SourceType.SINGLE_IMAGE
    assert page.acquisition_backend is None
    assert page.acquisition_backend_version is None


def test_image_folder_records_image_set_source_type(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    write_image(source / "page-1.png")
    write_image(source / "page-2.png")
    pages = SourceAcquisitionService().materialize(
        source,
        tmp_path / "out",
        recipe(),
    )
    assert all(page.source_type is SourceType.IMAGE_SET for page in pages)
    assert all(page.acquisition_backend is None for page in pages)
    assert all(page.acquisition_backend_version is None for page in pages)


def test_zip_records_image_set_source_type(tmp_path: Path) -> None:
    archive = tmp_path / "pages.zip"
    seed = tmp_path / "seed.png"
    write_image(seed)
    with ZipFile(archive, "w") as output:
        output.write(seed, "page-1.png")
        output.write(seed, "page-2.png")
    pages = SourceAcquisitionService().materialize(
        archive,
        tmp_path / "out",
        recipe(),
    )
    assert all(page.source_type is SourceType.IMAGE_SET for page in pages)
    assert all(page.acquisition_backend is None for page in pages)
    assert all(page.acquisition_backend_version is None for page in pages)
