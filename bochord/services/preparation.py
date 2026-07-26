# Copyright (C) 2026 Chris Malek.
"""Deterministic page-quality assessment and layout classification."""

from __future__ import annotations

import statistics
from typing import TYPE_CHECKING, Any, cast

from PIL import Image, ImageChops, ImageFilter, ImageStat

from bochord.models import (
    AssessmentThresholds,
    FlagSeverity,
    PageClass,
    PreparationRecipe,
    QualitySignal,
    SourcePageArtifact,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

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
