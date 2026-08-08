# DocumentRunOrchestrator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship Spec 0001’s thin `DocumentRunOrchestrator` so one config + one CLI command sequences prepare → multi-runner run → assemble-from-run → optional eval → issue review tasks → export under one logical `run_id`, without reimplementing stage logic.

**Architecture:** Facade only. Orchestrator calls existing stage modules (`PreparationBundleService`, `PassRunnerRegistry` + per-runner `RunnerExecutionService` factory, `AssembleManifestBuilder` + `AssembleOrchestrator`, `EvaluationService`, `BundleLayoutService.write_document_exports`, `ReviewCliService.issue`). Align/graph stay inside assemble/merge (Wave B waive stands). Human review **events** stay out of the automatic path; orchestrator auto-`issue`s pending tasks after assemble (and after eval when configured). Spec 0001 step “apply overlays” remains human-gated (`review apply` / `rebase`). CLI is a thin Click wrapper over a Pydantic `DocumentRunConfig`.

**Tech Stack:** Python 3.13, Click, Pydantic 2, pytest, existing `wordwending.services.*` stage modules.

## Locked Decisions

| Topic | Decision |
| --- | --- |
| Why now | Hands-off path closed manifest/tasks/rebase surgery. Runbook’s remaining product hole is **one orchestrated run id**. |
| Scope | Machine path only: prepare → run(s) → assemble → optional eval → `review issue` → export. **Not** auto `review apply` / `rebase` (needs human events). |
| Name | Class `DocumentRunOrchestrator` in `wordwending/services/document_run.py`. Keep `AssembleOrchestrator` for assemble-only. |
| Config | Single JSON `DocumentRunConfig`. **Path resolution:** `bundle_root`, `source_path`, `recipe_paths`, provenance/policy/gold paths resolve relative to the **config file’s parent directory** (or absolute). Not relative to `bundle_root` (source/recipes exist before prepare writes the tree). |
| document_id | Today `AssembleOrchestrator` sets `document_id=f"doc-{source.source_id}"`. **Lock:** either (A) extend `assemble_document` with optional `document_id=` kwarg used when provided, or (B) require `config.document_id == f"doc-{source.source_id}"` and validate. Prefer **(A)** so config is authoritative for run + assemble. |
| Runners | Config lists specs; `PassRunnerRegistry.resolve(runner_id)` returns a **class**, not an instance. Construct like CLI `_invoke_hosted_run` (RunnerReference + policy + endpoint URL + token + httpx client). Multi-runner → distinct `runs/{run_id}-{runner_id}/`. |
| skip_export vs stages | If `stages` is set, it is authoritative. `skip_export=True` only applies when `stages is None` (omit EXPORT from the default list). Do not combine contradictory meanings. |
| Eval | Optional. When `gold_page_paths` + `metric_profile_path` set, default stage order inserts **eval before issue_review_tasks** so issued tasks see eval flags. |
| Multi-runner ids | Execution `run_id` and run output folder stem = `{config.run_id}-{runner_id}` (matches `AssembleManifestBuilder` copy into `runs/<batch.run_id>/`). Never reuse bare `config.run_id` for two runners. |
| RunnerExecutionService | **Factory per runner** (CLI `_invoke_hosted_run` pattern). Do not inject one service bound to a single `PassRunner`. |
| Review issue API | Call shipped `ReviewCliService.issue(...)` (not `issue_tasks`). |
| Resume | Respect existing `ResumeLedgerService` on each `run` stage (`force` flag on config). No new global resume invent unless trivial. |
| Endpoints | Optional `ensure_endpoints: bool` — wire like CLI (`--ensure-endpoints`: settings overlay + hosted runner construction). |
| Out of scope | PageAlignmentService / PageGraphBuilder extraction; god-module splits; Phase 5 COMPLETE; Phase 10 COMPLETE; coordinate-rich kraken; auto review events. |
| ADR | 0001 workflow; 0002 bundle; 0004 raw untouched; 0006 registry; 0007 no new Fake adapter. |

## Subagent Model Policy

| Role | Model |
| --- | --- |
| Mechanical TDD | `composer-2.5-fast` |
| Integration / stuck / ADR review | `cursor-grok-4.5-medium` |
| Code-quality review | `composer-2.5-fast` |

Per task: implement → spec/ADR review → fix → quality review → fix → commit.

Every subagent prompt: workspace `/Users/cmalek/src/workspace/wordwending`; `source .venv/bin/activate`; `/usr/bin/cd`; graphify before explore; ruff/mypy/napoleon-gate/focused pytest; `graphify update .` after code.

## Global Constraints

- Activate `.venv`; `/usr/bin/cd` only.
- Relative posix `str` paths on SchemaModels.
- TDD; Napoleon `#:` / docstrings on non-test Python.
- Do not mark Spec 0004 Phase 5/10 COMPLETE.
- Prefer constructor injection of stage services; do not import Click inside the orchestrator.
- Do not duplicate assemble/run/prepare business logic — call collaborators.

## File Map

| File | Role |
| --- | --- |
| `wordwending/models/document_run.py` | **New** — `DocumentRunConfig`, stage result models |
| `wordwending/services/document_run.py` | **New** — `DocumentRunOrchestrator` |
| `wordwending/cli/cli.py` | Add `document-run` command |
| `tests/test_document_run.py` | **New** — orchestrator unit/integration with fakes/stubs |
| `tests/test_cli_commands.py` | CLI wiring tests |
| `tests/fixtures/document_run/` | **New** — minimal config + tiny source/recipe fixtures (or reuse hands_off/prep fixtures) |
| `doc/source/runbook/from_source_to_markdown.rst` | Document `document-run`; remove “Full DocumentRunOrchestrator” from missing |
| `README.md` | Add command |
| `AGENTS.md` | Mention `DocumentRunOrchestrator` alongside assemble/runner/merge orchestrators |

---

### Task 1: DocumentRunConfig models (TDD)

**Files:**
- Create: `wordwending/models/document_run.py`
- Create: `tests/test_document_run.py` (model validation section)
- Export from `wordwending/models/__init__.py` if that package re-exports peers

**Model:** `composer-2.5-fast`

**Interface (lock):**

```python
class DocumentRunStage(StrEnum):
    PREPARE = "prepare"
    RUN = "run"
    ASSEMBLE = "assemble"
    EVAL = "eval"
    EXPORT = "export"
    ISSUE_REVIEW_TASKS = "issue_review_tasks"

class DocumentRunnerSpec(SchemaModel):
    runner_id: str  # registry key: olmocr | kraken
    runner_reference_path: str  # JSON RunnerReference
    policy_path: str  # JSON RunnerExecutionPolicy
    # prepared_inputs_path optional: if omitted, orchestrator builds from prepare outputs

class DocumentRunConfig(SchemaModel):
    run_id: str
    document_id: str
    bundle_root: str  # relative or absolute; orchestrator resolves
    source_path: str
    recipe_paths: list[str] = Field(min_length=1)
    source_json: str
    bibliographic_json: str
    acquisition_json: str
    merge_policy_path: str
    runners: list[DocumentRunnerSpec] = Field(min_length=1)
    stages: list[DocumentRunStage] | None = None  # None = default full machine path
    force_rerun: bool = False
    ensure_endpoints: bool = False
    gold_page_paths: dict[str, str] = Field(default_factory=dict)  # page_id -> gold JSON
    metric_profile_path: str | None = None
    skip_export: bool = False
```

Default stages when `stages is None`:

- Without gold: `prepare → run → assemble → issue_review_tasks → export`
- With gold (`gold_page_paths` non-empty **and** `metric_profile_path` set):  
  `prepare → run → assemble → eval → issue_review_tasks → export`

- [ ] Failing validation tests (empty runners, empty recipes, unknown stage strings)
- [ ] Implement models
- [ ] GREEN + gates + commit

### Task 2: DocumentRunOrchestrator — prepare + run stages (TDD)

**Files:**
- Create: `wordwending/services/document_run.py`
- Modify: `tests/test_document_run.py`

**Model:** `cursor-grok-4.5-medium`

**Interface (lock):**

```python
@dataclass(frozen=True)
class DocumentRunResult:
    run_id: str
    document_id: str
    bundle_root: Path
    stages_completed: list[DocumentRunStage]
    document_bundle_path: Path | None
    export_root: Path | None
    pending_task_pages: list[str]

class DocumentRunOrchestrator:
    """Thin facade: sequence existing stage modules for one document run."""

    def __init__(
        self,
        *,
        preparation: PreparationBundleService,
        runner_registry: PassRunnerRegistry,
        manifest_builder: AssembleManifestBuilder,
        assemble: AssembleOrchestrator,
        bundles: BundleLayoutService,
        runner_service_factory: Callable[..., RunnerExecutionService],
        evaluation: EvaluationService | None = None,
        review_cli: ReviewCliService | None = None,
        endpoint_ensurer: Callable[..., None] | None = None,
    ) -> None: ...

    def run(self, config: DocumentRunConfig) -> DocumentRunResult:
        ...
```

`runner_service_factory(runner: PassRunner, bundle_root: Path, output_dir: Path, ...) -> RunnerExecutionService` mirrors CLI `_invoke_hosted_run` construction (one service instance per runner invocation).

**Prepare stage:** Call existing `PreparationBundleService.prepare_bundle` / `prepare_variants` with resolved paths (mirror CLI `prepare` logic for single-recipe default; multi-recipe → `prepare_variants`). `bundle_root` = prepare `output_dir`.

**Run stage:** For each `DocumentRunnerSpec`:

1. Load `RunnerReference` + `RunnerExecutionPolicy` from spec paths; assert `runner.runner_id == spec.runner_id`.
2. `runner_cls = runner_registry.resolve(spec.runner_id)` (**class**).
3. If `ensure_endpoints`, call `endpoint_ensurer` like CLI (settings URL overlay + token).
4. **Required in this task:** build `list[PreparedArtifactRef]` from `bundle_root/pages/**/preparation.json` (`PreparationResult` → full-page and/or `prepared_units` as `InputKind` artifacts with checksum/order/bbox when units). No operator-written prepared-inputs JSON.
5. `execution_run_id = f"{config.run_id}-{spec.runner_id}"`.
6. `output_dir = bundle_root / "runs" / execution_run_id`.
7. `service = runner_service_factory(runner_cls=..., runner=..., policy=..., endpoint_url=..., token=..., ...)` then `service.run(execution_run_id, config.document_id, artifacts, bundle_root, output_dir, force=config.force_rerun)`.

Note: resume ledger is per-`bundle_root` keyed by `batch_id`; distinct `execution_run_id` values must keep batch ids unique (existing runner behavior). Do not share one `run_id` across runners.

Unit tests: inject fake preparation/runner collaborators; assert call order and output dirs.

- [ ] Failing tests for prepare+run sequencing + prepared-inputs derivation
- [ ] Implement (includes prepared-inputs helper — Task 5 becomes no-op if done here)
- [ ] GREEN + gates + commit

### Task 3: Assemble + issue_review_tasks + export stages (TDD)

**Files:**
- Modify: `wordwending/services/document_run.py`
- Modify: `wordwending/services/assemble.py` — optional `document_id: str | None = None` on `assemble_document` (lock A)
- Modify: `tests/test_document_run.py`, `tests/test_assemble.py` as needed
- Fixtures under `tests/fixtures/document_run/` as needed

**Model:** `cursor-grok-4.5-medium`

**Assemble:** Load provenance + merge policy JSON from config paths. Call `AssembleManifestBuilder.build(bundle_root=..., run_dirs=[...all run output dirs...], ...)` where each run_dir is `bundle_root / "runs" / f"{config.run_id}-{runner_id}"`. Then `AssembleOrchestrator.assemble_document(..., document_id=config.document_id)` (lock A).

**eval (optional, before issue) — lock write-back:**

1. For each `page_id` in `gold_page_paths`, load gold JSON + `MetricProfile`.
2. `summary = EvaluationService.evaluate_page(page, gold, profile)`.
3. **Write back** onto the accepted page: `page.model_copy(update={"evaluation_summary": summary})` then `BundleLayoutService.write_page_graph` (public API from hands-off) and update `document-bundle.json` page entry so flags persist.
4. Escape hatch only if write_page_graph missing (should exist): also write `bundle_root / "evaluation" / f"{page_id}.json"` — but **issue reads page graph flags**, so write-back is mandatory for eval flags to affect `pending_tasks.json`.

**issue_review_tasks:** For each page in written bundle, call **`ReviewCliService.issue(bundle_root, page_id, run_id=config.run_id)`** so `pending_tasks.json` regenerates from current evaluation flags (merge + eval).

**export:** Load `document-bundle.json`, call `BundleLayoutService.write_document_exports(bundle, bundle_root)`.

**Assemble document_id:** Pass `config.document_id` into assemble (Task 3 includes AssembleOrchestrator kwarg if choosing lock A).

- [ ] Failing tests: full machine path with stubbed collaborators; skip eval when no gold; multi-runner passes two run_dirs into manifest builder
- [ ] Implement
- [ ] GREEN + gates + commit

### Task 4: CLI `document-run` (TDD)

**Files:**
- Modify: `wordwending/cli/cli.py`
- Modify: `tests/test_cli_commands.py`

**Model:** `composer-2.5-fast`

```text
wordwending document-run --config PATH
wordwending document-run --config PATH --force   # sets force_rerun
```

Thin: load `DocumentRunConfig`, construct real collaborators (same wiring style as other commands), call `orchestrator.run`, echo `DocumentRunResult` summary (stages, bundle path, export path, pending task page count).

- [ ] Failing CLI test with fixture config + monkeypatched orchestrator **or** tiny offline fixture (prefer mock orchestrator for CLI unit test + one deeper test in Task 3)
- [ ] Implement
- [ ] GREEN + gates + commit

### Task 5: Prepared-inputs builder — only if Task 2 deferred it

**Files:** `wordwending/services/prepared_inputs.py` (optional extract) + tests

**Model:** `composer-2.5-fast`

If Task 2 already ships derivation from `PreparationResult` → `list[PreparedArtifactRef]`, mark this task complete with no code. Otherwise extract helper and add focused tests (full-page vs prepared-unit kinds, checksum/order/bbox requirements).

### Task 6: Docs + AGENTS.md

**Files:**
- Modify: `doc/source/runbook/from_source_to_markdown.rst`
- Modify: `README.md`
- Modify: `AGENTS.md`

**Model:** `composer-2.5-fast`

- [ ] Document `document-run` as preferred machine-path entry; staged commands remain valid
- [ ] Remove “Full DocumentRunOrchestrator” from “What Is Missing”
- [ ] Note: human `review apply` / `rebase` still manual after issue
- [ ] Keep Phase 5/10 NOT COMPLETE
- [ ] AGENTS.md: cite `DocumentRunOrchestrator` as the document-run facade (not ExtractionOrchestrator fiction)
- [ ] Commit

### Task 7: Exit checklist

**Model:** `cursor-grok-4.5-medium` (reviewer)

- [ ] `pytest tests/test_document_run.py tests/test_cli_commands.py -k document_run -q` green
- [ ] `wordwending --help` shows `document-run`
- [ ] Runbook no longer lists DocumentRunOrchestrator as missing
- [ ] Human gate summary: what auto path covers vs review-events still manual

---

## Out of scope (next plans, not this one)

1. Coordinate-rich kraken geometry / Phase 7 alignment service split  
2. Phase 5 live bake-off evidence + cost/license scoring  
3. Phase 10 beyond ops skeleton  
4. God-module splits (`preparation.py` / `merge.py` / `models/ocr.py`)  
5. Auto-generating review **events**

## Execution Handoff

**Plan saved to:** `docs/superpowers/plans/2026-08-07-document-run-orchestrator.md`

**Recommended:** Subagent-Driven Development (`composer-2.5-fast` / `cursor-grok-4.5-medium` only).

1. Subagent-Driven (recommended)  
2. Inline Execution  

**Which approach?**
