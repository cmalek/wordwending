# Copyright (C) 2026 Chris Malek.
"""Materialize ordered source page rasters from images, ZIP archives, or PDFs."""

from __future__ import annotations

import hashlib
import io
import re
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZipInfo

import pypdfium2 as pdfium  # type: ignore[import-untyped]
from PIL import Image
from pypdfium2 import raw as pdfium_c  # type: ignore[import-untyped]

from bochord.models import (
    ColorMode,
    CoordinateSpace,
    PdfPageImageMode,
    PreparationRecipe,
    SourcePageArtifact,
)

#: Image suffixes accepted for single files, folders, and ZIP members.
_IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".tif", ".tiff", ".jp2"})
#: Minimum fraction of page width/height an embedded PDF image must cover.
_EMBEDDED_COVERAGE = 0.95
#: UNIX ``stat`` file-type mask stored in ZIP ``external_attr``.
_ZIP_S_IFMT = 0o170000
#: UNIX symlink file-type bits stored in ZIP ``external_attr``.
_ZIP_S_IFLNK = 0o120000


@dataclass(frozen=True)
class _MaterializedRaster:
    """One written page raster plus identifiers needed for the artifact."""

    #: Written page raster path under ``pages/``.
    destination: Path
    #: One-based page number.
    page_number: int
    #: Original source basename when available.
    source_filename: str
    #: Digest of the original source used for stable ids.
    source_checksum: str
    #: PDF acquisition mode, or ``None`` for image sources.
    acquisition_mode: PdfPageImageMode | None
    #: Effective raster DPI when known.
    dpi: float | None


class SourceAcquisitionService:
    """Copy or render source pages into a deterministic ``pages/`` layout."""

    def materialize(
        self,
        source: Path,
        output_dir: Path,
        recipe: PreparationRecipe,
    ) -> list[SourcePageArtifact]:
        """
        Materialize ordered source page rasters under ``output_dir/pages``.

        Side Effects:
            Creates ``output_dir/pages`` and writes one raster file per page.

        Args:
            source: PDF, single image, image folder, or ZIP of images.
            output_dir: Destination root for materialized ``pages/``.
            recipe: Preparation profile controlling PDF extraction and DPI.

        Returns:
            Ordered source page artifacts with checksums and coordinate spaces.

        Raises:
            ValueError: If ``source`` is unsupported or a ZIP member is unsafe.
            FileNotFoundError: If ``source`` does not exist.

        """
        source = source.resolve()
        if not source.exists():
            msg = f"source does not exist: {source}"
            raise FileNotFoundError(msg)

        pages_dir = output_dir / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)

        if source.is_dir():
            return self._materialize_image_paths(
                _image_paths_in_directory(source),
                pages_dir,
                _directory_source_checksum(source),
            )
        suffix = source.suffix.casefold()
        if suffix in _IMAGE_EXTENSIONS:
            return self._materialize_image_paths(
                [source],
                pages_dir,
                _sha256_label(source.read_bytes()),
            )
        if suffix == ".zip":
            return self._materialize_zip(source, pages_dir)
        if suffix == ".pdf":
            return self._materialize_pdf(source, pages_dir, recipe)
        msg = f"unsupported source type: {source}"
        raise ValueError(msg)

    def _materialize_image_paths(
        self,
        paths: list[Path],
        pages_dir: Path,
        source_checksum: str,
    ) -> list[SourcePageArtifact]:
        """
        Copy image paths into ``pages_dir`` in the given order.

        Side Effects:
            Writes copied page rasters under ``pages_dir``.

        Args:
            paths: Ordered source image paths.
            pages_dir: Destination directory for page files.
            source_checksum: Digest used to derive stable page identifiers.

        Returns:
            Ordered source page artifacts.

        Raises:
            ValueError: If ``paths`` is empty.

        """
        if not paths:
            msg = "no image pages found in source"
            raise ValueError(msg)
        artifacts: list[SourcePageArtifact] = []
        for index, path in enumerate(paths, start=1):
            destination = pages_dir / f"{index}{path.suffix.casefold()}"
            shutil.copy2(path, destination)
            artifacts.append(
                _artifact_from_raster(
                    _MaterializedRaster(
                        destination=destination,
                        page_number=index,
                        source_filename=path.name,
                        source_checksum=source_checksum,
                        acquisition_mode=None,
                        dpi=_image_dpi(destination),
                    )
                )
            )
        return artifacts

    def _materialize_zip(
        self,
        archive: Path,
        pages_dir: Path,
    ) -> list[SourcePageArtifact]:
        """
        Extract validated image members from ``archive`` into ``pages_dir``.

        Side Effects:
            Writes extracted page rasters under ``pages_dir``.

        Args:
            archive: ZIP archive path.
            pages_dir: Destination directory for page files.

        Returns:
            Ordered source page artifacts.

        Raises:
            ValueError: If the archive is empty, unsafe, or non-image.

        """
        source_checksum = _sha256_label(archive.read_bytes())
        with ZipFile(archive) as zip_file:
            members = [info for info in zip_file.infolist() if not info.is_dir()]
            if not members:
                msg = "empty archive"
                raise ValueError(msg)
            validated: list[tuple[str, ZipInfo]] = []
            seen: set[str] = set()
            for info in members:
                name = _validate_zip_member(info)
                if name in seen:
                    msg = f"duplicate archive member path: {name}"
                    raise ValueError(msg)
                seen.add(name)
                suffix = Path(name).suffix.casefold()
                if suffix not in _IMAGE_EXTENSIONS:
                    msg = f"non-image archive member: {name}"
                    raise ValueError(msg)
                validated.append((name, info))
            validated.sort(key=lambda item: _natural_key(Path(item[0])))
            artifacts: list[SourcePageArtifact] = []
            for index, (name, info) in enumerate(validated, start=1):
                destination = pages_dir / f"{index}{Path(name).suffix.casefold()}"
                with zip_file.open(info) as handle, destination.open("wb") as output:
                    shutil.copyfileobj(handle, output)
                artifacts.append(
                    _artifact_from_raster(
                        _MaterializedRaster(
                            destination=destination,
                            page_number=index,
                            source_filename=PurePosixPath(name).name,
                            source_checksum=source_checksum,
                            acquisition_mode=None,
                            dpi=_image_dpi(destination),
                        )
                    )
                )
            return artifacts

    def _materialize_pdf(
        self,
        pdf_path: Path,
        pages_dir: Path,
        recipe: PreparationRecipe,
    ) -> list[SourcePageArtifact]:
        """
        Extract or render each PDF page into ``pages_dir``.

        Side Effects:
            Writes page rasters under ``pages_dir``; opens and closes PDFium
            handles.

        Args:
            pdf_path: PDF source path.
            pages_dir: Destination directory for page files.
            recipe: Controls extraction mode, render DPI, and color mode.

        Returns:
            Ordered source page artifacts.

        Raises:
            ValueError: If forced embedded extraction is impossible.

        """
        source_checksum = _sha256_label(pdf_path.read_bytes())
        document = pdfium.PdfDocument(pdf_path)
        artifacts: list[SourcePageArtifact] = []
        try:
            for index in range(len(document)):
                page_number = index + 1
                page = document[index]
                try:
                    mode, image, dpi = _pdf_page_image(page, recipe)
                    destination = pages_dir / f"{page_number}.png"
                    _save_png(image, destination)
                    artifacts.append(
                        _artifact_from_raster(
                            _MaterializedRaster(
                                destination=destination,
                                page_number=page_number,
                                source_filename=pdf_path.name,
                                source_checksum=source_checksum,
                                acquisition_mode=mode,
                                dpi=dpi,
                            )
                        )
                    )
                finally:
                    page.close()
        finally:
            document.close()
        return artifacts


def _natural_key(path: Path) -> list[int | str]:
    """
    Build a natural-sort key from ``path.name``.

    Args:
        path: Filesystem path whose basename is sorted.

    Returns:
        Alternating text and integer key parts.

    """
    return [
        int(part) if part.isdigit() else part
        for part in re.split(r"(\d+)", path.name.casefold())
    ]


def _image_paths_in_directory(directory: Path) -> list[Path]:
    """
    List image files in ``directory`` using natural basename order.

    Args:
        directory: Directory to scan (non-recursive).

    Returns:
        Ordered image paths.

    """
    paths = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.casefold() in _IMAGE_EXTENSIONS
    ]
    return sorted(paths, key=_natural_key)


def _directory_source_checksum(directory: Path) -> str:
    """
    Digest ordered image basenames and bytes under ``directory``.

    Args:
        directory: Image directory.

    Returns:
        ``sha256:...`` label for stable page identifiers.

    """
    digest = hashlib.sha256()
    for path in _image_paths_in_directory(directory):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return f"sha256:{digest.hexdigest()}"


def _sha256_label(payload: bytes) -> str:
    """
    Format a SHA-256 digest label for ``payload``.

    Args:
        payload: Bytes to hash.

    Returns:
        ``sha256:<hex>`` label.

    """
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _zip_member_is_symlink(info: ZipInfo) -> bool:
    """
    Detect UNIX symlink members via ``external_attr``.

    Args:
        info: ZIP member metadata.

    Returns:
        ``True`` when the member mode bits indicate a symlink.

    """
    mode = info.external_attr >> 16
    return (mode & _ZIP_S_IFMT) == _ZIP_S_IFLNK


def _validate_zip_member(info: ZipInfo) -> str:
    """
    Reject unsafe ZIP members and return a normalized relative path.

    Args:
        info: ZIP member metadata.

    Returns:
        Normalized POSIX-relative member path.

    Raises:
        ValueError: If the member is absolute, uses ``..``, or is a symlink.

    """
    name = info.filename
    path = PurePosixPath(name)
    if path.is_absolute() or any(part == ".." for part in path.parts):
        msg = f"unsafe archive member: {name}"
        raise ValueError(msg)
    if _zip_member_is_symlink(info):
        msg = f"unsafe archive member symlink: {name}"
        raise ValueError(msg)
    normalized = path.as_posix()
    if not normalized or normalized == ".":
        msg = f"unsafe archive member: {name}"
        raise ValueError(msg)
    return normalized


def _image_dpi(path: Path) -> float | None:
    """
    Read an effective DPI from ``path`` when Pillow exposes one.

    Args:
        path: Raster path.

    Returns:
        DPI value, or ``None`` when absent.

    """
    with Image.open(path) as image:
        dpi = image.info.get("dpi")
        if isinstance(dpi, tuple) and dpi:
            return float(dpi[0])
        if isinstance(dpi, (int, float)):
            return float(dpi)
    return None


def _save_png(image: Image.Image, destination: Path) -> None:
    """
    Persist ``image`` as PNG without volatile metadata.

    Side Effects:
        Writes ``destination``.

    Args:
        image: Pillow image to save.
        destination: Output PNG path.

    """
    image.save(destination, format="PNG")


def _page_ids(source_checksum: str, page_number: int) -> tuple[str, str, str]:
    """
    Derive stable artifact, page, and space ids from source checksum.

    Args:
        source_checksum: Digest of the original source.
        page_number: One-based page number.

    Returns:
        ``(artifact_id, source_page_id, space_id)``.

    """
    material = f"{source_checksum}:{page_number}".encode()
    digest = hashlib.sha256(material).hexdigest()
    return f"artifact-{digest}", f"page-{digest}", f"space-{digest}"


def _artifact_from_raster(raster: _MaterializedRaster) -> SourcePageArtifact:
    """
    Build a ``SourcePageArtifact`` from a materialized raster file.

    Args:
        raster: Written page raster and acquisition metadata.

    Returns:
        Populated source page artifact.

    """
    payload = raster.destination.read_bytes()
    checksum = _sha256_label(payload)
    artifact_id, source_page_id, space_id = _page_ids(
        raster.source_checksum,
        raster.page_number,
    )
    with Image.open(io.BytesIO(payload)) as image:
        width_px, height_px = image.size
    return SourcePageArtifact(
        artifact_id=artifact_id,
        source_page_id=source_page_id,
        page_number=raster.page_number,
        source_path=f"pages/{raster.destination.name}",
        source_filename=raster.source_filename,
        checksum=checksum,
        acquisition_mode=raster.acquisition_mode,
        coordinate_space=CoordinateSpace(
            space_id=space_id,
            width_px=width_px,
            height_px=height_px,
            dpi=raster.dpi,
        ),
    )


def _pdf_page_image(
    page: pdfium.PdfPage,
    recipe: PreparationRecipe,
) -> tuple[PdfPageImageMode, Image.Image, float]:
    """
    Choose extract-or-render for one PDF page per ``recipe``.

    Args:
        page: Open PDFium page.
        recipe: Preparation profile.

    Returns:
        Acquisition mode, Pillow image, and effective DPI.

    Raises:
        ValueError: If ``extract-embedded`` is required but unavailable.

    """
    mode = recipe.pdf_page_image_mode
    if mode in {PdfPageImageMode.AUTO, PdfPageImageMode.EXTRACT_EMBEDDED}:
        extracted = _try_extract_embedded(page, recipe)
        if extracted is not None:
            return PdfPageImageMode.EXTRACT_EMBEDDED, extracted[0], extracted[1]
        if mode is PdfPageImageMode.EXTRACT_EMBEDDED:
            msg = "embedded page image extraction failed"
            raise ValueError(msg)
    return (
        PdfPageImageMode.RENDER_PAGE,
        *_render_page(page, recipe),
    )


def _try_extract_embedded(
    page: pdfium.PdfPage,
    recipe: PreparationRecipe,
) -> tuple[Image.Image, float] | None:
    """
    Extract a full-page embedded raster when acquisition rules allow.

    Args:
        page: Open PDFium page.
        recipe: Preparation profile providing ``minimum_dpi``.

    Returns:
        Pillow image and native DPI, or ``None`` when rules fail.

    """
    images = [
        obj
        for obj in page.get_objects(filter=[pdfium_c.FPDF_PAGEOBJ_IMAGE])
        if isinstance(obj, pdfium.PdfImage)
    ]
    if len(images) != 1:
        return None
    pdf_image = images[0]
    left, bottom, right, top = pdf_image.get_bounds()
    display_w = right - left
    display_h = top - bottom
    page_w = page.get_width()
    page_h = page.get_height()
    if page_w <= 0 or page_h <= 0 or display_w <= 0 or display_h <= 0:
        return None
    if (
        display_w / page_w < _EMBEDDED_COVERAGE
        or display_h / page_h < _EMBEDDED_COVERAGE
    ):
        return None
    px_w, px_h = pdf_image.get_px_size()
    dpi_x = px_w / (display_w / 72.0)
    dpi_y = px_h / (display_h / 72.0)
    native_dpi = min(dpi_x, dpi_y)
    if native_dpi < recipe.thresholds.minimum_dpi:
        return None
    bitmap = pdf_image.get_bitmap()
    try:
        try:
            image = bitmap.to_pil()
            # Force decode validation via Pillow round-trip load.
            image.load()
        except Exception:  # noqa: BLE001 - any decode failure falls back to render
            return None
    finally:
        bitmap.close()
    return image, float(native_dpi)


def _render_page(
    page: pdfium.PdfPage,
    recipe: PreparationRecipe,
) -> tuple[Image.Image, float]:
    """
    Render ``page`` at ``recipe.render_dpi``.

    Args:
        page: Open PDFium page.
        recipe: Preparation profile.

    Returns:
        Rendered Pillow image and render DPI.

    """
    scale = recipe.render_dpi / 72
    bitmap = page.render(
        scale=scale,
        grayscale=recipe.color_mode == ColorMode.GRAYSCALE,
    )
    try:
        image = bitmap.to_pil()
        image.load()
    finally:
        bitmap.close()
    return image, float(recipe.render_dpi)
