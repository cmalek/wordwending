# Graph Report - wordwending  (2026-08-07)

## Corpus Check
- 158 files · ~206,304 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3459 nodes · 9211 edges · 142 communities (121 shown, 21 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 765 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04262b36`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/preparation.py
- models/__init__.py
- RunnerExecutionPolicy
- _NoteCandidate
- RunnerThroughputSummary
- test_document_export.py
- PageClass
- BundleLayoutService
- test_evaluation_service.py
- Detailed OCR Process
- services/evaluation.py
- ._write_page_evaluation_and_manifest
- model_validator
- cli.py
- _extract_openai_chat_completion_lines
- services/merge.py
- HuggingFaceOlmocrRunner
- ADR 0010 Structured Output Boundary
- _try_rebind_event
- ResumeLedgerService
- check_napoleon_gate.py
- BundlePaths
- test_olmocr_runner.py
- BT Witness Preparation Slice
- TestConfiguration
- PageXmlInterchangeService
- test_merge_review.py
- PreparationRecipe
- PagePreparationOverride
- test_ocr_models.py
- SourceAcquisitionService
- test_page_interchange.py
- SpanRecord
- ReviewOverlayService
- test_runner_execution.py
- test_assemble.py
- ReviewTaskType
- File map
- DocumentExportService
- Rename `bochord` → `wordwending` Design
- PlannedRunnerBatch
- ._coords
- _AssembleExecution
- cli
- evaluation_cohorts.py
- Settings
- test_bakeoff.py
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- _review_polygon
- MergeOrchestrator
- BundlePage
- test_cli_utils.py
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- HuggingFaceKrakenRunner
- test_preparation_service.py
- Preparation Gold Specs
- Raw OCR witness layer
- create_progress
- Spec 0002: V1 Bundle Layout and Data Shape
- ._build_region_chunk
- Coding Standards Docs
- .score
- ReviewTask
- ADR 0009 OCR-D PAGE eScriptorium
- Spec 0006: Exports and Retrieval Views
- README, Operator Docs, and Thin Export CLI Implementation Plan
- .validate_item_page_alignment
- Normalized Page Graph
- Configuration: Command Line Tool
- Anglian dialect group
- ._pick_scaffold_witness
- NoteRecord
- Learner lacks stable conceptual map of sound-change order
- Lesson 0001 Sound Change and Reconstruction
- test_merge_service.py
- ADR 0004 Layered Truth
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- run_runner
- Spec 0016 RAG Line Contract Follow-up Implementation Plan
- TestConsoleQuietMode
- 2026-08-07-v1-spine-and-phase-completion.md
- _detect_structure_conflict
- TestCLISettings
- Sphinx Docs Index
- Lesson 0003 Pronouncing Old English Letters
- Path
- .validate_https_huggingface_endpoints
- Page Graph Line
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- .apply
- page_dir_name
- review
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
- ReviewScope
- OCR Evidence Not Philological Semantics
- ADR 0002 Bundle Model
- Page Bundle as Page-Local Truth Unit
- ADR 0003 Page Graph
- SourceProvenanceService
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- .reject_historical_modernization
- Mixed dialect spellings from copying history
- Reference Sound Terms
- test_cli_commands.py
- TestCLIErrorHandling
- TestCLIReview
- Spec 0005: Human Markup and Review
- wordwending
- CoordinateSpace
- .__init__
- ._write_page_xml
- TestCLIExport
- Assemble eval fixtures
- test_assemble_eval_export_wave_a_exit
- test_live_hf_bakeoff_requires_integration_marker
- _PreparedInputsManifest

## God Nodes (most connected - your core abstractions)
1. `BundlePage` - 139 edges
2. `AlternateCandidate` - 120 edges
3. `SchemaModel` - 116 edges
4. `CoordinateSpace` - 75 edges
5. `SpanRecord` - 75 edges
6. `RegionRecord` - 73 edges
7. `PreparedPage` - 70 edges
8. `BundleLayoutService` - 70 edges
9. `MergePolicy` - 69 edges
10. `cli()` - 66 edges

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

## Communities (142 total, 21 thin omitted)

### Community 0 - "services/preparation.py"
Cohesion: 0.05
Nodes (76): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _build_prepared_units(), _column_ink_profile() (+68 more)

### Community 1 - "models/__init__.py"
Cohesion: 0.03
Nodes (143): Enum, Runner, overlay, and gold contracts should fit the planned workflow., _event_base(), _polygon(), datetime, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is… (+135 more)

### Community 2 - "RunnerExecutionPolicy"
Cohesion: 0.09
Nodes (44): Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), artifacts(), capability(), policy(), _prepared_unit(), Return a default multi-item runner capability with optional overrides., Return a default runner execution policy with optional overrides. (+36 more)

### Community 3 - "_NoteCandidate"
Cohesion: 0.09
Nodes (37): NamedTuple, _apply_note_link_resolution(), _map_marker_span_ids(), _mapped_note_link_sets(), _MarkerMappingContext, _min_merge_confidence(), _note_link_alternates(), _note_marker_links_from_mapped_sets() (+29 more)

### Community 4 - "RunnerThroughputSummary"
Cohesion: 0.06
Nodes (41): Persisted batch status must agree with submitted and failed items., ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all wordwending errors., RunnerEndpointUnavailable (+33 more)

### Community 5 - "test_document_export.py"
Cohesion: 0.07
Nodes (49): test_document_bundle_manifest_rejects_non_positive_page_count(), test_document_bundle_manifest_round_trip(), _document_bundle(), _load_frozen_document_bundle_v1(), _minimal_document_bundle(), Document export filenames stay fixed under exports/., Wrap accepted pages in a valid multi-page document bundle., Wrap one accepted page in a valid document bundle. (+41 more)

### Community 6 - "PageClass"
Cohesion: 0.05
Nodes (83): test_operator_override_requires_reason(), _prepare_overrides(), Validate and convert optional CLI override values. Args: mode: Optional…, FlagSeverity, PageClass, PreparationMode, Page-level layout cohorts used by preparation and evaluation., Prepared-page subdivision modes. (+75 more)

### Community 7 - "BundleLayoutService"
Cohesion: 0.05
Nodes (78): _accept_review_event(), load_export_minimal_bundle(), load_frozen_document_bundle_v1(), load_minimal_bundle(), Path, source_files keys must be bare basenames, not path segments., page_exports basenames must not escape the page exports directory., Append inserts a separator when prior JSONL lacks a trailing newline. (+70 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.11
Nodes (54): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+46 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "services/evaluation.py"
Cohesion: 0.04
Nodes (60): test_metric_profile_rejects_invalid_iou_threshold(), MetricProfile, BaseModel, Versioned, deterministic evaluation policy., GoldStyleSpan, Gold style target for one span or image-anchored area., _box_iou(), _boxes_intersect() (+52 more)

### Community 11 - "._write_page_evaluation_and_manifest"
Cohesion: 0.08
Nodes (32): _atomic_write_json(), _atomic_write_text(), _collect_page_flags(), _needs_trailing_newline(), Path, ReviewEvent, Return ``path`` relative to ``root`` without a leading ``./``. Args: root:…, Gather evaluation flags from all page summary families. Args: summary: Per-page… (+24 more)

### Community 12 - "model_validator"
Cohesion: 0.05
Nodes (25): _known_page_space_ids(), _known_preparation_space_ids(), model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Require provenance pointers to stay local to the owning page. Args: provenance:… (+17 more)

### Community 13 - "cli.py"
Cohesion: 0.11
Nodes (34): argument, assemble_document(), bakeoff_matrix(), _echo_export_paths(), _echo_page_flags(), eval_cohorts(), eval_page(), export_document() (+26 more)

### Community 14 - "_extract_openai_chat_completion_lines"
Cohesion: 0.18
Nodes (9): _extract_openai_chat_completion_lines(), KrakenChatCompletionAdapter, OlmocrChatCompletionAdapter, Parse exact kraken chat.completion JSON bytes into diplomatic text lines. This…, Extract newline-split assistant content from chat.completion bytes. Args:…, Initialize with runner_id-keyed chat.completion parsing strategies., Extract newline-split assistant content from chat.completion bytes. Shared by…, Parse exact olmOCR chat.completion JSON bytes into diplomatic text lines. This… (+1 more)

### Community 15 - "services/merge.py"
Cohesion: 0.10
Nodes (37): Orthogonal visual typography facets for one text span., Typography, _apply_span_text_resolution(), _first_candidate_by_runner_precedence(), _flagged_object_ids(), Any, Collect unique witness ids from span candidates in input order. Args:…, Collect unique runner ids from span candidates in input order. Args:… (+29 more)

### Community 16 - "HuggingFaceOlmocrRunner"
Cohesion: 0.06
Nodes (39): BatchUnitKind, Batch grouping units for runner execution., _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _ItemInvokeResult, _load_direct_image(), _load_image_from_pdf() (+31 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "_try_rebind_event"
Cohesion: 0.10
Nodes (21): _coordinate_space_ids(), _nested_object_ids(), ReviewEvent, Apply one append-only event onto a mutable overlay state. Args: state:…, Record trust, applied event id, and reviewed/corrected dimensions. Args: state:…, Apply event-specific override fields named by the event contract. Structural…, Rebind one event when every required id resolves; otherwise skip it. Args:…, Collect nested marker/region/line/note ids that must remap. Args: event:… (+13 more)

### Community 19 - "ResumeLedgerService"
Cohesion: 0.11
Nodes (22): Path, test_corrupt_ledger_is_treated_as_empty(), test_missing_ledger_is_empty(), test_record_completed_persists_and_reloads(), test_record_completed_replaces_same_batch_id(), One successfully completed runner batch recorded for resume., Persisted set of successfully completed runner batches under a bundle., ResumeLedger (+14 more)

### Community 20 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 21 - "BundlePaths"
Cohesion: 0.07
Nodes (28): Multiple source/pages/NNNN.* files must not silently pick one., test_bundle_paths_match_spec_0002_layout(), test_resolve_source_image_path_rejects_ambiguous_extensions(), test_source_page_image_rejects_empty_extension(), BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:… (+20 more)

### Community 22 - "test_olmocr_runner.py"
Cohesion: 0.05
Nodes (92): LookupError, PassRunnerClass, hosted_runner(), kraken_response(), mock_client(), planned_batch(), policy(), policy_with_endpoint() (+84 more)

### Community 23 - "BT Witness Preparation Slice"
Cohesion: 0.05
Nodes (42): ExtractionOrchestrator, Project Structure (models/services/cli/settings), Single Responsibility Service Architecture, Dual Text Contract, Historical Character Preservation, LineJoinRecord, text-norm-v1 Policy, TextNormalizer (+34 more)

### Community 24 - "TestConfiguration"
Cohesion: 0.07
Nodes (21): Exception, patch, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder…, Test that environment variables override defaults. (+13 more)

### Community 25 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 26 - "test_merge_review.py"
Cohesion: 0.08
Nodes (38): _eval_flag(), _merge_flag(), _page_with_text_flags(), parametrize, Return one merge flag fixture., Return one evaluation flag with an explicit merge flag_type., Attach evaluation flags onto the text family only (legacy C3 shape)., Known merge flag types become Spec 0005 dimension packets even if mis-bucketed. (+30 more)

### Community 27 - "PreparationRecipe"
Cohesion: 0.10
Nodes (36): PdfPage, PreparationRecipe, One acquired source page before preparation., Deterministic page-preparation profile., SourcePageArtifact, _artifact_from_raster(), _image_dpi(), _image_paths_in_directory() (+28 more)

### Community 28 - "PagePreparationOverride"
Cohesion: 0.08
Nodes (21): test_page_override_requires_choice_and_reason(), PagePreparationOverride, model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Operator override for one acquired source page., Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The… (+13 more)

### Community 29 - "test_ocr_models.py"
Cohesion: 0.03
Nodes (101): _bundle_page_payload(), capability_payload(), execution_batch_payload(), _minimal_rag_document(), model_runner_payload(), parametrize, _rag_chunk(), Return a mutable dump of a valid bundle page with optional overrides. (+93 more)

### Community 30 - "SourceAcquisitionService"
Cohesion: 0.24
Nodes (20): pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe(), test_image_bounds_must_overlap_most_of_page_area(), test_image_folder_records_image_set_source_type() (+12 more)

### Community 31 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 32 - "SpanRecord"
Cohesion: 0.12
Nodes (18): Accepted text span in the page graph., SpanRecord, Collect stable graph object ids included in a region chunk. Args: objects:…, Resolve the stable identifier for one graph object. Args: obj: Graph object…, _apply_span_typography_resolution(), _collect_span_candidates(), _iter_accepted_objects(), _matching_spans_for_witness() (+10 more)

### Community 33 - "ReviewOverlayService"
Cohesion: 0.10
Nodes (35): _overlay_with_tasks(), Path, Return a span-scoped text review task for validation fixtures., Return a minimal PageOverlay carrying the given review tasks., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Dedicated validation rejects text tasks whose span ids are absent., GOLD tasks are not supported by review apply validation., Known span ids pass dedicated overlay-task validation. (+27 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.14
Nodes (41): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+33 more)

### Community 35 - "test_assemble.py"
Cohesion: 0.12
Nodes (39): _acquisition(), _bibliographic(), _coordinate_space(), _merge_policy(), _MergeWithExtraFlags, _orchestrator(), _prepared_page(), Path (+31 more)

### Community 36 - "ReviewTaskType"
Cohesion: 0.15
Nodes (11): HumanMarkupService task types must certify only their exclusive dimension., MonkeyPatch, Corrupt split dump shapes must raise ValueError, not shrink regions., Return a review task bound to the shared overlay evidence., _task(), test_successor_split_rebind_rejects_non_mapping_region(), Operator workflow represented by a review task packet., Verb vocabulary for append-only review events. (+3 more)

### Community 37 - "File map"
Cohesion: 0.13
Nodes (14): Done criteria (from spec), File map, Rename `bochord` → `wordwending` Implementation Plan, Task 10: GitHub rename + URL sweep, Task 11: Operator checklist (human), Task 1: Branch, Task 2: Move package directory, Task 3: Mechanical replace (in-scope only) (+6 more)

### Community 38 - "DocumentExportService"
Cohesion: 0.05
Nodes (47): _body_region_page(), _load_minimal_bundle(), _markdown_style_page(), _merge_page_regions(), _page_provenance(), _page_witness(), _prepared_page(), Bold+italic spans use ***text*** with bold outside italic. (+39 more)

### Community 39 - "Rename `bochord` → `wordwending` Design"
Cohesion: 0.17
Nodes (11): Done Criteria, Execution Order, Identity Map, In Scope, Locked Decisions, Non-Goals (Ponytail), Out of Scope, Purpose (+3 more)

### Community 40 - "PlannedRunnerBatch"
Cohesion: 0.09
Nodes (48): MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., bundle_root(), planned_batch(), fixture, Path (+40 more)

### Community 41 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 42 - "_AssembleExecution"
Cohesion: 0.16
Nodes (14): _AssembleExecution, _bundle_ready_page(), Path, Per-run mutable assemble state and page loop. Args: adapter: Witness adaptation…, Initialize per-run assemble accumulators. Keyword Args: adapter: Witness…, Adapt, merge, and accumulate one page into run state. Args: page_request:…, Adapt every raw witness on one page with unique-id checks. Args: page_request:…, Reject duplicate ``witness_id`` within a page or across pages. Keyword Args:… (+6 more)

### Community 43 - "cli"
Cohesion: 0.11
Nodes (14): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., Test the prepare command. (+6 more)

### Community 44 - "evaluation_cohorts.py"
Cohesion: 0.11
Nodes (38): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+30 more)

### Community 45 - "Settings"
Cohesion: 0.18
Nodes (12): BaseSettings, PydanticBaseSettingsSource, patch, Test the run command., _run_cli_args(), TestCLIRun, Path, Load settings from file with cascading configuration. Args: settings_cls:… (+4 more)

### Community 46 - "test_bakeoff.py"
Cohesion: 0.07
Nodes (76): _box(), _gold(), _prediction(), profile(), Path, Build one gold page annotation matching the prediction span., Schema defaults name real ADR 0007 candidates, not FakePassRunner., Matrix cells carry runner, page class, scores, latency, failure, license. (+68 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.05
Nodes (28): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events. (+20 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.15
Nodes (15): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Evidence-Bound Human Review, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy (+7 more)

### Community 50 - "_review_polygon"
Cohesion: 0.29
Nodes (6): Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces., _review_box(), _review_polygon()

### Community 51 - "MergeOrchestrator"
Cohesion: 0.07
Nodes (26): _LayoutObject, _apply_layout_merge_confidence(), _collect_note_candidates(), MergeOrchestrator, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Initialize merge orchestration for one page. Args: policy: Versioned merge…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph…, Choose the accepted prepared page variant for this merge. (+18 more)

### Community 52 - "BundlePage"
Cohesion: 0.11
Nodes (36): _expected_evidence(), _flag(), _page_witnesses(), parametrize, Return a minimal evaluation flag for queue fixtures., Return Spec 0005 evidence order with a dimension-specific item 3., Return page-local witnesses matching fixture provenance., test_adjudication_excludes_page_id_from_related_object_ids() (+28 more)

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
Cohesion: 0.25
Nodes (11): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Verner's Law (+3 more)

### Community 57 - "conftest.py"
Cohesion: 0.17
Nodes (14): Config, cli_context(), mock_console(), mock_settings(), fixture, pytest_configure(), Register custom markers used by optional live/external tests., Create a CLI runner for testing. (+6 more)

### Community 58 - "HuggingFaceKrakenRunner"
Cohesion: 0.06
Nodes (39): One raw witness artifact emitted by a pass runner., RunnerOutputArtifact, _encode_png_base64(), _failed_item_result(), HuggingFaceKrakenRunner, _ItemInvokeResult, _load_direct_image(), _load_image_from_pdf() (+31 more)

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

### Community 64 - "._build_region_chunk"
Cohesion: 0.09
Nodes (15): PageGraphIndex, Typed page-graph lookups keyed by object kind., Build one region retrieval chunk from accepted graph order. Args: document_id:…, Build one footnote retrieval chunk from an accepted note object. Args:…, Resolve span ids for region lines in graph order. Args: lines: Region lines…, Join diplomatic span text for one region in graph order. Args: lines: Region…, Aggregate trust for included graph objects. Args: objects: Graph objects whose…, Report whether any included object has human-reviewed trust. Args: objects:… (+7 more)

### Community 65 - "Coding Standards Docs"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 66 - ".score"
Cohesion: 0.24
Nodes (7): _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold…, Aggregate note-linkage success for covered gold edges. Args: prediction:…, Map predicted note ids to gold region annotation ids that name them. Args:…, Expand predicted notes into marker→note edges under gold aliases. Emits…, Return whether a gold note edge is in exhaustive NOTE_LINKAGE coverage. Args:…, Evaluate text, structure, and style families. Args: prediction: Accepted page…

### Community 67 - "ReviewTask"
Cohesion: 0.09
Nodes (24): _gold_task(), Return a gold task packet (unsupported by review apply)., Self-contained instructions and evidence binding for human review., ReviewTask, _FlagTargetBuckets, Mutable accumulator for flag-driven queue grouping., Initialize empty primary, related, and adjudication buckets., Build a span-scoped diplomatic-text review task packet. Task identity is scoped… (+16 more)

### Community 68 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.22
Nodes (9): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+1 more)

### Community 69 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 70 - "README, Operator Docs, and Thin Export CLI Implementation Plan"
Cohesion: 0.15
Nodes (12): Acceptance Checks, Deferred (explicitly not this plan), File Map, Global Constraints, Locked Decisions (from grilling), Plan Self-Review, README, Operator Docs, and Thin Export CLI Implementation Plan, Task 1: Thin `export` CLI (TDD) (+4 more)

### Community 71 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 72 - "Normalized Page Graph"
Cohesion: 0.29
Nodes (8): Normalized Page Graph, Footnote Chunk, Spec 0011: Structured Output Strategy, Standard OCR Intermediate Structure, TEI Dictionaries Chapter, TEI P5 as Downstream Reference, Domain Language, Shared Domain Glossary

### Community 73 - "Configuration: Command Line Tool"
Cohesion: 0.39
Nodes (8): Configuration: Command Line Tool, CLI Configuration Cascade, Frequently Asked Questions, Installation, Python 3.10+ Installation, Quickstart Guide, Quickstart CLI Entry Points, Using the Command Line Interface

### Community 74 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 75 - "._pick_scaffold_witness"
Cohesion: 0.33
Nodes (5): _coordinate_rich_line_count(), _first_witness_by_runner_preference(), Select one scaffold witness from structure-bearing candidates. Args:…, Pick the first eligible witness for the earliest preferred runner id. Args:…, Count lines carrying bounding boxes or baseline geometry. Args: witness: One…

### Community 76 - "NoteRecord"
Cohesion: 0.06
Nodes (39): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+31 more)

### Community 77 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 78 - "Lesson 0001 Sound Change and Reconstruction"
Cohesion: 0.29
Nodes (8): Comparative method of reconstruction, Lesson 0001 Sound Change and Reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods, Lehmann A Grammar of Proto-Germanic

### Community 79 - "test_merge_service.py"
Cohesion: 0.06
Nodes (118): _aligned_text_witnesses(), _bounding_box(), _coordinate_space(), _line(), _load_merge_fixture(), _note(), _prepared_page(), _provenance() (+110 more)

### Community 80 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Overlay Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 81 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.33
Nodes (6): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Historical Character Preservation, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts

### Community 82 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 83 - "run_runner"
Cohesion: 0.40
Nodes (6): Context, pass_context, Settings-related commands. Args: ctx: Click context object., Execute prepared artifacts against one hosted runner (olmOCR or kraken). Args:…, run_runner(), show_settings()

### Community 84 - "Spec 0016 RAG Line Contract Follow-up Implementation Plan"
Cohesion: 0.22
Nodes (8): Acceptance Checks, Exact Invariant Matrix, File Map, Global Constraints, Plan Self-Review, Spec 0016 RAG Line Contract Follow-up Implementation Plan, Task 1: Specify and Enforce Intrinsic RAG Line Invariants, Task 2: Regenerate Schema and Prove Frozen Export Compatibility

### Community 85 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 86 - "2026-08-07-v1-spine-and-phase-completion.md"
Cohesion: 0.06
Nodes (35): ADR Alignment (locked — do not silently invert), Execution Handoff, File Map, Global Constraints, Locked Decisions, Optional later plan (NOT this plan), Spec 0004 Completion Matrix (honest), Subagent Model Policy (+27 more)

### Community 87 - "_detect_structure_conflict"
Cohesion: 0.12
Nodes (16): _box_iou(), _detect_structure_conflict(), _geometry_alternates_for_regions(), _matching_notes_for_witness(), _note_by_id(), Sort regions by reading order index. Args: regions: Region nodes from one…, Decide whether region box presence disagrees between two witnesses. Args:…, Return whether paired regions fail the IoU match threshold. Args:… (+8 more)

### Community 88 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 89 - "Sphinx Docs Index"
Cohesion: 0.67
Nodes (4): Changelog, Sphinx Docs Index, README, Read the Docs Config

### Community 90 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 91 - "Path"
Cohesion: 0.14
Nodes (14): Path, Test assemble and inspect-bundle commands., Copy witness fixture and prepared image under bundle_root., Copy olmOCR + kraken fixtures and prepared image under bundle_root., Assemble materializes Spec 0002 bundle tree from manifest., Assemble followed by export produces all Spec 0006 export artifacts., inspect-bundle does not list export paths until export has run., inspect-bundle lists exports/* paths after assemble and export. (+6 more)

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

### Community 98 - ".apply"
Cohesion: 0.20
Nodes (8): Path, ReviewEvent, Validate an overlay, append new events, and rewrite overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, Reject overlay submissions whose page id does not match the CLI flag. Args:…, Resolve one bundle page number from its stable page id. Args: bundle_root:…, Append only review events whose ids are not already recorded. Args:…, Replay append-only review history for one page. Args: bundle_root: Filesystem…

### Community 99 - "page_dir_name"
Cohesion: 0.67
Nodes (3): test_page_dir_name_is_zero_padded(), page_dir_name(), Return the stable page directory name for one 1-based page number. Args:…

### Community 100 - "review"
Cohesion: 0.67
Nodes (3): group, Apply and materialize human review overlays on document bundles., review()

### Community 101 - "ADR 0008 Stable IDs and Review History"
Cohesion: 0.67
Nodes (3): ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States

### Community 102 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 113 - "ReviewScope"
Cohesion: 0.18
Nodes (7): Supported human review targets., ReviewScope, Ensure overlay task targets exist on the accepted page graph. Validation is…, Validate one review task's targets against the page graph. Args: page: Accepted…, Validate task target ids against the page graph for one review scope. Args:…, Return page-graph identifiers for one review target scope. Args: page: Accepted…, Reject empty or unknown object identifiers for a review task. Args: object_ids:…

### Community 128 - "test_cli_commands.py"
Cohesion: 0.10
Nodes (13): _dense_two_column_image(), Image, Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., Test the version command., Test the version command displays version information., Test the version command with verbose flag., Test the version command with quiet flag. (+5 more)

### Community 129 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 130 - "TestCLIReview"
Cohesion: 0.17
Nodes (9): Test review apply and materialize commands., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends overlay events and materializes current_state.json., Re-applying the same overlay must not rewrite prior JSONL bytes., Materialize replays JSONL history into current_state.json., Apply fails when --page-id does not match the overlay file., Apply fails when overlay tasks reference ids absent from the page., Materialize fails when the bundle has no matching page id. (+1 more)

### Community 131 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0009: Merge and Alignment (+3 more)

### Community 135 - "CoordinateSpace"
Cohesion: 0.04
Nodes (108): _object_provenance(), Return valid single-page provenance for programmatic graph tests., Separate region/line/span maps must not overwrite unlike graph records., test_typed_page_indexes_resolve_colliding_ids_by_object_kind(), page(), _provenance(), fixture, Return minimal provenance for graph fixtures. (+100 more)

### Community 145 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 148 - "TestCLIExport"
Cohesion: 0.25
Nodes (5): Test the export command., Export writes Spec 0006 derived artifacts under exports/., Export aborts when DocumentBundle JSON fails validation., Export requires --bundle-root., TestCLIExport

### Community 150 - "Assemble eval fixtures"
Cohesion: 0.33
Nodes (5): Assemble eval fixtures, Consumers, Files, Fixture pairing (`page-0001`), ID formula (locked)

### Community 151 - "test_assemble_eval_export_wave_a_exit"
Cohesion: 0.47
Nodes (5): Path, Copy witness fixture and prepared image under ``bundle_root``., Assemble page graph scores against assemble gold, then export markdown., _stage_bundle_inputs(), test_assemble_eval_export_wave_a_exit()

### Community 161 - "test_live_hf_bakeoff_requires_integration_marker"
Cohesion: 0.67
Nodes (3): integration, Live HF bake-off stays behind pytest.mark.integration (not default suite)., test_live_hf_bakeoff_requires_integration_marker()

### Community 162 - "_PreparedInputsManifest"
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
- **187 isolated node(s):** `release.sh script`, `wordwending`, `IPA_AUDIO`, `Locked Decisions (from grilling)`, `Global Constraints` (+182 more)
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
- **Why does `BundlePage` connect `BundlePage` to `models/__init__.py`, `test_document_export.py`, `CoordinateSpace`, `test_evaluation_service.py`, `services/evaluation.py`, `._write_page_evaluation_and_manifest`, `model_validator`, `cli.py`, `services/merge.py`, `._write_page_xml`, `PageXmlInterchangeService`, `test_merge_review.py`, `test_ocr_models.py`, `test_page_interchange.py`, `ReviewOverlayService`, `DocumentExportService`, `_AssembleExecution`, `test_bakeoff.py`, `MergeOrchestrator`, `._build_region_chunk`, `.score`, `ReviewTask`, `NoteRecord`, `test_merge_service.py`, `ReviewScope`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `services/preparation.py`, `RunnerExecutionPolicy`, `RunnerThroughputSummary`, `test_document_export.py`, `PageClass`, `BundleLayoutService`, `CoordinateSpace`, `test_evaluation_service.py`, `services/evaluation.py`, `services/merge.py`, `ResumeLedgerService`, `BundlePaths`, `test_merge_review.py`, `PreparationRecipe`, `PagePreparationOverride`, `SpanRecord`, `test_runner_execution.py`, `test_assemble.py`, `PlannedRunnerBatch`, `evaluation_cohorts.py`, `test_bakeoff.py`, `BundlePage`, `HuggingFaceKrakenRunner`, `ReviewTask`, `NoteRecord`, `test_merge_service.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `test_cli_commands.py`, `TestCLIErrorHandling`, `TestCLIReview`, `RunnerThroughputSummary`, `cli`, `cli.py`, `TestCLIExport`, `TestCLISettings`, `TestConfiguration`, `Path`, `.validate_https_huggingface_endpoints`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `BundlePage` (e.g. with `BakeoffCandidate` and `BakeoffInvocationOutcome`) actually correct?**
  _`BundlePage` has 19 INFERRED edges - model-reasoned connections that need verification._