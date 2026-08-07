# Copyright (C) 2026 Chris Malek.
"""Tests for olmOCR chat.completion witness adaptation into PassWitnessPage."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from wordwending.models import (
    CoordinateSpace,
    PageClass,
    PreparationMode,
    PreparedPage,
    RegionKind,
)
from wordwending.services.witness_adaptation import WitnessAdaptationService

_FIXTURE = (
    Path(__file__).parent / "fixtures" / "assemble" / "olmocr-chat-completion-v1.json"
)


def _prepared_page(*, prepared_page_id: str = "prepared-page-1") -> PreparedPage:
    """Return a minimal prepared page for adaptation tests."""
    return PreparedPage(
        prepared_page_id=prepared_page_id,
        preparation_mode=PreparationMode.FULL_PAGE,
        page_class=PageClass.ORDINARY_PROSE,
        image_path="page.png",
        source_artifact_id="source-1",
        image_checksum="sha256:image",
        preparation_recipe_id="prep-v1",
        preparation_recipe_digest="digest-prep-v1",
        coordinate_space=CoordinateSpace(
            space_id=prepared_page_id,
            width_px=200,
            height_px=300,
        ),
    )


def _coordinate_space(*, prepared_page_id: str = "prepared-page-1") -> CoordinateSpace:
    """Return coordinate space matching the test prepared page."""
    return CoordinateSpace(space_id=prepared_page_id, width_px=200, height_px=300)


def test_adapt_page_builds_provisional_two_line_graph(tmp_path: Path) -> None:
    """Fixture chat.completion yields one BODY region and two line/span pairs."""
    witness_path = tmp_path / "witness.json"
    shutil.copy(_FIXTURE, witness_path)
    prepared = _prepared_page()
    service = WitnessAdaptationService()

    page = service.adapt_page(
        prepared_page=prepared,
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=[str(witness_path)],
        coordinate_space=_coordinate_space(),
    )

    assert page.witness_id == "wit-1"
    assert page.runner_id == "olmocr"
    assert page.prepared_page_id == "prepared-page-1"
    assert len(page.regions) == 1
    assert len(page.lines) == 2
    assert len(page.spans) == 2

    region = page.regions[0]
    assert region.region_id == "prepared-page-1:r0"
    assert region.region_kind is RegionKind.BODY
    assert region.line_ids == ["prepared-page-1:l0", "prepared-page-1:l1"]
    assert region.bounding_box is not None
    assert region.bounding_box.x0 == 0
    assert region.bounding_box.y0 == 0
    assert region.bounding_box.x1 == 200
    assert region.bounding_box.y1 == 300
    assert region.bounding_box.coordinate_space_id == "prepared-page-1"

    assert page.lines[0].line_id == "prepared-page-1:l0"
    assert page.lines[1].line_id == "prepared-page-1:l1"
    assert page.spans[0].span_id == "prepared-page-1:s0"
    assert page.spans[1].span_id == "prepared-page-1:s1"
    assert page.spans[0].text_diplomatic == "Line one of diplomatic text."
    assert page.spans[1].text_diplomatic == "Line two of diplomatic text."
    assert page.spans[0].line_id == "prepared-page-1:l0"
    assert page.spans[1].line_id == "prepared-page-1:l1"
    assert page.lines[0].span_ids == ["prepared-page-1:s0"]
    assert page.lines[1].span_ids == ["prepared-page-1:s1"]
    assert page.lines[0].region_id == region.region_id
    assert page.lines[1].region_id == region.region_id


def test_adapt_page_stable_ids_across_rebuilds(tmp_path: Path) -> None:
    """Same inputs produce identical region/line/span ids on rebuild."""
    witness_path = tmp_path / "witness.json"
    shutil.copy(_FIXTURE, witness_path)
    prepared = _prepared_page()
    service = WitnessAdaptationService()
    space = _coordinate_space()

    first = service.adapt_page(
        prepared_page=prepared,
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=[str(witness_path)],
        coordinate_space=space,
    )
    second = service.adapt_page(
        prepared_page=prepared,
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=[str(witness_path)],
        coordinate_space=space,
    )

    assert [r.region_id for r in first.regions] == [
        r.region_id for r in second.regions
    ]
    assert [line.line_id for line in first.lines] == [
        line.line_id for line in second.lines
    ]
    assert [span.span_id for span in first.spans] == [
        span.span_id for span in second.spans
    ]


def test_adapt_page_rejects_empty_artifact_paths(tmp_path: Path) -> None:
    """Empty artifact_paths list is rejected before reading."""
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match="artifact_paths"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-1",
            runner_id="olmocr",
            artifact_paths=[],
            coordinate_space=_coordinate_space(),
        )


def test_adapt_page_rejects_non_chat_completion_json(tmp_path: Path) -> None:
    """Non-chat.completion JSON is rejected as an invalid raw witness."""
    witness_path = tmp_path / "bad.json"
    witness_path.write_text(
        json.dumps({"object": "not.chat.completion", "choices": []}),
        encoding="utf-8",
    )
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match=r"chat\.completion"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-1",
            runner_id="olmocr",
            artifact_paths=[str(witness_path)],
            coordinate_space=_coordinate_space(),
        )
