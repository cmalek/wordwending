# Copyright (C) 2026 Chris Malek.
"""Tests for runner_id-keyed chat.completion witness adaptation."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from wordwending.models import (
    CoordinateSpace,
    PageClass,
    Point,
    PreparationMode,
    PreparedPage,
    RegionKind,
)
from wordwending.services.merge import _coordinate_rich_line_count
from wordwending.services.witness_adaptation import WitnessAdaptationService

_FIXTURES = Path(__file__).parent / "fixtures" / "assemble"
_FIXTURE = _FIXTURES / "olmocr-chat-completion-v1.json"
_KRAKEN_FIXTURE = _FIXTURES / "kraken-chat-completion-v1.json"
_KRAKEN_SEGMENTATION_FIXTURE = _FIXTURES / "kraken-segmentation-v1.json"
_MANIFEST_FIXTURE = _FIXTURES / "manifest-v1.json"


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
    """
    Two independent adapt_page calls yield identical ids and diplomatic texts.

    ADR 0008 / A2 formula: ``{prepared_page_id}:r0``, ``:l{i}``, ``:s{i}``.
    """
    witness_path = tmp_path / "witness.json"
    shutil.copy(_FIXTURE, witness_path)
    prepared = _prepared_page()
    space = _coordinate_space()
    artifact_paths = [str(witness_path)]

    first = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=artifact_paths,
        coordinate_space=space,
    )
    second = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=artifact_paths,
        coordinate_space=space,
    )

    assert [r.region_id for r in first.regions] == [r.region_id for r in second.regions]
    assert [line.line_id for line in first.lines] == [
        line.line_id for line in second.lines
    ]
    assert [span.span_id for span in first.spans] == [
        span.span_id for span in second.spans
    ]
    assert [span.text_diplomatic for span in first.spans] == [
        span.text_diplomatic for span in second.spans
    ]


def test_adapt_page_span_ids_pair_with_assemble_gold(tmp_path: Path) -> None:
    """Adapted span ids and texts match assemble gold-v1 target_object_ids."""
    manifest = json.loads(_MANIFEST_FIXTURE.read_text(encoding="utf-8"))
    manifest_page = manifest["pages"][0]
    prepared = PreparedPage.model_validate(manifest_page["prepared_page"])
    witness = manifest_page["raw_witnesses"][0]
    coordinate_space = CoordinateSpace.model_validate(witness["coordinate_space"])

    gold_path = _FIXTURES / "gold-v1.json"
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    gold_page = gold["pages"][0]
    assert gold_page["page_id"] == manifest_page["page_id"]
    assert gold_page["prepared_image_checksum"] == prepared.image_checksum
    gold_span_ids = [
        annotation["target_object_id"] for annotation in gold_page["text_spans"]
    ]
    gold_texts = [
        annotation["text_diplomatic"] for annotation in gold_page["text_spans"]
    ]
    coverage_ids = gold_page["coverage"][0]["target_object_ids"]

    witness_path = tmp_path / "witness.json"
    shutil.copy(_FIXTURE, witness_path)
    page = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id=witness["witness_id"],
        runner_id=witness["runner_id"],
        artifact_paths=[str(witness_path)],
        coordinate_space=coordinate_space,
    )

    assert page.prepared_page_id == prepared.prepared_page_id
    adapted_ids = [span.span_id for span in page.spans]
    adapted_texts = [span.text_diplomatic for span in page.spans]
    assert adapted_ids == gold_span_ids == coverage_ids
    assert adapted_texts == gold_texts


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


def _write_chat_completion(
    tmp_path: Path,
    *,
    content: str | int,
    filename: str = "witness.json",
) -> Path:
    """Write a minimal chat.completion witness artifact for adaptation tests."""
    witness_path = tmp_path / filename
    witness_path.write_text(
        json.dumps(
            {
                "object": "chat.completion",
                "choices": [{"message": {"role": "assistant", "content": content}}],
            }
        ),
        encoding="utf-8",
    )
    return witness_path


def test_adapt_page_raises_value_error_for_wrong_json_field_types(
    tmp_path: Path,
) -> None:
    """Wrong JSON field types surface as ValueError, not TypeError."""
    witness_path = _write_chat_completion(tmp_path, content=123)
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match="content must be a string"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-1",
            runner_id="olmocr",
            artifact_paths=[str(witness_path)],
            coordinate_space=_coordinate_space(),
        )


def test_adapt_page_raises_value_error_for_corrupt_json(tmp_path: Path) -> None:
    """Corrupt JSON bytes are rejected as invalid witness payloads."""
    witness_path = tmp_path / "corrupt.json"
    witness_path.write_bytes(b"{not valid json")
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match=r"UTF-8 JSON chat\.completion"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-1",
            runner_id="olmocr",
            artifact_paths=[str(witness_path)],
            coordinate_space=_coordinate_space(),
        )


def test_adapt_page_raises_value_error_for_invalid_utf8(tmp_path: Path) -> None:
    """Invalid UTF-8 bytes are rejected as invalid witness payloads."""
    witness_path = tmp_path / "invalid-utf8.json"
    witness_path.write_bytes(b"\xff\xfe")
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match=r"UTF-8 JSON chat\.completion"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-1",
            runner_id="olmocr",
            artifact_paths=[str(witness_path)],
            coordinate_space=_coordinate_space(),
        )


def test_adapt_page_strips_trailing_newline_empty_line(tmp_path: Path) -> None:
    """Trailing newline must not produce an extra empty line/span."""
    witness_path = _write_chat_completion(
        tmp_path,
        content="Line one of diplomatic text.\nLine two of diplomatic text.\n",
    )
    service = WitnessAdaptationService()
    page = service.adapt_page(
        prepared_page=_prepared_page(),
        witness_id="wit-1",
        runner_id="olmocr",
        artifact_paths=[str(witness_path)],
        coordinate_space=_coordinate_space(),
    )

    assert len(page.lines) == 2
    assert len(page.spans) == 2
    assert page.spans[0].text_diplomatic == "Line one of diplomatic text."
    assert page.spans[1].text_diplomatic == "Line two of diplomatic text."


def test_adapt_page_builds_provisional_graph_for_kraken(tmp_path: Path) -> None:
    """C1-shaped kraken chat.completion yields non-empty provisional graph."""
    witness_path = tmp_path / "kraken-witness.json"
    shutil.copy(_KRAKEN_FIXTURE, witness_path)
    prepared = _prepared_page()
    service = WitnessAdaptationService()

    page = service.adapt_page(
        prepared_page=prepared,
        witness_id="wit-kraken-1",
        runner_id="kraken",
        artifact_paths=[str(witness_path)],
        coordinate_space=_coordinate_space(),
    )

    assert page.witness_id == "wit-kraken-1"
    assert page.runner_id == "kraken"
    assert page.prepared_page_id == "prepared-page-1"
    assert len(page.regions) == 1
    assert page.regions[0].region_kind is RegionKind.BODY
    assert page.regions[0].region_id == "prepared-page-1:r0"
    assert len(page.lines) == 2
    assert len(page.spans) == 2
    assert page.lines[0].line_id == "prepared-page-1:l0"
    assert page.lines[1].line_id == "prepared-page-1:l1"
    assert page.spans[0].span_id == "prepared-page-1:s0"
    assert page.spans[1].span_id == "prepared-page-1:s1"
    assert page.spans[0].text_diplomatic == "Kraken line one of diplomatic text."
    assert page.spans[1].text_diplomatic == "Kraken line two of diplomatic text."


def test_adapt_page_stable_ids_for_kraken_across_rebuilds(tmp_path: Path) -> None:
    """Kraken adapt_page rebuilds keep ADR 0008 stable ids and diplomatic text."""
    witness_path = tmp_path / "kraken-witness.json"
    shutil.copy(_KRAKEN_FIXTURE, witness_path)
    prepared = _prepared_page()
    space = _coordinate_space()
    artifact_paths = [str(witness_path)]

    first = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-kraken-1",
        runner_id="kraken",
        artifact_paths=artifact_paths,
        coordinate_space=space,
    )
    second = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-kraken-1",
        runner_id="kraken",
        artifact_paths=artifact_paths,
        coordinate_space=space,
    )

    assert [r.region_id for r in first.regions] == [r.region_id for r in second.regions]
    assert [line.line_id for line in first.lines] == [
        line.line_id for line in second.lines
    ]
    assert [span.span_id for span in first.spans] == [
        span.span_id for span in second.spans
    ]
    assert [span.text_diplomatic for span in first.spans] == [
        span.text_diplomatic for span in second.spans
    ]


def test_adapt_kraken_structured_sets_per_line_boxes_and_baselines(
    tmp_path: Path,
) -> None:
    """Structured kraken v1 content yields per-line geometry in prepared-page space."""
    witness_path = tmp_path / "kraken-segmentation-witness.json"
    shutil.copy(_KRAKEN_SEGMENTATION_FIXTURE, witness_path)
    prepared = _prepared_page()
    space_id = prepared.coordinate_space.space_id

    page = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-kraken-structured-1",
        runner_id="kraken",
        artifact_paths=[str(witness_path)],
        coordinate_space=_coordinate_space(),
    )

    assert page.runner_id == "kraken"
    assert len(page.lines) == 2
    assert page.lines[0].line_id == f"{space_id}:l0"
    assert page.lines[1].line_id == f"{space_id}:l1"
    assert page.spans[0].text_diplomatic == "Diplomatic line one"
    assert page.spans[1].text_diplomatic == "Diplomatic line two"

    line0_box = page.lines[0].bounding_box
    line1_box = page.lines[1].bounding_box
    assert line0_box is not None
    assert line1_box is not None
    assert (line0_box.x0, line0_box.y0, line0_box.x1, line0_box.y1) != (
        line1_box.x0,
        line1_box.y0,
        line1_box.x1,
        line1_box.y1,
    )
    assert line0_box.x0 == 10
    assert line0_box.y0 == 20
    assert line0_box.x1 == 180
    assert line0_box.y1 == 50
    assert line0_box.coordinate_space_id == space_id
    assert line1_box.x0 == 10
    assert line1_box.y0 == 60
    assert line1_box.x1 == 180
    assert line1_box.y1 == 90
    assert line1_box.coordinate_space_id == space_id

    assert page.lines[0].baseline == [
        Point(x=10, y=40),
        Point(x=180, y=42),
    ]
    assert page.lines[1].baseline == [
        Point(x=10, y=80),
        Point(x=180, y=82),
    ]
    assert page.lines[0].baseline_coordinate_space_id == space_id
    assert page.lines[1].baseline_coordinate_space_id == space_id

    assert _coordinate_rich_line_count(page) == 2


def test_adapt_kraken_plain_text_fallback_has_no_line_boxes(
    tmp_path: Path,
) -> None:
    """Plain-text kraken chat.completion must not assign page-wide line boxes."""
    witness_path = tmp_path / "kraken-plain-witness.json"
    shutil.copy(_KRAKEN_FIXTURE, witness_path)
    prepared = _prepared_page()

    page = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-kraken-plain-1",
        runner_id="kraken",
        artifact_paths=[str(witness_path)],
        coordinate_space=_coordinate_space(),
    )

    assert len(page.lines) == 2
    assert all(line.bounding_box is None for line in page.lines)
    assert _coordinate_rich_line_count(page) == 0


def test_adapt_olmocr_provisional_has_no_line_boxes(tmp_path: Path) -> None:
    """OlmOCR provisional adaptation must not use page-wide line boxes."""
    witness_path = tmp_path / "olmocr-witness.json"
    shutil.copy(_FIXTURE, witness_path)
    prepared = _prepared_page()

    page = WitnessAdaptationService().adapt_page(
        prepared_page=prepared,
        witness_id="wit-olmocr-1",
        runner_id="olmocr",
        artifact_paths=[str(witness_path)],
        coordinate_space=_coordinate_space(),
    )

    assert len(page.lines) == 2
    assert all(line.bounding_box is None for line in page.lines)
    assert _coordinate_rich_line_count(page) == 0


def test_adapt_page_rejects_unsupported_runner_id(tmp_path: Path) -> None:
    """Unknown runner_id is rejected before parsing strategy selection."""
    witness_path = tmp_path / "witness.json"
    shutil.copy(_FIXTURE, witness_path)
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match=r"unsupported runner_id"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-1",
            runner_id="not-a-runner",
            artifact_paths=[str(witness_path)],
            coordinate_space=_coordinate_space(),
        )


def test_adapt_page_rejects_non_chat_completion_json_for_kraken(
    tmp_path: Path,
) -> None:
    """Kraken strategy rejects non-chat.completion JSON with a clear ValueError."""
    witness_path = tmp_path / "bad-kraken.json"
    witness_path.write_text(
        json.dumps({"object": "not.chat.completion", "choices": []}),
        encoding="utf-8",
    )
    service = WitnessAdaptationService()
    with pytest.raises(ValueError, match=r"chat\.completion"):
        service.adapt_page(
            prepared_page=_prepared_page(),
            witness_id="wit-kraken-1",
            runner_id="kraken",
            artifact_paths=[str(witness_path)],
            coordinate_space=_coordinate_space(),
        )
