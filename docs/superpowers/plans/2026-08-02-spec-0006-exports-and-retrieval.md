# Spec 0006 Exports and Retrieval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate deterministic bundle-adjacent RAG JSON/JSONL and evidence-preserving Markdown from accepted page graphs, with traceable provenance, trust, footnotes, and stitched chunks.

**Architecture:** Add a pure DocumentExportService that derives RagDocument and Markdown from DocumentBundle. Keep file layout/writes in BundleLayoutService, which already owns exports paths and atomic JSON helpers. Bundle JSON remains source of truth; no exporter reads raw witness text as document text.

**Tech Stack:** Python 3.13, Pydantic 2, stdlib json/pathlib, pytest.

**Sequence:** 4 of 5. Obeys Spec 0011 boundary; Spec 0016 freezes model JSON afterward.

---

## Global Constraints

- Implementers: only **Composer 2.5 Fast** (mechanical) or **Cursor Grok 4.5** (integration judgment). Reviewers: any appropriate model.
- Per task: implementer → spec review → same implementer fixes/re-review → code-quality review → same implementer fixes/re-review. Fresh whole-plan reviewer after Task 4.
- Before Python: source .venv/bin/activate. After Python edits: touched-file ruff, mypy, make napoleon-gate, focused pytest.
- Create no external search/index integration, token-window chunker, TEI/XML serializer, or domain-specific dictionary/grammar model.
- Derive only from accepted BundlePage graph order, review/trust fields, and provenance. Raw witnesses remain evidence pointers only.
- V1 chunk types: region_chunk and footnote_chunk. table_chunk stays absent.
- Do not mutate DocumentBundle/page graph to make exports.

## Existing Baseline

- DocumentBundle, ExportSummary, RagDocument, RagChunk, StitchedChunk, RetrievalProvenance, and retrieval metadata models already exist in ocr.py.
- BundlePage validates graph references; regions have accepted reading order; notes carry marker span ids and provenance.
- BundleLayoutService writes the established bundle tree but does not build document RAG/Markdown outputs.

## File Map

- Create: bochord/services/document_export.py — pure chunk/Markdown renderer.
- Modify: bochord/services/bundle_layout.py — write named document export files via BundlePaths.
- Modify: tests/test_document_export.py — renderer and provenance tests.
- Modify: tests/test_bundle_layout.py — persisted export paths/content.
- Create: tests/fixtures/exports/minimal-bundle.json — compact graph with style + footnote coverage.

### Task 1: Derive Page-Local Region and Footnote Chunks

**Files:** Create bochord/services/document_export.py; Create tests/test_document_export.py; Create tests/fixtures/exports/minimal-bundle.json.

- [ ] **Step 1: Write failing chunk tests**

Load representative DocumentBundle. Assert build_rag_document:
- emits one region_chunk per region in reading order and one footnote_chunk per note;
- region text follows region line_order/span_ids;
- each footnote lists note_id, marker span ids, page id, and region id when present;
- provenance unions source pages, witnesses, runners from included graph objects;
- metadata includes page number, region kind, reviewed/corrected booleans, and typography signals;
- trust is corrected if any included object corrected, reviewed only if every included object reviewed/corrected, else machine.

- [ ] **Step 2: Verify RED**

    source .venv/bin/activate
    pytest tests/test_document_export.py::test_build_rag_document_emits_region_and_footnote_chunks -v

Expected: FAIL; service absent.

- [ ] **Step 3: Implement minimum pure renderer**

Implement DocumentExportService.build_rag_document(bundle) -> RagDocument. Use direct local helpers to resolve ordered lines/spans and aggregate data; reject dangling source ids only through existing validated models. Generate stable ids as region-{region_id} and footnote-{note_id}; chunking_recipe_id is a module constant. Do not introduce configurable chunk policies.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/document_export.py tests/test_document_export.py
    mypy bochord/services/document_export.py
    make napoleon-gate
    pytest tests/test_document_export.py -q
    git add bochord/services/document_export.py tests/test_document_export.py tests/fixtures/exports
    git commit -m "feat: derive page-local retrieval chunks"

### Task 2: Produce Accepted-Order Stitched Chunks

**Files:** Modify bochord/services/document_export.py; Modify tests/test_document_export.py.

- [ ] **Step 1: Write failing tests**

Assert stitched chunks use ordered component chunk ids and at least two distinct ordered page ids, never include footnote chunks in main-text stitch, preserve object/provenance union, and aggregate trust by same rule. Test two pages with joined continuation: page order derives from DocumentBundle.pages then accepted region order, never witness order. Assert a one-page run creates no StitchedChunk.

- [ ] **Step 2: Verify RED**

    pytest tests/test_document_export.py::test_stitching_uses_accepted_graph_order_not_witness_order -v

Expected: FAIL; stitched_chunks empty.

- [ ] **Step 3: Implement smallest stitch rule**

Emit one stitched main-text chunk only for a contiguous region-kind run spanning at least two pages. Its text joins component region chunk text with newline separators; it records every component id/page/object/provenance. A run contained on one page remains page-local only. No token window, semantic section detector, or footnote stitching.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/document_export.py tests/test_document_export.py
    mypy bochord/services/document_export.py
    make napoleon-gate
    pytest tests/test_document_export.py -q
    git add bochord/services/document_export.py tests/test_document_export.py
    git commit -m "feat: stitch accepted retrieval chunks"

### Task 3: Render Evidence-Preserving Markdown

**Files:** Modify bochord/services/document_export.py; Modify tests/test_document_export.py.

- [ ] **Step 1: Write failing Markdown tests**

Assert render_markdown:
- uses accepted region order and does not use witness text;
- renders italic/bold safely, with a fixed <sup> convention for superscripts;
- emits marker references in main text and matching note bodies in a Notes section;
- renders table/marginal/unknown regions as explicit labeled placeholders rather than prose flattening;
- keeps region/page boundaries visible and never silently drops footnotes.

- [ ] **Step 2: Verify RED**

    pytest tests/test_document_export.py::test_markdown_preserves_style_regions_and_note_linkage -v

Expected: FAIL; renderer absent.

- [ ] **Step 3: Implement direct renderer**

Add DocumentExportService.render_markdown(bundle) -> str. Escape Markdown control characters in diplomatic text before applying recoverable style markers. Map footnote marker spans using NoteRecord.linked_marker_span_ids, then append deterministic [^note-id] bodies. Use plain paragraphs for body prose; special regions receive short explicit delimiters/placeholders.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/document_export.py tests/test_document_export.py
    mypy bochord/services/document_export.py
    make napoleon-gate
    pytest tests/test_document_export.py -q
    git add bochord/services/document_export.py tests/test_document_export.py
    git commit -m "feat: render evidence-preserving markdown"

### Task 4: Write Standard Document Export Artifacts

**Files:** Modify bochord/services/bundle_layout.py; Modify tests/test_bundle_layout.py; Modify tests/test_document_export.py.

- [ ] **Step 1: Write failing integration test**

After BundleLayoutService writes a minimal bundle, call its new write_document_exports(bundle, root). Assert:
- exports/bundle.json validates as DocumentBundle and has a complete ExportSummary for all four output paths;
- exports/rag.jsonl has one JSON object per page-local chunk;
- exports/stitched_chunks.jsonl has one per stitched chunk;
- exports/document.md equals renderer output;
- every path equals returned ExportSummary, original input bundle is unchanged, and rerun atomically replaces export files but preserves overlays/review_events.jsonl.

- [ ] **Step 2: Verify RED**

    pytest tests/test_bundle_layout.py::test_write_document_exports_writes_derived_views -v

Expected: FAIL; writer absent.

- [ ] **Step 3: Implement narrow integration**

Instantiate DocumentExportService inside BundleLayoutService.write_document_exports. Reuse existing private atomic text/json write helpers and BundlePaths.document_exports_dir. Build complete ExportSummary paths, create a non-mutating bundle.model_copy(update={"exports": summary}), atomically write that copy to exports/bundle.json, then write RAG JSONL, stitched JSONL, and Markdown. Return that copied DocumentBundle; its exports is the completed summary. JSONL gets a trailing newline when nonempty. Do not change write_document_bundle behavior or add CLI wiring.

- [ ] **Step 4: Verify GREEN + commit**

    ruff check bochord/services/document_export.py bochord/services/bundle_layout.py tests/test_document_export.py tests/test_bundle_layout.py
    mypy bochord/services/document_export.py bochord/services/bundle_layout.py
    make napoleon-gate
    pytest tests/test_document_export.py tests/test_bundle_layout.py -q
    git add bochord/services/document_export.py bochord/services/bundle_layout.py tests/test_document_export.py tests/test_bundle_layout.py tests/fixtures/exports
    git commit -m "feat: write retrieval and markdown exports"

## Final Review Focus

- exports/bundle.json is canonical and complete; derived exports read accepted graph only.
- Page-local and stitched chunks retain stable ids, source objects, provenance, and explicit trust.
- Footnotes are independently retrievable and recoverable in Markdown context.
- No target-domain ontology, search backend, table semantics, or token chunking.

## Cost Stop

Stop at standard RAG JSONL, stitched JSONL, and Markdown. Add table chunks later only when data and evaluation justify them. Semantic consumer transforms belong in downstream packages — `bochord` is an OCR framework for faithful evidence-preserving output, not a general structured-data transformer.
