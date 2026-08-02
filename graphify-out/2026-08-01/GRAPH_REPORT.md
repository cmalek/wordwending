# Graph Report - bochord  (2026-07-31)

## Corpus Check
- 102 files · ~275,271 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2306 nodes · 5992 edges · 126 communities (114 shown, 12 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 559 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a84dc556`
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
- PageClass
- HuggingFaceOlmocrRunner
- ._resolve_context
- TestConfiguration
- cli.py
- check_napoleon_gate.py
- model_validator
- QualitySignal
- test_merge_service.py
- PageXmlInterchangeService
- test_page_interchange.py
- TestOcrModels
- cli
- services/merge.py
- services/evaluation.py
- _RateAccumulator
- PreparationRecipe
- services/preparation.py
- TestCLIGlobalOptions
- PreparedArtifactRef
- Spec 0002: V1 Bundle Layout and Data Shape
- test_bundle_layout.py
- services/bundle_layout.py
- test_text_normalization.py
- Detailed OCR Process
- BundleLayoutService
- Architecture Index
- Machine Assistance Resources
- Settings
- GoldPageAnnotation
- _parse_native_corrected
- Spec 0007: PDF-to-Image Preparation
- Spec 0004: Ordered V1 Implementation
- Phase 1 PAGE Interoperability Spike Plan
- i-mutation / i-umlaut
- conftest.py
- ._coords
- ._write_page_xml
- Raw OCR witness layer
- BundlePage
- BundlePaths
- Python Coding Standards
- Hugging Face Setup Runbook
- Spec 0005: Human Markup and Review
- Separate Text Structure Style Score Families
- Bundle JSON Export
- DocumentRunOrchestrator
- Gold Annotation Protocol
- PagePreparationOverride
- OE Grammar Resources
- prepare_pages
- Review Overlay
- ADR 0009 OCR-D PAGE eScriptorium
- Pass Runner
- Normalized Page Graph
- AGENTS.md
- Configuration: Command Line Tool
- SourceAcquisitionService
- _pixel_access
- Page Graph
- PagePreparationService
- Learner lacks stable conceptual map of sound-change order
- Spec 0003: V1 Evaluation Schema
- execution_batch_payload
- ADR 0004 Layered Truth
- Reference 0006 OCR Output Formats
- Comparative method of reconstruction
- TestCLISettings
- RunnerReference
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
- _border_shadow_signal
- _detect_structure_conflict
- Spec 0002 V1 Bundle Layout Implementation Plan
- Spec 0008 Text and Normalization Implementation Plan
- Spec 0009 Merge and Alignment Implementation Plan
- Spec 0013 Pass-Runner Interface Schema Implementation Plan
- PlannedRunnerBatch
- TestCLIVersion
- Image
- _measure_skew_degrees
- .settings_customise_sources
- TestPrintSuccess
- TestConsoleQuietMode
- _prepared_unit_from_box
- TestConsole
- TestCLIErrorHandling
- .prepare
- _build_preparation_result
- TestCLIEval
- test_prepared_unit_rejects_missing_or_empty_lineage_fields
- test_configuration.py
- recipe_payload

## God Nodes (most connected - your core abstractions)
1. `AlternateCandidate` - 114 edges
2. `SchemaModel` - 99 edges
3. `MergePolicy` - 54 edges
4. `BundlePage` - 53 edges
5. `SpanRecord` - 50 edges
6. `CoordinateSpace` - 49 edges
7. `BundlePaths` - 48 edges
8. `PageClass` - 48 edges
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

## Communities (126 total, 12 thin omitted)

### Community 0 - "models/__init__.py"
Cohesion: 0.04
Nodes (145): AlternateCandidate, MergeFlag, MergeFlagType, MergePageResult, StrEnum, One material merge disagreement surfaced for human review., Accepted page graph plus merge flags and abstention state., Material merge disagreement categories emitted as review flags. (+137 more)

### Community 1 - "test_preparation_service.py"
Cohesion: 0.10
Nodes (52): PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, MonkeyPatch (+44 more)

### Community 2 - "MergeOrchestrator"
Cohesion: 0.05
Nodes (45): _apply_note_link_resolution(), _mapped_note_link_sets(), _MarkerMappingContext, MergeOrchestrator, _note_link_alternates(), _note_marker_links_from_mapped_sets(), _note_marker_links_when_mapping_ambiguous(), _NoteCandidate (+37 more)

### Community 3 - "test_olmocr_runner.py"
Cohesion: 0.13
Nodes (41): hosted_runner(), mock_client(), MockHttpxClient, olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint() (+33 more)

### Community 4 - "test_evaluation_service.py"
Cohesion: 0.11
Nodes (51): BoundingBox, GoldCoverage, GoldNoteLink, GoldRegionAnnotation, Gold region or structure target., Gold note-marker linkage target., Explicit evaluation denominator and exclusion scope for a gold slice., Axis-aligned rectangle for page-relative geometry. (+43 more)

### Community 5 - "test_runner_execution.py"
Cohesion: 0.15
Nodes (33): HostedInvocationResult, Raw result returned from one hosted runner invocation., InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root() (+25 more)

### Community 6 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): print_info(), print_success(), Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling. (+1 more)

### Community 7 - "PageClass"
Cohesion: 0.06
Nodes (61): _prepare_overrides(), Validate and convert optional CLI override values. Args: mode: Optional…, EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view. (+53 more)

### Community 8 - "HuggingFaceOlmocrRunner"
Cohesion: 0.07
Nodes (45): InputKind, Runner input artifact categories., One raw witness artifact emitted by a pass runner., RunnerOutputArtifact, HostedEndpointPolicy, PackagedRunnerInput, StrEnum, Packaged artifact ready for hosted runner submission. (+37 more)

### Community 9 - "._resolve_context"
Cohesion: 0.25
Nodes (6): Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve assessment, class, and subdivision choices for one page. Args:…, Resolve final page class from automation or operator override. Args: suggested:…, _resolve_page_class(), _signal_value()

### Community 10 - "TestConfiguration"
Cohesion: 0.08
Nodes (18): Exception, patch, Test that settings fields have proper descriptions., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder…, Test that environment variables override defaults., Test that settings are case insensitive. (+10 more)

### Community 11 - "cli.py"
Cohesion: 0.06
Nodes (47): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``bochord run``., Execute prepared artifacts against one hosted olmOCR runner. Args: ctx: Click…, run_runner(), BochordError, ConfigurationError, FileError (+39 more)

### Community 12 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 13 - "model_validator"
Cohesion: 0.08
Nodes (13): model_validator, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Require at least one concrete replacement geometry. Returns: The validated…, Bind events to valid tasks, evidence revisions, targets, and actions. Returns:…, Require a resolvable anchor and explain every scoring exclusion. Returns: The…, Require an explanation for every scoring exclusion. Returns: The validated…, Require an explicit scope and explain every scoring exclusion. Returns: The… (+5 more)

### Community 14 - "QualitySignal"
Cohesion: 0.13
Nodes (28): FlagSeverity, Severity levels for review and evaluation flags., AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _bleedthrough_signal() (+20 more)

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
Cohesion: 0.12
Nodes (10): Return fields required by every review event., Contract checks for persisted OCR schema models., Review-event schema should discriminate on ``action``., A review task should be actionable without undocumented context., Preferred input must be one of the runner's accepted inputs., Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary. (+2 more)

### Community 19 - "cli"
Cohesion: 0.14
Nodes (14): cli(), Settings-related commands. Args: ctx: Click context object., bochord command line interface. Args: ctx: Click context object. verbose:…, show_settings(), Context, group, pass_context, _dense_two_column_image() (+6 more)

### Community 20 - "services/merge.py"
Cohesion: 0.04
Nodes (102): PassWitnessPage, One runner's proposed page graph fragment for merge input., NoteRecord, Orthogonal visual typography facets for one text span., Semantic role kept separate from visual typography., Accepted text span in the page graph., Accepted note object in the page graph., SpanRecord (+94 more)

### Community 21 - "services/evaluation.py"
Cohesion: 0.12
Nodes (20): Independent evidence dimensions a human may inspect and certify., ReviewDimension, _boxes_intersect(), _coverage_allows(), _edit_distance(), _graphemes(), _has_exhaustive_coverage(), _is_ligature() (+12 more)

### Community 22 - "_RateAccumulator"
Cohesion: 0.08
Nodes (28): EvaluationFlag, GoldStyleSpan, Gold style target for one span or image-anchored area., One review-driving evaluation flag., _facet_match(), _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:… (+20 more)

### Community 23 - "PreparationRecipe"
Cohesion: 0.10
Nodes (36): PreparationRecipe, One acquired source page before preparation., Deterministic page-preparation profile., SourcePageArtifact, _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key() (+28 more)

### Community 24 - "services/preparation.py"
Cohesion: 0.12
Nodes (24): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _crop_box(), _fill_color() (+16 more)

### Community 25 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 26 - "PreparedArtifactRef"
Cohesion: 0.09
Nodes (43): BatchItemRef, PreparedArtifactRef, Declared pass-runner input and batching contract., Prepared image or packaged artifact ready for runner execution., One source item included in a runner execution batch., RunnerCapability, Frozen execution policy for one runner and hosting boundary., RunnerExecutionPolicy (+35 more)

### Community 27 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.18
Nodes (11): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Review Overlays, Diplomatic Text Review, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0014: Review Task and Overlay Schema (+3 more)

### Community 28 - "test_bundle_layout.py"
Cohesion: 0.17
Nodes (24): DocumentBundleManifest, page_dir_name(), PageBundleManifest, Return the stable page directory name for one 1-based page number. Args:…, On-disk document manifest for one Spec 0002 bundle., On-disk page manifest for one Spec 0002 page bundle., AcquisitionProvenance, BibliographicProvenance (+16 more)

### Community 29 - "services/bundle_layout.py"
Cohesion: 0.11
Nodes (27): DocumentBundle, Canonical software-facing document export., _atomic_write_json(), _atomic_write_text(), _collect_page_flags(), _executed_passes(), Path, Derive unique runner references for witnesses emitted on one page. Args: page:… (+19 more)

### Community 30 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (43): bochord.models Package, LineJoinKind, LineJoinRecord, NoteMarkerNormalizedForm, model_validator, StrEnum, Unicode normalization form applied to diplomatic text., How inline note markers appear in normalized text. (+35 more)

### Community 31 - "Detailed OCR Process"
Cohesion: 0.23
Nodes (17): Detailed OCR Process, Kraken Runner, OCR Produces Evidence, Philological Watchlists, Stage 4 Align Evidence, Stage 7 Apply Overlays, Stage 3 Competing OCR Passes, Stage 6 Evaluate Against Gold (+9 more)

### Community 32 - "BundleLayoutService"
Cohesion: 0.06
Nodes (46): OverlayState, Current overlay state for one reviewable object., BundleLayoutService, Any, Write and read Spec 0002 document bundle trees., Read the document-level manifest from one bundle root. Args: root: Filesystem…, Read one page manifest from a bundle root. Args: root: Filesystem root for one…, Read one normalized page graph artifact. Args: root: Filesystem root for one… (+38 more)

### Community 33 - "Architecture Index"
Cohesion: 0.17
Nodes (16): bochord Context, bochord, Image-First OCR Orchestration, Preparation Recipe, Witness Production, API Models Autodoc, ADR 0001 Package Boundary, OCR Evidence Not Philological Semantics (+8 more)

### Community 34 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 35 - "Settings"
Cohesion: 0.20
Nodes (10): Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Settings, patch, Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIRun (+2 more)

### Community 36 - "GoldPageAnnotation"
Cohesion: 0.24
Nodes (9): GoldPageAnnotation, Gold data slice for one page., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold…, Aggregate note-linkage success for covered gold edges. Args: prediction:…, Map predicted note ids to gold region annotation ids that name them. Args:…, Expand predicted notes into marker→note edges under gold aliases. Emits…, Return whether a gold note edge is in exhaustive NOTE_LINKAGE coverage. Args:… (+1 more)

### Community 37 - "_parse_native_corrected"
Cohesion: 0.21
Nodes (12): _line_unicode(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids., Import must fail when native export no longer matches the canonical package. (+4 more)

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
Cohesion: 0.26
Nodes (12): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+4 more)

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

### Community 46 - "BundlePage"
Cohesion: 0.11
Nodes (21): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., BundlePage, GoldTextSpan, Canonical exported page object., Gold diplomatic and normalized text target., _box_iou() (+13 more)

### Community 47 - "BundlePaths"
Cohesion: 0.08
Nodes (23): BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page… (+15 more)

### Community 48 - "Python Coding Standards"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 49 - "Hugging Face Setup Runbook"
Cohesion: 0.31
Nodes (11): Client-Side Queue for Cold Starts, Custom OCR Container, Hugging Face Setup Runbook, Hugging Face Inference Endpoints, Immutable Model Commit Pinning, Local Laptop Boundary, RunnerReference Provenance, olmOCR Runner (+3 more)

### Community 50 - "Spec 0005: Human Markup and Review"
Cohesion: 0.25
Nodes (8): V1 Typography and Role Vocabulary, Spec 0005: Human Markup and Review, Evidence-Bound Human Review, Independent Review Dimensions, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence, Reject eScriptorium as Review Boundary, PAGE Region/Line Reuse Boundary

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

### Community 55 - "PagePreparationOverride"
Cohesion: 0.17
Nodes (21): PagePreparationOverride, Operator override for one acquired source page., _index_page_overrides(), _normalize_page_overrides(), Index page overrides and reject duplicate or inconsistent ids. Args:…, Index page overrides by ``source_page_id``. Args: overrides: Validated page…, MockerFixture, test_page_override_requires_choice_and_reason() (+13 more)

### Community 56 - "OE Grammar Resources"
Cohesion: 0.18
Nodes (11): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+3 more)

### Community 57 - "prepare_pages"
Cohesion: 0.14
Nodes (20): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), prepare_pages(), Path, Print the some version info of this package, (+12 more)

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

### Community 65 - "_pixel_access"
Cohesion: 0.15
Nodes (15): _longest_dark_run(), _pixel_access(), Any, Return Pillow pixel access for ``image``. Args: image: Image whose pixels will…, Mark rows that contain enough ink to count as text. Args: gray: Grayscale…, Collect lengths of contiguous ``True`` runs. Args: mask: Boolean sequence.…, Return the longest contiguous run of values below ``threshold``. Args: values:…, Mark rows whose longest dark run spans enough of the page width. Args: gray:… (+7 more)

### Community 66 - "Page Graph"
Cohesion: 0.43
Nodes (7): Page Graph, Shared Page Coordinates, ADR 0003 Page Graph, Page Graph Line, Page Graph Note, Page Graph Region, Page Graph Span

### Community 67 - "PagePreparationService"
Cohesion: 0.38
Nodes (7): PagePreparationService, Stage 1 Acquire Source, Stage 2 PDF-to-Image Preparation, When To Rerun vs Rebuild, Phase 3 Acquisition Preparation Plan, Pillow and pypdfium2 Stack, SourceAcquisitionService

### Community 68 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 69 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.22
Nodes (9): Spec 0003: V1 Evaluation Schema, Evaluation Review Flags, Evaluation Score Families, Trust States machine/reviewed/corrected, Historical Character Preservation, Spec 0009: Merge and Alignment, Abstaining Merge Policy, Machine/Merge/Trust Confidence Triad (+1 more)

### Community 70 - "execution_batch_payload"
Cohesion: 0.29
Nodes (8): capability_payload(), execution_batch_payload(), model_runner_payload(), Return a valid model-backed runner payload with optional overrides., Return a valid runner capability payload with optional overrides., Return a valid runner execution batch payload with optional overrides., test_model_backed_runner_requires_hardware_class(), test_spec_0013_runner_invariants_reject_invalid_payloads()

### Community 71 - "ADR 0004 Layered Truth"
Cohesion: 0.33
Nodes (6): Raw Witness Artifact, ADR 0004 Layered Truth, Derived Graph Layer, Export Layer, Rebuild Derived Outputs From Raw Artifacts, Raw Witness Layer

### Community 72 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 73 - "Comparative method of reconstruction"
Cohesion: 0.40
Nodes (5): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), Proto-Germanic Introduction: Linguistic Methods

### Community 74 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 75 - "RunnerReference"
Cohesion: 0.18
Nodes (8): Identity for one runner implementation and model revision., RunnerReference, Bind one hosted olmOCR runner to endpoint settings and an HTTP client. Args:…, Return the runner identity used for hosted requests. Returns: Model-backed…, Client, Persisted batch status must agree with submitted and failed items., test_runner_reference_accepts_immutable_digest_revision(), test_runner_reference_rejects_mutable_model_revision()

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

### Community 104 - "_border_shadow_signal"
Cohesion: 0.24
Nodes (10): _border_shadow_signal(), _gutter_shadow_signal(), _margin_strip_width(), Warn when ``value`` exceeds ``maximum``. Args: value: Measured value. maximum:…, Measure mean darkness ratio inside ``box``. Args: gray: Grayscale working…, Width of the 8% border/gutter strip in pixels. Args: width: Page width in…, Measure darkness of the center 8% vertical strip. Args: gray: Grayscale working…, Measure darkness of the left/right 8% vertical strips. Args: gray: Grayscale… (+2 more)

### Community 105 - "_detect_structure_conflict"
Cohesion: 0.25
Nodes (8): _detect_structure_conflict(), _geometry_alternates_for_regions(), Serialize losing witness regions as geometry alternate candidates. Args:…, Decide whether witness regions disagree with the chosen scaffold. Args:…, Sort regions by reading order index. Args: regions: Region nodes from one…, Decide whether region box presence disagrees between two witnesses. Args:…, _region_box_presence_mismatch(), _regions_by_reading_order()

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
Cohesion: 0.11
Nodes (35): PackagingStrategy, Runner packaging policies., PlannedRunnerBatch, One planned invocation batch before packaging and submission., Bind batch planning, packaging, and hosted runner collaborators. Args: planner:…, _load_rgb_images(), _page_numbers(), Image (+27 more)

### Community 111 - "TestCLIVersion"
Cohesion: 0.25
Nodes (5): Test the version command., Test the version command displays version information., Test the version command with verbose flag., Test the version command with quiet flag., TestCLIVersion

### Community 112 - "Image"
Cohesion: 0.15
Nodes (17): _column_count_signal(), _column_ink_profile(), _column_unit_boxes(), _column_valley_centers(), _fixed_tile_boxes(), _prepared_coordinate_space(), Image, Build the canonical coordinate space for the prepared page image. Args:… (+9 more)

### Community 113 - "_measure_skew_degrees"
Cohesion: 0.33
Nodes (6): _downsample_for_heuristics(), _measure_skew_degrees(), Estimate page skew degrees via row-projection variance. Args: gray: Grayscale…, Downsample so the longest edge is at most ``_HEURISTIC_MAX_EDGE_PX``. Args:…, Compute variance of per-row ink sums. Args: gray: Grayscale page image.…, _row_projection_variance()

### Community 114 - ".settings_customise_sources"
Cohesion: 0.22
Nodes (6): BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, PydanticBaseSettingsSource, Test loading configuration with TOML file.

### Community 115 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 116 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 117 - "_prepared_unit_from_box"
Cohesion: 0.33
Nodes (6): _prepared_unit_from_box(), Format a SHA-256 digest label for ``payload``. Args: payload: Bytes to hash.…, Persist ``image`` as PNG with fixed options and return its checksum. Side…, Crop, save, and describe one prepared unit. Side Effects: Writes one unit PNG…, _save_prepared_png(), _sha256_label()

### Community 118 - "TestConsole"
Cohesion: 0.50
Nodes (3): Test console objects., Test that console objects are properly initialized., TestConsole

### Community 119 - "TestCLIErrorHandling"
Cohesion: 0.33
Nodes (4): Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., TestCLIErrorHandling

### Community 120 - ".prepare"
Cohesion: 0.10
Nodes (23): _build_prepared_units(), _derive_prepared_page_id(), _ensure_supported_recipe(), _persist_prepared_page(), _persist_recipe(), PreparationBundleService, Path, Derive a stable prepared-page id from checksum, recipe, and mode. Args:… (+15 more)

### Community 121 - "_build_preparation_result"
Cohesion: 0.50
Nodes (4): _build_assessment(), _build_preparation_result(), Build assessment metadata for one prepared page. Keyword Args: source_page:…, Assemble the persisted result model for one prepared page. Args: source_page:…

### Community 122 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 123 - "test_prepared_unit_rejects_missing_or_empty_lineage_fields"
Cohesion: 0.50
Nodes (3): parametrize, Boxes must represent a positive-area rectangle., test_prepared_unit_rejects_missing_or_empty_lineage_fields()

### Community 125 - "recipe_payload"
Cohesion: 0.67
Nodes (3): Return a valid preparation-recipe payload with optional overrides., recipe_payload(), test_recipe_rejects_overlap_not_smaller_than_tile()

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
- **Why does `BundlePage` connect `BundlePage` to `models/__init__.py`, `BundleLayoutService`, `MergeOrchestrator`, `GoldPageAnnotation`, `test_evaluation_service.py`, `cli.py`, `._write_page_xml`, `model_validator`, `test_merge_service.py`, `PageXmlInterchangeService`, `test_page_interchange.py`, `services/merge.py`, `services/evaluation.py`, `_RateAccumulator`, `services/bundle_layout.py`, `test_text_normalization.py`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `test_evaluation_service.py`, `test_runner_execution.py`, `PageClass`, `HuggingFaceOlmocrRunner`, `cli.py`, `QualitySignal`, `test_merge_service.py`, `services/merge.py`, `_RateAccumulator`, `PreparationRecipe`, `services/preparation.py`, `PreparedArtifactRef`, `test_bundle_layout.py`, `services/bundle_layout.py`, `test_text_normalization.py`, `BundleLayoutService`, `GoldPageAnnotation`, `BundlePage`, `BundlePaths`, `PagePreparationOverride`, `RunnerReference`, `PlannedRunnerBatch`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `AlternateCandidate` connect `models/__init__.py` to `MergeOrchestrator`, `test_evaluation_service.py`, `PageClass`, `HuggingFaceOlmocrRunner`, `cli.py`, `QualitySignal`, `services/merge.py`, `services/evaluation.py`, `_RateAccumulator`, `services/preparation.py`, `PreparedArtifactRef`, `test_bundle_layout.py`, `services/bundle_layout.py`, `BundleLayoutService`, `GoldPageAnnotation`, `BundlePage`, `RunnerReference`, `_detect_structure_conflict`, `PlannedRunnerBatch`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._