# Copyright (C) 2026 Chris Malek.
"""Multi-witness merge prefers structured kraken geometry over provisional olmOCR."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from wordwending.models import (
    CoordinateSpace,
    MergePageInput,
    MergePolicy,
    PageClass,
    PassWitnessPage,
    PreparationMode,
    PreparedPage,
)
from wordwending.services.merge import (
    AbstainingMergeService,
    _coordinate_rich_line_count,
)
from wordwending.services.witness_adaptation import WitnessAdaptationService

_FIXTURES = Path(__file__).parent / "fixtures" / "assemble"
_OLMOCR_FIXTURE = _FIXTURES / "olmocr-chat-completion-v1.json"
_KRAKEN_SEGMENTATION_FIXTURE = _FIXTURES / "kraken-segmentation-v1.json"
_MULTI_WITNESS_MANIFEST = _FIXTURES / "manifest-multi-witness-v1.json"
_HANDS_OFF_MERGE_POLICY = (
    Path(__file__).parent / "fixtures" / "hands_off" / "merge-policy.json"
)
_DOCUMENT_RUN_MERGE_POLICY = (
    Path(__file__).parent / "fixtures" / "document_run" / "merge-policy.json"
)

# Distinct per-line boxes from kraken-segmentation-v1 (not full-page).
_KRAKEN_LINE_BOXES = (
    (10.0, 20.0, 180.0, 50.0),
    (10.0, 60.0, 180.0, 90.0),
)


def _prepared_page(*, prepared_page_id: str = "prepared-page-1") -> PreparedPage:
    """Return a minimal prepared page matching assemble fixtures."""
    return PreparedPage(
        prepared_page_id=prepared_page_id,
        preparation_mode=PreparationMode.FULL_PAGE,
        page_class=PageClass.ORDINARY_PROSE,
        image_path="prepared/page.png",
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


def _adapt_olmocr_and_kraken(
    tmp_path: Path,
) -> tuple[PassWitnessPage, PassWitnessPage]:
    """
    Adapt plain olmOCR + structured kraken witnesses for the same prepared page.

    Returns:
        ``(olmocr_witness, kraken_witness)`` adapted ``PassWitnessPage`` graphs.

    """
    olmocr_path = tmp_path / "olmocr-chat-completion-v1.json"
    kraken_path = tmp_path / "kraken-segmentation-v1.json"
    shutil.copy(_OLMOCR_FIXTURE, olmocr_path)
    shutil.copy(_KRAKEN_SEGMENTATION_FIXTURE, kraken_path)
    prepared = _prepared_page()
    space = _coordinate_space()
    adapter = WitnessAdaptationService()
    olmocr = adapter.adapt_page(
        prepared_page=prepared,
        witness_id="wit-olmocr",
        runner_id="olmocr",
        artifact_paths=[str(olmocr_path)],
        coordinate_space=space,
    )
    kraken = adapter.adapt_page(
        prepared_page=prepared,
        witness_id="wit-kraken",
        runner_id="kraken",
        artifact_paths=[str(kraken_path)],
        coordinate_space=space,
    )
    return olmocr, kraken


def _kraken_preferring_policy() -> MergePolicy:
    """Return multi-witness merge policy with kraken-first structure scaffold."""
    return MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        runner_text_precedence=["olmocr", "kraken"],
        structure_scaffold_runner_ids=["kraken", "olmocr"],
    )


def _olmocr_preferring_policy() -> MergePolicy:
    """Return multi-witness merge policy with olmOCR-first structure scaffold."""
    return MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        runner_text_precedence=["olmocr", "kraken"],
        structure_scaffold_runner_ids=["olmocr", "kraken"],
    )


def test_adapted_kraken_is_more_coordinate_rich_than_olmocr(tmp_path: Path) -> None:
    """Structured kraken lines carry geometry; provisional olmOCR lines do not."""
    olmocr, kraken = _adapt_olmocr_and_kraken(tmp_path)

    assert _coordinate_rich_line_count(kraken) > _coordinate_rich_line_count(olmocr)
    assert _coordinate_rich_line_count(olmocr) == 0
    assert _coordinate_rich_line_count(kraken) == 2


def test_multi_witness_merge_prefers_kraken_geometry(tmp_path: Path) -> None:
    """Merge with kraken-first scaffold accepts distinct kraken line boxes."""
    olmocr, kraken = _adapt_olmocr_and_kraken(tmp_path)
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[olmocr, kraken],
    )

    result = AbstainingMergeService().merge_page(
        page_input,
        _kraken_preferring_policy(),
    )

    assert len(result.page.lines) == 2
    boxes = []
    for line in result.page.lines:
        assert line.bounding_box is not None
        box = line.bounding_box
        assert box.coordinate_space_id == "prepared-page-1"
        # Must not collapse to full-page provisional geometry.
        assert (box.x0, box.y0, box.x1, box.y1) != (0.0, 0.0, 200.0, 300.0)
        boxes.append((box.x0, box.y0, box.x1, box.y1))
    assert tuple(boxes) == _KRAKEN_LINE_BOXES


def test_multi_witness_merge_olmocr_first_scaffold_skips_kraken_geometry(
    tmp_path: Path,
) -> None:
    """
    OlmOCR-first scaffold order keeps provisional null boxes, not kraken geometry.

    ``structure_scaffold_runner_ids`` is evaluated in order: olmOCR wins when
    listed first even though kraken carries coordinate-rich line boxes. Only
    kraken-first policy (see ``test_multi_witness_merge_prefers_kraken_geometry``)
    selects kraken-distinct line boxes for the merged page.
    """
    olmocr, kraken = _adapt_olmocr_and_kraken(tmp_path)
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[olmocr, kraken],
    )

    result = AbstainingMergeService().merge_page(
        page_input,
        _olmocr_preferring_policy(),
    )

    assert len(result.page.lines) == 2
    for line in result.page.lines:
        assert line.bounding_box is None
    boxes = tuple(
        None
        if line.bounding_box is None
        else (
            line.bounding_box.x0,
            line.bounding_box.y0,
            line.bounding_box.x1,
            line.bounding_box.y1,
        )
        for line in result.page.lines
    )
    assert boxes != _KRAKEN_LINE_BOXES


def test_multi_witness_merge_policy_fixtures_prefer_kraken_scaffold() -> None:
    """Multi-witness merge-policy fixtures list kraken before olmocr for scaffold."""
    manifest = json.loads(_MULTI_WITNESS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["merge_policy"]["structure_scaffold_runner_ids"] == [
        "kraken",
        "olmocr",
    ]

    for path in (_HANDS_OFF_MERGE_POLICY, _DOCUMENT_RUN_MERGE_POLICY):
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["structure_scaffold_runner_ids"] == ["kraken", "olmocr"]
