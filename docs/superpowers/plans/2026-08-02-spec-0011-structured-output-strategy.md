# Spec 0011 Structured Output Strategy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Freeze evidence-preserving bochord output as the product boundary and explicitly defer TEI-inspired dictionary, grammar, reader, and translation ontologies to downstream packages.

**Architecture:** This is a documentation/architecture checkpoint, not a feature. Existing BundlePage, DocumentBundle, review metadata, and export models remain standard layer 1. No target-domain model, XML serializer, transform registry, or downstream package is created before repeated real use proves it belongs here.

**Tech Stack:** reStructuredText, Sphinx, existing Pydantic public models.

**Sequence:** 3 of 5. It constrains Specs 0006 and 0016.

---

## Global Constraints

- This plan has no production-code implementation task. Do not fabricate code merely to make a policy executable.
- Implementer model policy when editing docs: **Composer 2.5 Fast**; use **Cursor Grok 4.5** only if cross-reference repair needs judgment. Reviewers: any appropriate model.
- Per task: implementer → spec review → same implementer fixes/re-review → documentation-quality review. Fresh whole-plan reviewer after Task 3.
- Do not add TEI dependency, XML export, generic transformation interface, plugin registry, or model classes named Entry/Sense/GrammarSection/Translation.
- If a later product need appears in two or more downstream consumers, open a new ADR/spec first; do not extend this plan.

## Existing Baseline

- Spec 0011 already states layer 1 (standard evidence-rich OCR), layer 2 (optional profiles), and layer 3 (consumer models).
- Existing models already carry prepared artifacts, witnesses, accepted page graph, review/evaluation metadata, provenance, and provisional RAG shapes.
- ADR 0007 prevents premature generic runner abstraction; same evidence-first YAGNI principle applies to downstream ontology.

## File Map

- Create: doc/source/adr/adr_0010_structured_output_boundary.rst — accepted boundary decision (required ADR location).
- Modify: doc/source/architecture/index.rst — include the relative ADR 0010 toctree entry.
- README.md — no change; current file lacks a dedicated architecture/consumer-contract section.

### Task 1: Write Decision Record

**Files:** Create doc/source/adr/adr_0010_structured_output_boundary.rst; Modify doc/source/architecture/index.rst.

- [ ] **Step 1: Write review checklist before ADR text**

In a temporary planning note or review comment, list required assertions:
- layer 1 is bochord’s canonical output;
- TEI P5 is reference, never v1 XML requirement;
- downstream packages own dictionary/grammar/reader models;
- stable ids and bibliographic/acquisition provenance must survive transformation;
- shared profile requires demonstrated repeated use.

- [ ] **Step 2: Verify checklist against spec**

    rg -n "standard|TEI|downstream|provenance|shared" doc/source/architecture/spec_0011_structured_output_strategy.rst

Expected: every checklist claim has direct spec support.

- [ ] **Step 3: Write minimal ADR**

Use current ADR reStructuredText format. Record context, decision, consequences, and rejected alternative “universal target schema/XML-first workflow.” Create doc/source/adr/ if absent, then add ../adr/adr_0010_structured_output_boundary to the existing architecture index toctree.

- [ ] **Step 4: Build docs + commit**

    source .venv/bin/activate
    make napoleon-gate
    make -C doc html
    git add doc/source/adr/adr_0010_structured_output_boundary.rst doc/source/architecture/index.rst
    git commit -m "docs: record structured output boundary"

### Task 2: Verify No Public Documentation Change Is Needed

**Files:** None.

- [ ] **Step 1: Confirm README scope**

    rg -n "^Architecture$|^Consumer|^Output Contract" README.md

Expected: no dedicated architecture/consumer-contract section exists.

- [ ] **Step 2: Record deliberate no-op**

State in task report and final plan review: “README unchanged; ADR is the authoritative architecture statement.” Do not add a README paragraph to a non-existent section and do not create an empty commit.

- [ ] **Step 3: Verify ADR is discoverable**

    source .venv/bin/activate
    make -C doc html

Expected: Sphinx resolves the architecture-index relative ADR toctree entry.

### Task 3: Audit Later Plans Against Boundary

**Files:** Modify docs/superpowers/plans/2026-08-02-spec-0006-exports-and-retrieval.md; Modify docs/superpowers/plans/2026-08-02-spec-0016-concrete-export-models.md only if wording contradicts ADR.

- [ ] **Step 1: Review explicit non-goals**

Check planned exports/models do not create dictionary entries, grammar sections, TEI serializers, or a generic transform framework.

- [ ] **Step 2: Record any required one-line constraint**

If needed, add: “No document-specific ontology; downstream packages transform DocumentBundle/RagDocument.” Do not change task scope otherwise.

- [ ] **Step 3: Verify**

    rg -n "TEI|dictionary|grammar|translation|transform registry" docs/superpowers/plans/2026-08-02-spec-0006-exports-and-retrieval.md docs/superpowers/plans/2026-08-02-spec-0016-concrete-export-models.md

Expected: only explicit deferral/non-goal references remain.

- [ ] **Step 4: Commit only real changes**

    git add docs/superpowers/plans/2026-08-02-spec-0006-exports-and-retrieval.md docs/superpowers/plans/2026-08-02-spec-0016-concrete-export-models.md
    git commit -m "docs: constrain export plans to standard output"

## Final Review Focus

- ADR accurately reflects accepted spec from required doc/source/adr/ location; no new runtime mechanism.
- Every later export/model task consumes evidence-rich standard structures rather than inventing a universal target ontology.
- No unnecessary dependency or XML work added.

## Cost Stop

This policy is implementation complete after ADR/docs validation. Add a shared downstream profile only after documented repeat demand.
