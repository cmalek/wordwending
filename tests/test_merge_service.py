# Copyright (C) 2026 Chris Malek.
"""Tests for abstaining merge policy models and merge service."""

from __future__ import annotations

import json
from pathlib import Path

from bochord.models import (
    BaselineShift,
    BoundingBox,
    CoordinateSpace,
    FontSlant,
    FontWeight,
    LineRecord,
    MergeFlagType,
    MergePageInput,
    MergePolicy,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PassWitnessPage,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    SpanRecord,
    TextRole,
    Typography,
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
    notes: list[NoteRecord] | None = None,
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
        notes=notes or [],
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


def _span(  # noqa: PLR0913
    span_id: str,
    *,
    line_id: str,
    text: str,
    bounding_box: BoundingBox | None = None,
    typography: Typography | None = None,
    roles: list[TextRole] | None = None,
) -> SpanRecord:
    """Build one span record for merge tests."""
    return SpanRecord(
        span_id=span_id,
        line_id=line_id,
        text_diplomatic=text,
        text_normalized=text,
        bounding_box=bounding_box,
        typography=typography or Typography(),
        roles=roles or [TextRole.TEXT],
        provenance=_provenance(),
    )


def _note(  # noqa: PLR0913
    note_id: str,
    *,
    text: str,
    linked_marker_span_ids: list[str] | None = None,
    bounding_box: BoundingBox | None = None,
    note_kind: NoteKind = NoteKind.FOOTNOTE_BLOCK,
    region_id: str | None = None,
) -> NoteRecord:
    """Build one note record for merge tests."""
    return NoteRecord(
        note_id=note_id,
        note_kind=note_kind,
        region_id=region_id,
        text_diplomatic=text,
        text_normalized=text,
        linked_marker_span_ids=linked_marker_span_ids or [],
        bounding_box=bounding_box,
        provenance=_provenance(),
    )


def _aligned_text_witnesses(
    *,
    scaffold_text: str,
    alternate_text: str,
    scaffold_runner: str = "runner-scaffold",
    alternate_runner: str = "runner-alt",
) -> tuple[PassWitnessPage, PassWitnessPage]:
    """Build two witnesses with overlapping geometry and differing span text."""
    box = BoundingBox(x0=0, y0=0, x1=80, y1=10)
    alt_box = BoundingBox(x0=1, y0=1, x1=79, y1=9)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id=scaffold_runner,
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-scaffold"],
                bounding_box=box,
            )
        ],
        spans=[
            _span(
                "span-scaffold",
                line_id="line-scaffold",
                text=scaffold_text,
                bounding_box=box,
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id=alternate_runner,
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-alt"],
                bounding_box=alt_box,
            )
        ],
        spans=[
            _span(
                "span-alt",
                line_id="line-alt",
                text=alternate_text,
                bounding_box=alt_box,
            )
        ],
    )
    return scaffold, alternate


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
        spans=[_span("span-a", line_id="line-a", text="beta")],
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


def test_scaffold_preference_picks_first_witness_for_duplicate_runner_id() -> None:
    """When multiple witnesses share a preferred runner, the first one wins."""
    first_runner_a = _witness_page(
        witness_id="wit-a-first",
        runner_id="runner-a",
        regions=[_region("region-a-first", reading_order_index=1, line_ids=["line-a-first"])],
        lines=[_line("line-a-first", region_id="region-a-first", line_order=1, span_ids=["span-a-first"])],
        spans=[_span("span-a-first", line_id="line-a-first", text="first")],
    )
    second_runner_a = _witness_page(
        witness_id="wit-a-second",
        runner_id="runner-a",
        regions=[_region("region-a-second", reading_order_index=1, line_ids=["line-a-second"])],
        lines=[_line("line-a-second", region_id="region-a-second", line_order=1, span_ids=["span-a-second"])],
        spans=[_span("span-a-second", line_id="line-a-second", text="first")],
    )
    runner_b = _witness_page(
        witness_id="wit-b",
        runner_id="runner-b",
        regions=[_region("region-b", reading_order_index=1, line_ids=["line-b"])],
        lines=[_line("line-b", region_id="region-b", line_order=1, span_ids=["span-b"])],
        spans=[_span("span-b", line_id="line-b", text="first")],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[first_runner_a, second_runner_a, runner_b],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-a", "runner-b"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.page.regions[0].region_id == "region-a-first"
    assert result.page.lines[0].line_id == "line-a-first"
    assert result.page.spans[0].text_diplomatic == "first"
    assert result.abstained is False


def test_merge_page_does_not_mutate_input_witnesses() -> None:
    """Merge deep-copies scaffold layout without altering input witness graphs."""
    witness = _witness_page(
        witness_id="wit-a",
        runner_id="runner-a",
        regions=[_region("region-a", reading_order_index=1, line_ids=["line-a"])],
        lines=[_line("line-a", region_id="region-a", line_order=1, span_ids=["span-a"])],
        spans=[_span("span-a", line_id="line-a", text="alpha")],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[witness],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-a"],
    )
    witness_snapshot = witness.model_dump(mode="json")

    AbstainingMergeService().merge_page(page_input, policy)

    assert witness.model_dump(mode="json") == witness_snapshot


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


def test_empty_precedence_text_disagreement_abstains() -> None:
    """Empty precedence with differing text flags disagreement and abstains."""
    scaffold, alternate = _aligned_text_witnesses(
        scaffold_text="scaffold-text",
        alternate_text="alternate-text",
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.text_diplomatic == "scaffold-text"
    assert span.provenance.merge_confidence == 0.3
    assert result.abstained is True
    text_flags = [
        flag for flag in result.flags if flag.flag_type == MergeFlagType.TEXT_DISAGREEMENT
    ]
    assert len(text_flags) == 1
    assert text_flags[0].target_object_ids == ["span-scaffold"]
    text_alternates = [
        candidate
        for candidate in span.provenance.alternate_candidates
        if candidate.value_kind == "text"
    ]
    assert len(text_alternates) >= 1


def test_precedence_picks_winner_and_flags_with_confidence_0_7() -> None:
    """Non-empty precedence accepts runner text at 0.7 when texts differ."""
    scaffold, alternate = _aligned_text_witnesses(
        scaffold_text="scaffold-text",
        alternate_text="alternate-text",
        scaffold_runner="runner-a",
        alternate_runner="runner-b",
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-a"],
        runner_text_precedence=["runner-b", "runner-a"],
        min_merge_confidence_to_accept=0.6,
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.text_diplomatic == "alternate-text"
    assert span.provenance.merge_confidence == 0.7
    assert result.abstained is False
    assert any(
        flag.flag_type == MergeFlagType.TEXT_DISAGREEMENT for flag in result.flags
    )


def test_precedence_confidence_0_7_abstains_when_min_is_0_8() -> None:
    """Precedence acceptance at 0.7 abstains when policy minimum is 0.8."""
    scaffold, alternate = _aligned_text_witnesses(
        scaffold_text="scaffold-text",
        alternate_text="alternate-text",
        scaffold_runner="runner-a",
        alternate_runner="runner-b",
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-a"],
        runner_text_precedence=["runner-b"],
        min_merge_confidence_to_accept=0.8,
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.page.spans[0].provenance.merge_confidence == 0.7
    assert result.abstained is True


def test_normalized_text_equality_no_disagreement_flag() -> None:
    """NFC-equivalent diplomatic strings agree without TEXT_DISAGREEMENT."""
    composed = "caf\u00e9"
    decomposed = "caf\u0065\u0301"
    scaffold, alternate = _aligned_text_witnesses(
        scaffold_text=composed,
        alternate_text=decomposed,
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.provenance.merge_confidence == 1.0
    assert not any(
        flag.flag_type == MergeFlagType.TEXT_DISAGREEMENT for flag in result.flags
    )
    assert result.abstained is False


def test_typography_facet_conflict_unknown_only_for_conflicting_facet() -> None:
    """Typography conflict sets unknown on the conflicting facet only."""
    box = BoundingBox(x0=0, y0=0, x1=80, y1=10)
    alt_box = BoundingBox(x0=1, y0=1, x1=79, y1=9)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-scaffold"],
                bounding_box=box,
            )
        ],
        spans=[
            _span(
                "span-scaffold",
                line_id="line-scaffold",
                text="same-text",
                bounding_box=box,
                typography=Typography(
                    weight=FontWeight.BOLD,
                    slant=FontSlant.UPRIGHT,
                    baseline_shift=BaselineShift.BASELINE,
                ),
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-alt"],
                bounding_box=alt_box,
            )
        ],
        spans=[
            _span(
                "span-alt",
                line_id="line-alt",
                text="same-text",
                bounding_box=alt_box,
                typography=Typography(
                    weight=FontWeight.REGULAR,
                    slant=FontSlant.UPRIGHT,
                    baseline_shift=BaselineShift.BASELINE,
                ),
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.typography.weight == FontWeight.UNKNOWN
    assert span.typography.slant == FontSlant.UPRIGHT
    assert span.typography.baseline_shift == BaselineShift.BASELINE
    assert span.provenance.merge_confidence == 0.3
    assert any(
        flag.flag_type == MergeFlagType.TYPOGRAPHY_CONFLICT for flag in result.flags
    )
    typo_alternates = [
        candidate
        for candidate in span.provenance.alternate_candidates
        if candidate.value_kind == "typography"
    ]
    assert len(typo_alternates) >= 1


def test_missing_typography_evidence_stays_unknown() -> None:
    """Witnesses without typography evidence never invent regular/upright."""
    box = BoundingBox(x0=0, y0=0, x1=80, y1=10)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-scaffold"],
                bounding_box=box,
            )
        ],
        spans=[
            _span(
                "span-scaffold",
                line_id="line-scaffold",
                text="same-text",
                bounding_box=box,
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=9),
            )
        ],
        spans=[
            _span(
                "span-alt",
                line_id="line-alt",
                text="same-text",
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=9),
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.typography.weight == FontWeight.UNKNOWN
    assert span.typography.slant == FontSlant.UNKNOWN
    assert span.typography.baseline_shift == BaselineShift.UNKNOWN
    assert not any(
        flag.flag_type == MergeFlagType.TYPOGRAPHY_CONFLICT for flag in result.flags
    )


def test_role_conflict_without_changing_typography() -> None:
    """Conflicting roles emit ROLE_CONFLICT without altering visual facets."""
    box = BoundingBox(x0=0, y0=0, x1=80, y1=10)
    alt_box = BoundingBox(x0=1, y0=1, x1=79, y1=9)
    bold_upright = Typography(
        weight=FontWeight.BOLD,
        slant=FontSlant.UPRIGHT,
        baseline_shift=BaselineShift.BASELINE,
    )
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-scaffold"],
                bounding_box=box,
            )
        ],
        spans=[
            _span(
                "span-scaffold",
                line_id="line-scaffold",
                text="same-text",
                bounding_box=box,
                typography=bold_upright,
                roles=[TextRole.TEXT],
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-alt"],
                bounding_box=alt_box,
            )
        ],
        spans=[
            _span(
                "span-alt",
                line_id="line-alt",
                text="same-text",
                bounding_box=alt_box,
                typography=bold_upright,
                roles=[TextRole.FOOTNOTE_MARKER],
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.roles == [TextRole.UNKNOWN]
    assert span.typography.weight == FontWeight.BOLD
    assert span.typography.slant == FontSlant.UPRIGHT
    assert any(flag.flag_type == MergeFlagType.ROLE_CONFLICT for flag in result.flags)
    assert span.provenance.merge_confidence == 0.3
    role_alternates = [
        candidate
        for candidate in span.provenance.alternate_candidates
        if candidate.value_kind == "role"
    ]
    assert len(role_alternates) >= 2
    assert {alt.runner_id for alt in role_alternates} == {
        "runner-scaffold",
        "runner-alt",
    }


def test_span_matching_without_bbox_ignores_line_order_witness() -> None:
    """Witnesses without bboxes do not match by reading order; scaffold text kept."""
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-scaffold"],
            )
        ],
        spans=[
            _span(
                "span-scaffold",
                line_id="line-scaffold",
                text="scaffold-text",
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-alt"],
            )
        ],
        spans=[
            _span(
                "span-alt",
                line_id="line-alt",
                text="alternate-text",
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    span = result.page.spans[0]
    assert span.text_diplomatic == "scaffold-text"
    assert not any(
        flag.flag_type == MergeFlagType.TEXT_DISAGREEMENT for flag in result.flags
    )


def test_span_matching_with_bbox_iou_flags_text_disagreement() -> None:
    """Overlapping witness bboxes with differing text emit TEXT_DISAGREEMENT."""
    scaffold, alternate = _aligned_text_witnesses(
        scaffold_text="alpha",
        alternate_text="beta",
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert any(
        flag.flag_type == MergeFlagType.TEXT_DISAGREEMENT for flag in result.flags
    )


def test_ambiguous_marker_iou_mapping_flags_note_link_ambiguous() -> None:
    """One witness marker overlapping two accepted spans is ambiguous linkage."""
    note_box = BoundingBox(x0=0, y0=20, x1=80, y1=35)
    alt_note_box = BoundingBox(x0=1, y0=21, x1=79, y1=34)
    marker_a_box = BoundingBox(x0=0, y0=0, x1=15, y1=10)
    marker_b_box = BoundingBox(x0=5, y0=0, x1=20, y1=10)
    witness_marker_box = BoundingBox(x0=5, y0=0, x1=18, y1=10)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-marker-a", "span-marker-b"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            )
        ],
        spans=[
            _span(
                "span-marker-a",
                line_id="line-scaffold",
                text="1",
                bounding_box=marker_a_box,
                roles=[TextRole.FOOTNOTE_MARKER],
            ),
            _span(
                "span-marker-b",
                line_id="line-scaffold",
                text="2",
                bounding_box=marker_b_box,
                roles=[TextRole.FOOTNOTE_MARKER],
            ),
        ],
        notes=[
            _note(
                "note-scaffold",
                text="Footnote body.",
                linked_marker_span_ids=["span-marker-a"],
                bounding_box=note_box,
                region_id="region-scaffold",
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-marker-x"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=9),
            )
        ],
        spans=[
            _span(
                "span-marker-x",
                line_id="line-alt",
                text="1",
                bounding_box=witness_marker_box,
                roles=[TextRole.FOOTNOTE_MARKER],
            )
        ],
        notes=[
            _note(
                "note-alt",
                text="Footnote body.",
                linked_marker_span_ids=["span-marker-x"],
                bounding_box=alt_note_box,
                region_id="region-alt",
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    note = result.page.notes[0]
    assert note.linked_marker_span_ids == []
    assert any(
        flag.flag_type == MergeFlagType.NOTE_LINK_AMBIGUOUS for flag in result.flags
    )


def test_ambiguous_note_links_clear_ids_and_flag() -> None:
    """Conflicting note link sets emit NOTE_LINK_AMBIGUOUS and clear links."""
    note_box = BoundingBox(x0=0, y0=20, x1=80, y1=35)
    alt_note_box = BoundingBox(x0=1, y0=21, x1=79, y1=34)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-marker-a"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            )
        ],
        spans=[
            _span(
                "span-marker-a",
                line_id="line-scaffold",
                text="1",
                bounding_box=BoundingBox(x0=0, y0=0, x1=10, y1=10),
                roles=[TextRole.FOOTNOTE_MARKER],
            )
        ],
        notes=[
            _note(
                "note-scaffold",
                text="Footnote body.",
                linked_marker_span_ids=["span-marker-a"],
                bounding_box=note_box,
                region_id="region-scaffold",
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-marker-b", "span-marker-c"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=9),
            )
        ],
        spans=[
            _span(
                "span-marker-b",
                line_id="line-alt",
                text="1",
                bounding_box=BoundingBox(x0=5, y0=1, x1=15, y1=9),
                roles=[TextRole.FOOTNOTE_MARKER],
            ),
            _span(
                "span-marker-c",
                line_id="line-alt",
                text="2",
                bounding_box=BoundingBox(x0=60, y0=1, x1=70, y1=9),
                roles=[TextRole.FOOTNOTE_MARKER],
            ),
        ],
        notes=[
            _note(
                "note-alt",
                text="Footnote body.",
                linked_marker_span_ids=["span-marker-c"],
                bounding_box=alt_note_box,
                region_id="region-alt",
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    note = result.page.notes[0]
    assert note.linked_marker_span_ids == []
    assert note.provenance.merge_confidence == 0.3
    assert result.abstained is True
    assert any(
        flag.flag_type == MergeFlagType.NOTE_LINK_AMBIGUOUS for flag in result.flags
    )
    link_alternates = [
        candidate
        for candidate in note.provenance.alternate_candidates
        if candidate.value_kind == "note_link"
    ]
    assert len(link_alternates) >= 1


def test_unambiguous_note_link_accepted() -> None:
    """Agreeing note link sets are accepted at merge_confidence 1.0."""
    note_box = BoundingBox(x0=0, y0=20, x1=80, y1=35)
    alt_note_box = BoundingBox(x0=1, y0=21, x1=79, y1=34)
    scaffold = _witness_page(
        witness_id="wit-scaffold",
        runner_id="runner-scaffold",
        regions=[
            _region(
                "region-scaffold",
                reading_order_index=1,
                line_ids=["line-scaffold"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=40),
            )
        ],
        lines=[
            _line(
                "line-scaffold",
                region_id="region-scaffold",
                line_order=1,
                span_ids=["span-marker-a"],
                bounding_box=BoundingBox(x0=0, y0=0, x1=80, y1=10),
            )
        ],
        spans=[
            _span(
                "span-marker-a",
                line_id="line-scaffold",
                text="1",
                bounding_box=BoundingBox(x0=0, y0=0, x1=10, y1=10),
                roles=[TextRole.FOOTNOTE_MARKER],
            )
        ],
        notes=[
            _note(
                "note-scaffold",
                text="Footnote body.",
                linked_marker_span_ids=["span-marker-a"],
                bounding_box=note_box,
                region_id="region-scaffold",
            )
        ],
    )
    alternate = _witness_page(
        witness_id="wit-alt",
        runner_id="runner-alt",
        regions=[
            _region(
                "region-alt",
                reading_order_index=1,
                line_ids=["line-alt"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=39),
            )
        ],
        lines=[
            _line(
                "line-alt",
                region_id="region-alt",
                line_order=1,
                span_ids=["span-marker-b"],
                bounding_box=BoundingBox(x0=1, y0=1, x1=79, y1=9),
            )
        ],
        spans=[
            _span(
                "span-marker-b",
                line_id="line-alt",
                text="1",
                bounding_box=BoundingBox(x0=1, y0=1, x1=9, y1=9),
                roles=[TextRole.FOOTNOTE_MARKER],
            )
        ],
        notes=[
            _note(
                "note-alt",
                text="Footnote body.",
                linked_marker_span_ids=["span-marker-b"],
                bounding_box=alt_note_box,
                region_id="region-alt",
            )
        ],
    )
    page_input = MergePageInput(
        page_id="page-0001",
        page_number=1,
        prepared_page=_prepared_page(),
        witnesses=[scaffold, alternate],
    )
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    note = result.page.notes[0]
    assert note.linked_marker_span_ids == ["span-marker-a"]
    assert note.provenance.merge_confidence == 1.0
    assert not any(
        flag.flag_type == MergeFlagType.NOTE_LINK_AMBIGUOUS for flag in result.flags
    )


def test_text_disagreement_fixture_smoke() -> None:
    """text_disagreement.json loads and merge flags text disagreement."""
    page_input = _load_merge_fixture("text_disagreement.json")
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert result.abstained is True
    assert any(
        flag.flag_type == MergeFlagType.TEXT_DISAGREEMENT for flag in result.flags
    )


def test_typography_conflict_fixture_smoke() -> None:
    """typography_conflict.json loads and merge flags typography conflict."""
    page_input = _load_merge_fixture("typography_conflict.json")
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert any(
        flag.flag_type == MergeFlagType.TYPOGRAPHY_CONFLICT for flag in result.flags
    )
    assert result.page.spans[0].typography.weight == FontWeight.UNKNOWN


def test_note_link_ambiguous_fixture_smoke() -> None:
    """note_link_ambiguous.json loads and merge flags ambiguous note links."""
    page_input = _load_merge_fixture("note_link_ambiguous.json")
    policy = MergePolicy(
        policy_id="merge-v1",
        version="1.0.0",
        structure_scaffold_runner_ids=["runner-scaffold"],
    )

    result = AbstainingMergeService().merge_page(page_input, policy)

    assert any(
        flag.flag_type == MergeFlagType.NOTE_LINK_AMBIGUOUS for flag in result.flags
    )
    assert result.page.notes[0].linked_marker_span_ids == []
