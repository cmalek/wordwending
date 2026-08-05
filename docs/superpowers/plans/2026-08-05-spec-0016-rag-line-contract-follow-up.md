# Spec 0016 RAG Line Contract Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make standalone `RagChunk` and `StitchedChunk` JSONL lines enforce Spec 0016 page/provenance truth, while keeping `RagDocument` responsible only for document-wide references.

**Architecture:** Keep canonical DTOs in `bochord.models.ocr`. Put intrinsic tier invariants on their own Pydantic models so `rag.jsonl` and `stitched_chunks.jsonl` reject invalid lines before wrapping; retain only ownership, id uniqueness, component resolution, and component-union checks on `RagDocument`. Document one shared ordered-distinct page rule in Spec 0016; Spec 0006 remains high-level export behavior.

**Tech Stack:** Python 3.13, Pydantic 2, pytest, stdlib `json` and `pathlib`.

## Global Constraints

- Before Python: `source .venv/bin/activate`; use repo-local `.venv` tools.
- Canonical DTOs remain in `bochord.models.ocr`; no export framework, dependency, CLI, or service abstraction.
- Generate JSON Schema from Pydantic only. Regenerate checked-in snapshot when field constraints change; do not hand-edit schema JSON.
- Preserve existing BundlePage and PreparedPage validators and all unrelated dirty worktree changes.
- TDD: add failing observable validation tests before model code, then run focused tests.
- After Python source edits: `ruff`, `mypy`, `make napoleon-gate`, and focused pytest must pass.
- Do not implement Spec 0004 Phases 5, 6, or 10; no bake-off, runner-boundary rewrite, or ops hardening.
- Do not add table extraction, XML/TEI, search integration, target-domain models, or any Spec 0006 non-goal.

## Exact Invariant Matrix

| Contract | `RagChunk` line model | `StitchedChunk` line model | `RagDocument` only |
| --- | --- | --- | --- |
| page tier | `page_ids` has exactly one id | `page_ids` has at least two ids and no repeated id | Validates component-derived span has at least two distinct pages |
| provenance pages | `page_ids == provenance.source_page_ids` | `page_ids == provenance.source_page_ids` | Calculates ordered-distinct page union from resolved component chunks and requires it equal `stitched.page_ids` |
| source objects | `source_object_ids` is non-empty | Existing required field unchanged; no new speculative cardinality rule | None |
| standalone JSONL | Validation applies through `model_validate_json` | Validation applies through `model_validate_json` | Not required for a single line |
| document relationship | None | None | Unique chunk/stitch ids; every child `document_id` equals parent; every component id resolves |

**Ordered-distinct page rule:** preserve first occurrence order; reject duplicate page identities in a `StitchedChunk` line. Its provenance page list must be exactly the same ordered sequence. `RagDocument` uses that same first-seen union over component `RagChunk.provenance.source_page_ids`. This is one definition per boundary: line models own intrinsic shape; document model owns cross-line resolution. A stitch must retain at least one component id because Spec 0006 requires component references, but component membership and its full page union remain document-level facts.

## File Map

- Modify: `doc/source/architecture/spec_0016_concrete_export_models.rst` — state exact line-tier and ordered-distinct provenance rules; no duplicate normative rule in Spec 0006.
- Modify: `bochord/models/ocr.py` — local Pydantic field bounds and model validators on `RagChunk` and `StitchedChunk`; slim `RagDocument.validate_references` to relational checks.
- Modify: `tests/test_ocr_models.py` — direct construction and `model_validate_json` negative tests, plus relocated document-level tests.
- Modify: `tests/fixtures/export_models/rag-document-v1.schema.json` — regenerated Pydantic schema only.
- Verify unchanged: `tests/fixtures/export_models/rag-document-v1.json`, `bochord/services/document_export.py`, and `bochord/services/bundle_layout.py`; current fixture and JSONL tests already exercise valid emitted lines.

### Task 1: Specify and Enforce Intrinsic RAG Line Invariants

**Files:** Modify `doc/source/architecture/spec_0016_concrete_export_models.rst`; Modify `bochord/models/ocr.py`; Modify `tests/test_ocr_models.py`.

**Consumes:** Existing `_rag_chunk`, `_stitched_chunk`, `_retrieval_provenance`, and `_minimal_rag_document` builders in `tests/test_ocr_models.py`.

**Produces:** `RagChunk.validate_page_provenance()` and `StitchedChunk.validate_page_provenance()` that make valid line instances safe before `RagDocument` exists.

- [ ] **Step 1: Write failing standalone line tests**

  Add focused tests beside existing RAG model tests. Use direct model construction for each intrinsic invalid shape and `model_validate_json` for JSONL boundary proof:

  ```python
  def test_rag_chunk_json_line_rejects_multi_page_provenance() -> None:
      payload = _rag_chunk().model_dump(mode="json")
      payload["page_ids"] = ["page-0001", "page-0002"]
      payload["provenance"]["source_page_ids"] = [
          "page-0001",
          "page-0002",
      ]
      with pytest.raises(ValidationError):
          RagChunk.model_validate_json(json.dumps(payload))

  def test_stitched_chunk_json_line_rejects_single_page_provenance() -> None:
      payload = _stitched_chunk().model_dump(mode="json")
      payload["page_ids"] = ["page-0001"]
      payload["provenance"]["source_page_ids"] = ["page-0001"]
      with pytest.raises(ValidationError):
          StitchedChunk.model_validate_json(json.dumps(payload))
  ```

  Assert `ValidationError` for field-cardinality failures and stable custom error fragments for provenance equality or duplicate-page failures. Cover all following negative cases:

  - `RagChunk`: zero pages, two pages, different one-page provenance, empty `source_object_ids`.
  - `StitchedChunk`: one page with one-page provenance; duplicate page id such as `["page-0001", "page-0001"]`; multi-page `page_ids` with only one provenance page; multi-page pages with provenance in different order; empty `component_chunk_ids`.
  - `RagDocument`: keep duplicate ids, child `document_id`, unknown component ids, and component ordered-distinct union mismatch tests. Move former local tier tests to direct line-model tests so no assertion relies on wrapper-only validation.

- [ ] **Step 2: Run focused tests and confirm RED**

  ```bash
  source .venv/bin/activate
  rtk pytest tests/test_ocr_models.py -k "rag_chunk or stitched_chunk or rag_document" -q
  ```

  Expected: new standalone malformed lines validate, so new rejection assertions fail.

- [ ] **Step 3: Make minimal contract and model changes**

  In Spec 0016 RAG Contract, replace generic stitched-page sentence with exact paragraph: page-local chunks have exactly one page and matching singleton provenance; stitched chunks have two or more distinct page ids in first-seen order and exactly matching provenance ids; their component union uses that same rule. Keep Spec 0006 prose as product-level behavior, avoiding a second divergent validation definition.

  In `bochord/models/ocr.py`, use Pydantic field bounds where JSON Schema can express cardinality, then short after-model validators for equality and uniqueness:

  ```python
  class RagChunk(SchemaModel):
      page_ids: list[str] = Field(min_length=1, max_length=1)
      source_object_ids: list[str] = Field(min_length=1)
      # ...

      @model_validator(mode="after")
      def validate_page_provenance(self) -> RagChunk:
          if self.page_ids != self.provenance.source_page_ids:
              raise ValueError(
                  "page-local RagChunk page_ids must match provenance.source_page_ids"
              )
          return self
  ```

  ```python
  class StitchedChunk(SchemaModel):
      component_chunk_ids: list[str] = Field(min_length=1)
      page_ids: list[str] = Field(min_length=2)
      # ...

      @model_validator(mode="after")
      def validate_page_provenance(self) -> StitchedChunk:
          if len(set(self.page_ids)) != len(self.page_ids):
              raise ValueError("StitchedChunk page_ids must be distinct")
          if self.page_ids != self.provenance.source_page_ids:
              raise ValueError(
                  "StitchedChunk page_ids must match provenance.source_page_ids"
              )
          return self
  ```

  Remove repeated local cardinality, source-object, and page/provenance checks from `RagDocument.validate_references`. Retain its document ownership, unique ids, missing component, component-union, and component-span validation. Keep the current first-seen loop as single document-level union implementation; do not add a helper or service change.

- [ ] **Step 4: Run focused tests and confirm GREEN**

  ```bash
  source .venv/bin/activate
  rtk pytest tests/test_ocr_models.py -k "rag_chunk or stitched_chunk or rag_document" -q
  ```

  Expected: standalone invalid JSON lines reject; valid region, footnote, and multi-page stitch still round-trip.

- [ ] **Step 5: Run required code quality checks**

  ```bash
  source .venv/bin/activate
  rtk .venv/bin/ruff check bochord/models/ocr.py tests/test_ocr_models.py
  rtk .venv/bin/mypy bochord/models/ocr.py
  rtk make napoleon-gate
  rtk pytest tests/test_ocr_models.py -k "rag_chunk or stitched_chunk or rag_document" -q
  ```

- [ ] **Step 6: Commit Task 1**

  ```bash
  git add doc/source/architecture/spec_0016_concrete_export_models.rst bochord/models/ocr.py tests/test_ocr_models.py
  git commit -m "fix: validate rag export lines"
  ```

### Task 2: Regenerate Schema and Prove Frozen Export Compatibility

**Files:** Modify `tests/fixtures/export_models/rag-document-v1.schema.json`; verify `tests/fixtures/export_models/rag-document-v1.json`, `tests/test_bundle_layout.py`, `bochord/services/document_export.py`, and `bochord/services/bundle_layout.py` unchanged.

**Consumes:** Task 1 field bounds and existing `_stable_json_schema(RagDocument)` snapshot test; `test_write_document_exports_frozen_contract_jsonl_validates` already parses every emitted `rag.jsonl` line as `RagChunk` and every stitched JSONL line as `StitchedChunk`.

**Produces:** Schema snapshot containing Pydantic `minItems`/`maxItems` constraints for local RAG line cardinality, with frozen payload and service outputs still valid.

- [ ] **Step 1: Run snapshot test and confirm RED**

  ```bash
  source .venv/bin/activate
  rtk pytest tests/test_ocr_models.py::test_generated_schema_rag_document_v1_matches_snapshot -q
  ```

  Expected: FAIL because `Field(min_length=...)`/`max_length=...` alters Pydantic-generated JSON Schema while checked-in snapshot still lacks corresponding `minItems` and `maxItems`.

- [ ] **Step 2: Regenerate only RAG schema snapshot from Pydantic**

  From activated venv, run this one-off regeneration command; it keeps deterministic indentation, key order, and trailing newline without adding a runtime export command:

  ```bash
  python -c 'import json; from pathlib import Path; from bochord.models import RagDocument; Path("tests/fixtures/export_models/rag-document-v1.schema.json").write_text(json.dumps(RagDocument.model_json_schema(), indent=2, sort_keys=True) + "\n", encoding="utf-8")'
  ```

  Do not change `rag-document-v1.json`: it already has valid single-page chunks and ordered distinct stitched provenance. Do not regenerate `document-bundle-v1.schema.json`: no `DocumentBundle` field changed.

- [ ] **Step 3: Prove schema, frozen fixture, and emitted JSONL GREEN**

  ```bash
  source .venv/bin/activate
  rtk pytest tests/test_ocr_models.py -k "export_model_fixture_rag_document_v1 or generated_schema_rag_document_v1" -q
  rtk pytest tests/test_document_export.py::test_build_rag_document_frozen_contract_validates -q
  rtk pytest tests/test_bundle_layout.py::test_write_document_exports_frozen_contract_jsonl_validates -q
  ```

  Expected: frozen RAG document validates; every persisted JSONL line validates directly; emitted stitched lines retain two or more distinct pages with provenance exactly equal to `page_ids`.

- [ ] **Step 4: Run full required quality gate**

  ```bash
  source .venv/bin/activate
  rtk .venv/bin/ruff check bochord/models/ocr.py tests/test_ocr_models.py tests/test_document_export.py tests/test_bundle_layout.py
  rtk .venv/bin/mypy bochord/models/ocr.py
  rtk make napoleon-gate
  rtk pytest tests/test_ocr_models.py tests/test_document_export.py tests/test_bundle_layout.py -q
  ```

  If an existing exporter test fails, repair only its emitted data in `bochord/services/document_export.py`; preserve its current `_ordered_page_ids_from_chunks` and `_union_chunk_provenance` first-seen logic unless the failure proves they diverge. No service edit is expected from current code/fixtures.

- [ ] **Step 5: Commit Task 2**

  ```bash
  git add tests/fixtures/export_models/rag-document-v1.schema.json
  git commit -m "test: freeze rag line contract schema"
  ```

## Acceptance Checks

- `RagChunk.model_validate_json` rejects no pages, multiple pages, mismatched singleton provenance, and no source objects.
- `StitchedChunk.model_validate_json` rejects one-page stitches even when its provenance also says one page; rejects duplicate page identity; rejects incomplete or reordered provenance; rejects no component id.
- Valid standalone multi-page stitch has ordered-distinct `page_ids` equal to its provenance source pages.
- `RagDocument` still rejects duplicate ids, wrong child document ids, missing component ids, component spans under two pages, and page list different from component provenance union; it does not redefine local line invariants.
- Existing frozen fixture round-trips unchanged; regenerated `rag-document-v1.schema.json` exactly matches `RagDocument.model_json_schema()`.
- Existing frozen-layout test validates every `rag.jsonl` and `stitched_chunks.jsonl` line directly and confirms Spec 0016 no longer permits a stitch to claim one provenance page.
- No BundlePage/PreparedPage validation change; no Spec 0004 Phase 5/6/10, Spec 0006 non-goal, TEI/XML, table, search, CLI, runner, or dependency work.

## Plan Self-Review

- Spec coverage: Spec 0016 exact prose and line validation are Task 1; Spec 0006 component and JSONL behavior are Task 2; ADR 0002 page-local truth and ADR 0010 structured-output boundary are preserved by keeping page/retrieval DTOs in `bochord.models.ocr` without domain models.
- No duplicate local tier definition: direct models validate their own persisted line; `RagDocument` validates relations needing sibling chunks.
- No schema hand-maintenance: Task 2 writes snapshot exclusively from `RagDocument.model_json_schema()`.
