# Coordinate-Rich Kraken Adaptation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the kraken pass truly coordinate-rich on the assemble/merge spine: persist and adapt per-line geometry (bbox + baseline) into `PassWitnessPage`, so Spec 0004 Phase 4’s “coordinate-rich second runner” claim is honest and merge scaffold/IoU can prefer kraken structure over olmOCR text.

**Architecture:** Keep ADR 0004 (exact raw bytes). Extend the hosted kraken wire so `message.content` is a JSON document (kraken-shaped segmentation), still wrapped in OpenAI `chat.completion` for HF compatibility. `KrakenChatCompletionAdapter` detects structured content and maps lines/regions into graph nodes with real geometry; plain-text content remains a fallback. Stop lying that provisional full-page boxes are “coordinate-rich” (merge’s `_coordinate_rich_line_count` counts any `bounding_box`). No new PassRunner Protocol work; no Phase 5 COMPLETE.

**Tech Stack:** Python 3.13, Pydantic 2, pytest, existing `witness_adaptation.py`, `kraken_runner.py`, `AbstainingMergeService`, assemble fixtures.

## Locked Decisions

| Topic | Decision |
| --- | --- |
| Why now | Operator spine + `document-run` done; Phase 4 coordinate-rich bullet still deferred in runbook. |
| Raw layer | Still exact HF response bytes (`chat.completion`). Structured geometry lives in `choices[0].message.content` as a **JSON string** (not a parallel invented file schema outside the runner). |
| Content schema | Lock `wordwending.kraken_segmentation/v1` (below) — inspired by `kraken.containers.Segmentation` / `BaselineLine`, mapped into our `LineRecord`/`RegionRecord`. |
| Fallback | If content is plain text (current fixtures), keep newline provisional **without** page-wide fake boxes (`bounding_box=None`, empty baseline). |
| olmOCR | Stay text-first. Change shared `_build_provisional_page` so provisional lines/spans/regions do **not** get full-page `bounding_box` (fixes false coordinate-rich counting). Region may keep a page box only if needed for graph validity — prefer region box OK, **line/span boxes None**. |
| IDs | Stable: `region_id = f"{prepared_page_id}:r{i}"`, `line_id = f"{prepared_page_id}:l{i}"`, `span_id = f"{prepared_page_id}:s{i}"` (same family as Wave A). |
| Coords | All geometry in `PreparedPage.coordinate_space` (shared page space). No PageAlignmentService extraction this slice. |
| Runner prompt | Update `KRAKEN_TRANSCRIPTION_PROMPT` → request only the v1 JSON object (no markdown fences, no commentary). |
| artifact_kind | Keep `text` + `application/json` unless Spec 0013 forces a new kind — do not invent `layout` without model support. |
| Merge policy | Multi-witness defaults must prefer kraken for structure: `structure_scaffold_runner_ids: ["kraken", "olmocr"]`. Update assemble helper + multi-witness fixtures (olmocr-only fixtures stay `["olmocr"]`). Without this, `_pick_scaffold_witness` short-circuits on first listed runner and never uses `_coordinate_rich_line_count`. |
| Space ids | Every `BoundingBox.coordinate_space_id`, `Polygon.coordinate_space_id`, and `LineRecord.baseline_coordinate_space_id` MUST equal `PreparedPage.coordinate_space.space_id` (e.g. `"prepared-page-1"`). Do **not** rely on BoundingBox’s default `"prepared-page"` — mismatched ids exclude the witness from merge. |
| Baseline iff | Follow `LineRecord.validate_baseline_coordinate_space`: baseline present ↔ `baseline_coordinate_space_id` set (same space id). |
| Out of scope | Live HF bake-off; Phase 5/10 COMPLETE; god-module splits; PAGE-XML path; auto review events. |

## Witness content schema (lock)

When structured, `message.content` is a JSON object (stringified inside chat.completion):

```json
{
  "schema": "wordwending.kraken_segmentation/v1",
  "type": "baselines",
  "text_direction": "horizontal-lr",
  "regions": [
    {
      "id": "region_0",
      "bbox": [0, 0, 200, 300]
    }
  ],
  "lines": [
    {
      "id": "line_0",
      "text": "Diplomatic line one",
      "baseline": [[10, 40], [180, 42]],
      "boundary": [[10, 20], [180, 20], [180, 50], [10, 50]],
      "bbox": [10, 20, 180, 50],
      "region_ids": ["region_0"]
    },
    {
      "id": "line_1",
      "text": "Diplomatic line two",
      "baseline": [[10, 80], [180, 82]],
      "boundary": [[10, 60], [180, 60], [180, 90], [10, 90]],
      "bbox": [10, 60, 180, 90],
      "region_ids": ["region_0"]
    }
  ]
}
```

**Mapping rules:**

| Kraken v1 field | Graph field |
| --- | --- |
| `regions[].bbox` `[x0,y0,x1,y1]` | `RegionRecord.bounding_box` with `coordinate_space_id=space.space_id` |
| `lines[].bbox` | `LineRecord.bounding_box` + span box (same space id) |
| `lines[].baseline` `[[x,y],…]` | `LineRecord.baseline` as `Point` list + `baseline_coordinate_space_id=space.space_id` |
| `lines[].boundary` | `LineRecord.polygon` (`Polygon` with ≥3 points + same space id; close ring if needed) |
| `lines[].text` | Span diplomatic text |
| missing regions | Synthesize one BODY region from union of line boxes (same space id) |
| `type: "bbox"` only | Baselines optional; boxes required |

**Reject / accept rules:**

- Reject structured payload if any line lacks **`bbox` or `baseline`** (boundary-only is not enough — `_coordinate_rich_line_count` only counts `bounding_box` or `baseline`).
- Boundary alone may decorate a line that already has bbox/baseline; do not accept a line that only has `boundary`.
- Plain-text fallback: no line/span boxes; no baseline.

## Subagent Model Policy

| Role | Model |
| --- | --- |
| Mechanical TDD | `composer-2.5-fast` |
| Integration / stuck / ADR review | `cursor-grok-4.5-medium` |
| Code-quality review | `composer-2.5-fast` |

Per task: implement → spec/ADR review → fix → quality review → fix → commit.

Every subagent: workspace `/Users/cmalek/src/workspace/wordwending`; `source .venv/bin/activate`; `/usr/bin/cd`; graphify before explore; ruff/mypy/napoleon-gate/focused pytest; `graphify update .` after code.

## Global Constraints

- Activate `.venv`; `/usr/bin/cd` only.
- ADR 0004: do not invent a second on-disk raw schema outside runner-persisted bytes.
- ADR 0003: geometry in shared prepared-page coordinates.
- ADR 0008: stable ids across rebuilds for same structured input.
- TDD; Napoleon `#:` / docstrings on non-test Python.
- Do not mark Phase 5/10 COMPLETE.

## File Map

| File | Role |
| --- | --- |
| `wordwending/services/kraken_runner.py` | Prompt + docstring: expect structured JSON content |
| `wordwending/services/witness_adaptation.py` | Structured kraken parse + provisional without fake line boxes |
| `tests/fixtures/assemble/kraken-segmentation-v1.json` | **New** chat.completion whose content is stringified v1 segmentation |
| `tests/fixtures/assemble/kraken-chat-completion-v1.json` | Keep as plain-text fallback fixture |
| `tests/test_witness_adaptation.py` | Structured + fallback + olmOCR provisional null line boxes |
| `tests/test_assemble.py` | `_merge_policy`: when runners include `kraken`, set `structure_scaffold_runner_ids=["kraken", …rest]` (not `[ordered[0]]`) |
| `tests/fixtures/assemble/manifest-multi-witness-v1.json` | `structure_scaffold_runner_ids: ["kraken", "olmocr"]` |
| `tests/fixtures/hands_off/merge-policy.json` | Same multi-witness scaffold order |
| `tests/fixtures/document_run/merge-policy.json` | Same multi-witness scaffold order |
| `tests/test_coordinate_rich_merge.py` | **New** olmOCR text + kraken structured → scaffold prefers kraken; line boxes distinct |
| `tests/test_kraken_runner.py` | Prompt/content contract if asserted |
| `doc/source/runbook/from_source_to_markdown.rst` | Drop “coordinate-rich deferred” where this slice lands |
| `doc/source/architecture/wave_b_architecture_notes.rst` | Same honesty update |
| `README.md` | Brief honesty update |

---

### Task 1: Fixture + structured parse unit tests (TDD)

**Files:**
- Create: `tests/fixtures/assemble/kraken-segmentation-v1.json`
- Modify: `tests/test_witness_adaptation.py`

**Model:** `composer-2.5-fast`

Fixture = OpenAI `chat.completion` with `message.content` = **string** of the v1 JSON object (not nested object — real HF content is a string).

Tests:

```python
def test_adapt_kraken_structured_sets_per_line_boxes_and_baselines(...):
    # two lines; distinct bboxes; baselines non-empty; space ids match prepared page
    # _coordinate_rich_line_count semantics: both lines count

def test_adapt_kraken_plain_text_fallback_has_no_line_boxes(...):
    # existing kraken-chat-completion-v1.json → lines with bounding_box is None

def test_adapt_olmocr_provisional_has_no_line_boxes(...):
    # regression: olmOCR provisional must not use page-wide line boxes
```

- [ ] Step 1: Write failing tests + fixture
- [ ] Step 2: RED
- [ ] Step 3: (implementation in Task 2) — stop after RED if preferred, or continue in Task 2
- [ ] Commit fixture + failing tests only **or** fold into Task 2 single commit after GREEN

### Task 2: Kraken structured adapter + provisional box honesty (TDD)

**Files:**
- Modify: `wordwending/services/witness_adaptation.py`
- Modify: `tests/test_witness_adaptation.py` (from Task 1)

**Model:** `cursor-grok-4.5-medium`

**Behavior (lock):**

1. `KrakenChatCompletionAdapter.extract_segmentation(raw_bytes) -> StructuredKrakenPage | list[str]`:
   - Parse chat.completion content string.
   - If content parses as JSON object with `schema == "wordwending.kraken_segmentation/v1"`, return structured model (small TypedDict/dataclass/Pydantic in this module or `models/`).
   - Else treat as plain text → newline lines (fallback).
2. `WitnessAdaptationService.adapt_page` for `kraken`:
   - Structured → build regions/lines/spans with real geometry (mapping table above).
   - All geometry space ids = `prepared_page.coordinate_space.space_id`.
   - Baseline iff `baseline_coordinate_space_id` (`LineRecord.validate_baseline_coordinate_space`).
   - Fallback → `_build_provisional_page` **without** line/span page-wide boxes.
3. olmOCR path: `_build_provisional_page` without line/span page-wide boxes (region may retain page box for a single BODY region).
4. Docstrings: remove “coordinate-rich fields are not present” for kraken when structured; document dual-mode.

- [ ] Implement until Task 1 tests GREEN
- [ ] ruff/mypy/napoleon-gate + `graphify update .`
- [ ] Commit

### Task 3: Kraken runner prompt contract (TDD)

**Files:**
- Modify: `wordwending/services/kraken_runner.py`
- Modify: `tests/test_kraken_runner.py`

**Model:** `composer-2.5-fast`

Replace `KRAKEN_TRANSCRIPTION_PROMPT` with a prompt that demands **only** the v1 JSON object (schema id, lines with bbox/baseline/text, optional regions). Assert prompt string contains `wordwending.kraken_segmentation/v1` in tests.

Still persist `response.content` exact bytes (ADR 0004). No second write path.

- [ ] Failing test on prompt constant
- [ ] Update prompt
- [ ] GREEN + gates + commit

### Task 4: Multi-witness merge prefers kraken geometry (TDD)

**Files:**
- Create: `tests/test_coordinate_rich_merge.py` (or extend `tests/test_assemble.py`)
- Modify: `tests/test_assemble.py` (`_merge_policy` helper)
- Modify: `tests/fixtures/assemble/manifest-multi-witness-v1.json`
- Modify: `tests/fixtures/hands_off/merge-policy.json`
- Modify: `tests/fixtures/document_run/merge-policy.json`
- Fixtures: olmOCR plain chat.completion + kraken segmentation v1 under `tests/fixtures/assemble/`

**Model:** `cursor-grok-4.5-medium`

**Scenario:**

1. Adapt olmOCR plain + kraken structured for same `PreparedPage`.
2. `AbstainingMergeService.merge_page` with `MergePolicy(structure_scaffold_runner_ids=["kraken", "olmocr"], ...)`.
3. Assert accepted lines use kraken-distinct boxes (not full-page), and/or scaffold witness is kraken (`_coordinate_rich_line_count(kraken) > _coordinate_rich_line_count(olmocr)` when olmOCR has null boxes).
4. **Wire the assemble spine:** change `_merge_policy` so when `runners` contains `kraken`, scaffold order is `["kraken", …other runners…]` (today it uses `[ordered[0]]`, which keeps olmocr first for `["olmocr", "kraken"]` and never falls through to coordinate-rich counting). Update multi-witness merge-policy JSON fixtures the same way. Leave single-runner olmocr fixtures as `["olmocr"]`.
5. Optional assemble-level test: two raw witnesses → bundle page line boxes match kraken fixture boxes.

- [ ] Failing tests
- [ ] Update `_merge_policy` + multi-witness fixture scaffold order
- [ ] GREEN (should pass once Task 2 done; fix merge only if unexpected)
- [ ] Commit

### Task 5: Docs honesty

**Files:**
- `doc/source/runbook/from_source_to_markdown.rst`
- `doc/source/architecture/wave_b_architecture_notes.rst`
- `README.md`

**Model:** `composer-2.5-fast`

- [ ] State: kraken structured segmentation v1 → coordinate-rich adapt; plain-text fallback remains provisional
- [ ] Remove blanket “coordinate-rich second-runner deferred” **or** narrow to “live HF endpoint must emit v1 JSON; fixtures prove the spine”
- [ ] Keep Phase 5/10 NOT COMPLETE
- [ ] Commit

### Task 6: Exit checklist

**Model:** `cursor-grok-4.5-medium` (reviewer)

- [ ] `pytest tests/test_witness_adaptation.py tests/test_coordinate_rich_merge.py tests/test_kraken_runner.py -q` green (adjust paths if names differ)
- [ ] Structured kraken lines have baselines + distinct boxes; olmOCR provisional lines have `bounding_box is None`
- [ ] All geometry space ids == prepared page `space_id` (not default `"prepared-page"`)
- [ ] Multi-witness fixtures / `_merge_policy` scaffold order starts with `kraken`
- [ ] Runbook/README honesty matches code
- [ ] Human gate summary

---

## Out of scope (later)

1. Phase 5 live bake-off / cost-license scoring  
2. Extract `PageAlignmentService` / `PageGraphBuilder` from merge  
3. Native non-chat.completion kraken HTTP API (if HF later exposes one)  
4. God-module splits  

## Execution Handoff

**Plan saved to:** `docs/superpowers/plans/2026-08-08-coordinate-rich-kraken.md`

**Recommended:** Subagent-Driven (`composer-2.5-fast` / `cursor-grok-4.5-medium` only).

1. Subagent-Driven (recommended)  
2. Inline Execution  

**Which approach?**
