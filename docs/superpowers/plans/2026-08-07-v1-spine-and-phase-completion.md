# V1 Spine and Spec 0004 Phase Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the witness-production assemble spine so operators can go from prepared pages + raw witnesses → merge → document bundle → eval/export without hand-edited JSON; then finish incomplete Spec 0004 phases in **ADR-legal order**, with honest exit claims (no Fake-as-second-adapter, no invented raw schemas, no false Phase 5/10 COMPLETE).

**Architecture:** Thin `AssembleOrchestrator` (Spec 0001’s assemble slice of `DocumentRunOrchestrator`) sequences adapt → abstaining merge → `BundleLayoutService.write_document_bundle`. Adapter parses **real** persisted olmOCR chat-completion witness bytes (ADR 0004 raw layer). Alignment/graph-build either reuse merge’s existing alignment or get an explicit waive-in-writing. Pass-runner Protocol + registry land **only after** two real hosted adapters (ADR 0007 / Spec 0013). Fake runners are **test doubles only** — they do not close Phase 4 “coordinate-rich,” Phase 5, or Phase 6.

**Tech Stack:** Python 3.13, Click, Pydantic 2, pytest, existing `wordwending.services.*` / `wordwending.models.*`, Hugging Face hosted endpoints (live optional behind `pytest.mark.integration`).

## ADR Alignment (locked — do not silently invert)

| ADR | Plan obligation |
| --- | --- |
| 0001 | Stay OCR orchestration; no TEI/dict/grammar |
| 0002 | Assemble writes document + page bundles |
| 0003 | Page graph = region/line/span/note in shared coords; Wave A text-only geometry is **provisional**; Phase 7 alignment exit owns real multi-pass align |
| 0004 | Raw witness layer = **exact** runner bytes unchanged; adapter reads them; no invented `olmocr-raw-witness/v1` schema |
| 0005 | Eval on assembled predictions; bake-off is architecture, not afterthought |
| 0006 | Common pass-runner interface — extracted after real adapters prove boundary |
| **0007** | Bake-off / real candidates **before** Protocol extract; Fake ≠ real adapter; no speculative plugin framework first |
| 0008 | Stable object IDs across rebuilds; append-only review history; dimension-qualified trust |
| 0009 | Spike rejected eScriptorium; custom review CLI is the chosen human boundary (state explicitly) |
| 0010 | Layer-1 evidence only; domain transforms out of scope |

## Locked Decisions

| Topic | Decision |
| --- | --- |
| Right next step | **Wave A** = deferred `B*` assemble spine (Phase 4 **exit sentence**). Full Phase 4 bullets need Wave C (2nd real runner path) + Wave D (review). |
| FakePassRunner | **Test double only.** Never counts toward Phase 4 coordinate-rich, Phase 5 bake-off, or Phase 6 exit. |
| Phase 6 Protocol | Extract **after** olmOCR + one other **real** hosted candidate adapter (provisional kraken HF per ADR 0007). Spec 0013 prior plan stands. |
| Phase order | Restore Spec 0004/ADR 0007 spirit: spine → review path → bake-off harness targeting real candidates → Protocol extract → ops skeleton. Do **not** gate bake-off on Fake Protocol. |
| Phase 5/10 COMPLETE | **Forbidden** under Wave F/H current scope. Ship harness/resume with documented **deferred** Spec exits. |
| Spec 0001 align/graph | **Waive separate modules for Wave A:** document that `AbstainingMergeService` currently owns scaffold/align/merge. Add Task B1 ADR-level note. Revisit if bake-off forces split. |
| Orchestrator name | Call it `AssembleOrchestrator` in code (assemble-only). Spec 0001 full `DocumentRunOrchestrator` (prepare→run→…→export) remains future; do not oversell. |
| Paths in models | Relative **posix `str`** paths (like `RunnerOutputArtifact.artifact_path`), never `list[Path]` on SchemaModel. |
| Raw fixture | Recorded OpenAI `chat.completion` JSON identical in shape to `tests/test_olmocr_runner.py::olmocr_response`. |
| Stable IDs | Lock deterministic ID derivation in adapt (ADR 0008) before eval gold matching. |
| Review CLI | Explicit ADR 0009 follow-up: custom CLI replaces eScriptorium as human boundary. |
| Models for subagents | **Only** `composer-2.5-fast` (mechanical) and `cursor-grok-4.5-medium` (integration / stuck / review). |

**Phase order note for agents:** Spec 0004 numbers run 5→6→7→8; this plan intentionally does Waves C/D (merge/review operator path) before F/G (bake-off/Protocol). That is **not** an ADR 0007 invert — bake-off still precedes Protocol extract. Follow **wave letters**, not Spec phase numbers.

## Subagent Model Policy

| Role | Model slug |
| --- | --- |
| Mechanical TDD (1–2 files, clear steps) | `composer-2.5-fast` |
| Multi-file integration, debugging, stuck | `cursor-grok-4.5-medium` |
| Spec-compliance / ADR reviewer | `cursor-grok-4.5-medium` |
| Code-quality reviewer | `composer-2.5-fast` |
| Final wave review | `cursor-grok-4.5-medium` |

Per task (serial Superpowers loop):

1. Implementer implements, runs listed checks, self-reviews, commits.
2. Spec/ADR-compliance reviewer (`cursor-grok-4.5-medium`) reviews without editing.
3. Same implementer fixes; re-review until approved.
4. Fresh code-quality reviewer (`composer-2.5-fast`) reviews without editing.
5. Same fix/re-review loop for quality findings.

After each **Wave**, fresh `cursor-grok-4.5-medium` audits against ADRs above + Spec 0004 exit text. Do not start the next wave with open findings.

Include in every subagent prompt:

- Workspace: `/Users/cmalek/src/workspace/wordwending`
- Before explore: `graphify query/path/explain`; use `user-code-index`
- Python: `source .venv/bin/activate`; `/usr/bin/cd` only
- After Python: `.venv/bin/ruff`, `.venv/bin/mypy` on touched files, `make napoleon-gate`, focused pytest
- After code edits: `graphify update .`
- Never invent `ExtractionOrchestrator` / `DdlExtractor`
- Never invent a second raw-witness schema; parse real runner bytes
- Never count FakePassRunner toward Phase 4/5/6 exits

## Global Constraints

- Before Python: `/usr/bin/cd` into repo; `source .venv/bin/activate`; use `.venv` tools.
- Bare `cd` is a broken bash function — always `/usr/bin/cd`.
- Do **not** extract `PassRunner` Protocol / registry until two real hosted adapters exist (ADR 0007).
- Do not add local OCR-model inference (ADR 0007).
- Dictionary/grammar/TEI transforms stay out of scope (ADR 0010).
- Prefer constructor injection; keep CLI thin; business logic in `wordwending.services`.
- Settings only via `wordwending/settings.py`.
- TDD: failing test → implement → pass → quality gate → commit.
- Preserve Napoleon `#:` / docstring contract on all non-test Python.
- Prefer botocraft for AWS; stop and ask if missing (unlikely here).

## Spec 0004 Completion Matrix (honest)

| Phase | Wave | Done means (honest) |
| --- | --- | --- |
| 1 | — | Closed (spike reject). No work. |
| 2 | — | DONE. No work unless Wave A exposes scoring gaps. |
| 3 | — | DONE. |
| 4 exit sentence | **A** | Fixture: adapt(real chat.completion)→merge→bundle→eval→export; no hand JSON. |
| 4 full bullets | **A+C+D** | Second **real** runner on assemble (C); review tasks + overlay (D). |
| 5 | **F** | Harness + matrix artifact targeting real candidates. **FORBIDDEN to mark COMPLETE** under Wave F alone — see Wave F exit. |
| 6 | **G** | Protocol + registry extracted from olmOCR + 2nd real adapter. Fake = tests only. |
| 7 | **B note + C** | Multi-witness merge on spine; alignment remains inside merge unless bake-off forces split. |
| 8 | **D** | Review CLI; ADR 0009 follow-up written. |
| 9 | **A+E** | Assemble writes bundle; inspect; export from assembled tree. |
| 10 | **H** | Resume ledger + checksum on inspect. **Do not mark Spec Phase 10 COMPLETE** (HF ops/deploy deferred). |

---

## File Map

| File | Role |
| --- | --- |
| `wordwending/services/witness_adaptation.py` | **New** — parse real raw witnesses → `PassWitnessPage` |
| `wordwending/services/assemble.py` | **New** — `AssembleOrchestrator` |
| `wordwending/models/assemble.py` | **New** — manifest + request models (relative `str` paths) |
| `wordwending/services/bundle_layout.py` | Called by assemble |
| `wordwending/services/merge.py` | Called by assemble (no reimplementation) |
| `wordwending/services/olmocr_runner.py` | Unchanged shape; Wave G conforms to Protocol later |
| `wordwending/services/kraken_runner.py` | **New in Wave C/G** — provisional HF kraken (or other ADR 0007 candidate) adapter |
| `wordwending/services/pass_runner.py` | **New in Wave G only** — Protocol extracted from reality |
| `wordwending/services/pass_runner_registry.py` | **New in Wave G only** |
| `wordwending/services/fake_pass_runner.py` | **New when needed for tests** — test double; never Phase exit |
| `wordwending/services/runner_execution.py` | Retype to Protocol in Wave G |
| `wordwending/services/review_overlay.py` | Wave D CLI |
| `wordwending/services/review_markup.py` | Wave D tasks |
| `wordwending/services/bakeoff.py` | Wave F harness |
| `wordwending/cli/cli.py` | `assemble`, `inspect-bundle`, `review`; later `bakeoff` |
| `AGENTS.md` | Fix fictional orchestrator; name `AssembleOrchestrator` |
| `doc/source/architecture/` or runbook | ADR 0009 follow-up note; Spec 0001 waive note |
| `doc/source/runbook/from_source_to_markdown.rst` | Honest assemble path |
| `README.md` | Honest CLI list |
| `tests/fixtures/assemble/` | Real chat.completion witness fixtures + manifests |
| `tests/test_witness_adaptation.py` | **New** |
| `tests/test_assemble.py` | **New** |
| `tests/test_cli_commands.py` | Extended |

**Out of scope until optional later plan:** splitting `preparation.py` / `merge.py` / `models/ocr.py` (former Wave G deepening).

---

# Wave A — Assemble spine (`B*`) / Phase 4 exit sentence

**Exit:** One representative page: real raw witness → adapt → merge → `write_document_bundle` → `eval` → `export` without hand-edited `DocumentBundle` JSON. CLI: `assemble`, `inspect-bundle`.

**Does not claim:** Phase 4 COMPLETE, coordinate-rich second runner, Protocol, bake-off.

### Task A1: Fix stale AGENTS.md orchestrator fiction

**Files:** Modify `AGENTS.md`  
**Model:** `composer-2.5-fast`

- [ ] **Step 1:** Replace `ExtractionOrchestrator` / `orchestrator.py` / `DdlExtractor` / `RunStats` with:
  - `RunnerExecutionOrchestrator` — `wordwending/services/runner_execution.py`
  - `MergeOrchestrator` — `wordwending/services/merge.py`
  - Note: `AssembleOrchestrator` lands in Task A3
- [ ] **Step 2: Commit**

### Task A2: Witness adapter parses real olmOCR chat.completion (TDD)

**Files:**
- Create: `wordwending/services/witness_adaptation.py`
- Create: `tests/test_witness_adaptation.py`
- Create: `tests/fixtures/assemble/olmocr-chat-completion-v1.json`

**Model:** `cursor-grok-4.5-medium`

**Raw fixture (lock — ADR 0004):** identical shape to `olmocr_response()` in `tests/test_olmocr_runner.py`:

```json
{
  "id": "chatcmpl-assemble-fixture",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Line one of diplomatic text.\nLine two of diplomatic text."
      },
      "finish_reason": "stop"
    }
  ]
}
```

This is what `HuggingFaceOlmocrRunner` persists via `witness_path.write_bytes(response.content)`. **Do not** invent a parallel schema. Adapter extracts assistant `content` text from that JSON.

**Provisional graph (ADR 0003 honesty):** Wave A builds conservative full-page region + one line/span per newline. Label as provisional text-only geometry in docstrings. Not a claim of coordinate-rich OCR.

**Stable IDs (ADR 0008 lock):**

```text
region_id = f"{prepared_page_id}:r0"
line_id   = f"{prepared_page_id}:l{line_index}"
span_id   = f"{prepared_page_id}:s{line_index}"
```

Same inputs → same IDs across rebuilds when text lines unchanged.

**Interface (lock):**

```python
class WitnessAdaptationService:
    """Convert persisted raw witness artifacts into merge-ready page fragments."""

    def adapt_page(
        self,
        *,
        prepared_page: PreparedPage,
        witness_id: str,
        runner_id: str,
        artifact_paths: list[str],  # relative or absolute strings; resolve vs bundle_root at call site
        coordinate_space: CoordinateSpace,
    ) -> PassWitnessPage:
        ...
```

- [ ] **Step 1: Failing tests** — adapt fixture → non-empty region/line/span; two lines; stable IDs; reject empty paths; reject non-chat.completion JSON
- [ ] **Step 2: RED**
- [ ] **Step 3: Implement** `WitnessAdaptationService` + `OlmocrChatCompletionAdapter`
- [ ] **Step 4: GREEN + gates + `graphify update .`**
- [ ] **Step 5: Commit**

### Task A3: Assemble models + AssembleOrchestrator (library, TDD)

**Files:**
- Create: `wordwending/models/assemble.py`
- Create: `wordwending/services/assemble.py`
- Create: `tests/test_assemble.py`

**Model:** `cursor-grok-4.5-medium`

**Adapt contract (lock):**

- Orchestrator owns adapt. CLI never calls adapter directly.
- Requests carry raw witness refs (paths as **relative posix `str`**), not pre-built `PassWitnessPage`.

```python
class RawWitnessRef(SchemaModel):
    witness_id: str
    runner_id: str
    artifact_paths: list[str] = Field(min_length=1)  # posix-relative to bundle_root or manifest base
    coordinate_space: CoordinateSpace

class AssemblePageRequest(SchemaModel):
    page_id: str
    page_number: int
    prepared_page: PreparedPage
    raw_witnesses: list[RawWitnessRef] = Field(min_length=1)

class AssembleOrchestrator:
    """Sequence adapt → merge → document-bundle write for one assemble pass."""

    def __init__(
        self,
        *,
        adapter: WitnessAdaptationService,
        merge: AbstainingMergeService,
        bundles: BundleLayoutService,
    ) -> None: ...

    def assemble_document(
        self,
        *,
        bundle_root: Path,
        source: SourceDescriptor,
        bibliographic: BibliographicProvenance,
        acquisition: AcquisitionProvenance,
        pages: list[AssemblePageRequest],
        merge_policy: MergePolicy,
    ) -> DocumentBundle:
        ...
```

Behavior: adapt each ref → `merge_page` → build `DocumentBundle`/`BundlePage` → `write_document_bundle` → return bundle.

Single-witness required for Wave A. Multi-witness = Wave C.

- [ ] **Step 1–5:** TDD, gates, commit

### Task A4: CLI `assemble` + `inspect-bundle` + run→manifest binding note

**Files:**
- Modify: `wordwending/cli/cli.py`
- Modify: `tests/test_cli_commands.py`
- Create: `tests/fixtures/assemble/manifest-v1.json` (relative paths)
- Update: runbook + README

**Model:** `composer-2.5-fast` (escalate to Grok if stuck)

```text
wordwending assemble --bundle-root DIR --manifest PATH
wordwending inspect-bundle --bundle-root DIR
```

`AssembleManifest` in `models/assemble.py`: explicit page list + relative witness paths. Prefer paths under `bundle_root` matching what `run` already writes (`witnesses/...`). Document in runbook: after `run`, point manifest at those relative artifact paths (no scanning magic in Wave A).

- [ ] CLI tests + smoke: assemble → export → `exports/document.md`
- [ ] Runbook: remove “assemble deferred”; note review CLI still Wave D
- [ ] Commit

### Task A5: Wave A exit checklist

**Model:** `cursor-grok-4.5-medium` (reviewer)

- [ ] pytest adapt/assemble/cli assemble path green
- [ ] Fixture path: assemble → prediction from page dir (`page_id` aligned) → `eval` vs assemble-scoped gold pair under `tests/fixtures/assemble/` (copy/adapt from `tests/fixtures/evaluation/` with matching ids) → `export`
- [ ] Docs do **not** say “Phase 4 COMPLETE”
- [ ] Human gate

---

# Wave B — Spec 0001 / ADR notes + assemble hardening

**Exit:** Written decisions; ID/eval pairing solid; no new Protocol.

### Task B1: Spec 0001 waive + ADR 0009 follow-up (docs)

**Files:** short RST under `doc/source/architecture/` or runbook section  
**Model:** `composer-2.5-fast`

- [ ] **Waive (temporary):** separate `PageAlignmentService` / `PageGraphBuilder` — merge module currently owns scaffold/align/merge; revisit after bake-off if locality fails.
- [ ] **ADR 0009 follow-up:** spike rejected eScriptorium; **custom `wordwending review` CLI** is the chosen human correction boundary for v1; PAGE interchange remains optional import/export via `PageXmlInterchangeService`, not the review UI.
- [ ] Commit

### Task B2: Harden stable IDs + gold pairing for assemble eval

**Model:** `cursor-grok-4.5-medium`

- [ ] Tests that rebuild adapt twice → identical object ids (ADR 0008)
- [ ] Assemble-scoped gold/`BundlePage` ids documented in fixture README
- [ ] Commit + human gate

---

# Wave C — Second real runner path + Phase 7 multi-witness on spine

**Exit:** Provisional **real** second hosted adapter (prefer kraken HF per ADR 0007) can produce raw witnesses; assemble consumes ≥1 olmOCR + optional second witness; multi-witness disagreement flags persist and are inspectable.

**Does not claim:** Phase 6 Protocol complete; Phase 5 bake-off complete.

### Task C1: Provisional second hosted adapter (real, not Fake)

**Files:** `wordwending/services/kraken_runner.py` (or chosen ADR 0007 candidate), tests with mocked httpx like olmOCR  
**Model:** `cursor-grok-4.5-medium`

- [ ] Same packaging/execution call shape the spine already uses (`invoke(batch, packaged, output_dir) -> HostedInvocationResult` until Wave G renames)
- [ ] Persists **exact** response bytes as raw witnesses (ADR 0004)
- [ ] CLI `run --runner kraken` (or id) can select it without a Protocol/registry yet (simple if/else or factory dict is OK — not a plugin framework)

### Task C2: Adapter strategy for second runner’s raw bytes → PassWitnessPage

**Model:** `cursor-grok-4.5-medium`

- [ ] Extend `WitnessAdaptationService` with a second strategy keyed by `runner_id`
- [ ] Conservative geometry OK if engine is text-first; if coordinate-rich fields exist in raw output, map them (ADR 0003)

### Task C3: Multi-witness assemble fixture + flag persistence

**Model:** `composer-2.5-fast` / Grok for bundle persistence

- [ ] Two witnesses, intentional text disagreement → merge flags non-empty
- [ ] Flags inspectable via `inspect-bundle` or page sidecar — use existing merge result fields (Spec 0009); no second flag schema
- [ ] Human gate

---

# Wave D — Phase 8 Review CLI (ADR 0008 + 0009)

**Exit:** Operator applies overlay + materializes without REPL; merge flags can become review tasks where Spec 0005 models exist.

### Task D1: `wordwending review` CLI

**Model:** `composer-2.5-fast`

```text
wordwending review apply --bundle-root DIR --overlay PATH --page-id ID
wordwending review materialize --bundle-root DIR --page-id ID
```

Wire `ReviewOverlayService` / `HumanMarkupService` / `BundleLayoutService.write_overlay_state`.

- [ ] Append-only overlay history preserved (ADR 0008) — do not collapse to mutable blob
- [ ] Stop and ask if Spec 0005/0014 models missing a required field

### Task D2: Merge flags → review task packets

**Model:** `cursor-grok-4.5-medium`

- [ ] Map existing flag types to Spec 0005 tasks where models exist
- [ ] No shadow schema

### Task D3: Docs — Phase 4 full bullets status + human gate

- [ ] After D: may say Phase 4 bullets met **if** Wave C second real runner is on assemble path; else say remaining gap explicitly

---

# Wave E — Phase 9 Export polish

**Exit:** Assembled bundles export Spec 0016 artifacts; `inspect-bundle` lists export paths; RAG line regressions green.

### Task E1–E3

**Model:** `composer-2.5-fast`

- [ ] Assemble → export integration test
- [ ] Runbook/README honesty pass
- [ ] Human gate

---

# Wave F — Phase 5 Bake-Off Harness (do NOT mark COMPLETE)

**Exit:** Reproducible harness writes `bakeoff-matrix-v1.json` comparing runners on held-out fixtures using `EvaluationService` metrics + latency/failure fields. Default tests use recorded/mocked hosted responses. Live HF behind `pytest.mark.integration`.

**Forbidden:** Marking Spec 0004 Phase 5 COMPLETE until matrix includes olmOCR + ≥1 other **real** candidate evidence (live or recorded from real endpoint shapes). Document deferred: cost/license/operability scoring, full corpus held-out slices.

### Task F1: `BakeoffService` + models + optional CLI

**Model:** `cursor-grok-4.5-medium`

- [ ] Fake allowed **only** inside unit tests of harness plumbing
- [ ] Matrix schema includes runner_id, page_class, score families, latency, failure, license placeholder fields
- [ ] Commit + human gate with explicit “Phase 5 NOT COMPLETE” note in runbook

---

# Wave G — Phase 6 Runner Boundary (ADR 0007 / Spec 0013)

**Exit:** `PassRunner` Protocol extracted from **olmOCR + second real adapter** call sites; registry resolves by id; execution spine typed to Protocol.

**Prerequisite:** Wave C second real adapter exists.

### Task G1: Extract Protocol from reality

**Model:** `composer-2.5-fast`

Match call site exactly:

```python
invocation = self._runner.invoke(planned, packaged, self._output_dir)
# -> HostedInvocationResult (rename to RunnerInvocationResult only if both adapters + spine updated together)
```

- [ ] Both real adapters satisfy Protocol
- [ ] Fake may also satisfy for tests — still not a Phase exit by itself

### Task G2: Registry + retype spine; collapse shallow facade if pass-through

**Model:** `cursor-grok-4.5-medium`

- [x] `PassRunnerRegistry`
- [x] Replace concrete type annotations
- [x] Human gate — **now** Phase 6 may be marked COMPLETE

---

# Wave H — Phase 10 Minimal Hardening (do NOT mark Spec COMPLETE)

**Exit:** Resume ledger for completed batches on `run`; checksum/corruption verification on `inspect-bundle`.

**Forbidden:** Marking Spec 0004 Phase 10 COMPLETE. Document deferred: HF deploy/ops, quotas, cost controls, corpus regression gates, operator calibration monitoring.

### Task H1–H3

**Model:** `cursor-grok-4.5-medium` / `composer-2.5-fast`

- [ ] Resume ledger under bundle_root; `--force` to bypass
- [ ] Inspect verifies checksums where bundle layout already records them
- [ ] Runbook: “ops skeleton only; Phase 10 Spec exit deferred”
- [ ] Final whole-program ADR review (`cursor-grok-4.5-medium`)

---

# Optional later plan (NOT this plan)

God-module splits: `preparation.py`, `MergeOrchestrator` internals, `models/ocr.py` re-exports. Unlock only after Waves A–H green and human asks.

---

## Execution Handoff

**Plan saved to:** `docs/superpowers/plans/2026-08-07-v1-spine-and-phase-completion.md`

**Recommended:** Subagent-Driven Development, **Wave A only** first.

1. Subagent-Driven (recommended) — models: `composer-2.5-fast` / `cursor-grok-4.5-medium` only  
2. Inline Execution — this session with checkpoints  

**Which approach?**
