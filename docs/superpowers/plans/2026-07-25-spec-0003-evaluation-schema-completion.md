# Spec 0003 Evaluation Schema Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close remaining Spec 0003 gaps by exposing exactly three top-level score families and adding watchlist-character exact-match scoring.

**Architecture:** Keep existing Phase 2 scorers and denominators. Nest existing typography and note-linkage summaries under one `style` family, then add one accumulator to existing text scorer; do not rewrite evaluation logic.

**Tech Stack:** Python 3.13, Pydantic 2, existing `regex` grapheme handling, pytest.

**Sequence:** 1 of 4. Finish this plan before starting Spec 0007.

## Global Constraints

- Preserve existing text, structure, typography, and note-linkage metric semantics.
- Top-level page and document families are exactly `text`, `structure`, and `style`.
- `style` keeps typography and note linkage independently inspectable.
- Add `watchlist_exact_match_rate`; retain existing per-family recall metrics.
- Gold coverage defines every denominator; `do_not_score` never enters one.
- Emit no blended score.
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

- Phase 2 already implements all required text, structure, typography, note-linkage, and review-flag behavior.
- `PageEvaluationSummary` and `DocumentEvaluationSummary` currently expose four top-level fields: `text`, `structure`, `typography`, `note_linkage`.
- Existing text scoring emits `exact_span_match_rate`, but Spec 0003 separately requires exact match over watchlist characters.

---

## File Map

- Modify: `bochord/models/ocr.py` — three-family output shape.
- Modify: `bochord/models/__init__.py` — export `StyleEvaluationSummary`.
- Modify: `bochord/services/evaluation.py` — construct nested style summary and accumulate watchlist exact match.
- Modify: `bochord/cli/cli.py` — update output contract wording only.
- Modify: `tests/test_ocr_models.py` — strict three-family schema checks.
- Modify: `tests/test_evaluation_service.py` — nested style and watchlist exact-match semantics.
- Modify: `tests/test_cli_commands.py` — serialized CLI output shape.
- Modify: `tests/fixtures/evaluation/page.json` — nested style fixture when summary is present.

### Task 1: Make Score Families Match Spec 0003

**Files:**

- Modify: `bochord/models/ocr.py`
- Modify: `bochord/models/__init__.py`
- Modify: `bochord/services/evaluation.py`
- Modify: `tests/test_ocr_models.py`
- Modify: `tests/test_evaluation_service.py`
- Modify: `tests/fixtures/evaluation/page.json`

**Interfaces:**

- Consumes: existing `EvaluationFamilySummary`.
- Produces:

```python
class StyleEvaluationSummary(SchemaModel):
    typography: EvaluationFamilySummary = Field(
        default_factory=EvaluationFamilySummary
    )
    note_linkage: EvaluationFamilySummary = Field(
        default_factory=EvaluationFamilySummary
    )


class PageEvaluationSummary(SchemaModel):
    text: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    structure: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    style: StyleEvaluationSummary = Field(default_factory=StyleEvaluationSummary)


class DocumentEvaluationSummary(SchemaModel):
    text: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    structure: EvaluationFamilySummary = Field(default_factory=EvaluationFamilySummary)
    style: StyleEvaluationSummary = Field(default_factory=StyleEvaluationSummary)
```

- [ ] **Step 1: Write failing schema and service tests**

```python
def test_page_evaluation_has_exactly_three_top_level_families() -> None:
    summary = PageEvaluationSummary()
    assert set(summary.model_dump()) == {"text", "structure", "style"}
    assert set(summary.style.model_dump()) == {"typography", "note_linkage"}


def test_evaluation_keeps_style_subfamilies_independent() -> None:
    typography = EvaluationService().evaluate_page(
        bold_but_not_italic_prediction(),
        bold_italic_gold(),
        profile(),
    )
    typography_metrics = {
        metric.metric_id: metric for metric in typography.style.typography.metrics
    }
    assert typography_metrics["font_slant_accuracy"].denominator == 1

    note_linkage = EvaluationService().evaluate_page(
        wrong_note_link_prediction(),
        note_link_gold(),
        profile(),
    )
    note_metrics = {
        metric.metric_id: metric for metric in note_linkage.style.note_linkage.metrics
    }
    assert note_metrics["note_linkage_success"].denominator == 1
```

Update any existing `summary.typography` and `summary.note_linkage` assertions to
`summary.style.typography` and `summary.style.note_linkage`.

- [ ] **Step 2: Run focused tests and verify failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py tests/test_evaluation_service.py \
  -k "evaluation or style"
```

Expected: missing `StyleEvaluationSummary` or old four-family assertions fail.

- [ ] **Step 3: Implement minimal schema nesting**

Add `StyleEvaluationSummary` next to existing evaluation summary models. Replace
top-level `typography` and `note_linkage` fields in page/document summaries with
`style`. Export new model from `bochord.models`.

Change only `EvaluationService.evaluate_page` construction:

```python
return PageEvaluationSummary(
    text=self._evaluate_text(prediction, gold, profile),
    structure=_StructureScorer().score(prediction, gold, profile),
    style=StyleEvaluationSummary(
        typography=_TypographyScorer().score(prediction, gold, profile),
        note_linkage=_NoteLinkageScorer().score(prediction, gold, profile),
    ),
)
```

Do not combine typography and note-linkage metric lists.

- [ ] **Step 4: Update fixtures and run focused tests**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py tests/test_evaluation_service.py
```

Expected: pass.

- [ ] **Step 5: Commit**

```bash
rtk git add bochord/models/ocr.py bochord/models/__init__.py \
  bochord/services/evaluation.py tests/test_ocr_models.py \
  tests/test_evaluation_service.py tests/fixtures/evaluation/page.json
rtk git commit -m "fix: expose three evaluation score families"
```

### Task 2: Add Watchlist Exact-Match Rate and CLI Contract

**Files:**

- Modify: `bochord/services/evaluation.py`
- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_evaluation_service.py`
- Modify: `tests/test_cli_commands.py`

**Interfaces:**

- Consumes: existing NFC grapheme lists and macron/ligature/thorn-eth predicates.
- Produces: text metric `MetricScore(metric_id="watchlist_exact_match_rate", ...)`.

One covered gold span contributes one denominator only when it contains at
least one watchlist grapheme. It succeeds only when prediction has exactly the
same ordered watchlist-grapheme sequence.

- [ ] **Step 1: Write failing exact-match tests**

```python
def test_watchlist_exact_match_counts_only_watchlist_spans() -> None:
    prediction, gold = text_case("þā", "þā")
    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}
    score = metrics["watchlist_exact_match_rate"]
    assert (score.numerator, score.denominator, score.value) == (1.0, 1.0, 1.0)

    plain_prediction, plain_gold = text_case("wrong", "plain")
    plain_summary = EvaluationService().evaluate_page(
        plain_prediction,
        plain_gold,
        profile(),
    )
    plain_metrics = {
        metric.metric_id: metric for metric in plain_summary.text.metrics
    }
    assert plain_metrics["watchlist_exact_match_rate"].denominator == 0


def test_watchlist_exact_match_rejects_extra_or_missing_watchlist_graphemes() -> None:
    prediction, gold = text_case("þþa", "þā")
    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}
    score = metrics["watchlist_exact_match_rate"]
    assert (score.numerator, score.denominator, score.value) == (0.0, 1.0, 0.0)

    reordered_prediction, reordered_gold = text_case("āþ", "þā")
    reordered = EvaluationService().evaluate_page(
        reordered_prediction,
        reordered_gold,
        profile(),
    )
    reordered_metrics = {
        metric.metric_id: metric for metric in reordered.text.metrics
    }
    assert reordered_metrics["watchlist_exact_match_rate"].value == 0
```

- [ ] **Step 2: Run tests and verify missing metric**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_service.py -k "watchlist_exact"
```

Expected: metric lookup fails.

- [ ] **Step 3: Add one accumulator to existing text loop**

Add `watchlist_exact` to `rates`. In `_score_text_pair`, after NFC grapheme
creation, filter ordered lists through any existing watchlist
predicate:

```python
watchlist_predicates = (_is_macron_grapheme, _is_ligature, _is_thorn_eth)
reference_watchlist = [
    grapheme
    for grapheme in ref_gs
    if any(predicate(grapheme) for predicate in watchlist_predicates)
]
if reference_watchlist:
    hypothesis_watchlist = [
        grapheme
        for grapheme in hyp_gs
        if any(predicate(grapheme) for predicate in watchlist_predicates)
    ]
    rates["watchlist_exact"].add(
        float(reference_watchlist == hypothesis_watchlist),
        1.0,
    )
```

Emit:

```python
rates["watchlist_exact"].to_metric(
    "watchlist_exact_match_rate",
    as_error_rate=False,
)
```

Keep `exact_span_match_rate` unchanged for backward analytical continuity.

- [ ] **Step 4: Assert serialized CLI shape**

Update CLI test to assert:

```python
payload = json.loads(output_json.read_text())
assert set(payload) == {"text", "structure", "style"}
assert "watchlist_exact_match_rate" in {
    item["metric_id"] for item in payload["text"]["metrics"]
}
```

Update `eval_page` docstring return-path wording from four families to three.

- [ ] **Step 5: Run required quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/models/ocr.py bochord/models/__init__.py \
  bochord/services/evaluation.py bochord/cli/cli.py \
  tests/test_ocr_models.py tests/test_evaluation_service.py \
  tests/test_cli_commands.py
rtk .venv/bin/mypy bochord/models/ocr.py bochord/models/__init__.py \
  bochord/services/evaluation.py bochord/cli/cli.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
rtk git add bochord/services/evaluation.py bochord/cli/cli.py \
  tests/test_evaluation_service.py tests/test_cli_commands.py
rtk git commit -m "feat: score exact watchlist retention"
```

## Cost Stop

Stop after schema nesting and missing metric. No evaluator rewrite, dataframe,
plotting, threshold dashboard, or blended score. Cohort aggregation belongs to
Spec 0010 plan.
