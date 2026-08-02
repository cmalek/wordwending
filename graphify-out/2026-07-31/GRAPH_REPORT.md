# Graph Report - bochord  (2026-07-31)

## Corpus Check
- 102 files · ~274,908 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2298 nodes · 5972 edges · 121 communities (109 shown, 12 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 559 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a717e91b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models/__init__.py
- test_preparation_service.py
- MergeOrchestrator
- test_olmocr_runner.py
- test_evaluation_service.py
- test_runner_execution.py
- test_cli_utils.py
- PageEvaluationSummary
- _ItemInvokeResult
- PageClass
- Settings
- cli.py
- check_napoleon_gate.py
- model_validator
- services/preparation.py
- test_merge_service.py
- PageXmlInterchangeService
- test_page_interchange.py
- TestOcrModels
- cli
- services/merge.py
- services/evaluation.py
- _RateAccumulator
- PreparationRecipe
- source_page
- TestCLIGlobalOptions
- RunnerBatchPlanner
- Diplomatic Text Review
- test_bundle_layout.py
- ._write_page_evaluation_and_manifest
- test_text_normalization.py
- Detailed OCR Process
- BundleLayoutService
- Architecture Index
- Machine Assistance Resources
- TestCLIRun
- BundlePage
- _parse_native_corrected
- Spec 0007: PDF-to-Image Preparation
- Spec 0004: Ordered V1 Implementation
- Phase 1 PAGE Interoperability Spike Plan
- i-mutation / i-umlaut
- conftest.py
- ._coords
- ._write_page_xml
- Raw OCR witness layer
- MetricProfile
- BundlePaths
- Python Coding Standards
- Hugging Face Setup Runbook
- Spec 0002: V1 Bundle Layout and Data Shape
- Separate Text Structure Style Score Families
- Bundle JSON Export
- DocumentRunOrchestrator
- Gold Annotation Protocol
- model_validator
- Anglian dialect group
- prepare_pages
- Review Overlay
- ADR 0009 OCR-D PAGE eScriptorium
- Pass Runner
- Normalized Page Graph
- AGENTS.md
- Configuration: Command Line Tool
- SourceAcquisitionService
- RunnerInputPackager
- Page Graph
- PagePreparationService
- Learner lacks stable conceptual map of sound-change order
- Spec 0005: Human Markup and Review
- test_ocr_models.py
- ADR 0004 Layered Truth
- Reference 0006 OCR Output Formats
- OE Grammar Resources
- EvaluationFamilySummary
- DocumentBundle
- print_error
- Lesson 0003 Pronouncing Old English Letters
- .validate_https_huggingface_endpoints
- ADR 0005 Evaluation First
- Guide to Old English Textbook
- Chris Malek
- Bibliographic Provenance
- Character Error Rate (CER)
- Machine Assistance Mission
- .validate_item_page_alignment
- create_progress
- release.sh
- Contributor Covenant 3.0
- Accepted Page Graph
- Old English Morphological Analysis Tool
- Worked BT entry example: abbad
- Old English c/g palatalization
- OE tēon walk-back (Grimm + h-loss + contraction)
- ipa-play.js
- bochord
- Mixed dialect spellings from copying history
- Reference Sound Terms
- ._pick_scaffold_witness
- _aggregate_family
- Spec 0002 V1 Bundle Layout Implementation Plan
- Spec 0008 Text and Normalization Implementation Plan
- Spec 0009 Merge and Alignment Implementation Plan
- Spec 0013 Pass-Runner Interface Schema Implementation Plan
- PlannedRunnerBatch
- MockHttpxClient
- _subdivision_boxes
- PreparationBundleService
- .get_config_paths
- TestPrintSuccess
- TestConsoleQuietMode
- dense_source_page
- TestConsole
- .test_settings_field_descriptions
- _persist_prepared_page

## God Nodes (most connected - your core abstractions)
1. `AlternateCandidate` - 114 edges
2. `SchemaModel` - 99 edges
3. `MergePolicy` - 54 edges
4. `BundlePage` - 53 edges
5. `SpanRecord` - 50 edges
6. `CoordinateSpace` - 49 edges
7. `PageClass` - 48 edges
8. `BundlePaths` - 47 edges
9. `MergePageInput` - 47 edges
10. `PreparationMode` - 47 edges

## Surprising Connections (you probably didn't know these)
- `Coverage Metric for OCR Comparison` --semantically_similar_to--> `GoldCoverage`  [INFERRED] [semantically similar]
  sources/I Spent the Summer Testing 14 OCR Engines _ by Ida Silfverskiöld _ Jul, 2026 _ Level Up Coding.pdf → doc/source/runbook/gold_annotation.rst
- `OCR Is a Routing and Evaluation Problem` --semantically_similar_to--> `Separate Text Structure Style Score Families`  [INFERRED] [semantically similar]
  sources/I Spent the Summer Testing 14 OCR Engines _ by Ida Silfverskiöld _ Jul, 2026 _ Level Up Coding.pdf → doc/source/runbook/ocr_process.rst
- `Derived Graph Layer` --semantically_similar_to--> `Page Graph`  [INFERRED] [semantically similar]
  doc/source/architecture/adr_0004_layered_artifacts.rst → CONTEXT.md
- `README` --semantically_similar_to--> `Sphinx Docs Index`  [AMBIGUOUS] [semantically similar]
  README.md → doc/source/index.rst
- `Reject Keyser Metathesis and Vowel Deletion` --conceptually_related_to--> `Note-Heavy Page page-0010`  [AMBIGUOUS]
  sources/Kiparsky-PhonologyOldEnglish-1976.pdf → doc/source/runbook/gold_annotation.rst

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Tooling Preflight Workflow** — code_index_tool, graphify_tool, context7_tool, package_registry_mcp_tool [EXTRACTED 1.00]
- **Post-Implementation Quality Gate** — ruff_tool, mypy_tool, napoleon_gate [EXTRACTED 1.00]
- **bochord Project Architecture** — bochord_models, bochord_services, bochord_cli, bochord_settings [EXTRACTED 1.00]
- **Four-Layer Truth Model** — doc_source_architecture_adr_0004_layered_truth_raw_witness_layer, doc_source_architecture_adr_0004_layered_truth_derived_graph_layer, doc_source_architecture_adr_0004_layered_truth_overlay_layer, doc_source_architecture_adr_0004_layered_truth_export_layer [EXTRACTED 1.00]
- **V1 Page Graph Node Kinds** — doc_source_architecture_adr_0003_page_graph_region, doc_source_architecture_adr_0003_page_graph_line, doc_source_architecture_adr_0003_page_graph_span, doc_source_architecture_adr_0003_page_graph_note [EXTRACTED 1.00]
- **V1 Core Service Collaborators** — doc_source_architecture_spec_0001_system_architecture_document_run_orchestrator, doc_source_architecture_spec_0001_system_architecture_page_preparation_service, doc_source_architecture_spec_0001_system_architecture_pass_runner_registry, doc_source_architecture_spec_0001_system_architecture_page_alignment_service, doc_source_architecture_spec_0001_system_architecture_page_graph_builder, doc_source_architecture_spec_0001_system_architecture_evaluation_service, doc_source_architecture_spec_0001_system_architecture_overlay_service, doc_source_architecture_spec_0001_system_architecture_bundle_writer [EXTRACTED 1.00]
- **Evidence-Preserving Text Pipeline** — doc_source_architecture_spec_0008_text_normalization_dual_text, doc_source_architecture_spec_0005_human_markup_diplomatic_text, doc_source_architecture_spec_0014_review_overlay_schema_correct_text [INFERRED 0.85]
- **Runner Execution Contract Stack** — doc_source_architecture_spec_0012_runner_execution_and_batching_batch_policy, doc_source_architecture_spec_0013_pass_runner_interface_schema_runner_capability, doc_source_architecture_spec_0013_pass_runner_interface_schema_execution_batch, doc_source_architecture_spec_0012_runner_execution_and_batching_hugging_face [INFERRED 0.85]
- **End-to-End bochord OCR Pipeline Stages** — doc_source_runbook_ocr_process_stage_acquire_source, doc_source_runbook_ocr_process_stage_pdf_to_image, doc_source_runbook_ocr_process_stage_competing_passes, doc_source_runbook_ocr_process_stage_align_evidence, doc_source_runbook_ocr_process_stage_page_graph, doc_source_runbook_ocr_process_stage_evaluate_gold, doc_source_runbook_ocr_process_stage_apply_overlays, doc_source_runbook_ocr_process_stage_export [EXTRACTED 1.00]
- **Spec Completion Sequence 0003→0007→0010→0012** — docs_superpowers_plans_2026_07_25_spec_0003_evaluation_schema_completion_document, docs_superpowers_plans_2026_07_25_spec_0007_preparation_completion_document, docs_superpowers_plans_2026_07_25_spec_0010_page_classification_cohorts_document, docs_superpowers_plans_2026_07_25_spec_0012_runner_execution_batching_document [EXTRACTED 1.00]
- **Evidence Preservation Layers** — doc_source_runbook_ocr_process_ocr_as_evidence, doc_source_runbook_operator_notes_preserve_run_artifacts, teaching_machine_assistance_notes_evidence_layer_separation, doc_source_runbook_ocr_process_stage_apply_overlays [INFERRED 0.85]
- **Witness-preserving OCR-to-structure workflow** — teaching_machine_assistance_lessons_0004_seven_stage_pipeline, teaching_machine_assistance_lessons_0004_raw_witness_layer, teaching_machine_assistance_lessons_0004_overlay_layer, teaching_machine_assistance_lessons_0004_normalized_export_layer, teaching_machine_assistance_lessons_0004_review_by_exception, teaching_machine_assistance_lessons_0006_entry_block_unit [EXTRACTED 1.00]
- **PIE to OE sound-change layering timeline** — teaching_oe_grammar_lessons_0001_proto_indo_european, teaching_oe_grammar_lessons_0001_grimms_law, teaching_oe_grammar_lessons_0001_verners_law, teaching_oe_grammar_lessons_0001_proto_germanic, teaching_oe_grammar_lessons_0001_i_mutation, teaching_oe_grammar_reference_0001_sound_change_order [EXTRACTED 1.00]
- **OE dialect recognition cue system** — teaching_oe_grammar_lessons_0002_west_saxon, teaching_oe_grammar_lessons_0002_anglian, teaching_oe_grammar_lessons_0002_kentish, teaching_oe_grammar_lessons_0002_mercian, teaching_oe_grammar_lessons_0002_northumbrian, teaching_oe_grammar_reference_0004_dialect_cue_table [EXTRACTED 1.00]

## Communities (121 total, 12 thin omitted)

### Community 0 - "models/__init__.py"
Cohesion: 0.04
Nodes (138): AlternateCandidate, MergeFlag, MergeFlagType, MergePageResult, PassWitnessPage, StrEnum, One material merge disagreement surfaced for human review., Accepted page graph plus merge flags and abstention state. (+130 more)

### Community 1 - "test_preparation_service.py"
Cohesion: 0.15
Nodes (39): PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, MockerFixture (+31 more)

### Community 2 - "MergeOrchestrator"
Cohesion: 0.05
Nodes (45): _apply_note_link_resolution(), _mapped_note_link_sets(), _MarkerMappingContext, MergeOrchestrator, _note_link_alternates(), _note_marker_links_from_mapped_sets(), _note_marker_links_when_mapping_ambiguous(), _NoteCandidate (+37 more)

### Community 3 - "test_olmocr_runner.py"
Cohesion: 0.16
Nodes (36): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+28 more)

### Community 4 - "test_evaluation_service.py"
Cohesion: 0.11
Nodes (52): BoundingBox, GoldCoverage, GoldLineJoin, GoldTextSpan, Gold diplomatic and normalized text target., Gold line-join annotation for hyphenation and continuation decisions., Explicit evaluation denominator and exclusion scope for a gold slice., Axis-aligned rectangle for page-relative geometry. (+44 more)

### Community 5 - "test_runner_execution.py"
Cohesion: 0.15
Nodes (33): HostedInvocationResult, Raw result returned from one hosted runner invocation., InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root() (+25 more)

### Community 6 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): print_info(), print_success(), Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling. (+1 more)

### Community 7 - "PageEvaluationSummary"
Cohesion: 0.18
Nodes (23): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+15 more)

### Community 8 - "_ItemInvokeResult"
Cohesion: 0.08
Nodes (28): _encode_png_base64(), _failed_item_result(), _ItemInvokeResult, _load_direct_image(), _load_image_from_pdf(), Any, Image, Path (+20 more)

### Community 9 - "PageClass"
Cohesion: 0.09
Nodes (48): _prepare_overrides(), Validate and convert optional CLI override values. Args: mode: Optional…, FlagSeverity, PageClass, PreparationMode, Page-level layout cohorts used by preparation and evaluation., Prepared-page subdivision modes., Supported top-level source kinds. (+40 more)

### Community 10 - "Settings"
Cohesion: 0.08
Nodes (26): BaseSettings, Load settings from file with cascading configuration. Args: config_file:…, Application settings with cascading configuration support. Note: The app_name…, Settings, Exception, PydanticBaseSettingsSource, patch, Unit tests for configuration settings. Tests the new OpenAI and summary… (+18 more)

### Community 11 - "cli.py"
Cohesion: 0.05
Nodes (49): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``bochord run``., BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail. (+41 more)

### Community 12 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 13 - "model_validator"
Cohesion: 0.08
Nodes (13): model_validator, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Require at least one concrete replacement geometry. Returns: The validated…, Bind events to valid tasks, evidence revisions, targets, and actions. Returns:…, Require a resolvable anchor and explain every scoring exclusion. Returns: The…, Require an explanation for every scoring exclusion. Returns: The validated…, Require an explicit scope and explain every scoring exclusion. Returns: The… (+5 more)

### Community 14 - "services/preparation.py"
Cohesion: 0.05
Nodes (90): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., AssessmentThresholds, BaseModel, Calibratable limits for deterministic image-quality heuristics., _adaptive_binary(), _apply_binarize(), _apply_color_mode() (+82 more)

### Community 15 - "test_merge_service.py"
Cohesion: 0.07
Nodes (105): MergePageInput, MergePolicy, Versioned deterministic merge precedence and acceptance thresholds., Competing witness fragments prepared for single-page merge., AbstainingMergeService, Stateless facade: merge one page of competing witnesses. Args: text_normalizer:…, Merge competing witness fragments into one accepted page graph. Args:…, _aligned_text_witnesses() (+97 more)

### Community 16 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 17 - "test_page_interchange.py"
Cohesion: 0.14
Nodes (22): _export_note_page(), _page_element(), Path, Export should round PAGE coordinates to importer-friendly integers., PAGE corrections should update text while sidecar evidence stays intact., PAGE diplomatic corrections should regenerate normalized span text., Import should fail when PAGE XML drops a canonical region id., Import should fail when PAGE XML repeats a canonical line id. (+14 more)

### Community 18 - "TestOcrModels"
Cohesion: 0.10
Nodes (13): parametrize, Return fields required by every review event., Contract checks for persisted OCR schema models., Review-event schema should discriminate on ``action``., A review task should be actionable without undocumented context., Boxes must represent a positive-area rectangle., Preferred input must be one of the runner's accepted inputs., Gold text without a graph target or geometry cannot be scored. (+5 more)

### Community 19 - "cli"
Cohesion: 0.06
Nodes (22): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test eval writes deterministic PageEvaluationSummary JSON., Test the prepare command. (+14 more)

### Community 20 - "services/merge.py"
Cohesion: 0.04
Nodes (88): Orthogonal visual typography facets for one text span., Semantic role kept separate from visual typography., TextRole, Typography, _apply_layout_merge_confidence(), _apply_span_text_resolution(), _apply_span_typography_resolution(), _box_iou() (+80 more)

### Community 21 - "services/evaluation.py"
Cohesion: 0.11
Nodes (22): GoldNoteLink, Gold note-marker linkage target., Independent evidence dimensions a human may inspect and certify., ReviewDimension, _boxes_intersect(), _coverage_allows(), _edit_distance(), _graphemes() (+14 more)

### Community 22 - "_RateAccumulator"
Cohesion: 0.08
Nodes (26): EvaluationFlag, GoldStyleSpan, Gold style target for one span or image-anchored area., One review-driving evaluation flag., _facet_match(), _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:… (+18 more)

### Community 23 - "PreparationRecipe"
Cohesion: 0.09
Nodes (38): PreparationRecipe, One acquired source page before preparation., Deterministic page-preparation profile., SourcePageArtifact, _ensure_supported_recipe(), Reject recipe modes that are intentionally unsupported today. Args: recipe:…, _artifact_from_raster(), _image_dpi() (+30 more)

### Community 24 - "source_page"
Cohesion: 0.13
Nodes (23): dark_gutter_image(), note_heavy_image(), Image, Build a source-page artifact backed by a written PNG. Keyword Args: dpi:…, Index quality signals by ``signal_id``. Args: signals: Measured quality signals…, Build a page of horizontal text-like bars, then rotate it. Keyword Args:…, Build a page with a dark vertical gutter in the center strip. Returns:…, Build a mostly flat page with dense salt-and-pepper noise. Returns: Grayscale… (+15 more)

### Community 25 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 26 - "RunnerBatchPlanner"
Cohesion: 0.19
Nodes (24): Declared pass-runner input and batching contract., RunnerCapability, Return the declared olmOCR input and batching contract. Returns: Hosted olmOCR…, Plan fixed runner batches from prepared artifacts and policy., RunnerBatchPlanner, Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), artifacts() (+16 more)

### Community 27 - "Diplomatic Text Review"
Cohesion: 0.29
Nodes (7): Diplomatic Text Review, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0014: Review Task and Overlay Schema, correct_text Event Semantics, ReviewTask Packet

### Community 28 - "test_bundle_layout.py"
Cohesion: 0.15
Nodes (26): DocumentBundleManifest, page_dir_name(), PageBundleManifest, Return the stable page directory name for one 1-based page number. Args:…, On-disk document manifest for one Spec 0002 bundle., On-disk page manifest for one Spec 0002 page bundle., AcquisitionProvenance, BibliographicProvenance (+18 more)

### Community 29 - "._write_page_evaluation_and_manifest"
Cohesion: 0.08
Nodes (27): _atomic_write_json(), _atomic_write_text(), _collect_page_flags(), Any, Path, Choose the page manifest source image path. Prefer ``source/pages/`` when a…, Return the overlay state manifest pointer when the artifact exists. Args: root:…, Atomically rewrite one page manifest. Side Effects: Replaces ``pages/page-… (+19 more)

### Community 30 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (43): bochord.models Package, LineJoinKind, LineJoinRecord, NoteMarkerNormalizedForm, model_validator, StrEnum, Unicode normalization form applied to diplomatic text., How inline note markers appear in normalized text. (+35 more)

### Community 31 - "Detailed OCR Process"
Cohesion: 0.23
Nodes (17): Detailed OCR Process, Kraken Runner, OCR Produces Evidence, Philological Watchlists, Stage 4 Align Evidence, Stage 7 Apply Overlays, Stage 3 Competing OCR Passes, Stage 6 Evaluate Against Gold (+9 more)

### Community 32 - "BundleLayoutService"
Cohesion: 0.09
Nodes (37): AcceptReviewEvent, OverlayState, Current overlay state for one reviewable object., Event recording unchanged human acceptance., BundleLayoutService, Write and read Spec 0002 document bundle trees., _accept_review_event(), load_minimal_bundle() (+29 more)

### Community 33 - "Architecture Index"
Cohesion: 0.17
Nodes (16): bochord Context, bochord, Image-First OCR Orchestration, Preparation Recipe, Witness Production, API Models Autodoc, ADR 0001 Package Boundary, OCR Evidence Not Philological Semantics (+8 more)

### Community 34 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 35 - "TestCLIRun"
Cohesion: 0.39
Nodes (5): patch, Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIRun

### Community 36 - "BundlePage"
Cohesion: 0.16
Nodes (14): BundlePage, GoldPageAnnotation, Canonical exported page object., Gold data slice for one page., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold…, Aggregate note-linkage success for covered gold edges. Args: prediction:…, Map predicted note ids to gold region annotation ids that name them. Args:… (+6 more)

### Community 37 - "_parse_native_corrected"
Cohesion: 0.21
Nodes (12): _line_unicode(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids., Import must fail when native export no longer matches the canonical package. (+4 more)

### Community 38 - "Spec 0007: PDF-to-Image Preparation"
Cohesion: 0.12
Nodes (17): Spec 0003: V1 Evaluation Schema, V1 Gold Data Expectations, Evaluation Review Flags, Evaluation Score Families, Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Coordinate and Image Provenance, Page Subdivision into OCR Units (+9 more)

### Community 39 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.18
Nodes (13): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy, Hugging Face Deployment Target (+5 more)

### Community 40 - "Phase 1 PAGE Interoperability Spike Plan"
Cohesion: 0.22
Nodes (13): Note-Heavy Page page-0010, Dictionary Headword Page page-0100, BundlePage Canonical JSON, Phase 1 PAGE Interoperability Spike Plan, PageXmlInterchangeService, Reject ocrd-models for Spike, Spec 0010 Page Classification Cohorts Plan, Weighted Evaluation Cohorts (+5 more)

### Community 41 - "i-mutation / i-umlaut"
Cohesion: 0.23
Nodes (13): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+5 more)

### Community 42 - "conftest.py"
Cohesion: 0.21
Nodes (12): cli_context(), mock_console(), mock_settings(), fixture, Test configuration and fixtures for the ai-coding project. This file contains…, Create a CLI runner for testing., Create a temporary directory for testing., Create a mock console for testing. (+4 more)

### Community 43 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 44 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 45 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 46 - "MetricProfile"
Cohesion: 0.13
Nodes (16): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., GoldRegionAnnotation, Gold region or structure target., _box_iou(), Return intersection-over-union for two axis-aligned boxes. Args: left: First…, Score gold FOOTNOTE regions under exhaustive STRUCTURE coverage. Args:… (+8 more)

### Community 47 - "BundlePaths"
Cohesion: 0.08
Nodes (23): BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page… (+15 more)

### Community 48 - "Python Coding Standards"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 49 - "Hugging Face Setup Runbook"
Cohesion: 0.31
Nodes (11): Client-Side Queue for Cold Starts, Custom OCR Container, Hugging Face Setup Runbook, Hugging Face Inference Endpoints, Immutable Model Commit Pinning, Local Laptop Boundary, RunnerReference Provenance, olmOCR Runner (+3 more)

### Community 50 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.20
Nodes (10): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Review Overlays, V1 Typography and Role Vocabulary, Evidence-Bound Human Review, PageOverlay Append-Only Log, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence (+2 more)

### Community 51 - "Separate Text Structure Style Score Families"
Cohesion: 0.20
Nodes (10): GoldCoverage, Separate Text Structure Style Score Families, Spec 0003 Evaluation Schema Completion Plan, StyleEvaluationSummary, watchlist_exact_match_rate, Spec 0007 Preparation Completion Plan, Preparation Recipe Variants, Coverage Metric for OCR Comparison (+2 more)

### Community 52 - "Bundle JSON Export"
Cohesion: 0.31
Nodes (9): Bundle JSON Export, Markdown Export, RAG JSON Export, Spec 0006: Exports and Retrieval Views, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 53 - "DocumentRunOrchestrator"
Cohesion: 0.25
Nodes (9): Document Bundle, Page Bundle, Page-Local Truth, ADR 0002 Bundle Model, Page Bundle as Page-Local Truth Unit, BundleWriter, DocumentRunOrchestrator, PageAlignmentService (+1 more)

### Community 54 - "Gold Annotation Protocol"
Cohesion: 0.33
Nodes (9): EvaluationService, bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, GoldDocument, MetricProfile, Phase 2 Gold Evaluator Plan, GoldLineJoin (+1 more)

### Community 55 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 56 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 57 - "prepare_pages"
Cohesion: 0.11
Nodes (26): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), prepare_pages(), Path, Print the some version info of this package, (+18 more)

### Community 58 - "Review Overlay"
Cohesion: 0.29
Nodes (8): Append-Only Review History, Review Overlay, Trust State, Overlay Layer, ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States, OverlayService

### Community 59 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.25
Nodes (8): Hosted Inference Boundary, PAGE Interchange, ADR 0007 V1 Engine Strategy, Hugging Face Hosted Endpoints, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE, OCR-D/eScriptorium Round-Trip Spike

### Community 60 - "Pass Runner"
Cohesion: 0.29
Nodes (8): Pass Family, Pass Runner, ADR 0006 Pass Runner Plugins, Pass Runner Common Interface, V1 Engine Bake-Off, kraken Candidate, olmocr Candidate, PassRunnerRegistry

### Community 61 - "Normalized Page Graph"
Cohesion: 0.29
Nodes (8): Normalized Page Graph, Footnote Chunk, Spec 0011: Structured Output Strategy, Standard OCR Intermediate Structure, TEI Dictionaries Chapter, TEI P5 as Downstream Reference, Domain Language, Shared Domain Glossary

### Community 62 - "AGENTS.md"
Cohesion: 0.09
Nodes (23): bochord.cli Package, main(), bochord.services Package, DdlExtractor, ExtractionOrchestrator, RunStats, bochord Virtual Environment, boto3 Library (+15 more)

### Community 63 - "Configuration: Command Line Tool"
Cohesion: 0.39
Nodes (8): Configuration: Command Line Tool, CLI Configuration Cascade, Frequently Asked Questions, Installation, Python 3.10+ Installation, Quickstart Guide, Quickstart CLI Entry Points, Using the Command Line Interface

### Community 64 - "SourceAcquisitionService"
Cohesion: 0.24
Nodes (20): _image_bounds_cover_page(), Copy or render source pages into a deterministic ``pages/`` layout., Check whether displayed image bounds cover enough of page bounds. Args: left:…, SourceAcquisitionService, pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional… (+12 more)

### Community 65 - "RunnerInputPackager"
Cohesion: 0.28
Nodes (17): Package one planned batch into a hosted-runner input artifact., RunnerInputPackager, bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests. (+9 more)

### Community 66 - "Page Graph"
Cohesion: 0.43
Nodes (7): Page Graph, Shared Page Coordinates, ADR 0003 Page Graph, Page Graph Line, Page Graph Note, Page Graph Region, Page Graph Span

### Community 67 - "PagePreparationService"
Cohesion: 0.38
Nodes (7): PagePreparationService, Stage 1 Acquire Source, Stage 2 PDF-to-Image Preparation, When To Rerun vs Rebuild, Phase 3 Acquisition Preparation Plan, Pillow and pypdfium2 Stack, SourceAcquisitionService

### Community 68 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 69 - "Spec 0005: Human Markup and Review"
Cohesion: 0.29
Nodes (7): Spec 0005: Human Markup and Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0009: Merge and Alignment, Abstaining Merge Policy, Machine/Merge/Trust Confidence Triad, Structure Scaffold Selection

### Community 70 - "test_ocr_models.py"
Cohesion: 0.08
Nodes (25): capability_payload(), execution_batch_payload(), model_runner_payload(), Return a valid model-backed runner payload with optional overrides., Return a valid runner capability payload with optional overrides., Return a valid runner execution batch payload with optional overrides., Return a valid preparation-recipe payload with optional overrides., Existing provenance fixtures stay valid without alternate candidates. (+17 more)

### Community 71 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): Raw Witness Artifact, ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 72 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 73 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 74 - "EvaluationFamilySummary"
Cohesion: 0.24
Nodes (15): EvaluationFamilySummary, MetricScore, One numeric evaluation metric., Scores and flags for one evaluation family., EvaluationCohortService, Aggregate page evaluation records into fixed cohort views. Emits weighted…, metric(), Return one metric from a family summary by id. (+7 more)

### Community 75 - "DocumentBundle"
Cohesion: 0.32
Nodes (5): DocumentBundle, Canonical software-facing document export., Materialize the on-disk tree (recomputable layers only). Side Effects: Creates…, Write document-level evaluation and export scaffolding. Side Effects: Creates…, Persist and return the document-level manifest. Side Effects: Writes…

### Community 76 - "print_error"
Cohesion: 0.21
Nodes (8): print_error(), Print error message with optional suggestions. Args: message: Error message…, Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError

### Community 77 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 78 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…, field_validator

### Community 79 - "ADR 0005 Evaluation First"
Cohesion: 0.67
Nodes (4): Gold Slice, Watchlist Metric, ADR 0005 Evaluation First, Separate Evaluation Score Families

### Community 80 - "Guide to Old English Textbook"
Cohesion: 0.50
Nodes (4): Guide to Old English Textbook, A Guide to Old English (Mitchell & Robinson), Old English Grammar for Students, Old English Grammar (Wright & Wright)

### Community 81 - "Chris Malek"
Cohesion: 0.67
Nodes (3): AUTHORS Credits, Chris Malek, MIT License

### Community 82 - "Bibliographic Provenance"
Cohesion: 0.67
Nodes (3): Acquisition Provenance, Bibliographic Provenance, SourceProvenanceService

### Community 83 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 84 - "Machine Assistance Mission"
Cohesion: 0.67
Nodes (3): Machine Assistance Mission, Teaching Workspaces README, oe-grammar vs machine-assistance Split

### Community 85 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 86 - "create_progress"
Cohesion: 0.22
Nodes (8): create_progress(), Create a rich progress indicator for long-running operations. Returns:…, Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress

### Community 104 - "._pick_scaffold_witness"
Cohesion: 0.33
Nodes (5): _coordinate_rich_line_count(), _first_witness_by_runner_preference(), Select one scaffold witness from region-bearing candidates. Args: candidates:…, Pick the first eligible witness for the earliest preferred runner id. Args:…, Count lines carrying bounding boxes or baseline geometry. Args: witness: One…

### Community 105 - "_aggregate_family"
Cohesion: 0.50
Nodes (4): _aggregate_family(), _aggregate_metric(), Sum numerators and denominators for one metric across cohort pages. Args:…, Aggregate one evaluation family across cohort pages. Args: families: Family…

### Community 106 - "Spec 0002 V1 Bundle Layout Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0002 V1 Bundle Layout Implementation Plan, Subagent Model Policy, Task 1: Manifest Models and Path Helpers (+2 more)

### Community 107 - "Spec 0008 Text and Normalization Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0008 Text and Normalization Implementation Plan, Subagent Model Policy, Task 1: Freeze Normalization Policy Models (+2 more)

### Community 108 - "Spec 0009 Merge and Alignment Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0009 Merge and Alignment Implementation Plan, Subagent Model Policy, Task 1: Merge Models and Provenance Alternates (+2 more)

### Community 109 - "Spec 0013 Pass-Runner Interface Schema Implementation Plan"
Cohesion: 0.20
Nodes (9): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0013 Pass-Runner Interface Schema Implementation Plan, Subagent Model Policy, Task 1: Reject Mutable Model Revisions (+1 more)

### Community 110 - "PlannedRunnerBatch"
Cohesion: 0.06
Nodes (56): BatchItemRef, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Runner packaging policies., Prepared image or packaged artifact ready for runner execution., One source item included in a runner execution batch. (+48 more)

### Community 111 - "MockHttpxClient"
Cohesion: 0.39
Nodes (5): MockHttpxClient, Any, BaseException, Response, Minimal httpx client stand-in for hosted runner tests.

### Community 112 - "_subdivision_boxes"
Cohesion: 0.50
Nodes (4): _fixed_tile_boxes(), Compute subdivision crop boxes and unit-kind label. Args: prepared_image:…, Build top-to-bottom fixed-tile crop boxes with configured overlap. Args: width:…, _subdivision_boxes()

### Community 113 - "PreparationBundleService"
Cohesion: 0.50
Nodes (3): PreparationBundleService, Acquire source pages and persist per-page preparation bundles. Args:…, Bind acquisition and per-page preparation collaborators. Args:…

### Community 114 - ".get_config_paths"
Cohesion: 0.30
Nodes (3): Path, Get list of configuration file paths that were loaded. Use this for debugging.…, Validate settings and ensure required directories exist. Raises:…

### Community 115 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 116 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 117 - "dense_source_page"
Cohesion: 0.50
Nodes (4): dense_source_page(), dense_two_column_image(), Build a two-column dense dictionary source page on disk. Returns: Source page…, Build a synthetic two-column page with short text-run bars. Keyword Args:…

### Community 118 - "TestConsole"
Cohesion: 0.50
Nodes (3): Test console objects., Test that console objects are properly initialized., TestConsole

### Community 120 - "_persist_prepared_page"
Cohesion: 0.09
Nodes (26): _build_prepared_units(), _index_page_overrides(), _normalize_page_overrides(), _persist_prepared_page(), _persist_recipe(), _prepared_coordinate_space(), _prepared_unit_from_box(), Path (+18 more)

## Ambiguous Edges - Review These
- `README` → `Sphinx Docs Index`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to
- `Frequently Asked Questions` → `Quickstart CLI Entry Points`  [AMBIGUOUS]
  doc/source/overview/faq.rst · relation: conceptually_related_to
- `Note-Heavy Page page-0010` → `Reject Keyser Metathesis and Vowel Deletion`  [AMBIGUOUS]
  sources/Kiparsky-PhonologyOldEnglish-1976.pdf · relation: conceptually_related_to
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to

## Knowledge Gaps
- **126 isolated node(s):** `release.sh script`, `bochord`, `IPA_AUDIO`, `Global Constraints`, `Subagent Model Policy` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `README` and `Sphinx Docs Index`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Frequently Asked Questions` and `Quickstart CLI Entry Points`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Note-Heavy Page page-0010` and `Reject Keyser Metathesis and Vowel Deletion`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `i-mutation / i-umlaut` and `Ablaut (inherited vowel alternation)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `BundlePage` connect `BundlePage` to `models/__init__.py`, `MergeOrchestrator`, `test_evaluation_service.py`, `test_ocr_models.py`, `cli.py`, `._write_page_xml`, `model_validator`, `MetricProfile`, `test_merge_service.py`, `PageXmlInterchangeService`, `test_page_interchange.py`, `services/merge.py`, `services/evaluation.py`, `_RateAccumulator`, `test_bundle_layout.py`, `._write_page_evaluation_and_manifest`, `test_text_normalization.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `test_evaluation_service.py`, `test_runner_execution.py`, `PageEvaluationSummary`, `PageClass`, `cli.py`, `services/preparation.py`, `test_merge_service.py`, `services/merge.py`, `services/evaluation.py`, `_RateAccumulator`, `PreparationRecipe`, `RunnerBatchPlanner`, `test_bundle_layout.py`, `test_text_normalization.py`, `BundleLayoutService`, `BundlePage`, `MetricProfile`, `BundlePaths`, `EvaluationFamilySummary`, `DocumentBundle`, `PlannedRunnerBatch`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `AlternateCandidate` connect `models/__init__.py` to `BundleLayoutService`, `MergeOrchestrator`, `BundlePage`, `test_evaluation_service.py`, `test_ocr_models.py`, `PageEvaluationSummary`, `PageClass`, `EvaluationFamilySummary`, `cli.py`, `DocumentBundle`, `PlannedRunnerBatch`, `services/preparation.py`, `MetricProfile`, `services/merge.py`, `services/evaluation.py`, `_RateAccumulator`, `RunnerBatchPlanner`, `test_bundle_layout.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._