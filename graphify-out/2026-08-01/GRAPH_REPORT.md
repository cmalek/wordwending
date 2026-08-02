# Graph Report - bochord  (2026-07-30)

## Corpus Check
- 78 files · ~247,177 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1764 nodes · 4336 edges · 116 communities (105 shown, 11 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 386 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0ff468f2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cli.py
- test_olmocr_runner.py
- evaluation_cohorts.py
- Settings
- models/__init__.py
- test_evaluation_service.py
- Image
- check_napoleon_gate.py
- services/evaluation.py
- TestOcrModels
- PageXmlInterchangeService
- TestCLIGlobalOptions
- Path
- prepare_pages
- model_validator
- RunnerThroughputSummary
- model_runner_payload
- source_acquisition.py
- services/preparation.py
- PreparedArtifactRef
- Stage 6 Evaluate Against Gold
- Machine Assistance Resources
- DocumentRunOrchestrator
- bochord
- Gold Annotation Protocol
- recipe
- cli
- test_cli_utils.py
- main
- Spec 0004: Ordered V1 Implementation
- Detailed OCR Process
- conftest.py
- i-mutation / i-umlaut
- print_error
- ._coords
- Spec 0007: PDF-to-Image Preparation
- Raw OCR witness layer
- TestCLISettings
- create_progress
- ._write_page_xml
- Spec 0005: Human Markup and Review
- Python Coding Standards
- Architecture Index
- Hugging Face Setup Runbook
- PagePreparationOverride
- ADR 0004 Layered Truth
- Spec 0006: Exports and Retrieval Views
- PagePreparationService
- Anglian dialect group
- TestCLIEval
- recipe_payload
- Review Overlay
- Spec 0002: V1 Bundle Layout and Data Shape
- Normalized Page Graph
- Configuration: Command Line Tool
- TestCLIVersion
- Pass Runner
- Note-Heavy Page page-0010
- Learner lacks stable conceptual map of sound-change order
- HuggingFaceOlmocrRunner
- SourceAcquisitionService
- PackagedRunnerInput
- Page Bundle
- Page Graph
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- OE Grammar Resources
- TestCLIErrorHandling
- TestPrintSuccess
- TestConsoleQuietMode
- BundlePage
- ADR 0005 Evaluation First
- RunnerReference
- Lesson 0003 Pronouncing Old English Letters
- test_page_interchange.py
- Guide to Old English Textbook
- TestConsole
- Chris Malek
- Bibliographic Provenance
- Old English Morphological Analyser
- Character Error Rate (CER)
- release.sh
- PageClass
- Contributor Covenant 3.0
- Accepted Page Graph
- Worked BT entry example: abbad
- Old English c/g palatalization
- OE tēon walk-back (Grimm + h-loss + contraction)
- ipa-play.js
- test_preparation_service.py
- bochord
- Mixed dialect spellings from copying history
- Reference Sound Terms
- test_cli_commands.py
- RunnerExecutionService
- Image
- _choose_preparation_mode
- test_configuration.py
- RunnerInputPackager
- _PreparedInputsManifest
- test_runner_execution.py
- .validate_https_huggingface_endpoints
- _table_rule_signal
- ._package_pdf
- MockHttpxClient
- QualitySignal
- Separate Text Structure Style Score Families
- Spec 0009: Merge and Alignment
- PreparationBundleService
- _transport_failure_warning

## God Nodes (most connected - your core abstractions)
1. `SchemaModel` - 80 edges
2. `PageClass` - 45 edges
3. `PreparationMode` - 44 edges
4. `PlannedRunnerBatch` - 44 edges
5. `HuggingFaceOlmocrRunner` - 41 edges
6. `cli()` - 40 edges
7. `PreparedArtifactRef` - 40 edges
8. `PreparationRecipe` - 40 edges
9. `Settings` - 40 edges
10. `PageXmlInterchangeService` - 37 edges

## Surprising Connections (you probably didn't know these)
- `Coverage Metric for OCR Comparison` --semantically_similar_to--> `GoldCoverage`  [INFERRED] [semantically similar]
  sources/I Spent the Summer Testing 14 OCR Engines _ by Ida Silfverskiöld _ Jul, 2026 _ Level Up Coding.pdf → doc/source/runbook/gold_annotation.rst
- `OCR Is a Routing and Evaluation Problem` --semantically_similar_to--> `Separate Text Structure Style Score Families`  [INFERRED] [semantically similar]
  sources/I Spent the Summer Testing 14 OCR Engines _ by Ida Silfverskiöld _ Jul, 2026 _ Level Up Coding.pdf → doc/source/runbook/ocr_process.rst
- `Derived Graph Layer` --semantically_similar_to--> `Page Graph`  [INFERRED] [semantically similar]
  doc/source/architecture/adr_0004_layered_artifacts.rst → CONTEXT.md
- `Reject Keyser Metathesis and Vowel Deletion` --conceptually_related_to--> `Note-Heavy Page page-0010`  [AMBIGUOUS]
  sources/Kiparsky-PhonologyOldEnglish-1976.pdf → doc/source/runbook/gold_annotation.rst
- `README` --semantically_similar_to--> `Sphinx Docs Index`  [AMBIGUOUS] [semantically similar]
  README.md → doc/source/index.rst

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Four-Layer Truth Model** — doc_source_architecture_adr_0004_layered_truth_raw_witness_layer, doc_source_architecture_adr_0004_layered_truth_derived_graph_layer, doc_source_architecture_adr_0004_layered_truth_overlay_layer, doc_source_architecture_adr_0004_layered_truth_export_layer [EXTRACTED 1.00]
- **V1 Page Graph Node Kinds** — doc_source_architecture_adr_0003_page_graph_region, doc_source_architecture_adr_0003_page_graph_line, doc_source_architecture_adr_0003_page_graph_span, doc_source_architecture_adr_0003_page_graph_note [EXTRACTED 1.00]
- **V1 Core Service Collaborators** — doc_source_architecture_spec_0001_system_architecture_document_run_orchestrator, doc_source_architecture_spec_0001_system_architecture_page_preparation_service, doc_source_architecture_spec_0001_system_architecture_pass_runner_registry, doc_source_architecture_spec_0001_system_architecture_page_alignment_service, doc_source_architecture_spec_0001_system_architecture_page_graph_builder, doc_source_architecture_spec_0001_system_architecture_evaluation_service, doc_source_architecture_spec_0001_system_architecture_overlay_service, doc_source_architecture_spec_0001_system_architecture_bundle_writer [EXTRACTED 1.00]
- **V1 Export Family Triad** — doc_source_architecture_spec_0006_exports_and_retrieval_bundle_json, doc_source_architecture_spec_0006_exports_and_retrieval_rag_json, doc_source_architecture_spec_0006_exports_and_retrieval_markdown [EXTRACTED 1.00]
- **Evidence-Preserving Text Pipeline** — doc_source_architecture_spec_0008_text_normalization_dual_text, doc_source_architecture_spec_0005_human_markup_diplomatic_text, doc_source_architecture_spec_0014_review_overlay_schema_correct_text [INFERRED 0.85]
- **Runner Execution Contract Stack** — doc_source_architecture_spec_0012_runner_execution_and_batching_batch_policy, doc_source_architecture_spec_0013_pass_runner_interface_schema_runner_capability, doc_source_architecture_spec_0013_pass_runner_interface_schema_execution_batch, doc_source_architecture_spec_0012_runner_execution_and_batching_hugging_face [INFERRED 0.85]
- **End-to-End bochord OCR Pipeline Stages** — doc_source_runbook_ocr_process_stage_acquire_source, doc_source_runbook_ocr_process_stage_pdf_to_image, doc_source_runbook_ocr_process_stage_competing_passes, doc_source_runbook_ocr_process_stage_align_evidence, doc_source_runbook_ocr_process_stage_page_graph, doc_source_runbook_ocr_process_stage_evaluate_gold, doc_source_runbook_ocr_process_stage_apply_overlays, doc_source_runbook_ocr_process_stage_export [EXTRACTED 1.00]
- **Spec Completion Sequence 0003→0007→0010→0012** — docs_superpowers_plans_2026_07_25_spec_0003_evaluation_schema_completion_document, docs_superpowers_plans_2026_07_25_spec_0007_preparation_completion_document, docs_superpowers_plans_2026_07_25_spec_0010_page_classification_cohorts_document, docs_superpowers_plans_2026_07_25_spec_0012_runner_execution_batching_document [EXTRACTED 1.00]
- **Evidence Preservation Layers** — doc_source_runbook_ocr_process_ocr_as_evidence, doc_source_runbook_operator_notes_preserve_run_artifacts, teaching_machine_assistance_notes_evidence_layer_separation, doc_source_runbook_ocr_process_stage_apply_overlays [INFERRED 0.85]
- **Witness-preserving OCR-to-structure workflow** — teaching_machine_assistance_lessons_0004_seven_stage_pipeline, teaching_machine_assistance_lessons_0004_raw_witness_layer, teaching_machine_assistance_lessons_0004_overlay_layer, teaching_machine_assistance_lessons_0004_normalized_export_layer, teaching_machine_assistance_lessons_0004_review_by_exception, teaching_machine_assistance_lessons_0006_entry_block_unit [EXTRACTED 1.00]
- **PIE to OE sound-change layering timeline** — teaching_oe_grammar_lessons_0001_proto_indo_european, teaching_oe_grammar_lessons_0001_grimms_law, teaching_oe_grammar_lessons_0001_verners_law, teaching_oe_grammar_lessons_0001_proto_germanic, teaching_oe_grammar_lessons_0001_i_mutation, teaching_oe_grammar_reference_0001_sound_change_order [EXTRACTED 1.00]
- **OE dialect recognition cue system** — teaching_oe_grammar_lessons_0002_west_saxon, teaching_oe_grammar_lessons_0002_anglian, teaching_oe_grammar_lessons_0002_kentish, teaching_oe_grammar_lessons_0002_mercian, teaching_oe_grammar_lessons_0002_northumbrian, teaching_oe_grammar_reference_0004_dialect_cue_table [EXTRACTED 1.00]

## Communities (116 total, 11 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.09
Nodes (40): BatchItemRef, InputKind, PackagingStrategy, Runner input artifact categories., Runner packaging policies., Declared pass-runner input and batching contract., One source item included in a runner execution batch., One raw witness artifact emitted by a pass runner. (+32 more)

### Community 1 - "test_olmocr_runner.py"
Cohesion: 0.20
Nodes (31): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy_with_endpoint(), Path, Return a policy whose endpoint block includes ``endpoint_overrides``. (+23 more)

### Community 2 - "evaluation_cohorts.py"
Cohesion: 0.11
Nodes (41): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+33 more)

### Community 3 - "Settings"
Cohesion: 0.07
Nodes (28): BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, Application settings with cascading configuration support. Note: The app_name…, Settings, Exception, PydanticBaseSettingsSource (+20 more)

### Community 4 - "models/__init__.py"
Cohesion: 0.04
Nodes (120): AcceptReviewEvent, AcquisitionProvenance, BaselineShift, BatchUnitKind, BibliographicProvenance, ChunkType, CorrectGeometryReviewEvent, CorrectStyleReviewEvent (+112 more)

### Community 5 - "test_evaluation_service.py"
Cohesion: 0.10
Nodes (59): BoundingBox, GoldCoverage, GoldTextSpan, LineRecord, Gold diplomatic and normalized text target., Explicit evaluation denominator and exclusion scope for a gold slice., Axis-aligned rectangle for page-relative geometry., Orthogonal visual typography facets for one text span. (+51 more)

### Community 6 - "Image"
Cohesion: 0.08
Nodes (38): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _column_ink_profile(), _crop_box() (+30 more)

### Community 7 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 8 - "services/evaluation.py"
Cohesion: 0.04
Nodes (66): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., AnchoredGoldAnnotation, EvaluationFlag, GoldNoteLink, GoldRegionAnnotation, GoldStyleSpan (+58 more)

### Community 9 - "TestOcrModels"
Cohesion: 0.12
Nodes (11): parametrize, Return fields required by every review event., Contract checks for persisted OCR schema models., Review-event schema should discriminate on ``action``., A review task should be actionable without undocumented context., Boxes must represent a positive-area rectangle., Graph parent-child identifiers must resolve within the page., Gold text without a graph target or geometry cannot be scored. (+3 more)

### Community 10 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 11 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 12 - "Path"
Cohesion: 0.15
Nodes (17): _export_note_page(), Path, Export should round PAGE coordinates to importer-friendly integers., PAGE corrections should update text while sidecar evidence stays intact., Import should fail when PAGE XML drops a canonical region id., Import should fail when PAGE XML repeats a canonical line id., Import should fail when corrected PAGE points at a different image identity., Import should fail when PAGE XML drops a canonical word id. (+9 more)

### Community 13 - "prepare_pages"
Cohesion: 0.11
Nodes (26): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), prepare_pages(), Path, Print the some version info of this package, (+18 more)

### Community 14 - "model_validator"
Cohesion: 0.08
Nodes (13): model_validator, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Require at least one concrete replacement geometry. Returns: The validated…, Bind events to valid tasks, evidence revisions, targets, and actions. Returns:…, Require a resolvable anchor and explain every scoring exclusion. Returns: The…, Require an explanation for every scoring exclusion. Returns: The validated…, Require an explicit scope and explain every scoring exclusion. Returns: The… (+5 more)

### Community 15 - "RunnerThroughputSummary"
Cohesion: 0.07
Nodes (32): BatchResultStatus, Execution outcome for one runner batch., Exact persisted record for one runner invocation., RunnerExecutionBatch, Measured throughput for one runner execution segment., RunnerThroughputSummary, _atomic_write_text(), _derive_result_status() (+24 more)

### Community 16 - "model_runner_payload"
Cohesion: 0.67
Nodes (3): model_runner_payload(), Return a valid model-backed runner payload with optional overrides., test_model_backed_runner_requires_hardware_class()

### Community 17 - "source_acquisition.py"
Cohesion: 0.09
Nodes (35): _artifact_from_raster(), _image_bounds_cover_page(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), _pdf_page_image(), Image (+27 more)

### Community 18 - "services/preparation.py"
Cohesion: 0.12
Nodes (27): _build_prepared_units(), _column_unit_boxes(), _column_valley_centers(), _fixed_tile_boxes(), _persist_prepared_page(), _persist_recipe(), _prepared_coordinate_space(), _prepared_unit_from_box() (+19 more)

### Community 19 - "PreparedArtifactRef"
Cohesion: 0.19
Nodes (25): PreparedArtifactRef, Prepared image or packaged artifact ready for runner execution., Plan fixed runner batches from prepared artifacts and policy., Reject runs that exceed hosted item or cost caps before planning output. Args:…, RunnerBatchPlanner, Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap() (+17 more)

### Community 20 - "Stage 6 Evaluate Against Gold"
Cohesion: 0.22
Nodes (11): Philological Watchlists, Stage 7 Apply Overlays, Stage 6 Evaluate Against Gold, Stage 8 Export, Common OCR Failure Shapes, Machine Assistance Mission, Dependable Machine Assistance for Old English, Machine Assistance Notes (+3 more)

### Community 21 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 22 - "DocumentRunOrchestrator"
Cohesion: 0.18
Nodes (14): AGENTS.md Agent Guidance, bochord.cli, bochord.models, bochord.services, botocraft Preference, ExtractionOrchestrator, Napoleon Documentation Gate, bochord.settings (+6 more)

### Community 23 - "bochord"
Cohesion: 0.19
Nodes (14): bochord Context, bochord, Image-First OCR Orchestration, Preparation Recipe, Witness Production, API Models Autodoc, ADR 0001 Package Boundary, OCR Evidence Not Philological Semantics (+6 more)

### Community 24 - "Gold Annotation Protocol"
Cohesion: 0.31
Nodes (11): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Phase 2 Gold Evaluator Plan (+3 more)

### Community 25 - "recipe"
Cohesion: 0.19
Nodes (21): MockerFixture, binary_recipe(), bundle_service(), parametrize, Path, Write a single-page source raster for bundle tests. Returns: Path to a…, Write a two-page image folder for multi-page bundle tests. Returns: Path to a…, Build a preparation bundle service wired to ``acquisition``. Args: acquisition:… (+13 more)

### Community 26 - "cli"
Cohesion: 0.18
Nodes (10): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test the prepare command., Test prepare aborts before writes when override lacks a reason. (+2 more)

### Community 27 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): print_info(), print_success(), Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling. (+1 more)

### Community 28 - "main"
Cohesion: 0.23
Nodes (8): main(), patch, Tests for the main module., Test the main function., Test that main function calls the CLI., Test that main function can be imported and called., Test that main function exists and is callable., TestMain

### Community 29 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.18
Nodes (13): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy, Hugging Face Deployment Target (+5 more)

### Community 30 - "Detailed OCR Process"
Cohesion: 0.29
Nodes (13): Detailed OCR Process, Kraken Runner, OCR Produces Evidence, olmOCR Runner, Stage 1 Acquire Source, Stage 4 Align Evidence, Stage 3 Competing OCR Passes, Stage 5 Build Page Graph (+5 more)

### Community 31 - "conftest.py"
Cohesion: 0.21
Nodes (12): cli_context(), mock_console(), mock_settings(), fixture, Test configuration and fixtures for the ai-coding project. This file contains…, Create a CLI runner for testing., Create a temporary directory for testing., Create a mock console for testing. (+4 more)

### Community 32 - "i-mutation / i-umlaut"
Cohesion: 0.23
Nodes (13): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+5 more)

### Community 33 - "print_error"
Cohesion: 0.21
Nodes (8): print_error(), Print error message with optional suggestions. Args: message: Error message…, Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError

### Community 34 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 35 - "Spec 0007: PDF-to-Image Preparation"
Cohesion: 0.17
Nodes (12): V1 Gold Data Expectations, Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Coordinate and Image Provenance, Page Subdivision into OCR Units, Preparation Pipeline Stage, Preparation Recipe, V1 Page Class Taxonomy (+4 more)

### Community 36 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 37 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 38 - "create_progress"
Cohesion: 0.22
Nodes (8): create_progress(), Create a rich progress indicator for long-running operations. Returns:…, Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress

### Community 39 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Merge PAGE-supported corrections into canonical sidecar data. Args:…

### Community 40 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Review Overlays, Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0014: Review Task and Overlay Schema (+3 more)

### Community 41 - "Python Coding Standards"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 42 - "Architecture Index"
Cohesion: 0.22
Nodes (10): Hosted Inference Boundary, PAGE Interchange, ADR 0003 Page Graph, ADR 0007 V1 Engine Strategy, Hugging Face Hosted Endpoints, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+2 more)

### Community 43 - "Hugging Face Setup Runbook"
Cohesion: 0.36
Nodes (10): Client-Side Queue for Cold Starts, Custom OCR Container, Hugging Face Setup Runbook, Hugging Face Inference Endpoints, Immutable Model Commit Pinning, Local Laptop Boundary, RunnerReference Provenance, Spec 0012 Runner Execution Batching Plan (+2 more)

### Community 44 - "PagePreparationOverride"
Cohesion: 0.10
Nodes (17): PagePreparationOverride, model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Operator override for one acquired source page., Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…, _index_page_overrides() (+9 more)

### Community 45 - "ADR 0004 Layered Truth"
Cohesion: 0.22
Nodes (9): Bundle JSON Export, Markdown Export, RAG JSON Export, Raw Witness Artifact, ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Rebuild Derived Outputs From Raw Artifacts (+1 more)

### Community 46 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 47 - "PagePreparationService"
Cohesion: 0.40
Nodes (6): Phase 3 Acquisition Preparation Plan, PagePreparationService, Pillow and pypdfium2 Stack, SourceAcquisitionService, Spec 0007 Preparation Completion Plan, Preparation Recipe Variants

### Community 48 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 49 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 50 - "recipe_payload"
Cohesion: 0.67
Nodes (3): Return a valid preparation-recipe payload with optional overrides., recipe_payload(), test_recipe_rejects_overlap_not_smaller_than_tile()

### Community 51 - "Review Overlay"
Cohesion: 0.29
Nodes (8): Append-Only Review History, Review Overlay, Trust State, Overlay Layer, ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States, OverlayService

### Community 52 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.25
Nodes (8): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, V1 Typography and Role Vocabulary, Evidence-Bound Human Review, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence, Reject eScriptorium as Review Boundary, PAGE Region/Line Reuse Boundary

### Community 53 - "Normalized Page Graph"
Cohesion: 0.29
Nodes (8): Normalized Page Graph, Footnote Chunk, Spec 0011: Structured Output Strategy, Standard OCR Intermediate Structure, TEI Dictionaries Chapter, TEI P5 as Downstream Reference, Domain Language, Shared Domain Glossary

### Community 54 - "Configuration: Command Line Tool"
Cohesion: 0.39
Nodes (8): Configuration: Command Line Tool, CLI Configuration Cascade, Frequently Asked Questions, Installation, Python 3.10+ Installation, Quickstart Guide, Quickstart CLI Entry Points, Using the Command Line Interface

### Community 55 - "TestCLIVersion"
Cohesion: 0.25
Nodes (5): Test the version command., Test the version command displays version information., Test the version command with verbose flag., Test the version command with quiet flag., TestCLIVersion

### Community 56 - "Pass Runner"
Cohesion: 0.33
Nodes (7): Pass Family, Pass Runner, ADR 0006 Pass Runner Plugins, Pass Runner Common Interface, V1 Engine Bake-Off, kraken Candidate, olmocr Candidate

### Community 57 - "Note-Heavy Page page-0010"
Cohesion: 0.22
Nodes (13): Note-Heavy Page page-0010, Dictionary Headword Page page-0100, BundlePage Canonical JSON, Phase 1 PAGE Interoperability Spike Plan, PageXmlInterchangeService, Reject ocrd-models for Spike, Spec 0010 Page Classification Cohorts Plan, Weighted Evaluation Cohorts (+5 more)

### Community 58 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 59 - "HuggingFaceOlmocrRunner"
Cohesion: 0.08
Nodes (27): _encode_png_base64(), HuggingFaceOlmocrRunner, _load_direct_image(), _load_image_from_pdf(), Any, Image, Path, Response (+19 more)

### Community 60 - "SourceAcquisitionService"
Cohesion: 0.31
Nodes (17): Copy or render source pages into a deterministic ``pages/`` layout., SourceAcquisitionService, pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe() (+9 more)

### Community 61 - "PackagedRunnerInput"
Cohesion: 0.20
Nodes (7): PackagedRunnerInput, model_validator, Packaged artifact ready for hosted runner submission., Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…, test_packaged_runner_input_rejects_mismatched_item_page_lengths()

### Community 62 - "Page Bundle"
Cohesion: 0.40
Nodes (6): Document Bundle, Page Bundle, Page-Local Truth, ADR 0002 Bundle Model, Page Bundle as Page-Local Truth Unit, BundleWriter

### Community 63 - "Page Graph"
Cohesion: 0.53
Nodes (6): Page Graph, Shared Page Coordinates, Page Graph Line, Page Graph Note, Page Graph Region, Page Graph Span

### Community 64 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.33
Nodes (6): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Historical Character Preservation, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts

### Community 65 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 66 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 67 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 68 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 69 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 70 - "BundlePage"
Cohesion: 0.12
Nodes (19): BundlePage, GoldPageAnnotation, NoteRecord, Canonical exported page object., Gold data slice for one page., Accepted note object in the page graph., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold… (+11 more)

### Community 71 - "ADR 0005 Evaluation First"
Cohesion: 0.50
Nodes (5): Gold Slice, Watchlist Metric, ADR 0005 Evaluation First, Separate Evaluation Score Families, EvaluationService

### Community 72 - "RunnerReference"
Cohesion: 0.12
Nodes (12): Identity for one runner implementation and model revision., RunnerReference, Bind one hosted olmOCR runner to endpoint settings and an HTTP client. Args:…, Return the runner identity used for hosted requests. Returns: Model-backed…, Client, Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., policy() (+4 more)

### Community 73 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 74 - "test_page_interchange.py"
Cohesion: 0.21
Nodes (15): _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids. (+7 more)

### Community 75 - "Guide to Old English Textbook"
Cohesion: 0.50
Nodes (4): Guide to Old English Textbook, A Guide to Old English (Mitchell & Robinson), Old English Grammar for Students, Old English Grammar (Wright & Wright)

### Community 76 - "TestConsole"
Cohesion: 0.50
Nodes (3): Test console objects., Test that console objects are properly initialized., TestConsole

### Community 77 - "Chris Malek"
Cohesion: 0.67
Nodes (3): AUTHORS Credits, Chris Malek, MIT License

### Community 78 - "Bibliographic Provenance"
Cohesion: 0.67
Nodes (3): Acquisition Provenance, Bibliographic Provenance, SourceProvenanceService

### Community 79 - "Old English Morphological Analyser"
Cohesion: 1.00
Nodes (3): Old English Morphological Analyser, Old English Morphological Analysis Tool, 95% Morphological Recall Claim

### Community 80 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 82 - "PageClass"
Cohesion: 0.09
Nodes (50): _prepare_overrides(), Validate and convert optional CLI override values. Args: mode: Optional…, CoordinateSpace, FlagSeverity, PageClass, PreparationMode, PreparedPage, Page-level layout cohorts used by preparation and evaluation. (+42 more)

### Community 91 - "test_preparation_service.py"
Cohesion: 0.15
Nodes (34): PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, MonkeyPatch (+26 more)

### Community 99 - "test_cli_commands.py"
Cohesion: 0.38
Nodes (5): patch, Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIRun

### Community 100 - "RunnerExecutionService"
Cohesion: 0.18
Nodes (12): BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all bochord errors., RunnerEndpointUnavailable (+4 more)

### Community 101 - "Image"
Cohesion: 0.18
Nodes (11): dark_gutter_image(), dense_two_column_image(), Image, Build a synthetic two-column page with short text-run bars. Keyword Args:…, Build a page of horizontal text-like bars, then rotate it. Keyword Args:…, Build a page with a dark vertical gutter in the center strip. Returns:…, Build a page dominated by sustained dark table rules. Keyword Args: rule_count:…, Persist a source raster and return its ``sha256:`` checksum label. Args: image:… (+3 more)

### Community 102 - "_choose_preparation_mode"
Cohesion: 0.25
Nodes (7): _choose_preparation_mode(), Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve subdivision mode from automation or operator override. Args:…, Choose subdivision mode from page class and quality signals. Args: page_class:…, _resolve_preparation_mode(), _signal_value()

### Community 104 - "RunnerInputPackager"
Cohesion: 0.28
Nodes (17): Package one planned batch into a hosted-runner input artifact., RunnerInputPackager, bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests. (+9 more)

### Community 105 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``bochord run``.

### Community 106 - "test_runner_execution.py"
Cohesion: 0.15
Nodes (31): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+23 more)

### Community 107 - ".validate_https_huggingface_endpoints"
Cohesion: 0.27
Nodes (4): AnyHttpUrl, Validate settings and ensure required directories exist. Raises:…, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…, field_validator

### Community 108 - "_table_rule_signal"
Cohesion: 0.22
Nodes (10): _longest_dark_run(), Collect lengths of contiguous ``True`` runs. Args: mask: Boolean sequence.…, Return the longest contiguous run of values below ``threshold``. Args: values:…, Mark rows whose longest dark run spans enough of the page width. Args: gray:…, Mark columns whose longest dark run spans enough of the page height. Args:…, Count sustained dark horizontal and vertical rules. Args: gray: Grayscale…, _rule_column_mask(), _rule_row_mask() (+2 more)

### Community 109 - "._package_pdf"
Cohesion: 0.27
Nodes (9): _load_rgb_images(), Image, Path, Return the canonical checksum label for ``payload``. Args: payload: Raw…, Combine prepared images into one PDF runner input. Args: batch: Planned batch…, Open source images as RGB, closing partial loads on failure. Args:…, Persist ``images`` as one multi-page PDF at ``destination``. Args: images: Open…, _sha256_label() (+1 more)

### Community 110 - "MockHttpxClient"
Cohesion: 0.39
Nodes (5): MockHttpxClient, Any, BaseException, Response, Minimal httpx client stand-in for hosted runner tests.

### Community 111 - "QualitySignal"
Cohesion: 0.10
Nodes (36): AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _bleedthrough_signal(), _border_shadow_signal(), _colored_marking_signal() (+28 more)

### Community 112 - "Separate Text Structure Style Score Families"
Cohesion: 0.29
Nodes (7): Separate Text Structure Style Score Families, Spec 0003 Evaluation Schema Completion Plan, StyleEvaluationSummary, watchlist_exact_match_rate, Coverage Metric for OCR Comparison, OCR Is a Routing and Evaluation Problem, I Spent the Summer Testing 14 OCR Engines

### Community 113 - "Spec 0009: Merge and Alignment"
Cohesion: 0.40
Nodes (5): Trust States machine/reviewed/corrected, Spec 0009: Merge and Alignment, Abstaining Merge Policy, Machine/Merge/Trust Confidence Triad, Structure Scaffold Selection

### Community 114 - "PreparationBundleService"
Cohesion: 0.50
Nodes (3): PreparationBundleService, Acquire source pages and persist per-page preparation bundles. Args:…, Bind acquisition and per-page preparation collaborators. Args:…

### Community 115 - "_transport_failure_warning"
Cohesion: 0.67
Nodes (3): Build a warning message for one hosted transport-layer failure. Args: item_id:…, _transport_failure_warning(), RequestError

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
- **89 isolated node(s):** `release.sh script`, `bochord`, `IPA_AUDIO`, `AUTHORS Credits`, `Contributor Covenant 3.0` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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
- **Why does `SchemaModel` connect `models/__init__.py` to `cli.py`, `evaluation_cohorts.py`, `test_evaluation_service.py`, `BundlePage`, `Image`, `services/evaluation.py`, `RunnerReference`, `PagePreparationOverride`, `RunnerThroughputSummary`, `QualitySignal`, `PageClass`, `PreparedArtifactRef`, `PackagedRunnerInput`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `BundlePage` connect `BundlePage` to `cli.py`, `models/__init__.py`, `test_evaluation_service.py`, `._write_page_xml`, `services/evaluation.py`, `TestOcrModels`, `PageXmlInterchangeService`, `test_page_interchange.py`, `model_validator`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `PageClass` connect `PageClass` to `cli.py`, `evaluation_cohorts.py`, `models/__init__.py`, `test_evaluation_service.py`, `_choose_preparation_mode`, `services/evaluation.py`, `PagePreparationOverride`, `QualitySignal`, `services/preparation.py`, `recipe`, `test_preparation_service.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._