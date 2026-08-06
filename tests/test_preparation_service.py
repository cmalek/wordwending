# Copyright (C) 2026 Chris Malek.
"""Tests for page quality assessment and classification."""

from __future__ import annotations

import hashlib
import json
import random
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from PIL import Image, ImageDraw

from wordwending.models import (
    CoordinateSpace,
    DewarpMode,
    FlagSeverity,
    PageClass,
    PagePreparationOverride,
    PreparationMode,
    PreparationRecipe,
    QualitySignal,
    SourcePageArtifact,
    SourceType,
)
from wordwending.services.preparation import (
    PageClassifier,
    PagePreparationService,
    PageQualityAssessor,
    PreparationBundleService,
    _recipe_digest,
)
from wordwending.services.source_acquisition import SourceAcquisitionService

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

#: Canonical preparation recipe fixture used by preparation tests.
_RECIPE_PATH = Path("tests/fixtures/preparation/recipe-v1.json")


def binary_recipe(**overrides: object) -> PreparationRecipe:
    """
    Load a binary/Otsu recipe variant for multi-recipe bundle tests.

    Keyword Args:
        overrides: Recipe fields to replace in the fixture payload.

    Returns:
        Validated binary preparation recipe.

    """
    return recipe(color_mode="binary", binarize_mode="otsu", **overrides)


def recipe(**overrides: object) -> PreparationRecipe:
    """
    Load the Phase 3 recipe fixture with optional field overrides.

    Keyword Args:
        overrides: Recipe fields to replace in the fixture payload.

    Returns:
        Validated preparation recipe.

    """
    payload = json.loads(_RECIPE_PATH.read_text(encoding="utf-8"))
    payload.update(overrides)
    return PreparationRecipe.model_validate(payload)


def _write_source_png(image: Image.Image, destination: Path) -> str:
    """
    Persist a source raster and return its ``sha256:`` checksum label.

    Args:
        image: Raster to write.
        destination: Output PNG path.

    Returns:
        Digest label for the written bytes.

    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(
        destination,
        format="PNG",
        optimize=False,
        compress_level=6,
        pnginfo=None,
        exif=b"",
        icc_profile=None,
    )
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    return f"sha256:{digest}"


def source_image() -> Path:
    """
    Write a single-page source raster for bundle tests.

    Returns:
        Path to a temporary PNG source image.

    """
    path = Path(tempfile.mkdtemp(prefix="wordwending-bundle-")) / "page.png"
    Image.new("L", (600, 800), "white").save(path)
    return path


def two_page_source() -> Path:
    """
    Write a two-page image folder for multi-page bundle tests.

    Returns:
        Path to a temporary folder with two ordered page images.

    """
    folder = Path(tempfile.mkdtemp(prefix="wordwending-two-page-"))
    Image.new("L", (600, 800), "white").save(folder / "page-1.png")
    dense_two_column_image(text_height=12).save(folder / "page-2.png")
    return folder


def bundle_service(
    acquisition: SourceAcquisitionService,
) -> PreparationBundleService:
    """
    Build a preparation bundle service wired to ``acquisition``.

    Args:
        acquisition: Source-page materializer used by the bundle service.

    Returns:
        Bundle service with stock page preparation collaborators.

    """
    return PreparationBundleService(
        acquisition,
        PagePreparationService(PageQualityAssessor(), PageClassifier()),
    )


def preparation_service() -> PagePreparationService:
    """
    Build the default page-preparation service for tests.

    Returns:
        Page preparation service with stock assessor and classifier.

    """
    return PagePreparationService(PageQualityAssessor(), PageClassifier())


def source_page(
    *,
    dpi: float | None = 400.0,
    image: Image.Image | None = None,
) -> SourcePageArtifact:
    """
    Build a source-page artifact backed by a written PNG.

    Keyword Args:
        dpi: Effective DPI recorded on the coordinate space.
        image: Optional raster; defaults to a blank RGB page.

    Returns:
        Source page artifact pointing at a temporary PNG file.

    """
    raster = (
        image if image is not None else Image.new("RGB", (1000, 1400), (255, 255, 255))
    )
    path = Path(tempfile.mkdtemp(prefix="wordwending-prep-")) / "0001.png"
    checksum = _write_source_png(raster, path)
    width, height = raster.size
    return SourcePageArtifact(
        artifact_id="artifact-page-1",
        source_page_id="page-0001",
        page_number=1,
        source_path=str(path),
        source_filename="0001.png",
        checksum=checksum,
        acquisition_mode=None,
        source_type=SourceType.SINGLE_IMAGE,
        acquisition_backend=None,
        acquisition_backend_version=None,
        coordinate_space=CoordinateSpace(
            space_id="space-page-1",
            width_px=width,
            height_px=height,
            dpi=dpi,
        ),
    )


def dense_source_page() -> SourcePageArtifact:
    """
    Build a two-column dense dictionary source page on disk.

    Returns:
        Source page artifact for column-subdivision tests.

    """
    return source_page(image=dense_two_column_image(text_height=12))


def signal_map(signals: list[QualitySignal]) -> dict[str, QualitySignal]:
    """
    Index quality signals by ``signal_id``.

    Args:
        signals: Measured quality signals from an assessment.

    Returns:
        Mapping from signal id to signal.

    """
    return {signal.signal_id: signal for signal in signals}


def dense_two_column_image(*, text_height: int = 12) -> Image.Image:
    """
    Build a synthetic two-column page with short text-run bars.

    Keyword Args:
        text_height: Height in pixels of each dark text-run bar.

    Returns:
        RGB page image with a clear center gutter.

    """
    width, height = 1000, 1400
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    left_x0, left_x1 = 60, 440
    right_x0, right_x1 = 560, 940
    y = 80
    while y + text_height < height - 80:
        draw.rectangle(
            (left_x0, y, left_x1, y + text_height - 1),
            fill=(20, 20, 20),
        )
        draw.rectangle(
            (right_x0, y, right_x1, y + text_height - 1),
            fill=(20, 20, 20),
        )
        y += text_height + 10
    return image


def skewed_line_image(*, angle_degrees: float = 2.0) -> Image.Image:
    """
    Build a page of horizontal text-like bars, then rotate it.

    Keyword Args:
        angle_degrees: Clockwise rotation applied after drawing bars.

    Returns:
        Grayscale page image with measurable skew.

    """
    width, height = 1000, 1400
    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)
    for y in range(100, height - 100, 28):
        draw.rectangle((80, y, width - 80, y + 6), fill=20)
    # Pillow rotate is counter-clockwise for positive angles; negate for clockwise.
    return image.rotate(
        -angle_degrees, resample=Image.Resampling.BICUBIC, fillcolor=255
    )


def dark_gutter_image() -> Image.Image:
    """
    Build a page with a dark vertical gutter in the center strip.

    Returns:
        Grayscale page image with elevated center-strip darkness.

    """
    width, height = 1000, 1400
    image = Image.new("L", (width, height), 240)
    draw = ImageDraw.Draw(image)
    gutter_width = int(width * 0.08)
    x0 = (width - gutter_width) // 2
    draw.rectangle((x0, 0, x0 + gutter_width - 1, height - 1), fill=30)
    return image


def speckled_image() -> Image.Image:
    """
    Build a mostly flat page with dense salt-and-pepper noise.

    Returns:
        Grayscale page image with elevated speckle ratio.

    """
    width, height = 1000, 1400
    image = Image.new("L", (width, height), 220)
    rng = random.Random(7)  # noqa: S311
    pixels = image.load()
    assert pixels is not None
    for _ in range(width * height // 8):
        x = rng.randrange(width)
        y = rng.randrange(height)
        pixels[x, y] = 0 if rng.random() < 0.5 else 255
    return image


def note_heavy_image() -> Image.Image:
    """
    Build a page with sparse body ink and dense bottom-quarter notes.

    Returns:
        Grayscale page image with elevated lower-page ink ratio.

    """
    width, height = 1000, 1400
    image = Image.new("L", (width, height), 250)
    draw = ImageDraw.Draw(image)
    # Sparse single-column body strokes in the middle half.
    for y in range(height // 4, (3 * height) // 4, 48):
        draw.rectangle((280, y, 720, y + 3), fill=40)
    # Dense bottom-quarter note field without page-wide rule runs.
    pixels = image.load()
    assert pixels is not None
    for y in range((3 * height) // 4, height - 10):
        for x in range(120, 880):
            if (x + 3 * y) % 3 != 0:
                pixels[x, y] = 25
    return image


def table_rule_image(*, rule_count: int = 8) -> Image.Image:
    """
    Build a page dominated by sustained dark table rules.

    Keyword Args:
        rule_count: Number of long horizontal rules to draw.

    Returns:
        Grayscale page image with many table rules.

    """
    width, height = 1000, 1400
    image = Image.new("L", (width, height), 250)
    draw = ImageDraw.Draw(image)
    for index in range(rule_count):
        y = 120 + index * 80
        draw.rectangle((80, y, width - 80, y + 3), fill=10)
    for x in (80, 350, 650, width - 80):
        draw.rectangle((x, 120, x + 3, 120 + (rule_count - 1) * 80), fill=10)
    return image


def test_dense_two_column_page_is_suggested_as_dictionary() -> None:
    image = dense_two_column_image(text_height=12)
    signals = PageQualityAssessor().assess(source_page(), image, recipe())

    assert PageClassifier().suggest(signals) is PageClass.DENSE_DICTIONARY


def test_low_contrast_page_emits_warning_signal() -> None:
    image = Image.new("L", (1000, 1400), 180)
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    contrast = signal_map(signals)["contrast_stddev"]
    assert contrast.severity is FlagSeverity.WARNING


def test_skewed_page_reports_nonzero_skew() -> None:
    image = skewed_line_image(angle_degrees=2.0)
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    skew = signal_map(signals)["skew_degrees"]
    assert skew.value is not None
    assert abs(skew.value) >= 1.5
    assert skew.severity is FlagSeverity.WARNING


def test_dark_gutter_emits_warning_signal() -> None:
    image = dark_gutter_image()
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    gutter = signal_map(signals)["gutter_shadow_ratio"]
    assert gutter.value is not None
    assert gutter.value > 0.25
    assert gutter.severity is FlagSeverity.WARNING


def test_speckled_page_emits_warning_signal() -> None:
    image = speckled_image()
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    speckle = signal_map(signals)["speckle_ratio"]
    assert speckle.value is not None
    assert speckle.value > 0.02
    assert speckle.severity is FlagSeverity.WARNING


def test_lower_page_note_density_is_suggested_as_note_heavy() -> None:
    image = note_heavy_image()
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    lower = signal_map(signals)["lower_page_ink_ratio"]
    assert lower.value is not None
    assert lower.value >= 1.5
    assert PageClassifier().suggest(signals) is PageClass.NOTE_HEAVY


def test_table_rule_page_is_suggested_as_table_heavy() -> None:
    image = table_rule_image(rule_count=8)
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    rules = signal_map(signals)["table_rule_count"]
    assert rules.value is not None
    assert rules.value >= 6
    assert PageClassifier().suggest(signals) is PageClass.TABLE_HEAVY


@pytest.mark.parametrize(
    ("page_class", "expected"),
    [
        (PageClass.ORDINARY_PROSE, ["prefer-full-page"]),
        (PageClass.DENSE_DICTIONARY, ["consider-column-subdivision"]),
        (
            PageClass.NOTE_HEAVY,
            ["preserve-note-regions", "review-note-linkage"],
        ),
        (
            PageClass.TABLE_HEAVY,
            ["preserve-table-regions", "avoid-prose-flattening"],
        ),
        (
            PageClass.MIXED_COMPLEX,
            ["preserve-layout-conservatively", "require-stronger-review"],
        ),
    ],
)
def test_final_page_class_emits_stable_preparation_actions(
    page_class: PageClass,
    expected: list[str],
    tmp_path: Path,
) -> None:
    result = preparation_service().prepare(
        source_page(),
        recipe(),
        tmp_path,
        page_class_override=page_class,
        override_reason="operator classified page",
    )
    assert result.assessment.recommended_actions == expected


def test_prepared_page_binds_full_recipe_digest(tmp_path: Path) -> None:
    result = preparation_service().prepare(source_page(), recipe(), tmp_path)
    expected = hashlib.sha256(
        recipe().model_dump_json().encode("utf-8")
    ).hexdigest()
    assert result.prepared_page.preparation_recipe_digest == expected


def test_same_input_and_recipe_produce_same_checksum(tmp_path: Path) -> None:
    service = PagePreparationService(PageQualityAssessor(), PageClassifier())
    first = service.prepare(source_page(), recipe(), tmp_path / "first")
    second = service.prepare(source_page(), recipe(), tmp_path / "second")
    assert first.prepared_page.image_checksum == second.prepared_page.image_checksum
    assert first.prepared_page.prepared_page_id == second.prepared_page.prepared_page_id


def test_operator_columns_without_valleys_raises(tmp_path: Path) -> None:
    with pytest.raises(
        ValueError,
        match="columns mode was requested but vertical valleys were not detected",
    ):
        PagePreparationService(
            PageQualityAssessor(),
            PageClassifier(),
        ).prepare(
            source_page(),
            recipe(),
            tmp_path,
            mode_override=PreparationMode.COLUMNS,
            override_reason="force columns without detectable valleys",
        )


def test_auto_columns_without_valleys_falls_back_to_full_page(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "wordwending.services.preparation._column_valley_centers",
        lambda _gray: [],
    )
    result = PagePreparationService(
        PageQualityAssessor(),
        PageClassifier(),
    ).prepare(dense_source_page(), recipe(), tmp_path)
    assert result.prepared_page.preparation_mode is PreparationMode.FULL_PAGE
    assert result.prepared_page.prepared_units == []
    assert any(
        "columns were requested but vertical valleys were not detected"
        in warning
        for warning in result.assessment.warnings
    )


def test_column_units_map_back_to_prepared_page(tmp_path: Path) -> None:
    result = PagePreparationService(
        PageQualityAssessor(),
        PageClassifier(),
    ).prepare(
        dense_source_page(),
        recipe(),
        tmp_path,
        mode_override=PreparationMode.COLUMNS,
        override_reason="known two-column dictionary leaf",
    )
    units = result.prepared_page.prepared_units
    assert len(units) == 2
    assert [unit.prepared_unit_id for unit in units] == [
        "page-0001-column-001",
        "page-0001-column-002",
    ]
    assert [unit.order for unit in units] == [1, 2]
    assert all(
        unit.parent_prepared_page_id == result.prepared_page.prepared_page_id
        for unit in units
    )
    assert all(unit.checksum for unit in units)
    assert all(
        unit.bounding_box is not None
        and unit.bounding_box.coordinate_space_id == "prepared-page-0001"
        for unit in units
    )


def test_fixed_tile_units_overlap_and_order(tmp_path: Path) -> None:
    result = PagePreparationService(
        PageQualityAssessor(),
        PageClassifier(),
    ).prepare(
        source_page(),
        recipe(fixed_tile_height_px=500, subdivision_overlap_px=100),
        tmp_path,
        mode_override=PreparationMode.FIXED_TILES,
        override_reason="force fixed tiles for overlap check",
    )
    units = result.prepared_page.prepared_units
    assert len(units) >= 2
    assert [unit.order for unit in units] == list(range(1, len(units) + 1))
    assert [unit.prepared_unit_id for unit in units] == [
        f"page-0001-tile-{index:03d}" for index in range(1, len(units) + 1)
    ]
    assert all(
        unit.parent_prepared_page_id == result.prepared_page.prepared_page_id
        for unit in units
    )
    for earlier, later in zip(units, units[1:], strict=False):
        assert earlier.bounding_box is not None
        assert later.bounding_box is not None
        assert earlier.bounding_box.y0 < later.bounding_box.y0
        assert earlier.bounding_box.y1 > later.bounding_box.y0
        overlap = earlier.bounding_box.y1 - later.bounding_box.y0
        assert overlap == pytest.approx(100)


def test_transform_chain_targets_final_prepared_space(tmp_path: Path) -> None:
    image = Image.new("RGB", (1000, 1400), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((200, 200, 800, 1200), fill=(20, 20, 20))
    result = PagePreparationService(
        PageQualityAssessor(),
        PageClassifier(),
    ).prepare(
        source_page(image=image),
        recipe(crop_mode="content-bounding-box"),
        tmp_path,
    )
    transforms = result.prepared_page.transforms
    assert transforms
    assert (
        transforms[-1].target_space_id
        == result.prepared_page.coordinate_space.space_id
        == "prepared-page-0001"
    )


def test_two_recipes_preserve_two_variants_without_reacquisition(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    acquisition = SourceAcquisitionService()
    spy = mocker.spy(acquisition, "materialize")
    recipes = [recipe(recipe_id="gray"), binary_recipe(recipe_id="binary")]
    source = source_image()

    service = bundle_service(acquisition)
    results = service.prepare_variants(
        source,
        recipes,
        tmp_path,
    )

    assert spy.call_count == 1
    assert len(results) == 2
    assert len({item.prepared_page.prepared_page_id for item in results}) == 2
    assert all(Path(tmp_path, item.prepared_page.image_path).exists() for item in results)
    assert len(list((tmp_path / "recipes").glob("*.json"))) == 2

    variant_dirs = sorted((tmp_path / "pages/page-0001/prepared").iterdir())
    first_metadata = {
        variant_dir / "preparation.json": (variant_dir / "preparation.json").read_bytes()
        for variant_dir in variant_dirs
    }

    results_rerun = service.prepare_variants(source, recipes, tmp_path)

    assert len(list((tmp_path / "pages/page-0001/prepared").iterdir())) == len(
        variant_dirs
    )
    assert len(results_rerun) == 2
    for variant_dir in variant_dirs:
        preparation_path = variant_dir / "preparation.json"
        assert preparation_path.read_bytes() == first_metadata[preparation_path]


def test_recipe_artifact_collision_raises(tmp_path: Path) -> None:
    colliding = recipe(recipe_id="gray")
    recipe_name = f"gray-{_recipe_digest(colliding)}.json"
    recipe_path = tmp_path / "recipes" / recipe_name
    recipe_path.parent.mkdir(parents=True)
    recipe_path.write_text('{"recipe_id": "gray", "wrong": true}', encoding="utf-8")

    with pytest.raises(ValueError, match="recipe artifact collision"):
        bundle_service(SourceAcquisitionService()).prepare_variants(
            source_image(),
            [colliding],
            tmp_path,
        )


def test_basic_dewarp_requires_mapping_artifact(tmp_path: Path) -> None:
    with pytest.raises(
        ValueError,
        match="basic dewarp requires a replayable mapping artifact",
    ):
        PagePreparationService(PageQualityAssessor(), PageClassifier()).prepare(
            source_page(),
            recipe(dewarp_mode=DewarpMode.BASIC),
            tmp_path,
        )


def test_only_target_page_is_forced(tmp_path: Path) -> None:
    results = bundle_service(SourceAcquisitionService()).prepare_variants(
        two_page_source(),
        [recipe()],
        tmp_path,
        page_overrides=[
            PagePreparationOverride(
                source_page_id="page-0002",
                preparation_mode=PreparationMode.COLUMNS,
                page_class=PageClass.DENSE_DICTIONARY,
                reason="operator confirmed two lexical columns",
            )
        ],
    )
    assert results[0].preparation_choice_source == "auto"
    assert results[1].preparation_choice_source == "operator"
    assert results[1].assessment.page_class_source == "operator"


def test_page_override_applies_to_every_recipe_variant(tmp_path: Path) -> None:
    results = bundle_service(SourceAcquisitionService()).prepare_variants(
        two_page_source(),
        [
            recipe(recipe_id="gray"),
            recipe(recipe_id="gray-denoised", denoise=True),
        ],
        tmp_path,
        page_overrides=[
            PagePreparationOverride(
                source_page_id="page-0002",
                preparation_mode=PreparationMode.COLUMNS,
                page_class=PageClass.DENSE_DICTIONARY,
                reason="operator confirmed two lexical columns",
            )
        ],
    )
    page_0002_results = [
        result
        for result in results
        if result.source_page.source_page_id == "page-0002"
    ]
    assert len(page_0002_results) == 2
    assert all(
        result.preparation_choice_source == "operator"
        for result in page_0002_results
    )
    assert all(
        result.assessment.page_class_source == "operator"
        for result in page_0002_results
    )


def test_page_override_rejects_duplicate_source_page_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="duplicate page override"):
        bundle_service(SourceAcquisitionService()).prepare_variants(
            two_page_source(),
            [recipe()],
            tmp_path,
            page_overrides=[
                PagePreparationOverride(
                    source_page_id="page-0002",
                    preparation_mode=PreparationMode.COLUMNS,
                    reason="first override",
                ),
                PagePreparationOverride(
                    source_page_id="page-0002",
                    page_class=PageClass.DENSE_DICTIONARY,
                    reason="duplicate override",
                ),
            ],
        )
    assert not (tmp_path / "source").exists()


def test_page_override_rejects_unknown_source_page_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown page override"):
        bundle_service(SourceAcquisitionService()).prepare_variants(
            source_image(),
            [recipe()],
            tmp_path,
            page_overrides=[
                PagePreparationOverride(
                    source_page_id="page-0099",
                    preparation_mode=PreparationMode.COLUMNS,
                    reason="operator confirmed two lexical columns",
                )
            ],
        )
    assert not (tmp_path / "pages").exists()
