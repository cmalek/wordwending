# Phase 3 Acquisition and Preparation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn a PDF, image, ordered image folder, or ZIP into deterministic prepared page images with checksums, coordinate provenance, quality warnings, page class, and optional subdivisions.

**Architecture:** `SourceAcquisitionService` materializes ordered source pages. `PagePreparationService` is a thin facade over deterministic Pillow transforms, `PageQualityAssessor`, and `PageClassifier`; it writes preserved prepared images and metadata. Existing `PreparedPage` remains canonical output and gains its missing stable id.

**Tech Stack:** Python 3.13, Pydantic 2, Pillow 12, pypdfium2 5, stdlib path/archive/hash/JSON tools, Click, pytest.

## Global Constraints

- Accept PDF, single image, ordered image folder, and ZIP of images.
- Accept PNG, JPEG, TIFF, and JP2 where Pillow build supports decoder.
- For PDF pages, direct extraction is allowed only for one usable raster covering the page; otherwise render.
- Record acquisition mode per page.
- Preserve source ordering, names, checksums, dimensions, DPI, and source-to-prepared transforms.
- Preparation choice is per page and operator-overridable with recorded reason.
- Support `full-page`, `columns`, and `fixed-tiles`.
- Never execute OCR models.
- Add only `Pillow>=12.3.0` and `pypdfium2>=5.12.1`.
- Unsupported recipe modes fail clearly; no silent no-op transform.
- Follow repository Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Give Cursor one task section at a time plus only its listed files.

## Dependency Decision

Pillow is the established image primitive (13.6k GitHub stars and active 2026
releases). `pypdfium2` is actively released, liberal-licensed, renders PDF pages,
and extracts embedded rasters, so it replaces a two-library `pypdf` + renderer
stack. Package registry versions checked: Pillow `12.3.0`, pypdfium2 `5.12.1`.

---

## File Map

- Create: `bochord/models/preparation.py` — recipes, thresholds, acquisition, assessment, result.
- Modify: `bochord/models/ocr.py:819-840` — add `prepared_page_id`.
- Modify: `bochord/models/__init__.py` — export preparation contracts.
- Create: `bochord/services/source_acquisition.py` — source detection and page materialization.
- Create: `bochord/services/preparation.py` — assessment, classification, transforms, subdivision.
- Modify: `bochord/cli/cli.py` — thin `prepare` command.
- Create: `tests/test_source_acquisition.py`
- Create: `tests/test_preparation_service.py`
- Modify: `tests/test_cli_commands.py`
- Create: `tests/fixtures/preparation/recipe-v1.json`
- Modify: `pyproject.toml`, `uv.lock`

### Task 1: Preparation Contracts and Dependencies

**Files:**

- Create: `bochord/models/preparation.py`
- Modify: `bochord/models/ocr.py`
- Modify: `bochord/models/__init__.py`
- Modify: `tests/test_ocr_models.py`
- Create: `tests/fixtures/preparation/recipe-v1.json`
- Modify: `pyproject.toml`
- Modify: `uv.lock`

**Interfaces:**

```python
class PdfPageImageMode(StrEnum):
    EXTRACT_EMBEDDED = "extract-embedded"
    RENDER_PAGE = "render-page"
    AUTO = "auto"


class PreparationRecipe(BaseModel):
    recipe_id: str
    pdf_page_image_mode: PdfPageImageMode
    render_dpi: int
    color_mode: ColorMode
    deskew: bool
    denoise: bool
    crop_mode: CropMode
    binarize_mode: BinarizeMode
    dewarp_mode: DewarpMode
    subdivision_overlap_px: int
    fixed_tile_height_px: int
    thresholds: AssessmentThresholds
    notes: str | None = None


class SourcePageArtifact(BaseModel):
    artifact_id: str
    source_page_id: str
    page_number: int
    source_path: str
    source_filename: str
    checksum: str
    acquisition_mode: PdfPageImageMode | None
    coordinate_space: CoordinateSpace


class QualitySignal(BaseModel):
    signal_id: str
    value: float | None
    unit: str | None
    severity: FlagSeverity
    measured: bool


class PreparationAssessment(BaseModel):
    assessment_id: str
    source_page_id: str
    prepared_page_id: str | None
    signals: list[QualitySignal]
    flags: list[str]
    recommended_actions: list[str]
    warnings: list[str]
    page_class_suggested: PageClass
    page_class_final: PageClass
    page_class_source: Literal["auto", "operator"]
    operator_override_reason: str | None


class PreparationResult(BaseModel):
    source_page: SourcePageArtifact
    prepared_page: PreparedPage
    assessment: PreparationAssessment
    preparation_choice_source: Literal["auto", "operator"]
    operator_override_reason: str | None
```

`PreparedPage` gains:

```python
prepared_page_id: str
```

`PreparedArtifactRef` gains:

```python
parent_prepared_page_id: str | None = None
checksum: str | None = None
order: int | None = Field(default=None, ge=1)
```

Require all three fields when `kind is InputKind.PREPARED_UNIT`.

- [ ] **Step 1: Write failing contract tests**

```python
def test_operator_override_requires_reason() -> None:
    with pytest.raises(ValidationError):
        PreparationAssessment(
            assessment_id="assessment-page-1",
            source_page_id="page-0001",
            prepared_page_id=None,
            signals=[],
            flags=[],
            recommended_actions=[],
            warnings=[],
            page_class_suggested=PageClass.ORDINARY_PROSE,
            page_class_final=PageClass.DENSE_DICTIONARY,
            page_class_source="operator",
            operator_override_reason=None,
        )


def test_recipe_rejects_overlap_not_smaller_than_tile() -> None:
    payload = recipe_payload(subdivision_overlap_px=500, fixed_tile_height_px=500)
    with pytest.raises(ValidationError):
        PreparationRecipe.model_validate(payload)
```

- [ ] **Step 2: Run tests and verify imports fail**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py
```

Expected: new preparation model imports fail.

- [ ] **Step 3: Add image dependencies**

```bash
source .venv/bin/activate
rtk uv add "Pillow>=12.3.0" "pypdfium2>=5.12.1"
```

- [ ] **Step 4: Implement strict models and validators**

Threshold defaults:

```python
class AssessmentThresholds(BaseModel):
    """Calibratable limits for deterministic image-quality heuristics."""

    model_config = ConfigDict(extra="forbid")
    minimum_dpi: float = Field(default=300, gt=0)
    minimum_contrast_stddev: float = Field(default=25, ge=0)
    maximum_abs_skew_degrees: float = Field(default=1.5, gt=0)
    maximum_dark_margin_ratio: float = Field(default=0.25, ge=0, le=1)
    maximum_speckle_ratio: float = Field(default=0.02, ge=0, le=1)
    minimum_text_run_height_px: float = Field(default=18, gt=0)
```

Validators:

- operator class/mode override requires non-empty reason;
- `subdivision_overlap_px < fixed_tile_height_px`;
- render DPI and tile height are positive;
- prepared units require parent id, checksum, positive order, and bounding box;
- `dewarp_mode="basic"` raises during preparation until a replayable mapping artifact exists;
- every model uses `extra="forbid"`.

- [ ] **Step 5: Create `recipe-v1.json`**

```json
{
  "recipe_id": "historical-print-v1",
  "pdf_page_image_mode": "auto",
  "render_dpi": 400,
  "color_mode": "grayscale",
  "deskew": false,
  "denoise": false,
  "crop_mode": "none",
  "binarize_mode": "none",
  "dewarp_mode": "none",
  "subdivision_overlap_px": 64,
  "fixed_tile_height_px": 1600,
  "thresholds": {
    "minimum_dpi": 300,
    "minimum_contrast_stddev": 25,
    "maximum_abs_skew_degrees": 1.5,
    "maximum_dark_margin_ratio": 0.25,
    "maximum_speckle_ratio": 0.02,
    "minimum_text_run_height_px": 18
  },
  "notes": "Initial deterministic profile; calibrate from held-out gold."
}
```

- [ ] **Step 6: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py
rtk git add bochord/models pyproject.toml uv.lock \
  tests/test_ocr_models.py tests/fixtures/preparation/recipe-v1.json
rtk git commit -m "feat: define preparation contracts"
```

### Task 2: Source Acquisition

**Files:**

- Create: `bochord/services/source_acquisition.py`
- Create: `tests/test_source_acquisition.py`

**Interfaces:**

```python
class SourceAcquisitionService:
    def materialize(
        self,
        source: Path,
        output_dir: Path,
        recipe: PreparationRecipe,
    ) -> list[SourcePageArtifact]: ...
```

- [ ] **Step 1: Write failing image, ZIP, and PDF tests**

```python
def test_image_folder_uses_natural_page_order(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    write_image(source / "page-10.png")
    write_image(source / "page-2.jpg")

    pages = SourceAcquisitionService().materialize(
        source,
        tmp_path / "out",
        recipe(),
    )

    assert [page.source_filename for page in pages] == ["page-2.jpg", "page-10.png"]
    assert all(page.checksum.startswith("sha256:") for page in pages)


def test_zip_rejects_parent_path_member(tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with ZipFile(archive, "w") as output:
        output.writestr("../escape.png", b"bad")
    with pytest.raises(ValueError, match="unsafe archive member"):
        SourceAcquisitionService().materialize(archive, tmp_path / "out", recipe())


def test_pdf_auto_extracts_single_page_raster(tmp_path: Path) -> None:
    pdf = tmp_path / "one-page.pdf"
    Image.new("RGB", (200, 300), "white").save(pdf, "PDF", resolution=400)

    pages = SourceAcquisitionService().materialize(
        pdf,
        tmp_path / "out",
        recipe(pdf_page_image_mode="auto"),
    )

    assert len(pages) == 1
    assert pages[0].acquisition_mode in {
        PdfPageImageMode.EXTRACT_EMBEDDED,
        PdfPageImageMode.RENDER_PAGE,
    }
```

Add forced-render test asserting output dimensions equal page inches times `render_dpi`.

- [ ] **Step 2: Run tests and verify service import failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_source_acquisition.py
```

Expected: import failure for `SourceAcquisitionService`.

- [ ] **Step 3: Implement file and archive paths**

Rules:

- Natural sort uses stdlib `re.split(r"(\d+)", path.name.casefold())`.
- Single images and folder images retain source extension.
- ZIP supports only listed image extensions.
- Reject absolute members, `..` members, symlinks, duplicate normalized paths, empty archives, and non-image archives.
- Copy source pages to `<output_dir>/pages/<page-number><extension>`.
- Hash bytes with SHA-256 after materialization.
- Build ids from source checksum + one-based page number, never random UUID.

- [ ] **Step 4: Implement PDF paths**

Use `pypdfium2.PdfDocument`.

`auto` direct extraction rule:

1. page has exactly one displayed `PdfImage`;
2. image bounds cover at least 95% of page width and height;
3. native pixel dimensions imply at least `minimum_dpi`;
4. image can be decoded by Pillow.

Otherwise render:

```python
scale = recipe.render_dpi / 72
bitmap = page.render(scale=scale, grayscale=recipe.color_mode == ColorMode.GRAYSCALE)
image = bitmap.to_pil()
```

Record `EXTRACT_EMBEDDED` or `RENDER_PAGE` on each page. Close page, bitmap, and document objects deterministically.

- [ ] **Step 5: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_source_acquisition.py
rtk git add bochord/services/source_acquisition.py tests/test_source_acquisition.py
rtk git commit -m "feat: materialize ordered source pages"
```

### Task 3: Quality Assessment and Page Classification

**Files:**

- Create: `bochord/services/preparation.py`
- Create: `tests/test_preparation_service.py`

**Interfaces:**

```python
class PageQualityAssessor:
    def assess(
        self,
        source_page: SourcePageArtifact,
        image: Image.Image,
        recipe: PreparationRecipe,
    ) -> list[QualitySignal]: ...


class PageClassifier:
    def suggest(self, signals: list[QualitySignal]) -> PageClass: ...
```

Required signal ids:

```text
effective_dpi
skew_degrees
gutter_shadow_ratio
border_shadow_ratio
contrast_stddev
speckle_ratio
colored_marking_ratio
bleedthrough_proxy
median_text_run_height_px
column_count
table_rule_count
lower_page_ink_ratio
```

- [ ] **Step 1: Write failing synthetic-image tests**

```python
def test_dense_two_column_page_is_suggested_as_dictionary() -> None:
    image = dense_two_column_image(text_height=12)
    signals = PageQualityAssessor().assess(source_page(), image, recipe())

    assert PageClassifier().suggest(signals) is PageClass.DENSE_DICTIONARY


def test_low_contrast_page_emits_warning_signal() -> None:
    image = Image.new("L", (1000, 1400), 180)
    signals = PageQualityAssessor().assess(source_page(), image, recipe())
    contrast = signal_map(signals)["contrast_stddev"]
    assert contrast.severity is FlagSeverity.WARNING
```

Add skew, dark gutter, speckle, lower-page note density, and table-rule cases.

- [ ] **Step 2: Run tests and verify failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py -k "assess or class"
```

Expected: service import failure.

- [ ] **Step 3: Implement cheap deterministic signals**

Use Pillow only:

- grayscale `ImageStat.Stat` standard deviation for contrast;
- row-projection variance over angles `-3.0` through `3.0` in `0.5` steps for skew;
- left/right 8% and center 8% strip darkness for border/gutter;
- difference from `MedianFilter(size=3)` for speckle ratio;
- RGB channel spread for colored marking proxy;
- light/dark paired-pixel ratio for bleed-through proxy;
- thresholded row runs for median text height;
- sustained low-ink vertical valleys for column count;
- sustained dark horizontal/vertical runs for table-rule count;
- bottom-quarter versus middle-half ink density for note proxy.

Downsample longest edge to 1600 pixels before heuristics. Record scale so text-height signal returns source-image pixels.

- [ ] **Step 4: Implement auditable classifier**

Priority:

1. `TABLE_HEAVY` when `table_rule_count >= 6`.
2. `DENSE_DICTIONARY` when `column_count >= 2` and text height is below threshold.
3. `NOTE_HEAVY` when lower-page ink ratio is at least `1.5`.
4. `MIXED_COMPLEX` when at least three warning signals exist.
5. `ORDINARY_PROSE`.

Add:

```python
# ponytail: fixed heuristics; replace with calibrated cohort thresholds only
# when held-out evaluation shows a repeatable classification failure.
```

- [ ] **Step 5: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py -k "assess or class"
rtk git add bochord/services/preparation.py tests/test_preparation_service.py
rtk git commit -m "feat: assess and classify page images"
```

### Task 4: Deterministic Preparation and Subdivision

**Files:**

- Modify: `bochord/services/preparation.py`
- Modify: `tests/test_preparation_service.py`

**Interfaces:**

```python
class PagePreparationService:
    def __init__(
        self,
        assessor: PageQualityAssessor,
        classifier: PageClassifier,
    ) -> None: ...

    def prepare(
        self,
        source_page: SourcePageArtifact,
        recipe: PreparationRecipe,
        output_dir: Path,
        *,
        mode_override: PreparationMode | None = None,
        page_class_override: PageClass | None = None,
        override_reason: str | None = None,
    ) -> PreparationResult: ...
```

- [ ] **Step 1: Write failing deterministic and subdivision tests**

```python
def test_same_input_and_recipe_produce_same_checksum(tmp_path: Path) -> None:
    service = PagePreparationService(PageQualityAssessor(), PageClassifier())
    first = service.prepare(source_page(), recipe(), tmp_path / "first")
    second = service.prepare(source_page(), recipe(), tmp_path / "second")
    assert first.prepared_page.image_checksum == second.prepared_page.image_checksum
    assert first.prepared_page.prepared_page_id == second.prepared_page.prepared_page_id


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
    assert all(unit.parent_prepared_page_id == result.prepared_page.prepared_page_id for unit in units)
    assert all(unit.checksum for unit in units)
    assert all(unit.bounding_box.coordinate_space_id == "prepared-page-0001" for unit in units)
```

Add fixed-tile overlap/order test and unsupported dewarp failure.

- [ ] **Step 2: Run tests and verify failures**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py -k "checksum or units or tile or dewarp"
```

Expected: missing `PagePreparationService` or assertions fail.

- [ ] **Step 3: Implement supported transforms**

Supported now:

- color conversion: grayscale/RGB/binary;
- crop: none/trim margin/content bounding box;
- binarization: none/Otsu/adaptive;
- deskew: apply measured angle;
- denoise: median filter.

Reject `dewarp_mode="basic"` with `ValueError("basic dewarp requires a replayable mapping artifact")`.

Save PNG with fixed options and no volatile metadata. Hash saved bytes. Derive `prepared_page_id` from source checksum + canonical recipe JSON + mode.

- [ ] **Step 4: Implement preparation choice and units**

Auto mode:

- dense dictionary with `column_count >= 2` -> columns;
- text-size warning without reliable columns -> fixed tiles;
- otherwise full page.

Column units use detected vertical valleys, left-to-right order, and configured overlap. Fixed tiles use top-to-bottom order, configured height, and overlap. Every unit records:

- stable `prepared_unit_id`;
- parent prepared page id;
- bounding box in prepared-page coordinates;
- artifact path;
- checksum;
- order.

Keep logical page id unchanged.

- [ ] **Step 5: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py
rtk git add bochord/services/preparation.py tests/test_preparation_service.py
rtk git commit -m "feat: prepare and subdivide page images"
```

### Task 5: `bochord prepare` Vertical Check

**Files:**

- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_cli_commands.py`

**Interfaces:**

```text
bochord prepare SOURCE --recipe RECIPE.json --output-dir OUTPUT
  [--mode full-page|columns|fixed-tiles]
  [--page-class ordinary-prose|dense-dictionary|note-heavy|table-heavy|mixed-complex]
  [--override-reason TEXT]
```

Output:

```text
OUTPUT/
  source/pages/...
  pages/page-0001/image/page.png
  pages/page-0001/image/units/...
  pages/page-0001/preparation.json
```

- [ ] **Step 1: Write failing CLI test**

```python
def test_prepare_command_writes_reproducible_metadata(runner, tmp_path) -> None:
    source = tmp_path / "page.png"
    Image.new("L", (600, 800), "white").save(source)
    output = tmp_path / "bundle"

    result = runner.invoke(
        cli,
        [
            "prepare",
            str(source),
            "--recipe",
            "tests/fixtures/preparation/recipe-v1.json",
            "--output-dir",
            str(output),
        ],
    )

    assert result.exit_code == 0
    result_path = output / "pages/page-0001/preparation.json"
    assert PreparationResult.model_validate_json(result_path.read_text())
```

- [ ] **Step 2: Implement thin CLI orchestration**

Command body:

1. validate recipe JSON;
2. call `SourceAcquisitionService.materialize`;
3. call `PagePreparationService.prepare` per source page;
4. write each `PreparationResult` JSON;
5. print page count, warning count, and output path;
6. convert file, archive, decode, and validation failures to `click.ClickException`.

Reject override without reason at CLI boundary before writing files.

- [ ] **Step 3: Run required quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/models/preparation.py bochord/models/ocr.py \
  bochord/services/source_acquisition.py bochord/services/preparation.py \
  bochord/cli/cli.py tests/test_ocr_models.py \
  tests/test_source_acquisition.py tests/test_preparation_service.py \
  tests/test_cli_commands.py
rtk .venv/bin/mypy bochord/models/preparation.py bochord/models/ocr.py \
  bochord/services/source_acquisition.py bochord/services/preparation.py \
  bochord/cli/cli.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all pass.

- [ ] **Step 4: Commit**

```bash
rtk git add bochord/cli/cli.py tests/test_cli_commands.py
rtk git commit -m "feat: expose deterministic page preparation"
```

## Cost Stop

Stop after deterministic page artifacts and metadata. No recipe search, learned classifier, OpenCV, distributed workers, caching layer, or document orchestrator. Add one only when Phase 5 evaluation shows a measured need.
