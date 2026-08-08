# Copyright (C) 2026 Chris Malek.
"""Adapt persisted raw runner witnesses into merge-ready PassWitnessPage graphs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from wordwending.models import (
    BoundingBox,
    CoordinateSpace,
    LineRecord,
    ObjectProvenance,
    PassWitnessPage,
    Point,
    Polygon,
    PreparedPage,
    RegionKind,
    RegionRecord,
    SpanRecord,
    TextRole,
    Typography,
)

#: Schema id for structured kraken segmentation inside chat.completion content.
KRAKEN_SEGMENTATION_SCHEMA = "wordwending.kraken_segmentation/v1"


class StructuredKrakenRegion(BaseModel):
    """One region from a ``wordwending.kraken_segmentation/v1`` payload."""

    #: Region identifier in the kraken payload (mapped to stable graph ids later).
    id: str
    #: Axis-aligned box as ``[x0, y0, x1, y1]``.
    bbox: tuple[float, float, float, float]


class StructuredKrakenLine(BaseModel):
    """One line from a ``wordwending.kraken_segmentation/v1`` payload."""

    #: Line identifier in the kraken payload (mapped to stable graph ids later).
    id: str
    #: Diplomatic text for the line.
    text: str
    #: Axis-aligned box as ``[x0, y0, x1, y1]`` when present.
    bbox: tuple[float, float, float, float] | None = None
    #: Baseline polyline as ``[[x, y], ...]`` when present.
    baseline: list[tuple[float, float]] | None = None
    #: Optional boundary polygon vertices as ``[[x, y], ...]``.
    boundary: list[tuple[float, float]] | None = None
    #: Kraken region ids this line belongs to.
    region_ids: list[str] = Field(default_factory=list)


class StructuredKrakenPage(BaseModel):
    """Parsed ``wordwending.kraken_segmentation/v1`` content object."""

    #: Pydantic config allowing ``schema`` alias population.
    model_config = ConfigDict(populate_by_name=True)

    #: Locked schema identifier for structured kraken segmentation.
    schema_id: Literal["wordwending.kraken_segmentation/v1"] = Field(
        alias="schema",
    )
    #: Segmentation type (``baselines`` or ``bbox``).
    type: str
    #: Optional text direction hint from the runner.
    text_direction: str | None = None
    #: Regions when the payload supplies them; empty triggers synthesis.
    regions: list[StructuredKrakenRegion] = Field(default_factory=list)
    #: Ordered diplomatic lines with geometry.
    lines: list[StructuredKrakenLine]


def _extract_openai_chat_completion_content(
    raw_bytes: bytes,
    *,
    engine_label: str,
) -> str:
    """
    Extract assistant ``content`` string from chat.completion bytes.

    Shared by olmOCR and kraken adapters: both persist OpenAI-compatible
    ``chat.completion`` JSON (ADR 0004). Strategies remain keyed by
    ``runner_id`` even though the wire shape is the same family.

    Args:
        raw_bytes: Exact JSON bytes persisted for one runner witness.

    Keyword Args:
        engine_label: Human-readable engine name for error messages.

    Returns:
        Assistant message content string.

    Raises:
        ValueError: If the payload is not a chat.completion with assistant
            content.
        TypeError: If required JSON fields have the wrong types.

    """
    try:
        payload: Any = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        msg = f"{engine_label} witness must be UTF-8 JSON chat.completion bytes"
        raise ValueError(msg) from exc
    if not isinstance(payload, dict):
        msg = (
            f"{engine_label} witness must be a JSON object with object=chat.completion"
        )
        raise TypeError(msg)
    if payload.get("object") != "chat.completion":
        msg = f"{engine_label} witness must have object=chat.completion"
        raise ValueError(msg)
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "chat.completion witness requires a non-empty choices list"
        raise ValueError(msg)
    first = choices[0]
    if not isinstance(first, dict):
        msg = "chat.completion choices[0] must be an object"
        raise TypeError(msg)
    message = first.get("message")
    if not isinstance(message, dict):
        msg = "chat.completion choices[0].message must be an object"
        raise TypeError(msg)
    content = message.get("content")
    if not isinstance(content, str):
        msg = "chat.completion assistant content must be a string"
        raise TypeError(msg)
    return content


def _split_diplomatic_lines(content: str) -> list[str]:
    """
    Split assistant content into diplomatic text lines.

    Args:
        content: Assistant message content string.

    Returns:
        Newline-split lines with a single trailing empty line removed.

    """
    lines = content.splitlines()
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _extract_openai_chat_completion_lines(
    raw_bytes: bytes,
    *,
    engine_label: str,
) -> list[str]:
    """
    Extract newline-split assistant content from chat.completion bytes.

    Args:
        raw_bytes: Exact JSON bytes persisted for one runner witness.

    Keyword Args:
        engine_label: Human-readable engine name for error messages.

    Returns:
        Diplomatic text lines split on newlines.

    Raises:
        ValueError: If the payload is not a chat.completion with assistant
            content.
        TypeError: If required JSON fields have the wrong types.

    """
    content = _extract_openai_chat_completion_content(
        raw_bytes,
        engine_label=engine_label,
    )
    return _split_diplomatic_lines(content)


#: Minimum polygon vertex count required by ``Polygon``.
_MIN_POLYGON_POINTS = 3


def _bbox_from_xyxy(
    values: tuple[float, float, float, float],
    *,
    space_id: str,
) -> BoundingBox:
    """
    Build a BoundingBox from ``[x0, y0, x1, y1]`` in the prepared-page space.

    Args:
        values: Axis-aligned box corners.

    Keyword Args:
        space_id: Prepared-page coordinate space id.

    Returns:
        BoundingBox with the given space id.

    """
    x0, y0, x1, y1 = values
    return BoundingBox(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        coordinate_space_id=space_id,
    )


def _points_from_pairs(pairs: list[tuple[float, float]]) -> list[Point]:
    """
    Convert ``[[x, y], ...]`` pairs into Point models.

    Args:
        pairs: Coordinate pairs from the structured payload.

    Returns:
        Point list in the same order.

    """
    return [Point(x=x, y=y) for x, y in pairs]


def _polygon_from_boundary(
    boundary: list[tuple[float, float]],
    *,
    space_id: str,
) -> Polygon | None:
    """
    Build a closed Polygon from a boundary ring when it has enough vertices.

    Args:
        boundary: Boundary vertices from the structured payload.

    Keyword Args:
        space_id: Prepared-page coordinate space id.

    Returns:
        Polygon with a closed ring, or ``None`` when fewer than three points.

    """
    if len(boundary) < _MIN_POLYGON_POINTS:
        return None
    points = _points_from_pairs(boundary)
    first = points[0]
    last = points[-1]
    if first.x != last.x or first.y != last.y:
        points.append(Point(x=first.x, y=first.y))
    if len(points) < _MIN_POLYGON_POINTS:
        return None
    return Polygon(coordinate_space_id=space_id, points=points)


def _union_boxes(boxes: list[BoundingBox], *, space_id: str) -> BoundingBox | None:
    """
    Compute the axis-aligned union of boxes in one coordinate space.

    Args:
        boxes: Non-empty candidate boxes to union.

    Keyword Args:
        space_id: Prepared-page coordinate space id for the result.

    Returns:
        Union box, or ``None`` when ``boxes`` is empty.

    """
    if not boxes:
        return None
    return BoundingBox(
        x0=min(box.x0 for box in boxes),
        y0=min(box.y0 for box in boxes),
        x1=max(box.x1 for box in boxes),
        y1=max(box.y1 for box in boxes),
        coordinate_space_id=space_id,
    )


def _line_has_required_geometry(
    line: StructuredKrakenLine,
    *,
    segmentation_type: str,
) -> bool:
    """
    Return whether a structured line meets accept rules for its type.

    Args:
        line: Structured kraken line candidate.

    Keyword Args:
        segmentation_type: Payload ``type`` (``bbox`` requires boxes).

    Returns:
        ``True`` when the line has acceptable geometry.

    """
    has_bbox = line.bbox is not None
    has_baseline = bool(line.baseline)
    if segmentation_type == "bbox":
        return has_bbox
    return has_bbox or has_baseline


class OlmocrChatCompletionAdapter:
    """
    Parse exact olmOCR chat.completion JSON bytes into diplomatic text lines.

    This adapter reads the persisted OpenAI-compatible payload written by
    ``HuggingFaceOlmocrRunner`` (ADR 0004). It does not invent a parallel
    raw-witness schema.
    """

    def extract_lines(self, raw_bytes: bytes) -> list[str]:
        """
        Extract newline-split assistant content from chat.completion bytes.

        Args:
            raw_bytes: Exact JSON bytes persisted for one olmOCR witness.

        Returns:
            Diplomatic text lines split on newlines.

        Raises:
            ValueError: If the payload is not a chat.completion with assistant
                content.
            TypeError: If required JSON fields have the wrong types.

        """
        return _extract_openai_chat_completion_lines(
            raw_bytes,
            engine_label="olmOCR",
        )


class KrakenChatCompletionAdapter:
    """
    Parse exact kraken chat.completion JSON bytes in dual mode.

    Reads the persisted OpenAI-compatible payload written by
    ``HuggingFaceKrakenRunner`` (ADR 0004 / C1). When ``message.content`` is a
    JSON object with ``schema == wordwending.kraken_segmentation/v1``, returns
    structured segmentation for coordinate-rich adaptation. Otherwise treats
    content as plain diplomatic text (provisional fallback without line/span
    boxes).
    """

    def extract_lines(self, raw_bytes: bytes) -> list[str]:
        """
        Extract diplomatic text lines, structured or plain-text fallback.

        Args:
            raw_bytes: Exact JSON bytes persisted for one kraken witness.

        Returns:
            Diplomatic text lines (structured line texts or newline split).

        Raises:
            ValueError: If the payload is not a chat.completion with assistant
                content, or structured v1 content fails validation.
            TypeError: If required JSON fields have the wrong types.

        """
        result = self.extract_segmentation(raw_bytes)
        if isinstance(result, list):
            return result
        return [line.text for line in result.lines]

    def extract_segmentation(
        self,
        raw_bytes: bytes,
    ) -> StructuredKrakenPage | list[str]:
        """
        Parse kraken chat.completion content as structured v1 or plain text.

        Args:
            raw_bytes: Exact JSON bytes persisted for one kraken witness.

        Returns:
            ``StructuredKrakenPage`` when content is v1 segmentation JSON;
            otherwise newline-split plain-text lines.

        Raises:
            ValueError: If the payload is not a chat.completion with assistant
                content, or structured v1 content fails accept rules.
            TypeError: If required JSON fields have the wrong types.

        """
        content = _extract_openai_chat_completion_content(
            raw_bytes,
            engine_label="kraken",
        )
        try:
            parsed: Any = json.loads(content)
        except json.JSONDecodeError:
            return _split_diplomatic_lines(content)
        if not isinstance(parsed, dict):
            return _split_diplomatic_lines(content)
        if parsed.get("schema") != KRAKEN_SEGMENTATION_SCHEMA:
            return _split_diplomatic_lines(content)
        try:
            page = StructuredKrakenPage.model_validate(parsed)
        except ValidationError as exc:
            msg = "kraken structured segmentation v1 failed validation"
            raise ValueError(msg) from exc
        self._validate_structured_geometry(page)
        return page

    def _validate_structured_geometry(self, page: StructuredKrakenPage) -> None:
        """
        Reject structured lines that lack required bbox/baseline geometry.

        Args:
            page: Parsed structured kraken segmentation.

        Raises:
            ValueError: If any line lacks accept-rule geometry.

        """
        for line in page.lines:
            if not _line_has_required_geometry(
                line,
                segmentation_type=page.type,
            ):
                msg = (
                    "kraken structured line requires bbox or baseline "
                    f"(boundary-only is not enough); line id={line.id!r}"
                )
                raise ValueError(msg)


class WitnessAdaptationService:
    """
    Convert persisted raw witness artifacts into merge-ready page fragments.

    Strategies are keyed by ``runner_id`` (``olmocr``, ``kraken``). olmOCR and
    plain-text kraken build provisional graphs: one BODY region (page box
    allowed) with line/span ``bounding_box=None``. Structured kraken v1 builds
    real per-line geometry in the prepared-page coordinate space. Paths are
    used as given (absolute or cwd-relative); callers resolve bundle-relative
    paths before adapt.
    """

    def __init__(self) -> None:
        """Initialize with runner_id-keyed chat.completion parsing strategies."""
        #: Parser for persisted olmOCR OpenAI-compatible chat.completion JSON.
        self._olmocr = OlmocrChatCompletionAdapter()
        #: Parser for persisted kraken OpenAI-compatible chat.completion JSON.
        self._kraken = KrakenChatCompletionAdapter()
        #: Strategy lookup keyed by logical ``runner_id``.
        self._strategies: dict[
            str,
            OlmocrChatCompletionAdapter | KrakenChatCompletionAdapter,
        ] = {
            "olmocr": self._olmocr,
            "kraken": self._kraken,
        }

    def adapt_page(
        self,
        *,
        prepared_page: PreparedPage,
        witness_id: str,
        runner_id: str,
        artifact_paths: list[str],
        coordinate_space: CoordinateSpace,
    ) -> PassWitnessPage:
        """
        Build a PassWitnessPage from raw witness artifact paths.

        Keyword Args:
            prepared_page: Prepared page this witness aligns to.
            witness_id: Witness artifact identifier for provenance.
            runner_id: Runner identifier selecting the adaptation strategy.
            artifact_paths: Existing absolute or cwd-relative path strings;
                resolve vs bundle_root at the call site before adapt.
            coordinate_space: Coordinate space for page geometry.

        Returns:
            Merge-ready page fragment. Structured kraken yields real line
            geometry; olmOCR and plain-text kraken yield provisional text
            without line/span boxes.

        Raises:
            ValueError: If ``artifact_paths`` is empty, ``runner_id`` is
                unsupported, or the artifact is not a chat.completion payload.
            FileNotFoundError: If a path cannot be read.

        """
        if not artifact_paths:
            msg = "artifact_paths must contain at least one witness path"
            raise ValueError(msg)
        strategy = self._strategies.get(runner_id)
        if strategy is None:
            supported = ", ".join(sorted(self._strategies))
            msg = f"unsupported runner_id {runner_id!r}; supported: {supported}"
            raise ValueError(msg)
        raw_bytes = Path(artifact_paths[0]).read_bytes()
        try:
            if runner_id == "kraken":
                segmentation = self._kraken.extract_segmentation(raw_bytes)
                if isinstance(segmentation, StructuredKrakenPage):
                    return self._build_structured_kraken_page(
                        prepared_page=prepared_page,
                        witness_id=witness_id,
                        runner_id=runner_id,
                        coordinate_space=coordinate_space,
                        structured=segmentation,
                    )
                lines = segmentation
            else:
                lines = strategy.extract_lines(raw_bytes)
        except TypeError as exc:
            raise ValueError(str(exc)) from exc
        return self._build_provisional_page(
            prepared_page=prepared_page,
            witness_id=witness_id,
            runner_id=runner_id,
            coordinate_space=coordinate_space,
            lines=lines,
        )

    def _build_provisional_page(
        self,
        *,
        prepared_page: PreparedPage,
        witness_id: str,
        runner_id: str,
        coordinate_space: CoordinateSpace,
        lines: list[str],
    ) -> PassWitnessPage:
        """
        Build conservative full-page region + one line/span per text line.

        Line and span boxes are intentionally ``None`` so provisional text is
        not counted as coordinate-rich. The single BODY region may retain a
        page-wide box.

        Keyword Args:
            prepared_page: Prepared page supplying stable id prefixes.
            witness_id: Witness artifact identifier for provenance.
            runner_id: Runner identifier for provenance.
            coordinate_space: Page coordinate space for the region box.
            lines: Diplomatic text lines from the raw witness.

        Returns:
            PassWitnessPage with provisional text-only line/span geometry.

        """
        prepared_page_id = prepared_page.prepared_page_id
        provenance = ObjectProvenance(
            source_page_id=prepared_page_id,
            witness_ids=[witness_id],
            runner_ids=[runner_id],
        )
        page_box = BoundingBox(
            x0=0,
            y0=0,
            x1=float(coordinate_space.width_px),
            y1=float(coordinate_space.height_px),
            coordinate_space_id=coordinate_space.space_id,
        )
        region_id = f"{prepared_page_id}:r0"
        line_records: list[LineRecord] = []
        span_records: list[SpanRecord] = []
        line_ids: list[str] = []
        for line_index, text in enumerate(lines):
            line_id = f"{prepared_page_id}:l{line_index}"
            span_id = f"{prepared_page_id}:s{line_index}"
            line_ids.append(line_id)
            line_records.append(
                LineRecord(
                    line_id=line_id,
                    region_id=region_id,
                    line_order=line_index + 1,
                    bounding_box=None,
                    span_ids=[span_id],
                    provenance=provenance,
                )
            )
            span_records.append(
                SpanRecord(
                    span_id=span_id,
                    line_id=line_id,
                    text_diplomatic=text,
                    text_normalized=text,
                    typography=Typography(),
                    roles=[TextRole.TEXT],
                    bounding_box=None,
                    provenance=provenance,
                )
            )
        region = RegionRecord(
            region_id=region_id,
            region_kind=RegionKind.BODY,
            reading_order_index=1,
            bounding_box=page_box,
            line_ids=line_ids,
            provenance=provenance,
        )
        return PassWitnessPage(
            witness_id=witness_id,
            runner_id=runner_id,
            prepared_page_id=prepared_page_id,
            coordinate_space=coordinate_space,
            regions=[region],
            lines=line_records,
            spans=span_records,
        )

    def _build_structured_kraken_page(
        self,
        *,
        prepared_page: PreparedPage,
        witness_id: str,
        runner_id: str,
        coordinate_space: CoordinateSpace,
        structured: StructuredKrakenPage,
    ) -> PassWitnessPage:
        """
        Map structured kraken v1 segmentation into a coordinate-rich page graph.

        Keyword Args:
            prepared_page: Prepared page supplying stable id prefixes.
            witness_id: Witness artifact identifier for provenance.
            runner_id: Runner identifier for provenance.
            coordinate_space: Prepared-page coordinate space for all geometry.
            structured: Validated kraken segmentation v1 payload.

        Returns:
            PassWitnessPage with real region/line/span geometry.

        """
        prepared_page_id = prepared_page.prepared_page_id
        space_id = prepared_page.coordinate_space.space_id
        provenance = ObjectProvenance(
            source_page_id=prepared_page_id,
            witness_ids=[witness_id],
            runner_ids=[runner_id],
        )

        kraken_to_stable_region: dict[str, str] = {}
        region_boxes: dict[str, BoundingBox | None] = {}
        if structured.regions:
            for region_index, region in enumerate(structured.regions):
                stable_id = f"{prepared_page_id}:r{region_index}"
                kraken_to_stable_region[region.id] = stable_id
                region_boxes[stable_id] = _bbox_from_xyxy(
                    region.bbox,
                    space_id=space_id,
                )
        else:
            default_region_id = f"{prepared_page_id}:r0"
            kraken_to_stable_region[""] = default_region_id
            line_boxes = [
                _bbox_from_xyxy(line.bbox, space_id=space_id)
                for line in structured.lines
                if line.bbox is not None
            ]
            region_boxes[default_region_id] = _union_boxes(
                line_boxes,
                space_id=space_id,
            )

        default_region_id = next(iter(region_boxes))
        region_line_ids: dict[str, list[str]] = {
            region_id: [] for region_id in region_boxes
        }
        line_records: list[LineRecord] = []
        span_records: list[SpanRecord] = []

        for line_index, line in enumerate(structured.lines):
            line_id = f"{prepared_page_id}:l{line_index}"
            span_id = f"{prepared_page_id}:s{line_index}"
            region_id = default_region_id
            for kraken_region_id in line.region_ids:
                mapped = kraken_to_stable_region.get(kraken_region_id)
                if mapped is not None:
                    region_id = mapped
                    break
            region_line_ids.setdefault(region_id, []).append(line_id)

            line_box = (
                _bbox_from_xyxy(line.bbox, space_id=space_id)
                if line.bbox is not None
                else None
            )
            baseline_points = (
                _points_from_pairs(list(line.baseline)) if line.baseline else []
            )
            baseline_space_id = space_id if baseline_points else None
            polygon = (
                _polygon_from_boundary(list(line.boundary), space_id=space_id)
                if line.boundary
                else None
            )
            line_records.append(
                LineRecord(
                    line_id=line_id,
                    region_id=region_id,
                    line_order=line_index + 1,
                    bounding_box=line_box,
                    polygon=polygon,
                    baseline=baseline_points,
                    baseline_coordinate_space_id=baseline_space_id,
                    span_ids=[span_id],
                    provenance=provenance,
                )
            )
            span_records.append(
                SpanRecord(
                    span_id=span_id,
                    line_id=line_id,
                    text_diplomatic=line.text,
                    text_normalized=line.text,
                    typography=Typography(),
                    roles=[TextRole.TEXT],
                    bounding_box=line_box,
                    provenance=provenance,
                )
            )

        regions: list[RegionRecord] = []
        for reading_order, (region_id, box) in enumerate(region_boxes.items(), start=1):
            regions.append(
                RegionRecord(
                    region_id=region_id,
                    region_kind=RegionKind.BODY,
                    reading_order_index=reading_order,
                    bounding_box=box,
                    line_ids=region_line_ids.get(region_id, []),
                    provenance=provenance,
                )
            )

        return PassWitnessPage(
            witness_id=witness_id,
            runner_id=runner_id,
            prepared_page_id=prepared_page_id,
            coordinate_space=coordinate_space,
            regions=regions,
            lines=line_records,
            spans=span_records,
        )
