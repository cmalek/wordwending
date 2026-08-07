# Task D2 Report

## Status

**COMPLETE**

BASE confirmed: `89a7f3205a07b3512bd462af2603c67068bd4f68`  
**Commit:** `1cd3b644e23794279cbc8aedd6a979266bef6c99`

## Delivered

Map Spec 0009 `MergeFlag` / `EvaluationFlag` types → Spec 0005 `ReviewTask` packets (no shadow schema).

### Mapping

| MergeFlagType | Spec 0005 packet |
|---|---|
| `text_disagreement` (span targets) | `TEXT` |
| `role_conflict` | `TEXT` |
| `typography_conflict` | `TYPOGRAPHY` |
| `note_link_ambiguous` | `NOTE_LINKAGE` |
| `structure_scaffold_conflict` (region targets) | `LAYOUT` / `STRUCTURE` |
| `insufficient_evidence` | `ADJUDICATION` (no dedicated packet) |
| `text_disagreement` (note targets) | `ADJUDICATION` (no note-text packet) |

### Behavior

- **`MergeFlagReviewService`** projects merge flags into the correct `PageEvaluationSummary` families and builds packets via `HumanMarkupService`
- **`HumanMarkupService._classify_flag_targets`** resolves known merge `flag_type` values even when flags were mis-bucketed into `text` (C3 legacy shape)
- **Assemble** uses `MergeFlagReviewService.project_onto_page` instead of dumping every merge flag into the text family
- No new CLI (YAGNI; D1 owns apply/materialize); library + tests sufficient

## Files

- `wordwending/services/merge_review.py` — new mapper / projector / packet builder
- `wordwending/services/review_markup.py` — merge `flag_type` override in classification
- `wordwending/services/assemble.py` — dimension-aware projection
- `tests/test_merge_review.py` — mapping + projection tests

## Tests

```
tests/test_merge_review.py — 9 passed
tests/test_review_markup.py — regression green
tests/test_assemble.py — regression green
```

Focused suite: **39 passed**

## Quality gates

- `ruff` on touched files — pass
- `mypy` on touched services — pass
- `make napoleon-gate` — pass (no new violations)
- `graphify update .` — pass

## Concerns / follow-ups

- **Task packets still not persisted** to a bundle sidecar (Spec 0002 has no review-task path yet); operators get packets in-memory via `MergeFlagReviewService.build_review_tasks` / `HumanMarkupService.build_review_tasks`
- **Structure flags with line ids** still send line ids to adjudication (layout packets are region-scoped only) — pre-existing Spec 0005 scope limit
- **`insufficient_evidence` storage** remains in the text evaluation family for sidecar collection; classification forces adjudication

## BLOCKED items

None — Spec 0005 models sufficient for all mapped merge flag types.

---

## Important fixes (post-review)

**Status:** COMPLETE  
**BASE:** `1cd3b644e23794279cbc8aedd6a979266bef6c99`

### Changes

1. **Enum/map exhaustiveness** — `test_merge_flag_dimension_map_is_exhaustive` asserts `set(_MERGE_FLAG_DIMENSION) == set(MergeFlagType)` (module-level assert blocked by ruff S101).
2. **DI** — `MergeFlagReviewService` injected into `AssembleOrchestrator` / `_AssembleExecution` via optional `merge_flag_review` kwarg (defaults to fresh instance); removed module singleton `_MERGE_FLAG_REVIEW`.
3. **Assemble integration coverage** — `test_assemble_document_projects_non_text_merge_flags` uses a thin `_MergeWithExtraFlags` merge wrapper to assert typography/structure flags land in non-text evaluation families through the full assemble path.

### Tests

```
tests/test_merge_review.py — 10 passed (+1 exhaustiveness)
tests/test_assemble.py — 6 passed (+1 non-text projection)
tests/test_review_markup.py — regression green
```

Focused suite: **41 passed**

### Quality gates

- `ruff` — pass
- `mypy` — pass
- `make napoleon-gate` — pass
- `graphify update .` — pass

### Remaining concerns

- Task packets still not persisted to bundle sidecar (unchanged, out of scope)
- Structure flags with line ids still route to adjudication (pre-existing Spec 0005 limit)
- `insufficient_evidence` remains stored in text family for sidecar collection
