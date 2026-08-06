# Graph Report - bochord  (2026-08-06)

## Corpus Check
- 127 files · ~181,985 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2859 nodes · 7372 edges · 136 communities (115 shown, 21 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 564 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b4eb7fde`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/preparation.py
- test_document_export.py
- test_text_normalization.py
- RagChunk
- cli.py
- BundlePage
- FlagSeverity
- BundleLayoutService
- test_evaluation_service.py
- Detailed OCR Process
- MetricProfile
- _SpanCandidate
- model_validator
- prepare_pages
- Image
- ._write_page_evaluation_and_manifest
- ._invoke_item
- ADR 0010 Structured Output Boundary
- PlannedRunnerBatch
- test_bundle_layout.py
- check_napoleon_gate.py
- BundlePaths
- test_olmocr_runner.py
- BT Witness Preparation Slice
- TestConfiguration
- PageXmlInterchangeService
- ReviewDimension
- SourcePageArtifact
- PreparationRecipe
- _bundle_page_payload
- SourceAcquisitionService
- test_page_interchange.py
- _RateAccumulator
- ReviewOverlayService
- test_runner_execution.py
- PageEvaluationSummary
- models/__init__.py
- File map
- test_ocr_models.py
- Rename `bochord` → `wordwending` Design
- RunnerInputPackager
- ._coords
- RunnerBatchPlanner
- cli
- PageClass
- Settings
- Path
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- _rag_chunk
- MergeOrchestrator
- TestCLISettings
- test_cli_utils.py
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- print_error
- test_preparation_service.py
- Preparation Gold Specs
- Raw OCR witness layer
- create_progress
- Spec 0002: V1 Bundle Layout and Data Shape
- Diplomatic Text Review
- Coding Standards Docs
- TestCLIGlobalOptions
- ReviewTask
- ADR 0009 OCR-D PAGE eScriptorium
- Spec 0006: Exports and Retrieval Views
- README, Operator Docs, and Thin Export CLI Implementation Plan
- Normalized Page Graph
- Configuration: Command Line Tool
- Anglian dialect group
- TestCLIVersion
- ._normalize_text
- Learner lacks stable conceptual map of sound-change order
- OE Grammar Resources
- MergePolicy
- ADR 0004 Layered Truth
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- TestCLIErrorHandling
- Spec 0016 RAG Line Contract Follow-up Implementation Plan
- TestConsoleQuietMode
- test_merge_service.py
- valid_bundle_page
- model_runner_payload
- Sphinx Docs Index
- Lesson 0003 Pronouncing Old English Letters
- MockHttpxClient
- .validate_https_huggingface_endpoints
- Page Graph Line
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- _review_polygon
- .validate_item_page_alignment
- _NoteCandidate
- ADR 0008 Stable IDs and Review History
- Character Error Rate (CER)
- Napoleon Documentation Contract
- release.sh
- Contributor Covenant 3.0
- ADR 0006 Pass Runner Plugins
- Worked BT entry example: abbad
- Old English c/g palatalization
- OE tēon walk-back (Grimm + h-loss + contraction)
- ipa-play.js
- botocraft AWS Preference
- _prepared_unit_ref
- OCR Evidence Not Philological Semantics
- ADR 0002 Bundle Model
- Page Bundle as Page-Local Truth Unit
- ADR 0003 Page Graph
- SourceProvenanceService
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- TestCLIEval
- Mixed dialect spellings from copying history
- Reference Sound Terms
- TestPrintSuccess
- ._resolve_context
- Spec 0005: Human Markup and Review
- wordwending
- services/merge.py
- _PreparedInputsManifest
- .reject_historical_modernization
- .__init__

## God Nodes (most connected - your core abstractions)
1. `AlternateCandidate` - 120 edges
2. `SchemaModel` - 99 edges
3. `BundlePage` - 99 edges
4. `SpanRecord` - 67 edges
5. `RegionRecord` - 65 edges
6. `MergePolicy` - 59 edges
7. `CoordinateSpace` - 56 edges
8. `LineRecord` - 55 edges
9. `MergePageInput` - 53 edges
10. `PreparedPage` - 53 edges

## Surprising Connections (you probably didn't know these)
- `README` --semantically_similar_to--> `Sphinx Docs Index`  [AMBIGUOUS] [semantically similar]
  README.md → doc/source/index.rst
- `Layer 1 Evidence-Preserving OCR Intermediate` --semantically_similar_to--> `Product Boundary`  [INFERRED] [semantically similar]
  doc/source/adr/adr_0010_structured_output_boundary.rst → CONTEXT.md
- `ExtractionOrchestrator` --semantically_similar_to--> `MergeOrchestrator`  [INFERRED] [semantically similar]
  AGENTS.md → docs/superpowers/plans/2026-07-31-spec-0009-merge-policy.md
- `TextNormalizer Service` --semantically_similar_to--> `TextNormalizer`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-07-31-spec-0008-text-normalization.md → doc/source/architecture/text_normalization_policy_v1.rst
- `Diplomatic vs Normalized Dual Fields` --semantically_similar_to--> `Dual Text Contract`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-07-31-spec-0008-text-normalization.md → doc/source/architecture/text_normalization_policy_v1.rst

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **V1 Page Graph Node Kinds** — doc_source_architecture_adr_0003_page_graph_region, doc_source_architecture_adr_0003_page_graph_line, doc_source_architecture_adr_0003_page_graph_span, doc_source_architecture_adr_0003_page_graph_note [EXTRACTED 1.00]
- **Four-Layer Truth Model** — doc_source_architecture_adr_0004_layered_truth_raw_witness_layer, doc_source_architecture_adr_0004_layered_truth_derived_graph_layer, doc_source_architecture_adr_0004_layered_truth_overlay_layer, doc_source_architecture_adr_0004_layered_truth_export_layer [EXTRACTED 1.00]
- **V1 Core Service Collaborators** — doc_source_architecture_spec_0001_system_architecture_document_run_orchestrator, doc_source_architecture_spec_0001_system_architecture_page_preparation_service, doc_source_architecture_spec_0001_system_architecture_pass_runner_registry, doc_source_architecture_spec_0001_system_architecture_page_alignment_service, doc_source_architecture_spec_0001_system_architecture_page_graph_builder, doc_source_architecture_spec_0001_system_architecture_evaluation_service, doc_source_architecture_spec_0001_system_architecture_overlay_service, doc_source_architecture_spec_0001_system_architecture_bundle_writer [EXTRACTED 1.00]
- **V1 Export Family Triad** — doc_source_architecture_spec_0006_exports_and_retrieval_bundle_json, doc_source_architecture_spec_0006_exports_and_retrieval_rag_json, doc_source_architecture_spec_0006_exports_and_retrieval_markdown [EXTRACTED 1.00]
- **Evidence-Preserving Text Pipeline** — doc_source_architecture_spec_0008_text_normalization_dual_text, doc_source_architecture_spec_0005_human_markup_diplomatic_text, doc_source_architecture_spec_0014_review_overlay_schema_correct_text [INFERRED 0.85]
- **Runner Execution Contract Stack** — doc_source_architecture_spec_0012_runner_execution_and_batching_batch_policy, doc_source_architecture_spec_0013_pass_runner_interface_schema_runner_capability, doc_source_architecture_spec_0013_pass_runner_interface_schema_execution_batch, doc_source_architecture_spec_0012_runner_execution_and_batching_hugging_face [INFERRED 0.85]
- **End-to-End bochord OCR Pipeline Stages** — doc_source_runbook_ocr_process_stage_acquire_source, doc_source_runbook_ocr_process_stage_pdf_to_image, doc_source_runbook_ocr_process_stage_competing_passes, doc_source_runbook_ocr_process_stage_align_evidence, doc_source_runbook_ocr_process_stage_page_graph, doc_source_runbook_ocr_process_stage_evaluate_gold, doc_source_runbook_ocr_process_stage_apply_overlays, doc_source_runbook_ocr_process_stage_export [EXTRACTED 1.00]
- **Evidence Preservation Layers** — doc_source_runbook_ocr_process_ocr_as_evidence, doc_source_runbook_operator_notes_preserve_run_artifacts, teaching_machine_assistance_notes_evidence_layer_separation, doc_source_runbook_ocr_process_stage_apply_overlays [INFERRED 0.85]
- **Spec Completion Sequence 0003→0007→0010→0012** — docs_superpowers_plans_2026_07_25_spec_0003_evaluation_schema_completion_document, docs_superpowers_plans_2026_07_25_spec_0007_preparation_completion_document, docs_superpowers_plans_2026_07_25_spec_0010_page_classification_cohorts_document, docs_superpowers_plans_2026_07_25_spec_0012_runner_execution_batching_document [EXTRACTED 1.00]
- **Text Normalization V1 Pipeline** — docs_superpowers_plans_2026_07_31_spec_0008_text_normalization_textnormalizationpolicy, docs_superpowers_plans_2026_07_31_spec_0008_text_normalization_textnormalizer, doc_source_architecture_text_normalization_policy_v1_text_norm_v1, doc_source_architecture_text_normalization_policy_v1_dual_text_contract, docs_superpowers_plans_2026_08_01_text_normalization_policy_v1_docs_only_contract [EXTRACTED 1.00]
- **BT Witness Prep Through CLI Pipeline** — docs_superpowers_specs_2026_07_10_bt_ocr_witness_preparation_design_bt_witness_prep, docs_superpowers_specs_2026_07_10_bt_ocr_stage_b_live_pairing_and_clamp_regression_design_prepare_pages, docs_superpowers_specs_2026_07_12_wyrdcraeft_ocr_bosworth_toller_bosworth_toller_cli, docs_superpowers_specs_2026_07_12_wyrdcraeft_ocr_bosworth_toller_bt_witness_ocr [EXTRACTED 1.00]
- **Witness-preserving OCR-to-structure workflow** — teaching_machine_assistance_lessons_0004_seven_stage_pipeline, teaching_machine_assistance_lessons_0004_raw_witness_layer, teaching_machine_assistance_lessons_0004_overlay_layer, teaching_machine_assistance_lessons_0004_normalized_export_layer, teaching_machine_assistance_lessons_0004_review_by_exception, teaching_machine_assistance_lessons_0006_entry_block_unit [EXTRACTED 1.00]
- **PIE to OE sound-change layering timeline** — teaching_oe_grammar_lessons_0001_proto_indo_european, teaching_oe_grammar_lessons_0001_grimms_law, teaching_oe_grammar_lessons_0001_verners_law, teaching_oe_grammar_lessons_0001_proto_germanic, teaching_oe_grammar_lessons_0001_i_mutation, teaching_oe_grammar_reference_0001_sound_change_order [EXTRACTED 1.00]
- **OE dialect recognition cue system** — teaching_oe_grammar_lessons_0002_west_saxon, teaching_oe_grammar_lessons_0002_anglian, teaching_oe_grammar_lessons_0002_kentish, teaching_oe_grammar_lessons_0002_mercian, teaching_oe_grammar_lessons_0002_northumbrian, teaching_oe_grammar_reference_0004_dialect_cue_table [EXTRACTED 1.00]
- **Standard Export Families** — context_bundle_json, context_rag_json, context_markdown_export [EXTRACTED 1.00]
- **V1 Retrieval Chunk Types** — docs_superpowers_plans_2026_08_02_spec_0006_exports_and_retrieval_region_chunk, docs_superpowers_plans_2026_08_02_spec_0006_exports_and_retrieval_footnote_chunk, docs_superpowers_plans_2026_08_02_spec_0006_exports_and_retrieval_stitched_chunk [EXTRACTED 1.00]
- **Structured Output Layer Stack** — doc_source_adr_adr_0010_structured_output_boundary_layer_1, doc_source_adr_adr_0010_structured_output_boundary_layer_2_3, doc_source_adr_adr_0010_structured_output_boundary_tei_p5, doc_source_adr_adr_0010_structured_output_boundary_adr_0010 [EXTRACTED 1.00]

## Communities (136 total, 21 thin omitted)

### Community 0 - "services/preparation.py"
Cohesion: 0.05
Nodes (98): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _adaptive_binary() (+90 more)

### Community 1 - "test_document_export.py"
Cohesion: 0.06
Nodes (61): _body_region_page(), _load_frozen_document_bundle_v1(), _load_minimal_bundle(), _markdown_style_page(), _merge_page_regions(), _page_provenance(), _page_witness(), _prepared_page() (+53 more)

### Community 2 - "test_text_normalization.py"
Cohesion: 0.09
Nodes (33): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+25 more)

### Community 3 - "RagChunk"
Cohesion: 0.16
Nodes (9): RagChunk, Page-local retrieval chunk., Build cross-page stitched chunks from contiguous BODY region runs. Args:…, Emit one stitched chunk when a BODY run spans multiple pages. Args:…, Collect ordered distinct page ids from component chunks. Args: chunks: Region…, Union source object ids from component region chunks. Args: chunks: Region…, Union provenance pointers from component region chunks. Args: chunks: Region…, Aggregate trust from one or more trust-state values. Args: trust_states: Trust… (+1 more)

### Community 4 - "cli.py"
Cohesion: 0.05
Nodes (49): Client, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all wordwending errors., RunnerEndpointUnavailable (+41 more)

### Community 5 - "BundlePage"
Cohesion: 0.16
Nodes (24): _expected_evidence(), _page_witnesses(), parametrize, Return Spec 0005 evidence order with a dimension-specific item 3., Return page-local witnesses matching fixture provenance., test_create_adjudication_flag_task_rejects_empty_dimensions(), test_create_note_linkage_task_rejects_unknown_related_span_ids(), test_create_text_task_rejects_empty_target_object_ids() (+16 more)

### Community 6 - "FlagSeverity"
Cohesion: 0.10
Nodes (29): FlagSeverity, Supported top-level source kinds., Severity levels for review and evaluation flags., SourceType, BinarizeMode, ColorMode, CropMode, DewarpMode (+21 more)

### Community 7 - "BundleLayoutService"
Cohesion: 0.06
Nodes (65): _accept_review_event(), load_minimal_bundle(), Path, source_files keys must be bare basenames, not path segments., page_exports basenames must not escape the page exports directory., Append inserts a separator when prior JSONL lacks a trailing newline., Heal must not UnicodeDecodeError when prior JSONL ends on multi-byte UTF-8., Corrupt JSONL lines name the file and line number. (+57 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.06
Nodes (86): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+78 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "MetricProfile"
Cohesion: 0.10
Nodes (18): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., _edit_distance(), _graphemes(), _is_ligature(), _is_macron_grapheme(), _is_thorn_eth() (+10 more)

### Community 11 - "_SpanCandidate"
Cohesion: 0.07
Nodes (42): _apply_span_text_resolution(), _apply_span_typography_resolution(), _first_candidate_by_runner_precedence(), Any, Collect unique witness ids from span candidates in input order. Args:…, Collect unique runner ids from span candidates in input order. Args:…, Apply text agreement or disagreement resolution for one span. Args: span:…, Resolve typography facets from witness span candidates. Args: typography:… (+34 more)

### Community 12 - "model_validator"
Cohesion: 0.05
Nodes (24): _known_page_space_ids(), _known_preparation_space_ids(), model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The… (+16 more)

### Community 13 - "prepare_pages"
Cohesion: 0.11
Nodes (28): argument, command, Context, option, pass_context, eval_cohorts(), eval_page(), export_document() (+20 more)

### Community 14 - "Image"
Cohesion: 0.15
Nodes (13): dark_gutter_image(), note_heavy_image(), Image, Build a page of horizontal text-like bars, then rotate it. Keyword Args:…, Build a page with a dark vertical gutter in the center strip. Returns:…, Build a mostly flat page with dense salt-and-pepper noise. Returns: Grayscale…, Build a page with sparse body ink and dense bottom-quarter notes. Returns:…, Build a page dominated by sustained dark table rules. Keyword Args: rule_count:… (+5 more)

### Community 15 - "._write_page_evaluation_and_manifest"
Cohesion: 0.06
Nodes (40): Multiple source/pages/NNNN.* files must not silently pick one., test_resolve_source_image_path_rejects_ambiguous_extensions(), _atomic_write_json(), _atomic_write_text(), _collect_page_flags(), _executed_passes(), _needs_trailing_newline(), Any (+32 more)

### Community 16 - "._invoke_item"
Cohesion: 0.09
Nodes (24): RequestError, _encode_png_base64(), _failed_item_result(), _load_direct_image(), _load_image_from_pdf(), Any, Image, Path (+16 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "PlannedRunnerBatch"
Cohesion: 0.08
Nodes (51): Runner, overlay, and gold contracts should fit the planned workflow., TypedDict, BatchItemRef, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Runner packaging policies. (+43 more)

### Community 19 - "test_bundle_layout.py"
Cohesion: 0.09
Nodes (43): load_export_minimal_bundle(), load_frozen_document_bundle_v1(), Persisted document exports match renderer output and preserve overlays., Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the compact export-fixture DocumentBundle., Load the frozen document-bundle-v1 contract fixture., test_document_bundle_manifest_rejects_non_positive_page_count(), test_document_bundle_manifest_round_trip() (+35 more)

### Community 20 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 21 - "BundlePaths"
Cohesion: 0.08
Nodes (23): test_bundle_paths_match_spec_0002_layout(), test_source_page_image_rejects_empty_extension(), BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:… (+15 more)

### Community 22 - "test_olmocr_runner.py"
Cohesion: 0.16
Nodes (36): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+28 more)

### Community 23 - "BT Witness Preparation Slice"
Cohesion: 0.05
Nodes (42): ExtractionOrchestrator, Project Structure (models/services/cli/settings), Single Responsibility Service Architecture, Dual Text Contract, Historical Character Preservation, LineJoinRecord, text-norm-v1 Policy, TextNormalizer (+34 more)

### Community 24 - "TestConfiguration"
Cohesion: 0.07
Nodes (21): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+13 more)

### Community 25 - "PageXmlInterchangeService"
Cohesion: 0.10
Nodes (22): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+14 more)

### Community 26 - "ReviewDimension"
Cohesion: 0.10
Nodes (19): HumanMarkupService task types must certify only their exclusive dimension., Return a review task bound to the shared overlay evidence., _task(), Supported human review targets., Independent evidence dimensions a human may inspect and certify., Operator workflow represented by a review task packet., Verb vocabulary for append-only review events., ReviewAction (+11 more)

### Community 27 - "SourcePageArtifact"
Cohesion: 0.10
Nodes (30): One acquired source page before preparation., SourcePageArtifact, _build_assessment(), _build_preparation_result(), Build assessment metadata for one prepared page. Keyword Args: source_page:…, Assemble the persisted result model for one prepared page. Args: source_page:…, _artifact_from_raster(), _image_dpi() (+22 more)

### Community 28 - "PreparationRecipe"
Cohesion: 0.07
Nodes (36): PdfPage, PreparationRecipe, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Deterministic page-preparation profile., _build_prepared_units(), _derive_prepared_page_id(), _ensure_supported_recipe(), _fixed_tile_boxes() (+28 more)

### Community 29 - "_bundle_page_payload"
Cohesion: 0.09
Nodes (24): _bundle_page_payload(), _provenance(), Return a mutable dump of a valid bundle page with optional overrides., Return valid single-page object provenance., Graph boxes and polygons must name a known page coordinate space., Non-empty baselines require an explicit baseline coordinate space id., Baseline coordinate spaces must resolve to a known page space., Every line listed by a region must claim that region as parent. (+16 more)

### Community 30 - "SourceAcquisitionService"
Cohesion: 0.24
Nodes (20): pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe(), test_image_bounds_must_overlap_most_of_page_area(), test_image_folder_records_image_set_source_type() (+12 more)

### Community 31 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 32 - "_RateAccumulator"
Cohesion: 0.10
Nodes (20): _facet_match(), _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:…, Score footnote-marker retention when gold carries that role. Args: gold_span:…, Emit partial collapse when weight and slant XOR-match. Fires only when both…, Score one enum typography facet when gold is known. Args: rate: Target…, Score small-caps or letter-spacing when gold is known. Args: rate: Target… (+12 more)

### Community 33 - "ReviewOverlayService"
Cohesion: 0.06
Nodes (39): MonkeyPatch, Replay of frozen fixture events must equal fixture current_state., Successor copies resolvable events only and keeps conflict packets., Successor remaps nested region and line ids on a copied split event., Corrupt split dump shapes must raise ValueError, not shrink regions., test_overlay_v1_fixture_replay_matches_current_state(), test_successor_rebases_only_resolved_events_and_queues_conflicts(), test_successor_rebases_split_region_nested_ids() (+31 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.15
Nodes (31): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+23 more)

### Community 35 - "PageEvaluationSummary"
Cohesion: 0.11
Nodes (24): _flag(), Return a minimal evaluation flag for queue fixtures., test_adjudication_excludes_page_id_from_related_object_ids(), test_blank_target_object_id_routes_to_adjudication(), test_build_review_tasks_preserves_dimension_specific_coverage(), test_note_linkage_marker_only_flags_collapse_to_adjudication(), EvaluationFamilySummary, EvaluationFlag (+16 more)

### Community 36 - "models/__init__.py"
Cohesion: 0.05
Nodes (101): Alternate merge interpretations live in provenance, not duplicate nodes., test_object_provenance_accepts_alternate_candidates(), _event_base(), _polygon(), datetime, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is… (+93 more)

### Community 37 - "File map"
Cohesion: 0.13
Nodes (14): Done criteria (from spec), File map, Rename `bochord` → `wordwending` Implementation Plan, Task 10: GitHub rename + URL sweep, Task 11: Operator checklist (human), Task 1: Branch, Task 2: Move package directory, Task 3: Mechanical replace (in-scope only) (+6 more)

### Community 38 - "test_ocr_models.py"
Cohesion: 0.06
Nodes (29): Prepared-unit identifiers must be unique on one prepared page., Prepared units must belong to the prepared page and known spaces., Return a valid preparation-recipe payload with optional overrides., Return Pydantic-generated JSON Schema with stable key ordering. Args:…, Frozen document-bundle-v1.json must validate and dump identically., Frozen rag-document-v1.json must validate and dump identically., DocumentBundle JSON Schema must match the checked-in generated snapshot., RagDocument JSON Schema must match the checked-in generated snapshot. (+21 more)

### Community 39 - "Rename `bochord` → `wordwending` Design"
Cohesion: 0.17
Nodes (11): Done Criteria, Execution Order, Identity Map, In Scope, Locked Decisions, Non-Goals (Ponytail), Out of Scope, Purpose (+3 more)

### Community 40 - "RunnerInputPackager"
Cohesion: 0.28
Nodes (17): bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests., test_direct_packaging_references_original_artifact(), test_direct_packaging_rejects_multi_item_batch() (+9 more)

### Community 41 - "._coords"
Cohesion: 0.13
Nodes (10): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered… (+2 more)

### Community 42 - "RunnerBatchPlanner"
Cohesion: 0.15
Nodes (27): Persisted batch status must agree with submitted and failed items., Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), test_spec_0013_runner_invariants_reject_invalid_payloads(), artifacts(), capability(), policy() (+19 more)

### Community 43 - "cli"
Cohesion: 0.13
Nodes (16): group, _dense_two_column_image(), Image, Path, Test the prepare command., Test prepare aborts before writes when override lacks a reason., Test the export command., Export writes Spec 0006 derived artifacts under exports/. (+8 more)

### Community 44 - "PageClass"
Cohesion: 0.09
Nodes (45): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+37 more)

### Community 45 - "Settings"
Cohesion: 0.16
Nodes (13): BaseSettings, PydanticBaseSettingsSource, patch, Test the run command., _run_cli_args(), TestCLIRun, Test loading configuration with TOML file., Path (+5 more)

### Community 46 - "Path"
Cohesion: 0.14
Nodes (21): MockerFixture, binary_recipe(), bundle_service(), dense_two_column_image(), Path, Write a single-page source raster for bundle tests. Returns: Path to a…, Write a two-page image folder for multi-page bundle tests. Returns: Path to a…, Build a preparation bundle service wired to ``acquisition``. Args: acquisition:… (+13 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.05
Nodes (27): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events. (+19 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.18
Nodes (13): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy, Hugging Face Deployment Target (+5 more)

### Community 50 - "_rag_chunk"
Cohesion: 0.07
Nodes (46): _minimal_rag_document(), _rag_chunk(), Return multi-page retrieval provenance with stable witness pointers., Return a page-local retrieval chunk with optional field overrides., Return a cross-page stitched chunk with optional field overrides., Return a document-level RAG export with optional chunk overrides., Page-local chunk ids must stay unique within a RagDocument., Stitched chunk ids must stay unique within a RagDocument. (+38 more)

### Community 51 - "MergeOrchestrator"
Cohesion: 0.11
Nodes (16): MergeOrchestrator, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph…, Choose the accepted prepared page variant for this merge., Keep same-variant witnesses and record skipped cross-variant evidence., Pick one coordinate-rich structure scaffold and detect layout conflicts., Record insufficient evidence when no layout scaffold is available., Compare other witnesses against the chosen scaffold and flag conflicts. Args:… (+8 more)

### Community 52 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 53 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling., TestPrintInfo, print_info(), print_success(), Print success message. Args: message: Success message (+1 more)

### Community 54 - "main"
Cohesion: 0.23
Nodes (8): patch, Tests for the main module., Test the main function., Test that main function calls the CLI., Test that main function can be imported and called., Test that main function exists and is callable., TestMain, main()

### Community 55 - "DocumentRunOrchestrator"
Cohesion: 0.15
Nodes (13): ADR 0001 Package Boundary, Acquire-Prepare-Pass-Align-Evaluate-Review-Export Workflow, ADR 0005 Evaluation First, Separate Evaluation Score Families, Spec 0001 System Architecture, BundleWriter, DocumentRunOrchestrator, EvaluationService (+5 more)

### Community 56 - "i-mutation / i-umlaut"
Cohesion: 0.23
Nodes (13): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+5 more)

### Community 57 - "conftest.py"
Cohesion: 0.21
Nodes (12): cli_context(), mock_console(), mock_settings(), fixture, Test configuration and fixtures for the ai-coding project. This file contains…, Create a CLI runner for testing., Create a temporary directory for testing., Create a mock console for testing. (+4 more)

### Community 58 - "print_error"
Cohesion: 0.21
Nodes (8): Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError, print_error(), Print error message with optional suggestions. Args: message: Error message…

### Community 59 - "test_preparation_service.py"
Cohesion: 0.17
Nodes (35): dense_source_page(), preparation_service(), MonkeyPatch, parametrize, Build the default page-preparation service for tests. Returns: Page preparation…, Build a source-page artifact backed by a written PNG. Keyword Args: dpi:…, Build a two-column dense dictionary source page on disk. Returns: Source page…, Index quality signals by ``signal_id``. Args: signals: Measured quality signals… (+27 more)

### Community 60 - "Preparation Gold Specs"
Cohesion: 0.17
Nodes (12): V1 Gold Data Expectations, Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Coordinate and Image Provenance, Page Subdivision into OCR Units, Preparation Pipeline Stage, Preparation Recipe, V1 Page Class Taxonomy (+4 more)

### Community 61 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 62 - "create_progress"
Cohesion: 0.22
Nodes (8): Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress, create_progress(), Create a rich progress indicator for long-running operations. Returns:…

### Community 63 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.25
Nodes (8): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, V1 Typography and Role Vocabulary, Evidence-Bound Human Review, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence, Reject eScriptorium as Review Boundary, PAGE Region/Line Reuse Boundary

### Community 64 - "Diplomatic Text Review"
Cohesion: 0.20
Nodes (10): Review Overlays, Diplomatic Text Review, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Historical Character Preservation, Retrieval Convenience Text Fields, Spec 0014: Review Task and Overlay Schema, correct_text Event Semantics (+2 more)

### Community 65 - "Coding Standards Docs"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 66 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 67 - "ReviewTask"
Cohesion: 0.14
Nodes (13): Self-contained instructions and evidence binding for human review., ReviewTask, Build a span-scoped diplomatic-text review task packet. Task identity is scoped…, Build a region-scoped layout/structure review task packet. Split and merge work…, Build a span-scoped typography review task packet. Typography certification is…, Build a note-scoped linkage review task packet. Primary targets are note ids.…, Build a page-scoped preparation / subdivision task packet. Args: page: Accepted…, Build a page-scoped adjudication task for empty or unknown flag targets. Args:… (+5 more)

### Community 68 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.22
Nodes (9): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+1 more)

### Community 69 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 70 - "README, Operator Docs, and Thin Export CLI Implementation Plan"
Cohesion: 0.15
Nodes (12): Acceptance Checks, Deferred (explicitly not this plan), File Map, Global Constraints, Locked Decisions (from grilling), Plan Self-Review, README, Operator Docs, and Thin Export CLI Implementation Plan, Task 1: Thin `export` CLI (TDD) (+4 more)

### Community 72 - "Normalized Page Graph"
Cohesion: 0.29
Nodes (8): Normalized Page Graph, Footnote Chunk, Spec 0011: Structured Output Strategy, Standard OCR Intermediate Structure, TEI Dictionaries Chapter, TEI P5 as Downstream Reference, Domain Language, Shared Domain Glossary

### Community 73 - "Configuration: Command Line Tool"
Cohesion: 0.39
Nodes (8): Configuration: Command Line Tool, CLI Configuration Cascade, Frequently Asked Questions, Installation, Python 3.10+ Installation, Quickstart Guide, Quickstart CLI Entry Points, Using the Command Line Interface

### Community 74 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 75 - "TestCLIVersion"
Cohesion: 0.25
Nodes (5): Test the version command., Test the version command displays version information., Test the version command with verbose flag., Test the version command with quiet flag., TestCLIVersion

### Community 76 - "._normalize_text"
Cohesion: 0.13
Nodes (8): Normalize span diplomatic text without note-marker rewriting. Args:…, Normalize note diplomatic text, including note-marker policy. Args:…, Return a span copy with ``text_normalized`` regenerated. Args: span: Accepted…, Return a note copy with ``text_normalized`` regenerated. Args: note: Accepted…, Normalize every span and note while leaving diplomatic text unchanged. Args:…, Apply policy-ordered Unicode, whitespace, and optional marker rules. Args:…, Map known superscript codepoints when flattening is enabled. Args: text: Text…, Replace documented marker codepoints when placeholder mode is enabled. Args:…

### Community 77 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 78 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 79 - "MergePolicy"
Cohesion: 0.06
Nodes (110): _aligned_text_witnesses(), _bounding_box(), _line(), _load_merge_fixture(), _prepared_page(), Empty precedence with differing text flags disagreement and abstains., When multiple IoU-matched spans share a preferred runner, the first wins., Return a minimal prepared page shared by merge tests. (+102 more)

### Community 80 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Overlay Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 81 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.33
Nodes (6): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Abstaining Merge Policy, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts

### Community 82 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 83 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 84 - "Spec 0016 RAG Line Contract Follow-up Implementation Plan"
Cohesion: 0.22
Nodes (8): Acceptance Checks, Exact Invariant Matrix, File Map, Global Constraints, Plan Self-Review, Spec 0016 RAG Line Contract Follow-up Implementation Plan, Task 1: Specify and Enforce Intrinsic RAG Line Invariants, Task 2: Regenerate Schema and Prove Frozen Export Compatibility

### Community 85 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 86 - "test_merge_service.py"
Cohesion: 0.18
Nodes (13): _coordinate_space(), _note(), _provenance(), Return coordinate space aligned to the test prepared page., Build one note record for merge tests., Return valid single-page object provenance., PassWitnessPage serializes and validates a runner page graph fragment., test_pass_witness_page_round_trip() (+5 more)

### Community 87 - "valid_bundle_page"
Cohesion: 0.22
Nodes (9): _page_witness(), Return a witness owned by the given page., Document page ids must stay unique., Source page_count must remain exact versus exported pages., Return a minimal valid page graph for join-reference tests., test_bundle_rejects_unknown_line_join_target(), test_document_bundle_rejects_duplicate_page_ids(), test_document_bundle_rejects_inexact_source_page_count() (+1 more)

### Community 88 - "model_runner_payload"
Cohesion: 0.17
Nodes (11): capability_payload(), execution_batch_payload(), model_runner_payload(), parametrize, Return a valid model-backed runner payload with optional overrides., Return a valid runner capability payload with optional overrides., Return a valid runner execution batch payload with optional overrides., Boxes must represent a positive-area rectangle. (+3 more)

### Community 89 - "Sphinx Docs Index"
Cohesion: 0.67
Nodes (4): Changelog, Sphinx Docs Index, README, Read the Docs Config

### Community 90 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 91 - "MockHttpxClient"
Cohesion: 0.29
Nodes (7): MockHttpxClient, Any, BaseException, Response, Minimal httpx client stand-in for hosted runner tests., BatchUnitKind, Batch grouping units for runner execution.

### Community 92 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, field_validator, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…

### Community 93 - "Page Graph Line"
Cohesion: 0.50
Nodes (4): Page Graph Line, Page Graph Note, Page Graph Region, Page Graph Span

### Community 94 - "Phase 1 PAGE Interoperability Spike Plan"
Cohesion: 0.83
Nodes (4): BundlePage Canonical JSON, Phase 1 PAGE Interoperability Spike Plan, PageXmlInterchangeService, Reject ocrd-models for Spike

### Community 95 - "RunnerReference"
Cohesion: 0.50
Nodes (4): Mutable Model Revision Rejection, RunnerCapability, RunnerExecutionBatch, RunnerReference

### Community 96 - "TestConsole"
Cohesion: 0.50
Nodes (3): Test console objects., Test that console objects are properly initialized., TestConsole

### Community 97 - "Chris Malek"
Cohesion: 0.67
Nodes (3): AUTHORS Credits, Chris Malek, MIT License

### Community 98 - "_review_polygon"
Cohesion: 0.29
Nodes (6): Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces., _review_box(), _review_polygon()

### Community 99 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 100 - "_NoteCandidate"
Cohesion: 0.10
Nodes (34): NamedTuple, _apply_note_link_resolution(), _mapped_note_link_sets(), _MarkerMappingContext, _min_merge_confidence(), _note_link_alternates(), _note_marker_links_from_mapped_sets(), _note_marker_links_when_mapping_ambiguous() (+26 more)

### Community 101 - "ADR 0008 Stable IDs and Review History"
Cohesion: 0.67
Nodes (3): ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States

### Community 102 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 113 - "_prepared_unit_ref"
Cohesion: 0.50
Nodes (4): _prepared_unit_ref(), Return a prepared-unit artifact bound to page preparation context., Transform and prepared-unit spaces are valid geometry contexts., test_bundle_page_accepts_known_transform_and_unit_spaces()

### Community 122 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 128 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 129 - "._resolve_context"
Cohesion: 0.25
Nodes (6): Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve assessment, class, and subdivision choices for one page. Args:…, Resolve final page class from automation or operator override. Args: suggested:…, _resolve_page_class(), _signal_value()

### Community 131 - "Spec 0005: Human Markup and Review"
Cohesion: 0.33
Nodes (6): Spec 0005: Human Markup and Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0009: Merge and Alignment, Machine/Merge/Trust Confidence Triad, Structure Scaffold Selection

### Community 135 - "services/merge.py"
Cohesion: 0.03
Nodes (116): _LayoutObject, _object_provenance(), Return valid single-page provenance for programmatic graph tests., Separate region/line/span maps must not overwrite unlike graph records., test_typed_page_indexes_resolve_colliding_ids_by_object_kind(), page(), _provenance(), fixture (+108 more)

### Community 138 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``wordwending run``.

## Ambiguous Edges - Review These
- `README` → `Sphinx Docs Index`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to
- `Frequently Asked Questions` → `Quickstart CLI Entry Points`  [AMBIGUOUS]
  doc/source/overview/faq.rst · relation: conceptually_related_to
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to

## Knowledge Gaps
- **158 isolated node(s):** `release.sh script`, `wordwending`, `IPA_AUDIO`, `Locked Decisions (from grilling)`, `Global Constraints` (+153 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `README` and `Sphinx Docs Index`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Frequently Asked Questions` and `Quickstart CLI Entry Points`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `i-mutation / i-umlaut` and `Ablaut (inherited vowel alternation)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `BundlePage` connect `BundlePage` to `test_document_export.py`, `test_text_normalization.py`, `RagChunk`, `cli.py`, `services/merge.py`, `test_evaluation_service.py`, `MetricProfile`, `model_validator`, `._write_page_evaluation_and_manifest`, `test_bundle_layout.py`, `PageXmlInterchangeService`, `ReviewDimension`, `test_page_interchange.py`, `_RateAccumulator`, `PageEvaluationSummary`, `models/__init__.py`, `test_ocr_models.py`, `._coords`, `MergeOrchestrator`, `ReviewTask`, `._normalize_text`, `MergePolicy`, `test_merge_service.py`, `valid_bundle_page`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `services/preparation.py`, `test_document_export.py`, `test_text_normalization.py`, `RagChunk`, `cli.py`, `BundlePage`, `FlagSeverity`, `services/merge.py`, `test_evaluation_service.py`, `BundleLayoutService`, `MetricProfile`, `PlannedRunnerBatch`, `test_bundle_layout.py`, `BundlePaths`, `SourcePageArtifact`, `PreparationRecipe`, `PageEvaluationSummary`, `RunnerBatchPlanner`, `PageClass`, `ReviewTask`, `MergePolicy`, `test_merge_service.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `TestCLIGlobalOptions`, `cli.py`, `cli`, `TestCLIVersion`, `TestCLIErrorHandling`, `TestCLISettings`, `TestConfiguration`, `TestCLIEval`, `.validate_https_huggingface_endpoints`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 94 inferred relationships involving `AlternateCandidate` (e.g. with `BundlePage` and `CoordinateSpace`) actually correct?**
  _`AlternateCandidate` has 94 INFERRED edges - model-reasoned connections that need verification._