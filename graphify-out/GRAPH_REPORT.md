# Graph Report - feature-spec-0013-pass-runner-interface-schema  (2026-08-01)

## Corpus Check
- 86 files · ~118,877 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2036 nodes · 4615 edges · 116 communities (104 shown, 12 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 388 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `80b9953f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models/__init__.py
- test_preparation_service.py
- cli.py
- test_olmocr_runner.py
- test_evaluation_service.py
- test_runner_execution.py
- test_cli_utils.py
- evaluation_cohorts.py
- HuggingFaceOlmocrRunner
- run_runner
- Settings
- RunnerExecutionOrchestrator
- check_napoleon_gate.py
- _persist_prepared_page
- QualitySignal
- services/preparation.py
- PageXmlInterchangeService
- test_page_interchange.py
- TestOcrModels
- cli
- PageClass
- NoteRecord
- BundlePage
- source_acquisition.py
- model_validator
- ._resolve_context
- _normalize_page_overrides
- RunnerBatchPlanner
- services/evaluation.py
- Spec 0012 Runner Execution and Batching Implementation Plan
- test_ocr_models.py
- Detailed OCR Process
- AGENTS.md
- bochord
- Seven-stage OCR-to-structured-data pipeline
- test_cli_commands.py
- TestCLISettings
- RunnerReference
- Spec 0007: PDF-to-Image Preparation
- Spec 0004: Ordered V1 Implementation
- Phase 1 PAGE Interoperability Spike Plan
- i-mutation / i-umlaut
- conftest.py
- ._coords
- AGENTS.md
- Raw OCR witness layer
- ._write_page_xml
- Spec 0002: V1 Bundle Layout and Data Shape
- Python Coding Standards
- Hugging Face Setup Runbook
- File Map
- Separate Text Structure Style Score Families
- Bundle JSON Export
- DocumentRunOrchestrator
- Gold Annotation Protocol
- Spec 0003: V1 Evaluation Schema
- Anglian dialect group
- .validate_operator_override
- Review Overlay
- ADR 0009 OCR-D PAGE eScriptorium
- Pass Runner
- Normalized Page Graph
- Spec 0005: Human Markup and Review
- Configuration: Command Line Tool
- TestCLIVersion
- .validate_item_page_alignment
- Page Graph
- PagePreparationService
- Mission: Old English Grammar And Translation
- Point
- Spec 0010 Page Classification and Cohorts Implementation Plan
- ADR 0004 Layered Truth
- Reference 0006 OCR Output Formats
- oe-grammar/RESOURCES.md
- TestCLIErrorHandling
- Spec 0002 V1 Bundle Layout Implementation Plan
- Spec 0008 Text and Normalization Implementation Plan
- Lesson 0003 Pronouncing Old English Letters
- Spec 0009 Merge and Alignment Implementation Plan
- ADR 0005 Evaluation First
- Guide to Old English Textbook
- Chris Malek
- Bibliographic Provenance
- Character Error Rate (CER)
- Machine Assistance Mission
- bochord
- File Map
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
- RunnerInputPackager
- Spec 0007 Preparation Completion Implementation Plan
- Spec 0013 Pass-Runner Interface Schema Implementation Plan
- Phase 1 PAGE/eScriptorium Interoperability Spike Implementation Plan
- Spec 0003 Evaluation Schema Completion Implementation Plan
- machine-assistance/RESOURCES.md
- Mission: Machine Assistance For Old English Work
- bochord Context
- Architecture Index
- _PreparedInputsManifest
- machine-assistance/NOTES.md
- teaching/README.md

## God Nodes (most connected - your core abstractions)
1. `SchemaModel` - 80 edges
2. `PageClass` - 45 edges
3. `PreparationMode` - 44 edges
4. `PlannedRunnerBatch` - 44 edges
5. `PreparedArtifactRef` - 41 edges
6. `HuggingFaceOlmocrRunner` - 41 edges
7. `cli()` - 40 edges
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

## Communities (116 total, 12 thin omitted)

### Community 0 - "models/__init__.py"
Cohesion: 0.04
Nodes (81): AcceptReviewEvent, BaselineShift, ChunkType, CorrectStyleReviewEvent, CorrectTextReviewEvent, DatasetSplit, FlagReviewEvent, FontFamilyCandidate (+73 more)

### Community 1 - "test_preparation_service.py"
Cohesion: 0.06
Nodes (92): prepare_pages(), Acquire and prepare source pages into a reproducible output bundle. Args:…, Reject mixing per-page overrides with legacy global CLI overrides. Keyword…, Reject global CLI overrides when multiple recipes are requested. Args:…, _reject_conflicting_overrides(), _reject_multi_recipe_global_overrides(), PageClassifier, PagePreparationService (+84 more)

### Community 2 - "cli.py"
Cohesion: 0.07
Nodes (57): BatchItemRef, BatchUnitKind, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Batch grouping units for runner execution., Runner packaging policies. (+49 more)

### Community 3 - "test_olmocr_runner.py"
Cohesion: 0.17
Nodes (35): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+27 more)

### Community 4 - "test_evaluation_service.py"
Cohesion: 0.08
Nodes (66): bochord.models Package, BoundingBox, GoldCoverage, GoldPageAnnotation, GoldTextSpan, LineRecord, Gold diplomatic and normalized text target., Gold diplomatic and normalized text target. (+58 more)

### Community 5 - "test_runner_execution.py"
Cohesion: 0.17
Nodes (32): HostedInvocationResult, Raw result returned from one hosted runner invocation., Thin facade that delegates one run to ``RunnerExecutionOrchestrator``. Args:…, RunnerExecutionService, execution_service(), _fail_all_items(), _fail_second_item(), fixture_root() (+24 more)

### Community 6 - "test_cli_utils.py"
Cohesion: 0.05
Nodes (36): create_progress(), print_error(), print_info(), print_success(), Create a rich progress indicator for long-running operations. Returns:…, Print error message with optional suggestions. Args: message: Error message…, Print success message. Args: message: Success message, Print informational message. Args: message: Informational message (+28 more)

### Community 7 - "evaluation_cohorts.py"
Cohesion: 0.10
Nodes (43): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+35 more)

### Community 8 - "HuggingFaceOlmocrRunner"
Cohesion: 0.07
Nodes (32): _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _load_direct_image(), _load_image_from_pdf(), Any, Image, Path (+24 more)

### Community 9 - "run_runner"
Cohesion: 0.14
Nodes (20): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), Context, Path, Print the some version info of this package, (+12 more)

### Community 10 - "Settings"
Cohesion: 0.06
Nodes (33): AnyHttpUrl, BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:… (+25 more)

### Community 11 - "RunnerExecutionOrchestrator"
Cohesion: 0.07
Nodes (34): BatchResultStatus, Execution outcome for one runner batch., Exact persisted record for one runner invocation., Exact persisted record for one runner invocation., RunnerExecutionBatch, _atomic_write_text(), _derive_result_status(), Path (+26 more)

### Community 12 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 13 - "_persist_prepared_page"
Cohesion: 0.11
Nodes (22): _build_prepared_units(), _fixed_tile_boxes(), _persist_prepared_page(), _persist_recipe(), _prepared_coordinate_space(), _prepared_unit_from_box(), Path, Format a SHA-256 digest label for ``payload``. Args: payload: Bytes to hash.… (+14 more)

### Community 14 - "QualitySignal"
Cohesion: 0.10
Nodes (36): AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _bleedthrough_signal(), _border_shadow_signal(), _colored_marking_signal() (+28 more)

### Community 15 - "services/preparation.py"
Cohesion: 0.07
Nodes (56): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _column_ink_profile(), _column_unit_boxes() (+48 more)

### Community 16 - "PageXmlInterchangeService"
Cohesion: 0.12
Nodes (17): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+9 more)

### Community 17 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (32): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+24 more)

### Community 18 - "TestOcrModels"
Cohesion: 0.05
Nodes (32): capability_payload(), execution_batch_payload(), model_runner_payload(), parametrize, Return fields required by every review event., Return fields required by every review event., Contract checks for persisted OCR schema models., Review-event schema should discriminate on ``action``. (+24 more)

### Community 19 - "cli"
Cohesion: 0.09
Nodes (18): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test global CLI options., Test verbose flag is properly set. (+10 more)

### Community 20 - "PageClass"
Cohesion: 0.09
Nodes (53): _prepare_overrides(), Validate and convert optional CLI override values. Args: mode: Optional…, CoordinateSpace, FlagSeverity, PageClass, PreparationMode, PreparedPage, Page-level layout cohorts used by preparation and evaluation. (+45 more)

### Community 21 - "NoteRecord"
Cohesion: 0.19
Nodes (11): GoldNoteLink, NoteRecord, Gold note-marker linkage target., Gold note-marker linkage target., Accepted note object in the page graph., Accepted note object in the page graph., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold… (+3 more)

### Community 22 - "BundlePage"
Cohesion: 0.05
Nodes (48): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., BundlePage, EvaluationFamilySummary, EvaluationFlag, Canonical exported page object., Canonical exported page object. (+40 more)

### Community 23 - "source_acquisition.py"
Cohesion: 0.09
Nodes (35): _artifact_from_raster(), _image_bounds_cover_page(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), _pdf_page_image(), Image (+27 more)

### Community 24 - "model_validator"
Cohesion: 0.05
Nodes (27): CorrectGeometryReviewEvent, model_validator, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Event replacing object geometry without changing its content., Event replacing object geometry without changing its content. (+19 more)

### Community 25 - "._resolve_context"
Cohesion: 0.18
Nodes (10): _choose_preparation_mode(), Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve assessment, class, and subdivision choices for one page. Args:…, Resolve final page class from automation or operator override. Args: suggested:…, Resolve subdivision mode from automation or operator override. Args:…, Choose subdivision mode from page class and quality signals. Args: page_class:…, _resolve_page_class() (+2 more)

### Community 26 - "_normalize_page_overrides"
Cohesion: 0.50
Nodes (4): _index_page_overrides(), _normalize_page_overrides(), Index page overrides and reject duplicate or inconsistent ids. Args:…, Index page overrides by ``source_page_id``. Args: overrides: Validated page…

### Community 27 - "RunnerBatchPlanner"
Cohesion: 0.18
Nodes (26): Declared pass-runner input and batching contract., Declared pass-runner input and batching contract., RunnerCapability, Plan fixed runner batches from prepared artifacts and policy., RunnerBatchPlanner, Return a valid runner execution policy payload with optional overrides., Return a valid runner execution policy payload with optional overrides., runner_policy_payload() (+18 more)

### Community 28 - "services/evaluation.py"
Cohesion: 0.08
Nodes (33): AnchoredGoldAnnotation, GoldRegionAnnotation, GoldStyleSpan, Gold annotation that resolves to graph evidence or prepared image geometry., Gold annotation that resolves to graph evidence or prepared image geometry., Gold style target for one span or image-anchored area., Gold style target for one span or image-anchored area., Gold region or structure target. (+25 more)

### Community 29 - "Spec 0012 Runner Execution and Batching Implementation Plan"
Cohesion: 0.15
Nodes (12): Cost Stop, Dependency Decision, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0012 Runner Execution and Batching Implementation Plan, Subagent Model Policy (+4 more)

### Community 30 - "test_ocr_models.py"
Cohesion: 0.04
Nodes (69): AcquisitionProvenance, BibliographicProvenance, DocumentBundle, DocumentEvaluationSummary, ExportSummary, GoldDocument, GoldLineJoin, ObjectProvenance (+61 more)

### Community 31 - "Detailed OCR Process"
Cohesion: 0.23
Nodes (17): Detailed OCR Process, Kraken Runner, OCR Produces Evidence, Philological Watchlists, Stage 4 Align Evidence, Stage 7 Apply Overlays, Stage 3 Competing OCR Passes, Stage 6 Evaluate Against Gold (+9 more)

### Community 32 - "AGENTS.md"
Cohesion: 0.09
Nodes (23): bochord.cli Package, main(), bochord.services Package, DdlExtractor, ExtractionOrchestrator, RunStats, bochord Virtual Environment, boto3 Library (+15 more)

### Community 33 - "bochord"
Cohesion: 0.22
Nodes (11): bochord, Image-First OCR Orchestration, Preparation Recipe, Witness Production, API Models Autodoc, OCR Evidence Not Philological Semantics, Changelog, Sphinx Docs Index (+3 more)

### Community 34 - "Seven-stage OCR-to-structured-data pipeline"
Cohesion: 0.17
Nodes (11): New applied learning goal: difficult Old English OCR to structured data, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation, Page preparation ladder (least destructive first) (+3 more)

### Community 35 - "test_cli_commands.py"
Cohesion: 0.23
Nodes (8): patch, Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIEval, TestCLIRun

### Community 36 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 37 - "RunnerReference"
Cohesion: 0.08
Nodes (25): BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all bochord errors., RunnerEndpointUnavailable (+17 more)

### Community 38 - "Spec 0007: PDF-to-Image Preparation"
Cohesion: 0.15
Nodes (13): V1 Gold Data Expectations, Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Coordinate and Image Provenance, Page Subdivision into OCR Units, Preparation Pipeline Stage, Spec 0010: Page Classification and Cohorts, Page-Class Evaluation Cohorts (+5 more)

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

### Community 44 - "AGENTS.md"
Cohesion: 0.17
Nodes (10): ADRs, Architecture (Required), AWS Interaction, Documentation Contract (Required), graphify, Implementation Priority (Required), Post-Implementation Quality Gate (Required), Project Structure (Mandatory) (+2 more)

### Community 45 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 46 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Merge PAGE-supported corrections into canonical sidecar data. Args:…

### Community 47 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.18
Nodes (11): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Review Overlays, Diplomatic Text Review, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0014: Review Task and Overlay Schema (+3 more)

### Community 48 - "Python Coding Standards"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 49 - "Hugging Face Setup Runbook"
Cohesion: 0.31
Nodes (11): Client-Side Queue for Cold Starts, Custom OCR Container, Hugging Face Setup Runbook, Hugging Face Inference Endpoints, Immutable Model Commit Pinning, Local Laptop Boundary, RunnerReference Provenance, olmOCR Runner (+3 more)

### Community 50 - "File Map"
Cohesion: 0.18
Nodes (10): Cost Stop, Dependency Decision, File Map, Global Constraints, Phase 3 Acquisition and Preparation Implementation Plan, Task 1: Preparation Contracts and Dependencies, Task 2: Source Acquisition, Task 3: Quality Assessment and Page Classification (+2 more)

### Community 51 - "Separate Text Structure Style Score Families"
Cohesion: 0.22
Nodes (9): GoldCoverage, Separate Text Structure Style Score Families, Spec 0003 Evaluation Schema Completion Plan, StyleEvaluationSummary, watchlist_exact_match_rate, Spec 0007 Preparation Completion Plan, Coverage Metric for OCR Comparison, OCR Is a Routing and Evaluation Problem (+1 more)

### Community 52 - "Bundle JSON Export"
Cohesion: 0.31
Nodes (9): Bundle JSON Export, Markdown Export, RAG JSON Export, Spec 0006: Exports and Retrieval Views, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 53 - "DocumentRunOrchestrator"
Cohesion: 0.22
Nodes (10): Document Bundle, Page Bundle, Page-Local Truth, ADR 0002 Bundle Model, Page Bundle as Page-Local Truth Unit, BundleWriter, DocumentRunOrchestrator, PageAlignmentService (+2 more)

### Community 54 - "Gold Annotation Protocol"
Cohesion: 0.33
Nodes (9): EvaluationService, bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, GoldDocument, MetricProfile, Phase 2 Gold Evaluator Plan, GoldLineJoin (+1 more)

### Community 55 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.22
Nodes (9): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Trust States machine/reviewed/corrected, Historical Character Preservation, Spec 0009: Merge and Alignment, Abstaining Merge Policy, Machine/Merge/Trust Confidence Triad (+1 more)

### Community 56 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 57 - ".validate_operator_override"
Cohesion: 0.25
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

### Community 62 - "Spec 0005: Human Markup and Review"
Cohesion: 0.25
Nodes (8): V1 Typography and Role Vocabulary, Spec 0005: Human Markup and Review, Evidence-Bound Human Review, Independent Review Dimensions, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence, Reject eScriptorium as Review Boundary, PAGE Region/Line Reuse Boundary

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

### Community 68 - "Mission: Old English Grammar And Translation"
Cohesion: 0.14
Nodes (11): Learner lacks stable conceptual map of sound-change order, Starting point: motivated Old English learner, not yet confident with sound-change map, Constraints, Read and translate Old English with grammatical confidence, Mission: Old English Grammar And Translation, Out of scope, OCR and engineering workflows out of scope for OE grammar workspace, Success looks like (+3 more)

### Community 69 - "Point"
Cohesion: 0.22
Nodes (7): Point, Polygon, One point in an identified image coordinate space., Polygon geometry for non-rectangular regions and curved text lines., Parse PAGE point strings into coordinate pairs. Args: points: Space-separated…, Derive one polygon from PAGE Coords when enough points exist. Args: coords:…, Derive one point list from PAGE Baseline or Coords. Args: element: Optional…

### Community 70 - "Spec 0010 Page Classification and Cohorts Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Global Constraints, Spec 0010 Page Classification and Cohorts Implementation Plan, Subagent Model Policy, Task 1: Emit Page-Class Preparation Guidance, Task 2: Define Evaluation Records and Cohort Output (+2 more)

### Community 71 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): Raw Witness Artifact, ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 72 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 73 - "oe-grammar/RESOURCES.md"
Cohesion: 0.20
Nodes (9): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), Proto-Germanic Introduction: Linguistic Methods, Gaps, Knowledge, Old English Grammar And Translation Resources (+1 more)

### Community 74 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 75 - "Spec 0002 V1 Bundle Layout Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0002 V1 Bundle Layout Implementation Plan, Subagent Model Policy, Task 1: Manifest Models and Path Helpers (+2 more)

### Community 76 - "Spec 0008 Text and Normalization Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0008 Text and Normalization Implementation Plan, Subagent Model Policy, Task 1: Freeze Normalization Policy Models (+2 more)

### Community 77 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 78 - "Spec 0009 Merge and Alignment Implementation Plan"
Cohesion: 0.18
Nodes (10): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0009 Merge and Alignment Implementation Plan, Subagent Model Policy, Task 1: Merge Models and Provenance Alternates (+2 more)

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

### Community 85 - "bochord"
Cohesion: 0.18
Nodes (10): bochord, Commands, Common Use Cases, Core Features, Feature 1, Feature 2, Installation, Quick Start (+2 more)

### Community 86 - "File Map"
Cohesion: 0.20
Nodes (9): Cost Stop, Dependency Decision, File Map, Global Constraints, Phase 2 Gold Protocol and Evaluator Implementation Plan, Task 1: Freeze Metric and Gold Contracts, Task 2: Text Evaluation, Task 3: Structure, Typography, Note Linkage, and Flags (+1 more)

### Community 88 - "Contributor Covenant 3.0"
Cohesion: 0.18
Nodes (10): Addressing and Repairing Harm, Attribution, Contributor Covenant 3.0, Encouraged Behaviors, Contributor Covenant, Other Restrictions, Our Pledge, Reporting an Issue (+2 more)

### Community 104 - "RunnerInputPackager"
Cohesion: 0.24
Nodes (18): Bind batch planning, packaging, and hosted runner collaborators. Args: planner:…, Package one planned batch into a hosted-runner input artifact., RunnerInputPackager, bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``. (+10 more)

### Community 105 - "Spec 0007 Preparation Completion Implementation Plan"
Cohesion: 0.20
Nodes (9): Cost Stop, Existing Baseline, File Map, Global Constraints, Spec 0007 Preparation Completion Implementation Plan, Subagent Model Policy, Task 1: Complete Acquisition and Recipe Provenance, Task 2: Preserve Competing Preparation Variants (+1 more)

### Community 106 - "Spec 0013 Pass-Runner Interface Schema Implementation Plan"
Cohesion: 0.20
Nodes (9): Cost Stop, Existing Baseline, File Map, Final Review Focus, Global Constraints, Spec 0013 Pass-Runner Interface Schema Implementation Plan, Subagent Model Policy, Task 1: Reject Mutable Model Revisions (+1 more)

### Community 107 - "Phase 1 PAGE/eScriptorium Interoperability Spike Implementation Plan"
Cohesion: 0.22
Nodes (8): Cost Stop, Dependency Decision, File Map, Global Constraints, Phase 1 PAGE/eScriptorium Interoperability Spike Implementation Plan, Task 1: Canonical PAGE XML Boundary, Task 2: Real eScriptorium Round Trip, Task 3: Exit Gate and Decision Record

### Community 108 - "Spec 0003 Evaluation Schema Completion Implementation Plan"
Cohesion: 0.22
Nodes (8): Cost Stop, Existing Baseline, File Map, Global Constraints, Spec 0003 Evaluation Schema Completion Implementation Plan, Subagent Model Policy, Task 1: Make Score Families Match Spec 0003, Task 2: Add Watchlist Exact-Match Rate and CLI Contract

### Community 109 - "machine-assistance/RESOURCES.md"
Cohesion: 0.22
Nodes (8): Lower CER can still reduce trustworthiness via silent normalization, Gaps, HIPE-OCRepair 2026 competition report, OCR Error Post-Correction with LLMs (Kanerva et al.), Knowledge, Machine Assistance For Old English Work Resources, olmOCR paper (Poznanski et al.), Wisdom (Communities)

### Community 110 - "Mission: Machine Assistance For Old English Work"
Cohesion: 0.33
Nodes (5): Constraints, Mission: Machine Assistance For Old English Work, Out of scope, Success looks like, Why

### Community 111 - "bochord Context"
Cohesion: 0.40
Nodes (4): bochord Context, Boundary, Canonical Terms, Mission

### Community 112 - "Architecture Index"
Cohesion: 0.50
Nodes (5): ADR 0001 Package Boundary, Acquire-Prepare-Pass-Align-Evaluate-Review-Export Workflow, ADR 0003 Page Graph, Architecture Index, Spec 0001 System Architecture

### Community 113 - "_PreparedInputsManifest"
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
- **220 isolated node(s):** `release.sh script`, `bochord`, `IPA_AUDIO`, `Tooling Preflight (Required)`, `ADRs` (+215 more)
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
- **Why does `SchemaModel` connect `test_ocr_models.py` to `models/__init__.py`, `cli.py`, `test_evaluation_service.py`, `Point`, `RunnerReference`, `evaluation_cohorts.py`, `test_runner_execution.py`, `RunnerExecutionOrchestrator`, `QualitySignal`, `services/preparation.py`, `PageClass`, `NoteRecord`, `BundlePage`, `RunnerBatchPlanner`, `services/evaluation.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `BundlePage` connect `BundlePage` to `models/__init__.py`, `cli.py`, `test_evaluation_service.py`, `._write_page_xml`, `PageXmlInterchangeService`, `test_page_interchange.py`, `TestOcrModels`, `model_validator`, `services/evaluation.py`, `test_ocr_models.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `PageClass` connect `PageClass` to `models/__init__.py`, `test_preparation_service.py`, `cli.py`, `test_evaluation_service.py`, `evaluation_cohorts.py`, `_persist_prepared_page`, `QualitySignal`, `services/preparation.py`, `BundlePage`, `._resolve_context`, `test_ocr_models.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._