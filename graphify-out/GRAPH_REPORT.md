# Graph Report - wordwending  (2026-08-07)

## Corpus Check
- 186 files · ~233,163 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3878 nodes · 10321 edges · 154 communities (133 shown, 21 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 861 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b17a464`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/preparation.py
- MergeOrchestrator
- test_text_normalization.py
- test_merge_review.py
- model_validator
- CoordinateSpace
- SchemaModel
- load_minimal_bundle
- test_evaluation_service.py
- Detailed OCR Process
- test_assemble_manifest.py
- EndpointSessionLedgerStore
- test_kraken_runner.py
- cli.py
- RunnerReference
- BundleLayoutService
- test_olmocr_runner.py
- ADR 0010 Structured Output Boundary
- ConfigurationError
- BundlePage
- check_napoleon_gate.py
- Path
- ReviewTask
- BT Witness Preparation Slice
- TestConfiguration
- PageXmlInterchangeService
- TextRole
- SourcePageArtifact
- PreparationRecipe
- test_ocr_models.py
- ._score_text_pair
- Path
- GoldPageAnnotation
- ReviewOverlayService
- test_runner_execution.py
- test_bakeoff.py
- ._invoke_item
- File map
- WitnessAdaptationService
- Rename `bochord` → `wordwending` Design
- PlannedRunnerBatch
- ._coords
- ._build_task
- services/bakeoff.py
- models/__init__.py
- Settings
- 2026-08-07-v1-spine-and-phase-completion.md
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- test_assemble.py
- PageClass
- cli
- test_cli_utils.py
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- .apply
- test_preparation_service.py
- Preparation Gold Specs
- Raw OCR witness layer
- create_progress
- Spec 0002: V1 Bundle Layout and Data Shape
- ResumeLedgerService
- Coding Standards Docs
- RunnerBatchPlanner
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
- test_merge_service.py
- ADR 0004 Layered Truth
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- TestCLIReview
- Spec 0016 RAG Line Contract Follow-up Implementation Plan
- TestConsoleQuietMode
- HfEndpointClient
- Path
- test_endpoint_lifecycle.py
- Sphinx Docs Index
- Lesson 0003 Pronouncing Old English Letters
- test_pass_runner_registry.py
- .validate_https_huggingface_endpoints
- Page Graph Line
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- ._invoke_item
- .validate_item_page_alignment
- test_page_interchange.py
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
- TestCLIGlobalOptions
- Spec 0005: Human Markup and Review
- test_live_hf_bakeoff_requires_integration_marker
- inspect_bundle
- wordwending
- services/merge.py
- RagChunk
- ._write_page_xml
- EndpointLifecycleService
- TestCLIExport
- review.py
- Path
- .build
- PageEvaluationSummary
- TestCLIErrorHandling
- _review_polygon
- test_live_endpoint_lifecycle_smoke
- test_bundle_layout.py
- ._tasks_from_buckets
- _PreparedInputsManifest
- endpoints
- review
- .__init__

## God Nodes (most connected - your core abstractions)
1. `BundlePage` - 141 edges
2. `SchemaModel` - 130 edges
3. `AlternateCandidate` - 120 edges
4. `cli()` - 83 edges
5. `Settings` - 80 edges
6. `CoordinateSpace` - 77 edges
7. `MergePolicy` - 75 edges
8. `SpanRecord` - 75 edges
9. `PreparedPage` - 74 edges
10. `BundleLayoutService` - 74 edges

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

## Communities (154 total, 21 thin omitted)

### Community 0 - "services/preparation.py"
Cohesion: 0.04
Nodes (109): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., QualitySignal, One measured image-quality signal from preparation assessment., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms() (+101 more)

### Community 1 - "MergeOrchestrator"
Cohesion: 0.05
Nodes (37): _LayoutObject, _apply_layout_merge_confidence(), _attach_alternates_to_objects(), _collect_span_candidates(), _coordinate_rich_line_count(), _first_witness_by_runner_preference(), MergeOrchestrator, Gather matched span candidates from all eligible witnesses. Args:… (+29 more)

### Community 2 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (40): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+32 more)

### Community 3 - "test_merge_review.py"
Cohesion: 0.07
Nodes (43): _eval_flag(), _merge_flag(), _page_with_text_flags(), parametrize, Return one merge flag fixture., Return one evaluation flag with an explicit merge flag_type., Attach evaluation flags onto the text family only (legacy C3 shape)., Known merge flag types become Spec 0005 dimension packets even if mis-bucketed. (+35 more)

### Community 4 - "model_validator"
Cohesion: 0.06
Nodes (17): model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Keep page-local page ids aligned with provenance. Returns: The validated page-…, Keep stitched page ids distinct and aligned with provenance. Returns: The…, Keep page-local and stitched retrieval references coherent. Returns: The…, Reject duplicate related ids and overlap with primary targets. Returns: The…, Require flag events to record concern without changing trust state. Returns:… (+9 more)

### Community 5 - "CoordinateSpace"
Cohesion: 0.03
Nodes (129): _body_region_page(), _load_frozen_document_bundle_v1(), _load_minimal_bundle(), _markdown_style_page(), _merge_page_regions(), _object_provenance(), _page_provenance(), _page_witness() (+121 more)

### Community 6 - "SchemaModel"
Cohesion: 0.07
Nodes (46): Enum, BundlePage carries graph-v0 by default for overlay binding., test_bundle_page_defaults_graph_revision(), FlagSeverity, GoldDocument, _known_page_space_ids(), _known_preparation_space_ids(), PreparedPage (+38 more)

### Community 7 - "load_minimal_bundle"
Cohesion: 0.05
Nodes (59): _accept_review_event(), load_minimal_bundle(), Path, source_files keys must be bare basenames, not path segments., page_exports basenames must not escape the page exports directory., Append inserts a separator when prior JSONL lacks a trailing newline., Heal must not UnicodeDecodeError when prior JSONL ends on multi-byte UTF-8., Corrupt JSONL lines name the file and line number. (+51 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.07
Nodes (71): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+63 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "test_assemble_manifest.py"
Cohesion: 0.12
Nodes (37): _acquisition(), _bibliographic(), _build(), _load_batch(), _merge_policy(), Path, Single succeeded run yields one page with one copied witness., Two runner runs merge into one page with two witnesses. (+29 more)

### Community 11 - "EndpointSessionLedgerStore"
Cohesion: 0.10
Nodes (32): Path, test_corrupt_ledger_loads_empty(), test_ledger_round_trip(), test_mark_down_records_pause_action(), test_missing_ledger_loads_empty(), test_save_persists_ledger(), test_touch_rejects_invalid_action(), test_touch_replaces_same_runner_id() (+24 more)

### Community 12 - "test_kraken_runner.py"
Cohesion: 0.13
Nodes (40): hosted_runner(), kraken_response(), mock_client(), MockHttpxClient, planned_batch(), policy(), policy_with_endpoint(), Any (+32 more)

### Community 13 - "cli.py"
Cohesion: 0.12
Nodes (22): bakeoff_matrix(), _ensure_catalogued_bakeoff_endpoints(), _huggingface_token(), _overlay_ensure_endpoints(), _prepare_overrides(), Context, pass_context, Score recorded candidate predictions into bakeoff-matrix-v1.json. Thin offline… (+14 more)

### Community 14 - "RunnerReference"
Cohesion: 0.05
Nodes (74): LookupError, Persisted batch status must agree with submitted and failed items., Runner, overlay, and gold contracts should fit the planned workflow., test_packaged_runner_input_rejects_mismatched_item_page_lengths(), test_runner_reference_accepts_immutable_digest_revision(), _invoke_hosted_run(), Construct a hosted runner and execute one run. Keyword Args: runner_cls:…, BatchItemRef (+66 more)

### Community 15 - "BundleLayoutService"
Cohesion: 0.06
Nodes (55): Overlay write before bundle write still records overlay presence., Multiple source/pages/NNNN.* files must not silently pick one., test_page_bundle_manifest_round_trip(), test_resolve_source_image_path_rejects_ambiguous_extensions(), test_write_overlay_state_creates_manifest_when_missing(), BundlePaths, PageBundleManifest, On-disk page manifest for one Spec 0002 page bundle. (+47 more)

### Community 16 - "test_olmocr_runner.py"
Cohesion: 0.12
Nodes (42): hosted_runner(), mock_client(), MockHttpxClient, olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint() (+34 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "ConfigurationError"
Cohesion: 0.05
Nodes (48): test_spec_0013_runner_invariants_reject_invalid_payloads(), ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all wordwending errors., RunnerEndpointUnavailable (+40 more)

### Community 19 - "BundlePage"
Cohesion: 0.14
Nodes (31): _expected_evidence(), _flag(), _page_witnesses(), parametrize, Return a minimal evaluation flag for queue fixtures., Return Spec 0005 evidence order with a dimension-specific item 3., Return page-local witnesses matching fixture provenance., test_adjudication_excludes_page_id_from_related_object_ids() (+23 more)

### Community 20 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 21 - "Path"
Cohesion: 0.07
Nodes (19): Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page…, Return the page evaluation scores artifact path. Args: page_number: 1-based… (+11 more)

### Community 22 - "ReviewTask"
Cohesion: 0.07
Nodes (36): _gold_task(), _overlay_with_tasks(), Path, Return a span-scoped text review task for validation fixtures., Return a gold task packet (unsupported by review apply)., Return a minimal PageOverlay carrying the given review tasks., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Dedicated validation rejects text tasks whose span ids are absent. (+28 more)

### Community 23 - "BT Witness Preparation Slice"
Cohesion: 0.05
Nodes (42): ExtractionOrchestrator, Project Structure (models/services/cli/settings), Single Responsibility Service Architecture, Dual Text Contract, Historical Character Preservation, LineJoinRecord, text-norm-v1 Policy, TextNormalizer (+34 more)

### Community 24 - "TestConfiguration"
Cohesion: 0.06
Nodes (22): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+14 more)

### Community 25 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 26 - "TextRole"
Cohesion: 0.14
Nodes (14): FontSlant, Visual font-slant classification independent of weight and role., Semantic role kept separate from visual typography., TextRole, _facet_match(), Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:…, Score footnote-marker retention when gold carries that role. Args: gold_span:… (+6 more)

### Community 27 - "SourcePageArtifact"
Cohesion: 0.10
Nodes (34): PdfPage, One acquired source page before preparation., SourcePageArtifact, _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids() (+26 more)

### Community 28 - "PreparationRecipe"
Cohesion: 0.07
Nodes (34): Empty artifact group for a page/runner raises zero-witnesses error., test_raw_witness_ref_zero_artifacts_errors(), PreparationRecipe, PreparationResult, model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The… (+26 more)

### Community 29 - "test_ocr_models.py"
Cohesion: 0.03
Nodes (117): _bundle_page_payload(), capability_payload(), execution_batch_payload(), _minimal_rag_document(), model_runner_payload(), _prepared_unit_ref(), _provenance(), parametrize (+109 more)

### Community 30 - "._score_text_pair"
Cohesion: 0.12
Nodes (14): _edit_distance(), _graphemes(), _is_ligature(), _is_macron_grapheme(), _is_thorn_eth(), Return whether ``grapheme`` carries a macron in NFC or NFD form. Args:…, Return whether ``grapheme`` is thorn or eth. Args: grapheme: One NFC grapheme…, Return whether ``grapheme`` is an OE ligature under watch. Args: grapheme: One… (+6 more)

### Community 31 - "Path"
Cohesion: 0.13
Nodes (19): _export_note_page(), Path, Export should round PAGE coordinates to importer-friendly integers., PAGE corrections should update text while sidecar evidence stays intact., PAGE diplomatic corrections should regenerate normalized span text., Import should fail when PAGE XML drops a canonical region id., Import should fail when PAGE XML repeats a canonical line id., Import should fail when corrected PAGE points at a different image identity. (+11 more)

### Community 32 - "GoldPageAnnotation"
Cohesion: 0.08
Nodes (32): test_metric_profile_rejects_invalid_iou_threshold(), MetricProfile, BaseModel, Versioned, deterministic evaluation policy., GoldPageAnnotation, Gold data slice for one page., _has_exhaustive_coverage(), _NoteLinkageScorer (+24 more)

### Community 33 - "ReviewOverlayService"
Cohesion: 0.11
Nodes (21): Replay of frozen fixture events must equal fixture current_state., test_overlay_v1_fixture_replay_matches_current_state(), _coordinate_space_ids(), _nested_object_ids(), ReviewEvent, Apply one append-only event onto a mutable overlay state. Args: state:…, Record trust, applied event id, and reviewed/corrected dimensions. Args: state:…, Apply event-specific override fields named by the event contract. Structural… (+13 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.16
Nodes (34): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+26 more)

### Community 35 - "test_bakeoff.py"
Cohesion: 0.11
Nodes (44): _box(), _gold(), _prediction(), profile(), Path, Build one gold page annotation matching the prediction span., Schema defaults name real ADR 0007 candidates, not FakePassRunner., Harness scores recorded (mocked) responses for both real candidates. (+36 more)

### Community 36 - "._invoke_item"
Cohesion: 0.08
Nodes (25): _encode_png_base64(), _load_direct_image(), _load_image_from_pdf(), Any, Image, Path, RequestError, Response (+17 more)

### Community 37 - "File map"
Cohesion: 0.13
Nodes (14): Done criteria (from spec), File map, Rename `bochord` → `wordwending` Implementation Plan, Task 10: GitHub rename + URL sweep, Task 11: Operator checklist (human), Task 1: Branch, Task 2: Move package directory, Task 3: Mechanical replace (in-scope only) (+6 more)

### Community 38 - "WitnessAdaptationService"
Cohesion: 0.09
Nodes (44): _coordinate_space(), _prepared_page(), Path, Adapted span ids and texts match assemble gold-v1 target_object_ids., Empty artifact_paths list is rejected before reading., Non-chat.completion JSON is rejected as an invalid raw witness., Write a minimal chat.completion witness artifact for adaptation tests., Wrong JSON field types surface as ValueError, not TypeError. (+36 more)

### Community 39 - "Rename `bochord` → `wordwending` Design"
Cohesion: 0.17
Nodes (11): Done Criteria, Execution Order, Identity Map, In Scope, Locked Decisions, Non-Goals (Ponytail), Out of Scope, Purpose (+3 more)

### Community 40 - "PlannedRunnerBatch"
Cohesion: 0.12
Nodes (32): bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests., test_direct_packaging_references_original_artifact(), test_direct_packaging_rejects_multi_item_batch() (+24 more)

### Community 41 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 42 - "._build_task"
Cohesion: 0.13
Nodes (10): Build a span-scoped diplomatic-text review task packet. Task identity is scoped…, Build a region-scoped layout/structure review task packet. Split and merge work…, Build a span-scoped typography review task packet. Typography certification is…, Build a note-scoped linkage review task packet. Primary targets are note ids.…, Build a page-scoped source-quality triage task packet. Args: page: Accepted…, Build a page-scoped preparation / subdivision task packet. Args: page: Accepted…, Emit dimension-specific packets for non-empty compatible target sets. Args:…, Assemble a dimension-specific packet with typed evidence binding. Args: page:… (+2 more)

### Community 43 - "services/bakeoff.py"
Cohesion: 0.13
Nodes (16): BakeoffMatrix, BakeoffPredictionRef, Filesystem reference to one recorded prediction for a candidate., Reproducible bake-off matrix written as ``bakeoff-matrix-v1.json``., BakeoffCandidateInvoker, _outcome_from_prediction_ref(), Path, Protocol (+8 more)

### Community 44 - "models/__init__.py"
Cohesion: 0.04
Nodes (128): HumanMarkupService task types must certify only their exclusive dimension., _event_base(), _polygon(), datetime, MonkeyPatch, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is… (+120 more)

### Community 45 - "Settings"
Cohesion: 0.10
Nodes (34): BaseSettings, PydanticBaseSettingsSource, configured_settings(), ExplodingEndpointLifecycleService, fake_service(), FakeEndpointLifecycleService, datetime, fixture (+26 more)

### Community 46 - "2026-08-07-v1-spine-and-phase-completion.md"
Cohesion: 0.06
Nodes (35): ADR Alignment (locked — do not silently invert), Execution Handoff, File Map, Global Constraints, Locked Decisions, Optional later plan (NOT this plan), Spec 0004 Completion Matrix (honest), Subagent Model Policy (+27 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.05
Nodes (28): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events. (+20 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.15
Nodes (15): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Evidence-Bound Human Review, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy (+7 more)

### Community 50 - "test_assemble.py"
Cohesion: 0.07
Nodes (64): _acquisition(), _bibliographic(), _coordinate_space(), _merge_policy(), _MergeWithExtraFlags, _orchestrator(), _prepared_page(), Path (+56 more)

### Community 51 - "PageClass"
Cohesion: 0.08
Nodes (53): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+45 more)

### Community 52 - "cli"
Cohesion: 0.07
Nodes (31): _dense_two_column_image(), Image, patch, Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., Test the version command., Test the version command displays version information., Test the run command. (+23 more)

### Community 53 - "test_cli_utils.py"
Cohesion: 0.09
Nodes (21): Tests for CLI utilities., Test success panel has correct styling., Test info printing functions., Test basic info printing., Test info panel has correct styling., Test error printing functions., Test basic error printing., Test error printing with suggestions. (+13 more)

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

### Community 58 - ".apply"
Cohesion: 0.14
Nodes (12): Path, ReviewEvent, Validate an overlay, append new events, and rewrite overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, Reject overlay submissions whose page id does not match the CLI flag. Args:…, Resolve one bundle page number from its stable page id. Args: bundle_root:…, Append only review events whose ids are not already recorded. Args:…, Replay append-only review history for one page. Args: bundle_root: Filesystem… (+4 more)

### Community 59 - "test_preparation_service.py"
Cohesion: 0.06
Nodes (87): MockerFixture, binary_recipe(), bundle_service(), dark_gutter_image(), dense_source_page(), dense_two_column_image(), note_heavy_image(), preparation_service() (+79 more)

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

### Community 66 - "RunnerBatchPlanner"
Cohesion: 0.23
Nodes (22): Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), artifacts(), capability(), policy(), _prepared_unit(), Return a default multi-item runner capability with optional overrides. (+14 more)

### Community 67 - "EndpointCatalogEntry"
Cohesion: 0.15
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
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

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
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 79 - "test_merge_service.py"
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

### Community 83 - "TestCLIReview"
Cohesion: 0.17
Nodes (9): Test review apply and materialize commands., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends overlay events and materializes current_state.json., Re-applying the same overlay must not rewrite prior JSONL bytes., Materialize replays JSONL history into current_state.json., Apply fails when --page-id does not match the overlay file., Apply fails when overlay tasks reference ids absent from the page., Materialize fails when the bundle has no matching page id. (+1 more)

### Community 84 - "Spec 0016 RAG Line Contract Follow-up Implementation Plan"
Cohesion: 0.22
Nodes (8): Acceptance Checks, Exact Invariant Matrix, File Map, Global Constraints, Plan Self-Review, Spec 0016 RAG Line Contract Follow-up Implementation Plan, Task 1: Specify and Enforce Intrinsic RAG Line Invariants, Task 2: Regenerate Schema and Prove Frozen Export Compatibility

### Community 85 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 86 - "HfEndpointClient"
Cohesion: 0.10
Nodes (27): InferenceEndpoint, _FakeInferenceEndpoint, MonkeyPatch, test_constructor_requires_token(), test_create_omits_scale_to_zero_when_disabled(), test_create_passes_catalog_fields_and_scale_to_zero(), test_describe_maps_remote_state(), test_hub_errors_map_to_endpoint_lifecycle_error() (+19 more)

### Community 87 - "Path"
Cohesion: 0.07
Nodes (25): Path, inspect-bundle lists exports/* paths after assemble and export., inspect-bundle prints document and page summary., inspect-bundle surfaces OK after assemble seals prepared-image digests., inspect-bundle surfaces OK when layout digests match on-disk bytes., inspect-bundle prints merge flags after multi-witness disagreement., Assemble fails when manifest witness paths are absent under bundle_root., Assemble fails when manifest JSON is invalid. (+17 more)

### Community 88 - "test_endpoint_lifecycle.py"
Cohesion: 0.30
Nodes (17): _assert_is_endpoint_client(), _catalog(), Path, _service(), _settings(), test_down_pauses_by_default_delete_flag_destroys(), test_ensure_up_already_running_skips_create_and_resume(), test_ensure_up_creates_missing_and_returns_https_url() (+9 more)

### Community 89 - "Sphinx Docs Index"
Cohesion: 0.67
Nodes (4): Changelog, Sphinx Docs Index, README, Read the Docs Config

### Community 90 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 91 - "test_pass_runner_registry.py"
Cohesion: 0.17
Nodes (11): PassRunnerClass, test_default_registry_resolves_kraken_adapter(), test_default_registry_resolves_olmocr_adapter(), test_register_overrides_or_adds_runner_id(), test_resolve_unknown_runner_id_fails_clearly(), PassRunnerRegistry, Resolve hosted ``PassRunner`` adapter classes by stable ``runner_id``. Defaults…, Bind known runner classes for resolution. Args: runners: Optional mapping of… (+3 more)

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

### Community 98 - "._invoke_item"
Cohesion: 0.07
Nodes (26): _encode_png_base64(), _load_direct_image(), _load_image_from_pdf(), Any, Image, Path, RequestError, Response (+18 more)

### Community 99 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 100 - "test_page_interchange.py"
Cohesion: 0.21
Nodes (15): _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids. (+7 more)

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

### Community 130 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 131 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0009: Merge and Alignment (+3 more)

### Community 132 - "test_live_hf_bakeoff_requires_integration_marker"
Cohesion: 0.67
Nodes (3): integration, Live HF bake-off stays behind pytest.mark.integration (not default suite)., test_live_hf_bakeoff_requires_integration_marker()

### Community 133 - "inspect_bundle"
Cohesion: 0.20
Nodes (10): _echo_checksum_results(), _echo_export_paths(), _echo_page_flags(), inspect_bundle(), Load export path hints from the best available bundle JSON on disk. Args:…, Print OK/FAIL/SKIPPED lines for bundle-layout recorded checksums. Args:…, Print bundle-relative export artifact paths that exist on disk. Args:…, Print evaluation/merge flags from one page ``flags.json`` sidecar. Args:… (+2 more)

### Community 135 - "services/merge.py"
Cohesion: 0.04
Nodes (102): NamedTuple, _apply_note_link_resolution(), _apply_span_text_resolution(), _apply_span_typography_resolution(), _box_iou(), _detect_structure_conflict(), _first_candidate_by_runner_precedence(), _flagged_object_ids() (+94 more)

### Community 137 - "RagChunk"
Cohesion: 0.19
Nodes (8): RagChunk, Page-local retrieval chunk., Build cross-page stitched chunks from contiguous BODY region runs. Args:…, Emit one stitched chunk when a BODY run spans multiple pages. Args:…, Collect ordered distinct page ids from component chunks. Args: chunks: Region…, Union source object ids from component region chunks. Args: chunks: Region…, Union provenance pointers from component region chunks. Args: chunks: Region…, Aggregate trust from one or more trust-state values. Args: trust_states: Trust…

### Community 138 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 139 - "EndpointLifecycleService"
Cohesion: 0.07
Nodes (34): test_overlay_endpoints_merges_runner_urls_immutably(), build_endpoint_lifecycle_service(), endpoints_down(), endpoints_status(), endpoints_up(), ensure_and_overlay_settings(), _handle_lifecycle_errors(), command (+26 more)

### Community 140 - "TestCLIExport"
Cohesion: 0.25
Nodes (5): Test the export command., Export writes Spec 0006 derived artifacts under exports/., Export aborts when DocumentBundle JSON fails validation., Export requires --bundle-root., TestCLIExport

### Community 141 - "review.py"
Cohesion: 0.36
Nodes (7): command, option, Path, Append overlay review events and write materialized overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, review_apply(), review_materialize()

### Community 142 - "Path"
Cohesion: 0.13
Nodes (24): argument, assemble_document(), _assemble_manifest_from_run(), eval_cohorts(), eval_page(), export_document(), _load_page_overrides(), _load_preparation_recipe() (+16 more)

### Community 143 - ".build"
Cohesion: 0.38
Nodes (5): _load_preparation(), Path, Copy usable batch witnesses into ``bundle_root`` and record page refs. Keyword…, Load the sole ``PreparationResult`` for ``page_id`` under ``bundle_root``.…, Scan run batches and prepare trees into an assemble manifest. Keyword Args:…

### Community 144 - "PageEvaluationSummary"
Cohesion: 0.13
Nodes (14): Matrix cells carry runner, page class, scores, latency, failure, license., test_matrix_cell_schema_includes_required_fields(), test_page_evaluation_has_exactly_three_top_level_families(), BakeoffMatrixCell, BakeoffPageRef, Filesystem reference to one bake-off page gold annotation., One runner x page cell in the bake-off matrix artifact., PageEvaluationSummary (+6 more)

### Community 145 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 147 - "_review_polygon"
Cohesion: 0.29
Nodes (6): Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces., _review_box(), _review_polygon()

### Community 150 - "test_bundle_layout.py"
Cohesion: 0.08
Nodes (37): load_export_minimal_bundle(), load_frozen_document_bundle_v1(), Persisted document exports match renderer output and preserve overlays., Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the compact export-fixture DocumentBundle., Load the frozen document-bundle-v1 contract fixture., test_bundle_paths_match_spec_0002_layout(), test_document_bundle_manifest_rejects_non_positive_page_count() (+29 more)

### Community 152 - "._tasks_from_buckets"
Cohesion: 0.18
Nodes (7): _FlagTargetBuckets, Mutable accumulator for flag-driven queue grouping., Initialize empty primary, related, and adjudication buckets., Build a page-scoped adjudication task for empty or unknown flag targets. Args:…, Derive a deterministic review queue from page evaluation flags. Flags are…, Build unsorted packets from classified flag-target buckets. Args: page:…, Classify evaluation-flag targets into dimension buckets. Args: page: Accepted…

### Community 157 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``wordwending run``.

### Community 158 - "endpoints"
Cohesion: 0.67
Nodes (3): endpoints(), group, Ensure, pause, or inspect Hugging Face Inference Endpoints.

### Community 159 - "review"
Cohesion: 0.67
Nodes (3): group, Apply and materialize human review overlays on document bundles., review()

## Ambiguous Edges - Review These
- `README` → `Sphinx Docs Index`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to
- `Frequently Asked Questions` → `Quickstart CLI Entry Points`  [AMBIGUOUS]
  doc/source/overview/faq.rst · relation: conceptually_related_to
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to

## Knowledge Gaps
- **228 isolated node(s):** `release.sh script`, `wordwending`, `IPA_AUDIO`, `Locked Decisions (from grilling)`, `Global Constraints` (+223 more)
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
- **Why does `BundlePage` connect `BundlePage` to `MergeOrchestrator`, `test_text_normalization.py`, `test_merge_review.py`, `CoordinateSpace`, `SchemaModel`, `services/merge.py`, `test_evaluation_service.py`, `RagChunk`, `test_assemble_manifest.py`, `._write_page_xml`, `cli.py`, `BundleLayoutService`, `PageEvaluationSummary`, `test_bundle_layout.py`, `ReviewTask`, `._tasks_from_buckets`, `PageXmlInterchangeService`, `test_ocr_models.py`, `GoldPageAnnotation`, `test_bakeoff.py`, `._build_task`, `services/bakeoff.py`, `models/__init__.py`, `test_assemble.py`, `test_merge_service.py`, `test_page_interchange.py`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `SchemaModel` to `services/preparation.py`, `test_text_normalization.py`, `test_merge_review.py`, `CoordinateSpace`, `test_evaluation_service.py`, `RagChunk`, `EndpointSessionLedgerStore`, `EndpointLifecycleService`, `RunnerReference`, `BundleLayoutService`, `PageEvaluationSummary`, `ConfigurationError`, `BundlePage`, `test_bundle_layout.py`, `ReviewTask`, `SourcePageArtifact`, `PreparationRecipe`, `test_ocr_models.py`, `GoldPageAnnotation`, `test_bakeoff.py`, `PlannedRunnerBatch`, `services/bakeoff.py`, `models/__init__.py`, `Settings`, `test_assemble.py`, `PageClass`, `cli`, `ResumeLedgerService`, `EndpointCatalogEntry`, `test_bundle_checksum.py`, `test_merge_service.py`, `EndpointRemoteState`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `cli()` connect `cli` to `test_assemble_eval_export_wave_a_exit`, `TestCLIGlobalOptions`, `test_bakeoff.py`, `TestCLIExport`, `Settings`, `cli.py`, `Path`, `TestCLIErrorHandling`, `TestCLIReview`, `test_cli_utils.py`, `main`, `Path`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `BundlePage` (e.g. with `BakeoffCandidate` and `BakeoffInvocationOutcome`) actually correct?**
  _`BundlePage` has 19 INFERRED edges - model-reasoned connections that need verification._