# Spec 0005 Human Markup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create evidence-bound, dimension-specific human-review task packets; humans never directly rewrite witnesses, graphs, or exports.

**Architecture:** One cohesive HumanMarkupService maps accepted BundlePage content plus evaluation flags to explicit ReviewTask packets. Its constructor receives the current guideline id/version and relevant calibration ids from orchestration; it never invents review guidance. Reuse PAGE XML interchange; Spec 0014 freezes persistence/replay JSON after the packet behavior is established.

**Tech Stack:** Python 3.13, Pydantic 2, pytest.

**Sequence:** 1 of 5. Finish before Spec 0014.

---

## Global Constraints

- Implementers: only **Composer 2.5 Fast** (mechanical) or **Cursor Grok 4.5** (integration judgment). Reviewers: any appropriate model.
- Per task: implementer → spec review → same implementer fixes/re-review → code-quality review → same implementer fixes/re-review. Fresh whole-plan reviewer after Task 4.
- Before Python: source .venv/bin/activate. After Python edits: touched-file ruff, mypy, make napoleon-gate, focused pytest.
- Create task packets only. No UI, CLI, graph mutation, overlay write/replay, or duplicate external review format.
- Fixed evidence order: prepared image; scope overlay; raw witness; independent witnesses; accepted graph; flags/prior events; controls/checklist.
- Reuse existing ReviewTask, ReviewDimension, ReviewTaskType, ReviewScope, ReviewAction, EvaluationFlag, BundlePage. Add only task image-checksum binding, related ids, and source/preparation dispositions this spec needs.

## Existing Baseline

- ocr models already carry review tasks, append-only events, overlays, per-object trust, and evaluation flags.
- PageXmlInterchangeService already exports supported PAGE review packages.
- No service creates concrete review task packets from a canonical page.

## File Map

- Create: bochord/services/review_markup.py — packet factory + queue builder.
- Modify: bochord/models/ocr.py — task image-checksum/related ids and source/preparation decision event/disposition shapes.
- Modify: tests/test_review_markup.py — task behavior.
- Modify: tests/test_ocr_models.py — new shape validation.
- Modify: bochord/services/__init__.py only if service exports are public there.

### Task 1: Create Exact Text-Review Packets

**Files:** Create bochord/services/review_markup.py; Create tests/test_review_markup.py.

- [ ] **Step 1: Write failing test**

    def test_text_packet_has_exact_scope_and_evidence_order(page: BundlePage) -> None:
        service = HumanMarkupService("review-v1", "1.0.0", ["cal-1"])
        task = service.create_text_task(
            page, ["span-2"], run_id="run-1", graph_revision="graph-1"
        )
        assert task.target_scope is ReviewScope.SPAN
        assert task.target_object_ids == ["span-2"]
        assert task.dimensions == [ReviewDimension.TEXT]
        assert task.required_evidence == [
            "prepared-page-image", "scope-overlay", "raw-text-witnesses",
            "independent-witnesses", "accepted-page-graph",
            "evaluation-and-prior-review", "decision-controls-and-checklist",
        ]
        assert task.allowed_actions == [
            ReviewAction.ACCEPT, ReviewAction.CORRECT_TEXT,
            ReviewAction.MARK_ILLEGIBLE, ReviewAction.FLAG,
        ]

- [ ] **Step 2: Verify RED**

    source .venv/bin/activate
    pytest tests/test_review_markup.py::test_text_packet_has_exact_scope_and_evidence_order -v

Expected: FAIL; service absent.

- [ ] **Step 3: Implement minimum**

Add required ReviewTask.prepared_image_checksum first. Update every existing ReviewTask fixture in tests/test_ocr_models.py with its bound checksum and add one missing-checksum rejection case. Create HumanMarkupService(guideline_id, guideline_version, calibration_example_ids=()). Reject missing/blank guidance at construction, reject non-span ids, produce concrete diplomatic-text question/completion criterion, and copy supplied guidance plus page.prepared_page.image_checksum to every task. Use deterministic task id from page id/type/target ids. No registry/configuration.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/models/ocr.py bochord/services/review_markup.py tests/test_ocr_models.py tests/test_review_markup.py
    mypy bochord/models/ocr.py bochord/services/review_markup.py
    make napoleon-gate
    pytest tests/test_ocr_models.py tests/test_review_markup.py -q
    git add bochord/models/ocr.py bochord/services/review_markup.py tests/test_ocr_models.py tests/test_review_markup.py
    git commit -m "feat: build evidence-bound text review tasks"

### Task 2: Add Layout, Typography, and Note-Linkage Packets

**Files:** Modify bochord/services/review_markup.py; Modify tests/test_review_markup.py.

- [ ] **Step 1: Write failing parameterized tests**

Cover one region layout, one span typography, and one note-linkage task. Assert concrete question, correct exclusive dimension and scope, exact ids, abstention support, and allowed actions: layout uses geometry/reclassify/reorder/split/merge; typography uses correct_style; notes use link_note/unlink_note. For note linkage, primary target is note scope/id and linked marker span ids are in an explicit related_object_ids field. Assert no text task certifies typography.

- [ ] **Step 2: Verify RED**

    pytest tests/test_review_markup.py -k "layout or typography or note_linkage" -v

Expected: FAIL; factory methods absent.

- [ ] **Step 3: Implement direct methods**

First add ReviewTask.related_object_ids with duplicate/overlap rejection, then add create_layout_task, create_typography_task, create_note_linkage_task. Validate primary ids against regions/spans/notes and related marker ids against spans. Split/merge task scope contains every source region. Preserve separate trust dimensions.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/review_markup.py tests/test_review_markup.py
    mypy bochord/services/review_markup.py
    make napoleon-gate
    pytest tests/test_review_markup.py -q
    git add bochord/services/review_markup.py tests/test_review_markup.py
    git commit -m "feat: add dimension-specific review packets"

### Task 3: Add Source and Preparation Packets

**Files:** Modify bochord/services/review_markup.py; Modify tests/test_review_markup.py.

- [ ] **Step 1: Write failing tests**

Assert create_source_triage_task and create_preparation_task target page_id, name whole-page and small-font checks, keep checksum/transform evidence visible, and allow explicit source outcomes (usable, usable-with-warning, reprepare, reacquire) or explicit preparation decision (full-page/subdivide), plus abstention.

- [ ] **Step 2: Verify RED**

    pytest tests/test_review_markup.py -k "source_triage or preparation" -v

Expected: FAIL; methods absent.

- [ ] **Step 3: Implement minimum**

In ocr.py add only SourceTriageDecision and PreparationDecision enums plus two discriminated review events carrying their decision and optional reason; add their fixed ReviewAction values and union exports. Validate their task type/dimension in PageOverlay. Then return page-scoped concrete packets exposing only their matching decision action, accept where meaningful, flag, and abstention path. Do not add a workflow engine or image processing trigger.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/models/ocr.py bochord/services/review_markup.py tests/test_ocr_models.py tests/test_review_markup.py
    mypy bochord/models/ocr.py bochord/services/review_markup.py
    make napoleon-gate
    pytest tests/test_review_markup.py -q
    git add bochord/models/ocr.py bochord/services/review_markup.py tests/test_ocr_models.py tests/test_review_markup.py
    git commit -m "feat: add source and preparation review tasks"

### Task 4: Build Deterministic Flag-Driven Queue

**Files:** Modify bochord/services/review_markup.py; Modify tests/test_review_markup.py.

- [ ] **Step 1: Write failing integration test**

Create a page with text, structure, typography, note-linkage, and unknown-target flags. Assert build_review_tasks preserves every flagged id, maps unknown/empty ids to one page-scoped ADJUDICATION flag task, sorts deterministic dimension/scope/id order, and never marks a sample as page-wide certified coverage.

- [ ] **Step 2: Verify RED**

    pytest tests/test_review_markup.py::test_build_review_tasks_preserves_dimension_specific_coverage -v

Expected: FAIL; queue builder absent.

- [ ] **Step 3: Implement queue builder**

Flatten PageEvaluationSummary flags, group only compatible dimension/scope targets, and call factory methods. Add create_adjudication_flag_task using existing ReviewTaskType.ADJUDICATION, ReviewScope.PAGE, page_id target, the page checksum, and only flag/accept controls; unknown/empty target ids use it. Return list[ReviewTask]; do not persist.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/review_markup.py tests/test_review_markup.py
    mypy bochord/services/review_markup.py
    make napoleon-gate
    pytest tests/test_review_markup.py tests/test_page_interchange.py -q
    git add bochord/services/review_markup.py tests/test_review_markup.py
    git commit -m "feat: derive review queue from evaluation flags"

## Final Review Focus

- Exact scope, evidence sequence, concrete questions, allowed controls, abstention path, and independent dimensions.
- No review UI, direct graph rewrite, or implicit cross-dimension trust upgrade.
- Existing PAGE exchange reused; no second interchange format.

## Cost Stop

Stop after packet construction. Event replay/rebase/schema changes are next plan; operator UI is unrequested.
