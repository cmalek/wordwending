# Spec 0010 Page Classification and Cohorts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish Spec 0010 by turning shipped page-class provenance into explicit preparation guidance and weighted evaluation cohorts.

**Architecture:** Keep Phase 3 deterministic classifier unchanged. Add class-specific recommended actions at assessment time, represent each evaluated page with run/preparation/runner context, then aggregate existing metric numerators and denominators into fixed cohort views.

**Tech Stack:** Python 3.13, Pydantic 2, stdlib grouping/JSON, Click, pytest.

**Sequence:** 3 of 4. Start only after the Spec 0007 plan passes final review.

## Global Constraints

- Keep v1 taxonomy exactly: `ordinary-prose`, `dense-dictionary`, `note-heavy`, `table-heavy`, `mixed-complex`.
- Page class remains auto-suggested, human-overridable, and stored in preparation provenance.
- Page class guides defaults; it never blocks an explicit operator choice.
- Aggregate metrics from summed numerators/denominators, never mean page values.
- Baseline views group by page class first.
- Support page-class-only, page-class/preparation-mode, and page-class/runner views.
- Preserve text, structure, and style families; emit no blended score.
- Add no dependency.
- Requires Spec 0003 completion plan before Task 2.
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

- `PageClass`, deterministic `PageClassifier`, final class/source/override reason, and preparation-mode interaction already ship.
- `PreparationAssessment.recommended_actions` exists but Phase 3 always writes an empty list.
- `EvaluationService` scores one page but outputs no run/document/preparation/runner context.
- No cohort aggregation service exists.

---

## File Map

- Modify: `bochord/services/preparation.py` — page-class guidance.
- Modify: `tests/test_preparation_service.py` — guidance and override checks.
- Modify: `bochord/models/evaluation.py` — evaluation records and cohort result models.
- Modify: `bochord/models/__init__.py` — export cohort contracts.
- Create: `bochord/services/evaluation_cohorts.py` — fixed weighted cohort aggregation.
- Modify: `bochord/services/__init__.py` — export cohort service if package convention requires it.
- Create: `tests/test_evaluation_cohorts.py` — cross-document/preparation/runner grouping.
- Modify: `bochord/cli/cli.py` — `eval-cohorts` file boundary.
- Modify: `tests/test_cli_commands.py` — cohort CLI contract.
- Create: `tests/fixtures/evaluation/cohort-records.json` — two classes, modes, documents, and runners.

### Task 1: Emit Page-Class Preparation Guidance

**Files:**

- Modify: `bochord/services/preparation.py`
- Modify: `tests/test_preparation_service.py`

**Interfaces:**

Existing `PreparationAssessment.recommended_actions: list[str]` receives stable
machine-readable actions:

```text
prefer-full-page
consider-column-subdivision
preserve-note-regions
review-note-linkage
preserve-table-regions
avoid-prose-flattening
preserve-layout-conservatively
require-stronger-review
```

Mapping:

```python
_PAGE_CLASS_ACTIONS = {
    PageClass.ORDINARY_PROSE: ["prefer-full-page"],
    PageClass.DENSE_DICTIONARY: ["consider-column-subdivision"],
    PageClass.NOTE_HEAVY: ["preserve-note-regions", "review-note-linkage"],
    PageClass.TABLE_HEAVY: ["preserve-table-regions", "avoid-prose-flattening"],
    PageClass.MIXED_COMPLEX: [
        "preserve-layout-conservatively",
        "require-stronger-review",
    ],
}
```

- [ ] **Step 1: Write failing guidance tests**

```python
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
```

- [ ] **Step 2: Run focused tests and verify empty list**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py -k "preparation_actions"
```

- [ ] **Step 3: Populate actions from final class**

Replace `recommended_actions=[]` in assessment construction with a copied list:

```python
recommended_actions=list(_PAGE_CLASS_ACTIONS[page_class_final])
```

Use final class, not suggested class, so operator override controls downstream
guidance. Keep mode-selection code unchanged.

- [ ] **Step 4: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_preparation_service.py
rtk git add bochord/services/preparation.py tests/test_preparation_service.py
rtk git commit -m "feat: emit page-class preparation guidance"
```

### Task 2: Define Evaluation Records and Cohort Output

**Files:**

- Modify: `bochord/models/evaluation.py`
- Modify: `bochord/models/__init__.py`
- Modify: `tests/test_ocr_models.py`
- Create: `tests/fixtures/evaluation/cohort-records.json`

**Interfaces:**

```python
class PageEvaluationRecord(SchemaModel):
    run_id: str
    document_id: str
    page_id: str
    page_class: PageClass
    preparation_mode: PreparationMode
    prepared_page_id: str
    runner_id: str
    summary: PageEvaluationSummary


class EvaluationCohortKey(SchemaModel):
    page_class: PageClass
    preparation_mode: PreparationMode | None = None
    runner_id: str | None = None


class EvaluationCohortSummary(SchemaModel):
    key: EvaluationCohortKey
    document_ids: list[str]
    page_ids: list[str]
    summary: PageEvaluationSummary


class EvaluationCohortReport(SchemaModel):
    by_page_class: list[EvaluationCohortSummary]
    by_page_class_and_preparation_mode: list[EvaluationCohortSummary]
    by_page_class_and_runner: list[EvaluationCohortSummary]
```

- [ ] **Step 1: Write failing strict-model tests**

```python
def test_page_evaluation_record_carries_comparison_context() -> None:
    record = PageEvaluationRecord(
        run_id="run-1",
        document_id="bt",
        page_id="page-0001",
        page_class=PageClass.DENSE_DICTIONARY,
        preparation_mode=PreparationMode.COLUMNS,
        prepared_page_id="prepared-a",
        runner_id="olmocr",
        summary=PageEvaluationSummary(),
    )
    assert record.page_class is PageClass.DENSE_DICTIONARY
    assert record.preparation_mode is PreparationMode.COLUMNS
```

Validate fixture with `TypeAdapter(list[PageEvaluationRecord])`.

- [ ] **Step 2: Run model test and verify missing imports**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py -k "evaluation_record"
```

- [ ] **Step 3: Add bare strict models and exports**

Models contain fields and validation only. Do not put grouping or averaging
logic in model classes. Fixture contains at least:

- two documents;
- ordinary and dense-dictionary pages;
- full-page and columns preparation;
- olmocr and kraken runner ids;
- one metric with denominator greater than one.

- [ ] **Step 4: Run model tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py
rtk git add bochord/models/evaluation.py bochord/models/__init__.py \
  tests/test_ocr_models.py tests/fixtures/evaluation/cohort-records.json
rtk git commit -m "feat: define evaluation cohort contracts"
```

### Task 3: Aggregate Fixed Cohort Views

**Files:**

- Create: `bochord/services/evaluation_cohorts.py`
- Modify: `bochord/services/__init__.py`
- Create: `tests/test_evaluation_cohorts.py`

**Interfaces:**

```python
class EvaluationCohortService:
    def summarize(
        self,
        records: list[PageEvaluationRecord],
    ) -> EvaluationCohortReport: ...
```

Grouping keys are fixed:

```python
lambda record: (record.page_class,)
lambda record: (record.page_class, record.preparation_mode)
lambda record: (record.page_class, record.runner_id)
```

Sort enum values by `.value`, runner ids lexically, document ids/page ids
lexically.

- [ ] **Step 1: Write failing weighted aggregation tests**

```python
def test_page_class_summary_sums_metric_denominators() -> None:
    report = EvaluationCohortService().summarize(
        [
            record("doc-a", numerator=8, denominator=10),
            record("doc-b", numerator=1, denominator=2),
        ]
    )
    score = metric(report.by_page_class[0].summary.text, "macron_recall")
    assert (score.numerator, score.denominator, score.value) == (9.0, 12.0, 0.75)
    assert report.by_page_class[0].document_ids == ["doc-a", "doc-b"]


def test_reports_split_same_class_by_mode_and_runner() -> None:
    report = EvaluationCohortService().summarize(
        [
            record("doc-a", mode=PreparationMode.FULL_PAGE, runner="olmocr"),
            record("doc-b", mode=PreparationMode.COLUMNS, runner="kraken"),
        ]
    )
    assert len(report.by_page_class) == 1
    assert len(report.by_page_class_and_preparation_mode) == 2
    assert len(report.by_page_class_and_runner) == 2
```

Also test empty input returns three empty lists.

- [ ] **Step 2: Run tests and verify service import failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_cohorts.py
```

- [ ] **Step 3: Implement weighted family aggregation**

For every metric id, sum numeric numerator and denominator. When total
denominator is zero:

- return unit error (`value=1`, `numerator=None`) only if any input metric has
  `denominator == 0`, `numerator is None`, and `value == 1`;
- otherwise return zero over zero.

```python
def _aggregate_metric(scores: list[MetricScore]) -> MetricScore:
    denominator = sum(score.denominator or 0.0 for score in scores)
    if denominator == 0:
        unit_error = any(
            score.numerator is None and score.value == 1.0 for score in scores
        )
        return MetricScore(
            metric_id=scores[0].metric_id,
            value=1.0 if unit_error else 0.0,
            numerator=None if unit_error else 0.0,
            denominator=0.0,
            note=(
                "one or more empty-reference predictions produced unit error"
                if unit_error
                else None
            ),
        )
    numerator = sum(score.numerator or 0.0 for score in scores)
    return MetricScore(
        metric_id=scores[0].metric_id,
        value=numerator / denominator,
        numerator=numerator,
        denominator=denominator,
    )
```

Aggregate text, structure, style typography, and style note linkage separately.
Carry flags in stable record order; do not invent cohort thresholds.

- [ ] **Step 4: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_evaluation_cohorts.py tests/test_evaluation_service.py
rtk git add bochord/services/evaluation_cohorts.py \
  bochord/services/__init__.py tests/test_evaluation_cohorts.py
rtk git commit -m "feat: summarize weighted evaluation cohorts"
```

### Task 4: Expose Cohort Summaries at CLI Boundary

**Files:**

- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_cli_commands.py`

**Interfaces:**

```text
bochord eval-cohorts RECORDS.json --output-json REPORT.json
```

`RECORDS.json` is a JSON array of `PageEvaluationRecord`.

- [ ] **Step 1: Write failing CLI test**

```python
def test_eval_cohorts_writes_all_fixed_views(runner, tmp_path: Path) -> None:
    output = tmp_path / "cohorts.json"
    result = runner.invoke(
        cli,
        [
            "eval-cohorts",
            "tests/fixtures/evaluation/cohort-records.json",
            "--output-json",
            str(output),
        ],
    )
    assert result.exit_code == 0
    report = EvaluationCohortReport.model_validate_json(output.read_text())
    assert report.by_page_class
    assert report.by_page_class_and_preparation_mode
    assert report.by_page_class_and_runner
```

- [ ] **Step 2: Implement thin command**

Command body:

1. read JSON;
2. validate with `TypeAdapter(list[PageEvaluationRecord])`;
3. call `EvaluationCohortService.summarize`;
4. write deterministic indented JSON;
5. translate I/O/JSON/Pydantic failures to `click.ClickException`.

No grouping or metric arithmetic in CLI.

- [ ] **Step 3: Run required quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/models/evaluation.py bochord/models/__init__.py \
  bochord/services/preparation.py bochord/services/evaluation_cohorts.py \
  bochord/services/__init__.py bochord/cli/cli.py \
  tests/test_ocr_models.py tests/test_preparation_service.py \
  tests/test_evaluation_cohorts.py tests/test_cli_commands.py
rtk .venv/bin/mypy bochord/models/evaluation.py bochord/models/__init__.py \
  bochord/services/preparation.py bochord/services/evaluation_cohorts.py \
  bochord/services/__init__.py bochord/cli/cli.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all pass.

- [ ] **Step 4: Commit**

```bash
rtk git add bochord/cli/cli.py tests/test_cli_commands.py
rtk git commit -m "feat: expose page-class cohort summaries"
```

## Cost Stop

Stop after fixed cohort JSON. No pandas, plots, ranking, statistical
significance engine, learned classifier, or threshold tuning. Add calibration
only after held-out cohort evidence shows repeatable classifier error.
