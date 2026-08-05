# Graph Report - bochord  (2026-08-05)

## Corpus Check
- 124 files · ~177,297 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2811 nodes · 7311 edges · 133 communities (112 shown, 21 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 559 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3bc4c389`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/merge.py
- SpanRecord
- QualitySignal
- PlannedRunnerBatch
- RunnerReference
- BundlePage
- Image
- test_bundle_layout.py
- test_evaluation_service.py
- Detailed OCR Process
- RunnerThroughputSummary
- test_text_normalization.py
- AlternateCandidate
- models/__init__.py
- test_preparation_service.py
- BundlePaths
- HuggingFaceOlmocrRunner
- ADR 0010 Structured Output Boundary
- SourceAcquisitionService
- _SpanCandidate
- check_napoleon_gate.py
- Path
- test_olmocr_runner.py
- BT Witness Preparation Slice
- TestConfiguration
- PageEvaluationSummary
- RunnerInputPackager
- source_acquisition.py
- _NoteCandidate
- MergeOrchestrator
- Path
- test_page_interchange.py
- _stable_json_schema
- test_document_export.py
- test_runner_execution.py
- model_validator
- test_review_overlay.py
- ._coords
- RunnerCapability
- PageXmlInterchangeService
- _bundle_page_payload
- services/evaluation.py
- RunnerBatchPlanner
- cli
- cli.py
- Settings
- services/preparation.py
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- test_ocr_models.py
- _parse_native_corrected
- TestCLISettings
- test_cli_utils.py
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- print_error
- _pixel_access
- Preparation Gold Specs
- Raw OCR witness layer
- CLI Progress Utils
- Spec 0002: V1 Bundle Layout and Data Shape
- Spec 0005: Human Markup and Review
- Coding Standards Docs
- RagChunk
- model_validator
- ADR 0009 OCR-D PAGE eScriptorium
- Spec 0006: Exports and Retrieval Views
- _border_shadow_signal
- .settings_customise_sources
- Normalized Page Graph
- Configuration: Command Line Tool
- Anglian dialect group
- TestCLIVersion
- .validate_item_page_alignment
- Learner lacks stable conceptual map of sound-change order
- OE Grammar Resources
- test_merge_service.py
- ADR 0004 Layered Truth
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- TestCLIErrorHandling
- Spec 0016 RAG Line Contract Follow-up Implementation Plan
- TestConsoleQuietMode
- Point
- valid_bundle_page
- _median_text_height_signal
- Sphinx Docs Index
- Lesson 0003 Pronouncing Old English Letters
- MockHttpxClient
- .validate_https_huggingface_endpoints
- Page Graph Line
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- ._pick_scaffold_witness
- ._write_page_xml
- _measure_skew_degrees
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
- OCR Evidence Not Philological Semantics
- ADR 0002 Bundle Model
- Page Bundle as Page-Local Truth Unit
- ADR 0003 Page Graph
- SourceProvenanceService
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- bochord
- Mixed dialect spellings from copying history
- Reference Sound Terms
- TestPrintSuccess
- PreparationBundleService
- test_write_document_exports_frozen_contract_jsonl_validates
- ._extend_unique
- _page_witnesses

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

## Communities (133 total, 21 thin omitted)

### Community 0 - "services/merge.py"
Cohesion: 0.07
Nodes (39): _apply_layout_merge_confidence(), _attach_alternates_to_objects(), _attach_layout_alternates(), _box_iou(), _collect_note_candidates(), _detect_structure_conflict(), _geometry_alternates_for_regions(), _matching_notes_for_witness() (+31 more)

### Community 1 - "SpanRecord"
Cohesion: 0.07
Nodes (52): MergeFlag, MergeFlagType, MergePageResult, PassWitnessPage, StrEnum, One material merge disagreement surfaced for human review., Accepted page graph plus merge flags and abstention state., Material merge disagreement categories emitted as review flags. (+44 more)

### Community 2 - "QualitySignal"
Cohesion: 0.16
Nodes (21): QualitySignal, One measured image-quality signal from preparation assessment., _bleedthrough_signal(), _colored_marking_signal(), _column_count_signal(), _contrast_signal(), _effective_dpi_signal(), _lower_page_ink_signal() (+13 more)

### Community 3 - "PlannedRunnerBatch"
Cohesion: 0.08
Nodes (52): BatchItemRef, BatchUnitKind, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Batch grouping units for runner execution., Runner packaging policies. (+44 more)

### Community 4 - "RunnerReference"
Cohesion: 0.14
Nodes (23): DocumentBundleManifest, On-disk document manifest for one Spec 0002 bundle., AcquisitionProvenance, BibliographicProvenance, DocumentEvaluationSummary, ExportSummary, Document-level grouped evaluation output., Top-level run metadata for one bundle export. (+15 more)

### Community 5 - "BundlePage"
Cohesion: 0.06
Nodes (63): BundlePage, EvaluationFamilySummary, EvaluationFlag, StrEnum, Canonical exported page object., Self-contained instructions and evidence binding for human review., Supported human review targets., Independent evidence dimensions a human may inspect and certify. (+55 more)

### Community 6 - "Image"
Cohesion: 0.13
Nodes (23): _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _crop_box(), _fill_color(), _load_source_image(), _maybe_crop() (+15 more)

### Community 7 - "test_bundle_layout.py"
Cohesion: 0.05
Nodes (73): page_dir_name(), Return the stable page directory name for one 1-based page number. Args:…, OverlayState, Current overlay state for one reviewable object., _accept_review_event(), load_export_minimal_bundle(), load_minimal_bundle(), Path (+65 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.09
Nodes (61): GoldCoverage, GoldNoteLink, GoldPageAnnotation, GoldRegionAnnotation, GoldTextSpan, Gold diplomatic and normalized text target., Gold region or structure target., Gold note-marker linkage target. (+53 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "RunnerThroughputSummary"
Cohesion: 0.06
Nodes (43): BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all bochord errors., RunnerEndpointUnavailable (+35 more)

### Community 11 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (43): LineJoinKind, LineJoinRecord, NoteMarkerNormalizedForm, model_validator, StrEnum, Unicode normalization form applied to diplomatic text., How inline note markers appear in normalized text., How superscript characters appear in normalized text. (+35 more)

### Community 12 - "AlternateCandidate"
Cohesion: 0.04
Nodes (70): AlternateCandidate, One rejected or alternate merge interpretation kept in provenance., AcceptReviewEvent, AnchoredGoldAnnotation, ChunkType, CorrectGeometryReviewEvent, CorrectStyleReviewEvent, DatasetSplit (+62 more)

### Community 13 - "models/__init__.py"
Cohesion: 0.06
Nodes (80): CoordinateSpace, CoordinateTransform, FlagSeverity, PageClass, PreparationMode, PreparedPage, BaseModel, Page-level layout cohorts used by preparation and evaluation. (+72 more)

### Community 14 - "test_preparation_service.py"
Cohesion: 0.11
Nodes (50): PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, dark_gutter_image() (+42 more)

### Community 15 - "BundlePaths"
Cohesion: 0.07
Nodes (49): BundlePaths, PageBundleManifest, On-disk page manifest for one Spec 0002 page bundle., Relative path helpers for one document bundle root. Args: root: Filesystem root…, Pointer from accepted graph content back to raw machine evidence., WitnessReference, _atomic_write_json(), _atomic_write_text() (+41 more)

### Community 16 - "HuggingFaceOlmocrRunner"
Cohesion: 0.07
Nodes (33): _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _load_direct_image(), _load_image_from_pdf(), Any, Image, Path (+25 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "SourceAcquisitionService"
Cohesion: 0.24
Nodes (20): _image_bounds_cover_page(), Copy or render source pages into a deterministic ``pages/`` layout., Check whether displayed image bounds cover enough of page bounds. Args: left:…, SourceAcquisitionService, pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional… (+12 more)

### Community 19 - "_SpanCandidate"
Cohesion: 0.07
Nodes (44): _apply_span_text_resolution(), _apply_span_typography_resolution(), _first_candidate_by_runner_precedence(), Any, Confidence, alternates, and flag callback for span-role resolution., Collect unique witness ids from span candidates in input order. Args:…, Collect unique runner ids from span candidates in input order. Args:…, Apply text agreement or disagreement resolution for one span. Args: span:… (+36 more)

### Community 20 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 21 - "Path"
Cohesion: 0.07
Nodes (19): Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page…, Return the page evaluation scores artifact path. Args: page_number: 1-based… (+11 more)

### Community 22 - "test_olmocr_runner.py"
Cohesion: 0.16
Nodes (36): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+28 more)

### Community 23 - "BT Witness Preparation Slice"
Cohesion: 0.05
Nodes (42): ExtractionOrchestrator, Project Structure (models/services/cli/settings), Single Responsibility Service Architecture, Dual Text Contract, Historical Character Preservation, LineJoinRecord, text-norm-v1 Policy, TextNormalizer (+34 more)

### Community 24 - "TestConfiguration"
Cohesion: 0.07
Nodes (21): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+13 more)

### Community 25 - "PageEvaluationSummary"
Cohesion: 0.10
Nodes (42): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+34 more)

### Community 26 - "RunnerInputPackager"
Cohesion: 0.24
Nodes (18): Bind batch planning, packaging, and hosted runner collaborators. Args: planner:…, Package one planned batch into a hosted-runner input artifact., RunnerInputPackager, bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``. (+10 more)

### Community 27 - "source_acquisition.py"
Cohesion: 0.10
Nodes (32): _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), _pdf_page_image(), Image, Path (+24 more)

### Community 28 - "_NoteCandidate"
Cohesion: 0.11
Nodes (32): _apply_note_link_resolution(), _map_marker_span_ids(), _mapped_note_link_sets(), _MarkerMappingContext, _min_merge_confidence(), _note_link_alternates(), _note_marker_links_from_mapped_sets(), _note_marker_links_when_mapping_ambiguous() (+24 more)

### Community 29 - "MergeOrchestrator"
Cohesion: 0.08
Nodes (20): _flagged_object_ids(), MergeOrchestrator, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Collect object ids already referenced by merge flags. Args: flags: Merge flags…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph…, Choose the accepted prepared page variant for this merge., Keep same-variant witnesses and record skipped cross-variant evidence., Pick one coordinate-rich structure scaffold and detect layout conflicts. (+12 more)

### Community 30 - "Path"
Cohesion: 0.22
Nodes (16): MockerFixture, binary_recipe(), bundle_service(), Path, Write a single-page source raster for bundle tests. Returns: Path to a…, Write a two-page image folder for multi-page bundle tests. Returns: Path to a…, Build a preparation bundle service wired to ``acquisition``. Args: acquisition:…, Load a binary/Otsu recipe variant for multi-recipe bundle tests. Keyword Args:… (+8 more)

### Community 31 - "test_page_interchange.py"
Cohesion: 0.12
Nodes (24): FontSlant, Visual font-slant classification independent of weight and role., _export_note_page(), _page_element(), Path, Export should round PAGE coordinates to importer-friendly integers., PAGE corrections should update text while sidecar evidence stays intact., PAGE diplomatic corrections should regenerate normalized span text. (+16 more)

### Community 32 - "_stable_json_schema"
Cohesion: 0.33
Nodes (6): Return Pydantic-generated JSON Schema with stable key ordering. Args:…, DocumentBundle JSON Schema must match the checked-in generated snapshot., RagDocument JSON Schema must match the checked-in generated snapshot., _stable_json_schema(), test_generated_schema_document_bundle_v1_matches_snapshot(), test_generated_schema_rag_document_v1_matches_snapshot()

### Community 33 - "test_document_export.py"
Cohesion: 0.04
Nodes (74): DocumentBundle, RagDocument, Canonical software-facing document export., Document-level retrieval export., Human-review trust level for accepted graph content., Orthogonal visual typography facets for one text span., Accepted region classes for the page graph., RegionKind (+66 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.20
Nodes (27): execution_service(), _fail_all_items(), _fail_second_item(), fixture_root(), hosted_result(), policy(), prepared_artifacts(), Path (+19 more)

### Community 35 - "model_validator"
Cohesion: 0.06
Nodes (17): model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Keep page-local page ids aligned with provenance. Returns: The validated page-…, Keep stitched page ids distinct and aligned with provenance. Returns: The…, Keep page-local and stitched retrieval references coherent. Returns: The…, Reject duplicate related ids and overlap with primary targets. Returns: The…, Require flag events to record concern without changing trust state. Returns:… (+9 more)

### Community 36 - "test_review_overlay.py"
Cohesion: 0.04
Nodes (73): CorrectTextReviewEvent, MarkIllegibleReviewEvent, PageOverlay, Event recording corrected diplomatic text., Event recording one-to-many structural region correction., Event recording that source content cannot be transcribed defensibly., Exact JSON shape for one page overlay file., Lifecycle state for a human review task. (+65 more)

### Community 37 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 38 - "RunnerCapability"
Cohesion: 0.14
Nodes (11): Declared pass-runner input and batching contract., RunnerCapability, Return the declared olmOCR input and batching contract. Returns: Hosted olmOCR…, InvokeResult, parametrize, Persisted batch status must agree with submitted and failed items., test_prepared_unit_rejects_missing_or_empty_lineage_fields(), test_spec_0013_runner_invariants_reject_invalid_payloads() (+3 more)

### Community 39 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 40 - "_bundle_page_payload"
Cohesion: 0.06
Nodes (37): Compact review state attached to accepted graph objects., ReviewSummary, _bundle_page_payload(), _page_witness(), _prepared_unit_ref(), _provenance(), Graph parent-child identifiers must resolve within the page., Return a prepared-unit artifact bound to page preparation context. (+29 more)

### Community 41 - "services/evaluation.py"
Cohesion: 0.04
Nodes (71): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., BaselineShift, FontWeight, GoldStyleSpan, Gold style target for one span or image-anchored area., Visual font-weight classification independent of other typography. (+63 more)

### Community 42 - "RunnerBatchPlanner"
Cohesion: 0.23
Nodes (22): Plan fixed runner batches from prepared artifacts and policy., RunnerBatchPlanner, Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), artifacts(), capability(), policy() (+14 more)

### Community 43 - "cli"
Cohesion: 0.09
Nodes (18): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test global CLI options., Test verbose flag is properly set. (+10 more)

### Community 44 - "cli.py"
Cohesion: 0.10
Nodes (31): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), _prepare_overrides(), prepare_pages(), _PreparedInputsManifest (+23 more)

### Community 45 - "Settings"
Cohesion: 0.20
Nodes (11): Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Settings, patch, Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., Test the run command., _run_cli_args() (+3 more)

### Community 46 - "services/preparation.py"
Cohesion: 0.14
Nodes (20): _build_prepared_units(), _column_ink_profile(), _column_unit_boxes(), _column_valley_centers(), _fixed_tile_boxes(), _prepared_unit_from_box(), Format a SHA-256 digest label for ``payload``. Args: payload: Bytes to hash.…, Persist ``image`` as PNG with fixed options and return its checksum. Side… (+12 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.05
Nodes (27): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events. (+19 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.15
Nodes (15): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Evidence-Bound Human Review, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy (+7 more)

### Community 50 - "test_ocr_models.py"
Cohesion: 0.05
Nodes (70): Multi-page provenance retained by retrieval exports., Cross-page retrieval chunk stitched from accepted page-local chunks., RetrievalProvenance, StitchedChunk, capability_payload(), execution_batch_payload(), _minimal_rag_document(), model_runner_payload() (+62 more)

### Community 51 - "_parse_native_corrected"
Cohesion: 0.21
Nodes (12): _line_unicode(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids., Import must fail when native export no longer matches the canonical package. (+4 more)

### Community 52 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 53 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): print_info(), print_success(), Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling. (+1 more)

### Community 54 - "main"
Cohesion: 0.23
Nodes (8): main(), patch, Tests for the main module., Test the main function., Test that main function calls the CLI., Test that main function can be imported and called., Test that main function exists and is callable., TestMain

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
Nodes (8): print_error(), Print error message with optional suggestions. Args: message: Error message…, Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError

### Community 59 - "_pixel_access"
Cohesion: 0.22
Nodes (11): _longest_dark_run(), _pixel_access(), Any, Return Pillow pixel access for ``image``. Args: image: Image whose pixels will…, Return the longest contiguous run of values below ``threshold``. Args: values:…, Mark rows whose longest dark run spans enough of the page width. Args: gray:…, Mark columns whose longest dark run spans enough of the page height. Args:…, Count sustained dark horizontal and vertical rules. Args: gray: Grayscale… (+3 more)

### Community 60 - "Preparation Gold Specs"
Cohesion: 0.17
Nodes (12): V1 Gold Data Expectations, Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Coordinate and Image Provenance, Page Subdivision into OCR Units, Preparation Pipeline Stage, Preparation Recipe, V1 Page Class Taxonomy (+4 more)

### Community 61 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 62 - "CLI Progress Utils"
Cohesion: 0.22
Nodes (8): create_progress(), Create a rich progress indicator for long-running operations. Returns:…, Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress

### Community 63 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.18
Nodes (11): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Review Overlays, V1 Typography and Role Vocabulary, Spec 0014: Review Task and Overlay Schema, correct_text Event Semantics, PageOverlay Append-Only Log, ReviewTask Packet (+3 more)

### Community 64 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0009: Merge and Alignment (+3 more)

### Community 65 - "Coding Standards Docs"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 66 - "RagChunk"
Cohesion: 0.27
Nodes (6): RagChunk, Page-local retrieval chunk., Emit one stitched chunk when a BODY run spans multiple pages. Args:…, Collect ordered distinct page ids from component chunks. Args: chunks: Region…, Union source object ids from component region chunks. Args: chunks: Region…, Union provenance pointers from component region chunks. Args: chunks: Region…

### Community 67 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 68 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.22
Nodes (9): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+1 more)

### Community 69 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 70 - "_border_shadow_signal"
Cohesion: 0.24
Nodes (10): _border_shadow_signal(), _gutter_shadow_signal(), _margin_strip_width(), Warn when ``value`` exceeds ``maximum``. Args: value: Measured value. maximum:…, Measure mean darkness ratio inside ``box``. Args: gray: Grayscale working…, Width of the 8% border/gutter strip in pixels. Args: width: Page width in…, Measure darkness of the center 8% vertical strip. Args: gray: Grayscale working…, Measure darkness of the left/right 8% vertical strips. Args: gray: Grayscale… (+2 more)

### Community 71 - ".settings_customise_sources"
Cohesion: 0.22
Nodes (6): BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, PydanticBaseSettingsSource, Test loading configuration with TOML file.

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

### Community 76 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 77 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 78 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 79 - "test_merge_service.py"
Cohesion: 0.06
Nodes (119): MergePageInput, MergePolicy, Versioned deterministic merge precedence and acceptance thresholds., Competing witness fragments prepared for single-page merge., BoundingBox, Axis-aligned rectangle for page-relative geometry., AbstainingMergeService, Initialize merge orchestration for one page. Args: policy: Versioned merge… (+111 more)

### Community 80 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Overlay Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 81 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.33
Nodes (6): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Historical Character Preservation, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts

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

### Community 86 - "Point"
Cohesion: 0.15
Nodes (11): Point, Complete replayable structural definition for a corrected region., Require resolvable geometry with a single coordinate-space identity. Returns:…, One point in an identified image coordinate space., RegionRevision, Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity. (+3 more)

### Community 87 - "valid_bundle_page"
Cohesion: 0.29
Nodes (7): Document page ids must stay unique., Source page_count must remain exact versus exported pages., Return a minimal valid page graph for join-reference tests., test_bundle_rejects_unknown_line_join_target(), test_document_bundle_rejects_duplicate_page_ids(), test_document_bundle_rejects_inexact_source_page_count(), valid_bundle_page()

### Community 88 - "_median_text_height_signal"
Cohesion: 0.25
Nodes (8): _median_text_height_signal(), Warn when ``value`` falls below ``minimum``. Args: value: Measured value.…, Mark rows that contain enough ink to count as text. Args: gray: Grayscale…, Collect lengths of contiguous ``True`` runs. Args: mask: Boolean sequence.…, Estimate median text-run height in source-image pixels. Args: gray: Grayscale…, _run_lengths(), _severity_min(), _text_row_mask()

### Community 89 - "Sphinx Docs Index"
Cohesion: 0.50
Nodes (5): API Models Autodoc, Changelog, Sphinx Docs Index, README, Read the Docs Config

### Community 90 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 91 - "MockHttpxClient"
Cohesion: 0.39
Nodes (5): MockHttpxClient, Any, BaseException, Response, Minimal httpx client stand-in for hosted runner tests.

### Community 92 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…, field_validator

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

### Community 98 - "._pick_scaffold_witness"
Cohesion: 0.33
Nodes (5): _coordinate_rich_line_count(), _first_witness_by_runner_preference(), Select one scaffold witness from structure-bearing candidates. Args:…, Pick the first eligible witness for the earliest preferred runner id. Args:…, Count lines carrying bounding boxes or baseline geometry. Args: witness: One…

### Community 99 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 100 - "_measure_skew_degrees"
Cohesion: 0.33
Nodes (6): _downsample_for_heuristics(), _measure_skew_degrees(), Estimate page skew degrees via row-projection variance. Args: gray: Grayscale…, Downsample so the longest edge is at most ``_HEURISTIC_MAX_EDGE_PX``. Args:…, Compute variance of per-row ink sums. Args: gray: Grayscale page image.…, _row_projection_variance()

### Community 101 - "ADR 0008 Stable IDs and Review History"
Cohesion: 0.67
Nodes (3): ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States

### Community 102 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 128 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 129 - "PreparationBundleService"
Cohesion: 0.50
Nodes (3): PreparationBundleService, Acquire source pages and persist per-page preparation bundles. Args:…, Bind acquisition and per-page preparation collaborators. Args:…

### Community 130 - "test_write_document_exports_frozen_contract_jsonl_validates"
Cohesion: 0.50
Nodes (4): load_frozen_document_bundle_v1(), Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the frozen document-bundle-v1 contract fixture., test_write_document_exports_frozen_contract_jsonl_validates()

## Ambiguous Edges - Review These
- `README` → `Sphinx Docs Index`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to
- `Frequently Asked Questions` → `Quickstart CLI Entry Points`  [AMBIGUOUS]
  doc/source/overview/faq.rst · relation: conceptually_related_to
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to

## Knowledge Gaps
- **127 isolated node(s):** `release.sh script`, `bochord`, `IPA_AUDIO`, `Global Constraints`, `Exact Invariant Matrix` (+122 more)
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
- **Why does `BundlePage` connect `BundlePage` to `services/merge.py`, `SpanRecord`, `RunnerReference`, `test_evaluation_service.py`, `test_text_normalization.py`, `AlternateCandidate`, `models/__init__.py`, `BundlePaths`, `MergeOrchestrator`, `test_page_interchange.py`, `test_document_export.py`, `PageXmlInterchangeService`, `_bundle_page_payload`, `services/evaluation.py`, `cli.py`, `test_ocr_models.py`, `test_merge_service.py`, `valid_bundle_page`, `._write_page_xml`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `AlternateCandidate` connect `AlternateCandidate` to `services/merge.py`, `SpanRecord`, `PlannedRunnerBatch`, `RunnerReference`, `BundlePage`, `test_bundle_layout.py`, `test_evaluation_service.py`, `RunnerThroughputSummary`, `models/__init__.py`, `BundlePaths`, `_SpanCandidate`, `PageEvaluationSummary`, `_NoteCandidate`, `test_page_interchange.py`, `test_document_export.py`, `test_review_overlay.py`, `RunnerCapability`, `_bundle_page_payload`, `services/evaluation.py`, `test_ocr_models.py`, `RagChunk`, `test_merge_service.py`, `Point`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `SpanRecord`, `QualitySignal`, `PlannedRunnerBatch`, `RunnerReference`, `BundlePage`, `test_bundle_layout.py`, `test_evaluation_service.py`, `RunnerThroughputSummary`, `test_text_normalization.py`, `AlternateCandidate`, `BundlePaths`, `PageEvaluationSummary`, `test_document_export.py`, `test_review_overlay.py`, `RunnerCapability`, `_bundle_page_payload`, `services/evaluation.py`, `test_ocr_models.py`, `RagChunk`, `test_merge_service.py`, `Point`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 94 inferred relationships involving `AlternateCandidate` (e.g. with `BundlePage` and `CoordinateSpace`) actually correct?**
  _`AlternateCandidate` has 94 INFERRED edges - model-reasoned connections that need verification._