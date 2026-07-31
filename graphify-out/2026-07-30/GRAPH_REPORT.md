# Graph Report - bochord  (2026-07-30)

## Corpus Check
- 78 files · ~246,720 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1756 nodes · 4290 edges · 106 communities (95 shown, 11 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 385 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9c5c37a9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/evaluation.py
- test_olmocr_runner.py
- evaluation_cohorts.py
- Settings
- models/__init__.py
- test_evaluation_service.py
- services/preparation.py
- check_napoleon_gate.py
- _RateAccumulator
- RunnerReference
- PageXmlInterchangeService
- TestCLIGlobalOptions
- test_page_interchange.py
- cli.py
- model_validator
- PlannedRunnerBatch
- model_runner_payload
- SourcePageArtifact
- PageClass
- BundlePage
- Stage 6 Evaluate Against Gold
- Machine Assistance Resources
- DocumentRunOrchestrator
- bochord
- Gold Annotation Protocol
- _normalize_page_overrides
- cli
- TestPrintInfo
- main
- Spec 0004: Ordered V1 Implementation
- Detailed OCR Process
- conftest.py
- i-mutation / i-umlaut
- test_cli_utils.py
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
- model_validator
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
- MetricProfile
- .validate_item_page_alignment
- Page Bundle
- Page Graph
- Spec 0003: V1 Evaluation Schema
- Reference 0006 OCR Output Formats
- OE Grammar Resources
- TestCLIErrorHandling
- TestPrintSuccess
- TestConsoleQuietMode
- GoldPageAnnotation
- ADR 0005 Evaluation First
- Lesson 0003 Pronouncing Old English Letters
- Guide to Old English Textbook
- TestConsole
- Chris Malek
- Bibliographic Provenance
- Old English Morphological Analyser
- Character Error Rate (CER)
- release.sh
- PreparationMode
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
- Point
- _choose_preparation_mode
- settings.py
- RunnerInputPackager
- _PreparedInputsManifest
- test_runner_execution.py
- .validate_https_huggingface_endpoints
- QualitySignal

## God Nodes (most connected - your core abstractions)
1. `SchemaModel` - 80 edges
2. `PageClass` - 45 edges
3. `PreparationMode` - 44 edges
4. `PlannedRunnerBatch` - 43 edges
5. `HuggingFaceOlmocrRunner` - 41 edges
6. `PreparedArtifactRef` - 40 edges
7. `PreparationRecipe` - 40 edges
8. `Settings` - 40 edges
9. `cli()` - 39 edges
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

## Communities (106 total, 11 thin omitted)

### Community 0 - "services/evaluation.py"
Cohesion: 0.10
Nodes (21): GoldNoteLink, Gold note-marker linkage target., _boxes_intersect(), _coverage_allows(), _edit_distance(), _graphemes(), _has_exhaustive_coverage(), _is_ligature() (+13 more)

### Community 1 - "test_olmocr_runner.py"
Cohesion: 0.13
Nodes (37): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Any (+29 more)

### Community 2 - "evaluation_cohorts.py"
Cohesion: 0.10
Nodes (43): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+35 more)

### Community 3 - "Settings"
Cohesion: 0.07
Nodes (29): BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Settings, Exception (+21 more)

### Community 4 - "models/__init__.py"
Cohesion: 0.04
Nodes (112): AcceptReviewEvent, AcquisitionProvenance, BaselineShift, BibliographicProvenance, ChunkType, CorrectGeometryReviewEvent, CorrectStyleReviewEvent, CorrectTextReviewEvent (+104 more)

### Community 5 - "test_evaluation_service.py"
Cohesion: 0.13
Nodes (46): BoundingBox, GoldCoverage, LineRecord, Explicit evaluation denominator and exclusion scope for a gold slice., Axis-aligned rectangle for page-relative geometry., Accepted text span in the page graph., Accepted line node in the page graph., SpanRecord (+38 more)

### Community 6 - "services/preparation.py"
Cohesion: 0.06
Nodes (66): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _build_prepared_units(), _column_count_signal() (+58 more)

### Community 7 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 8 - "_RateAccumulator"
Cohesion: 0.08
Nodes (28): AnchoredGoldAnnotation, EvaluationFlag, GoldStyleSpan, Gold annotation that resolves to graph evidence or prepared image geometry., Gold style target for one span or image-anchored area., One review-driving evaluation flag., _facet_match(), _RateAccumulator (+20 more)

### Community 9 - "RunnerReference"
Cohesion: 0.07
Nodes (23): Identity for one runner implementation and model revision., Declared pass-runner input and batching contract., RunnerCapability, RunnerReference, Bind one hosted olmOCR runner to endpoint settings and an HTTP client. Args:…, Return the runner identity used for hosted requests. Returns: Model-backed…, Return the declared olmOCR input and batching contract. Returns: Hosted olmOCR…, Client (+15 more)

### Community 10 - "PageXmlInterchangeService"
Cohesion: 0.12
Nodes (18): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+10 more)

### Community 11 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., TestCLIGlobalOptions

### Community 12 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (32): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+24 more)

### Community 13 - "cli.py"
Cohesion: 0.13
Nodes (26): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), prepare_pages(), Path, Print the some version info of this package, (+18 more)

### Community 14 - "model_validator"
Cohesion: 0.08
Nodes (13): model_validator, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Require at least one concrete replacement geometry. Returns: The validated…, Bind events to valid tasks, evidence revisions, targets, and actions. Returns:…, Require a resolvable anchor and explain every scoring exclusion. Returns: The…, Require an explanation for every scoring exclusion. Returns: The validated…, Require an explicit scope and explain every scoring exclusion. Returns: The… (+5 more)

### Community 15 - "PlannedRunnerBatch"
Cohesion: 0.06
Nodes (63): BatchItemRef, BatchResultStatus, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Runner packaging policies., Execution outcome for one runner batch. (+55 more)

### Community 16 - "model_runner_payload"
Cohesion: 0.67
Nodes (3): model_runner_payload(), Return a valid model-backed runner payload with optional overrides., test_model_backed_runner_requires_hardware_class()

### Community 17 - "SourcePageArtifact"
Cohesion: 0.09
Nodes (36): One acquired source page before preparation., SourcePageArtifact, Reject override ids that are absent from the acquired source. Args:…, _validate_page_override_ids(), _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key() (+28 more)

### Community 18 - "PageClass"
Cohesion: 0.10
Nodes (32): PageClass, Page-level layout cohorts used by preparation and evaluation., PreparationRecipe, PreparationResult, Full preparation outcome for one source page., Deterministic page-preparation profile., _build_assessment(), _build_preparation_result() (+24 more)

### Community 19 - "BundlePage"
Cohesion: 0.14
Nodes (18): BundlePage, FontSlant, Canonical exported page object., Orthogonal visual typography facets for one text span., Visual font-slant classification independent of weight and role., Accepted region node in the page graph., RegionRecord, Typography (+10 more)

### Community 20 - "Stage 6 Evaluate Against Gold"
Cohesion: 0.13
Nodes (18): Philological Watchlists, Separate Text Structure Style Score Families, Stage 7 Apply Overlays, Stage 6 Evaluate Against Gold, Stage 8 Export, Common OCR Failure Shapes, Spec 0003 Evaluation Schema Completion Plan, StyleEvaluationSummary (+10 more)

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
Cohesion: 0.24
Nodes (14): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Dictionary Headword Page page-0100 (+6 more)

### Community 25 - "_normalize_page_overrides"
Cohesion: 0.50
Nodes (4): _index_page_overrides(), _normalize_page_overrides(), Index page overrides and reject duplicate or inconsistent ids. Args:…, Index page overrides by ``source_page_id``. Args: overrides: Validated page…

### Community 26 - "cli"
Cohesion: 0.18
Nodes (10): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test the prepare command., Test prepare aborts before writes when override lacks a reason. (+2 more)

### Community 27 - "TestPrintInfo"
Cohesion: 0.33
Nodes (4): Test info printing functions., Test basic info printing., Test info panel has correct styling., TestPrintInfo

### Community 28 - "main"
Cohesion: 0.23
Nodes (8): main(), patch, Tests for the main module., Test the main function., Test that main function calls the CLI., Test that main function can be imported and called., Test that main function exists and is callable., TestMain

### Community 29 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.15
Nodes (15): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Evidence-Bound Human Review, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy (+7 more)

### Community 30 - "Detailed OCR Process"
Cohesion: 0.29
Nodes (13): Detailed OCR Process, Kraken Runner, OCR Produces Evidence, olmOCR Runner, Stage 1 Acquire Source, Stage 4 Align Evidence, Stage 3 Competing OCR Passes, Stage 5 Build Page Graph (+5 more)

### Community 31 - "conftest.py"
Cohesion: 0.21
Nodes (12): cli_context(), mock_console(), mock_settings(), fixture, Test configuration and fixtures for the ai-coding project. This file contains…, Create a CLI runner for testing., Create a temporary directory for testing., Create a mock console for testing. (+4 more)

### Community 32 - "i-mutation / i-umlaut"
Cohesion: 0.23
Nodes (13): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+5 more)

### Community 33 - "test_cli_utils.py"
Cohesion: 0.15
Nodes (13): print_error(), print_info(), print_success(), Print error message with optional suggestions. Args: message: Error message…, Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test error printing functions. (+5 more)

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
Cohesion: 0.17
Nodes (7): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., TestCLISettings

### Community 38 - "create_progress"
Cohesion: 0.22
Nodes (8): create_progress(), Create a rich progress indicator for long-running operations. Returns:…, Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress

### Community 39 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Merge PAGE-supported corrections into canonical sidecar data. Args:…

### Community 40 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Trust States machine/reviewed/corrected, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0009: Merge and Alignment (+3 more)

### Community 41 - "Python Coding Standards"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 42 - "Architecture Index"
Cohesion: 0.22
Nodes (10): Hosted Inference Boundary, PAGE Interchange, ADR 0003 Page Graph, ADR 0007 V1 Engine Strategy, Hugging Face Hosted Endpoints, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+2 more)

### Community 43 - "Hugging Face Setup Runbook"
Cohesion: 0.36
Nodes (10): Client-Side Queue for Cold Starts, Custom OCR Container, Hugging Face Setup Runbook, Hugging Face Inference Endpoints, Immutable Model Commit Pinning, Local Laptop Boundary, RunnerReference Provenance, Spec 0012 Runner Execution Batching Plan (+2 more)

### Community 44 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 45 - "ADR 0004 Layered Truth"
Cohesion: 0.22
Nodes (9): Bundle JSON Export, Markdown Export, RAG JSON Export, Raw Witness Artifact, ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Rebuild Derived Outputs From Raw Artifacts (+1 more)

### Community 46 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 47 - "PagePreparationService"
Cohesion: 0.25
Nodes (9): Phase 3 Acquisition Preparation Plan, PagePreparationService, Pillow and pypdfium2 Stack, SourceAcquisitionService, Spec 0007 Preparation Completion Plan, Preparation Recipe Variants, Spec 0010 Page Classification Cohorts Plan, Weighted Evaluation Cohorts (+1 more)

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
Cohesion: 0.18
Nodes (11): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Review Overlays, V1 Typography and Role Vocabulary, Spec 0014: Review Task and Overlay Schema, correct_text Event Semantics, PageOverlay Append-Only Log, ReviewTask Packet (+3 more)

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
Cohesion: 0.43
Nodes (7): Note-Heavy Page page-0010, BundlePage Canonical JSON, Phase 1 PAGE Interoperability Spike Plan, PageXmlInterchangeService, Reject ocrd-models for Spike, The Phonology of Old English Inflections, Reject Keyser Metathesis and Vowel Deletion

### Community 58 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 59 - "HuggingFaceOlmocrRunner"
Cohesion: 0.06
Nodes (51): BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all bochord errors., RunnerEndpointUnavailable (+43 more)

### Community 60 - "MetricProfile"
Cohesion: 0.09
Nodes (22): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., GoldRegionAnnotation, GoldTextSpan, Gold diplomatic and normalized text target., Gold region or structure target., _box_iou() (+14 more)

### Community 61 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

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

### Community 70 - "GoldPageAnnotation"
Cohesion: 0.22
Nodes (11): GoldPageAnnotation, NoteRecord, Gold data slice for one page., Accepted note object in the page graph., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold…, Aggregate note-linkage success for covered gold edges. Args: prediction:…, Map predicted note ids to gold region annotation ids that name them. Args:… (+3 more)

### Community 71 - "ADR 0005 Evaluation First"
Cohesion: 0.50
Nodes (5): Gold Slice, Watchlist Metric, ADR 0005 Evaluation First, Separate Evaluation Score Families, EvaluationService

### Community 73 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

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

### Community 82 - "PreparationMode"
Cohesion: 0.16
Nodes (29): _prepare_overrides(), Validate and convert optional CLI override values. Args: mode: Optional…, CoordinateSpace, FlagSeverity, PreparationMode, PreparedPage, Prepared-page subdivision modes., Supported top-level source kinds. (+21 more)

### Community 91 - "test_preparation_service.py"
Cohesion: 0.06
Nodes (90): PagePreparationOverride, Operator override for one acquired source page., PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:… (+82 more)

### Community 99 - "test_cli_commands.py"
Cohesion: 0.38
Nodes (5): patch, Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIRun

### Community 101 - "Point"
Cohesion: 0.33
Nodes (4): Point, One point in an identified image coordinate space., Parse PAGE point strings into coordinate pairs. Args: points: Space-separated…, Derive one point list from PAGE Baseline or Coords. Args: element: Optional…

### Community 102 - "_choose_preparation_mode"
Cohesion: 0.25
Nodes (7): _choose_preparation_mode(), Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve subdivision mode from automation or operator override. Args:…, Choose subdivision mode from page class and quality signals. Args: page_class:…, _resolve_preparation_mode(), _signal_value()

### Community 104 - "RunnerInputPackager"
Cohesion: 0.10
Nodes (29): Bind collaborators and run identifiers for one execution segment. Keyword Args:…, Bind batch planning, packaging, and hosted runner collaborators. Args: planner:…, _load_rgb_images(), _page_numbers(), Image, Path, Package one planned batch into a hosted-runner input artifact., Package one batch using the requested strategy. Args: batch: Planned batch… (+21 more)

### Community 105 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``bochord run``.

### Community 106 - "test_runner_execution.py"
Cohesion: 0.10
Nodes (50): Plan fixed runner batches from prepared artifacts and policy., RunnerBatchPlanner, InvokeResult, Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), artifacts(), capability() (+42 more)

### Community 107 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…, field_validator

### Community 111 - "QualitySignal"
Cohesion: 0.10
Nodes (37): QualitySignal, One measured image-quality signal from preparation assessment., _bleedthrough_signal(), _border_shadow_signal(), _colored_marking_signal(), _contrast_signal(), _effective_dpi_signal(), _gutter_shadow_signal() (+29 more)

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
- **Why does `BundlePage` connect `BundlePage` to `services/evaluation.py`, `models/__init__.py`, `test_evaluation_service.py`, `GoldPageAnnotation`, `._write_page_xml`, `_RateAccumulator`, `PageXmlInterchangeService`, `test_page_interchange.py`, `cli.py`, `model_validator`, `MetricProfile`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `services/evaluation.py`, `evaluation_cohorts.py`, `test_evaluation_service.py`, `services/preparation.py`, `GoldPageAnnotation`, `_RateAccumulator`, `Point`, `RunnerReference`, `test_preparation_service.py`, `PlannedRunnerBatch`, `QualitySignal`, `SourcePageArtifact`, `PreparationMode`, `BundlePage`, `PageClass`, `HuggingFaceOlmocrRunner`, `MetricProfile`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `cli()` connect `cli` to `test_cli_utils.py`, `test_cli_commands.py`, `Settings`, `TestCLIErrorHandling`, `TestCLISettings`, `TestCLIGlobalOptions`, `cli.py`, `TestCLIEval`, `TestCLIVersion`, `main`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._