# Graph Report - bochord  (2026-08-03)

## Corpus Check
- 123 files · ~174,979 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2774 nodes · 7254 edges · 135 communities (109 shown, 26 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 559 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `98f14236`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- services/evaluation.py
- AlternateCandidate
- services/preparation.py
- PlannedRunnerBatch
- test_bundle_layout.py
- BundlePage
- MetricProfile
- BundleLayoutService
- test_evaluation_service.py
- Detailed OCR Process
- PreparedArtifactRef
- test_text_normalization.py
- ocr.py
- models/__init__.py
- test_preparation_service.py
- Path
- HuggingFaceOlmocrRunner
- ADR 0010 Structured Output Boundary
- _review_base
- _SpanCandidate
- check_napoleon_gate.py
- BundlePaths
- test_olmocr_runner.py
- BT Witness Preparation Slice
- Settings
- SchemaModel
- ReviewOverlayService
- PreparationRecipe
- _NoteCandidate
- MergeOrchestrator
- .score
- test_page_interchange.py
- test_ocr_models.py
- test_document_export.py
- test_runner_execution.py
- model_validator
- _try_rebind_event
- Point
- GoldPageAnnotation
- PageXmlInterchangeService
- _bundle_page_payload
- _RateAccumulator
- BoundingBox
- cli
- cli.py
- test_cli_commands.py
- _persist_prepared_page
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- _rag_chunk
- ReviewDimension
- TestCLISettings
- TestPrintInfo
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- test_cli_utils.py
- .__init__
- Preparation Gold Specs
- Raw OCR witness layer
- CLI Progress Utils
- Spec 0002: V1 Bundle Layout and Data Shape
- Spec 0005: Human Markup and Review
- Coding Standards Docs
- TestCLIGlobalOptions
- model_validator
- ADR 0009 OCR-D PAGE eScriptorium
- Spec 0006: Exports and Retrieval Views
- ReviewSummary
- Typography
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
- .create_successor
- TestConsoleQuietMode
- _review_polygon
- valid_bundle_page
- model_runner_payload
- Sphinx Docs Index
- Lesson 0003 Pronouncing Old English Letters
- Spec 0009: Merge and Alignment
- .validate_https_huggingface_endpoints
- Page Graph Line
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- test_write_document_exports_writes_derived_views
- ._write_page_xml
- TestCLIEval
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
- _expected_evidence
- NoteKind
- .test_page_overlay_rejects_task_with_mismatched_prepared_image_checksum
- _PreparedInputsManifest
- _evidence_with_witness
- .__init__
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

## Communities (135 total, 26 thin omitted)

### Community 0 - "services/evaluation.py"
Cohesion: 0.12
Nodes (19): BaselineShift, FontSlant, FontWeight, Visual font-weight classification independent of other typography., Visual font-slant classification independent of weight and role., Vertical placement of a span relative to the local baseline., _boxes_intersect(), _coverage_allows() (+11 more)

### Community 1 - "AlternateCandidate"
Cohesion: 0.05
Nodes (89): AlternateCandidate, MergeFlag, MergeFlagType, MergePageResult, PassWitnessPage, StrEnum, One material merge disagreement surfaced for human review., Accepted page graph plus merge flags and abstention state. (+81 more)

### Community 2 - "services/preparation.py"
Cohesion: 0.06
Nodes (84): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _adaptive_binary() (+76 more)

### Community 3 - "PlannedRunnerBatch"
Cohesion: 0.12
Nodes (36): PackagingStrategy, Runner packaging policies., PackagedRunnerInput, PlannedRunnerBatch, One planned invocation batch before packaging and submission., Packaged artifact ready for hosted runner submission., _load_rgb_images(), _page_numbers() (+28 more)

### Community 4 - "test_bundle_layout.py"
Cohesion: 0.07
Nodes (51): DocumentBundleManifest, page_dir_name(), PageBundleManifest, Return the stable page directory name for one 1-based page number. Args:…, On-disk document manifest for one Spec 0002 bundle., On-disk page manifest for one Spec 0002 page bundle., AcquisitionProvenance, BibliographicProvenance (+43 more)

### Community 5 - "BundlePage"
Cohesion: 0.08
Nodes (48): BundlePage, Canonical exported page object., Self-contained instructions and evidence binding for human review., Supported human review targets., Verb vocabulary for append-only review events., Typography and note-linkage scores grouped under the style family., ReviewAction, ReviewScope (+40 more)

### Community 6 - "MetricProfile"
Cohesion: 0.10
Nodes (20): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., GoldTextSpan, Gold diplomatic and normalized text target., _edit_distance(), _graphemes(), _is_macron_grapheme() (+12 more)

### Community 7 - "BundleLayoutService"
Cohesion: 0.06
Nodes (65): OverlayState, Current overlay state for one reviewable object., BundleLayoutService, Write and read Spec 0002 document bundle trees., _accept_review_event(), load_minimal_bundle(), Path, page_exports basenames must not escape the page exports directory. (+57 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.13
Nodes (46): GoldCoverage, GoldLineJoin, Gold line-join annotation for hyphenation and continuation decisions., Explicit evaluation denominator and exclusion scope for a gold slice., EvaluationService, Score one predicted page against a gold annotation slice. Orchestrates text,…, _box(), note_link_gold() (+38 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "PreparedArtifactRef"
Cohesion: 0.05
Nodes (58): BatchItemRef, BatchResultStatus, GoldDocument, InputKind, PreparedArtifactRef, Runner input artifact categories., Execution outcome for one runner batch., Document-level gold annotation file. (+50 more)

### Community 11 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (44): LineJoinKind, LineJoinRecord, NoteMarkerNormalizedForm, model_validator, StrEnum, Unicode normalization form applied to diplomatic text., How inline note markers appear in normalized text., How superscript characters appear in normalized text. (+36 more)

### Community 12 - "ocr.py"
Cohesion: 0.09
Nodes (50): AcceptReviewEvent, CorrectGeometryReviewEvent, CorrectStyleReviewEvent, CorrectTextReviewEvent, DecidePreparationReviewEvent, DecideSourceTriageReviewEvent, FlagReviewEvent, LinkNoteReviewEvent (+42 more)

### Community 13 - "models/__init__.py"
Cohesion: 0.07
Nodes (64): CoordinateSpace, DatasetSplit, FlagSeverity, PageClass, PreparationDecision, PreparationMode, PreparedPage, StrEnum (+56 more)

### Community 14 - "test_preparation_service.py"
Cohesion: 0.06
Nodes (87): PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, Bind acquisition and per-page preparation collaborators. Args:… (+79 more)

### Community 15 - "Path"
Cohesion: 0.08
Nodes (21): _atomic_write_json(), _atomic_write_text(), _needs_trailing_newline(), Any, Path, ReviewEvent, Materialize the on-disk tree (recomputable layers only). Side Effects: Creates…, Write derived document export artifacts under ``exports/``. Side Effects:… (+13 more)

### Community 16 - "HuggingFaceOlmocrRunner"
Cohesion: 0.06
Nodes (47): BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all bochord errors., RunnerEndpointUnavailable (+39 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "_review_base"
Cohesion: 0.11
Nodes (14): _minimal_page_overlay(), Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events., Review-event schema should discriminate on ``action``., Source-triage events carry an explicit disposition and optional reason., Preparation events carry full-page or subdivide plus optional reason. (+6 more)

### Community 19 - "_SpanCandidate"
Cohesion: 0.07
Nodes (43): Semantic role kept separate from visual typography., TextRole, _apply_span_text_resolution(), _apply_span_typography_resolution(), _first_candidate_by_runner_precedence(), Any, Collect unique witness ids from span candidates in input order. Args:…, Collect unique runner ids from span candidates in input order. Args:… (+35 more)

### Community 20 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 21 - "BundlePaths"
Cohesion: 0.08
Nodes (23): BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page… (+15 more)

### Community 22 - "test_olmocr_runner.py"
Cohesion: 0.13
Nodes (40): hosted_runner(), mock_client(), MockHttpxClient, olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint() (+32 more)

### Community 23 - "BT Witness Preparation Slice"
Cohesion: 0.05
Nodes (42): ExtractionOrchestrator, Project Structure (models/services/cli/settings), Single Responsibility Service Architecture, Dual Text Contract, Historical Character Preservation, LineJoinRecord, text-norm-v1 Policy, TextNormalizer (+34 more)

### Community 24 - "Settings"
Cohesion: 0.06
Nodes (30): BaseSettings, Path, Load settings from file with cascading configuration. Args: config_file:…, Get list of configuration file paths that were loaded. Use this for debugging.…, Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Settings, Exception (+22 more)

### Community 25 - "SchemaModel"
Cohesion: 0.10
Nodes (47): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+39 more)

### Community 26 - "ReviewOverlayService"
Cohesion: 0.13
Nodes (17): Lifecycle state for a human review task., ReviewTaskStatus, Replay append-only review events and build explicit successor overlays., ReviewOverlayService, MonkeyPatch, Replay of frozen fixture events must equal fixture current_state., Successor copies resolvable events only and keeps conflict packets., Successor remaps nested region and line ids on a copied split event. (+9 more)

### Community 27 - "PreparationRecipe"
Cohesion: 0.08
Nodes (38): PreparationRecipe, Deterministic page-preparation profile., _derive_prepared_page_id(), _ensure_supported_recipe(), Derive a stable prepared-page id from checksum, recipe, and mode. Args:…, Reject recipe modes that are intentionally unsupported today. Args: recipe:…, _artifact_from_raster(), _image_dpi() (+30 more)

### Community 28 - "_NoteCandidate"
Cohesion: 0.10
Nodes (34): _apply_note_link_resolution(), _mapped_note_link_sets(), _MarkerMappingContext, _min_merge_confidence(), _note_link_alternates(), _note_marker_links_from_mapped_sets(), _note_marker_links_when_mapping_ambiguous(), _note_text_alternates_from_candidates() (+26 more)

### Community 29 - "MergeOrchestrator"
Cohesion: 0.06
Nodes (31): _coordinate_rich_line_count(), _first_witness_by_runner_preference(), _flagged_object_ids(), MergeOrchestrator, Return a span flagged for missing witness text evidence. Args: span: Accepted…, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Initialize merge orchestration for one page. Args: policy: Versioned merge…, Collect object ids already referenced by merge flags. Args: flags: Merge flags… (+23 more)

### Community 30 - ".score"
Cohesion: 0.13
Nodes (15): AnchoredGoldAnnotation, GoldRegionAnnotation, Gold annotation that resolves to graph evidence or prepared image geometry., Gold region or structure target., _box_iou(), Return intersection-over-union for two axis-aligned boxes. Args: left: First…, Resolve a gold region by id or same-kind highest IoU. Args: gold_region: Gold…, Score structure metrics and provenance-backed structure flags. Covers region… (+7 more)

### Community 31 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 32 - "test_ocr_models.py"
Cohesion: 0.08
Nodes (22): Return a valid preparation-recipe payload with optional overrides., Frozen document-bundle-v1.json must validate and dump identically., Frozen rag-document-v1.json must validate and dump identically., DocumentBundle JSON Schema must match the checked-in generated snapshot., RagDocument JSON Schema must match the checked-in generated snapshot., Frozen page-overlay-v1.json must validate and dump identically., recipe_payload(), test_endpoint_policy_rejects_estimate_above_run_cap() (+14 more)

### Community 33 - "test_document_export.py"
Cohesion: 0.04
Nodes (75): ChunkType, DocumentBundle, RagDocument, Canonical software-facing document export., Document-level retrieval export., Human-review trust level for accepted graph content., Retrieval chunk families., Accepted region classes for the page graph. (+67 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.14
Nodes (36): HostedInvocationResult, Raw result returned from one hosted runner invocation., Thin facade that delegates one run to ``RunnerExecutionOrchestrator``. Args:…, RunnerExecutionService, InvokeResult, execution_service(), _fail_all_items(), _fail_second_item() (+28 more)

### Community 35 - "model_validator"
Cohesion: 0.05
Nodes (25): _known_page_space_ids(), _known_preparation_space_ids(), model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Require provenance pointers to stay local to the owning page. Args: provenance:… (+17 more)

### Community 36 - "_try_rebind_event"
Cohesion: 0.12
Nodes (18): _coordinate_space_ids(), _nested_object_ids(), ReviewEvent, Apply one append-only event onto a mutable overlay state. Args: state:…, Record trust, applied event id, and reviewed/corrected dimensions. Args: state:…, Apply event-specific override fields named by the event contract. Structural…, Rebind one event when every required id resolves; otherwise skip it. Args:…, Collect nested marker/region/line/note ids that must remap. Args: event:… (+10 more)

### Community 37 - "Point"
Cohesion: 0.18
Nodes (8): Point, One point in an identified image coordinate space., Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 38 - "GoldPageAnnotation"
Cohesion: 0.20
Nodes (11): GoldNoteLink, GoldPageAnnotation, Gold note-marker linkage target., Gold data slice for one page., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold…, Aggregate note-linkage success for covered gold edges. Args: prediction:…, Map predicted note ids to gold region annotation ids that name them. Args:… (+3 more)

### Community 39 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 40 - "_bundle_page_payload"
Cohesion: 0.12
Nodes (16): _bundle_page_payload(), Return a mutable dump of a valid bundle page with optional overrides., Graph boxes and polygons must name a known page coordinate space., Non-empty baselines require an explicit baseline coordinate space id., Baseline coordinate spaces must resolve to a known page space., Every span listed by a line must claim that line as parent., Line order values must be positive and unique within a parent region., Provenance source/witness/runner ids must belong to the owning page. (+8 more)

### Community 41 - "_RateAccumulator"
Cohesion: 0.11
Nodes (19): EvaluationFlag, GoldStyleSpan, Gold style target for one span or image-anchored area., One review-driving evaluation flag., _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:…, Score footnote-marker retention when gold carries that role. Args: gold_span:… (+11 more)

### Community 42 - "BoundingBox"
Cohesion: 0.08
Nodes (42): BoundingBox, _geometry_space_id(), Polygon, Return the named coordinate space for optional box or polygon geometry. Args:…, Require graph geometry to name one known page coordinate space. Args: box:…, Reject mixed coordinate-space identity when both geometry forms are present.…, Axis-aligned rectangle for page-relative geometry., Polygon geometry for non-rectangular regions and curved text lines. (+34 more)

### Community 43 - "cli"
Cohesion: 0.18
Nodes (10): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test the prepare command., Test prepare aborts before writes when override lacks a reason. (+2 more)

### Community 44 - "cli.py"
Cohesion: 0.12
Nodes (28): argument, eval_cohorts(), eval_page(), _load_page_overrides(), _load_preparation_recipe(), _prepare_overrides(), prepare_pages(), Path (+20 more)

### Community 45 - "test_cli_commands.py"
Cohesion: 0.38
Nodes (5): patch, Test the run command., _run_cli_args(), _runner_reference_json(), TestCLIRun

### Community 46 - "_persist_prepared_page"
Cohesion: 0.06
Nodes (38): _build_prepared_units(), _column_unit_boxes(), _column_valley_centers(), _fixed_tile_boxes(), _index_page_overrides(), _normalize_page_overrides(), _persist_prepared_page(), _persist_recipe() (+30 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.09
Nodes (12): Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Contract checks for persisted OCR schema models., Region revisions must include at least one geometry form., Flag events record concern without changing trust state., A review task should be actionable without undocumented context., Review tasks must bind to the prepared image the operator inspects. (+4 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.18
Nodes (13): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy, Hugging Face Deployment Target (+5 more)

### Community 50 - "_rag_chunk"
Cohesion: 0.07
Nodes (42): RagChunk, Multi-page provenance retained by retrieval exports., Page-local retrieval chunk., Cross-page retrieval chunk stitched from accepted page-local chunks., RetrievalProvenance, StitchedChunk, Build cross-page stitched chunks from contiguous BODY region runs. Args:…, Emit one stitched chunk when a BODY run spans multiple pages. Args:… (+34 more)

### Community 51 - "ReviewDimension"
Cohesion: 0.13
Nodes (13): Independent evidence dimensions a human may inspect and certify., Operator workflow represented by a review task packet., ReviewDimension, ReviewTaskType, Build a deterministic task id from page, type, and target ids. Identity is…, Append novel review dimensions while preserving first-seen order. Args:…, _union_dimensions(), HumanMarkupService task types must certify only their exclusive dimension. (+5 more)

### Community 52 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., Settings output must not expose the raw Hugging Face token., TestCLISettings

### Community 53 - "TestPrintInfo"
Cohesion: 0.33
Nodes (4): Test info printing functions., Test basic info printing., Test info panel has correct styling., TestPrintInfo

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

### Community 58 - "test_cli_utils.py"
Cohesion: 0.11
Nodes (17): print_error(), print_info(), print_success(), Print error message with optional suggestions. Args: message: Error message…, Print success message. Args: message: Success message, Print informational message. Args: message: Informational message, Tests for CLI utilities., Test success panel has correct styling. (+9 more)

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
Cohesion: 0.25
Nodes (8): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, V1 Typography and Role Vocabulary, Evidence-Bound Human Review, Spike 0001: PAGE / eScriptorium Interoperability, bochord.json Sidecar Evidence, Reject eScriptorium as Review Boundary, PAGE Region/Line Reuse Boundary

### Community 64 - "Spec 0005: Human Markup and Review"
Cohesion: 0.18
Nodes (11): Review Overlays, Spec 0005: Human Markup and Review, Diplomatic Text Review, Independent Review Dimensions, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Retrieval Convenience Text Fields, Spec 0014: Review Task and Overlay Schema (+3 more)

### Community 65 - "Coding Standards Docs"
Cohesion: 0.27
Nodes (11): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings, Fork-Clone-PR Contribution Workflow, Contributing Guide (+3 more)

### Community 66 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 67 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 68 - "ADR 0009 OCR-D PAGE eScriptorium"
Cohesion: 0.22
Nodes (9): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate, ADR 0009 OCR-D PAGE eScriptorium, eScriptorium, OCR-D Workflows and PAGE (+1 more)

### Community 69 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.25
Nodes (9): Spec 0006: Exports and Retrieval Views, Bundle JSON Export, Markdown Export, RAG JSON Export, Document-Level Stitched Chunks, Downstream Transformation Packages, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle Pydantic Model (+1 more)

### Community 70 - "ReviewSummary"
Cohesion: 0.20
Nodes (12): Compact review state attached to accepted graph objects., ReviewSummary, _provenance(), Return valid single-page object provenance., Every line listed by a region must claim that region as parent., Every note listed by a region must claim that region as parent., Region reading_order_index values must be positive and unique., Existing provenance fixtures stay valid without alternate candidates. (+4 more)

### Community 71 - "Typography"
Cohesion: 0.27
Nodes (9): Orthogonal visual typography facets for one text span., Typography, Report whether typography carries at least one known facet. Args: typography:…, bold_but_not_italic_prediction(), bold_italic_gold(), One span that is bold but upright (not italic)., Gold style requiring both bold and italic facets., test_style_facets_are_independent() (+1 more)

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
Cohesion: 0.07
Nodes (114): MergePageInput, MergePolicy, Versioned deterministic merge precedence and acceptance thresholds., Competing witness fragments prepared for single-page merge., AbstainingMergeService, Stateless facade: merge one page of competing witnesses. Args: text_normalizer:…, _aligned_text_witnesses(), _bounding_box() (+106 more)

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

### Community 84 - ".create_successor"
Cohesion: 0.20
Nodes (8): _normalize_tasks(), Normalize a successor task map or list into a task-id dictionary. Args:…, Reject task maps that point at missing successor tasks. Args: task_id_map:…, Derive successor run, graph, and checksum from caller-supplied tasks. Args:…, Replay ``overlay.review_events`` into per-object overlay state. Ignores any…, Build a rebased successor overlay without mutating the predecessor. Copies only…, _require_mapped_tasks(), _successor_bindings()

### Community 85 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 86 - "_review_polygon"
Cohesion: 0.29
Nodes (6): Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces., _review_box(), _review_polygon()

### Community 87 - "valid_bundle_page"
Cohesion: 0.22
Nodes (9): _page_witness(), Return a witness owned by the given page., Document page ids must stay unique., Source page_count must remain exact versus exported pages., Return a minimal valid page graph for join-reference tests., test_bundle_rejects_unknown_line_join_target(), test_document_bundle_rejects_duplicate_page_ids(), test_document_bundle_rejects_inexact_source_page_count() (+1 more)

### Community 88 - "model_runner_payload"
Cohesion: 0.25
Nodes (8): capability_payload(), execution_batch_payload(), model_runner_payload(), Return a valid model-backed runner payload with optional overrides., Return a valid runner capability payload with optional overrides., Return a valid runner execution batch payload with optional overrides., test_model_backed_runner_requires_hardware_class(), test_runner_reference_rejects_mutable_model_revision()

### Community 89 - "Sphinx Docs Index"
Cohesion: 0.50
Nodes (5): API Models Autodoc, Changelog, Sphinx Docs Index, README, Read the Docs Config

### Community 90 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 91 - "Spec 0009: Merge and Alignment"
Cohesion: 0.40
Nodes (5): Trust States machine/reviewed/corrected, Spec 0009: Merge and Alignment, Abstaining Merge Policy, Machine/Merge/Trust Confidence Triad, Structure Scaffold Selection

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

### Community 98 - "test_write_document_exports_writes_derived_views"
Cohesion: 0.50
Nodes (4): load_export_minimal_bundle(), Persisted document exports match renderer output and preserve overlays., Load the compact export-fixture DocumentBundle., test_write_document_exports_writes_derived_views()

### Community 99 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 100 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 101 - "ADR 0008 Stable IDs and Review History"
Cohesion: 0.67
Nodes (3): ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States

### Community 102 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 133 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``bochord run``.

## Ambiguous Edges - Review These
- `README` → `Sphinx Docs Index`  [AMBIGUOUS]
  README.md · relation: semantically_similar_to
- `Frequently Asked Questions` → `Quickstart CLI Entry Points`  [AMBIGUOUS]
  doc/source/overview/faq.rst · relation: conceptually_related_to
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to

## Knowledge Gaps
- **121 isolated node(s):** `release.sh script`, `bochord`, `IPA_AUDIO`, `Update Requirements Workflow`, `Post-Implementation Quality Gate` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `README` and `Sphinx Docs Index`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Frequently Asked Questions` and `Quickstart CLI Entry Points`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `i-mutation / i-umlaut` and `Ablaut (inherited vowel alternation)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `BundlePage` connect `BundlePage` to `services/evaluation.py`, `AlternateCandidate`, `test_bundle_layout.py`, `MetricProfile`, `test_evaluation_service.py`, `test_text_normalization.py`, `ocr.py`, `models/__init__.py`, `Path`, `SchemaModel`, `MergeOrchestrator`, `.score`, `test_page_interchange.py`, `test_ocr_models.py`, `test_document_export.py`, `model_validator`, `GoldPageAnnotation`, `PageXmlInterchangeService`, `_RateAccumulator`, `cli.py`, `_rag_chunk`, `Typography`, `test_merge_service.py`, `valid_bundle_page`, `._write_page_xml`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `AlternateCandidate` connect `AlternateCandidate` to `services/evaluation.py`, `NoteKind`, `services/preparation.py`, `PlannedRunnerBatch`, `test_bundle_layout.py`, `BundlePage`, `MetricProfile`, `BundleLayoutService`, `test_evaluation_service.py`, `PreparedArtifactRef`, `ocr.py`, `models/__init__.py`, `HuggingFaceOlmocrRunner`, `_SpanCandidate`, `SchemaModel`, `ReviewOverlayService`, `_NoteCandidate`, `.score`, `test_ocr_models.py`, `test_document_export.py`, `Point`, `GoldPageAnnotation`, `_RateAccumulator`, `BoundingBox`, `_rag_chunk`, `ReviewDimension`, `ReviewSummary`, `Typography`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `SchemaModel` to `AlternateCandidate`, `services/preparation.py`, `PlannedRunnerBatch`, `test_bundle_layout.py`, `BundlePage`, `MetricProfile`, `BundleLayoutService`, `test_evaluation_service.py`, `PreparedArtifactRef`, `test_text_normalization.py`, `ocr.py`, `models/__init__.py`, `BundlePaths`, `PreparationRecipe`, `.score`, `test_document_export.py`, `test_runner_execution.py`, `Point`, `GoldPageAnnotation`, `_RateAccumulator`, `BoundingBox`, `_rag_chunk`, `ReviewSummary`, `Typography`, `test_merge_service.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 94 inferred relationships involving `AlternateCandidate` (e.g. with `BundlePage` and `CoordinateSpace`) actually correct?**
  _`AlternateCandidate` has 94 INFERRED edges - model-reasoned connections that need verification._