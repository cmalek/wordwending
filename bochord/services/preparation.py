# Copyright (C) 2026 Chris Malek.
"""Deterministic page-quality assessment, classification, and preparation."""

from __future__ import annotations

import hashlib
import statistics
from typing import TYPE_CHECKING, Any, Literal, cast

from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageStat

from bochord.models import (
    AssessmentThresholds,
    BinarizeMode,
    BoundingBox,
    ColorMode,
    CoordinateSpace,
    CoordinateTransform,
    CropMode,
    DewarpMode,
    FlagSeverity,
    InputKind,
    PageClass,
    PreparationAssessment,
    PreparationMode,
    PreparationRecipe,
    PreparationResult,
    PreparedArtifactRef,
    PreparedPage,
    QualitySignal,
    SourcePageArtifact,
    TransformKind,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

#: Longest edge used for cheap heuristic measurement.
_HEURISTIC_MAX_EDGE_PX = 1600
#: Candidate deskew angles searched by row-projection variance.
_SKEW_ANGLES_DEGREES = tuple(angle / 2 for angle in range(-6, 7))
#: Fraction of page width used for border and gutter strips.
_MARGIN_STRIP_FRACTION = 0.08
#: Absolute luminance delta treated as speckle after median filtering.
_SPECKLE_DELTA = 24
#: RGB channel spread treated as non-neutral colored marking.
_COLOR_SPREAD_THRESHOLD = 30
#: Luminance below this value counts as dark ink.
_INK_THRESHOLD = 128
#: Mid-tone band upper bound for bleed-through proxy pixels.
_BLEED_LIGHT_MAX = 200
#: Minimum ink fraction for a row to count as a text run.
_TEXT_ROW_INK_FRACTION = 0.02
#: Minimum run length (downsampled px) kept for text-height statistics.
_MIN_TEXT_RUN_PX = 2
#: Minimum samples required to compute a projection variance.
_MIN_VARIANCE_SAMPLES = 2
#: Vertical valley must stay below this fraction of peak column ink.
_COLUMN_VALLEY_FRACTION = 0.35
#: Minimum valley width as a fraction of page width.
_COLUMN_VALLEY_MIN_WIDTH_FRACTION = 0.03
#: Horizontal/vertical rule must cover this fraction of the opposite axis.
_TABLE_RULE_COVERAGE = 0.70
#: Minimum consecutive dark samples that form one table rule.
_TABLE_RULE_MIN_RUN = 3
#: Lower-page ink ratio that promotes note-heavy classification.
_NOTE_HEAVY_INK_RATIO = 1.5
#: Table-rule count that promotes table-heavy classification.
_TABLE_HEAVY_RULE_COUNT = 6
#: Minimum column count for dense-dictionary classification.
_MIN_DICTIONARY_COLUMNS = 2
#: Dense-dictionary text-height cutoff matching AssessmentThresholds default.
_DENSE_TEXT_HEIGHT_PX = 18.0
#: Warning-signal count that promotes mixed-complex classification.
_MIXED_COMPLEX_WARNING_COUNT = 3
#: Floor used when middle-half ink density is effectively zero.
_INK_DENSITY_EPSILON = 1e-9
#: Full 8-bit luminance range used when converting darkness ratios.
_LUMINANCE_MAX = 255
#: Fixed PNG zlib compression level for reproducible prepared artifacts.
_PNG_COMPRESS_LEVEL = 6
#: Median-filter window used for denoise transforms.
_DENOISE_MEDIAN_SIZE = 3
#: Adaptive-threshold local window size in pixels.
_ADAPTIVE_WINDOW = 15
#: Adaptive-threshold bias subtracted from the local mean.
_ADAPTIVE_BIAS = 10
#: Exact rejection message for unsupported basic dewarp.
_BASIC_DEWARP_MESSAGE = "basic dewarp requires a replayable mapping artifact"


class PageQualityAssessor:
    """Measure cheap, deterministic quality signals for one page raster."""

    def assess(
        self,
        source_page: SourcePageArtifact,
        image: Image.Image,
        recipe: PreparationRecipe,
    ) -> list[QualitySignal]:
        """
        Assess quality and layout cues for ``image``.

        Args:
            source_page: Acquired source page providing DPI metadata.
            image: Source page raster to measure.
            recipe: Preparation profile supplying assessment thresholds.

        Returns:
            Ordered quality signals with severities relative to thresholds.

        """
        thresholds = recipe.thresholds
        working, scale = _downsample_for_heuristics(image)
        gray = working.convert("L")
        rgb = working.convert("RGB")
        return [
            _effective_dpi_signal(source_page, thresholds),
            _skew_signal(gray, thresholds),
            _gutter_shadow_signal(gray, thresholds),
            _border_shadow_signal(gray, thresholds),
            _contrast_signal(gray, thresholds),
            _speckle_signal(gray, thresholds),
            _colored_marking_signal(rgb),
            _bleedthrough_signal(gray),
            _median_text_height_signal(gray, scale, thresholds),
            _column_count_signal(gray),
            _table_rule_signal(gray),
            _lower_page_ink_signal(gray),
        ]


class PageClassifier:
    """Suggest a page-class cohort from measured quality signals."""

    def suggest(self, signals: list[QualitySignal]) -> PageClass:
        """
        Suggest a page class using the fixed priority heuristics.

        Args:
            signals: Quality signals from ``PageQualityAssessor.assess``.

        Returns:
            Highest-priority matching ``PageClass`` cohort.

        """
        by_id = {signal.signal_id: signal for signal in signals}
        # ponytail: fixed heuristics; replace with calibrated cohort thresholds only
        # when held-out evaluation shows a repeatable classification failure.
        table_rules = _signal_value(by_id, "table_rule_count")
        if table_rules is not None and table_rules >= _TABLE_HEAVY_RULE_COUNT:
            return PageClass.TABLE_HEAVY

        column_count = _signal_value(by_id, "column_count")
        text_height = _signal_value(by_id, "median_text_run_height_px")
        if (
            column_count is not None
            and column_count >= _MIN_DICTIONARY_COLUMNS
            and text_height is not None
            and text_height < _DENSE_TEXT_HEIGHT_PX
        ):
            return PageClass.DENSE_DICTIONARY

        lower_ink = _signal_value(by_id, "lower_page_ink_ratio")
        if lower_ink is not None and lower_ink >= _NOTE_HEAVY_INK_RATIO:
            return PageClass.NOTE_HEAVY

        warning_count = sum(
            1 for signal in signals if signal.severity is FlagSeverity.WARNING
        )
        if warning_count >= _MIXED_COMPLEX_WARNING_COUNT:
            return PageClass.MIXED_COMPLEX
        return PageClass.ORDINARY_PROSE


class PagePreparationService:
    """
    Apply deterministic transforms and subdivision for one source page.

    Args:
        assessor: Quality-signal measurer for the source raster.
        classifier: Page-class suggester over measured signals.

    """

    def __init__(
        self,
        assessor: PageQualityAssessor,
        classifier: PageClassifier,
    ) -> None:
        """
        Bind assessor and classifier collaborators.

        Args:
            assessor: Quality-signal measurer for the source raster.
            classifier: Page-class suggester over measured signals.

        """
        #: Quality assessor used before preparation choice.
        self._assessor = assessor
        #: Page classifier used when no operator override is supplied.
        self._classifier = classifier

    def prepare(  # noqa: PLR0913
        self,
        source_page: SourcePageArtifact,
        recipe: PreparationRecipe,
        output_dir: Path,
        *,
        mode_override: PreparationMode | None = None,
        page_class_override: PageClass | None = None,
        override_reason: str | None = None,
    ) -> PreparationResult:
        """
        Prepare one source page into a preserved raster and optional units.

        Side Effects:
            Writes prepared page and unit PNG files under ``output_dir``.

        Args:
            source_page: Acquired source page artifact to prepare.
            recipe: Deterministic preparation profile.
            output_dir: Bundle root receiving prepared artifacts.

        Keyword Args:
            mode_override: Operator-forced subdivision mode.
            page_class_override: Operator-forced page class.
            override_reason: Required reason when any override is set.

        Returns:
            Full preparation outcome for the source page.

        Raises:
            ValueError: If ``dewarp_mode`` is ``basic`` or an override lacks a
                reason.

        """
        if recipe.dewarp_mode is DewarpMode.BASIC:
            raise ValueError(_BASIC_DEWARP_MESSAGE)

        with Image.open(source_page.source_path) as opened:
            source_image = opened.copy()

        signals = self._assessor.assess(source_page, source_image, recipe)
        suggested = self._classifier.suggest(signals)
        page_class, page_class_source = _resolve_page_class(
            suggested,
            page_class_override,
            override_reason,
        )
        mode, choice_source = _resolve_preparation_mode(
            page_class,
            signals,
            mode_override,
            override_reason,
        )
        prepared_image, transforms = _apply_recipe_transforms(
            source_image,
            source_page,
            recipe,
        )
        prepared_page_id = _derive_prepared_page_id(source_page.checksum, recipe, mode)
        prepared_page = _persist_prepared_page(
            prepared_image,
            transforms=transforms,
            source_page=source_page,
            recipe=recipe,
            mode=mode,
            page_class=page_class,
            prepared_page_id=prepared_page_id,
            space_id=f"prepared-page-{source_page.page_number:04d}",
            output_dir=output_dir,
        )
        assessment = _build_assessment(
            source_page=source_page,
            prepared_page_id=prepared_page_id,
            signals=signals,
            page_class_suggested=suggested,
            page_class_final=page_class,
            page_class_source=page_class_source,
            operator_override_reason=(
                override_reason if page_class_source == "operator" else None
            ),
        )
        return PreparationResult(
            source_page=source_page,
            prepared_page=prepared_page,
            assessment=assessment,
            preparation_choice_source=choice_source,
            operator_override_reason=(
                override_reason if choice_source == "operator" else None
            ),
        )


def _resolve_page_class(
    suggested: PageClass,
    override: PageClass | None,
    override_reason: str | None,
) -> tuple[PageClass, Literal["auto", "operator"]]:
    """
    Resolve final page class from automation or operator override.

    Args:
        suggested: Classifier suggestion.
        override: Optional operator page class.
        override_reason: Operator reason when override is set.

    Returns:
        Final page class and whether it came from automation or an operator.

    Raises:
        ValueError: If an override is set without a non-empty reason.

    """
    if override is None:
        return suggested, "auto"
    if not override_reason or not override_reason.strip():
        msg = "override_reason is required when page_class_override is set"
        raise ValueError(msg)
    return override, "operator"


def _resolve_preparation_mode(
    page_class: PageClass,
    signals: list[QualitySignal],
    override: PreparationMode | None,
    override_reason: str | None,
) -> tuple[PreparationMode, Literal["auto", "operator"]]:
    """
    Resolve subdivision mode from automation or operator override.

    Args:
        page_class: Final page class for auto mode choice.
        signals: Measured quality signals.
        override: Optional operator preparation mode.
        override_reason: Operator reason when override is set.

    Returns:
        Preparation mode and whether it came from automation or an operator.

    Raises:
        ValueError: If an override is set without a non-empty reason.

    """
    if override is not None:
        if not override_reason or not override_reason.strip():
            msg = "override_reason is required when mode_override is set"
            raise ValueError(msg)
        return override, "operator"
    return _choose_preparation_mode(page_class, signals), "auto"


def _choose_preparation_mode(
    page_class: PageClass,
    signals: list[QualitySignal],
) -> PreparationMode:
    """
    Choose subdivision mode from page class and quality signals.

    Args:
        page_class: Final page class.
        signals: Measured quality signals.

    Returns:
        Automatic preparation mode for the page.

    """
    by_id = {signal.signal_id: signal for signal in signals}
    column_count = _signal_value(by_id, "column_count")
    if (
        page_class is PageClass.DENSE_DICTIONARY
        and column_count is not None
        and column_count >= _MIN_DICTIONARY_COLUMNS
    ):
        return PreparationMode.COLUMNS
    text = by_id.get("median_text_run_height_px")
    reliable_columns = (
        column_count is not None and column_count >= _MIN_DICTIONARY_COLUMNS
    )
    if (
        text is not None
        and text.severity is FlagSeverity.WARNING
        and not reliable_columns
    ):
        return PreparationMode.FIXED_TILES
    return PreparationMode.FULL_PAGE


def _derive_prepared_page_id(
    source_checksum: str,
    recipe: PreparationRecipe,
    mode: PreparationMode,
) -> str:
    """
    Derive a stable prepared-page id from checksum, recipe, and mode.

    Args:
        source_checksum: Source raster digest label.
        recipe: Preparation recipe used for the variant.
        mode: Subdivision mode applied to the variant.

    Returns:
        ``prepared-<hex>`` identifier.

    """
    material = f"{source_checksum}\n{recipe.model_dump_json()}\n{mode.value}".encode()
    return f"prepared-{hashlib.sha256(material).hexdigest()}"


def _sha256_label(payload: bytes) -> str:
    """
    Format a SHA-256 digest label for ``payload``.

    Args:
        payload: Bytes to hash.

    Returns:
        ``sha256:<hex>`` label.

    """
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _save_prepared_png(image: Image.Image, destination: Path) -> str:
    """
    Persist ``image`` as PNG with fixed options and return its checksum.

    Side Effects:
        Writes ``destination``.

    Args:
        image: Prepared raster to save.
        destination: Output PNG path.

    Returns:
        Digest label for the saved bytes.

    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    clean = image.copy()
    clean.info.clear()
    clean.save(
        destination,
        format="PNG",
        optimize=False,
        compress_level=_PNG_COMPRESS_LEVEL,
        pnginfo=None,
        exif=b"",
        icc_profile=None,
    )
    return _sha256_label(destination.read_bytes())


def _persist_prepared_page(  # noqa: PLR0913
    prepared_image: Image.Image,
    *,
    transforms: list[CoordinateTransform],
    source_page: SourcePageArtifact,
    recipe: PreparationRecipe,
    mode: PreparationMode,
    page_class: PageClass,
    prepared_page_id: str,
    space_id: str,
    output_dir: Path,
) -> PreparedPage:
    """
    Write the prepared page image and assemble its ``PreparedPage`` record.

    Side Effects:
        Writes the prepared page PNG and any subdivision unit PNGs.

    Args:
        prepared_image: Fully transformed prepared page raster.

    Keyword Args:
        transforms: Source-to-prepared transform chain.
        source_page: Logical source page identity.
        recipe: Preparation recipe used for this variant.
        mode: Subdivision mode applied to the page.
        page_class: Final page class for the page.
        prepared_page_id: Stable prepared-page identifier.
        space_id: Prepared-page coordinate-space identifier.
        output_dir: Bundle root receiving artifacts.

    Returns:
        Prepared page model with optional units.

    """
    image_rel = f"pages/{source_page.source_page_id}/image/page.png"
    image_checksum = _save_prepared_png(prepared_image, output_dir / image_rel)
    units = _build_prepared_units(
        prepared_image,
        mode=mode,
        recipe=recipe,
        source_page=source_page,
        prepared_page_id=prepared_page_id,
        space_id=space_id,
        output_dir=output_dir,
    )
    return PreparedPage(
        prepared_page_id=prepared_page_id,
        preparation_mode=mode,
        page_class=page_class,
        image_path=image_rel,
        source_artifact_id=source_page.artifact_id,
        image_checksum=image_checksum,
        preparation_recipe_id=recipe.recipe_id,
        coordinate_space=CoordinateSpace(
            space_id=space_id,
            width_px=prepared_image.width,
            height_px=prepared_image.height,
            dpi=source_page.coordinate_space.dpi,
            parent_space_id=source_page.coordinate_space.space_id,
        ),
        transforms=transforms,
        prepared_units=units,
    )


def _apply_recipe_transforms(
    source_image: Image.Image,
    source_page: SourcePageArtifact,
    recipe: PreparationRecipe,
) -> tuple[Image.Image, list[CoordinateTransform]]:
    """
    Apply supported deterministic recipe transforms to ``source_image``.

    Args:
        source_image: Source page raster.
        source_page: Source artifact providing coordinate-space identity.
        recipe: Preparation profile controlling transforms.

    Returns:
        Prepared image and ordered transform records.

    """
    working = source_image.copy()
    transforms: list[CoordinateTransform] = []
    current_space = source_page.coordinate_space.space_id
    working, current_space = _maybe_deskew(
        working, recipe.deskew, current_space, transforms
    )
    if recipe.denoise:
        working = working.filter(ImageFilter.MedianFilter(size=_DENOISE_MEDIAN_SIZE))
    working, _current_space = _maybe_crop(
        working, recipe.crop_mode, current_space, transforms
    )
    working = _apply_color_mode(working, recipe.color_mode)
    if recipe.binarize_mode is not BinarizeMode.NONE:
        working = _apply_binarize(working, recipe.binarize_mode)
    elif recipe.color_mode is ColorMode.BINARY:
        working = _threshold_binary(working.convert("L"), _INK_THRESHOLD)
    return working, transforms


def _maybe_deskew(
    image: Image.Image,
    deskew: bool,
    current_space: str,
    transforms: list[CoordinateTransform],
) -> tuple[Image.Image, str]:
    """
    Optionally deskew ``image`` and record the transform.

    Args:
        image: Working raster.
        deskew: Whether deskew is enabled.
        current_space: Current coordinate-space identifier.
        transforms: Mutable transform chain to append to.

    Returns:
        Possibly deskewed image and updated space id.

    """
    if not deskew:
        return image, current_space
    skew = _measure_skew_degrees(image.convert("L"))
    if abs(skew) == 0:
        return image, current_space
    rotated = image.rotate(
        -skew,
        resample=Image.Resampling.BICUBIC,
        expand=False,
        fillcolor=_fill_color(image),
    )
    target = f"{current_space}-deskew"
    transforms.append(
        CoordinateTransform(
            kind=TransformKind.DESKEW,
            source_space_id=current_space,
            target_space_id=target,
            parameters={"angle_degrees": -skew},
        )
    )
    return rotated, target


def _maybe_crop(
    image: Image.Image,
    crop_mode: CropMode,
    current_space: str,
    transforms: list[CoordinateTransform],
) -> tuple[Image.Image, str]:
    """
    Optionally crop ``image`` and record the transform.

    Args:
        image: Working raster.
        crop_mode: Crop strategy.
        current_space: Current coordinate-space identifier.
        transforms: Mutable transform chain to append to.

    Returns:
        Possibly cropped image and updated space id.

    """
    if crop_mode is CropMode.NONE:
        return image, current_space
    box = _crop_box(image, crop_mode)
    if box is None:
        return image, current_space
    left, upper, right, lower = box
    cropped = image.crop(box)
    target = f"{current_space}-crop"
    transforms.append(
        CoordinateTransform(
            kind=TransformKind.CROP,
            source_space_id=current_space,
            target_space_id=target,
            parameters={
                "x0": float(left),
                "y0": float(upper),
                "x1": float(right),
                "y1": float(lower),
            },
        )
    )
    return cropped, target


def _fill_color(image: Image.Image) -> int | tuple[int, ...]:
    """
    Choose a background fill matching ``image`` mode.

    Args:
        image: Image being rotated or expanded.

    Returns:
        Mode-appropriate white/background fill value.

    """
    if image.mode == "L":
        return 255
    if image.mode == "1":
        return 1
    if image.mode == "RGBA":
        return (255, 255, 255, 255)
    return (255, 255, 255)


def _crop_box(
    image: Image.Image,
    crop_mode: CropMode,
) -> tuple[int, int, int, int] | None:
    """
    Compute a crop box for ``crop_mode``.

    Args:
        image: Image to crop.
        crop_mode: Crop strategy.

    Returns:
        Inclusive-exclusive Pillow crop box, or ``None`` when empty.

    """
    gray = image.convert("L")
    if crop_mode is CropMode.TRIM_MARGIN:
        inverted = ImageOps.invert(gray)
        return inverted.getbbox()
    if crop_mode is CropMode.CONTENT_BOUNDING_BOX:
        mask = gray.point(lambda value: 255 if value < _INK_THRESHOLD else 0)
        return mask.getbbox()
    return None


def _apply_color_mode(image: Image.Image, color_mode: ColorMode) -> Image.Image:
    """
    Convert ``image`` to the recipe color mode before optional binarization.

    Args:
        image: Working raster.
        color_mode: Target color encoding.

    Returns:
        Color-converted image.

    """
    if color_mode is ColorMode.GRAYSCALE:
        return image.convert("L")
    if color_mode is ColorMode.RGB:
        return image.convert("RGB")
    return image.convert("L")


def _apply_binarize(image: Image.Image, mode: BinarizeMode) -> Image.Image:
    """
    Binarize ``image`` with Otsu or adaptive thresholding.

    Args:
        image: Working raster.
        mode: Binarization strategy.

    Returns:
        Binary (mode ``1``) image.

    """
    gray = image.convert("L")
    if mode is BinarizeMode.OTSU:
        return _threshold_binary(gray, _otsu_threshold(gray))
    return _adaptive_binary(gray)


def _otsu_threshold(gray: Image.Image) -> int:
    """
    Compute a global Otsu threshold for ``gray``.

    Args:
        gray: Grayscale image.

    Returns:
        Threshold in ``0..255``.

    """
    histogram = gray.histogram()
    total = sum(histogram)
    if total == 0:
        return _INK_THRESHOLD
    sum_total = sum(index * count for index, count in enumerate(histogram))
    sum_background = 0.0
    weight_background = 0.0
    best_threshold = 0
    best_variance = -1.0
    for threshold, count in enumerate(histogram):
        weight_background += count
        if weight_background == 0:
            continue
        weight_foreground = total - weight_background
        if weight_foreground == 0:
            break
        sum_background += threshold * count
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        variance = (
            weight_background
            * weight_foreground
            * (mean_background - mean_foreground) ** 2
        )
        if variance > best_variance:
            best_variance = variance
            best_threshold = threshold
    return best_threshold


def _adaptive_binary(gray: Image.Image) -> Image.Image:
    """
    Binarize ``gray`` with a local-mean adaptive threshold.

    Args:
        gray: Grayscale image.

    Returns:
        Binary (mode ``1``) image.

    """
    # ponytail: box-blur local mean; swap for a stronger adaptive kernel only if
    # held-out pages show systematic threshold failure on textured backgrounds.
    blurred = gray.filter(ImageFilter.BoxBlur(_ADAPTIVE_WINDOW // 2))
    width, height = gray.size
    source = _pixel_access(gray)
    local = _pixel_access(blurred)
    out = Image.new("1", (width, height), 1)
    dest = _pixel_access(out)
    for y in range(height):
        for x in range(width):
            threshold = int(local[x, y]) - _ADAPTIVE_BIAS
            dest[x, y] = 0 if source[x, y] < threshold else 1
    return out


def _threshold_binary(gray: Image.Image, threshold: int) -> Image.Image:
    """
    Threshold ``gray`` into a binary image.

    Args:
        gray: Grayscale image.
        threshold: Inclusive upper bound for ink pixels.

    Returns:
        Binary (mode ``1``) image.

    """
    return gray.point(lambda value, cut=threshold: 0 if value < cut else 255, mode="1")


def _measure_skew_degrees(gray: Image.Image) -> float:
    """
    Estimate page skew degrees via row-projection variance.

    Args:
        gray: Grayscale page image.

    Returns:
        Estimated skew in degrees (positive clockwise).

    """
    working, _scale = _downsample_for_heuristics(gray)
    best_angle = 0.0
    best_variance = -1.0
    for angle in _SKEW_ANGLES_DEGREES:
        rotated = working.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            fillcolor=255,
        )
        variance = _row_projection_variance(rotated)
        if variance > best_variance:
            best_variance = variance
            best_angle = float(angle)
    return -best_angle


def _build_prepared_units(  # noqa: PLR0913
    prepared_image: Image.Image,
    *,
    mode: PreparationMode,
    recipe: PreparationRecipe,
    source_page: SourcePageArtifact,
    prepared_page_id: str,
    space_id: str,
    output_dir: Path,
) -> list[PreparedArtifactRef]:
    """
    Subdivide ``prepared_image`` into prepared units when required.

    Side Effects:
        Writes unit PNG files under ``output_dir``.

    Args:
        prepared_image: Fully transformed prepared page raster.

    Keyword Args:
        mode: Subdivision mode.
        recipe: Recipe supplying overlap and tile height.
        source_page: Logical source page identity.
        prepared_page_id: Parent prepared-page identifier.
        space_id: Prepared-page coordinate-space identifier.
        output_dir: Bundle root for unit artifacts.

    Returns:
        Ordered prepared-unit artifact references.

    """
    if mode is PreparationMode.FULL_PAGE:
        return []
    boxes, kind = _subdivision_boxes(prepared_image, mode=mode, recipe=recipe)
    units_dir = output_dir / "pages" / source_page.source_page_id / "image" / "units"
    units_dir.mkdir(parents=True, exist_ok=True)
    return [
        _prepared_unit_from_box(
            prepared_image,
            box=box,
            order=order,
            kind=kind,
            source_page=source_page,
            prepared_page_id=prepared_page_id,
            space_id=space_id,
            output_dir=output_dir,
        )
        for order, box in enumerate(boxes, start=1)
    ]


def _subdivision_boxes(
    prepared_image: Image.Image,
    *,
    mode: PreparationMode,
    recipe: PreparationRecipe,
) -> tuple[list[tuple[int, int, int, int]], str]:
    """
    Compute subdivision crop boxes and unit-kind label.

    Args:
        prepared_image: Prepared page raster.

    Keyword Args:
        mode: Subdivision mode (columns or fixed tiles).
        recipe: Recipe supplying overlap and tile height.

    Returns:
        Crop boxes and unit-kind fragment (``column`` or ``tile``).

    """
    if mode is PreparationMode.COLUMNS:
        return (
            _column_unit_boxes(
                prepared_image,
                overlap_px=recipe.subdivision_overlap_px,
            ),
            "column",
        )
    return (
        _fixed_tile_boxes(
            prepared_image.width,
            prepared_image.height,
            tile_height_px=recipe.fixed_tile_height_px,
            overlap_px=recipe.subdivision_overlap_px,
        ),
        "tile",
    )


def _prepared_unit_from_box(  # noqa: PLR0913
    prepared_image: Image.Image,
    *,
    box: tuple[int, int, int, int],
    order: int,
    kind: str,
    source_page: SourcePageArtifact,
    prepared_page_id: str,
    space_id: str,
    output_dir: Path,
) -> PreparedArtifactRef:
    """
    Crop, save, and describe one prepared unit.

    Side Effects:
        Writes one unit PNG under ``output_dir``.

    Args:
        prepared_image: Prepared page raster.

    Keyword Args:
        box: Crop box in prepared-page coordinates.
        order: One-based reading order.
        kind: Unit-kind fragment such as ``column`` or ``tile``.
        source_page: Logical source page identity.
        prepared_page_id: Parent prepared-page identifier.
        space_id: Prepared-page coordinate-space identifier.
        output_dir: Bundle root for unit artifacts.

    Returns:
        Prepared-unit artifact reference.

    """
    unit_id = f"{source_page.source_page_id}-{kind}-{order:03d}"
    rel = f"pages/{source_page.source_page_id}/image/units/{unit_id}.png"
    checksum = _save_prepared_png(prepared_image.crop(box), output_dir / rel)
    x0, y0, x1, y1 = box
    return PreparedArtifactRef(
        artifact_id=f"artifact-{unit_id}",
        kind=InputKind.PREPARED_UNIT,
        page_id=source_page.source_page_id,
        prepared_unit_id=unit_id,
        artifact_path=rel,
        parent_prepared_page_id=prepared_page_id,
        checksum=checksum,
        order=order,
        bounding_box=BoundingBox(
            x0=float(x0),
            y0=float(y0),
            x1=float(x1),
            y1=float(y1),
            coordinate_space_id=space_id,
        ),
    )


def _column_valley_centers(gray: Image.Image) -> list[int]:
    """
    Locate midpoints of sustained low-ink vertical valleys.

    Args:
        gray: Grayscale prepared page.

    Returns:
        Valley center x-coordinates in left-to-right order.

    """
    profile = _column_ink_profile(gray)
    peak = max(profile) if profile else 0.0
    if peak <= 0:
        return []
    valley_limit = peak * _COLUMN_VALLEY_FRACTION
    min_width = max(
        1,
        cast("int", round(len(profile) * _COLUMN_VALLEY_MIN_WIDTH_FRACTION)),
    )
    centers: list[int] = []
    run = 0
    run_start = 0
    in_content = False
    for index, ink in enumerate(profile):
        if ink > valley_limit:
            if run >= min_width and in_content:
                centers.append(run_start + run // 2)
            run = 0
            in_content = True
        else:
            if run == 0:
                run_start = index
            run += 1
    return centers


def _column_unit_boxes(
    image: Image.Image,
    *,
    overlap_px: int,
) -> list[tuple[int, int, int, int]]:
    """
    Build left-to-right column crop boxes with configured overlap.

    Args:
        image: Prepared page raster.

    Keyword Args:
        overlap_px: Horizontal overlap into adjacent columns.

    Returns:
        Crop boxes ``(x0, y0, x1, y1)`` in prepared-page coordinates.

    """
    gray = image.convert("L")
    width, height = gray.size
    centers = _column_valley_centers(gray)
    if not centers:
        return [(0, 0, width, height)]
    splits = [0, *centers, width]
    boxes: list[tuple[int, int, int, int]] = []
    last_index = len(splits) - 2
    for index in range(last_index + 1):
        x0 = splits[index]
        x1 = splits[index + 1]
        if index > 0:
            x0 = max(0, x0 - overlap_px)
        if index < last_index:
            x1 = min(width, x1 + overlap_px)
        if x1 > x0:
            boxes.append((x0, 0, x1, height))
    return boxes


def _fixed_tile_boxes(
    width: int,
    height: int,
    *,
    tile_height_px: int,
    overlap_px: int,
) -> list[tuple[int, int, int, int]]:
    """
    Build top-to-bottom fixed-tile crop boxes with configured overlap.

    Args:
        width: Prepared page width in pixels.
        height: Prepared page height in pixels.

    Keyword Args:
        tile_height_px: Nominal tile height.
        overlap_px: Vertical overlap between adjacent tiles.

    Returns:
        Crop boxes ``(x0, y0, x1, y1)`` in prepared-page coordinates.

    """
    stride = max(1, tile_height_px - overlap_px)
    boxes: list[tuple[int, int, int, int]] = []
    y0 = 0
    while y0 < height:
        y1 = min(y0 + tile_height_px, height)
        boxes.append((0, y0, width, y1))
        if y1 >= height:
            break
        y0 += stride
    return boxes


def _build_assessment(  # noqa: PLR0913
    *,
    source_page: SourcePageArtifact,
    prepared_page_id: str,
    signals: list[QualitySignal],
    page_class_suggested: PageClass,
    page_class_final: PageClass,
    page_class_source: Literal["auto", "operator"],
    operator_override_reason: str | None,
) -> PreparationAssessment:
    """
    Build assessment metadata for one prepared page.

    Keyword Args:
        source_page: Source page under assessment.
        prepared_page_id: Prepared page produced for the source.
        signals: Measured quality signals.
        page_class_suggested: Automatic class suggestion.
        page_class_final: Final class used for preparation.
        page_class_source: Whether the final class was automatic or operator.
        operator_override_reason: Operator reason when class was overridden.

    Returns:
        Validated preparation assessment.

    """
    flags = [
        signal.signal_id
        for signal in signals
        if signal.severity is FlagSeverity.WARNING
    ]
    return PreparationAssessment(
        assessment_id=f"assessment-{source_page.source_page_id}",
        source_page_id=source_page.source_page_id,
        prepared_page_id=prepared_page_id,
        signals=signals,
        flags=flags,
        recommended_actions=[],
        warnings=list(flags),
        page_class_suggested=page_class_suggested,
        page_class_final=page_class_final,
        page_class_source=page_class_source,
        operator_override_reason=operator_override_reason,
    )


def _pixel_access(image: Image.Image) -> Any:
    """
    Return Pillow pixel access for ``image``.

    Args:
        image: Image whose pixels will be read.

    Returns:
        Pixel-access object for direct indexing.

    Raises:
        RuntimeError: If Pillow cannot provide pixel access.

    """
    pixels = image.load()
    if pixels is None:
        msg = "Pillow pixel access is unavailable for image"
        raise RuntimeError(msg)
    return pixels


def _signal_value(by_id: dict[str, QualitySignal], signal_id: str) -> float | None:
    """
    Read one signal value by id.

    Args:
        by_id: Signals indexed by ``signal_id``.
        signal_id: Stable signal identifier.

    Returns:
        Numeric value, or ``None`` when missing.

    """
    signal = by_id.get(signal_id)
    if signal is None:
        return None
    return signal.value


def _downsample_for_heuristics(image: Image.Image) -> tuple[Image.Image, float]:
    """
    Downsample so the longest edge is at most ``_HEURISTIC_MAX_EDGE_PX``.

    Args:
        image: Source raster.

    Returns:
        ``(working_image, scale)`` where ``scale`` is working/source size.

    """
    width, height = image.size
    longest = max(width, height)
    if longest <= _HEURISTIC_MAX_EDGE_PX:
        return image.copy(), 1.0
    scale = _HEURISTIC_MAX_EDGE_PX / float(longest)
    size = (
        max(1, cast("int", round(width * scale))),
        max(1, cast("int", round(height * scale))),
    )
    return image.resize(size, resample=Image.Resampling.LANCZOS), scale


def _make_signal(
    signal_id: str,
    value: float | None,
    *,
    unit: str | None,
    severity: FlagSeverity,
    measured: bool,
) -> QualitySignal:
    """
    Build one ``QualitySignal`` row.

    Args:
        signal_id: Stable signal identifier.
        value: Measured numeric value when available.

    Keyword Args:
        unit: Measurement unit when applicable.
        severity: Threshold severity for the signal.
        measured: Whether the value came from a direct measurement.

    Returns:
        Populated quality signal.

    """
    return QualitySignal(
        signal_id=signal_id,
        value=value,
        unit=unit,
        severity=severity,
        measured=measured,
    )


def _severity_min(value: float, minimum: float) -> FlagSeverity:
    """
    Warn when ``value`` falls below ``minimum``.

    Args:
        value: Measured value.
        minimum: Inclusive lower bound.

    Returns:
        ``WARNING`` or ``INFO``.

    """
    if value < minimum:
        return FlagSeverity.WARNING
    return FlagSeverity.INFO


def _severity_max(value: float, maximum: float) -> FlagSeverity:
    """
    Warn when ``value`` exceeds ``maximum``.

    Args:
        value: Measured value.
        maximum: Inclusive upper bound.

    Returns:
        ``WARNING`` or ``INFO``.

    """
    if value > maximum:
        return FlagSeverity.WARNING
    return FlagSeverity.INFO


def _effective_dpi_signal(
    source_page: SourcePageArtifact,
    thresholds: AssessmentThresholds,
) -> QualitySignal:
    """
    Emit effective DPI from the source coordinate space.

    Args:
        source_page: Source page carrying DPI metadata.
        thresholds: Assessment thresholds.

    Returns:
        ``effective_dpi`` quality signal.

    """
    dpi = source_page.coordinate_space.dpi
    if dpi is None:
        return _make_signal(
            "effective_dpi",
            None,
            unit="dpi",
            severity=FlagSeverity.WARNING,
            measured=False,
        )
    return _make_signal(
        "effective_dpi",
        float(dpi),
        unit="dpi",
        severity=_severity_min(float(dpi), thresholds.minimum_dpi),
        measured=True,
    )


def _row_projection_variance(gray: Image.Image) -> float:
    """
    Compute variance of per-row ink sums.

    Args:
        gray: Grayscale page image.

    Returns:
        Variance of row ink projections.

    """
    width, height = gray.size
    pixels = _pixel_access(gray)
    row_sums = []
    for y in range(height):
        ink = 0
        for x in range(width):
            ink += _LUMINANCE_MAX - pixels[x, y]
        row_sums.append(ink)
    if len(row_sums) < _MIN_VARIANCE_SAMPLES:
        return 0.0
    return float(statistics.pvariance(row_sums))


def _skew_signal(gray: Image.Image, thresholds: AssessmentThresholds) -> QualitySignal:
    """
    Estimate skew via row-projection variance over candidate angles.

    Args:
        gray: Grayscale working image.
        thresholds: Assessment thresholds.

    Returns:
        ``skew_degrees`` quality signal.

    """
    best_angle = 0.0
    best_variance = -1.0
    for angle in _SKEW_ANGLES_DEGREES:
        rotated = gray.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            fillcolor=255,
        )
        variance = _row_projection_variance(rotated)
        if variance > best_variance:
            best_variance = variance
            best_angle = float(angle)
    # Best straighten angle is the opposite of the page skew.
    skew = -best_angle
    return _make_signal(
        "skew_degrees",
        skew,
        unit="degrees",
        severity=_severity_max(abs(skew), thresholds.maximum_abs_skew_degrees),
        measured=True,
    )


def _strip_darkness_ratio(gray: Image.Image, box: tuple[int, int, int, int]) -> float:
    """
    Measure mean darkness ratio inside ``box``.

    Args:
        gray: Grayscale working image.
        box: Crop box ``(left, upper, right, lower)``.

    Returns:
        Mean ``(255 - luminance) / 255`` in the strip.

    """
    region = gray.crop(box)
    if region.size[0] == 0 or region.size[1] == 0:
        return 0.0
    mean = float(ImageStat.Stat(region).mean[0])
    return (_LUMINANCE_MAX - mean) / float(_LUMINANCE_MAX)


def _margin_strip_width(width: int) -> int:
    """
    Width of the 8% border/gutter strip in pixels.

    Args:
        width: Page width in pixels.

    Returns:
        At least one pixel of strip width.

    """
    return max(1, cast("int", round(width * _MARGIN_STRIP_FRACTION)))


def _gutter_shadow_signal(
    gray: Image.Image,
    thresholds: AssessmentThresholds,
) -> QualitySignal:
    """
    Measure darkness of the center 8% vertical strip.

    Args:
        gray: Grayscale working image.
        thresholds: Assessment thresholds.

    Returns:
        ``gutter_shadow_ratio`` quality signal.

    """
    width, height = gray.size
    strip = _margin_strip_width(width)
    x0 = max(0, (width - strip) // 2)
    ratio = _strip_darkness_ratio(gray, (x0, 0, min(width, x0 + strip), height))
    return _make_signal(
        "gutter_shadow_ratio",
        ratio,
        unit="ratio",
        severity=_severity_max(ratio, thresholds.maximum_dark_margin_ratio),
        measured=True,
    )


def _border_shadow_signal(
    gray: Image.Image,
    thresholds: AssessmentThresholds,
) -> QualitySignal:
    """
    Measure darkness of the left/right 8% vertical strips.

    Args:
        gray: Grayscale working image.
        thresholds: Assessment thresholds.

    Returns:
        ``border_shadow_ratio`` quality signal.

    """
    width, height = gray.size
    strip = _margin_strip_width(width)
    left = _strip_darkness_ratio(gray, (0, 0, strip, height))
    right = _strip_darkness_ratio(gray, (max(0, width - strip), 0, width, height))
    ratio = max(left, right)
    return _make_signal(
        "border_shadow_ratio",
        ratio,
        unit="ratio",
        severity=_severity_max(ratio, thresholds.maximum_dark_margin_ratio),
        measured=True,
    )


def _contrast_signal(
    gray: Image.Image,
    thresholds: AssessmentThresholds,
) -> QualitySignal:
    """
    Measure grayscale luminance standard deviation.

    Args:
        gray: Grayscale working image.
        thresholds: Assessment thresholds.

    Returns:
        ``contrast_stddev`` quality signal.

    """
    stddev = float(ImageStat.Stat(gray).stddev[0])
    return _make_signal(
        "contrast_stddev",
        stddev,
        unit=None,
        severity=_severity_min(stddev, thresholds.minimum_contrast_stddev),
        measured=True,
    )


def _speckle_signal(
    gray: Image.Image,
    thresholds: AssessmentThresholds,
) -> QualitySignal:
    """
    Measure isolated pixel noise relative to a median filter.

    Args:
        gray: Grayscale working image.
        thresholds: Assessment thresholds.

    Returns:
        ``speckle_ratio`` quality signal.

    """
    filtered = gray.filter(ImageFilter.MedianFilter(size=3))
    diff = ImageChops.difference(gray, filtered)
    pixels = _pixel_access(diff)
    width, height = gray.size
    speckles = 0
    total = width * height
    for y in range(height):
        for x in range(width):
            if pixels[x, y] >= _SPECKLE_DELTA:
                speckles += 1
    ratio = speckles / total if total else 0.0
    return _make_signal(
        "speckle_ratio",
        ratio,
        unit="ratio",
        severity=_severity_max(ratio, thresholds.maximum_speckle_ratio),
        measured=True,
    )


def _colored_marking_signal(rgb: Image.Image) -> QualitySignal:
    """
    Measure non-neutral RGB channel-spread coverage.

    Args:
        rgb: RGB working image.

    Returns:
        ``colored_marking_ratio`` quality signal.

    """
    pixels = _pixel_access(rgb)
    width, height = rgb.size
    colored = 0
    total = width * height
    for y in range(height):
        for x in range(width):
            red, green, blue = pixels[x, y][:3]
            if max(red, green, blue) - min(red, green, blue) >= _COLOR_SPREAD_THRESHOLD:
                colored += 1
    ratio = colored / total if total else 0.0
    return _make_signal(
        "colored_marking_ratio",
        ratio,
        unit="ratio",
        severity=FlagSeverity.INFO,
        measured=True,
    )


def _bleedthrough_signal(gray: Image.Image) -> QualitySignal:
    """
    Estimate bleed-through via light-to-dark paired-pixel ratio.

    Args:
        gray: Grayscale working image.

    Returns:
        ``bleedthrough_proxy`` quality signal.

    """
    pixels = _pixel_access(gray)
    width, height = gray.size
    dark = 0
    light = 0
    for y in range(height):
        for x in range(width):
            value = pixels[x, y]
            if value < _INK_THRESHOLD:
                dark += 1
            elif value < _BLEED_LIGHT_MAX:
                light += 1
    ratio = light / dark if dark else float(light)
    return _make_signal(
        "bleedthrough_proxy",
        ratio,
        unit="ratio",
        severity=FlagSeverity.INFO,
        measured=True,
    )


def _text_row_mask(gray: Image.Image) -> list[bool]:
    """
    Mark rows that contain enough ink to count as text.

    Args:
        gray: Grayscale working image.

    Returns:
        Per-row boolean mask of text-bearing rows.

    """
    pixels = _pixel_access(gray)
    width, height = gray.size
    min_ink = max(1, int(width * _TEXT_ROW_INK_FRACTION))
    rows: list[bool] = []
    for y in range(height):
        ink = 0
        for x in range(width):
            if pixels[x, y] < _INK_THRESHOLD:
                ink += 1
        rows.append(ink >= min_ink)
    return rows


def _run_lengths(mask: Sequence[bool]) -> list[int]:
    """
    Collect lengths of contiguous ``True`` runs.

    Args:
        mask: Boolean sequence.

    Returns:
        Run lengths in sample units.

    """
    lengths: list[int] = []
    run = 0
    for flag in mask:
        if flag:
            run += 1
            continue
        if run:
            lengths.append(run)
            run = 0
    if run:
        lengths.append(run)
    return lengths


def _median_text_height_signal(
    gray: Image.Image,
    scale: float,
    thresholds: AssessmentThresholds,
) -> QualitySignal:
    """
    Estimate median text-run height in source-image pixels.

    Args:
        gray: Grayscale working image.
        scale: Working-image size divided by source-image size.
        thresholds: Assessment thresholds.

    Returns:
        ``median_text_run_height_px`` quality signal.

    """
    runs = [
        length
        for length in _run_lengths(_text_row_mask(gray))
        if length >= _MIN_TEXT_RUN_PX
    ]
    if not runs or scale <= 0:
        height_px = 0.0
    else:
        height_px = float(statistics.median(runs)) / scale
    return _make_signal(
        "median_text_run_height_px",
        height_px,
        unit="px",
        severity=_severity_min(height_px, thresholds.minimum_text_run_height_px),
        measured=True,
    )


def _column_ink_profile(gray: Image.Image) -> list[float]:
    """
    Build a per-column ink sum profile.

    Args:
        gray: Grayscale working image.

    Returns:
        Ink totals for each x coordinate.

    """
    pixels = _pixel_access(gray)
    width, height = gray.size
    profile: list[float] = []
    for x in range(width):
        ink = 0.0
        for y in range(height):
            value = pixels[x, y]
            if value < _INK_THRESHOLD:
                ink += _LUMINANCE_MAX - value
        profile.append(ink)
    return profile


def _column_count_signal(gray: Image.Image) -> QualitySignal:
    """
    Count columns via sustained low-ink vertical valleys.

    Args:
        gray: Grayscale working image.

    Returns:
        ``column_count`` quality signal.

    """
    profile = _column_ink_profile(gray)
    peak = max(profile) if profile else 0.0
    if peak <= 0:
        columns = 1.0
    else:
        valley_limit = peak * _COLUMN_VALLEY_FRACTION
        min_width = max(
            1,
            cast("int", round(len(profile) * _COLUMN_VALLEY_MIN_WIDTH_FRACTION)),
        )
        valleys = 0
        run = 0
        in_content = False
        for ink in profile:
            if ink > valley_limit:
                if run >= min_width and in_content:
                    valleys += 1
                run = 0
                in_content = True
            else:
                run += 1
        columns = float(valleys + 1) if in_content else 1.0
    return _make_signal(
        "column_count",
        columns,
        unit="count",
        severity=FlagSeverity.INFO,
        measured=True,
    )


def _longest_dark_run(values: Sequence[int], threshold: int) -> int:
    """
    Return the longest contiguous run of values below ``threshold``.

    Args:
        values: One row or column of luminance samples.
        threshold: Inclusive upper bound for dark pixels.

    Returns:
        Longest dark run length in samples.

    """
    longest = 0
    run = 0
    for value in values:
        if value < threshold:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return longest


def _rule_row_mask(gray: Image.Image) -> list[bool]:
    """
    Mark rows whose longest dark run spans enough of the page width.

    Args:
        gray: Grayscale working image.

    Returns:
        Per-row mask of horizontal rule candidates.

    """
    pixels = _pixel_access(gray)
    width, height = gray.size
    min_run = max(1, cast("int", round(width * _TABLE_RULE_COVERAGE)))
    mask: list[bool] = []
    for y in range(height):
        row = [pixels[x, y] for x in range(width)]
        mask.append(_longest_dark_run(row, _INK_THRESHOLD) >= min_run)
    return mask


def _rule_column_mask(gray: Image.Image) -> list[bool]:
    """
    Mark columns whose longest dark run spans enough of the page height.

    Args:
        gray: Grayscale working image.

    Returns:
        Per-column mask of vertical rule candidates.

    """
    pixels = _pixel_access(gray)
    width, height = gray.size
    min_run = max(1, cast("int", round(height * _TABLE_RULE_COVERAGE)))
    mask: list[bool] = []
    for x in range(width):
        column = [pixels[x, y] for y in range(height)]
        mask.append(_longest_dark_run(column, _INK_THRESHOLD) >= min_run)
    return mask


def _table_rule_signal(gray: Image.Image) -> QualitySignal:
    """
    Count sustained dark horizontal and vertical rules.

    Args:
        gray: Grayscale working image.

    Returns:
        ``table_rule_count`` quality signal.

    """
    horizontal = sum(
        1
        for length in _run_lengths(_rule_row_mask(gray))
        if length >= _TABLE_RULE_MIN_RUN
    )
    vertical = sum(
        1
        for length in _run_lengths(_rule_column_mask(gray))
        if length >= _TABLE_RULE_MIN_RUN
    )
    return _make_signal(
        "table_rule_count",
        float(horizontal + vertical),
        unit="count",
        severity=FlagSeverity.INFO,
        measured=True,
    )


def _lower_page_ink_signal(gray: Image.Image) -> QualitySignal:
    """
    Compare bottom-quarter ink density to the middle half.

    Args:
        gray: Grayscale working image.

    Returns:
        ``lower_page_ink_ratio`` quality signal.

    """
    width, height = gray.size
    quarter = height // 4
    bottom = _strip_darkness_ratio(gray, (0, height - quarter, width, height))
    middle = _strip_darkness_ratio(gray, (0, quarter, width, height - quarter))
    ratio = bottom / middle if middle > _INK_DENSITY_EPSILON else float(bottom)
    return _make_signal(
        "lower_page_ink_ratio",
        ratio,
        unit="ratio",
        severity=FlagSeverity.INFO,
        measured=True,
    )
