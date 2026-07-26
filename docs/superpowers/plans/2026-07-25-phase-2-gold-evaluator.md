# Phase 2 Gold Protocol and Evaluator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make one partial gold page reproducibly score text, structure, typography, and note linkage with fixed, explicit denominators.

**Architecture:** Reuse existing `GoldDocument`, `GoldPageAnnotation`, `BundlePage`, and evaluation-summary models. Add one versioned metric profile, one missing line-join gold record, and one cohesive `EvaluationService`. CLI only loads files, calls service, and writes JSON.

**Tech Stack:** Python 3.13, Pydantic 2, `regex` for Unicode grapheme clusters, stdlib JSON/Unicode handling, Click, pytest.

## Global Constraints

- Unicode text scoring uses NFC grapheme clusters.
- Whitespace, punctuation, case, line-break, tokenizer, illegibility, unknown-facet, empty-gold, and exclusion policies are explicit in metric profile.
- Gold coverage defines every denominator; `do_not_score` never enters a denominator.
- Test split is assigned before engine comparison.
- No blended score.
- No annotation UI, database, dataframe library, plotting library, or model inference.
- Add only `regex>=2026.7.19`; use stdlib for edit distance and aggregation.
- Phase 1 decision record must exist before execution starts.
- Follow repository Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Give Cursor one task section at a time plus only its listed files.

## Dependency Decision

Python stdlib normalizes Unicode but does not segment extended grapheme
clusters. `regex` directly supplies `\X`; package registry shows active releases
through `2026.7.19`. Do not add `jiwer`, `rapidfuzz`, or a metrics framework:
the remaining fixed-policy edit distance is one tested helper.

---

## File Map

- Create: `bochord/models/evaluation.py` — versioned metric policy.
- Modify: `bochord/models/ocr.py:1618-1800` — add `GoldLineJoin` and page field.
- Modify: `bochord/models/__init__.py` — export new contracts.
- Create: `bochord/services/evaluation.py` — all four score families.
- Modify: `bochord/cli/cli.py` — thin `eval` command.
- Create: `tests/test_evaluation_service.py` — metric semantics.
- Modify: `tests/test_cli_commands.py` — CLI contract.
- Create: `tests/fixtures/evaluation/metric-profile-v1.json` — frozen policy.
- Create: `tests/fixtures/evaluation/page.json` — one prediction for CLI check.
- Create: `tests/fixtures/evaluation/gold.json` — matching gold document.
- Create: `doc/source/runbook/gold_annotation.rst` — annotation/adjudication protocol.
- Modify: `doc/source/index.rst` — include protocol.
- Modify: `pyproject.toml`, `uv.lock` — `regex` dependency.

### Task 1: Freeze Metric and Gold Contracts

**Files:**

- Create: `bochord/models/evaluation.py`
- Modify: `bochord/models/ocr.py`
- Modify: `bochord/models/__init__.py`
- Create: `tests/fixtures/evaluation/metric-profile-v1.json`
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Modify: `tests/test_ocr_models.py`

**Interfaces:**

```python
class MetricProfile(BaseModel):
    profile_id: str
    version: str
    whitespace_significant: bool
    punctuation_significant: bool
    case_sensitive: bool
    line_breaks_significant: bool
    tokenizer_pattern: str
    region_iou_threshold: float
    exclude_illegible: bool
    unknown_style_is_incorrect: bool


class GoldLineJoin(SchemaModel):
    annotation_id: str
    left_line_id: str
    right_line_id: str
    joined: bool
    do_not_score: bool = False
    exclusion_reason: str | None = None
```

`GoldPageAnnotation` gains:

```python
line_joins: list[GoldLineJoin] = Field(default_factory=list)
```

`LineRecord` gains:

```python
joins_to_line_id: str | None = None
```

Extend `BundlePage.validate_graph_references` to reject a join target missing from
the same page.

- [ ] **Step 1: Add failing model tests**

```python
def test_metric_profile_rejects_invalid_iou_threshold() -> None:
    with pytest.raises(ValidationError):
        MetricProfile(
            profile_id="diplomatic-v1",
            version="1.0.0",
            whitespace_significant=True,
            punctuation_significant=True,
            case_sensitive=True,
            line_breaks_significant=True,
            tokenizer_pattern=r"\w+(?:['’]\w+)*|[^\w\s]",
            region_iou_threshold=1.1,
            exclude_illegible=True,
            unknown_style_is_incorrect=True,
        )


def test_excluded_line_join_requires_reason() -> None:
    with pytest.raises(ValidationError):
        GoldLineJoin(
            annotation_id="join-1",
            left_line_id="line-1",
            right_line_id="line-2",
            joined=True,
            do_not_score=True,
        )


def test_bundle_rejects_unknown_line_join_target() -> None:
    page = valid_bundle_page()
    page.lines[0].joins_to_line_id = "missing-line"
    with pytest.raises(ValidationError, match="unknown joined line"):
        BundlePage.model_validate(page.model_dump())
```

- [ ] **Step 2: Run tests and verify failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py
```

Expected: import failure for `MetricProfile` or `GoldLineJoin`.

- [ ] **Step 3: Add dependency and contracts**

```bash
source .venv/bin/activate
rtk uv add "regex>=2026.7.19"
```

Implement strict models:

```python
from pydantic import BaseModel, ConfigDict, Field


class MetricProfile(BaseModel):
    """Versioned, deterministic evaluation policy."""

    model_config = ConfigDict(extra="forbid")
    profile_id: str
    version: str
    whitespace_significant: bool = True
    punctuation_significant: bool = True
    case_sensitive: bool = True
    line_breaks_significant: bool = True
    tokenizer_pattern: str = r"\w+(?:['’]\w+)*|[^\w\s]"
    region_iou_threshold: float = Field(default=0.5, gt=0, le=1)
    exclude_illegible: bool = True
    unknown_style_is_incorrect: bool = True
```

Give `GoldLineJoin` the same exclusion validator used by `AnchoredGoldAnnotation`: `do_not_score=True` requires non-empty `exclusion_reason`.

- [ ] **Step 4: Create frozen profile**

`metric-profile-v1.json` values:

```json
{
  "profile_id": "diplomatic-page-v1",
  "version": "1.0.0",
  "whitespace_significant": true,
  "punctuation_significant": true,
  "case_sensitive": true,
  "line_breaks_significant": true,
  "tokenizer_pattern": "\\w+(?:['’]\\w+)*|[^\\w\\s]",
  "region_iou_threshold": 0.5,
  "exclude_illegible": true,
  "unknown_style_is_incorrect": true
}
```

- [ ] **Step 5: Run model tests**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
rtk git add bochord/models pyproject.toml uv.lock \
  tests/test_ocr_models.py tests/fixtures/evaluation/metric-profile-v1.json
rtk git commit -m "feat: freeze gold metric profile"
```

### Task 2: Text Evaluation

**Files:**

- Create: `bochord/services/evaluation.py`
- Create: `tests/test_evaluation_service.py`

**Interfaces:**

```python
class EvaluationService:
    def evaluate_page(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> PageEvaluationSummary: ...
```

Test helper `text_case(predicted, reference)` must return one `BundlePage` span
and one exhaustive, target-id-anchored `GoldTextSpan` covering text. `profile()`
loads `tests/fixtures/evaluation/metric-profile-v1.json`; neither helper may
change metric defaults.

Metric ids:

- `character_error_rate`
- `word_error_rate`
- `exact_span_match_rate`
- `macron_recall`
- `ligature_preservation_rate`
- `thorn_eth_preservation_rate`

- [ ] **Step 1: Write failing text test**

```python
def test_text_metrics_use_nfc_graphemes_and_explicit_denominators() -> None:
    prediction, gold = text_case(
        predicted="þæt drēam",
        reference="þæt dre\u0304am",
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].value == 0
    assert metrics["character_error_rate"].denominator == 9
    assert metrics["word_error_rate"].value == 0
    assert metrics["macron_recall"].value == 1
    assert metrics["thorn_eth_preservation_rate"].value == 1
```

Add cases for empty covered gold, `do_not_score`, excluded illegible text, punctuation policy, and missing `æ/þ/ð/macron`.

- [ ] **Step 2: Run test and verify failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_service.py -k text
```

Expected: import failure for `EvaluationService`.

- [ ] **Step 3: Implement text metrics**

Use these exact helpers:

```python
import unicodedata
import regex


def _graphemes(value: str) -> list[str]:
    return regex.findall(r"\X", unicodedata.normalize("NFC", value))


def _edit_distance(left: list[str], right: list[str]) -> int:
    previous = list(range(len(right) + 1))
    for left_index, left_item in enumerate(left, start=1):
        current = [left_index]
        for right_index, right_item in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1] + (left_item != right_item),
                )
            )
        previous = current
    return previous[-1]
```

Rules:

1. Resolve `target_object_id` directly; otherwise select same-family predicted object with highest box IoU at or above profile threshold.
2. Filter by exhaustive text coverage and exclusions.
3. Apply profile transformations before grapheme/token splitting.
4. Empty reference and empty prediction scores `0/0` with value `0`.
5. Empty reference and non-empty prediction records denominator `0`, value `1`, and explanatory note.
6. Watchlist recall counts reference graphemes, never unique character types.

Keep each method under 60 lines.

- [ ] **Step 4: Run text tests**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_service.py -k text
```

Expected: all text cases pass.

- [ ] **Step 5: Commit**

```bash
rtk git add bochord/services/evaluation.py tests/test_evaluation_service.py
rtk git commit -m "feat: score diplomatic OCR text"
```

### Task 3: Structure, Typography, Note Linkage, and Flags

**Files:**

- Modify: `bochord/services/evaluation.py`
- Modify: `tests/test_evaluation_service.py`

**Interfaces:**

Structure metric ids:

- `line_ordering_correctness`
- `region_coverage`
- `line_join_fidelity`
- `table_region_detection`

Typography/role metric ids:

- `font_weight_accuracy`
- `font_slant_accuracy`
- `baseline_shift_accuracy`
- `small_caps_accuracy`
- `letter_spacing_accuracy`
- `footnote_marker_retention`
- `footnote_block_detection`

- [ ] **Step 1: Write one failing test per score family**

```python
def test_structure_scores_region_order_iou_and_line_joins() -> None:
    summary = EvaluationService().evaluate_page(
        structured_prediction(),
        structured_gold(),
        profile(),
    )
    metrics = {metric.metric_id: metric.value for metric in summary.structure.metrics}
    assert metrics["region_coverage"] == 1
    assert metrics["line_ordering_correctness"] == 1
    assert metrics["line_join_fidelity"] == 1


def test_style_facets_are_independent() -> None:
    summary = EvaluationService().evaluate_page(
        bold_but_not_italic_prediction(),
        bold_italic_gold(),
        profile(),
    )
    metrics = {metric.metric_id: metric.value for metric in summary.typography.metrics}
    assert metrics["font_weight_accuracy"] == 1
    assert metrics["font_slant_accuracy"] == 0


def test_wrong_note_edge_emits_targeted_flag() -> None:
    summary = EvaluationService().evaluate_page(
        wrong_note_link_prediction(),
        note_link_gold(),
        profile(),
    )
    metrics = {
        metric.metric_id: metric.value for metric in summary.note_linkage.metrics
    }
    assert metrics["note_linkage_success"] == 0
    assert {flag.flag_type for flag in summary.note_linkage.flags} == {
        "ambiguous_note_linkage"
    }
```

- [ ] **Step 2: Run tests and verify failures**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_service.py -k "structure or style or note"
```

Expected: missing metrics or assertion failures.

- [ ] **Step 3: Implement remaining families**

Rules:

- Region match: same region kind, highest IoU, threshold from profile.
- Reading order: adjacent ordered relations from covered gold regions; denominator is count of gold adjacent pairs.
- Line join: compare each non-excluded `GoldLineJoin` to
  `LineRecord.joins_to_line_id`; no text-shape inference.
- Table presence: score only when exhaustive structure coverage contains a gold table region.
- Style: score each non-unknown facet separately. `bold + italic` contributes to two denominators.
- Note linkage: compare exact `(marker_span_id, note_id)` edges.
- Footnote marker and block are separate role/object metrics.

Emit these flags only when evidence exists:

```text
missing_watchlist_character
style_family_collapse
ambiguous_note_linkage
low_confidence_merged_graph_region
raw_pass_disagreement
```

Use `ObjectProvenance.merge_confidence` and `disagreement_note`; do not invent confidence from metric scores.

- [ ] **Step 4: Run evaluator tests**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_service.py
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
rtk git add bochord/services/evaluation.py tests/test_evaluation_service.py
rtk git commit -m "feat: score page evidence families"
```

### Task 4: Reproducible Operator Protocol and CLI

**Files:**

- Create: `doc/source/runbook/gold_annotation.rst`
- Modify: `doc/source/index.rst`
- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_cli_commands.py`

**Interfaces:**

```text
bochord eval --prediction PAGE.json --gold GOLD.json \
  --profile tests/fixtures/evaluation/metric-profile-v1.json \
  --output-json SCORES.json
```

- [ ] **Step 1: Write failing CLI test**

```python
def test_eval_command_writes_reproducible_scores(runner, tmp_path) -> None:
    output = tmp_path / "scores.json"
    result = runner.invoke(
        cli,
        [
            "eval",
            "--prediction",
            "tests/fixtures/evaluation/page.json",
            "--gold",
            "tests/fixtures/evaluation/gold.json",
            "--profile",
            "tests/fixtures/evaluation/metric-profile-v1.json",
            "--output-json",
            str(output),
        ],
    )
    assert result.exit_code == 0
    assert json.loads(output.read_text())["text"]["metrics"]
```

Create the small `page.json` and `gold.json` fixtures from passing service-test objects.

- [ ] **Step 2: Implement thin command**

Command body may only:

1. load `BundlePage`, `GoldDocument`, and `MetricProfile`;
2. select matching gold page by `page_id`;
3. call `EvaluationService.evaluate_page`;
4. write `PageEvaluationSummary.model_dump_json(indent=2)`;
5. convert validation/file errors to `click.ClickException`.

- [ ] **Step 3: Publish annotation protocol**

Document exact sequence:

1. assign `train`, `development`, or `test`;
2. record guideline id/version;
3. annotate coverage before annotations;
4. annotate diplomatic text, each typography facet, regions/order, line joins, and note edges;
5. record exclusions and illegibility separately;
6. second-annotate sampled slices;
7. retain both originals;
8. adjudicator writes resolution plus superseded ids;
9. run CLI twice and compare output bytes.

Include dictionary and footnote calibration examples using Phase 1 pages.

- [ ] **Step 4: Run final quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/models/evaluation.py bochord/models/ocr.py \
  bochord/services/evaluation.py bochord/cli/cli.py \
  tests/test_ocr_models.py tests/test_evaluation_service.py \
  tests/test_cli_commands.py
rtk .venv/bin/mypy bochord/models/evaluation.py bochord/models/ocr.py \
  bochord/services/evaluation.py bochord/cli/cli.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
rtk git add bochord/cli tests/test_cli_commands.py tests/fixtures/evaluation \
  doc/source/runbook/gold_annotation.rst doc/source/index.rst
rtk git commit -m "feat: expose reproducible gold evaluation"
```

## Cost Stop

Stop at one page-local evaluator and JSON CLI. No corpus database, dashboard, inter-annotator statistics package, optimizer, or benchmark runner. Add corpus aggregation in Phase 5 after held-out pages exist.
