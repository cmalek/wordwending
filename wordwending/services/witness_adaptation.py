# Copyright (C) 2026 Chris Malek.
"""Adapt persisted raw runner witnesses into merge-ready PassWitnessPage graphs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wordwending.models import (
    BoundingBox,
    CoordinateSpace,
    LineRecord,
    ObjectProvenance,
    PassWitnessPage,
    PreparedPage,
    RegionKind,
    RegionRecord,
    SpanRecord,
    TextRole,
    Typography,
)


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
        try:
            payload: Any = json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            msg = "olmOCR witness must be UTF-8 JSON chat.completion bytes"
            raise ValueError(msg) from exc
        if not isinstance(payload, dict):
            msg = "olmOCR witness must be a JSON object with object=chat.completion"
            raise TypeError(msg)
        if payload.get("object") != "chat.completion":
            msg = "olmOCR witness must have object=chat.completion"
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
        return content.split("\n")


class WitnessAdaptationService:
    """
    Convert persisted raw witness artifacts into merge-ready page fragments.

    Wave A geometry is provisional text-only: one full-page BODY region and
    one line/span per newline. Paths are used as given (absolute or
    cwd-relative); callers resolve bundle-relative paths before adapt.
    """

    def __init__(self) -> None:
        """Initialize with the olmOCR chat.completion parsing strategy."""
        #: Parser for persisted olmOCR OpenAI-compatible chat.completion JSON.
        self._olmocr = OlmocrChatCompletionAdapter()

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
        Build a provisional PassWitnessPage from raw witness artifact paths.

        Keyword Args:
            prepared_page: Prepared page this witness aligns to.
            witness_id: Witness artifact identifier for provenance.
            runner_id: Runner identifier for provenance (caller-supplied).
            artifact_paths: Existing absolute or cwd-relative path strings;
                resolve vs bundle_root at the call site before adapt.
            coordinate_space: Coordinate space for provisional geometry.

        Returns:
            Merge-ready page fragment with provisional text-only geometry.

        Raises:
            ValueError: If ``artifact_paths`` is empty or the artifact is not
                a chat.completion payload.
            FileNotFoundError: If a path cannot be read.

        """
        if not artifact_paths:
            msg = "artifact_paths must contain at least one witness path"
            raise ValueError(msg)
        raw_bytes = Path(artifact_paths[0]).read_bytes()
        lines = self._olmocr.extract_lines(raw_bytes)
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

        Keyword Args:
            prepared_page: Prepared page supplying stable id prefixes.
            witness_id: Witness artifact identifier for provenance.
            runner_id: Runner identifier for provenance.
            coordinate_space: Page coordinate space for provisional boxes.
            lines: Diplomatic text lines from the raw witness.

        Returns:
            PassWitnessPage with provisional text-only geometry.

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
                    bounding_box=page_box,
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
                    bounding_box=page_box,
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
