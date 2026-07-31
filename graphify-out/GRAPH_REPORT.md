# Graph Report - bochord  (2026-07-31)

## Corpus Check
- 90 files · ~256,773 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1876 nodes · 4554 edges · 122 communities (108 shown, 14 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 394 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7837becf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models/__init__.py
- recipe
- cli.py
- test_olmocr_runner.py
- test_evaluation_service.py
- test_runner_execution.py
- test_cli_utils.py
- evaluation_cohorts.py
- HuggingFaceOlmocrRunner
- prepare_pages
- TestConfiguration
- RunnerThroughputSummary
- check_napoleon_gate.py
- PageClass
- services/preparation.py
- RunnerExecutionService
- PageXmlInterchangeService
- test_page_interchange.py
- TestOcrModels
- cli
- AssessmentThresholds
- .assess
- services/evaluation.py
- source_acquisition.py
- model_validator
- QualitySignal
- execution_batch_payload
- Spec 0002: V1 Bundle Layout and Data Shape
- Image
- _make_signal
- test_text_normalization.py
- Detailed OCR Process
- AGENTS.md
- Architecture Index
- Machine Assistance Resources
- Settings
- TestCLISettings
- RunnerReference
- Spec 0007: PDF-to-Image Preparation
- Spec 0004: Ordered V1 Implementation
- Phase 1 PAGE Interoperability Spike Plan
- i-mutation / i-umlaut
- conftest.py
- Point
- RunnerBatchPlanner
- Raw OCR witness layer
- MockHttpxClient
- Spec 0014: Review Task and Overlay Schema
- Python Coding Standards
- Hugging Face Setup Runbook
- _skew_signal
- Separate Text Structure Style Score Families
- Bundle JSON Export
- Page Bundle
- Gold Annotation Protocol
- SourceAcquisitionService
- Anglian dialect group
- model_validator
- Review Overlay
- ADR 0009 OCR-D PAGE eScriptorium
- Pass Runner
- Normalized Page Graph
- test_two_recipes_preserve_two_variants_without_reacquisition
- Configuration: Command Line Tool
- TestCLIVersion
- .validate_item_page_alignment
- Page Graph
- PagePreparationService
- Learner lacks stable conceptual map of sound-change order
- Spec 0003: V1 Evaluation Schema
- _table_rule_signal
- ADR 0004 Layered Truth
- Reference 0006 OCR Output Formats
- OE Grammar Resources
- TestCLIErrorHandling
- TestCLIGlobalOptions
- print_error
- Lesson 0003 Pronouncing Old English Letters
- .validate_https_huggingface_endpoints
- ADR 0005 Evaluation First
- Guide to Old English Textbook
- Chris Malek
- Bibliographic Provenance
- Character Error Rate (CER)
- Machine Assistance Mission
- Spec 0015: Gold Annotation Schema
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
- PlannedRunnerBatch
- Sphinx Docs Index
- Spec 0002 V1 Bundle Layout Implementation Plan
- Spec 0008 Text and Normalization Implementation Plan
- Spec 0009 Merge and Alignment Implementation Plan
- Spec 0013 Pass-Runner Interface Schema Implementation Plan
- test_preparation_service.py
- DocumentRunOrchestrator
- .settings_customise_sources
- .__init__
- bundle_service
- TestPrintSuccess
- TestConsoleQuietMode
- TestCLIEval
- TestConsole
- _PreparedInputsManifest
- .reject_historical_modernization
- test_configuration.py

## God Nodes (most connected - your core abstractions)
1. `SchemaModel` - 87 edges
2. `PageClass` - 46 edges
3. `PreparationMode` - 45 edges
4. `PlannedRunnerBatch` - 44 edges
5. `HuggingFaceOlmocrRunner` - 41 edges
6. `cli()` - 40 edges
7. `PreparedArtifactRef` - 40 edges
8. `PreparationRecipe` - 40 edges
9. `Settings` - 40 edges
10. `PageXmlInterchangeService` - 39 edges

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

## Communities (122 total, 14 thin omitted)

### Community 0 - "models/__init__.py"
Cohesion: 0.03
Nodes (125): AcceptReviewEvent, AcquisitionProvenance, AnchoredGoldAnnotation, BaselineShift, BibliographicProvenance, ChunkType, CorrectGeometryReviewEvent, CorrectStyleReviewEvent (+117 more)

### Community 1 - "recipe"
Cohesion: 0.16
Nodes (28): PageClassifier, PagePreparationService, Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, MonkeyPatch, dense_source_page(), preparation_service() (+20 more)

### Community 2 - "cli.py"
Cohesion: 0.10
Nodes (39): BatchItemRef, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Runner packaging policies., Declared pass-runner input and batching contract., Prepared image or packaged artifact ready for runner execution. (+31 more)

### Community 3 - "test_olmocr_runner.py"
Cohesion: 0.16
Nodes (36): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+28 more)

### Community 4 - "test_evaluation_service.py"
Cohesion: 0.10
Nodes (56): BoundingBox, GoldCoverage, LineRecord, Explicit evaluation denominator and exclusion scope for a gold slice., Axis-aligned rectangle for page-relative geometry., Accepted text span in the page graph., Accepted line node in the page graph., SpanRecord (+48 more)

### Community 5 - "test_runner_execution.py"
Cohesion: 0.15
Nodes (31): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+23 more)

### Community 6 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): print_info(), print_success(), Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling. (+1 more)

### Community 7 - "evaluation_cohorts.py"
Cohesion: 0.11
Nodes (42): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+34 more)

### Community 8 - "HuggingFaceOlmocrRunner"
Cohesion: 0.07
Nodes (32): _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _load_direct_image(), _load_image_from_pdf(), Any, Image, Path (+24 more)

### Community 9 - "prepare_pages"
Cohesion: 0.12
Nodes (22): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), _prepare_overrides(), prepare_pages(), Path (+14 more)

### Community 10 - "TestConfiguration"
Cohesion: 0.08
Nodes (18): Exception, patch, Test that settings fields have proper descriptions., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder…, Test that environment variables override defaults., Test that settings are case insensitive. (+10 more)

### Community 11 - "RunnerThroughputSummary"
Cohesion: 0.08
Nodes (31): BatchResultStatus, Execution outcome for one runner batch., Exact persisted record for one runner invocation., RunnerExecutionBatch, Measured throughput for one runner execution segment., RunnerThroughputSummary, _atomic_write_text(), _derive_result_status() (+23 more)

### Community 12 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 13 - "PageClass"
Cohesion: 0.06
Nodes (73): CoordinateSpace, FlagSeverity, PageClass, PreparationMode, PreparedPage, Page-level layout cohorts used by preparation and evaluation., Prepared-page subdivision modes., Supported top-level source kinds. (+65 more)

### Community 14 - "services/preparation.py"
Cohesion: 0.12
Nodes (24): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _crop_box(), _fill_color() (+16 more)

### Community 15 - "RunnerExecutionService"
Cohesion: 0.15
Nodes (14): Execute prepared artifacts against one hosted olmOCR runner. Args: ctx: Click…, run_runner(), BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference. (+6 more)

### Community 16 - "PageXmlInterchangeService"
Cohesion: 0.10
Nodes (22): PageXmlInterchangeService, Element, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region… (+14 more)

### Community 17 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 18 - "TestOcrModels"
Cohesion: 0.12
Nodes (10): Return fields required by every review event., Contract checks for persisted OCR schema models., Review-event schema should discriminate on ``action``., A review task should be actionable without undocumented context., Preferred input must be one of the runner's accepted inputs., Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary. (+2 more)

### Community 19 - "cli"
Cohesion: 0.14
Nodes (14): cli(), Settings-related commands. Args: ctx: Click context object., bochord command line interface. Args: ctx: Click context object. verbose:…, show_settings(), Context, group, pass_context, _dense_two_column_image() (+6 more)

### Community 20 - "AssessmentThresholds"
Cohesion: 0.12
Nodes (18): AssessmentThresholds, BaseModel, Calibratable limits for deterministic image-quality heuristics., _contrast_signal(), _effective_dpi_signal(), _median_text_height_signal(), Warn when ``value`` falls below ``minimum``. Args: value: Measured value.…, Emit effective DPI from the source coordinate space. Args: source_page: Source… (+10 more)

### Community 21 - ".assess"
Cohesion: 0.19
Nodes (13): _border_shadow_signal(), _gutter_shadow_signal(), _lower_page_ink_signal(), _margin_strip_width(), Assess quality and layout cues for ``image``. Args: source_page: Acquired…, Warn when ``value`` exceeds ``maximum``. Args: value: Measured value. maximum:…, Measure mean darkness ratio inside ``box``. Args: gray: Grayscale working…, Width of the 8% border/gutter strip in pixels. Args: width: Page width in… (+5 more)

### Community 22 - "services/evaluation.py"
Cohesion: 0.04
Nodes (79): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., BundlePage, EvaluationFlag, GoldPageAnnotation, GoldRegionAnnotation, GoldStyleSpan (+71 more)

### Community 23 - "source_acquisition.py"
Cohesion: 0.09
Nodes (35): _artifact_from_raster(), _image_bounds_cover_page(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), _pdf_page_image(), Image (+27 more)

### Community 24 - "model_validator"
Cohesion: 0.08
Nodes (13): model_validator, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Require at least one concrete replacement geometry. Returns: The validated…, Bind events to valid tasks, evidence revisions, targets, and actions. Returns:…, Require a resolvable anchor and explain every scoring exclusion. Returns: The…, Require an explanation for every scoring exclusion. Returns: The validated…, Require an explicit scope and explain every scoring exclusion. Returns: The… (+5 more)

### Community 25 - "QualitySignal"
Cohesion: 0.24
Nodes (10): QualitySignal, One measured image-quality signal from preparation assessment., _choose_preparation_mode(), Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve assessment, class, and subdivision choices for one page. Args:…, Resolve subdivision mode from automation or operator override. Args:…, Choose subdivision mode from page class and quality signals. Args: page_class:… (+2 more)

### Community 26 - "execution_batch_payload"
Cohesion: 0.29
Nodes (8): capability_payload(), execution_batch_payload(), model_runner_payload(), Return a valid model-backed runner payload with optional overrides., Return a valid runner capability payload with optional overrides., Return a valid runner execution batch payload with optional overrides., test_model_backed_runner_requires_hardware_class(), test_spec_0013_runner_invariants_reject_invalid_payloads()

### Community 27 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.25
Nodes (8): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, V1 Typography and Role Vocabulary, Evidence-Bound Human Review, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence, Reject eScriptorium as Review Boundary, PAGE Region/Line Reuse Boundary

### Community 28 - "Image"
Cohesion: 0.21
Nodes (13): _column_count_signal(), _column_ink_profile(), _column_unit_boxes(), _column_valley_centers(), _load_source_image(), Image, Locate midpoints of sustained low-ink vertical valleys. Args: gray: Grayscale…, Build left-to-right column crop boxes with configured overlap. Args: image:… (+5 more)

### Community 29 - "_make_signal"
Cohesion: 0.22
Nodes (11): _bleedthrough_signal(), _colored_marking_signal(), _make_signal(), _pixel_access(), Any, Return Pillow pixel access for ``image``. Args: image: Image whose pixels will…, Build one ``QualitySignal`` row. Args: signal_id: Stable signal identifier.…, Measure isolated pixel noise relative to a median filter. Args: gray: Grayscale… (+3 more)

### Community 30 - "test_text_normalization.py"
Cohesion: 0.07
Nodes (41): bochord.models Package, NoteRecord, Accepted note object in the page graph., LineJoinKind, LineJoinRecord, NoteMarkerNormalizedForm, StrEnum, Unicode normalization form applied to diplomatic text. (+33 more)

### Community 31 - "Detailed OCR Process"
Cohesion: 0.23
Nodes (17): Detailed OCR Process, Kraken Runner, OCR Produces Evidence, Philological Watchlists, Stage 4 Align Evidence, Stage 7 Apply Overlays, Stage 3 Competing OCR Passes, Stage 6 Evaluate Against Gold (+9 more)

### Community 32 - "AGENTS.md"
Cohesion: 0.09
Nodes (23): bochord.cli Package, main(), bochord.services Package, DdlExtractor, ExtractionOrchestrator, RunStats, bochord Virtual Environment, boto3 Library (+15 more)

### Community 33 - "Architecture Index"
Cohesion: 0.21
Nodes (12): bochord Context, bochord, Image-First OCR Orchestration, Preparation Recipe, Witness Production, ADR 0001 Package Boundary, OCR Evidence Not Philological Semantics, Acquire-Prepare-Pass-Align-Evaluate-Review-Export Workflow (+4 more)

### Community 34 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 35 - "Settings"
Cohesion: 0.20
Nodes (10): Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Settings, patch, Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIRun (+2 more)

### Community 36 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 37 - "RunnerReference"
Cohesion: 0.18
Nodes (8): Identity for one runner implementation and model revision., RunnerReference, Bind one hosted olmOCR runner to endpoint settings and an HTTP client. Args:…, Return the runner identity used for hosted requests. Returns: Model-backed…, Client, Persisted batch status must agree with submitted and failed items., test_runner_reference_accepts_immutable_digest_revision(), test_runner_reference_rejects_mutable_model_revision()

### Community 38 - "Spec 0007: PDF-to-Image Preparation"
Cohesion: 0.29
Nodes (7): Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Page Subdivision into OCR Units, Preparation Pipeline Stage, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts, V1 Page Class Taxonomy

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

### Community 43 - "Point"
Cohesion: 0.12
Nodes (12): Point, One point in an identified image coordinate space., Path, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned… (+4 more)

### Community 44 - "RunnerBatchPlanner"
Cohesion: 0.23
Nodes (22): Plan fixed runner batches from prepared artifacts and policy., RunnerBatchPlanner, Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), artifacts(), capability(), policy() (+14 more)

### Community 45 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 46 - "MockHttpxClient"
Cohesion: 0.29
Nodes (7): BatchUnitKind, Batch grouping units for runner execution., MockHttpxClient, Any, BaseException, Response, Minimal httpx client stand-in for hosted runner tests.

### Community 47 - "Spec 0014: Review Task and Overlay Schema"
Cohesion: 0.40
Nodes (5): Review Overlays, Spec 0014: Review Task and Overlay Schema, correct_text Event Semantics, PageOverlay Append-Only Log, ReviewTask Packet

### Community 48 - "Python Coding Standards"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 49 - "Hugging Face Setup Runbook"
Cohesion: 0.31
Nodes (11): Client-Side Queue for Cold Starts, Custom OCR Container, Hugging Face Setup Runbook, Hugging Face Inference Endpoints, Immutable Model Commit Pinning, Local Laptop Boundary, RunnerReference Provenance, olmOCR Runner (+3 more)

### Community 50 - "_skew_signal"
Cohesion: 0.25
Nodes (8): _downsample_for_heuristics(), _measure_skew_degrees(), Estimate page skew degrees via row-projection variance. Args: gray: Grayscale…, Downsample so the longest edge is at most ``_HEURISTIC_MAX_EDGE_PX``. Args:…, Compute variance of per-row ink sums. Args: gray: Grayscale page image.…, Estimate skew via row-projection variance over candidate angles. Args: gray:…, _row_projection_variance(), _skew_signal()

### Community 51 - "Separate Text Structure Style Score Families"
Cohesion: 0.22
Nodes (9): GoldCoverage, Separate Text Structure Style Score Families, Spec 0003 Evaluation Schema Completion Plan, StyleEvaluationSummary, watchlist_exact_match_rate, Spec 0007 Preparation Completion Plan, Coverage Metric for OCR Comparison, OCR Is a Routing and Evaluation Problem (+1 more)

### Community 52 - "Bundle JSON Export"
Cohesion: 0.27
Nodes (10): Bundle JSON Export, Markdown Export, RAG JSON Export, Export Layer, Spec 0006: Exports and Retrieval Views, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models (+2 more)

### Community 53 - "Page Bundle"
Cohesion: 0.40
Nodes (6): Document Bundle, Page Bundle, Page-Local Truth, ADR 0002 Bundle Model, Page Bundle as Page-Local Truth Unit, BundleWriter

### Community 54 - "Gold Annotation Protocol"
Cohesion: 0.33
Nodes (9): EvaluationService, bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, GoldDocument, MetricProfile, Phase 2 Gold Evaluator Plan, GoldLineJoin (+1 more)

### Community 55 - "SourceAcquisitionService"
Cohesion: 0.31
Nodes (17): Copy or render source pages into a deterministic ``pages/`` layout., SourceAcquisitionService, pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe() (+9 more)

### Community 56 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 57 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 58 - "Review Overlay"
Cohesion: 0.29
Nodes (8): Append-Only Review History, Review Overlay, Trust State, Overlay Layer, ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States, OverlayService

### Community 59 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.25
Nodes (8): Hosted Inference Boundary, PAGE Interchange, ADR 0007 V1 Engine Strategy, Hugging Face Hosted Endpoints, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE, OCR-D/eScriptorium Round-Trip Spike

### Community 60 - "Pass Runner"
Cohesion: 0.33
Nodes (7): Pass Family, Pass Runner, ADR 0006 Pass Runner Plugins, Pass Runner Common Interface, V1 Engine Bake-Off, kraken Candidate, olmocr Candidate

### Community 61 - "Normalized Page Graph"
Cohesion: 0.29
Nodes (8): Normalized Page Graph, Footnote Chunk, Spec 0011: Structured Output Strategy, Standard OCR Intermediate Structure, TEI Dictionaries Chapter, TEI P5 as Downstream Reference, Domain Language, Shared Domain Glossary

### Community 62 - "test_two_recipes_preserve_two_variants_without_reacquisition"
Cohesion: 0.20
Nodes (10): Derive a stable digest from the full preparation recipe JSON. Args: recipe:…, _recipe_digest(), MockerFixture, binary_recipe(), Write a single-page source raster for bundle tests. Returns: Path to a…, Load a binary/Otsu recipe variant for multi-recipe bundle tests. Keyword Args:…, source_image(), test_page_override_rejects_unknown_source_page_id() (+2 more)

### Community 63 - "Configuration: Command Line Tool"
Cohesion: 0.39
Nodes (8): Configuration: Command Line Tool, CLI Configuration Cascade, Frequently Asked Questions, Installation, Python 3.10+ Installation, Quickstart Guide, Quickstart CLI Entry Points, Using the Command Line Interface

### Community 64 - "TestCLIVersion"
Cohesion: 0.25
Nodes (5): Test the version command., Test the version command displays version information., Test the version command with verbose flag., Test the version command with quiet flag., TestCLIVersion

### Community 65 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

### Community 66 - "Page Graph"
Cohesion: 0.53
Nodes (6): Page Graph, Shared Page Coordinates, Page Graph Line, Page Graph Note, Page Graph Region, Page Graph Span

### Community 67 - "PagePreparationService"
Cohesion: 0.32
Nodes (8): PagePreparationService, Stage 1 Acquire Source, Stage 2 PDF-to-Image Preparation, When To Rerun vs Rebuild, Phase 3 Acquisition Preparation Plan, Pillow and pypdfium2 Stack, SourceAcquisitionService, Preparation Recipe Variants

### Community 68 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 69 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.14
Nodes (15): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0008: Text and Normalization (+7 more)

### Community 70 - "_table_rule_signal"
Cohesion: 0.29
Nodes (8): _longest_dark_run(), Return the longest contiguous run of values below ``threshold``. Args: values:…, Mark rows whose longest dark run spans enough of the page width. Args: gray:…, Mark columns whose longest dark run spans enough of the page height. Args:…, Count sustained dark horizontal and vertical rules. Args: gray: Grayscale…, _rule_column_mask(), _rule_row_mask(), _table_rule_signal()

### Community 71 - "ADR 0004 Layered Truth"
Cohesion: 0.40
Nodes (5): Raw Witness Artifact, ADR 0004 Layered Truth, Derived Graph Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 72 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 73 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 74 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 75 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

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

### Community 85 - "Spec 0015: Gold Annotation Schema"
Cohesion: 0.33
Nodes (6): V1 Gold Data Expectations, Coordinate and Image Provenance, Spec 0015: Gold Annotation Schema, do_not_score Exclusions, GoldDocument Annotation Binding, Held-Out Gold Splits

### Community 86 - "create_progress"
Cohesion: 0.22
Nodes (8): create_progress(), Create a rich progress indicator for long-running operations. Returns:…, Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress

### Community 104 - "PlannedRunnerBatch"
Cohesion: 0.12
Nodes (32): PlannedRunnerBatch, One planned invocation batch before packaging and submission., _load_rgb_images(), _page_numbers(), Image, Path, Package one batch using the requested strategy. Args: batch: Planned batch…, Reference one prepared artifact without copying bytes. Args: batch: Single-item… (+24 more)

### Community 105 - "Sphinx Docs Index"
Cohesion: 0.50
Nodes (5): API Models Autodoc, Changelog, Sphinx Docs Index, README, Read the Docs Config

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

### Community 110 - "test_preparation_service.py"
Cohesion: 0.18
Nodes (21): PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., dark_gutter_image(), note_heavy_image(), Image, Index quality signals by ``signal_id``. Args: signals: Measured quality signals…, Build a page of horizontal text-like bars, then rotate it. Keyword Args:…, Build a page with a dark vertical gutter in the center strip. Returns:… (+13 more)

### Community 111 - "DocumentRunOrchestrator"
Cohesion: 0.50
Nodes (4): DocumentRunOrchestrator, PageAlignmentService, PageGraphBuilder, PassRunnerRegistry

### Community 112 - ".settings_customise_sources"
Cohesion: 0.22
Nodes (6): BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, PydanticBaseSettingsSource, Test loading configuration with TOML file.

### Community 114 - "bundle_service"
Cohesion: 0.18
Nodes (12): PreparationBundleService, Acquire source pages and persist per-page preparation bundles. Args:…, Bind acquisition and per-page preparation collaborators. Args:…, bundle_service(), dense_two_column_image(), Write a two-page image folder for multi-page bundle tests. Returns: Path to a…, Build a preparation bundle service wired to ``acquisition``. Args: acquisition:…, Build a synthetic two-column page with short text-run bars. Keyword Args:… (+4 more)

### Community 115 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 116 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 117 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 118 - "TestConsole"
Cohesion: 0.50
Nodes (3): Test console objects., Test that console objects are properly initialized., TestConsole

### Community 119 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``bochord run``.

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
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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
- **Why does `SchemaModel` connect `models/__init__.py` to `cli.py`, `test_evaluation_service.py`, `RunnerReference`, `evaluation_cohorts.py`, `PlannedRunnerBatch`, `Point`, `RunnerThroughputSummary`, `PageClass`, `services/preparation.py`, `AssessmentThresholds`, `services/evaluation.py`, `QualitySignal`, `test_text_normalization.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `TestCLIVersion`, `cli.py`, `TestCLISettings`, `TestCLIErrorHandling`, `TestCLIGlobalOptions`, `TestConfiguration`, `.validate_https_huggingface_endpoints`, `RunnerExecutionService`, `.settings_customise_sources`, `cli`, `TestCLIEval`, `test_configuration.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `BundlePage` connect `services/evaluation.py` to `models/__init__.py`, `cli.py`, `test_evaluation_service.py`, `Point`, `PageClass`, `PageXmlInterchangeService`, `test_page_interchange.py`, `model_validator`, `test_text_normalization.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._