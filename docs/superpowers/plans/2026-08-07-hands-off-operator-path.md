# Hands-Off Operator Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the three remaining operator-surgery gaps so `prepare → run → assemble → review → export` works without hand-written `AssembleManifest`, hand-authored `ReviewTask` packets, or export ignoring accepted overlays.

**Architecture:** Add three deep modules at existing seams: (1) `AssembleManifestBuilder` scans prepare/run trees into `AssembleManifest`; (2) persist Spec 0005 tasks already buildable via `MergeFlagReviewService.build_review_tasks` / `HumanMarkupService.build_review_tasks`; (3) `GraphRebaseService` applies materialized `OverlayState` overrides onto the accepted `BundlePage` graph (new revision) so `export` sees corrections. CLI stays thin. No Protocol invent, no Fake-as-adapter, no Phase 5/10 COMPLETE claims.

**Tech Stack:** Python 3.13, Click, Pydantic 2, pytest, existing assemble / review_cli / merge_review / bundle_layout / HumanMarkupService.

## Locked Decisions

| Topic | Decision |
| --- | --- |
| Scope | Exactly three gaps: auto-manifest, auto ReviewTasks, overlay→graph rebase→export. No DocumentRunOrchestrator, no god-module splits, no Phase 5 live bake-off. |
| Auto-manifest | New library `AssembleManifestBuilder.build(...)` + CLI `assemble --from-run` (keep `--manifest` path). Prefer scanning persisted batch JSON + preparation.json over inventing a third layout. |
| Multi-run | `--from-run` accepts **one or more** `--run-dir` values (repeatable) so olmOCR + kraken witness trees merge into one manifest. |
| Provenance | `--from-run` requires explicit `--source-json` / `--bibliographic-json` / `--acquisition-json` / `--merge-policy` paths. **No** `--provenance-dir` shortcut in v1. Do not invent bibliographic metadata. |
| ReviewTasks | Library already builds packets. Persist under page tree as `overlays/pending_tasks.json` via new `BundlePaths` helper. Wire into assemble when merge flags exist; add `review issue` CLI for regenerate-from-flags. |
| Graph revision | **Add** `BundlePage.graph_revision: str` (default `"graph-v0"`). Assemble writes initial revision; rebase bumps it. ReviewTask / overlay `base_graph_revision` bind to this field (ADR 0008). |
| Rebase scope (v1) | Apply leaf overrides: text, typography, roles, geometry box/polygon, region_kind, note link ids. `illegible=True` → set target node `review` / trust fields only if `ReviewSummary` already supports it; else record via existing review summary flags — **do not** invent a new graph field. Structural split/merge/reorder remain audit/trust-only. |
| Rebase + overlays | After graph rewrite, call `ReviewOverlayService.create_successor` (or CLI-equivalent) so overlay tasks/events rebind to the new `base_graph_revision` (ADR 0008). Do not leave old overlay base pointing at dead revision. |
| Export | No export API change if rebase rewrites `page_graph.json` + `document-bundle.json` before export. |
| Run layout | Prepare `output_dir` is usually assemble `bundle_root`. `run --output-dir` may be a sibling. Builder **copies** witness files into `bundle_root` under a stable relative prefix (`runs/<run_id>/…` or existing page witness paths) and records those relative paths in the manifest. Do not require `run_dir ⊆ bundle_root`. |
| ADR | 0004 raw unchanged; 0008 append-only events stay + successor overlay on revision change; 0002 page bundle remains truth. |

## Subagent Model Policy

| Role | Model |
| --- | --- |
| Mechanical TDD | `composer-2.5-fast` |
| Integration / stuck / ADR review | `cursor-grok-4.5-medium` |
| Code-quality review | `composer-2.5-fast` |

Per task: implement → spec/ADR review → fix → quality review → fix → commit.

Every subagent prompt must include: workspace `/Users/cmalek/src/workspace/wordwending`; `source .venv/bin/activate`; `/usr/bin/cd`; graphify before explore; ruff/mypy/napoleon-gate/focused pytest; `graphify update .` after code edits.

## Global Constraints

- Activate `.venv` before Python work; `/usr/bin/cd` only.
- Relative posix `str` paths in SchemaModels (never `list[Path]`).
- TDD; Napoleon `#:` / docstrings on non-test Python.
- Do not mark Spec 0004 Phase 5/10 COMPLETE.
- Prefer wiring existing services over reimplementation.

## File Map

| File | Role |
| --- | --- |
| `wordwending/services/assemble_manifest.py` | **New** — `AssembleManifestBuilder` |
| `wordwending/models/ocr.py` | Add `BundlePage.graph_revision` |
| `wordwending/models/bundle_layout.py` | `BundlePaths` helper for `overlays/pending_tasks.json` |
| `wordwending/cli/cli.py` | `assemble --from-run` / repeatable `--run-dir` |
| `wordwending/services/assemble.py` | Set initial `graph_revision`; persist pending ReviewTasks |
| `wordwending/services/bundle_layout.py` | `write_pending_review_tasks` / `read_pending_review_tasks` / public `write_page_graph` |
| `wordwending/services/graph_rebase.py` | **New** — `GraphRebaseService` |
| `wordwending/services/review_cli.py` | `issue_tasks`, `rebase_graph` |
| `wordwending/cli/review.py` | `review issue`, `review rebase` |
| `doc/source/runbook/from_source_to_markdown.rst` | Remove “auto manifest / ReviewTask / rebase deferred” claims |
| `README.md` | Honest CLI list |
| `tests/test_assemble_manifest.py` | **New** |
| `tests/test_graph_rebase.py` | **New** |
| `tests/test_review_cli.py` | Extend |
| `tests/test_assemble.py` / `tests/test_cli_commands.py` | Extend |
| `tests/fixtures/hands_off/` | **New** prepare+run tree fixtures |

---

### Task 1: `BundlePage.graph_revision` + AssembleManifestBuilder (TDD)

**Files:**
- Modify: `wordwending/models/ocr.py` (`BundlePage`)
- Modify: tests that construct `BundlePage` if defaults break (prefer field default so fixtures keep working)
- Create: `wordwending/services/assemble_manifest.py`
- Create: `tests/test_assemble_manifest.py`
- Create: `tests/fixtures/hands_off/` (minimal: `PreparationResult` JSON as `preparation.json`, `batches/*.json`, witness JSON, prepared image stubs)

**Model:** `cursor-grok-4.5-medium`

**BundlePage field (lock):**

```python
#: Accepted page-graph revision; binds review tasks/overlays (ADR 0008).
graph_revision: str = "graph-v0"
```

Assemble sets a concrete initial value (e.g. `graph-v0` or `assemble-<document_id>-v0`). Rebase bumps (e.g. `graph-v1`, or `…-vN`).

**Interface (lock):**

```python
class AssembleManifestBuilder:
    """Build AssembleManifest by scanning prepare/run artifacts; copy witnesses into bundle_root."""

    def build(
        self,
        *,
        bundle_root: Path,
        run_dirs: list[Path],
        source: SourceDescriptor,
        bibliographic: BibliographicProvenance,
        acquisition: AcquisitionProvenance,
        merge_policy: MergePolicy,
    ) -> AssembleManifest:
        ...
```

**Scan rules (lock):**

1. For each `run_dir`, load every `batches/*.json` as `RunnerExecutionBatch`.
2. For each succeeded/partial batch, for each `output_artifacts[]` entry, resolve bytes under that `run_dir`, **copy** into `bundle_root/runs/<run_id>/<artifact_path>` (or flatten to page witness paths if layout already defines one — pick one scheme in implementation and test it), record **bundle_root-relative** posix paths in `RawWitnessRef.artifact_paths`.
3. Map batch `items[]` (`item_id` → `source_page_id`) via `output_artifacts[].batch_item_ids`.
4. Load `pages/<source_page_id>/prepared/<prepared_page_id>/preparation.json` as **`PreparationResult`** (not bare `PreparedPage`); take `.prepared_page` / page_number from wrapped source page fields as present today.
5. Build `RawWitnessRef` per (page, runner_id).
6. `page_number` from preparation/`SourcePageArtifact` when present; else stable sort of `page_id`.
7. Fail clearly if a page has zero witnesses, missing preparation.json, or unresolvable artifact path.

- [ ] **Step 1: Write failing tests** covering single-run one page, two-run (olmOCR+kraken) same page, missing batch → error, missing prep → error
- [ ] **Step 2: RED** — `pytest tests/test_assemble_manifest.py -q`
- [ ] **Step 3: Implement builder**
- [ ] **Step 4: GREEN + ruff + mypy + napoleon-gate + `graphify update .`**
- [ ] **Step 5: Commit**

### Task 2: CLI `assemble --from-run` (TDD)

**Files:**
- Modify: `wordwending/cli/cli.py` (`assemble` command)
- Modify: `tests/test_cli_commands.py`

**Model:** `composer-2.5-fast`

**CLI (lock):**

```text
wordwending assemble --bundle-root DIR --manifest PATH
  # unchanged

wordwending assemble --bundle-root DIR \
  --from-run \
  --run-dir DIR [--run-dir DIR ...] \
  --source-json PATH \
  --bibliographic-json PATH \
  --acquisition-json PATH \
  --merge-policy PATH \
  [--write-manifest PATH]
```

Mutual exclusion: `--manifest` XOR `--from-run`. When `--from-run`, build manifest via Task 1 (copies witnesses into bundle_root), optionally write manifest JSON, then call existing `AssembleOrchestrator.assemble_document`.

- [ ] Failing CLI tests (from-run happy path + mutual exclusion)
- [ ] Implement thin Click wiring
- [ ] GREEN + gates + commit

### Task 3: Persist pending ReviewTasks on assemble (TDD)

**Files:**
- Modify: `wordwending/services/assemble.py` (`_AssembleExecution`)
- Modify: `wordwending/services/bundle_layout.py` (write/read helpers)
- Modify: `tests/test_assemble.py` / `tests/test_merge_review.py` as needed
- Read: `MergeFlagReviewService.build_review_tasks`, `HumanMarkupService.build_review_tasks`

**Model:** `cursor-grok-4.5-medium`

**Behavior (lock):**

1. After merge flags are projected onto the page (already done), if flags non-empty, call `build_review_tasks(page, flags, markup=HumanMarkupService(), run_id=..., graph_revision=...)`.
2. Persist tasks as JSON list at page overlay path: `overlays/pending_tasks.json` (relative under page dir — follow `BundlePaths` conventions; add helper if missing).
3. Empty flags → write empty list or skip file; choose one and test it (prefer write `[]` for inspectability).
4. `run_id`: deterministic assemble run id already used when building the document (or `assemble-<document_id>`).
5. Each task’s `base_graph_revision` **must equal** `BundlePage.graph_revision` for that page.
6. Add `BundlePaths.pending_tasks_path(...)` + `BundleLayoutService.write_pending_review_tasks` / `read_pending_review_tasks`.

- [ ] Failing test: multi-witness disagreement assemble → `pending_tasks.json` exists, non-empty, validates as `list[ReviewTask]`, each `base_graph_revision == page.graph_revision`
- [ ] Implement
- [ ] GREEN + gates + commit

### Task 4: CLI `review issue` (TDD)

**Files:**
- Modify: `wordwending/services/review_cli.py`
- Modify: `wordwending/cli/review.py`
- Modify: `tests/test_review_cli.py`

**Model:** `composer-2.5-fast`

```text
wordwending review issue --bundle-root DIR --page-id ID [--run-id ID]
```

Rebuilds pending tasks from the page’s current evaluation flags via `HumanMarkupService.build_review_tasks` (covers eval-only flags too, not just merge). Writes `overlays/pending_tasks.json`. Echo task count.

- [ ] Failing tests
- [ ] Implement
- [ ] GREEN + gates + commit

### Task 5: GraphRebaseService (TDD)

**Files:**
- Create: `wordwending/services/graph_rebase.py`
- Create: `tests/test_graph_rebase.py`

**Model:** `cursor-grok-4.5-medium`

**Interface (lock):**

```python
class GraphRebaseService:
    """Apply materialized OverlayState rows onto an accepted BundlePage graph."""

    def rebase_page(
        self,
        page: BundlePage,
        states: list[OverlayState],
        *,
        new_graph_revision: str,
    ) -> BundlePage:
        ...
```

**Apply rules (lock):**

| OverlayState field | Effect |
| --- | --- |
| `text_diplomatic_override` | Set matching span/note diplomatic text (by `object_id` + scope) |
| `typography_override` / `role_overrides` | Update span typography / roles |
| `bounding_box_override` / `polygon_override` | Update geometry on target |
| `region_kind_override` | Update region kind |
| `illegible` | Update target `ReviewSummary` / trust using **existing** node fields only; if insufficient, leave graph text alone and keep illegible on overlay state (document). Do not add `BundlePage.illegible`. |
| `linked_marker_span_ids` | Update note linkage |
| Structural-only trust fields | Do **not** invent split/merge graph surgery in v1 |

Unknown `object_id` → raise `ValueError` with id. Return new `BundlePage` with `graph_revision=new_graph_revision`.

- [ ] Failing tests: text correction; typography; missing object id; revision bump; page equality otherwise
- [ ] Implement
- [ ] GREEN + gates + commit

### Task 6: CLI `review rebase` + successor overlay + export sees corrections (TDD)

**Files:**
- Modify: `wordwending/services/review_cli.py`
- Modify: `wordwending/cli/review.py`
- Modify: `wordwending/services/bundle_layout.py` — public `write_page_graph` + document-bundle page rewrite
- Modify: `tests/test_review_cli.py`, integration test file
- Use: `ReviewOverlayService.create_successor` (existing)

**Model:** `cursor-grok-4.5-medium`

```text
wordwending review rebase --bundle-root DIR --page-id ID [--graph-revision STR]
```

Flow (ADR 0008 lock):

1. Materialize states from append-only events (do **not** rewrite JSONL history).
2. Read current page graph (`old_revision = page.graph_revision`).
3. `GraphRebaseService.rebase_page(..., new_graph_revision=...)`.
4. Write updated page graph + update `document-bundle.json` page entry.
5. **Successor overlay persistence (lock — no mid-task ask):** Do **not** rewrite `review_events.jsonl`. Write Spec 0014 successor `PageOverlay` JSON to `overlays/page_overlay.json` (or `overlays/successor_overlay.json` if current layout already uses a name — prefer `page_overlay.json` and document). Call `write_overlay_state` with successor materialized `current_state`. Keep append-only JSONL as historical truth for the predecessor base; successor overlay carries rebound `base_graph_revision`.
6. Regenerate `overlays/pending_tasks.json` against the new graph (open tasks rebound; drop tasks whose targets vanished — test the chosen rule).
7. Echo old → new revision.

Integration test:

1. Assemble fixture page with known span text + `graph_revision`.
2. `review apply` overlay correcting that span’s text (`base_graph_revision` matches).
3. `review rebase`.
4. Assert page graph text updated + `graph_revision` bumped + overlay base revision updated/successor present.
5. `export` → corrected text in Markdown / bundle export.

- [ ] Failing integration test first
- [ ] Implement CLI + layout writes + successor path
- [ ] GREEN + gates + commit

### Task 7: Runbook + README honesty

**Files:**
- Modify: `doc/source/runbook/from_source_to_markdown.rst`
- Modify: `README.md`

**Model:** `composer-2.5-fast`

- [ ] Document `assemble --from-run` as preferred path; `--manifest` remains escape hatch
- [ ] Document `review issue` / `review rebase` / export-after-rebase
- [ ] Remove “auto manifest deferred”, “ReviewTask not auto-emitted”, “graph rebase deferred” as open gaps (or move to “done”)
- [ ] Keep Phase 5/10 NOT COMPLETE language
- [ ] Commit

### Task 8: Hands-off exit checklist

**Model:** `cursor-grok-4.5-medium` (reviewer)

Operator path on fixtures (no hand-edited AssembleManifest, no hand-built ReviewTask list for flag-driven pages):

```bash
# conceptual — exact fixture paths from tests/fixtures/hands_off/
wordwending assemble --bundle-root ... --from-run --run-dir ... \
  --source-json ... --bibliographic-json ... --acquisition-json ... --merge-policy ...
wordwending review issue --bundle-root ... --page-id ...
# apply a minimal overlay that references an issued task id (overlay events still operator-authored — OK)
wordwending review apply ...
wordwending review rebase ...
wordwending export ...
```

**Still OK to require:** human-authored **review events** (corrections). Not OK to require: hand AssembleManifest, hand ReviewTask packet construction for merge flags, export ignoring rebase.

- [ ] Run focused pytest suite for new modules + CLI
- [ ] Confirm runbook matches
- [ ] Human gate summary

---

## Out of scope

- Full `DocumentRunOrchestrator` single command
- Coordinate-rich kraken geometry
- Auto-generating review **events** (AI correction) — humans still write corrections
- Phase 5 live bake-off / Phase 10 full ops
- Splitting `preparation.py` / `merge.py` / `models/ocr.py`

## Execution Handoff

**Plan saved to:** `docs/superpowers/plans/2026-08-07-hands-off-operator-path.md`

**Recommended:** Subagent-Driven Development with `composer-2.5-fast` / `cursor-grok-4.5-medium` only.

1. Subagent-Driven (recommended)
2. Inline Execution

**Which approach?**
