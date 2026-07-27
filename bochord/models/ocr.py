# Copyright (C) 2026 Chris Malek.
"""Canonical OCR contract models for bundles, review, gold data, and RAG."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SchemaModel(BaseModel):
    """Shared strict base model for all exported OCR contracts."""

    #: Forbid unknown keys so exported JSON stays stable and reviewable.
    model_config = ConfigDict(extra="forbid")


class SourceType(StrEnum):
    """Supported top-level source kinds."""

    #: A multi-page PDF source that must be rendered or image-extracted per page.
    PDF = "pdf"
    #: An ordered collection of page images, regardless of image format.
    IMAGE_SET = "image-set"
    #: One standalone page image treated as a one-page document.
    SINGLE_IMAGE = "single-image"


class TrustState(StrEnum):
    """Human-review trust level for accepted graph content."""

    #: Machine-produced content with no human acceptance or correction yet.
    MACHINE = "machine"
    #: Human-checked content accepted without changing the machine result.
    REVIEWED = "reviewed"
    #: Human-corrected content that differs from the machine result.
    CORRECTED = "corrected"


class FontWeight(StrEnum):
    """Visual font-weight classification independent of other typography."""

    #: Glyph strokes have ordinary weight for the local typeface.
    REGULAR = "regular"
    #: Glyph strokes are visibly heavier than the local ordinary face.
    BOLD = "bold"
    #: Available evidence cannot establish the weight reliably.
    UNKNOWN = "unknown"


class FontSlant(StrEnum):
    """Visual font-slant classification independent of weight and role."""

    #: Glyphs use the local upright or roman face.
    UPRIGHT = "upright"
    #: Glyphs use an italic or oblique face.
    ITALIC = "italic"
    #: Available evidence cannot establish the slant reliably.
    UNKNOWN = "unknown"


class BaselineShift(StrEnum):
    """Vertical placement of a span relative to the local baseline."""

    #: Text sits on the ordinary line baseline.
    BASELINE = "baseline"
    #: Text is raised above the ordinary baseline.
    SUPERSCRIPT = "superscript"
    #: Text is lowered below the ordinary baseline.
    SUBSCRIPT = "subscript"
    #: Available evidence cannot establish the baseline relationship reliably.
    UNKNOWN = "unknown"


class TextRole(StrEnum):
    """Semantic role kept separate from visual typography."""

    #: Ordinary text without a more specific semantic role.
    TEXT = "text"
    #: A marker that points from running text to a note body.
    FOOTNOTE_MARKER = "footnote-marker"
    #: The span's semantic role remains unresolved.
    UNKNOWN = "unknown"


class RegionKind(StrEnum):
    """Accepted region classes for the page graph."""

    #: Ordinary main reading text for the page.
    BODY = "body"
    #: A note region, usually a footnote block separated from body text.
    FOOTNOTE = "footnote"
    #: Margin text or annotations that are not part of the main body block.
    MARGINALIA = "marginalia"
    #: Running header or other top-of-page header matter.
    HEADER = "header"
    #: Running footer, catchword, or other bottom-of-page footer matter.
    FOOTER = "footer"
    #: Table-like material that should not be flattened as ordinary prose.
    TABLE = "table"
    #: Front matter, side matter, or other non-body text not better
    #: classified elsewhere.
    PARATEXT = "paratext"
    #: A region whose class remains unresolved after current processing.
    UNKNOWN = "unknown"


class NoteKind(StrEnum):
    """Accepted note classes for v1."""

    #: A footnote body block associated with one or more inline markers.
    FOOTNOTE_BLOCK = "footnote-block"
    #: A note body collected outside the local page flow as an endnote.
    ENDNOTE_BLOCK = "endnote-block"
    #: A side note or marginal note treated as a note object.
    SIDE_NOTE = "side-note"
    #: A note-like object whose subtype is still unresolved.
    UNKNOWN = "unknown"


class PageClass(StrEnum):
    """Page-level layout cohorts used by preparation and evaluation."""

    #: Mostly regular prose with limited structural complication.
    ORDINARY_PROSE = "ordinary-prose"
    #: Small-type dictionary or glossary pages likely to need subdivision.
    DENSE_DICTIONARY = "dense-dictionary"
    #: Pages with substantial note activity relative to body text.
    NOTE_HEAVY = "note-heavy"
    #: Pages dominated by tables or tabular layout.
    TABLE_HEAVY = "table-heavy"
    #: Mixed or irregular pages that do not fit the simpler cohorts well.
    MIXED_COMPLEX = "mixed-complex"


class PreparationMode(StrEnum):
    """Prepared-page subdivision modes."""

    #: Use the whole prepared page as one OCR input unit.
    FULL_PAGE = "full-page"
    #: Split the page into column-based OCR units.
    COLUMNS = "columns"
    #: Split the page into fixed tiles when columns are insufficient.
    FIXED_TILES = "fixed-tiles"


class InputKind(StrEnum):
    """Runner input artifact categories."""

    #: A page image or prepared unit image fed directly to a runner.
    IMAGE = "image"
    #: A prepared subdivision of one logical page.
    PREPARED_UNIT = "prepared-unit"
    #: A PDF artifact used as the concrete runner input.
    PDF = "pdf"


class BatchUnitKind(StrEnum):
    """Batch grouping units for runner execution."""

    #: Batch items correspond to whole logical pages.
    PAGE = "page"
    #: Batch items correspond to subdivided prepared units.
    PREPARED_UNIT = "prepared-unit"
    #: Batch items correspond to packaged PDF documents.
    PDF_DOCUMENT = "pdf-document"


class PackagingStrategy(StrEnum):
    """Runner packaging policies."""

    #: Feed the prepared artifact directly without repackaging.
    DIRECT = "direct"
    #: Convert one or more prepared images into a PDF before execution.
    IMAGE_TO_PDF = "image-to-pdf"
    #: Package prepared subdivisions together into a batched PDF artifact.
    UNIT_TO_PDF_BATCH = "unit-to-pdf-batch"


class BatchResultStatus(StrEnum):
    """Execution outcome for one runner batch."""

    #: Every batch item completed and produced the expected outputs.
    SUCCEEDED = "succeeded"
    #: Some batch items completed but at least one failed or degraded.
    PARTIAL = "partial"
    #: The batch failed as a unit or produced no usable result.
    FAILED = "failed"


class ReviewScope(StrEnum):
    """Supported human review targets."""

    #: Review applies to page-level state or assessment.
    PAGE = "page"
    #: Review applies to a structural region object.
    REGION = "region"
    #: Review applies to a text line and its geometry or ordering.
    LINE = "line"
    #: Review applies to a note object and its accepted state.
    NOTE = "note"
    #: Review applies to a local text-bearing span object.
    SPAN = "span"


class ReviewDimension(StrEnum):
    """Independent evidence dimensions a human may inspect and certify."""

    #: Fitness and defects of the acquired source image.
    SOURCE_QUALITY = "source-quality"
    #: Crop, rotation, enhancement, and subdivision choices.
    PREPARATION = "preparation"
    #: Regions, lines, geometry, and reading order.
    STRUCTURE = "structure"
    #: Diplomatic transcription against the source image.
    TEXT = "text"
    #: Font family, size, weight, slant, and baseline placement.
    TYPOGRAPHY = "typography"
    #: Marker-to-note and note-body relationships.
    NOTE_LINKAGE = "note-linkage"


class ReviewTaskType(StrEnum):
    """Operator workflow represented by a review task packet."""

    #: Decide whether an acquired page is usable or requires reacquisition.
    SOURCE_TRIAGE = "source-triage"
    #: Choose or verify preparation and page subdivision.
    PREPARATION = "preparation"
    #: Correct page regions, lines, geometry, and reading order.
    LAYOUT = "layout"
    #: Verify or correct diplomatic transcription.
    TEXT = "text"
    #: Verify or correct independent typography facets.
    TYPOGRAPHY = "typography"
    #: Verify or correct marker-to-note relationships.
    NOTE_LINKAGE = "note-linkage"
    #: Create trusted evaluation annotations with explicit coverage.
    GOLD = "gold"
    #: Resolve conflicting or abstained review decisions.
    ADJUDICATION = "adjudication"


class ReviewTaskStatus(StrEnum):
    """Lifecycle state for a human review task."""

    #: Work has not yet been certified by an operator.
    PENDING = "pending"
    #: Required dimensions and coverage were inspected and certified.
    COMPLETED = "completed"
    #: Operator could not make a defensible decision from the evidence.
    ABSTAINED = "abstained"
    #: Conflicting evidence or decisions require adjudication.
    NEEDS_ADJUDICATION = "needs-adjudication"


class DatasetSplit(StrEnum):
    """Benchmark partition assigned before model comparison."""

    #: Examples available for development and model adaptation.
    TRAIN = "train"
    #: Examples used for development decisions but not final reporting.
    DEVELOPMENT = "development"
    #: Held-out examples used only for final comparative evaluation.
    TEST = "test"


class FlagSeverity(StrEnum):
    """Severity levels for review and evaluation flags."""

    #: Informational flag worth surfacing but not urgent.
    INFO = "info"
    #: Warning flag that likely deserves operator attention.
    WARNING = "warning"
    #: Error-level flag indicating materially broken or unsafe output.
    ERROR = "error"


class ReviewAction(StrEnum):
    """Verb vocabulary for append-only review events."""

    #: Human accepts the target unchanged after review.
    ACCEPT = "accept"
    #: Human replaces the accepted text for the target object.
    CORRECT_TEXT = "correct_text"
    #: Human changes accepted typography facets or semantic text roles.
    CORRECT_STYLE = "correct_style"
    #: Human replaces target geometry in the named coordinate space.
    CORRECT_GEOMETRY = "correct_geometry"
    #: Human replaces reading order for objects within one parent.
    REORDER = "reorder"
    #: Human changes the semantic class of a structural region.
    RECLASSIFY_REGION = "reclassify_region"
    #: Human certifies that source content cannot be read defensibly.
    MARK_ILLEGIBLE = "mark_illegible"
    #: Human asserts a marker-to-note linkage.
    LINK_NOTE = "link_note"
    #: Human removes a previously accepted marker-to-note linkage.
    UNLINK_NOTE = "unlink_note"
    #: Human replaces one accepted region with multiple regions.
    SPLIT_REGION = "split_region"
    #: Human replaces multiple accepted regions with one merged region.
    MERGE_REGION = "merge_region"
    #: Human records ambiguity or a problem without forcing a correction.
    FLAG = "flag"
    #: Human closes an existing review flag with an auditable resolution.
    RESOLVE_FLAG = "resolve_flag"


class TransformKind(StrEnum):
    """Preparation transform families recorded between image spaces."""

    #: Crop a rectangular area from a parent image space.
    CROP = "crop"
    #: Change image dimensions while preserving coordinate correspondence.
    SCALE = "scale"
    #: Rotate an image by an explicit angle.
    ROTATE = "rotate"
    #: Correct measured skew while retaining the transform record.
    DESKEW = "deskew"
    #: Apply a non-linear page-flattening transform.
    DEWARP = "dewarp"


class ChunkType(StrEnum):
    """Retrieval chunk families."""

    #: A retrieval chunk derived from one accepted region.
    REGION = "region_chunk"
    #: A retrieval chunk derived from one accepted footnote or note object.
    FOOTNOTE = "footnote_chunk"
    #: A retrieval chunk reserved for table-specific exports.
    TABLE = "table_chunk"


class BoundingBox(SchemaModel):
    """Axis-aligned rectangle for page-relative geometry."""

    #: Left edge in page coordinate units.
    x0: float
    #: Top edge in page coordinate units.
    y0: float
    #: Right edge in page coordinate units.
    x1: float
    #: Bottom edge in page coordinate units.
    y1: float
    #: Stable coordinate-space identifier in which the values are expressed.
    coordinate_space_id: str = "prepared-page"

    @model_validator(mode="after")
    def validate_positive_area(self) -> BoundingBox:
        """
        Reject empty, reversed, or negative page geometry.

        Returns:
            The validated bounding box.

        Raises:
            ValueError: If the rectangle is not a positive page area.

        """
        if self.x0 < 0 or self.y0 < 0 or self.x1 <= self.x0 or self.y1 <= self.y0:
            msg = "bounding boxes require non-negative origins and positive area"
            raise ValueError(msg)
        return self


class Point(SchemaModel):
    """One point in an identified image coordinate space."""

    #: Horizontal coordinate in the named space.
    x: float = Field(ge=0)
    #: Vertical coordinate in the named space.
    y: float = Field(ge=0)


class Polygon(SchemaModel):
    """Polygon geometry for non-rectangular regions and curved text lines."""

    #: Stable coordinate-space identifier for every point.
    coordinate_space_id: str
    #: Ordered polygon vertices; at least three are required.
    points: list[Point] = Field(min_length=3)


class CoordinateSpace(SchemaModel):
    """Identity and dimensions for a source or prepared image space."""

    #: Stable identifier referenced by boxes, polygons, and transforms.
    space_id: str
    #: Raster width in pixels.
    width_px: int = Field(gt=0)
    #: Raster height in pixels.
    height_px: int = Field(gt=0)
    #: Effective resolution when known.
    dpi: float | None = Field(default=None, gt=0)
    #: Parent space before the transform chain, when applicable.
    parent_space_id: str | None = None


class CoordinateTransform(SchemaModel):
    """Replayable mapping between two recorded coordinate spaces."""

    #: Preparation operation represented by this transform.
    kind: TransformKind
    #: Input coordinate-space identifier.
    source_space_id: str
    #: Output coordinate-space identifier.
    target_space_id: str
    #: Numeric operation parameters such as crop edges or rotation angle.
    parameters: dict[str, float] = Field(default_factory=dict)
    #: Artifact containing a non-linear mapping when parameters are insufficient.
    mapping_artifact_path: str | None = None


class FontFamilyCandidate(SchemaModel):
    """One possible font-family label with evidence confidence."""

    #: Typeface or model-supplied family label.
    name: str
    #: Confidence assigned to this candidate.
    confidence: float = Field(ge=0, le=1)


class Typography(SchemaModel):
    """Orthogonal visual typography facets for one text span."""

    #: Candidate font-family labels ordered by preference.
    font_families: list[FontFamilyCandidate] = Field(default_factory=list)
    #: Estimated local font size in typographic points.
    font_size_points: float | None = Field(default=None, gt=0)
    #: Confidence in the font-size estimate.
    font_size_confidence: float | None = Field(default=None, ge=0, le=1)
    #: Independent font-weight classification.
    weight: FontWeight = FontWeight.UNKNOWN
    #: Independent font-slant classification.
    slant: FontSlant = FontSlant.UNKNOWN
    #: Independent baseline-placement classification.
    baseline_shift: BaselineShift = BaselineShift.UNKNOWN
    #: Whether the face uses small capitals, when determinable.
    small_caps: bool | None = None
    #: Whether the span is intentionally letter-spaced, when determinable.
    letter_spaced: bool | None = None


class BibliographicProvenance(SchemaModel):
    """Stable descriptive metadata for the source work."""

    #: Human-readable work title.
    title: str
    #: Listed creator names in bibliographic order.
    authors: list[str]
    #: Publication year when known.
    publication_year: int | None = None
    #: Publisher or issuing body when known.
    publisher: str | None = None
    #: Edition or printing note when relevant.
    edition: str | None = None
    #: Shelfmark, call number, or local holding id when known.
    shelfmark: str | None = None
    #: Bibliographic note for anything not captured elsewhere.
    bibliographic_note: str | None = None


class AcquisitionProvenance(SchemaModel):
    """How the source files were obtained."""

    #: Acquisition channel such as ``archive-org`` or ``local-scan``.
    acquisition_kind: str
    #: Human-readable source label or provider.
    acquired_from: str
    #: URL or external identifier for the acquisition source.
    source_uri: str | None = None
    #: Timestamp describing when the source was acquired.
    acquired_at_utc: datetime | None = None
    #: Rights, restrictions, or operator notes about use.
    rights_note: str | None = None


class SourceDescriptor(SchemaModel):
    """Top-level input identity for one OCR document."""

    #: Stable source identifier for this input bundle.
    source_id: str
    #: Whether the input was a PDF, image set, or single image.
    source_type: SourceType
    #: Human-readable source filename or label.
    source_label: str
    #: Original filesystem path or import path.
    original_path: str
    #: Source page count when known.
    page_count: int | None = None
    #: Digest of the original source artifact when available.
    checksum: str | None = None


class RunnerReference(SchemaModel):
    """Identity for one runner implementation and model revision."""

    #: Stable logical runner id such as ``olmocr`` or ``kraken-layout``.
    runner_id: str
    #: Runner package or integration version when known.
    runner_version: str | None = None
    #: Underlying model name when relevant.
    model_name: str | None = None
    #: Underlying model revision or digest when relevant.
    model_revision: str | None = None
    #: Runtime or hosting backend, such as ``huggingface-endpoint``.
    runtime_name: str | None = None
    #: Container, runtime, or endpoint revision used for execution.
    runtime_revision: str | None = None
    #: Digest of runner configuration excluding secrets.
    config_digest: str | None = None
    #: Digest of the exact prompt or prompt template when one is used.
    prompt_digest: str | None = None

    @model_validator(mode="after")
    def validate_model_reproducibility(self) -> RunnerReference:
        """
        Require immutable evidence identity for model-backed runners.

        Returns:
            The validated runner reference.

        Raises:
            ValueError: If a named model lacks reproducibility metadata.

        """
        required = (
            self.model_revision,
            self.runtime_name,
            self.runtime_revision,
            self.config_digest,
            self.prompt_digest,
        )
        if self.model_name is not None and any(value is None for value in required):
            msg = "model-backed runners require model, runtime, and config revisions"
            raise ValueError(msg)
        if self.model_name is not None and (
            self.runtime_name is None
            or not self.runtime_name.startswith("huggingface")
        ):
            msg = "model-backed runners must use a Hugging Face hosted runtime"
            raise ValueError(msg)
        return self


class RunnerCapability(SchemaModel):
    """Declared pass-runner input and batching contract."""

    #: Input kinds this runner can consume without repackaging.
    accepted_input_kinds: list[InputKind]
    #: Preferred input kind for best quality or throughput.
    preferred_input_kind: InputKind
    #: Whether the runner can process more than one item per invocation.
    supports_multi_item_batching: bool
    #: Unit by which batching is defined for this runner.
    batch_unit_kind: BatchUnitKind
    #: Packaging policy required before invocation.
    packaging_strategy: PackagingStrategy

    @model_validator(mode="after")
    def validate_preferred_input(self) -> RunnerCapability:
        """
        Ensure the preferred input is accepted by the runner.

        Returns:
            The validated capability declaration.

        Raises:
            ValueError: If accepted inputs are empty or exclude the preference.

        """
        if not self.accepted_input_kinds:
            msg = "accepted_input_kinds must not be empty"
            raise ValueError(msg)
        if self.preferred_input_kind not in self.accepted_input_kinds:
            msg = "preferred_input_kind must appear in accepted_input_kinds"
            raise ValueError(msg)
        return self


class PreparedArtifactRef(SchemaModel):
    """Prepared image or packaged artifact ready for runner execution."""

    #: Stable artifact identifier within the document bundle.
    artifact_id: str
    #: Concrete artifact kind consumed by the runner.
    kind: InputKind
    #: Owning page identifier.
    page_id: str
    #: Prepared-unit identifier when the artifact is a subdivision.
    prepared_unit_id: str | None = None
    #: Filesystem-relative bundle path for this artifact.
    artifact_path: str
    #: Parent prepared-page identifier for prepared units.
    parent_prepared_page_id: str | None = None
    #: Digest binding the prepared artifact bytes.
    checksum: str | None = None
    #: Reading-order position for prepared units.
    order: int | None = Field(default=None, ge=1)
    #: Bounding box for the prepared unit within the source page when applicable.
    bounding_box: BoundingBox | None = None

    @model_validator(mode="after")
    def validate_prepared_unit_requirements(self) -> PreparedArtifactRef:
        """
        Require lineage and geometry for prepared-unit artifacts.

        Returns:
            The validated prepared artifact reference.

        Raises:
            ValueError: If a prepared unit lacks required metadata.

        """
        if self.kind != InputKind.PREPARED_UNIT:
            return self
        missing: list[str] = []
        if (
            self.parent_prepared_page_id is None
            or not self.parent_prepared_page_id.strip()
        ):
            missing.append("parent_prepared_page_id")
        if self.checksum is None or not self.checksum.strip():
            missing.append("checksum")
        if self.order is None:
            missing.append("order")
        if self.bounding_box is None:
            missing.append("bounding_box")
        if missing:
            msg = f"prepared units require {', '.join(missing)}"
            raise ValueError(msg)
        return self


class BatchItemRef(SchemaModel):
    """One source item included in a runner execution batch."""

    #: Stable batch-item identifier.
    item_id: str
    #: Owning page identifier.
    source_page_id: str
    #: Prepared-unit identifier when batching subdivisions.
    prepared_unit_id: str | None = None
    #: Artifact identifier actually fed into the runner.
    artifact_id: str


class RunnerOutputArtifact(SchemaModel):
    """One raw witness artifact emitted by a pass runner."""

    #: Stable result artifact identifier.
    artifact_id: str
    #: Artifact family such as ``text`` or ``layout``.
    artifact_kind: str
    #: Filesystem-relative output path.
    artifact_path: str
    #: Media type or serialization hint such as ``application/json``.
    media_type: str
    #: Batch items represented by this output artifact.
    batch_item_ids: list[str] = Field(min_length=1)


class RunnerExecutionBatch(SchemaModel):
    """Exact persisted record for one runner invocation."""

    #: Persisted runner-batch schema version.
    schema_version: str
    #: Stable batch identifier.
    batch_id: str
    #: Execution run identifier that owns this batch.
    run_id: str
    #: Document identifier under processing.
    document_id: str
    #: Runner identity used for this invocation.
    runner: RunnerReference
    #: Declared capability contract used by this invocation.
    capability: RunnerCapability
    #: Artifact id of the packaged batch input when created.
    packaging_artifact_id: str | None = None
    #: Number of items submitted in this invocation.
    batch_size: int = Field(gt=0)
    #: Exact items included in execution order.
    items: list[BatchItemRef]
    #: When invocation started.
    started_at_utc: datetime
    #: When invocation ended.
    finished_at_utc: datetime | None = None
    #: Retry source batch when this is a rerun.
    retry_of_batch_id: str | None = None
    #: Human-readable retry strategy label.
    retry_strategy: str | None = None
    #: Whether the invocation succeeded fully, partially, or failed.
    result_status: BatchResultStatus
    #: Item ids that failed when result status is partial or failed.
    failure_item_ids: list[str] = Field(default_factory=list)
    #: Output witness artifacts produced by this invocation.
    output_artifacts: list[RunnerOutputArtifact] = Field(default_factory=list)
    #: Warnings or non-fatal execution notes.
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_batch_consistency(self) -> RunnerExecutionBatch:
        """
        Keep counts, status, failures, timing, and outputs internally coherent.

        Returns:
            The validated execution batch.

        Raises:
            ValueError: If persisted execution facts contradict each other.

        """
        item_ids = [item.item_id for item in self.items]
        if self.batch_size != len(item_ids):
            msg = "batch_size must equal the number of batch items"
            raise ValueError(msg)
        if len(set(item_ids)) != len(item_ids):
            msg = "batch item ids must be unique"
            raise ValueError(msg)
        if not set(self.failure_item_ids).issubset(item_ids):
            msg = "failure_item_ids must identify submitted batch items"
            raise ValueError(msg)
        if self.result_status is BatchResultStatus.SUCCEEDED and self.failure_item_ids:
            msg = "succeeded batches cannot contain failed items"
            raise ValueError(msg)
        if self.result_status is BatchResultStatus.PARTIAL and (
            not self.failure_item_ids or len(self.failure_item_ids) == len(item_ids)
        ):
            msg = "partial batches require some but not all items to fail"
            raise ValueError(msg)
        if self.result_status is BatchResultStatus.FAILED and (
            set(self.failure_item_ids) != set(item_ids)
        ):
            msg = "failed batches must identify every submitted item as failed"
            raise ValueError(msg)
        if (
            self.finished_at_utc is not None
            and self.finished_at_utc < self.started_at_utc
        ):
            msg = "finished_at_utc cannot precede started_at_utc"
            raise ValueError(msg)
        for artifact in self.output_artifacts:
            if not set(artifact.batch_item_ids).issubset(item_ids):
                msg = "output artifacts must identify submitted batch items"
                raise ValueError(msg)
        return self


class WitnessReference(SchemaModel):
    """Pointer from accepted graph content back to raw machine evidence."""

    #: Stable witness artifact identifier.
    witness_id: str
    #: Witness family such as ``text`` or ``style``.
    witness_kind: str
    #: Artifact path for later audit.
    artifact_path: str
    #: Runner that emitted this witness.
    runner_id: str
    #: Owning page identifier.
    page_id: str
    #: Prepared-unit identifier when the witness came from a subdivision.
    prepared_unit_id: str | None = None


class ObjectProvenance(SchemaModel):
    """Accepted-object provenance pointers."""

    #: Page identifier from which the object ultimately derives.
    source_page_id: str
    #: Witness artifact ids that contributed to the accepted object.
    witness_ids: list[str]
    #: Runner ids that contributed to the accepted object.
    runner_ids: list[str]
    #: Confidence reported by the producing or merge stage when available.
    machine_confidence: float | None = Field(default=None, ge=0, le=1)
    #: Confidence assigned by merge logic when available.
    merge_confidence: float | None = Field(default=None, ge=0, le=1)
    #: Short disagreement note when sources materially conflicted.
    disagreement_note: str | None = None


class ReviewSummary(SchemaModel):
    """Compact review state attached to accepted graph objects."""

    #: Evidence dimensions explicitly inspected by a human.
    reviewed_dimensions: list[ReviewDimension] = Field(default_factory=list)
    #: Evidence dimensions changed by a human correction.
    corrected_dimensions: list[ReviewDimension] = Field(default_factory=list)
    #: Most recent event id that changed or affirmed this object.
    last_event_id: str | None = None
    #: Ordered review events applied to this object.
    event_ids: list[str] = Field(default_factory=list)


class MetricScore(SchemaModel):
    """One numeric evaluation metric."""

    #: Stable metric identifier such as ``character_error_rate``.
    metric_id: str
    #: Metric value as computed for the target scope.
    value: float
    #: Optional numerator used to derive the metric.
    numerator: float | None = None
    #: Optional denominator used to derive the metric.
    denominator: float | None = None
    #: Human-readable note explaining the metric context.
    note: str | None = None


class EvaluationFlag(SchemaModel):
    """One review-driving evaluation flag."""

    #: Stable flag identifier.
    flag_id: str
    #: Short machine-readable flag type.
    flag_type: str
    #: Severity level for triage.
    severity: FlagSeverity
    #: Human-readable message for the operator.
    message: str
    #: Optional object ids implicated by this flag.
    target_object_ids: list[str] = Field(default_factory=list)


class EvaluationFamilySummary(SchemaModel):
    """Scores and flags for one evaluation family."""

    #: Metrics emitted for this family.
    metrics: list[MetricScore] = Field(default_factory=list)
    #: Flags emitted for this family.
    flags: list[EvaluationFlag] = Field(default_factory=list)


class StyleEvaluationSummary(SchemaModel):
    """Typography and note-linkage scores grouped under the style family."""

    #: Typography metrics and flags, scored per independent visual facet.
    typography: EvaluationFamilySummary = Field(
        default_factory=EvaluationFamilySummary
    )
    #: Marker-role and marker-to-note linkage metrics and flags.
    note_linkage: EvaluationFamilySummary = Field(
        default_factory=EvaluationFamilySummary
    )


class PageEvaluationSummary(SchemaModel):
    """Per-page grouped evaluation output."""

    #: Text-fidelity metrics and flags.
    text: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    #: Structure metrics and flags.
    structure: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    #: Typography and note-linkage metrics and flags.
    style: StyleEvaluationSummary = Field(default_factory=StyleEvaluationSummary)


class PreparedPage(SchemaModel):
    """Preparation outcome for one page."""

    #: Stable prepared-page identifier within the document bundle.
    prepared_page_id: str
    #: Accepted preparation mode for the page.
    preparation_mode: PreparationMode
    #: Final page-class label used by later stages.
    page_class: PageClass
    #: Filesystem-relative path for the canonical prepared page image.
    image_path: str
    #: Artifact identifier of the source page before preparation.
    source_artifact_id: str
    #: Digest binding geometry and review to the exact prepared image.
    image_checksum: str
    #: Recipe identifier or digest used to prepare this page.
    preparation_recipe_id: str
    #: Canonical coordinate identity and raster dimensions for this image.
    coordinate_space: CoordinateSpace
    #: Ordered source-to-prepared transform chain.
    transforms: list[CoordinateTransform] = Field(default_factory=list)
    #: Prepared subdivisions preserved for runner use.
    prepared_units: list[PreparedArtifactRef] = Field(default_factory=list)


class SpanRecord(SchemaModel):
    """Accepted text span in the page graph."""

    #: Stable span identifier.
    span_id: str
    #: Parent line identifier.
    line_id: str
    #: Diplomatic text preserving source graphemes.
    text_diplomatic: str
    #: Deterministically normalized text when available.
    text_normalized: str | None = None
    #: Independent visual typography facets.
    typography: Typography = Field(default_factory=Typography)
    #: Semantic roles kept separate from visual typography.
    roles: list[TextRole] = Field(default_factory=lambda: [TextRole.TEXT])
    #: Bounding box for the span when available.
    bounding_box: BoundingBox | None = None
    #: Current trust state for this span.
    trust_state: TrustState = TrustState.MACHINE
    #: Evidence pointers supporting this span.
    provenance: ObjectProvenance
    #: Review summary for this span.
    review: ReviewSummary = Field(default_factory=ReviewSummary)


class LineRecord(SchemaModel):
    """Accepted line node in the page graph."""

    #: Stable line identifier.
    line_id: str
    #: Parent region identifier.
    region_id: str
    #: Line reading-order position inside the region.
    line_order: int
    #: Bounding box for the accepted line.
    bounding_box: BoundingBox | None = None
    #: Polygon for non-rectangular line extent when available.
    polygon: Polygon | None = None
    #: Baseline polyline points in reading order when available.
    baseline: list[Point] = Field(default_factory=list)
    #: Ordered span identifiers contained by the line.
    span_ids: list[str]
    #: Current trust state for this line.
    trust_state: TrustState = TrustState.MACHINE
    #: Evidence pointers supporting this line.
    provenance: ObjectProvenance
    #: Review summary for this line.
    review: ReviewSummary = Field(default_factory=ReviewSummary)
    #: Optional joined successor line when this line continues on the next line.
    joins_to_line_id: str | None = None


class NoteRecord(SchemaModel):
    """Accepted note object in the page graph."""

    #: Stable note identifier.
    note_id: str
    #: Accepted note class.
    note_kind: NoteKind
    #: Parent region identifier when the note lives in a region.
    region_id: str | None = None
    #: Diplomatic note text.
    text_diplomatic: str
    #: Deterministically normalized note text when available.
    text_normalized: str | None = None
    #: Marker span ids linked to this note.
    linked_marker_span_ids: list[str] = Field(default_factory=list)
    #: Bounding box for the note block when available.
    bounding_box: BoundingBox | None = None
    #: Current trust state for this note.
    trust_state: TrustState = TrustState.MACHINE
    #: Evidence pointers supporting this note.
    provenance: ObjectProvenance
    #: Review summary for this note.
    review: ReviewSummary = Field(default_factory=ReviewSummary)


class RegionRecord(SchemaModel):
    """Accepted region node in the page graph."""

    #: Stable region identifier.
    region_id: str
    #: Accepted region class.
    region_kind: RegionKind
    #: Page reading-order position for this region.
    reading_order_index: int
    #: Bounding box for the accepted region.
    bounding_box: BoundingBox | None = None
    #: Polygon for non-rectangular region extent when available.
    polygon: Polygon | None = None
    #: Ordered line identifiers contained by the region.
    line_ids: list[str]
    #: Note identifiers logically linked to the region.
    note_ids: list[str] = Field(default_factory=list)
    #: Current trust state for this region.
    trust_state: TrustState = TrustState.MACHINE
    #: Evidence pointers supporting this region.
    provenance: ObjectProvenance
    #: Review summary for this region.
    review: ReviewSummary = Field(default_factory=ReviewSummary)


class BundlePage(SchemaModel):
    """Canonical exported page object."""

    #: Stable page identifier.
    page_id: str
    #: One-based page number within the source order.
    page_number: int
    #: Human-readable label for the source page image when needed.
    source_page_label: str | None = None
    #: Accepted preparation output for this page.
    prepared_page: PreparedPage
    #: Witness artifacts produced for this page.
    witnesses: list[WitnessReference] = Field(default_factory=list)
    #: Accepted regions for this page.
    regions: list[RegionRecord] = Field(default_factory=list)
    #: Accepted lines for this page.
    lines: list[LineRecord] = Field(default_factory=list)
    #: Accepted spans for this page.
    spans: list[SpanRecord] = Field(default_factory=list)
    #: Accepted notes for this page.
    notes: list[NoteRecord] = Field(default_factory=list)
    #: Per-page evaluation summary.
    evaluation_summary: PageEvaluationSummary = Field(
        default_factory=PageEvaluationSummary
    )
    #: Review events applied to this page or its children.
    review_event_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_graph_references(self) -> BundlePage:  # noqa: PLR0912
        """
        Reject duplicate ids and dangling page-graph references.

        Returns:
            The validated bundle page.

        Raises:
            ValueError: If a graph id is duplicated or cannot be resolved.

        """
        region_ids = [region.region_id for region in self.regions]
        line_ids = [line.line_id for line in self.lines]
        span_ids = [span.span_id for span in self.spans]
        note_ids = [note.note_id for note in self.notes]
        for label, identifiers in (
            ("region", region_ids),
            ("line", line_ids),
            ("span", span_ids),
            ("note", note_ids),
        ):
            if len(set(identifiers)) != len(identifiers):
                msg = f"{label} ids must be unique within a page"
                raise ValueError(msg)
        region_id_set = set(region_ids)
        line_id_set = set(line_ids)
        span_id_set = set(span_ids)
        note_id_set = set(note_ids)
        for region in self.regions:
            if not set(region.line_ids).issubset(line_id_set):
                msg = f"region {region.region_id} references an unknown line"
                raise ValueError(msg)
            if not set(region.note_ids).issubset(note_id_set):
                msg = f"region {region.region_id} references an unknown note"
                raise ValueError(msg)
        for line in self.lines:
            if line.region_id not in region_id_set:
                msg = f"line {line.line_id} references an unknown region"
                raise ValueError(msg)
            if not set(line.span_ids).issubset(span_id_set):
                msg = f"line {line.line_id} references an unknown span"
                raise ValueError(msg)
            if (
                line.joins_to_line_id is not None
                and line.joins_to_line_id not in line_id_set
            ):
                msg = f"line {line.line_id} references an unknown joined line"
                raise ValueError(msg)
        for span in self.spans:
            if span.line_id not in line_id_set:
                msg = f"span {span.span_id} references an unknown line"
                raise ValueError(msg)
        for note in self.notes:
            if note.region_id is not None and note.region_id not in region_id_set:
                msg = f"note {note.note_id} references an unknown region"
                raise ValueError(msg)
            if not set(note.linked_marker_span_ids).issubset(span_id_set):
                msg = f"note {note.note_id} references an unknown marker span"
                raise ValueError(msg)
        return self


class DocumentEvaluationSummary(SchemaModel):
    """Document-level grouped evaluation output."""

    #: Text-fidelity metrics and flags across the document.
    text: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    #: Structure metrics and flags across the document.
    structure: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    #: Typography and note-linkage metrics and flags across the document.
    style: StyleEvaluationSummary = Field(default_factory=StyleEvaluationSummary)


class RunMetadata(SchemaModel):
    """Top-level run metadata for one bundle export."""

    #: Stable run identifier.
    run_id: str
    #: When the OCR orchestration run began.
    run_timestamp_utc: datetime
    #: Preparation recipe identifier or digest.
    preparation_recipe_id: str
    #: Digest of the complete run configuration excluding secrets.
    config_digest: str
    #: Runner set participating in the run.
    runner_set: list[RunnerReference]
    #: Bundle schema version used for serialization.
    bundle_schema_version: str


class ExportSummary(SchemaModel):
    """Pointers to derived export artifacts."""

    #: Relative path to the canonical bundle JSON.
    bundle_json_path: str
    #: Relative path to the retrieval chunk stream.
    rag_jsonl_path: str | None = None
    #: Relative path to stitched retrieval chunks.
    stitched_chunks_jsonl_path: str | None = None
    #: Relative path to the Markdown reading export.
    document_markdown_path: str | None = None


class DocumentBundle(SchemaModel):
    """Canonical software-facing document export."""

    #: Stable document identifier.
    document_id: str
    #: Schema version for the exported bundle JSON.
    bundle_schema_version: str
    #: Source identity for the input artifact(s).
    source: SourceDescriptor
    #: Bibliographic metadata kept with the document.
    bibliographic_provenance: BibliographicProvenance
    #: Acquisition metadata kept with the document.
    acquisition_provenance: AcquisitionProvenance
    #: Run metadata describing this export.
    run: RunMetadata
    #: Accepted page objects in source order.
    pages: list[BundlePage]
    #: Aggregated evaluation output for the whole document.
    evaluation_summary: DocumentEvaluationSummary
    #: Pointers to derived exports.
    exports: ExportSummary

    @model_validator(mode="after")
    def validate_bundle_consistency(self) -> DocumentBundle:
        """
        Keep top-level schema identity, page count, and page ids coherent.

        Returns:
            The validated document bundle.

        Raises:
            ValueError: If persisted bundle metadata contradicts its content.

        """
        if self.bundle_schema_version != self.run.bundle_schema_version:
            msg = "bundle and run schema versions must match"
            raise ValueError(msg)
        if (
            self.source.page_count is not None
            and self.source.page_count != len(self.pages)
        ):
            msg = "source page_count must equal exported page count"
            raise ValueError(msg)
        page_ids = [page.page_id for page in self.pages]
        page_numbers = [page.page_number for page in self.pages]
        if len(set(page_ids)) != len(page_ids):
            msg = "page ids must be unique"
            raise ValueError(msg)
        if page_numbers != sorted(page_numbers) or any(
            number < 1 for number in page_numbers
        ):
            msg = "pages must be in positive source order"
            raise ValueError(msg)
        return self


class RetrievalMetadata(SchemaModel):
    """Extra retrieval facets for a flattened chunk."""

    #: Reading-order position of the source region when applicable.
    reading_order_index: int | None = None
    #: One-based page number for chunk-local retrieval.
    page_number: int | None = None
    #: Region class carried into retrieval when relevant.
    region_kind: RegionKind | None = None
    #: Whether any reviewed content is included in the chunk.
    contains_reviewed_content: bool = False
    #: Whether any corrected content is included in the chunk.
    contains_corrected_content: bool = False
    #: Independent typography facets available for filtering.
    typography_signals: list[Typography] = Field(default_factory=list)


class RetrievalProvenance(SchemaModel):
    """Multi-page provenance retained by retrieval exports."""

    #: Ordered page identifiers represented in the retrieval text.
    source_page_ids: list[str] = Field(min_length=1)
    #: Witness artifacts contributing to the accepted source objects.
    witness_ids: list[str] = Field(default_factory=list)
    #: Runner ids contributing to the accepted source objects.
    runner_ids: list[str] = Field(default_factory=list)


class RagChunk(SchemaModel):
    """Page-local retrieval chunk."""

    #: Stable chunk identifier.
    chunk_id: str
    #: Retrieval chunk family.
    chunk_type: ChunkType
    #: Owning document identifier.
    document_id: str
    #: Page identifiers contributing to this chunk.
    page_ids: list[str]
    #: Retrieval text emitted for this chunk.
    text: str
    #: Aggregate trust state for this chunk.
    trust_state: TrustState
    #: Accepted graph object ids feeding this chunk.
    source_object_ids: list[str]
    #: Provenance pointers retained for audit and joins.
    provenance: RetrievalProvenance
    #: Typography hints retained for retrieval consumers.
    typography_summary: list[Typography] = Field(default_factory=list)
    #: Linked note ids or summaries relevant to the chunk.
    note_summary: list[str] = Field(default_factory=list)
    #: Retrieval metadata for filtering and ranking.
    retrieval_metadata: RetrievalMetadata = Field(default_factory=RetrievalMetadata)


class StitchedChunk(SchemaModel):
    """Cross-page retrieval chunk stitched from accepted page-local chunks."""

    #: Stable stitched chunk identifier.
    stitched_chunk_id: str
    #: Owning document identifier.
    document_id: str
    #: Ordered component page-local chunk identifiers.
    component_chunk_ids: list[str]
    #: Ordered page identifiers represented in the stitched text.
    page_ids: list[str]
    #: Stitched retrieval text.
    text: str
    #: Aggregate trust state for the stitched text.
    trust_state: TrustState
    #: Accepted graph object ids feeding this stitched chunk.
    source_object_ids: list[str]
    #: Provenance pointers retained for audit and joins.
    provenance: RetrievalProvenance


class RagDocument(SchemaModel):
    """Document-level retrieval export."""

    #: Persisted retrieval schema version.
    schema_version: str
    #: Reproducible recipe used to produce chunk boundaries and text.
    chunking_recipe_id: str
    #: Owning document identifier.
    document_id: str
    #: Page-local retrieval chunks.
    chunks: list[RagChunk]
    #: Cross-page stitched retrieval chunks.
    stitched_chunks: list[StitchedChunk] = Field(default_factory=list)


class ReviewTask(SchemaModel):
    """Self-contained instructions and evidence binding for human review."""

    #: Stable review-task identifier referenced by every resulting event.
    task_id: str
    #: Operator workflow represented by this task.
    task_type: ReviewTaskType
    #: Independent dimensions this task asks the operator to certify.
    dimensions: list[ReviewDimension] = Field(min_length=1)
    #: Scope shared by the task targets.
    target_scope: ReviewScope
    #: Exact graph objects or page ids the operator must inspect.
    target_object_ids: list[str] = Field(min_length=1)
    #: Concrete question the operator must answer.
    question: str
    #: Evidence views that must be inspected before completion.
    required_evidence: list[str] = Field(min_length=1)
    #: Event actions the review interface may offer for this task.
    allowed_actions: list[ReviewAction] = Field(min_length=1)
    #: Observable checks required before the task can be completed.
    completion_criteria: list[str] = Field(min_length=1)
    #: Review guideline family governing the task.
    guideline_id: str
    #: Exact guideline revision shown to the operator.
    guideline_version: str
    #: Calibration examples shown or available for comparison.
    calibration_example_ids: list[str] = Field(default_factory=list)
    #: Machine run against which the task was prepared.
    base_run_id: str
    #: Accepted graph revision against which the task was prepared.
    base_graph_revision: str
    #: Whether the operator may decline to assert an uncertain answer.
    supports_abstention: bool = True
    #: Current task lifecycle state.
    status: ReviewTaskStatus = ReviewTaskStatus.PENDING
    #: Coverage records certified when the task is completed.
    certified_coverage_ids: list[str] = Field(default_factory=list)


class OverlayState(SchemaModel):
    """Current overlay state for one reviewable object."""

    #: Stable target object identifier.
    object_id: str
    #: Review scope for the target object.
    scope: ReviewScope
    #: Current trust state after applying events.
    trust_state: TrustState
    #: Evidence dimensions explicitly inspected by a human.
    reviewed_dimensions: list[ReviewDimension] = Field(default_factory=list)
    #: Evidence dimensions changed by human correction.
    corrected_dimensions: list[ReviewDimension] = Field(default_factory=list)
    #: Active flag identifiers for the object.
    active_flag_ids: list[str] = Field(default_factory=list)
    #: Review events applied to this object in order.
    applied_event_ids: list[str] = Field(default_factory=list)
    #: Current diplomatic text override when text was corrected.
    text_diplomatic_override: str | None = None
    #: Current typography override when visual evidence was corrected.
    typography_override: Typography | None = None
    #: Current semantic role override kept separate from typography.
    role_overrides: list[TextRole] = Field(default_factory=list)
    #: Current geometry override in a bound coordinate space.
    bounding_box_override: BoundingBox | None = None
    #: Current region class after structural review.
    region_kind_override: RegionKind | None = None
    #: Whether the operator certified the target as illegible.
    illegible: bool = False
    #: Current linked note ids after note-link review.
    linked_note_ids: list[str] = Field(default_factory=list)


class ReviewEventBase(SchemaModel):
    """Fields shared by every append-only review event."""

    #: Stable event identifier.
    event_id: str
    #: Review task that supplied instructions and allowed actions.
    task_id: str
    #: Target object identifier affected by the event.
    target_object_id: str
    #: Scope of the review target.
    target_scope: ReviewScope
    #: Independent dimensions actually inspected during this event.
    review_dimensions: list[ReviewDimension] = Field(min_length=1)
    #: Machine run against which the decision was made.
    base_run_id: str
    #: Accepted graph revision against which the decision was made.
    base_graph_revision: str
    #: Exact human-review guideline revision used for the decision.
    guideline_version: str
    #: Trust state before applying this event.
    prior_trust_state: TrustState
    #: Trust state after applying this event.
    new_trust_state: TrustState
    #: Operator identifier or login.
    operator_id: str
    #: When the operator recorded the event.
    timestamp_utc: datetime
    #: Optional operator note explaining the decision.
    operator_note: str | None = None


class AcceptReviewEvent(ReviewEventBase):
    """Event recording unchanged human acceptance."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.ACCEPT] = ReviewAction.ACCEPT


class CorrectTextReviewEvent(ReviewEventBase):
    """Event recording corrected diplomatic text."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.CORRECT_TEXT] = ReviewAction.CORRECT_TEXT
    #: Replacement diplomatic text asserted by the operator.
    text_diplomatic: str
    #: Short reason for the correction.
    correction_reason: str | None = None


class CorrectStyleReviewEvent(ReviewEventBase):
    """Event recording corrected typography or semantic text role."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.CORRECT_STYLE] = ReviewAction.CORRECT_STYLE
    #: Prior typography facets if they were known to the operator.
    prior_typography: Typography | None = None
    #: Replacement typography facets asserted by the operator.
    new_typography: Typography
    #: Replacement semantic roles asserted independently of typography.
    new_roles: list[TextRole] = Field(default_factory=list)
    #: Short reason for the correction.
    correction_reason: str | None = None


class LinkNoteReviewEvent(ReviewEventBase):
    """Event asserting marker-to-note linkage."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.LINK_NOTE] = ReviewAction.LINK_NOTE
    #: Marker span ids being linked.
    marker_span_ids: list[str]
    #: Accepted note identifier for the linkage.
    note_id: str


class UnlinkNoteReviewEvent(ReviewEventBase):
    """Event removing an incorrect marker-to-note linkage."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.UNLINK_NOTE] = ReviewAction.UNLINK_NOTE
    #: Marker span ids being unlinked.
    marker_span_ids: list[str]
    #: Note identifier being detached.
    note_id: str


class RegionRevision(SchemaModel):
    """Complete replayable structural definition for a corrected region."""

    #: Stable accepted region identifier.
    region_id: str
    #: Accepted semantic region class.
    region_kind: RegionKind
    #: Page reading-order position after correction.
    reading_order_index: int = Field(gt=0)
    #: Accepted rectangle when sufficient.
    bounding_box: BoundingBox | None = None
    #: Accepted polygon when rectangle geometry is lossy.
    polygon: Polygon | None = None
    #: Ordered line identifiers assigned to this region.
    line_ids: list[str] = Field(default_factory=list)


class SplitRegionReviewEvent(ReviewEventBase):
    """Event recording one-to-many structural region correction."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.SPLIT_REGION] = ReviewAction.SPLIT_REGION
    #: Region id being replaced.
    source_region_id: str
    #: Complete replacement region definitions in reading order.
    replacement_regions: list[RegionRevision] = Field(min_length=2)


class MergeRegionReviewEvent(ReviewEventBase):
    """Event recording many-to-one structural region correction."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.MERGE_REGION] = ReviewAction.MERGE_REGION
    #: Region ids being merged.
    source_region_ids: list[str]
    #: Complete accepted replacement region definition.
    replacement_region: RegionRevision


class FlagReviewEvent(ReviewEventBase):
    """Event recording unresolved ambiguity or operator concern."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.FLAG] = ReviewAction.FLAG
    #: Stable flag identifier later consumed by ``resolve_flag``.
    flag_id: str
    #: Stable flag type for downstream triage.
    flag_type: str
    #: Severity selected by the operator.
    severity: FlagSeverity
    #: Human-readable flag message.
    message: str


class ResolveFlagReviewEvent(ReviewEventBase):
    """Event closing one previously raised review flag."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.RESOLVE_FLAG] = ReviewAction.RESOLVE_FLAG
    #: Existing flag identifier being closed.
    flag_id: str
    #: Human-readable resolution or adjudication outcome.
    resolution: str


class CorrectGeometryReviewEvent(ReviewEventBase):
    """Event replacing object geometry without changing its content."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.CORRECT_GEOMETRY] = ReviewAction.CORRECT_GEOMETRY
    #: Replacement bounding box when rectangular geometry is sufficient.
    bounding_box: BoundingBox | None = None
    #: Replacement polygon when a rectangle would lose material shape.
    polygon: Polygon | None = None

    @model_validator(mode="after")
    def validate_geometry(self) -> CorrectGeometryReviewEvent:
        """
        Require at least one concrete replacement geometry.

        Returns:
            The validated geometry event.

        Raises:
            ValueError: If no replacement geometry is supplied.

        """
        if self.bounding_box is None and self.polygon is None:
            msg = "correct_geometry requires a bounding box or polygon"
            raise ValueError(msg)
        return self


class ReorderReviewEvent(ReviewEventBase):
    """Event replacing reading order within one structural parent."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.REORDER] = ReviewAction.REORDER
    #: Complete ordered child-object identifiers after correction.
    ordered_object_ids: list[str] = Field(min_length=2)


class ReclassifyRegionReviewEvent(ReviewEventBase):
    """Event correcting one accepted region class."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.RECLASSIFY_REGION] = ReviewAction.RECLASSIFY_REGION
    #: Prior region class when known.
    prior_region_kind: RegionKind | None = None
    #: Replacement accepted region class.
    new_region_kind: RegionKind


class MarkIllegibleReviewEvent(ReviewEventBase):
    """Event recording that source content cannot be transcribed defensibly."""

    #: Fixed discriminator for JSON schema generation.
    action: Literal[ReviewAction.MARK_ILLEGIBLE] = ReviewAction.MARK_ILLEGIBLE
    #: Explanation of the source defect or unresolved evidence.
    reason: str


#: Discriminated union for every persisted append-only review event.
ReviewEvent = Annotated[
    AcceptReviewEvent
    | CorrectTextReviewEvent
    | CorrectStyleReviewEvent
    | LinkNoteReviewEvent
    | UnlinkNoteReviewEvent
    | SplitRegionReviewEvent
    | MergeRegionReviewEvent
    | FlagReviewEvent
    | ResolveFlagReviewEvent
    | CorrectGeometryReviewEvent
    | ReorderReviewEvent
    | ReclassifyRegionReviewEvent
    | MarkIllegibleReviewEvent,
    Field(discriminator="action"),
]


class PageOverlay(SchemaModel):
    """Exact JSON shape for one page overlay file."""

    #: Persisted overlay schema version.
    schema_version: str
    #: Stable overlay identity for supersession and audit.
    overlay_id: str
    #: Owning page identifier.
    page_id: str
    #: Machine run to which object ids and evidence refer.
    source_run_id: str
    #: Accepted graph revision to which review events apply.
    base_graph_revision: str
    #: Digest binding events to the image the operator inspected.
    prepared_image_checksum: str
    #: Earlier overlay superseded or rebased by this overlay.
    predecessor_overlay_id: str | None = None
    #: Self-contained task packets shown to operators.
    review_tasks: list[ReviewTask] = Field(default_factory=list)
    #: Append-only review events for the page and its children.
    review_events: list[ReviewEvent]
    #: Materialized current state for reviewed objects on the page.
    current_state: list[OverlayState] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_review_bindings(self) -> PageOverlay:  # noqa: PLR0912
        """
        Bind events to valid tasks, evidence revisions, targets, and actions.

        Returns:
            The validated page overlay.

        Raises:
            ValueError: If tasks, events, flags, or materialized state conflict.

        """
        tasks = {task.task_id: task for task in self.review_tasks}
        if len(tasks) != len(self.review_tasks):
            msg = "review task ids must be unique within an overlay"
            raise ValueError(msg)
        event_ids: set[str] = set()
        open_flag_ids: set[str] = set()
        for task in self.review_tasks:
            if (
                task.base_run_id != self.source_run_id
                or task.base_graph_revision != self.base_graph_revision
            ):
                msg = "review tasks must match the overlay run and graph revision"
                raise ValueError(msg)
        for event in self.review_events:
            if event.event_id in event_ids:
                msg = "review event ids must be unique within an overlay"
                raise ValueError(msg)
            event_ids.add(event.event_id)
            event_task = tasks.get(event.task_id)
            if event_task is None:
                msg = f"review event {event.event_id} references an unknown task"
                raise ValueError(msg)
            if event.target_object_id not in event_task.target_object_ids:
                msg = (
                    f"review event {event.event_id} targets an object outside its task"
                )
                raise ValueError(msg)
            if event.action not in event_task.allowed_actions:
                msg = (
                    f"review event {event.event_id} uses an action "
                    "not allowed by its task"
                )
                raise ValueError(msg)
            if not set(event.review_dimensions).issubset(event_task.dimensions):
                msg = f"review event {event.event_id} exceeds its task dimensions"
                raise ValueError(msg)
            if (
                event.base_run_id != self.source_run_id
                or event.base_graph_revision != self.base_graph_revision
            ):
                msg = f"review event {event.event_id} has a stale evidence binding"
                raise ValueError(msg)
            if isinstance(event, FlagReviewEvent):
                if event.flag_id in open_flag_ids:
                    msg = f"flag {event.flag_id} is already active"
                    raise ValueError(msg)
                open_flag_ids.add(event.flag_id)
            if isinstance(event, ResolveFlagReviewEvent):
                if event.flag_id not in open_flag_ids:
                    msg = f"flag {event.flag_id} cannot be resolved before it is raised"
                    raise ValueError(msg)
                open_flag_ids.remove(event.flag_id)
        for state in self.current_state:
            if not set(state.applied_event_ids).issubset(event_ids):
                msg = f"overlay state {state.object_id} references an unknown event"
                raise ValueError(msg)
            if not set(state.active_flag_ids).issubset(open_flag_ids):
                msg = f"overlay state {state.object_id} references an inactive flag"
                raise ValueError(msg)
        return self


class AnchoredGoldAnnotation(SchemaModel):
    """Gold annotation that resolves to graph evidence or prepared image geometry."""

    #: Stable annotation identifier.
    annotation_id: str
    #: Target graph object id when aligned to accepted structure.
    target_object_id: str | None = None
    #: Bounding box when the annotation is image-anchored.
    bounding_box: BoundingBox | None = None
    #: Polygon when an axis-aligned image anchor would be materially lossy.
    polygon: Polygon | None = None
    #: Exclude this annotation from metric denominators.
    do_not_score: bool = False
    #: Reason for exclusion when ``do_not_score`` is true.
    exclusion_reason: str | None = None

    @model_validator(mode="after")
    def validate_anchor_and_exclusion(self) -> AnchoredGoldAnnotation:
        """
        Require a resolvable anchor and explain every scoring exclusion.

        Returns:
            The validated gold annotation.

        Raises:
            ValueError: If the annotation is unanchored or exclusion is unexplained.

        """
        if (
            self.target_object_id is None
            and self.bounding_box is None
            and self.polygon is None
        ):
            msg = "gold annotations require a graph target, box, or polygon"
            raise ValueError(msg)
        if self.do_not_score and self.exclusion_reason is None:
            msg = "do_not_score annotations require an exclusion reason"
            raise ValueError(msg)
        return self


class GoldTextSpan(AnchoredGoldAnnotation):
    """Gold diplomatic and normalized text target."""

    #: Diplomatic gold text.
    text_diplomatic: str
    #: Normalized gold text when defined.
    text_normalized: str | None = None
    #: Whether the image was inspected but could not be transcribed defensibly.
    illegible: bool = False


class GoldStyleSpan(AnchoredGoldAnnotation):
    """Gold style target for one span or image-anchored area."""

    #: Gold independent typography facets.
    typography: Typography
    #: Gold semantic roles independent of visual typography.
    roles: list[TextRole] = Field(default_factory=list)


class GoldRegionAnnotation(AnchoredGoldAnnotation):
    """Gold region or structure target."""

    #: Gold region class.
    region_kind: RegionKind
    #: Gold reading-order position when annotated.
    reading_order_index: int | None = None


class GoldNoteLink(SchemaModel):
    """Gold note-marker linkage target."""

    #: Stable annotation identifier.
    annotation_id: str
    #: Marker span ids expected to link to the note.
    marker_span_ids: list[str]
    #: Note identifier or annotation id for the linked note body.
    note_target_id: str


class GoldLineJoin(SchemaModel):
    """Gold line-join annotation for hyphenation and continuation decisions."""

    #: Stable annotation identifier.
    annotation_id: str
    #: Left line in reading order for the join decision.
    left_line_id: str
    #: Right line in reading order for the join decision.
    right_line_id: str
    #: Whether the annotator judged the lines to be joined.
    joined: bool
    #: Exclude this join from metric denominators.
    do_not_score: bool = False
    #: Reason for exclusion when ``do_not_score`` is true.
    exclusion_reason: str | None = None

    @model_validator(mode="after")
    def validate_exclusion(self) -> GoldLineJoin:
        """
        Require an explanation for every scoring exclusion.

        Returns:
            The validated line-join annotation.

        Raises:
            ValueError: If ``do_not_score`` is true without an exclusion reason.

        """
        if self.do_not_score and self.exclusion_reason is None:
            msg = "do_not_score annotations require an exclusion reason"
            raise ValueError(msg)
        return self


class GoldCoverage(SchemaModel):
    """Explicit evaluation denominator and exclusion scope for a gold slice."""

    #: Stable coverage record identifier.
    coverage_id: str
    #: Evaluation dimensions exhaustively annotated within this scope.
    dimensions: list[ReviewDimension] = Field(min_length=1)
    #: Graph objects included in the coverage scope.
    target_object_ids: list[str] = Field(default_factory=list)
    #: Image area included in the coverage scope.
    bounding_box: BoundingBox | None = None
    #: Whether the coverage scope is the complete prepared page.
    whole_page: bool = False
    #: Whether every instance in the named scope and dimensions was annotated.
    exhaustive: bool
    #: Exclude the entire scope from metric denominators.
    do_not_score: bool = False
    #: Reason the scope is excluded from scoring.
    exclusion_reason: str | None = None

    @model_validator(mode="after")
    def validate_coverage_scope(self) -> GoldCoverage:
        """
        Require an explicit scope and explain every scoring exclusion.

        Returns:
            The validated coverage record.

        Raises:
            ValueError: If scope or exclusion semantics are incomplete.

        """
        if (
            not self.whole_page
            and not self.target_object_ids
            and self.bounding_box is None
        ):
            msg = "gold coverage requires page, graph-object, or image scope"
            raise ValueError(msg)
        if self.do_not_score and self.exclusion_reason is None:
            msg = "excluded gold coverage requires an exclusion reason"
            raise ValueError(msg)
        return self


class GoldPageAnnotation(SchemaModel):
    """Gold data slice for one page."""

    #: Stable page identifier.
    page_id: str
    #: One-based page number in source order.
    page_number: int = Field(gt=0)
    #: Machine run used to create graph-aligned annotations.
    source_run_id: str
    #: Accepted graph revision used to resolve graph targets.
    base_graph_revision: str
    #: Digest binding image anchors to the exact prepared image.
    prepared_image_checksum: str
    #: Whether the gold slice is partial rather than exhaustive.
    is_partial: bool = True
    #: Explicit metric coverage and exclusion scopes.
    coverage: list[GoldCoverage] = Field(min_length=1)
    #: Gold text annotations for the page.
    text_spans: list[GoldTextSpan] = Field(default_factory=list)
    #: Gold style annotations for the page.
    style_spans: list[GoldStyleSpan] = Field(default_factory=list)
    #: Gold note linkage annotations for the page.
    note_links: list[GoldNoteLink] = Field(default_factory=list)
    #: Gold region and structure annotations for the page.
    regions: list[GoldRegionAnnotation] = Field(default_factory=list)
    #: Gold line-join annotations for the page.
    line_joins: list[GoldLineJoin] = Field(default_factory=list)


class GoldDocument(SchemaModel):
    """Document-level gold annotation file."""

    #: Persisted gold annotation schema version.
    schema_version: str
    #: Stable document identifier.
    document_id: str
    #: Guideline or annotation-schema identifier.
    guideline_id: str
    #: Exact annotation-guideline revision used by annotators.
    guideline_version: str
    #: Benchmark partition assigned before model comparison.
    dataset_split: DatasetSplit = DatasetSplit.DEVELOPMENT
    #: When the gold file was created or last rewritten.
    created_at_utc: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    #: Annotator identifiers or team labels.
    annotators: list[str] = Field(default_factory=list)
    #: Adjudicator identity when conflicting annotations were resolved.
    adjudicator_id: str | None = None
    #: Page-local gold annotation slices.
    pages: list[GoldPageAnnotation]


#: Public OCR contract model exports.
__all__ = [
    "AcceptReviewEvent",
    "AcquisitionProvenance",
    "AnchoredGoldAnnotation",
    "BaselineShift",
    "BatchItemRef",
    "BatchResultStatus",
    "BatchUnitKind",
    "BibliographicProvenance",
    "BoundingBox",
    "BundlePage",
    "ChunkType",
    "CoordinateSpace",
    "CoordinateTransform",
    "CorrectGeometryReviewEvent",
    "CorrectStyleReviewEvent",
    "CorrectTextReviewEvent",
    "DatasetSplit",
    "DocumentBundle",
    "DocumentEvaluationSummary",
    "EvaluationFamilySummary",
    "EvaluationFlag",
    "ExportSummary",
    "FlagReviewEvent",
    "FlagSeverity",
    "FontFamilyCandidate",
    "FontSlant",
    "FontWeight",
    "GoldCoverage",
    "GoldDocument",
    "GoldNoteLink",
    "GoldPageAnnotation",
    "GoldRegionAnnotation",
    "GoldStyleSpan",
    "GoldTextSpan",
    "InputKind",
    "LineRecord",
    "LinkNoteReviewEvent",
    "MarkIllegibleReviewEvent",
    "MergeRegionReviewEvent",
    "MetricScore",
    "NoteKind",
    "NoteRecord",
    "ObjectProvenance",
    "OverlayState",
    "PackagingStrategy",
    "PageClass",
    "PageEvaluationSummary",
    "PageOverlay",
    "Point",
    "Polygon",
    "PreparationMode",
    "PreparedArtifactRef",
    "PreparedPage",
    "RagChunk",
    "RagDocument",
    "ReclassifyRegionReviewEvent",
    "RegionKind",
    "RegionRecord",
    "RegionRevision",
    "ReorderReviewEvent",
    "ResolveFlagReviewEvent",
    "RetrievalMetadata",
    "RetrievalProvenance",
    "ReviewAction",
    "ReviewDimension",
    "ReviewEvent",
    "ReviewScope",
    "ReviewSummary",
    "ReviewTask",
    "ReviewTaskStatus",
    "ReviewTaskType",
    "RunMetadata",
    "RunnerCapability",
    "RunnerExecutionBatch",
    "RunnerOutputArtifact",
    "RunnerReference",
    "SourceDescriptor",
    "SourceType",
    "SpanRecord",
    "SplitRegionReviewEvent",
    "StitchedChunk",
    "StyleEvaluationSummary",
    "TextRole",
    "TransformKind",
    "TrustState",
    "Typography",
    "UnlinkNoteReviewEvent",
    "WitnessReference",
]
