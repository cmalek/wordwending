# Spec 0007 Preparation Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete preparation provenance, preserve competing recipe variants, and support page-specific operator choices without replacing Phase 3 preparation.

**Architecture:** Reuse `SourceAcquisitionService`, `PagePreparationService`, and all Pillow heuristics/transforms. Add missing acquisition/recipe provenance, store each prepared identity in its own directory, and let the bundle facade apply optional overrides by source page.

**Tech Stack:** Python 3.13, Pydantic 2, existing Pillow 12 and pypdfium2 5, stdlib hashing/import metadata/JSON, Click, pytest.

**Sequence:** 2 of 4. Start only after the Spec 0003 plan passes final review.

## Global Constraints

- Phase 3 acquisition, assessment, transforms, and subdivision remain canonical.
- A recipe id plus different serialized content is a distinct variant, never a silent overwrite.
- Acquire source pages once when preparing multiple recipes.
- Preserve exact recipe JSON and SHA-256 digest in bundle.
- Record source type and PDF acquisition backend/version per page.
- Operator choices may target one page; every forced choice has a non-empty reason.
- Existing one-recipe `prepare_bundle` callers remain valid.
- Never execute OCR.
- Add no dependency.
- Follow repository Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Before Python commands: `source .venv/bin/activate`.
- After Python edits: touched-file `ruff`, touched-file `mypy`, `make napoleon-gate`, then focused/full pytest.

## Subagent Model Policy

- Dispatch each implementer with **Composer 2.5 fast**.
- Dispatch every task reviewer and final whole-plan reviewer with **Cursor Grok 4.5**.
- Fix rounds 1-3 resume Composer 2.5 fast; rounds 4-5 use fresh Cursor Grok 4.5 implementer.
- Use no other model.
- Give each implementer only generated task brief, prior-task interface decisions, and listed files.

For every task, use this serial Superpowers loop:

1. Composer 2.5 fast implements, runs the listed checks, self-reviews, and commits.
2. Cursor Grok 4.5 reviews spec compliance without editing.
3. Composer fixes rounds 1-3; if still failing, fresh Grok implementers handle
   rounds 4-5. The same Grok reviewer rechecks each round.
4. A fresh Cursor Grok 4.5 reviewer checks code quality without editing.
5. Apply the same fix-round policy to quality findings; that reviewer rechecks.

After the last task, a fresh Cursor Grok 4.5 reviewer audits the whole plan.
Do not start the next task or plan while either review has open findings.

## Existing Baseline

- Phase 3 already accepts PDF/image/folder/ZIP, assesses required quality signals, classifies pages, applies supported transforms, preserves checksums/transforms, and emits full-page/column/tile units.
- Current bundle layout stores one `preparation.json` and one prepared image per source page, so a second recipe overwrites the first.
- Current CLI overrides apply to every page.
- Current source artifacts record PDF acquisition mode but not source type or pypdfium2 identity.

---

## File Map

- Modify: `bochord/models/preparation.py` — source provenance and page override model.
- Modify: `bochord/models/ocr.py` — recipe digest on `PreparedPage`.
- Modify: `bochord/models/__init__.py` — export new contracts.
- Modify: `bochord/services/source_acquisition.py` — source type and backend identity.
- Modify: `bochord/services/preparation.py` — variant paths, recipe preservation, multi-recipe facade, per-page overrides.
- Modify: `bochord/cli/cli.py` — repeated recipe option and override manifest.
- Modify: `tests/test_ocr_models.py`
- Modify: `tests/test_source_acquisition.py`
- Modify: `tests/test_preparation_service.py`
- Modify: `tests/test_cli_commands.py`
- Modify: `tests/fixtures/preparation/recipe-v1.json` only if strict schema additions require it.
- Create: `tests/fixtures/preparation/page-overrides.json`

### Task 1: Complete Acquisition and Recipe Provenance

**Files:**

- Modify: `bochord/models/preparation.py`
- Modify: `bochord/models/ocr.py`
- Modify: `bochord/models/__init__.py`
- Modify: `bochord/services/source_acquisition.py`
- Modify: `bochord/services/preparation.py`
- Modify: `tests/test_ocr_models.py`
- Modify: `tests/test_source_acquisition.py`
- Modify: `tests/test_preparation_service.py`

**Interfaces:**

`SourcePageArtifact` gains:

```python
source_type: SourceType
acquisition_backend: str | None = None
acquisition_backend_version: str | None = None
```

`PreparedPage` gains:

```python
preparation_recipe_digest: str
```

Exact provenance values:

- PDF: `source_type=SourceType.PDF`, backend `pypdfium2`, installed distribution version.
- Single image: `source_type=SourceType.SINGLE_IMAGE`, backend fields `None`.
- Folder/ZIP: `source_type=SourceType.IMAGE_SET`, backend fields `None`.

- [ ] **Step 1: Write failing provenance tests**

```python
def test_pdf_page_records_acquisition_backend(tmp_path: Path) -> None:
    page = SourceAcquisitionService().materialize(
        pdf_fixture(),
        tmp_path,
        recipe(),
    )[0]
    assert page.source_type is SourceType.PDF
    assert page.acquisition_backend == "pypdfium2"
    assert page.acquisition_backend_version


def test_prepared_page_binds_full_recipe_digest(tmp_path: Path) -> None:
    result = preparation_service().prepare(source_page(), recipe(), tmp_path)
    expected = hashlib.sha256(
        recipe().model_dump_json().encode("utf-8")
    ).hexdigest()
    assert result.prepared_page.preparation_recipe_digest == expected
```

Add single-image and image-set source-type assertions.

- [ ] **Step 2: Run focused tests and verify validation failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py tests/test_source_acquisition.py \
  tests/test_preparation_service.py -k "provenance or source_type or recipe_digest"
```

Expected: missing fields.

- [ ] **Step 3: Populate provenance at acquisition boundary**

Pass `SourceType` into `_materialize_image_paths` based on caller. For PDF
artifacts, use stdlib package metadata:

```python
from importlib.metadata import version

backend = "pypdfium2"
backend_version = version(backend)
```

Do not put absolute source paths, credentials, or machine-local cache paths in
provenance.

- [ ] **Step 4: Bind prepared identity to recipe bytes**

Use one helper in `bochord.services.preparation`:

```python
def _recipe_digest(recipe: PreparationRecipe) -> str:
    return hashlib.sha256(
        recipe.model_dump_json().encode("utf-8")
    ).hexdigest()
```

Set `PreparedPage.preparation_recipe_digest` from this helper. Keep existing
prepared-page id derivation from source checksum, recipe JSON, and mode.

- [ ] **Step 5: Run focused tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py tests/test_source_acquisition.py \
  tests/test_preparation_service.py
rtk git add bochord/models/preparation.py bochord/models/ocr.py \
  bochord/models/__init__.py bochord/services/source_acquisition.py \
  bochord/services/preparation.py tests/test_ocr_models.py \
  tests/test_source_acquisition.py tests/test_preparation_service.py
rtk git commit -m "feat: complete preparation provenance"
```

### Task 2: Preserve Competing Preparation Variants

**Files:**

- Modify: `bochord/services/preparation.py`
- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_preparation_service.py`
- Modify: `tests/test_cli_commands.py`

**Interfaces:**

- Existing:

```python
PreparationBundleService.prepare_bundle(
    source: Path,
    recipe: PreparationRecipe,
    output_dir: Path,
    *,
    mode_override: PreparationMode | None = None,
    page_class_override: PageClass | None = None,
    override_reason: str | None = None,
) -> list[PreparationResult]
```

- New:

```python
PreparationBundleService.prepare_variants(
    source: Path,
    recipes: list[PreparationRecipe],
    output_dir: Path,
) -> list[PreparationResult]
```

`prepare_bundle` delegates to `prepare_variants` with one recipe and its current
global override behavior.

New layout:

```text
OUTPUT/
  source/pages/...
  recipes/<recipe-id>-<digest>.json
  pages/page-0001/prepared/<prepared-page-id>/image.png
  pages/page-0001/prepared/<prepared-page-id>/units/...
  pages/page-0001/prepared/<prepared-page-id>/preparation.json
```

- [ ] **Step 1: Write failing two-recipe test**

```python
def test_two_recipes_preserve_two_variants_without_reacquisition(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    acquisition = SourceAcquisitionService()
    spy = mocker.spy(acquisition, "materialize")
    recipes = [recipe(recipe_id="gray"), binary_recipe(recipe_id="binary")]

    results = bundle_service(acquisition).prepare_variants(
        source_image(),
        recipes,
        tmp_path,
    )

    assert spy.call_count == 1
    assert len(results) == 2
    assert len({item.prepared_page.prepared_page_id for item in results}) == 2
    assert all(Path(tmp_path, item.prepared_page.image_path).exists() for item in results)
    assert len(list((tmp_path / "recipes").glob("*.json"))) == 2
```

Add assertion that rerunning identical input/recipes produces byte-identical
metadata and does not create duplicate variant directories.

- [ ] **Step 2: Run focused test and verify overwrite**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py -k "two_recipes"
```

Expected: missing `prepare_variants`.

- [ ] **Step 3: Move persistence under prepared identity**

Pass `prepared_page_id` into output-path construction. Store page image, units,
and metadata inside its variant directory. `PreparedPage.image_path` and every
unit `artifact_path` remain bundle-relative.

Persist recipe with:

```python
recipe_name = f"{recipe.recipe_id}-{_recipe_digest(recipe)}.json"
recipe_path = output_dir / "recipes" / recipe_name
serialized = recipe.model_dump_json(indent=2)
if recipe_path.exists() and recipe_path.read_text(encoding="utf-8") != serialized:
    raise ValueError(f"recipe artifact collision: {recipe_name}")
recipe_path.write_text(serialized, encoding="utf-8")
```

Create parent directories before writes. Do not delete old variant directories.

- [ ] **Step 4: Add repeated CLI recipe input**

Make `--recipe` repeatable. One value calls `prepare_bundle`; two or more values
load all strict recipes and call `prepare_variants`.

CLI test:

```python
result = runner.invoke(
    cli,
    [
        "prepare",
        str(source),
        "--recipe",
        str(gray_recipe),
        "--recipe",
        str(binary_recipe),
        "--output-dir",
        str(output),
    ],
)
assert result.exit_code == 0
assert "variants: 2" in result.output
```

- [ ] **Step 5: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py tests/test_cli_commands.py
rtk git add bochord/services/preparation.py bochord/cli/cli.py \
  tests/test_preparation_service.py tests/test_cli_commands.py
rtk git commit -m "feat: preserve competing preparation variants"
```

### Task 3: Apply Page-Specific Operator Overrides

**Files:**

- Modify: `bochord/models/preparation.py`
- Modify: `bochord/models/__init__.py`
- Modify: `bochord/services/preparation.py`
- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_ocr_models.py`
- Modify: `tests/test_preparation_service.py`
- Modify: `tests/test_cli_commands.py`
- Create: `tests/fixtures/preparation/page-overrides.json`

**Interfaces:**

```python
class PagePreparationOverride(SchemaModel):
    source_page_id: str
    preparation_mode: PreparationMode | None = None
    page_class: PageClass | None = None
    reason: str

    @model_validator(mode="after")
    def validate_choice(self) -> PagePreparationOverride:
        if self.preparation_mode is None and self.page_class is None:
            raise ValueError("page override requires preparation_mode or page_class")
        if not self.reason.strip():
            raise ValueError("page override reason must not be empty")
        return self
```

`prepare_variants` becomes:

```python
PreparationBundleService.prepare_variants(
    source: Path,
    recipes: list[PreparationRecipe],
    output_dir: Path,
    *,
    page_overrides: dict[str, PagePreparationOverride] | None = None,
) -> list[PreparationResult]
```

Fixture:

```json
[
  {
    "source_page_id": "page-0002",
    "preparation_mode": "columns",
    "page_class": "dense-dictionary",
    "reason": "operator confirmed two lexical columns"
  }
]
```

- [ ] **Step 1: Write failing validation and mixed-page tests**

```python
def test_page_override_requires_choice_and_reason() -> None:
    with pytest.raises(ValidationError):
        PagePreparationOverride(source_page_id="page-0002", reason=" ")


def test_only_target_page_is_forced(tmp_path: Path) -> None:
    results = bundle_service().prepare_variants(
        two_page_source(),
        [recipe()],
        tmp_path,
        page_overrides={
            "page-0002": PagePreparationOverride(
                source_page_id="page-0002",
                preparation_mode=PreparationMode.COLUMNS,
                page_class=PageClass.DENSE_DICTIONARY,
                reason="operator confirmed two lexical columns",
            )
        },
    )
    assert results[0].preparation_choice_source == "auto"
    assert results[1].preparation_choice_source == "operator"
    assert results[1].assessment.page_class_source == "operator"
```

Also reject duplicate page ids and override ids absent from acquired source.

- [ ] **Step 2: Run focused tests and verify failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py tests/test_preparation_service.py \
  -k "page_override or target_page"
```

- [ ] **Step 3: Route one override per page**

Index overrides once, validate ids against acquired source ids, then pass only
matching values into `PagePreparationService.prepare`. Non-target pages receive
`None` overrides and remain automatic. Apply same page override to every recipe
variant so recipe comparisons do not change operator classification.

- [ ] **Step 4: Add `--overrides` manifest**

Add optional `--overrides PATH`. Reject use together with legacy global
`--mode`, `--page-class`, or `--override-reason`. Validate whole JSON before
acquisition so invalid input writes nothing.

```python
overrides = [
    PagePreparationOverride.model_validate(item)
    for item in json.loads(path.read_text(encoding="utf-8"))
]
```

- [ ] **Step 5: Run required quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/models/preparation.py bochord/models/ocr.py \
  bochord/models/__init__.py bochord/services/source_acquisition.py \
  bochord/services/preparation.py bochord/cli/cli.py \
  tests/test_ocr_models.py tests/test_source_acquisition.py \
  tests/test_preparation_service.py tests/test_cli_commands.py
rtk .venv/bin/mypy bochord/models/preparation.py bochord/models/ocr.py \
  bochord/models/__init__.py bochord/services/source_acquisition.py \
  bochord/services/preparation.py bochord/cli/cli.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
rtk git add bochord/models/preparation.py bochord/models/__init__.py \
  bochord/services/preparation.py bochord/cli/cli.py \
  tests/test_ocr_models.py tests/test_preparation_service.py \
  tests/test_cli_commands.py tests/fixtures/preparation/page-overrides.json
rtk git commit -m "feat: support per-page preparation overrides"
```

## Cost Stop

Stop after variants and page-local overrides. No recipe search, learned policy,
cache, database, distributed preparation, or UI. Add recipe ranking only after
cohort evaluation measures a repeatable winner.
