# Spec 0014 Review Task and Overlay Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make review overlays a validated append-only decision log with rebuildable materialized state and explicit successor/rebase handling.

**Architecture:** Keep persisted Pydantic shapes in bochord.models.ocr. Add a small ReviewOverlayService for deterministic replay and successor construction; BundleLayoutService remains responsible only for files. Do not add a database, event bus, UI, or mutable graph patch path.

**Tech Stack:** Python 3.13, Pydantic 2, pytest, stdlib json/datetime.

**Sequence:** 2 of 5. Depends on Spec 0005 packet factory.

---

## Global Constraints

- Implementers: only **Composer 2.5 Fast** (mechanical) or **Cursor Grok 4.5** (integration judgment). Reviewers: any appropriate model.
- Per task: implementer → spec review → same implementer fixes/re-review → code-quality review → same implementer fixes/re-review. Fresh whole-plan reviewer after Task 4.
- Before Python: source .venv/bin/activate. After Python edits: touched-file ruff, mypy, make napoleon-gate, focused pytest.
- Models remain in bochord.models.ocr. Service code stays in bochord.services.review_overlay. No dynamic action registry or generic event framework.
- Review events are append-only inputs. Rebuilding state never edits event data; a rebase always creates successor overlay with predecessor_overlay_id.
- Preserve diplomatic-only text corrections. Never introduce normalized-text operator input.

## Existing Baseline

- ReviewTask, including the prior plan's prepared-image checksum and related-object binding, thirteen-plus discriminated ReviewEvent shapes, OverlayState, PageOverlay, and binding validation exist in ocr.py.
- Existing validation catches duplicate ids, unknown tasks, task action/dimension violations, stale run/revision binding, and flag lifecycle.
- Missing contract proof/behavior: geometry-space agreement/resolution, event-to-task scope/guideline checks, deterministic state replay, and safe successor creation.

## File Map

- Modify: bochord/models/ocr.py — narrow schema/validator gaps.
- Create: bochord/services/review_overlay.py — replay + successor builder.
- Modify: bochord/models/__init__.py — public exports only if needed.
- Modify: tests/test_ocr_models.py — JSON schema and negative invariant tests.
- Create: tests/test_review_overlay.py — replay/rebase behavior.
- Create: tests/fixtures/review_overlay/page-overlay-v1.json — stable representative overlay JSON.

### Task 1: Close Schema Binding and Geometry-Identity Gaps

**Files:** Modify bochord/models/ocr.py; Modify tests/test_ocr_models.py.

- [ ] **Step 1: Write failing tests**

Cover each missing hard error:
1. correct_geometry with both box and polygon in different coordinate_space_id rejects;
2. RegionRevision with both box and polygon in different coordinate_space_id rejects;
3. event target_scope different from its ReviewTask target_scope rejects;
4. event guideline_version different from task guideline_version rejects;
5. task prepared_image_checksum different from PageOverlay prepared_image_checksum rejects;
6. FlagReviewEvent whose new_trust_state differs from prior_trust_state rejects;
7. RegionRevision without box or polygon rejects;
8. OverlayState object/scope mismatch with an applied event rejects.

- [ ] **Step 2: Verify RED**

    source .venv/bin/activate
    pytest tests/test_ocr_models.py -k "overlay and coordinate_space and guideline" -v

Expected: FAIL because current models accept at least these invalid shapes.

- [ ] **Step 3: Implement smallest validation**

BoundingBox.coordinate_space_id / Polygon.coordinate_space_id remain the single authoritative geometry identity; do not add an event-level duplicate. Add a small shared validator used by CorrectGeometryReviewEvent and RegionRevision to reject conflicting box/polygon spaces, and require RegionRevision to contain at least one geometry form; update any existing structural fixtures accordingly. Add FlagReviewEvent validator requiring new_trust_state == prior_trust_state. In PageOverlay.validate_review_bindings compare task checksum, event target scope, and guideline version to its task; build event-id lookup and reject state entries that reference events for another object or scope. Preserve current discriminated union and error messages where not changed.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/models/ocr.py tests/test_ocr_models.py
    mypy bochord/models/ocr.py
    make napoleon-gate
    pytest tests/test_ocr_models.py -k "overlay or coordinate_space or guideline" -q
    git add bochord/models/ocr.py tests/test_ocr_models.py
    git commit -m "fix: harden review overlay bindings"

### Task 2: Replay Append-Only Events Into OverlayState

**Files:** Create bochord/services/review_overlay.py; Create tests/test_review_overlay.py.

- [ ] **Step 1: Write failing replay tests**

Build one overlay containing accept, correct_text, correct_style, polygon-only correct_geometry, reclassify, link/unlink, mark_illegible, flag, and resolve_flag events. Assert replay returns state only from recorded order, has no normalized override, records applied ids, preserves orthogonal typography/roles, stores polygon override, records marker ids on the target note after link/unlink, removes inactive flags, and leaves trust unchanged for flag/resolve events.

- [ ] **Step 2: Verify RED**

    pytest tests/test_review_overlay.py::test_replay_materializes_only_append_only_event_effects -v

Expected: FAIL; ReviewOverlayService absent.

- [ ] **Step 3: Implement direct replay**

Add OverlayState.polygon_override and replace misleading linked_note_ids with linked_marker_span_ids (migrate any fixture use). Implement ReviewOverlayService.materialize(overlay) -> list[OverlayState]. Iterate existing validated events once in order; update per (target_object_id, target_scope). correct_geometry replaces box and/or polygon; link_note unions marker_span_ids into the target note; unlink_note removes exactly those marker ids. Apply state fields named by the event contract. Structural split/merge/reorder retain audit/trust/event ids but do not mutate BundlePage; that projection requires later graph-revision workflow. No cache or persistence.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/review_overlay.py tests/test_review_overlay.py
    mypy bochord/services/review_overlay.py
    make napoleon-gate
    pytest tests/test_review_overlay.py -q
    git add bochord/services/review_overlay.py tests/test_review_overlay.py
    git commit -m "feat: replay review overlays deterministically"

### Task 3: Create Successor Overlays for Rebase

**Files:** Modify bochord/services/review_overlay.py; Modify tests/test_review_overlay.py.

- [ ] **Step 1: Write failing tests**

Given old overlay, a complete caller-supplied successor task map, task-id map, object-id map, new run/graph/checksum, and resolvable coordinate-space ids, assert create_successor:
- allocates supplied new overlay id;
- sets predecessor_overlay_id;
- copies only events whose task, target ids, nested payload ids, and coordinate spaces still resolve;
- retains source events unchanged;
- retains caller-supplied PENDING ADJUDICATION ReviewTask packets for each conflict;
- materializes successor current_state from copied events.

- [ ] **Step 2: Verify RED**

    pytest tests/test_review_overlay.py::test_successor_rebases_only_resolved_events_and_queues_conflicts -v

Expected: FAIL; successor operation absent.

- [ ] **Step 3: Implement explicit successor**

Add ReviewOverlayService.create_successor. Require a complete successor ReviewTask map whose tasks already bind the new run/graph/checksum, plus explicit old→new task/object id maps and a resolvable coordinate-space-id set; reject missing task mappings, unresolved nested marker/region/line ids, or geometry outside the supplied set. No fuzzy id matching. Build distinct successor events by rebinding only mapped ids; caller provides event ids. Preserve original overlay untouched. Conflict task packets are caller-supplied existing ADJUDICATION tasks, never guessed by service.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/review_overlay.py tests/test_review_overlay.py
    mypy bochord/services/review_overlay.py
    make napoleon-gate
    pytest tests/test_review_overlay.py -q
    git add bochord/services/review_overlay.py tests/test_review_overlay.py
    git commit -m "feat: create auditable overlay successors"

### Task 4: Freeze JSON Contract and Bundle Integration

**Files:** Create tests/fixtures/review_overlay/page-overlay-v1.json; Modify tests/test_ocr_models.py; Modify tests/test_bundle_layout.py only if manifest pointer test needs change.

- [ ] **Step 1: Write failing fixture tests**

Load page-overlay-v1.json through PageOverlay, assert model_dump(mode="json") equals fixture, replay equals fixture current_state, and BundleLayoutService preserves review_events JSONL/current_state pointer on rerun.

- [ ] **Step 2: Verify RED**

    pytest tests/test_ocr_models.py tests/test_review_overlay.py tests/test_bundle_layout.py -k "overlay_v1 or overlay_state" -v

Expected: FAIL; fixture absent.

- [ ] **Step 3: Add fixture and only required manifest assertion**

Fixture includes an allowed task, changed text/style/polygon geometry, open and resolved flags, a note link marker list, and explicit coordinate-space ids. Do not make BundleLayoutService replay or overwrite overlays.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/models/ocr.py bochord/services/review_overlay.py tests/test_ocr_models.py tests/test_review_overlay.py tests/test_bundle_layout.py
    mypy bochord/models/ocr.py bochord/services/review_overlay.py
    make napoleon-gate
    pytest tests/test_ocr_models.py tests/test_review_overlay.py tests/test_bundle_layout.py -q
    git add bochord/models/ocr.py bochord/services/review_overlay.py tests/fixtures/review_overlay tests/test_ocr_models.py tests/test_review_overlay.py tests/test_bundle_layout.py
    git commit -m "test: freeze review overlay schema contract"

## Final Review Focus

- Invalid bindings, stale evidence, unknown state/event references, and coordinate-space ambiguity fail hard.
- Replay depends only on ordered event log and never writes it.
- Rebase makes successors and explicit adjudication conflicts; it never mutates predecessor or guesses target identity.

## Cost Stop

Stop after JSON parity, replay cache, and explicit rebase construction. Do not build UI, automatic graph mutation, database persistence, or conflict heuristics.
