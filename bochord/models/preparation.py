# Copyright (C) 2026 Chris Malek.
"""Preparation contracts for source acquisition and page preparation."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bochord.models.ocr import (
    CoordinateSpace,
    FlagSeverity,
    PageClass,
    PreparedPage,
    SchemaModel,
)


class ColorMode(StrEnum):
    """Raster color encoding applied during page preparation."""

    #: Single-channel luminance output.
    GRAYSCALE = "grayscale"
    #: Three-channel RGB output.
    RGB = "rgb"
    #: Single-bit foreground/background output.
    BINARY = "binary"


class CropMode(StrEnum):
    """Page crop strategy applied before OCR subdivision."""

    #: Preserve the full prepared raster extent.
    NONE = "none"
    #: Trim uniform outer margins from the raster.
    TRIM_MARGIN = "trim-margin"
    #: Crop to the detected content bounding box.
    CONTENT_BOUNDING_BOX = "content-bounding-box"


class BinarizeMode(StrEnum):
    """Binarization strategy applied during page preparation."""

    #: Preserve grayscale or RGB values unchanged.
    NONE = "none"
    #: Global Otsu thresholding.
    OTSU = "otsu"
    #: Adaptive local thresholding.
    ADAPTIVE = "adaptive"


class DewarpMode(StrEnum):
    """Dewarp strategy applied during page preparation."""

    #: No dewarp transform is applied.
    NONE = "none"
    #: Basic dewarp transform when a replayable mapping artifact exists.
    BASIC = "basic"


class PdfPageImageMode(StrEnum):
    """PDF page rasterization strategy during source acquisition."""

    #: Extract embedded page images when present.
    EXTRACT_EMBEDDED = "extract-embedded"
    #: Render the page vector content to a raster.
    RENDER_PAGE = "render-page"
    #: Prefer embedded images and fall back to rendering.
    AUTO = "auto"


class AssessmentThresholds(BaseModel):
    """Calibratable limits for deterministic image-quality heuristics."""

    #: Forbid unknown keys so persisted threshold profiles stay stable.
    model_config = ConfigDict(extra="forbid")
    #: Minimum acceptable effective raster DPI.
    minimum_dpi: float = Field(default=300, gt=0)
    #: Minimum acceptable luminance standard deviation.
    minimum_contrast_stddev: float = Field(default=25, ge=0)
    #: Maximum acceptable absolute skew in degrees.
    maximum_abs_skew_degrees: float = Field(default=1.5, gt=0)
    #: Maximum acceptable dark-margin coverage ratio.
    maximum_dark_margin_ratio: float = Field(default=0.25, ge=0, le=1)
    #: Maximum acceptable isolated speckle coverage ratio.
    maximum_speckle_ratio: float = Field(default=0.02, ge=0, le=1)
    #: Minimum acceptable text-run height in pixels.
    minimum_text_run_height_px: float = Field(default=18, gt=0)


class PreparationRecipe(SchemaModel):
    """Deterministic page-preparation profile."""

    #: Stable recipe identifier or digest.
    recipe_id: str
    #: PDF page image extraction or rendering strategy.
    pdf_page_image_mode: PdfPageImageMode
    #: Target DPI when rendering PDF pages.
    render_dpi: int = Field(gt=0)
    #: Output color encoding for prepared rasters.
    color_mode: ColorMode
    #: Whether to deskew the prepared raster.
    deskew: bool
    #: Whether to denoise the prepared raster.
    denoise: bool
    #: Crop strategy applied before subdivision.
    crop_mode: CropMode
    #: Binarization strategy applied to the prepared raster.
    binarize_mode: BinarizeMode
    #: Dewarp strategy applied to the prepared raster.
    dewarp_mode: DewarpMode
    #: Vertical overlap between fixed tiles in pixels.
    subdivision_overlap_px: int = Field(ge=0)
    #: Fixed tile height in pixels for subdivision.
    fixed_tile_height_px: int = Field(gt=0)
    #: Calibratable quality thresholds for assessment.
    thresholds: AssessmentThresholds
    #: Optional operator notes about calibration or scope.
    notes: str | None = None

    @model_validator(mode="after")
    def validate_subdivision_geometry(self) -> PreparationRecipe:
        """
        Keep tile overlap strictly smaller than tile height.

        Returns:
            The validated preparation recipe.

        Raises:
            ValueError: If overlap is not smaller than tile height.

        """
        if self.subdivision_overlap_px >= self.fixed_tile_height_px:
            msg = "subdivision_overlap_px must be smaller than fixed_tile_height_px"
            raise ValueError(msg)
        return self


class SourcePageArtifact(SchemaModel):
    """One acquired source page before preparation."""

    #: Stable artifact identifier for the source page raster.
    artifact_id: str
    #: Stable source-page identifier within the document.
    source_page_id: str
    #: One-based page number in source order.
    page_number: int
    #: Filesystem-relative path to the acquired source raster.
    source_path: str
    #: Original source filename when available.
    source_filename: str
    #: Digest binding the acquired source raster bytes.
    checksum: str
    #: Acquisition mode used for PDF sources when applicable.
    acquisition_mode: PdfPageImageMode | None
    #: Coordinate identity and dimensions for the source raster.
    coordinate_space: CoordinateSpace


class QualitySignal(SchemaModel):
    """One measured image-quality signal from preparation assessment."""

    #: Stable signal identifier such as ``contrast_stddev``.
    signal_id: str
    #: Measured numeric value when available.
    value: float | None
    #: Measurement unit when applicable.
    unit: str | None
    #: Severity when the signal crosses a threshold.
    severity: FlagSeverity
    #: Whether the signal was measured or inferred.
    measured: bool


class PreparationAssessment(SchemaModel):
    """Assessment outcome for one source page."""

    #: Stable assessment identifier.
    assessment_id: str
    #: Source page identifier under assessment.
    source_page_id: str
    #: Prepared-page identifier when preparation completed.
    prepared_page_id: str | None
    #: Measured quality signals for the page.
    signals: list[QualitySignal]
    #: Raised assessment flags.
    flags: list[str]
    #: Recommended follow-up actions for operators.
    recommended_actions: list[str]
    #: Non-blocking assessment warnings.
    warnings: list[str]
    #: Automatically suggested page class.
    page_class_suggested: PageClass
    #: Final page class used for preparation.
    page_class_final: PageClass
    #: Whether the final page class came from automation or an operator.
    page_class_source: Literal["auto", "operator"]
    #: Operator explanation when ``page_class_source`` is ``operator``.
    operator_override_reason: str | None

    @model_validator(mode="after")
    def validate_operator_override(self) -> PreparationAssessment:
        """
        Require a non-empty reason for operator page-class overrides.

        Returns:
            The validated preparation assessment.

        Raises:
            ValueError: If an operator override lacks a reason.

        """
        if self.page_class_source == "operator" and not self.operator_override_reason:
            msg = (
                "operator_override_reason is required when "
                "page_class_source is operator"
            )
            raise ValueError(msg)
        return self


class PreparationResult(SchemaModel):
    """Full preparation outcome for one source page."""

    #: Acquired source page artifact.
    source_page: SourcePageArtifact
    #: Prepared page artifact and subdivisions.
    prepared_page: PreparedPage
    #: Quality assessment for the prepared page.
    assessment: PreparationAssessment
    #: Whether preparation mode came from automation or an operator.
    preparation_choice_source: Literal["auto", "operator"]
    #: Operator explanation when ``preparation_choice_source`` is ``operator``.
    operator_override_reason: str | None

    @model_validator(mode="after")
    def validate_operator_override(self) -> PreparationResult:
        """
        Require a non-empty reason for operator preparation overrides.

        Returns:
            The validated preparation result.

        Raises:
            ValueError: If an operator override lacks a reason.

        """
        if (
            self.preparation_choice_source == "operator"
            and not self.operator_override_reason
        ):
            msg = (
                "operator_override_reason is required when "
                "preparation_choice_source is operator"
            )
            raise ValueError(msg)
        return self
