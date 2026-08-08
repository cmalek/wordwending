# Graph Report - wordwending  (2026-08-07)

## Corpus Check
- 199 files · ~245,847 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4154 nodes · 11575 edges · 166 communities (145 shown, 21 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1182 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `73a5ef06`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/preparation.py
- MergeOrchestrator
- test_text_normalization.py
- models/__init__.py
- model_validator
- _NoteCandidate
- DocumentRunOrchestrator
- load_minimal_bundle
- test_evaluation_service.py
- Detailed OCR Process
- test_assemble_manifest.py
- EndpointSessionLedgerStore
- test_kraken_runner.py
- PlannedRunnerBatch
- RunnerBatchPlanner
- test_document_export.py
- test_olmocr_runner.py
- ADR 0010 Structured Output Boundary
- RunnerExecutionOrchestrator
- BundlePage
- check_napoleon_gate.py
- Path
- test_review_cli.py
- BT Witness Preparation Slice
- TestConfiguration
- PageXmlInterchangeService
- test_graph_rebase.py
- source_acquisition.py
- model_validator
- _rag_chunk
- AlternateCandidate
- Path
- MetricProfile
- .create_successor
- test_runner_execution.py
- BakeoffService
- test_bakeoff.py
- File map
- WitnessAdaptationService
- Rename `bochord` → `wordwending` Design
- RunnerInputPackager
- ._coords
- Spec 0005: Human Markup and Review
- _bundle_page_payload
- test_review_overlay.py
- Settings
- 2026-08-07-v1-spine-and-phase-completion.md
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- test_assemble.py
- PageEvaluationSummary
- ._result_from_response
- test_cli_utils.py
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- test_page_interchange.py
- test_preparation_service.py
- Preparation Gold Specs
- Raw OCR witness layer
- create_progress
- Spec 0002: V1 Bundle Layout and Data Shape
- ResumeLedgerService
- Coding Standards Docs
- test_bundle_layout.py
- EndpointCatalogEntry
- ADR 0009 OCR-D PAGE eScriptorium
- Spec 0006: Exports and Retrieval Views
- README, Operator Docs, and Thin Export CLI Implementation Plan
- test_bundle_checksum.py
- Normalized Page Graph
- Configuration: Command Line Tool
- Anglian dialect group
- Hugging Face Endpoint Lifecycle Design
- Built-in Catalog Policy
- Learner lacks stable conceptual map of sound-change order
- OE Grammar Resources
- MergePolicy
- ADR 0004 Layered Truth
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- PassRunnerRegistry
- Spec 0016 RAG Line Contract Follow-up Implementation Plan
- TestConsoleQuietMode
- TestCLIReview
- Path
- ConfigurationError
- Sphinx Docs Index
- Lesson 0003 Pronouncing Old English Letters
- .apply
- PassRunner
- Page Graph Line
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- test_document_run.py
- .validate_item_page_alignment
- ._package_pdf
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
- EndpointRemoteState
- OCR Evidence Not Philological Semantics
- ADR 0002 Bundle Model
- Page Bundle as Page-Local Truth Unit
- ADR 0003 Page Graph
- SourceProvenanceService
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- File Map
- Mixed dialect spellings from copying history
- Reference Sound Terms
- Assemble eval fixtures
- test_assemble_eval_export_wave_a_exit
- cli
- test_evaluation_cohorts.py
- endpoints_down
- ._write_page_xml
- wordwending
- RagChunk
- TestCLIExport
- cli.py
- HfEndpointClient
- SourceAcquisitionService
- .render_markdown
- SchemaModel
- test_endpoint_lifecycle.py
- RunnerThroughputSummary
- .plan
- print_error
- .settings_customise_sources
- test_live_endpoint_lifecycle_smoke
- File Map
- _provenance
- test_ocr_models.py
- TestPrintSuccess
- test_live_hf_bakeoff_requires_integration_marker
- BundleLayoutService
- ReviewDimension
- page
- Any
- FontWeight
- test_write_document_exports_writes_derived_views
- .validate_https_huggingface_endpoints
- .validate_graph_references
- _PreparedInputsManifest
- endpoints
- review
- test_matrix_cell_schema_includes_required_fields

## God Nodes (most connected - your core abstractions)
1. `BundlePage` - 171 edges
2. `SchemaModel` - 134 edges
3. `AlternateCandidate` - 120 edges
4. `BundleLayoutService` - 96 edges
5. `cli()` - 93 edges
6. `MergePolicy` - 90 edges
7. `CoordinateSpace` - 89 edges
8. `PreparedPage` - 86 edges
9. `Settings` - 81 edges
10. `PageClass` - 79 edges

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

## Communities (166 total, 21 thin omitted)

### Community 0 - "services/preparation.py"
Cohesion: 0.04
Nodes (106): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _adaptive_binary() (+98 more)

### Community 1 - "MergeOrchestrator"
Cohesion: 0.08
Nodes (21): _flagged_object_ids(), MergeOrchestrator, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Initialize merge orchestration for one page. Args: policy: Versioned merge…, Collect object ids already referenced by merge flags. Args: flags: Merge flags…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph…, Choose the accepted prepared page variant for this merge., Keep same-variant witnesses and record skipped cross-variant evidence. (+13 more)

### Community 2 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (44): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+36 more)

### Community 3 - "models/__init__.py"
Cohesion: 0.05
Nodes (86): EvaluationCohortReport, Fixed cohort views emitted by evaluation aggregation., ChunkType, DatasetSplit, FlagSeverity, _known_page_space_ids(), _known_preparation_space_ids(), PageClass (+78 more)

### Community 4 - "model_validator"
Cohesion: 0.05
Nodes (21): model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Keep page-local page ids aligned with provenance. Returns: The validated page-…, Keep stitched page ids distinct and aligned with provenance. Returns: The…, Keep page-local and stitched retrieval references coherent. Returns: The…, Reject duplicate related ids and overlap with primary targets. Returns: The…, Reject mixed coordinate-space identity when both geometry forms are present.… (+13 more)

### Community 5 - "_NoteCandidate"
Cohesion: 0.11
Nodes (33): NamedTuple, _apply_note_link_resolution(), _map_marker_span_ids(), _mapped_note_link_sets(), _MarkerMappingContext, _min_merge_confidence(), _note_link_alternates(), _note_marker_links_from_mapped_sets() (+25 more)

### Community 6 - "DocumentRunOrchestrator"
Cohesion: 0.11
Nodes (26): DocumentRunConfig, Return whether gold and metric profile enable default eval. Returns: ``True``…, Configuration for one orchestrated document run., Return the stage order for this run. Returns: Explicit ``stages`` when set;…, Return the default machine path before ``skip_export`` filtering. Returns:…, DocumentRunOrchestrator, _DocumentRunState, _load_json_model() (+18 more)

### Community 7 - "load_minimal_bundle"
Cohesion: 0.05
Nodes (59): _accept_review_event(), load_minimal_bundle(), Path, Duplicate page_number values must fail before silent page overwrite., source_files keys must be bare basenames, not path segments., page_exports basenames must not escape the page exports directory., Append inserts a separator when prior JSONL lacks a trailing newline., Heal must not UnicodeDecodeError when prior JSONL ends on multi-byte UTF-8. (+51 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.05
Nodes (92): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+84 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "test_assemble_manifest.py"
Cohesion: 0.12
Nodes (37): _acquisition(), _bibliographic(), _build(), _load_batch(), _merge_policy(), Path, Single succeeded run yields one page with one copied witness., Two runner runs merge into one page with two witnesses. (+29 more)

### Community 11 - "EndpointSessionLedgerStore"
Cohesion: 0.11
Nodes (29): Path, test_corrupt_ledger_loads_empty(), test_ledger_round_trip(), test_mark_down_records_pause_action(), test_missing_ledger_loads_empty(), test_save_persists_ledger(), test_touch_rejects_invalid_action(), test_touch_replaces_same_runner_id() (+21 more)

### Community 12 - "test_kraken_runner.py"
Cohesion: 0.13
Nodes (39): hosted_runner(), kraken_response(), mock_client(), planned_batch(), policy(), policy_with_endpoint(), Any, BaseException (+31 more)

### Community 13 - "PlannedRunnerBatch"
Cohesion: 0.04
Nodes (96): LookupError, MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., Raised when a hosted runner endpoint is not ready for inference., RunnerEndpointUnavailable, BatchItemRef (+88 more)

### Community 14 - "RunnerBatchPlanner"
Cohesion: 0.23
Nodes (22): Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), artifacts(), capability(), policy(), _prepared_unit(), Return a default multi-item runner capability with optional overrides. (+14 more)

### Community 15 - "test_document_export.py"
Cohesion: 0.06
Nodes (47): _body_region_page(), _load_frozen_document_bundle_v1(), _load_minimal_bundle(), _merge_page_regions(), _page_provenance(), _page_witness(), _prepared_page(), Bold+italic spans use ***text*** with bold outside italic. (+39 more)

### Community 16 - "test_olmocr_runner.py"
Cohesion: 0.15
Nodes (38): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+30 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "RunnerExecutionOrchestrator"
Cohesion: 0.07
Nodes (29): Persisted batch status must agree with submitted and failed items., Exact persisted record for one runner invocation., RunnerExecutionBatch, _atomic_write_text(), _derive_result_status(), datetime, Path, Bind collaborators and run identifiers for one execution segment. Keyword Args:… (+21 more)

### Community 19 - "BundlePage"
Cohesion: 0.05
Nodes (68): _eval_flag(), _page_with_text_flags(), parametrize, Return one evaluation flag with an explicit merge flag_type., Attach evaluation flags onto the text family only (legacy C3 shape)., Known merge flag types become Spec 0005 dimension packets even if mis-bucketed., Every MergeFlagType has a Spec 0005 dimension mapping entry., Note-scoped text disagreement has no Spec 0005 text packet; use adjudication. (+60 more)

### Community 20 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 21 - "Path"
Cohesion: 0.07
Nodes (21): Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page…, Return the page evaluation scores artifact path. Args: page_number: 1-based… (+13 more)

### Community 22 - "test_review_cli.py"
Cohesion: 0.09
Nodes (52): _eval_flag(), _gold_task(), _overlay_with_tasks(), Path, Return a span-scoped text review task for validation fixtures., Return a gold task packet (unsupported by review apply)., Return a minimal PageOverlay carrying the given review tasks., Return one evaluation flag for pending-task regeneration fixtures. (+44 more)

### Community 23 - "BT Witness Preparation Slice"
Cohesion: 0.05
Nodes (42): ExtractionOrchestrator, Project Structure (models/services/cli/settings), Single Responsibility Service Architecture, Dual Text Contract, Historical Character Preservation, LineJoinRecord, text-norm-v1 Policy, TextNormalizer (+34 more)

### Community 24 - "TestConfiguration"
Cohesion: 0.06
Nodes (22): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+14 more)

### Community 25 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 26 - "test_graph_rebase.py"
Cohesion: 0.07
Nodes (54): _GraphNode, _page(), _provenance(), Text overrides rewrite span diplomatic text by object_id + scope., Text overrides rewrite note diplomatic text by object_id + scope., Typography and role overrides update the matching span., Unknown object_id raises ValueError naming the id., Returned page carries the caller-supplied graph_revision. (+46 more)

### Community 27 - "source_acquisition.py"
Cohesion: 0.10
Nodes (32): PdfPage, _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), _pdf_page_image(), Image (+24 more)

### Community 28 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 29 - "_rag_chunk"
Cohesion: 0.07
Nodes (46): _minimal_rag_document(), _rag_chunk(), Return multi-page retrieval provenance with stable witness pointers., Return a page-local retrieval chunk with optional field overrides., Return a cross-page stitched chunk with optional field overrides., Return a document-level RAG export with optional chunk overrides., Page-local chunk ids must stay unique within a RagDocument., Stitched chunk ids must stay unique within a RagDocument. (+38 more)

### Community 30 - "AlternateCandidate"
Cohesion: 0.02
Nodes (170): _LayoutObject, _markdown_style_page(), _object_provenance(), Return valid single-page provenance for programmatic graph tests., Separate region/line/span maps must not overwrite unlike graph records., Build one page exercising markdown style, regions, and footnote linkage., test_typed_page_indexes_resolve_colliding_ids_by_object_kind(), page() (+162 more)

### Community 31 - "Path"
Cohesion: 0.13
Nodes (19): _export_note_page(), Path, Export should round PAGE coordinates to importer-friendly integers., PAGE corrections should update text while sidecar evidence stays intact., PAGE diplomatic corrections should regenerate normalized span text., Import should fail when PAGE XML drops a canonical region id., Import should fail when PAGE XML repeats a canonical line id., Import should fail when corrected PAGE points at a different image identity. (+11 more)

### Community 32 - "MetricProfile"
Cohesion: 0.07
Nodes (32): test_metric_profile_rejects_invalid_iou_threshold(), MetricProfile, BaseModel, Versioned, deterministic evaluation policy., _NoteLinkageScorer, _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:… (+24 more)

### Community 33 - ".create_successor"
Cohesion: 0.06
Nodes (32): _identity_object_id_map(), ReviewEvent, Build an ADR 0008 successor overlay bound to ``new_graph_revision``. Leaf-only…, Build an identity object-id map for leaf-only graph rebase. Args: page: Rebased…, _coordinate_space_ids(), _nested_object_ids(), _normalize_tasks(), ReviewEvent (+24 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.13
Nodes (39): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+31 more)

### Community 35 - "BakeoffService"
Cohesion: 0.09
Nodes (38): Failed invocations populate failure and omit score families., test_run_records_failure_without_score_families(), BakeoffCandidate, BakeoffInvocationOutcome, BakeoffMatrix, BakeoffMatrixCell, BakeoffPageCase, BakeoffPredictionRef (+30 more)

### Community 36 - "test_bakeoff.py"
Cohesion: 0.13
Nodes (29): _box(), _gold(), _prediction(), profile(), Path, Build one gold page annotation matching the prediction span., Schema defaults name real ADR 0007 candidates, not FakePassRunner., Harness scores recorded (mocked) responses for both real candidates. (+21 more)

### Community 37 - "File map"
Cohesion: 0.13
Nodes (14): Done criteria (from spec), File map, Rename `bochord` → `wordwending` Implementation Plan, Task 10: GitHub rename + URL sweep, Task 11: Operator checklist (human), Task 1: Branch, Task 2: Move package directory, Task 3: Mechanical replace (in-scope only) (+6 more)

### Community 38 - "WitnessAdaptationService"
Cohesion: 0.08
Nodes (45): _coordinate_space(), _prepared_page(), Path, Adapted span ids and texts match assemble gold-v1 target_object_ids., Empty artifact_paths list is rejected before reading., Non-chat.completion JSON is rejected as an invalid raw witness., Write a minimal chat.completion witness artifact for adaptation tests., Wrong JSON field types surface as ValueError, not TypeError. (+37 more)

### Community 39 - "Rename `bochord` → `wordwending` Design"
Cohesion: 0.17
Nodes (11): Done Criteria, Execution Order, Identity Map, In Scope, Locked Decisions, Non-Goals (Ponytail), Out of Scope, Purpose (+3 more)

### Community 40 - "RunnerInputPackager"
Cohesion: 0.28
Nodes (17): bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests., test_direct_packaging_references_original_artifact(), test_direct_packaging_rejects_multi_item_batch() (+9 more)

### Community 41 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 42 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0009: Merge and Alignment (+3 more)

### Community 43 - "_bundle_page_payload"
Cohesion: 0.10
Nodes (20): _bundle_page_payload(), Return a mutable dump of a valid bundle page with optional overrides., Graph boxes and polygons must name a known page coordinate space., Non-empty baselines require an explicit baseline coordinate space id., Baseline coordinate spaces must resolve to a known page space., Every line listed by a region must claim that region as parent., Every span listed by a line must claim that line as parent., Every note listed by a region must claim that region as parent. (+12 more)

### Community 44 - "test_review_overlay.py"
Cohesion: 0.06
Nodes (62): _event_base(), _polygon(), datetime, MonkeyPatch, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is…, Replay builds OverlayState solely from ordered append-only events. (+54 more)

### Community 45 - "Settings"
Cohesion: 0.12
Nodes (33): configured_settings(), ExplodingEndpointLifecycleService, fake_service(), FakeEndpointLifecycleService, datetime, fixture, patch, Path (+25 more)

### Community 46 - "2026-08-07-v1-spine-and-phase-completion.md"
Cohesion: 0.06
Nodes (35): ADR Alignment (locked — do not silently invert), Execution Handoff, File Map, Global Constraints, Locked Decisions, Optional later plan (NOT this plan), Spec 0004 Completion Matrix (honest), Subagent Model Policy (+27 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.04
Nodes (33): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a valid review geometry bounding box., Return a minimal text-review task bound to the overlay defaults. (+25 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.15
Nodes (15): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Evidence-Bound Human Review, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy (+7 more)

### Community 50 - "test_assemble.py"
Cohesion: 0.13
Nodes (43): _acquisition(), _bibliographic(), _coordinate_space(), _merge_policy(), _MergeWithExtraFlags, _orchestrator(), _prepared_page(), Path (+35 more)

### Community 51 - "PageEvaluationSummary"
Cohesion: 0.14
Nodes (27): test_evaluation_cohort_models_accept_fixed_report_shape(), test_page_evaluation_record_carries_comparison_context(), BakeoffPageRef, Filesystem reference to one bake-off page gold annotation., EvaluationCohortKey, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context. (+19 more)

### Community 52 - "._result_from_response"
Cohesion: 0.15
Nodes (14): _encode_png_base64(), _load_direct_image(), _load_image_from_pdf(), Image, Path, Response, Open one direct image input as RGB. Args: image_path: Packaged image artifact…, Classify one hosted response and persist a witness on success. Keyword Args:… (+6 more)

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
Cohesion: 0.17
Nodes (14): Config, cli_context(), mock_console(), mock_settings(), fixture, pytest_configure(), Register custom markers used by optional live/external tests., Create a CLI runner for testing. (+6 more)

### Community 58 - "test_page_interchange.py"
Cohesion: 0.21
Nodes (15): _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids. (+7 more)

### Community 59 - "test_preparation_service.py"
Cohesion: 0.09
Nodes (66): MockerFixture, binary_recipe(), bundle_service(), dark_gutter_image(), dense_source_page(), dense_two_column_image(), note_heavy_image(), preparation_service() (+58 more)

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
Cohesion: 0.18
Nodes (11): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Review Overlays, V1 Typography and Role Vocabulary, Spec 0014: Review Task and Overlay Schema, correct_text Event Semantics, PageOverlay Append-Only Log, ReviewTask Packet (+3 more)

### Community 64 - "ResumeLedgerService"
Cohesion: 0.11
Nodes (22): Path, test_corrupt_ledger_is_treated_as_empty(), test_missing_ledger_is_empty(), test_record_completed_persists_and_reloads(), test_record_completed_replaces_same_batch_id(), One successfully completed runner batch recorded for resume., Persisted set of successfully completed runner batches under a bundle., ResumeLedger (+14 more)

### Community 65 - "Coding Standards Docs"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 66 - "test_bundle_layout.py"
Cohesion: 0.05
Nodes (63): Multiple source/pages/NNNN.* files must not silently pick one., test_bundle_paths_match_spec_0002_layout(), test_document_bundle_manifest_rejects_non_positive_page_count(), test_document_bundle_manifest_round_trip(), test_page_bundle_manifest_rejects_non_positive_page_number(), test_page_bundle_manifest_round_trip(), test_page_dir_name_is_zero_padded(), test_resolve_source_image_path_rejects_ambiguous_extensions() (+55 more)

### Community 67 - "EndpointCatalogEntry"
Cohesion: 0.16
Nodes (15): test_catalog_entry_rejects_mutable_revision(), test_default_catalog_includes_olmocr_and_kraken(), test_default_catalog_revisions_are_immutable(), test_mutable_revision_rejected(), test_settings_idle_and_ledger_defaults(), default_endpoint_catalog(), EndpointCatalogEntry, mutable_revision_rejected() (+7 more)

### Community 68 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.22
Nodes (9): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+1 more)

### Community 69 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 70 - "README, Operator Docs, and Thin Export CLI Implementation Plan"
Cohesion: 0.15
Nodes (12): Acceptance Checks, Deferred (explicitly not this plan), File Map, Global Constraints, Locked Decisions (from grilling), Plan Self-Review, README, Operator Docs, and Thin Export CLI Implementation Plan, Task 1: Thin `export` CLI (TDD) (+4 more)

### Community 71 - "test_bundle_checksum.py"
Cohesion: 0.08
Nodes (33): Path, Document source digests are omitted from verification when not recorded., Prepared units without recorded digests are skipped honestly., Materialize a minimal bundle whose recorded digests match on-disk bytes., Recorded digests that match on-disk bytes report OK., Tampered prepared image bytes report FAIL against the recorded digest., _sha256_label(), test_verify_matching_checksums_ok() (+25 more)

### Community 72 - "Normalized Page Graph"
Cohesion: 0.29
Nodes (8): Normalized Page Graph, Footnote Chunk, Spec 0011: Structured Output Strategy, Standard OCR Intermediate Structure, TEI Dictionaries Chapter, TEI P5 as Downstream Reference, Domain Language, Shared Domain Glossary

### Community 73 - "Configuration: Command Line Tool"
Cohesion: 0.39
Nodes (8): Configuration: Command Line Tool, CLI Configuration Cascade, Frequently Asked Questions, Installation, Python 3.10+ Installation, Quickstart Guide, Quickstart CLI Entry Points, Using the Command Line Interface

### Community 74 - "Anglian dialect group"
Cohesion: 0.25
Nodes (8): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues

### Community 75 - "Hugging Face Endpoint Lifecycle Design"
Cohesion: 0.11
Nodes (17): Architecture, Catalog, CLI, Decisions (locked in brainstorming), Docs / honesty, Error handling, Goals, Hugging Face Endpoint Lifecycle Design (+9 more)

### Community 76 - "Built-in Catalog Policy"
Cohesion: 0.12
Nodes (15): Built-in Catalog Policy, Execution Handoff, File Map, Global Constraints, HF Endpoint Lifecycle Implementation Plan, Locked Settings Names, Spec Coverage (self-check), Subagent Model Policy (locked) (+7 more)

### Community 77 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 78 - "OE Grammar Resources"
Cohesion: 0.29
Nodes (7): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods, Wright and Wright Old English Grammar

### Community 79 - "MergePolicy"
Cohesion: 0.06
Nodes (115): _aligned_text_witnesses(), _bounding_box(), _coordinate_space(), _line(), _load_merge_fixture(), _note(), _prepared_page(), _provenance() (+107 more)

### Community 80 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Overlay Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 81 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.33
Nodes (6): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Historical Character Preservation, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts

### Community 82 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 83 - "PassRunnerRegistry"
Cohesion: 0.18
Nodes (9): PassRunnerClass, test_register_overrides_or_adds_runner_id(), test_resolve_unknown_runner_id_fails_clearly(), PassRunnerRegistry, Resolve hosted ``PassRunner`` adapter classes by stable ``runner_id``. Defaults…, Bind known runner classes for resolution. Args: runners: Optional mapping of…, Stable runner ids currently registered. Returns: Frozen set of registered…, Register or replace one constructable ``PassRunner`` class. Args: runner_id:… (+1 more)

### Community 84 - "Spec 0016 RAG Line Contract Follow-up Implementation Plan"
Cohesion: 0.22
Nodes (8): Acceptance Checks, Exact Invariant Matrix, File Map, Global Constraints, Plan Self-Review, Spec 0016 RAG Line Contract Follow-up Implementation Plan, Task 1: Specify and Enforce Intrinsic RAG Line Invariants, Task 2: Regenerate Schema and Prove Frozen Export Compatibility

### Community 85 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 86 - "TestCLIReview"
Cohesion: 0.17
Nodes (9): Test review apply and materialize commands., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends overlay events and materializes current_state.json., Re-applying the same overlay must not rewrite prior JSONL bytes., Materialize replays JSONL history into current_state.json., Apply fails when --page-id does not match the overlay file., Apply fails when overlay tasks reference ids absent from the page., Materialize fails when the bundle has no matching page id. (+1 more)

### Community 87 - "Path"
Cohesion: 0.08
Nodes (23): Path, inspect-bundle does not list export paths until export has run., inspect-bundle lists exports/* paths after assemble and export., inspect-bundle prints document and page summary., inspect-bundle surfaces OK after assemble seals prepared-image digests., inspect-bundle surfaces OK when layout digests match on-disk bytes., inspect-bundle prints merge flags after multi-witness disagreement., Assemble fails when manifest witness paths are absent under bundle_root. (+15 more)

### Community 88 - "ConfigurationError"
Cohesion: 0.09
Nodes (26): test_overlay_endpoints_merges_runner_urls_immutably(), build_endpoint_lifecycle_service(), ensure_and_overlay_settings(), Construct an ``EndpointLifecycleService`` from effective settings. Args:…, Pause idle endpoints, ensure runners ready, and overlay HTTPS URLs. Args:…, ConfigurationError, EndpointLifecycleError, FileError (+18 more)

### Community 89 - "Sphinx Docs Index"
Cohesion: 0.67
Nodes (4): Changelog, Sphinx Docs Index, README, Read the Docs Config

### Community 90 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 91 - ".apply"
Cohesion: 0.08
Nodes (19): _bump_graph_revision(), Path, Validate an overlay, append new events, and rewrite overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, Rebuild pending review tasks from one page's evaluation flags. Args:…, Apply overlay corrections onto the page graph and write a successor overlay.…, Ensure overlay task targets exist on the accepted page graph. Validation is…, Validate one review task's targets against the page graph. Args: page: Accepted… (+11 more)

### Community 92 - "PassRunner"
Cohesion: 0.17
Nodes (8): PassRunner, Path, Protocol, Common runtime contract for hosted pass runners. Extracted from…, Frozen execution policy for hosted invocations., Declared input and batching contract for the orchestrator., Verify the hosted endpoint is ready for invocations. Raises:…, Execute one packaged batch against the hosted endpoint. Side Effects: Writes…

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

### Community 98 - "test_document_run.py"
Cohesion: 0.09
Nodes (50): Enum, _absolute_prepare_run_config(), _full_page_preparation_json(), _make_orchestrator(), Any, Path, Write preparation.json under the prepare-tree layout., Copy provenance, merge policy, gold, and metric fixtures into directory. (+42 more)

### Community 99 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 100 - "._package_pdf"
Cohesion: 0.17
Nodes (13): _load_rgb_images(), _page_numbers(), Image, Path, Package one batch using the requested strategy. Args: batch: Planned batch…, Reference one prepared artifact without copying bytes. Args: batch: Single-item…, Return the canonical checksum label for ``payload``. Args: payload: Raw…, Combine prepared images into one PDF runner input. Args: batch: Planned batch… (+5 more)

### Community 101 - "ADR 0008 Stable IDs and Review History"
Cohesion: 0.67
Nodes (3): ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States

### Community 102 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 113 - "EndpointRemoteState"
Cohesion: 0.10
Nodes (15): FakeHfEndpointClient, In-memory ``EndpointClient`` double for lifecycle unit tests., test_fake_satisfies_endpoint_client_protocol(), EndpointRemoteState, Remote Inference Endpoint snapshot from Hugging Face Hub., EndpointClient, Protocol, Scale one endpoint to zero replicas. Args: name: Inference Endpoint name in the… (+7 more)

### Community 122 - "File Map"
Cohesion: 0.12
Nodes (15): Execution Handoff, File Map, Global Constraints, Hands-Off Operator Path Implementation Plan, Locked Decisions, Out of scope, Subagent Model Policy, Task 1: `BundlePage.graph_revision` + AssembleManifestBuilder (TDD) (+7 more)

### Community 128 - "Assemble eval fixtures"
Cohesion: 0.33
Nodes (5): Assemble eval fixtures, Consumers, Files, Fixture pairing (`page-0001`), ID formula (locked)

### Community 129 - "test_assemble_eval_export_wave_a_exit"
Cohesion: 0.47
Nodes (5): Path, Copy witness fixture and prepared image under ``bundle_root``., Assemble page graph scores against assemble gold, then export markdown., _stage_bundle_inputs(), test_assemble_eval_export_wave_a_exit()

### Community 130 - "cli"
Cohesion: 0.05
Nodes (28): Settings output must not expose the raw Hugging Face token., Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format. (+20 more)

### Community 131 - "test_evaluation_cohorts.py"
Cohesion: 0.27
Nodes (13): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+5 more)

### Community 132 - "endpoints_down"
Cohesion: 0.26
Nodes (14): endpoints_down(), endpoints_status(), endpoints_up(), _handle_lifecycle_errors(), command, Context, option, pass_context (+6 more)

### Community 133 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 135 - "RagChunk"
Cohesion: 0.20
Nodes (9): RagChunk, Page-local retrieval chunk., Cross-page retrieval chunk stitched from accepted page-local chunks., StitchedChunk, Build cross-page stitched chunks from contiguous BODY region runs. Args:…, Emit one stitched chunk when a BODY run spans multiple pages. Args:…, Collect ordered distinct page ids from component chunks. Args: chunks: Region…, Union source object ids from component region chunks. Args: chunks: Region… (+1 more)

### Community 137 - "TestCLIExport"
Cohesion: 0.25
Nodes (5): Test the export command., Export writes Spec 0006 derived artifacts under exports/., Export aborts when DocumentBundle JSON fails validation., Export requires --bundle-root., TestCLIExport

### Community 138 - "cli.py"
Cohesion: 0.05
Nodes (74): argument, assemble_document(), _assemble_manifest_from_run(), bakeoff_matrix(), _build_document_run_endpoint_ensurer(), _build_document_run_orchestrator(), _build_document_run_runner_factory(), document_run() (+66 more)

### Community 139 - "HfEndpointClient"
Cohesion: 0.10
Nodes (25): InferenceEndpoint, _FakeInferenceEndpoint, MonkeyPatch, test_constructor_requires_token(), test_create_omits_scale_to_zero_when_disabled(), test_create_passes_catalog_fields_and_scale_to_zero(), test_describe_maps_remote_state(), test_hub_errors_map_to_endpoint_lifecycle_error() (+17 more)

### Community 140 - "SourceAcquisitionService"
Cohesion: 0.21
Nodes (21): pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe(), test_image_bounds_must_overlap_most_of_page_area(), test_image_folder_records_image_set_source_type() (+13 more)

### Community 141 - ".render_markdown"
Cohesion: 0.17
Nodes (6): Render an evidence-preserving Markdown reading view from accepted graphs. Args:…, Map linked marker span ids to owning note ids for one page. Args: page:…, Escape Markdown control characters in diplomatic text. Args: text: Raw…, Escape HTML-special characters in diplomatic text. Args: text: Markdown-escaped…, Render one span with recoverable typography and optional note marker. Args:…, Render one non-body region as an explicit labeled placeholder. Args: region:…

### Community 142 - "SchemaModel"
Cohesion: 0.05
Nodes (107): BundlePage carries graph-v0 by default for overlay binding., Empty artifact group for a page/runner raises zero-witnesses error., test_bundle_page_defaults_graph_revision(), test_raw_witness_ref_zero_artifacts_errors(), _document_bundle(), _minimal_document_bundle(), Wrap accepted pages in a valid multi-page document bundle., Wrap one accepted page in a valid document bundle. (+99 more)

### Community 143 - "test_endpoint_lifecycle.py"
Cohesion: 0.30
Nodes (17): _assert_is_endpoint_client(), _catalog(), Path, _service(), _settings(), test_down_pauses_by_default_delete_flag_destroys(), test_ensure_up_already_running_skips_create_and_resume(), test_ensure_up_creates_missing_and_returns_https_url() (+9 more)

### Community 144 - "RunnerThroughputSummary"
Cohesion: 0.10
Nodes (21): _dense_two_column_image(), Image, patch, Test the document-run command., document-run --help exits zero and documents options., document-run loads config, calls orchestrator, and echoes result., Test the eval command., --force sets force_rerun on the config passed to orchestrator.run. (+13 more)

### Community 145 - ".plan"
Cohesion: 0.20
Nodes (8): _batch_id(), _fixed_chunks(), _grouped_artifacts(), Plan fixed-size runner batches without runtime adaptation. Args: artifacts:…, Reject runs that exceed hosted item or cost caps before planning output. Args:…, Derive a stable batch identifier from policy, artifacts, and ordinal. Args:…, Group artifacts for page-local batching when required. Args: artifacts: Ordered…, Split artifacts into fixed-size chunks preserving order. Args: artifacts:…

### Community 146 - "print_error"
Cohesion: 0.21
Nodes (8): Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError, print_error(), Print error message with optional suggestions. Args: message: Error message…

### Community 147 - ".settings_customise_sources"
Cohesion: 0.22
Nodes (6): BaseSettings, PydanticBaseSettingsSource, Path, Load settings from file with cascading configuration. Args: settings_cls:…, Resolve the endpoint session ledger path. Returns: Configured ledger path or…, Get list of configuration file paths that were loaded. Use this for debugging.…

### Community 149 - "File Map"
Cohesion: 0.13
Nodes (14): DocumentRunOrchestrator Implementation Plan, Execution Handoff, File Map, Global Constraints, Locked Decisions, Out of scope (next plans, not this one), Subagent Model Policy, Task 1: DocumentRunConfig models (TDD) (+6 more)

### Community 150 - "_provenance"
Cohesion: 0.25
Nodes (7): _page_witness(), _provenance(), Graph parent-child identifiers must resolve within the page., Return valid single-page object provenance., Return a witness owned by the given page., Existing provenance fixtures stay valid without alternate candidates., test_object_provenance_defaults_empty_alternate_candidates()

### Community 151 - "test_ocr_models.py"
Cohesion: 0.04
Nodes (54): capability_payload(), execution_batch_payload(), model_runner_payload(), _prepared_unit_ref(), parametrize, Return a prepared-unit artifact bound to page preparation context., Prepared-unit identifiers must be unique on one prepared page., Prepared units must belong to the prepared page and known spaces. (+46 more)

### Community 152 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 153 - "test_live_hf_bakeoff_requires_integration_marker"
Cohesion: 0.67
Nodes (3): integration, Live HF bake-off stays behind pytest.mark.integration (not default suite)., test_live_hf_bakeoff_requires_integration_marker()

### Community 154 - "BundleLayoutService"
Cohesion: 0.09
Nodes (26): load_frozen_document_bundle_v1(), Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the frozen document-bundle-v1 contract fixture., Overlay write before bundle write still records overlay presence., test_write_document_exports_frozen_contract_jsonl_validates(), test_write_overlay_state_creates_manifest_when_missing(), command, option (+18 more)

### Community 155 - "ReviewDimension"
Cohesion: 0.10
Nodes (26): _merge_flag(), Return one merge flag fixture., Assemble projection places each merge flag into its Spec 0005 family., test_project_merge_flags_routes_into_evaluation_families(), MergeFlag, MergeFlagType, StrEnum, One material merge disagreement surfaced for human review. (+18 more)

### Community 156 - "page"
Cohesion: 0.29
Nodes (7): page(), _page_witnesses(), _provenance(), fixture, Return a page graph with regions, spans, and a note for packet targeting., Return minimal provenance for graph fixtures., Return page-local witnesses matching fixture provenance.

### Community 157 - "Any"
Cohesion: 0.47
Nodes (3): Any, BaseException, Response

### Community 158 - "FontWeight"
Cohesion: 0.33
Nodes (5): FontWeight, Visual font-weight classification independent of other typography., _facet_match(), Score one enum typography facet when gold is known. Args: rate: Target…, Compare one non-unknown gold facet to a prediction. Args: gold_value: Gold…

### Community 159 - "test_write_document_exports_writes_derived_views"
Cohesion: 0.50
Nodes (4): load_export_minimal_bundle(), Persisted document exports match renderer output and preserve overlays., Load the compact export-fixture DocumentBundle., test_write_document_exports_writes_derived_views()

### Community 160 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, field_validator, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…

### Community 161 - ".validate_graph_references"
Cohesion: 0.50
Nodes (3): Reject duplicate ids and dangling page-graph references. Returns: The validated…, Require provenance pointers to stay local to the owning page. Args: provenance:…, _validate_object_provenance()

### Community 162 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``wordwending run``.

### Community 163 - "endpoints"
Cohesion: 0.67
Nodes (3): endpoints(), group, Ensure, pause, or inspect Hugging Face Inference Endpoints.

### Community 164 - "review"
Cohesion: 0.67
Nodes (3): group, Apply, materialize, issue, and rebase human review overlays on bundles., review()

## Ambiguous Edges - Review These
- `README` → `Sphinx Docs Index`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to
- `Frequently Asked Questions` → `Quickstart CLI Entry Points`  [AMBIGUOUS]
  doc/source/overview/faq.rst · relation: conceptually_related_to
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to

## Knowledge Gaps
- **240 isolated node(s):** `release.sh script`, `wordwending`, `IPA_AUDIO`, `Locked Decisions (from grilling)`, `Global Constraints` (+235 more)
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
- **Why does `SchemaModel` connect `SchemaModel` to `services/preparation.py`, `test_text_normalization.py`, `models/__init__.py`, `test_evaluation_cohorts.py`, `DocumentRunOrchestrator`, `RagChunk`, `test_evaluation_service.py`, `EndpointSessionLedgerStore`, `PlannedRunnerBatch`, `RunnerThroughputSummary`, `RunnerExecutionOrchestrator`, `BundlePage`, `test_ocr_models.py`, `test_graph_rebase.py`, `ReviewDimension`, `AlternateCandidate`, `MetricProfile`, `BakeoffService`, `test_bakeoff.py`, `test_review_overlay.py`, `Settings`, `PageEvaluationSummary`, `ResumeLedgerService`, `test_bundle_layout.py`, `EndpointCatalogEntry`, `test_bundle_checksum.py`, `MergePolicy`, `test_document_run.py`, `EndpointRemoteState`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `BundlePage` connect `BundlePage` to `MergeOrchestrator`, `test_text_normalization.py`, `models/__init__.py`, `._write_page_xml`, `DocumentRunOrchestrator`, `RagChunk`, `test_evaluation_service.py`, `test_assemble_manifest.py`, `cli.py`, `.render_markdown`, `SchemaModel`, `test_document_export.py`, `_provenance`, `test_ocr_models.py`, `test_review_cli.py`, `PageXmlInterchangeService`, `test_graph_rebase.py`, `ReviewDimension`, `page`, `BundleLayoutService`, `AlternateCandidate`, `MetricProfile`, `.validate_graph_references`, `.create_successor`, `BakeoffService`, `test_bakeoff.py`, `PageEvaluationSummary`, `test_page_interchange.py`, `test_bundle_layout.py`, `MergePolicy`, `.apply`, `test_document_run.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `BundlePaths` connect `test_bundle_layout.py` to `models/__init__.py`, `SchemaModel`, `test_assemble.py`, `Path`, `test_review_cli.py`, `BundleLayoutService`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `BundlePage` (e.g. with `_FakePreparation` and `_FakeRegistry`) actually correct?**
  _`BundlePage` has 30 INFERRED edges - model-reasoned connections that need verification._