# Spec 0009 Merge and Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve competing pass witnesses into one accepted page graph via an abstaining merge: one primary value per object, alternates in provenance, flags instead of false certainty.

**Architecture:** Add merge policy/result models and one `AbstainingMergeService` facade driving a per-page `MergeOrchestrator`. V1 is deterministic precedence + geometry alignment heuristics; no learned ranker. Before corpus-calibrated runner precedence exists, text candidates stay equal-status and the merge abstains into review flags. Reuse Spec 0008 `TextNormalizer` when emitting accepted diplomatic/normalized text.

**Tech Stack:** Python 3.13, Pydantic 2, existing geometry helpers from evaluation (`_box_iou` pattern — extract shared util only if duplication exceeds ~15 lines), pytest. No new dependency.

**Sequence:** 3 of 4. Start only after Spec 0008 plan passes final review.

**Governing ADR:** ADR 0003 (shared page graph) and ADR 0004 (raw witnesses stay intact; merge writes derived graph only). Trust fields follow ADR 0008 vocabulary.

## Global Constraints

- One accepted interpretation per derived object; alternates live in provenance, not duplicate graph nodes.
- Merge decision order is fixed: prepared variant → coordinates → layout/lines → text → typography/roles → note linkage → emit graph + confidence/flags.
- Choose one structure scaffold per page (prefer coordinate-rich layout witness).
- Typography facets resolve independently; missing evidence → `unknown`, never silent regular/upright/baseline defaults.
- Note linkage is explicit; ambiguous → candidates + review flag.
- Confidence concepts stay separate: `machine_confidence`, `merge_confidence`, `trust_state`.
- Flag instead of resolve when disagreement is material or evidence is weak.
- One prepared variant per accepted page graph; other variants remain alternate run evidence.
- Human review later must not erase merge provenance (this plan only preserves fields for that).
- No probabilistic joint inference, global document optimization, or learned merge models.
- Follow Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Before Python commands: `source .venv/bin/activate`.
- After Python edits: touched-file `ruff`, touched-file `mypy`, `make napoleon-gate`, then focused pytest.

## Subagent Model Policy

- Implementation tasks may use only **Cursor Grok** (`cursor-grok-4.5-medium`) or **Composer 2.5 Fast** (`composer-2.5-fast`). No other implementer models.
- Prefer Composer 2.5 Fast for mechanical TDD; use Cursor Grok when stuck or judgment is required.
- Review steps (spec compliance, code quality, final whole-plan) may use any appropriate model.
- Give each implementer only the generated task brief, prior-task interface decisions, and listed files.

For every task, use this serial Superpowers loop:

1. Implementer (Composer 2.5 Fast or Cursor Grok) implements, runs listed checks, self-reviews, and commits.
2. Spec-compliance reviewer (any appropriate model) reviews without editing.
3. Same implementer fixes; re-review until approved.
4. Fresh code-quality reviewer (any appropriate model) reviews without editing.
5. Same fix/re-review loop for quality findings.

After the last task, a fresh reviewer audits the whole plan.
Do not start the next task or plan while either review has open findings.

## Existing Baseline

- Graph models (`RegionRecord`, `LineRecord`, `SpanRecord`, `NoteRecord`) and `ObjectProvenance` (`machine_confidence`, `merge_confidence`, `disagreement_note`) exist.
- `Typography` facets already default to `unknown`.
- Evaluation already flags low `merge_confidence` regions.
- Spec 0008 supplies `TextNormalizer` (required predecessor).
- No merge service, no alternate-candidate provenance structure, no merge flag emitter.

---

## File Map

- Create: `bochord/models/merge.py` — policy, candidates, merge result, flags.
- Modify: `bochord/models/ocr.py` — extend `ObjectProvenance` with alternate candidates (additive).
- Modify: `bochord/models/__init__.py` — exports.
- Create: `bochord/services/merge.py` — `AbstainingMergeService` + `MergeOrchestrator`.
- Create: `tests/test_merge_service.py`
- Create: `tests/fixtures/merge/` — minimal multi-witness pages.
- Modify: `tests/test_ocr_models.py` — provenance alternate validation.

### Task 1: Merge Models and Provenance Alternates

**Files:**

- Create: `bochord/models/merge.py`
- Modify: `bochord/models/ocr.py`
- Modify: `bochord/models/__init__.py`
- Modify: `tests/test_ocr_models.py`
- Create: `tests/test_merge_service.py` (model section)

**Interfaces:**

```python
class MergeFlagType(StrEnum):
    TEXT_DISAGREEMENT = "text_disagreement"
    TYPOGRAPHY_CONFLICT = "typography_conflict"
    ROLE_CONFLICT = "role_conflict"
    NOTE_LINK_AMBIGUOUS = "note_link_ambiguous"
    STRUCTURE_SCAFFOLD_CONFLICT = "structure_scaffold_conflict"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class AlternateCandidate(SchemaModel):
    witness_id: str
    runner_id: str
    value_kind: str  # "text" | "typography" | "role" | "note_link" | "geometry"
    value: dict[str, Any]  # ponytail: small typed payloads serialized as dict
    machine_confidence: float | None = Field(default=None, ge=0, le=1)


class ObjectProvenance(SchemaModel):  # extended
    source_page_id: str
    witness_ids: list[str]
    runner_ids: list[str]
    machine_confidence: float | None = Field(default=None, ge=0, le=1)
    merge_confidence: float | None = Field(default=None, ge=0, le=1)
    disagreement_note: str | None = None
    alternate_candidates: list[AlternateCandidate] = Field(default_factory=list)


class MergePolicy(SchemaModel):
    policy_id: str
    version: str
    # Empty means abstain on text disagreement (pre-benchmark default).
    runner_text_precedence: list[str] = Field(default_factory=list)
    structure_scaffold_runner_ids: list[str] = Field(default_factory=list)
    min_merge_confidence_to_accept: float = Field(default=0.6, ge=0, le=1)
    iou_match_threshold: float = Field(default=0.5, ge=0, le=1)
    text_normalization_policy_id: str = "text-norm-v1"


class PassWitnessPage(SchemaModel):
    """One runner's proposed page graph fragment for merge input."""

    witness_id: str
    runner_id: str
    prepared_page_id: str
    coordinate_space: CoordinateSpace
    regions: list[RegionRecord] = Field(default_factory=list)
    lines: list[LineRecord] = Field(default_factory=list)
    spans: list[SpanRecord] = Field(default_factory=list)
    notes: list[NoteRecord] = Field(default_factory=list)
    machine_confidence: float | None = Field(default=None, ge=0, le=1)


class MergePageInput(SchemaModel):
    page_id: str
    page_number: int
    prepared_page: PreparedPage
    witnesses: list[PassWitnessPage] = Field(min_length=1)
    # If multiple prepared variants appear, only matching prepared_page_id merges.


class MergeFlag(SchemaModel):
    flag_id: str
    flag_type: MergeFlagType
    target_object_ids: list[str]
    message: str


class MergePageResult(SchemaModel):
    page: BundlePage
    flags: list[MergeFlag] = Field(default_factory=list)
    abstained: bool = False
```

- [ ] **Step 1: Write failing model tests** for alternate candidates, empty-precedence policy default, and `PassWitnessPage` round-trip.

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement models** (additive provenance field; keep old fixtures valid via default empty list)

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: add abstaining merge policy models

EOF
)"
```

### Task 2: Structure Scaffold and Geometry Alignment

**Files:**

- Create: `bochord/services/merge.py`
- Modify: `tests/test_merge_service.py`
- Create: `tests/fixtures/merge/structure_conflict.json`
- Create: `tests/fixtures/merge/aligned_layout_text.json`

**Interfaces:**

```python
class MergeOrchestrator:
    """Per-page mutable merge state and step runner."""

    def __init__(
        self,
        policy: MergePolicy,
        page_input: MergePageInput,
        text_normalizer: TextNormalizer,
    ) -> None: ...

    def run(self) -> MergePageResult: ...

    def _select_prepared_variant(self) -> None: ...
    def _normalize_coordinates(self) -> None: ...
    def _choose_structure_scaffold(self) -> None: ...
    def _align_layout(self) -> None: ...


class AbstainingMergeService:
    """Stateless facade: merge one page of competing witnesses."""

    def __init__(self, text_normalizer: TextNormalizer | None = None) -> None:
        # When None: TextNormalizer(DEFAULT_TEXT_NORMALIZATION_POLICY)
        # from Spec 0008 (policy_id text-norm-v1). Must match
        # MergePolicy.text_normalization_policy_id unless caller injects
        # an explicit normalizer.
        ...

    def merge_page(
        self,
        page_input: MergePageInput,
        policy: MergePolicy,
    ) -> MergePageResult: ...
```

Scaffold selection:

1. If `structure_scaffold_runner_ids` set, pick first present witness in that order with regions/lines.
2. Else pick witness with most coordinate-rich lines (count of lines with bbox or baseline).
3. If two scaffolds disagree on region count/order beyond policy IoU matching → emit `STRUCTURE_SCAFFOLD_CONFLICT`, keep chosen scaffold, store loser regions as alternate candidates, set `abstained=True` when conflict is material.

Coordinate step: require all witnesses share `prepared_page_id` with `MergePageInput.prepared_page`; otherwise exclude cross-variant witnesses and record them only as skipped alternate evidence (do not invent cross-variant transforms in v1).

- [ ] **Step 1: Write failing tests** for scaffold preference, cross-variant exclusion, structure conflict flag.

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement orchestrator steps 1–4 (through layout align)**

Leave text/typography/notes as stubs returning empty accepted spans if needed, but keep method order in `run()` matching Spec 0009 sequence (stubs OK until Task 3).

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: choose merge structure scaffold and align layout

EOF
)"
```

### Task 3: Text, Typography, Notes, Flags

**Files:**

- Modify: `bochord/services/merge.py`
- Modify: `tests/test_merge_service.py`
- Create: `tests/fixtures/merge/text_disagreement.json`
- Create: `tests/fixtures/merge/typography_conflict.json`
- Create: `tests/fixtures/merge/note_link_ambiguous.json`

**Interfaces / rules:**

**`merge_confidence` v1 (no scoring model):** assign fixed constants only:

| Outcome | `merge_confidence` |
|---------|-------------------|
| Full agreement (no material conflict on that object) | `1.0` |
| Accepted via non-empty `runner_text_precedence` with differing alternates | `0.7` |
| Material disagreement / ambiguous note link / insufficient evidence | `0.3` |

After assigning confidence: if any accepted object's `merge_confidence < policy.min_merge_confidence_to_accept`, set result `abstained=True` and ensure a flag exists for that object. Do not invent continuous/heuristic scores.

Text:

- Match spans to scaffold lines by IoU ≥ threshold.
- Equality compare uses **only** Spec 0008 `TextNormalizer.normalize_span_text(diplomatic)` (no separate compare API). Differing normalized strings = material text disagreement.
- If `runner_text_precedence` empty and normalized texts differ: emit `TEXT_DISAGREEMENT`, set `merge_confidence=0.3`, store alternates, leave `text_diplomatic` from scaffold-aligned primary witness if one exists else abstain with `INSUFFICIENT_EVIDENCE`.
- If precedence non-empty: pick first available runner; store others as alternates; still flag when normalized texts differ (`merge_confidence=0.7` if accepted, else `0.3`).
- Always set accepted `text_normalized` via `text_normalizer.normalize_span_text` / `normalize_note_text`.

Typography:

- Resolve each facet independently from candidate witnesses.
- Agreement → accept (`merge_confidence=1.0` for that object if no other conflicts); conflict → `unknown` for that facet only + `TYPOGRAPHY_CONFLICT` flag + alternates (`merge_confidence=0.3`).
- Never invent `regular`/`upright`/`baseline` from missing evidence.
- Roles separate: conflicting roles → `ROLE_CONFLICT` / `unknown` role handling without changing visual facets.

Notes:

- Unambiguous marker→note mapping → accept (`merge_confidence=1.0`).
- Multiple candidates → `NOTE_LINK_AMBIGUOUS`, empty `linked_marker_span_ids` on accepted note or keep none, store candidates in provenance (`merge_confidence=0.3`).

Emit `ReviewTask`-shaped data? **No** in this plan — emit `MergeFlag` only. Review-task packets are Spec 0005 / Phase 8.

- [ ] **Step 1: Write failing tests** for each rule above (one focused test each).

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement remaining orchestrator steps**

Keep methods ≤ 60 lines; split helpers as needed (`_resolve_span_text`, `_resolve_typography`, `_resolve_note_links`).

- [ ] **Step 4: Run full merge suite**

```bash
pytest tests/test_merge_service.py tests/test_ocr_models.py -q
```

- [ ] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: abstain on weak merge text typography and notes

EOF
)"
```

## Final Review Focus

- Decision order matches Spec 0009.
- Alternates in provenance, not duplicate accepted nodes.
- Empty precedence → abstain/flag, not invented winner.
- Typography facets independent; unknowns preserved.
- Cross-prepared-variant confusion avoided.
- Raw witnesses never mutated (ADR 0004).
- No learned/probabilistic merge.

## Cost Stop

Stop after single-page abstaining merge service. No CLI command, no document-level stitch, no review-task packet builder, no bundle persistence (Spec 0002), no runner precedence calibration from eval scores.
