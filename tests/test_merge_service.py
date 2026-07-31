# Copyright (C) 2026 Chris Malek.
"""Tests for abstaining merge policy models and merge service."""

from __future__ import annotations

import json
from pathlib import Path

from bochord.models import (
    BoundingBox,
    CoordinateSpace,
    LineRecord,
    MergeFlagType,
    MergePageInput,
    MergePolicy,
    ObjectProvenance,
    PageClass,
    PassWitnessPage,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    SpanRecord,
)
from bochord.services.merge import AbstainingMergeService


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        machine_confidence=0.91,
        merge_confidence=0.84,
    )


def test_merge_policy_defaults_empty_runner_text_precedence() -> None:
    """Empty precedence list means abstain on text disagreement (pre-benchmark)."""
    policy = MergePolicy(policy_id="merge-v1", version="1.0.0")
    assert policy.runner_text_precedence == []
    assert policy.structure_scaffold_runner_ids == []
    assert policy.min_merge_confidence_to_accept == 0.6
    assert policy.iou_match_threshold == 0.5
    assert policy.text_normalization_policy_id == "text-norm-v1"


def test_pass_witness_page_round_trip() -> None:
    """PassWitnessPage serializes and validates a runner page graph fragment."""
    provenance = _provenance()
    coordinate_space = CoordinateSpace(
        space_id="prepared-page-1",
        width_px=100,
        height_px=100,
    )
    witness = PassWitnessPage(
        witness_id="wit-1",
        runner_id="olmocr",
        prepared_page_id="prepared-page-1",
        coordinate_space=coordinate_space,
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
                provenance=provenance,
            )
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic="hello",
                text_normalized="hello",
                provenance=provenance,
            )
        ],
        machine_confidence=0.88,
    )
    payload = witness.model_dump(mode="json")
    round_tripped = PassWitnessPage.model_validate_json(json.dumps(payload))
    assert round_tripped.witness_id == "wit-1"
    assert round_tripped.runner_id == "olmocr"
    assert round_tripped.prepared_page_id == "prepared-page-1"
    assert len(round_tripped.regions) == 1
    assert len(round_tripped.lines) == 1
    assert len(round_tripped.spans) == 1
    assert round_tripped.machine_confidence == 0.88


_FIXTURES = Path(__file__).parent / "fixtures" / "merge"


def _prepared_page() -> PreparedPage:
    """Return a minimal prepared page shared by merge tests."""
    return PreparedPage(
        prepared_page_id="prepared-page-1",
        preparation_mode=PreparationMode.FULL_PAGE,
        page_class=PageClass.ORDINARY_PROSE,
        image_path="page.png",
        source_artifact_id="source-1",
        image_checksum="sha256:image",
        preparation_recipe_id="prep-v1",
        preparation_recipe_digest="digest-prep-v1",
        coordinate_space=CoordinateSpace(
            space_id="prepared-page-1",
            width_px=100,
            height_px=100,
        ),
    )


def _coordinate_space() -> CoordinateSpace:
    """Return coordinate space aligned to the test prepared page."""
    return CoordinateSpace(space_id="prepared-page-1", width_px=100, height_px=100)


def _witness_page(  # noqa: PLR0913
    *,
    witness_id: str,
    runner_id: str,
    prepared_page_id: str = "prepared-page-1",
    regions: list[RegionRecord] | None = None,
    lines: list[LineRecord] | None = None,
    spans: list[SpanRecord] | None = None,
) -> PassWitnessPage:
    """Build one pass witness fragment for merge tests."""
    return PassWitnessPage(
        witness_id=witness_id,
        runner_id=runner_id,
        prepared_page_id=prepared_page_id,
        coordinate_space=_coordinate_space(),
        regions=regions or [],
        lines=lines or [],
        spans=spans or [],
        machine_confidence=0.9,
    )


def _region(
    region_id: str,
    *,
    reading_order_index: int,
    line_ids: list[str],
    bounding_box: BoundingBox | None = None,
) -> RegionRecord:
    """Build one region record for merge tests."""
    return RegionRecord(
        region_id=region_id,
        region_kind=RegionKind.BODY,
        reading_order_index=reading_order_index,
        bounding_box=bounding_box,
        line_ids=line_ids,
        provenance=_provenance(),
    )


def _line(  # noqa: PLR0913
    line_id: str,
    *,
    region_id: str,
    line_order: int,
    span_ids: list[str],
    bounding_box: BoundingBox | None = None,
    baseline: list[tuple[float, float]] | None = None,
) -> LineRecord:
    """Build one line record for merge tests."""
    from bochord.models import Point

    return LineRecord(
        line_id=line_id,
        region_id=region_id,
        line_order=line_order,
        bounding_box=bounding_box,
        baseline=[Point(x=x, y=y) for x, y in (baseline or [])],
        span_ids=span_ids,
        provenance=_provenance(),
    )


def _span(span_id: str, *, line_id: str, text: str) -> SpanRecord:
    """Build one span record for merge tests."""
    return SpanRecord(
        span_id=span_id,
        line_id=line_id,
        text_diplomatic=text,
        text_normalized=text,
        provenance=_provenance(),
    )


def _load_merge_fixture(name: str) -> MergePageInput:
    """Load a merge page input fixture from JSON."""
    payload = json.loads((_FIXTURES / name).read_text(encoding="utf-8"))
    return MergePageInput.model_validate(payload)


def test_scaffold_preference_uses_structure_scaffold_runner_ids() -> None:
    """Runner order in policy chooses the structure scaffold witness."""
    witness_a = _witness_page(
        witness_id="wit-a",
        runner_id="runner-a",
        regions=[_region("region-a", reading_order_index=1, line_ids=["line-a"])],
        lines=[_line("line-a", region_id="region-a", line_order=1, span_ids=["span-a"])],
        spans=[_span("span-a", line_id="line-a", text="alpha")],
    )
    witness_b = _witness_page(
        witness_id="wit-b",
        runner_id="runner-b",
        regions=[_region("region-b", reading_order_index=1, line_ids=["line-b"])],
        lines=[_line("line-b", region_id="region-b", line_order=1, span_ids=["span-b"])],
        spans=[_span("span-b", line_id="line-b", text="beta")],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[witness_a, witness_b],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-b", "runner-a"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.page.regions[0].region_id == "region-b"
    assert result.page.lines[0].line_id == "line-b"
    assert result.page.spans[0].text_diplomatic == "beta"
    assert result.abstained is False
    assert not any(
        flag.flag_type == MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT
        for flag in result.flags
    )


def test_scaffold_preference_uses_coordinate_rich_lines_when_no_runner_order() -> None:
    """Without runner order, the witness with more geometry-rich lines wins."""
    sparse = _witness_page(
        witness_id="wit-sparse",
        runner_id="runner-sparse",
        regions=[_region("region-sparse", reading_order_index=1, line_ids=["line-sparse"])],
        lines=[
            _line(
                "line-sparse",
                region_id="region-sparse",
                line_order=1,
                span_ids=["span-sparse"],
            )
        ],
        spans=[_span("span-sparse", line_id="line-sparse", text="sparse")],
    )
    rich = _witness_page(
        witness_id="wit-rich",
        runner_id="runner-rich",
        regions=[_region("region-rich", reading_order_index=1, line_ids=["line-rich-1", "line-rich-2"])],
        lines=[
            _line(
                "line-rich-1",
                region_id="region-rich",
                line_order=1,
                span_ids=["span-rich-1"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            ),
            _line(
                "line-rich-2",
                region_id="region-rich",
                line_order=2,
                span_ids=["span-rich-2"],
                baseline=[(0.0, 20.0), (80.0, 20.0)],
            ),
        ],
        spans=[
            _span("span-rich-1", line_id="line-rich-1", text="one"),
            _span("span-rich-2", line_id="line-rich-2", text="two"),
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[sparse, rich],
    )
    policy = MergePolicy(policy_id="merge-v1", version="1.0.0")

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.page.regions[0].region_id == "region-rich"
    assert {line.line_id for line in result.page.lines} == {"line-rich-1", "line-rich-2"}


def test_cross_variant_witnesses_are_excluded_from_merge() -> None:
    """Witnesses on a different prepared page variant are skipped evidence."""
    aligned = _witness_page(
        witness_id="wit-aligned",
        runner_id="runner-aligned",
        regions=[_region("region-aligned", reading_order_index=1, line_ids=["line-aligned"])],
        lines=[
            _line(
                "line-aligned",
                region_id="region-aligned",
                line_order=1,
                span_ids=["span-aligned"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            )
        ],
        spans=[_span("span-aligned", line_id="line-aligned", text="aligned")],
    )
    cross_variant = _witness_page(
        witness_id="wit-cross",
        runner_id="runner-cross",
        prepared_page_id="prepared-page-2",
        regions=[_region("region-cross", reading_order_index=1, line_ids=["line-cross"])],
        lines=[
            _line(
                "line-cross",
                region_id="region-cross",
                line_order=1,
                span_ids=["span-cross"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            )
        ],
        spans=[_span("span-cross", line_id="line-cross", text="cross")],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[aligned, cross_variant],
    )
    policy = MergePolicy(policy_id="merge-v1", version="1.0.0")

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.page.regions[0].region_id == "region-aligned"
    skipped = [
        candidate
        for candidate in result.page.regions[0].provenance.alternate_candidates
        if candidate.value_kind == "skipped_witness"
    ]
    assert len(skipped) == 1
    assert skipped[0].witness_id == "wit-cross"
    assert skipped[0].runner_id == "runner-cross"
    assert skipped[0].value["prepared_page_id"] == "prepared-page-2"


def test_structure_scaffold_conflict_flags_and_abstains() -> None:
    """Incompatible region scaffolds emit conflict flags and alternate geometry."""
    page_input = _load_merge_fixture("structure_conflict.json")
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold", "runner-conflict"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.abstained is True
    conflict_flags = [
        flag
        for flag in result.flags
        if flag.flag_type == MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT
    ]
    assert len(conflict_flags) == 1
    assert result.page.regions[0].region_id == "region-scaffold-1"
    geometry_alternates = [
        candidate
        for candidate in result.page.regions[0].provenance.alternate_candidates
        if candidate.value_kind == "geometry"
    ]
    assert len(geometry_alternates) >= 1
    assert any(
        candidate.witness_id == "wit-conflict" for candidate in geometry_alternates
    )


def test_aligned_layout_fixture_produces_valid_bundle_page() -> None:
    """Aligned witnesses merge into a graph that passes bundle validation."""
    page_input = _load_merge_fixture("aligned_layout_text.json")
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-b", "runner-a"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.abstained is False
    assert len(result.page.regions) == 1
    assert len(result.page.lines) == 2
    assert len(result.page.spans) == 2
    assert result.page.regions[0].region_id == "region-b-1"


def test_lines_only_witness_not_chosen_when_regions_available() -> None:
    """Lines-only witnesses are ineligible; region-bearing witness wins scaffold."""
    lines_only = _witness_page(
        witness_id="wit-lines",
        runner_id="runner-lines",
        lines=[
            _line(
                "line-only-1",
                region_id="missing-region",
                line_order=1,
                span_ids=["span-only-1"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            ),
            _line(
                "line-only-2",
                region_id="missing-region",
                line_order=2,
                span_ids=["span-only-2"],
                baseline=[(0.0, 20.0), (80.0, 20.0)],
            ),
        ],
        spans=[
            _span("span-only-1", line_id="line-only-1", text="one"),
            _span("span-only-2", line_id="line-only-2", text="two"),
        ],
    )
    with_regions = _witness_page(
        witness_id="wit-regions",
        runner_id="runner-regions",
        regions=[
            _region(
                "region-with-structure",
                reading_order_index=1,
                line_ids=["line-regions"],
            )
        ],
        lines=[
            _line(
                "line-regions",
                region_id="region-with-structure",
                line_order=1,
                span_ids=["span-regions"],
            )
        ],
        spans=[_span("span-regions", line_id="line-regions", text="regions")],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[lines_only, with_regions],
    )
    policy = MergePolicy(policy_id="merge-v1", version="1.0.0")

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.page.regions[0].region_id == "region-with-structure"
    assert result.page.lines[0].line_id == "line-regions"
    assert result.abstained is False


def test_lines_only_witnesses_abstain_insufficient_evidence() -> None:
    """When no witness has regions, merge abstains without crashing."""
    lines_only_a = _witness_page(
        witness_id="wit-a",
        runner_id="runner-a",
        lines=[
            _line(
                "line-a",
                region_id="orphan-a",
                line_order=1,
                span_ids=["span-a"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            )
        ],
        spans=[_span("span-a", line_id="line-a", text="alpha")],
    )
    lines_only_b = _witness_page(
        witness_id="wit-b",
        runner_id="runner-b",
        lines=[
            _line(
                "line-b",
                region_id="orphan-b",
                line_order=1,
                span_ids=["span-b"],
                baseline=[(0.0, 10.0), (80.0, 10.0)],
            )
        ],
        spans=[_span("span-b", line_id="line-b", text="beta")],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[lines_only_a, lines_only_b],
    )
    policy = MergePolicy(policy_id="merge-v1", version="1.0.0")

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.abstained is True
    assert result.page.regions == []
    assert result.page.lines == []
    assert any(
        flag.flag_type == MergeFlagType.INSUFFICIENT_EVIDENCE for flag in result.flags
    )


def test_reversed_reading_order_flags_structure_conflict() -> None:
    """Same geometry with reversed reading order is a structure scaffold conflict."""
    top_box = BoundingBox(x0=0, y0=0, x1=100, y1=40)
    bottom_box = BoundingBox(x0=0, y0=50, x1=100, y1=90)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-top",
                reading_order_index=1,
                line_ids=["line-top"],
                bounding_box=top_box,
            ),
            _region(
                "region-bottom",
                reading_order_index=2,
                line_ids=["line-bottom"],
                bounding_box=bottom_box,
            ),
        ],
        lines=[
            _line(
                "line-top",
                region_id="region-top",
                line_order=1,
                span_ids=["span-top"],
            ),
            _line(
                "line-bottom",
                region_id="region-bottom",
                line_order=1,
                span_ids=["span-bottom"],
            ),
        ],
        spans=[
            _span("span-top", line_id="line-top", text="top"),
            _span("span-bottom", line_id="line-bottom", text="bottom"),
        ],
    )
    reversed_order = _witness_page(
        witness_id="wit-reversed",
        runner_id="runner-reversed",
        regions=[
            _region(
                "region-top-alt",
                reading_order_index=2,
                line_ids=["line-top-alt"],
                bounding_box=top_box,
            ),
            _region(
                "region-bottom-alt",
                reading_order_index=1,
                line_ids=["line-bottom-alt"],
                bounding_box=bottom_box,
            ),
        ],
        lines=[
            _line(
                "line-top-alt",
                region_id="region-top-alt",
                line_order=1,
                span_ids=["span-top-alt"],
            ),
            _line(
                "line-bottom-alt",
                region_id="region-bottom-alt",
                line_order=1,
                span_ids=["span-bottom-alt"],
            ),
        ],
        spans=[
            _span("span-top-alt", line_id="line-top-alt", text="top"),
            _span("span-bottom-alt", line_id="line-bottom-alt", text="bottom"),
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, reversed_order],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.abstained is True
    assert any(
        flag.flag_type == MergeFlagType.STRUCTURE_SCAFFOLD_CONFLICT
        for flag in result.flags
    )
