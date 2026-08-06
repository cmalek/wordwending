# Graph Report - bochord  (2026-08-06)

## Corpus Check
- 125 files · ~179,444 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2834 nodes · 7349 edges · 145 communities (119 shown, 26 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 564 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `485d0274`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ._emit_result
- models/__init__.py
- test_text_normalization.py
- PlannedRunnerBatch
- test_bundle_layout.py
- BundlePage
- services/preparation.py
- BundleLayoutService
- test_evaluation_service.py
- Detailed OCR Process
- RunnerThroughputSummary
- TextNormalizer
- test_document_export.py
- cli.py
- test_preparation_service.py
- BundlePaths
- HuggingFaceOlmocrRunner
- ADR 0010 Structured Output Boundary
- services/evaluation.py
- _SpanCandidate
- check_napoleon_gate.py
- Path
- test_olmocr_runner.py
- BT Witness Preparation Slice
- TestConfiguration
- PageEvaluationSummary
- _try_rebind_event
- SourcePageArtifact
- _NoteCandidate
- MergeOrchestrator
- GoldPageAnnotation
- test_page_interchange.py
- _stable_json_schema
- DocumentExportService
- test_runner_execution.py
- model_validator
- test_review_overlay.py
- ._coords
- model_runner_payload
- PageXmlInterchangeService
- _bundle_page_payload
- _RateAccumulator
- RunnerExecutionPolicy
- cli
- run_runner
- Settings
- ._score_text_pair
- Machine Assistance Resources
- TestOcrModels
- Spec 0004: Ordered V1 Implementation
- _stitched_chunk
- _rag_chunk
- TestCLISettings
- test_cli_utils.py
- main
- DocumentRunOrchestrator
- i-mutation / i-umlaut
- conftest.py
- print_error
- .score
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
- README, Operator Docs, and Thin Export CLI Implementation Plan
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
- _review_polygon
- test_ocr_models.py
- _apply_span_text_resolution
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
- _apply_span_typography_resolution
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
- .create_successor
- DocumentBundle
- Typography
- _known_page_space_ids
- Point
- ReviewTaskType
- _validate_zip_member
- _page_witnesses
- TestCLIEval
- _PreparedInputsManifest
- .reject_historical_modernization
- ._provenance_flags
- _evidence_with_witness
- .__init__
- .__init__
- _expected_evidence

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

## Communities (145 total, 26 thin omitted)

### Community 0 - "._emit_result"
Cohesion: 0.50
Nodes (3): Build the accepted page graph result for this merge run. Returns: Merge result…, Project merge-input witnesses into page-local WitnessReference records. Args:…, _witness_references_for_page()

### Community 1 - "models/__init__.py"
Cohesion: 0.03
Nodes (158): AlternateCandidate, MergeFlag, MergeFlagType, MergePageResult, PassWitnessPage, StrEnum, One material merge disagreement surfaced for human review., Accepted page graph plus merge flags and abstention state. (+150 more)

### Community 2 - "test_text_normalization.py"
Cohesion: 0.14
Nodes (22): LineJoinKind, LineJoinRecord, NoteMarkerNormalizedForm, StrEnum, Unicode normalization form applied to diplomatic text., How inline note markers appear in normalized text., How superscript characters appear in normalized text., How adjacent lines were joined when building normalized text. (+14 more)

### Community 3 - "PlannedRunnerBatch"
Cohesion: 0.08
Nodes (56): BatchItemRef, InputKind, PackagingStrategy, PreparedArtifactRef, Runner input artifact categories., Runner packaging policies., Prepared image or packaged artifact ready for runner execution., One source item included in a runner execution batch. (+48 more)

### Community 4 - "test_bundle_layout.py"
Cohesion: 0.14
Nodes (25): DocumentBundleManifest, page_dir_name(), Return the stable page directory name for one 1-based page number. Args:…, On-disk document manifest for one Spec 0002 bundle., AcquisitionProvenance, BibliographicProvenance, Stable descriptive metadata for the source work., How the source files were obtained. (+17 more)

### Community 5 - "BundlePage"
Cohesion: 0.08
Nodes (52): BundlePage, EvaluationFamilySummary, EvaluationFlag, Canonical exported page object., Self-contained instructions and evidence binding for human review., Independent evidence dimensions a human may inspect and certify., Verb vocabulary for append-only review events., One review-driving evaluation flag. (+44 more)

### Community 6 - "services/preparation.py"
Cohesion: 0.05
Nodes (96): CoordinateTransform, FlagSeverity, Severity levels for review and evaluation flags., Replayable mapping between two recorded coordinate spaces., AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment. (+88 more)

### Community 7 - "BundleLayoutService"
Cohesion: 0.06
Nodes (62): BundleLayoutService, Write and read Spec 0002 document bundle trees., Serialize JSON objects as JSONL with a trailing newline when nonempty. Args:…, _accept_review_event(), load_minimal_bundle(), Path, source_files keys must be bare basenames, not path segments., page_exports basenames must not escape the page exports directory. (+54 more)

### Community 8 - "test_evaluation_service.py"
Cohesion: 0.11
Nodes (49): GoldCoverage, GoldLineJoin, GoldTextSpan, Gold diplomatic and normalized text target., Gold line-join annotation for hyphenation and continuation decisions., Explicit evaluation denominator and exclusion scope for a gold slice., EvaluationService, Score one predicted page against a gold annotation slice. Orchestrates text,… (+41 more)

### Community 9 - "Detailed OCR Process"
Cohesion: 0.06
Nodes (60): bochord eval CLI, Byte-Identical Evaluation Reproducibility, Gold Annotation Protocol, Gold Annotation Protocol, GoldCoverage, GoldDocument, MetricProfile, Note-Heavy Page page-0010 (+52 more)

### Community 10 - "RunnerThroughputSummary"
Cohesion: 0.07
Nodes (40): BochordError, ConfigurationError, FileError, Raised when settings or configuration fails., Raised when file I/O operations fail., Raised when a hosted runner endpoint is not ready for inference., Base exception for all bochord errors., RunnerEndpointUnavailable (+32 more)

### Community 11 - "TextNormalizer"
Cohesion: 0.08
Nodes (22): Return a span flagged for missing witness text evidence. Args: span: Accepted…, Initialize the merge facade. Args: text_normalizer: Optional normalizer;…, _span_with_insufficient_text_evidence(), Initialize interchange with optional text-normalization override. Args:…, Normalize span diplomatic text without note-marker rewriting. Args:…, Normalize note diplomatic text, including note-marker policy. Args:…, Join two line texts and return normalized output plus provenance. Hyphen-at-…, Return a span copy with ``text_normalized`` regenerated. Args: span: Accepted… (+14 more)

### Community 12 - "test_document_export.py"
Cohesion: 0.08
Nodes (41): BaselineShift, ChunkType, FontSlant, FontWeight, NoteKind, StrEnum, Accepted note classes for v1., Preparation transform families recorded between image spaces. (+33 more)

### Community 13 - "cli.py"
Cohesion: 0.05
Nodes (74): _load_page_overrides(), _load_preparation_recipe(), _prepare_overrides(), prepare_pages(), Path, Acquire and prepare source pages into a reproducible output bundle. Args:…, Load and validate a preparation recipe JSON file. Args: recipe:…, Load and validate a per-page override manifest. Args: overrides: Optional JSON… (+66 more)

### Community 14 - "test_preparation_service.py"
Cohesion: 0.09
Nodes (66): PageClassifier, PagePreparationService, PageQualityAssessor, Measure cheap, deterministic quality signals for one page raster., Suggest a page-class cohort from measured quality signals., Apply deterministic transforms and subdivision for one source page. Args:…, Bind assessor and classifier collaborators. Args: assessor: Quality-signal…, MockerFixture (+58 more)

### Community 15 - "BundlePaths"
Cohesion: 0.07
Nodes (48): BundlePaths, PageBundleManifest, On-disk page manifest for one Spec 0002 page bundle., Relative path helpers for one document bundle root. Args: root: Filesystem root…, OverlayState, Current overlay state for one reviewable object., Pointer from accepted graph content back to raw machine evidence., WitnessReference (+40 more)

### Community 16 - "HuggingFaceOlmocrRunner"
Cohesion: 0.07
Nodes (37): BatchUnitKind, Batch grouping units for runner execution., _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _ItemInvokeResult, _load_direct_image(), _load_image_from_pdf() (+29 more)

### Community 17 - "ADR 0010 Structured Output Boundary"
Cohesion: 0.05
Nodes (50): Accepted Page Graph, Acquisition Provenance, Bibliographic Provenance, bochord, Bundle JSON, Chunking Recipe, Diplomatic Text, Document Bundle (+42 more)

### Community 18 - "services/evaluation.py"
Cohesion: 0.13
Nodes (19): MetricProfile, BaseModel, Versioned, deterministic evaluation policy., _box_iou(), _boxes_intersect(), _coverage_allows(), _has_exhaustive_coverage(), Return intersection-over-union for two axis-aligned boxes. Args: left: First… (+11 more)

### Community 19 - "_SpanCandidate"
Cohesion: 0.15
Nodes (21): Any, Resolve typography facets from witness span candidates. Args: typography:…, Resolve each typography facet independently from span candidates. Args:…, Resolve font-family labels independently from span candidates. Args:…, Resolve enum-like typography facets from span candidates. Args: typography:…, Resolve optional boolean and float typography facets from span candidates.…, Resolve one enum-like typography facet from candidate values. Args: values:…, Resolve one optional boolean typography facet from candidate values. Args:… (+13 more)

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
Nodes (20): Exception, patch, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder…, Test that environment variables override defaults. (+12 more)

### Community 25 - "PageEvaluationSummary"
Cohesion: 0.11
Nodes (41): EvaluationCohortKey, EvaluationCohortReport, EvaluationCohortSummary, PageEvaluationRecord, One evaluated page with run, preparation, and runner context., Grouping key for one fixed evaluation cohort view., Aggregated evaluation output for one cohort., Fixed cohort views emitted by evaluation aggregation. (+33 more)

### Community 26 - "_try_rebind_event"
Cohesion: 0.11
Nodes (20): _coordinate_space_ids(), _nested_object_ids(), ReviewEvent, Apply one append-only event onto a mutable overlay state. Args: state:…, Record trust, applied event id, and reviewed/corrected dimensions. Args: state:…, Apply event-specific override fields named by the event contract. Structural…, Rebind one event when every required id resolves; otherwise skip it. Args:…, Collect nested marker/region/line/note ids that must remap. Args: event:… (+12 more)

### Community 27 - "SourcePageArtifact"
Cohesion: 0.07
Nodes (56): Print the some version info of this package,, version(), Supported top-level source kinds., SourceType, PdfPageImageMode, One acquired source page before preparation., PDF page rasterization strategy during source acquisition., SourcePageArtifact (+48 more)

### Community 28 - "_NoteCandidate"
Cohesion: 0.12
Nodes (31): _apply_note_link_resolution(), _mapped_note_link_sets(), _MarkerMappingContext, _min_merge_confidence(), _note_link_alternates(), _note_marker_links_from_mapped_sets(), _note_marker_links_when_mapping_ambiguous(), _note_text_alternates_from_candidates() (+23 more)

### Community 29 - "MergeOrchestrator"
Cohesion: 0.12
Nodes (14): MergeOrchestrator, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph…, Choose the accepted prepared page variant for this merge., Keep same-variant witnesses and record skipped cross-variant evidence., Pick one coordinate-rich structure scaffold and detect layout conflicts., Record insufficient evidence when no layout scaffold is available., Compare other witnesses against the chosen scaffold and flag conflicts. Args:… (+6 more)

### Community 30 - "GoldPageAnnotation"
Cohesion: 0.16
Nodes (13): GoldNoteLink, GoldPageAnnotation, Gold note-marker linkage target., Gold data slice for one page., _NoteLinkageScorer, Score exact marker-to-note edges and emit linkage flags. Gold…, Aggregate note-linkage success for covered gold edges. Args: prediction:…, Map predicted note ids to gold region annotation ids that name them. Args:… (+5 more)

### Community 31 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 32 - "_stable_json_schema"
Cohesion: 0.33
Nodes (6): Return Pydantic-generated JSON Schema with stable key ordering. Args:…, DocumentBundle JSON Schema must match the checked-in generated snapshot., RagDocument JSON Schema must match the checked-in generated snapshot., _stable_json_schema(), test_generated_schema_document_bundle_v1_matches_snapshot(), test_generated_schema_rag_document_v1_matches_snapshot()

### Community 33 - "DocumentExportService"
Cohesion: 0.05
Nodes (45): RagChunk, Page-local retrieval chunk., Cross-page retrieval chunk stitched from accepted page-local chunks., StitchedChunk, DocumentExportService, PageGraphIndex, Render an evidence-preserving Markdown reading view from accepted graphs. Args:…, Map linked marker span ids to owning note ids for one page. Args: page:… (+37 more)

### Community 34 - "test_runner_execution.py"
Cohesion: 0.15
Nodes (33): HostedInvocationResult, Raw result returned from one hosted runner invocation., InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root() (+25 more)

### Community 35 - "model_validator"
Cohesion: 0.05
Nodes (22): model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Keep top-level schema identity, page count, and page ids coherent. Returns: The…, Keep page-local page ids aligned with provenance. Returns: The validated page-…, Keep stitched page ids distinct and aligned with provenance. Returns: The…, Keep page-local and stitched retrieval references coherent. Returns: The…, Reject duplicate related ids and overlap with primary targets. Returns: The… (+14 more)

### Community 36 - "test_review_overlay.py"
Cohesion: 0.06
Nodes (66): AcceptReviewEvent, CorrectGeometryReviewEvent, CorrectStyleReviewEvent, CorrectTextReviewEvent, FlagReviewEvent, LinkNoteReviewEvent, MarkIllegibleReviewEvent, PageOverlay (+58 more)

### Community 37 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 38 - "model_runner_payload"
Cohesion: 0.18
Nodes (11): capability_payload(), execution_batch_payload(), model_runner_payload(), parametrize, Return a valid model-backed runner payload with optional overrides., Return a valid runner capability payload with optional overrides., Return a valid runner execution batch payload with optional overrides., test_model_backed_runner_requires_hardware_class() (+3 more)

### Community 39 - "PageXmlInterchangeService"
Cohesion: 0.12
Nodes (18): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+10 more)

### Community 40 - "_bundle_page_payload"
Cohesion: 0.09
Nodes (22): _bundle_page_payload(), Return a mutable dump of a valid bundle page with optional overrides., Graph boxes and polygons must name a known page coordinate space., Non-empty baselines require an explicit baseline coordinate space id., Baseline coordinate spaces must resolve to a known page space., Every line listed by a region must claim that region as parent., Every span listed by a line must claim that line as parent., Every note listed by a region must claim that region as parent. (+14 more)

### Community 41 - "_RateAccumulator"
Cohesion: 0.12
Nodes (19): GoldStyleSpan, Gold style target for one span or image-anchored area., Semantic role kept separate from visual typography., TextRole, _facet_match(), _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:… (+11 more)

### Community 42 - "RunnerExecutionPolicy"
Cohesion: 0.12
Nodes (32): Declared pass-runner input and batching contract., RunnerCapability, Frozen execution policy for one runner and hosting boundary., RunnerExecutionPolicy, Bind one hosted olmOCR runner to endpoint settings and an HTTP client. Args:…, Return the declared olmOCR input and batching contract. Returns: Hosted olmOCR…, _chunk_size(), Plan fixed runner batches from prepared artifacts and policy. (+24 more)

### Community 43 - "cli"
Cohesion: 0.13
Nodes (15): cli(), bochord command line interface. Args: ctx: Click context object. verbose:…, group, _dense_two_column_image(), Image, Path, Test the prepare command., Test prepare aborts before writes when override lacks a reason. (+7 more)

### Community 44 - "run_runner"
Cohesion: 0.20
Nodes (15): argument, eval_cohorts(), eval_page(), export_document(), Settings-related commands. Args: ctx: Click context object., Score one predicted page against gold annotations. Args: prediction: Predicted…, Summarize page evaluation records into fixed cohort views. Args: records: JSON…, Execute prepared artifacts against one hosted olmOCR runner. Args: ctx: Click… (+7 more)

### Community 45 - "Settings"
Cohesion: 0.19
Nodes (10): Settings management for bochord., Application settings with cascading configuration support. Note: The app_name…, Validate settings and ensure required directories exist. Raises:…, Settings, patch, Test the run command., _run_cli_args(), _runner_reference_json() (+2 more)

### Community 46 - "._score_text_pair"
Cohesion: 0.12
Nodes (14): _edit_distance(), _graphemes(), _is_ligature(), _is_macron_grapheme(), _is_thorn_eth(), Return whether ``grapheme`` carries a macron in NFC or NFD form. Args:…, Return whether ``grapheme`` is thorn or eth. Args: grapheme: One NFC grapheme…, Return whether ``grapheme`` is an OE ligature under watch. Args: grapheme: One… (+6 more)

### Community 47 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 48 - "TestOcrModels"
Cohesion: 0.05
Nodes (28): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Bundle pages store review event ids, not an embedded overlay graph., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events. (+20 more)

### Community 49 - "Spec 0004: Ordered V1 Implementation"
Cohesion: 0.15
Nodes (15): Spec 0004: Ordered V1 Implementation, Candidate Model Bake-Off, Hugging Face Hosted OCR Inference, Recommended Initial CLI, Ordered V1 Implementation Phases, Evidence-Bound Human Review, Spec 0012: Runner Execution and Batch Policy, Runner Batch Execution Policy (+7 more)

### Community 50 - "_stitched_chunk"
Cohesion: 0.09
Nodes (28): Return multi-page retrieval provenance with stable witness pointers., Return a cross-page stitched chunk with optional field overrides., Stitched chunk ids must stay unique within a RagDocument., Page-local chunks must not span multiple pages., Stitched chunks must span at least two distinct pages., JSONL stitched lines reject single-page provenance at parse time., Stitched page_ids must stay distinct in first-seen order., Stitched provenance must list every declared page. (+20 more)

### Community 51 - "_rag_chunk"
Cohesion: 0.12
Nodes (16): _rag_chunk(), Return a page-local retrieval chunk with optional field overrides., Page-local chunk ids must stay unique within a RagDocument., Page-local chunks must belong to the parent document., Stitched chunks must belong to the parent document., Page-local chunks must declare exactly one page., JSONL page-local lines reject multi-page provenance at parse time., Page-local chunks must retain at least one accepted source object. (+8 more)

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
Cohesion: 0.26
Nodes (12): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+4 more)

### Community 57 - "conftest.py"
Cohesion: 0.21
Nodes (12): cli_context(), mock_console(), mock_settings(), fixture, Test configuration and fixtures for the ai-coding project. This file contains…, Create a CLI runner for testing., Create a temporary directory for testing., Create a mock console for testing. (+4 more)

### Community 58 - "print_error"
Cohesion: 0.21
Nodes (8): print_error(), Print error message with optional suggestions. Args: message: Error message…, Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError

### Community 59 - ".score"
Cohesion: 0.19
Nodes (10): AnchoredGoldAnnotation, GoldRegionAnnotation, Gold annotation that resolves to graph evidence or prepared image geometry., Gold region or structure target., Score structure metrics and provenance-backed structure flags. Covers region…, Aggregate region, order, join, and table metrics for one page. Args:…, Resolve scored gold regions under exhaustive STRUCTURE coverage. Args:…, Score adjacent gold reading-order pairs among covered regions. Args: matches:… (+2 more)

### Community 60 - "Preparation Gold Specs"
Cohesion: 0.17
Nodes (12): V1 Gold Data Expectations, Spec 0007: PDF-to-Image Preparation, Competing Preparation Recipes, Coordinate and Image Provenance, Page Subdivision into OCR Units, Preparation Pipeline Stage, Preparation Recipe, V1 Page Class Taxonomy (+4 more)

### Community 61 - "Raw OCR witness layer"
Cohesion: 0.22
Nodes (9): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit, Lossless raw entry representation, OCR artifact ladder (witness/normalized/overlay/structured) (+1 more)

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

### Community 70 - "README, Operator Docs, and Thin Export CLI Implementation Plan"
Cohesion: 0.15
Nodes (12): Acceptance Checks, Deferred (explicitly not this plan), File Map, Global Constraints, Locked Decisions (from grilling), Plan Self-Review, README, Operator Docs, and Thin Export CLI Implementation Plan, Task 1: Thin `export` CLI (TDD) (+4 more)

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
Cohesion: 0.20
Nodes (10): Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Bosworth-Toller Anglo-Saxon Dictionary (+2 more)

### Community 79 - "test_merge_service.py"
Cohesion: 0.06
Nodes (124): MergePageInput, MergePolicy, Versioned deterministic merge precedence and acceptance thresholds., Competing witness fragments prepared for single-page merge., BoundingBox, FontFamilyCandidate, _geometry_space_id(), Return the named coordinate space for optional box or polygon geometry. Args:… (+116 more)

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

### Community 86 - "_review_polygon"
Cohesion: 0.29
Nodes (6): Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces., _review_box(), _review_polygon()

### Community 87 - "test_ocr_models.py"
Cohesion: 0.06
Nodes (27): _page_witness(), Return a witness owned by the given page., Existing provenance fixtures stay valid without alternate candidates., Document page ids must stay unique., Source page_count must remain exact versus exported pages., Return a valid preparation-recipe payload with optional overrides., Frozen document-bundle-v1.json must validate and dump identically., Frozen rag-document-v1.json must validate and dump identically. (+19 more)

### Community 88 - "_apply_span_text_resolution"
Cohesion: 0.20
Nodes (8): _apply_span_text_resolution(), Collect unique witness ids from span candidates in input order. Args:…, Collect unique runner ids from span candidates in input order. Args:…, Apply text agreement or disagreement resolution for one span. Args: span:…, Resolve diplomatic text for each accepted span from witness candidates., Choose diplomatic text for one accepted span from matched witnesses. Args:…, _runner_ids_from_candidates(), _witness_ids_from_candidates()

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

### Community 100 - "_apply_span_typography_resolution"
Cohesion: 0.22
Nodes (10): _apply_span_typography_resolution(), Confidence, alternates, and flag callback for span-role resolution., Resolve span roles from witness candidates. Args: candidates: Matched witness…, Apply typography and role resolution for one span. Args: span: Accepted span…, Resolve span roles from matched witness candidates. Args: candidates: Matched…, Serialize competing role lists as alternate candidates. Args: candidates:…, _resolve_span_role_conflicts(), _resolve_span_roles() (+2 more)

### Community 101 - "ADR 0008 Stable IDs and Review History"
Cohesion: 0.67
Nodes (3): ADR 0008 Stable IDs and Review History, Stable Graph Object IDs, machine/reviewed/corrected Trust States

### Community 102 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 128 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 129 - ".create_successor"
Cohesion: 0.20
Nodes (8): _normalize_tasks(), Normalize a successor task map or list into a task-id dictionary. Args:…, Reject task maps that point at missing successor tasks. Args: task_id_map:…, Derive successor run, graph, and checksum from caller-supplied tasks. Args:…, Replay ``overlay.review_events`` into per-object overlay state. Ignores any…, Build a rebased successor overlay without mutating the predecessor. Copies only…, _require_mapped_tasks(), _successor_bindings()

### Community 130 - "DocumentBundle"
Cohesion: 0.09
Nodes (22): DocumentBundle, Canonical software-facing document export., load_export_minimal_bundle(), load_frozen_document_bundle_v1(), Persisted document exports match renderer output and preserve overlays., Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the compact export-fixture DocumentBundle., Load the frozen document-bundle-v1 contract fixture. (+14 more)

### Community 131 - "Typography"
Cohesion: 0.36
Nodes (8): Orthogonal visual typography facets for one text span., Typography, bold_but_not_italic_prediction(), bold_italic_gold(), One span that is bold but upright (not italic)., Gold style requiring both bold and italic facets., test_style_facets_are_independent(), test_style_family_collapse_is_partial_xor()

### Community 132 - "_known_page_space_ids"
Cohesion: 0.33
Nodes (5): _known_page_space_ids(), _known_preparation_space_ids(), Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Keep prepared-unit ids unique and bound to this page's spaces. Returns: The…

### Community 133 - "Point"
Cohesion: 0.33
Nodes (4): Point, One point in an identified image coordinate space., Parse PAGE point strings into coordinate pairs. Args: points: Space-separated…, Derive one point list from PAGE Baseline or Coords. Args: element: Optional…

### Community 134 - "ReviewTaskType"
Cohesion: 0.33
Nodes (4): Operator workflow represented by a review task packet., ReviewTaskType, Build a deterministic task id from page, type, and target ids. Identity is…, HumanMarkupService task types must certify only their exclusive dimension.

### Community 135 - "_validate_zip_member"
Cohesion: 0.50
Nodes (5): Detect UNIX symlink members via ``external_attr``. Args: info: ZIP member…, Reject unsafe ZIP members and return a normalized relative path. Args: info:…, _validate_zip_member(), _zip_member_is_symlink(), ZipInfo

### Community 137 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 138 - "_PreparedInputsManifest"
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
- **137 isolated node(s):** `release.sh script`, `bochord`, `IPA_AUDIO`, `Locked Decisions (from grilling)`, `Global Constraints` (+132 more)
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
- **Why does `BundlePage` connect `BundlePage` to `._emit_result`, `models/__init__.py`, `test_text_normalization.py`, `DocumentBundle`, `test_bundle_layout.py`, `Typography`, `test_evaluation_service.py`, `TextNormalizer`, `test_document_export.py`, `cli.py`, `BundlePaths`, `services/evaluation.py`, `GoldPageAnnotation`, `test_page_interchange.py`, `DocumentExportService`, `model_validator`, `PageXmlInterchangeService`, `.score`, `test_merge_service.py`, `test_ocr_models.py`, `._write_page_xml`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `AlternateCandidate` connect `models/__init__.py` to `DocumentBundle`, `PlannedRunnerBatch`, `test_bundle_layout.py`, `BundlePage`, `services/preparation.py`, `Point`, `test_evaluation_service.py`, `ReviewTaskType`, `RunnerThroughputSummary`, `Typography`, `test_document_export.py`, `cli.py`, `BundlePaths`, `HuggingFaceOlmocrRunner`, `_SpanCandidate`, `PageEvaluationSummary`, `SourcePageArtifact`, `_NoteCandidate`, `GoldPageAnnotation`, `DocumentExportService`, `test_review_overlay.py`, `_RateAccumulator`, `RunnerExecutionPolicy`, `.score`, `test_merge_service.py`, `test_ocr_models.py`, `_apply_span_typography_resolution`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `DocumentBundle`, `PlannedRunnerBatch`, `test_bundle_layout.py`, `BundlePage`, `services/preparation.py`, `Point`, `test_evaluation_service.py`, `Typography`, `RunnerThroughputSummary`, `test_text_normalization.py`, `cli.py`, `BundlePaths`, `services/evaluation.py`, `PageEvaluationSummary`, `SourcePageArtifact`, `GoldPageAnnotation`, `DocumentExportService`, `test_runner_execution.py`, `test_review_overlay.py`, `RunnerExecutionPolicy`, `.score`, `test_merge_service.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 94 inferred relationships involving `AlternateCandidate` (e.g. with `BundlePage` and `CoordinateSpace`) actually correct?**
  _`AlternateCandidate` has 94 INFERRED edges - model-reasoned connections that need verification._