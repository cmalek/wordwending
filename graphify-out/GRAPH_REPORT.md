# Graph Report - wordwending  (2026-08-08)

## Corpus Check
- 201 files · ~249,790 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4043 nodes · 11528 edges · 143 communities (126 shown, 17 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1173 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `555b568e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- BundleLayoutService
- test_ocr_models.py
- services/preparation.py
- MergePolicy
- QualitySignal
- test_merge_review.py
- SpanRecord
- cli.py
- services/merge.py
- Path
- services/evaluation.py
- SchemaModel
- _build_document_run_orchestrator
- ReviewCliService
- test_preparation_service.py
- models/__init__.py
- _rag_chunk
- PlannedRunnerBatch
- test_write_document_exports_frozen_contract_jsonl_validates
- test_document_run.py
- test_evaluation_service.py
- test_runner_execution.py
- Path
- test_text_normalization.py
- evaluation_cohorts.py
- MergeOrchestrator
- test_olmocr_runner.py
- test_kraken_runner.py
- test_assemble.py
- RunnerThroughputSummary
- EndpointLifecycleService
- TestOcrModels
- ReviewTask
- check_napoleon_gate.py
- From Source Material to Markdown
- BundleChecksumService
- DocumentRunOrchestrator
- TestConfiguration
- BundlePaths
- test_assemble_manifest.py
- test_graph_rebase.py
- BT Witness Preparation Slice
- EndpointSessionLedgerStore
- test_review_cli.py
- WitnessAdaptationService
- HfEndpointClient
- source_acquisition.py
- PageXmlInterchangeService
- review_cli.py
- model_validator
- test_page_interchange.py
- Settings
- ResumeLedgerService
- EndpointRemoteState
- cli
- Hands-Off Operator Path Implementation Plan
- PreparedArtifactRef
- test_endpoint_lifecycle.py
- EndpointCatalogEntry
- SourceAcquisitionService
- Phase 2 Gold Evaluator Plan
- RunnerInputPackager
- Spec 0012: Runner Execution and Batch Policy
- Machine Assistance Resources
- TestCLIReview
- RagChunk
- Architecture review — wordwending
- conftest.py
- TestCLISettings
- TestCLIGlobalOptions
- build_endpoint_lifecycle_service
- Architecture documentation index
- Spec 0006: Exports and Retrieval Views
- i-mutation / i-umlaut
- test_cli_utils.py
- main
- ADR 0011: Hugging Face Endpoint Lifecycle
- Spec 0003: V1 Evaluation Schema
- Raw OCR witness layer
- print_error
- Image
- _AssembleExecution
- ._coords
- Coordinate-Rich Kraken Adaptation Plan
- create_progress
- ._write_page_xml
- Spec 0009: Merge and Alignment
- ._bbox_from_coords
- _line_has_required_geometry
- model_validator
- Anglian dialect group
- .validate_https_huggingface_endpoints
- TestCLIExport
- Learner lacks stable conceptual map of sound-change order
- OE Grammar Resources
- test_write_document_exports_writes_derived_views
- Spec 0007: PDF-to-Image Preparation
- Python Coding Standards
- DocumentExportService
- Machine Assistance Mission
- Reference 0006 OCR Output Formats
- Prepared Page Image (page-0001)
- test_assemble_eval_export_wave_a_exit
- TestCLIEval
- TestPrintSuccess
- TestConsoleQuietMode
- prepare_pages
- V1 Engine Bake-Off
- Spec 0002: V1 Bundle Layout and Data Shape
- Rename bochord to wordwending Implementation Plan
- Lesson 0003 Pronouncing Old English Letters
- ADR 0009: Adapt OCR-D/PAGE and eScriptorium Boundaries
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- Chris Malek
- Character Error Rate (CER)
- test_live_hf_bakeoff_requires_integration_marker
- test_live_endpoint_lifecycle_smoke
- review.py
- release.sh
- Contributor Covenant 3.0
- ADR 0005 Evaluation First
- Domain Language
- Worked BT entry example: abbad
- Old English c/g palatalization
- OE tēon walk-back (Grimm + h-loss + contraction)
- ipa-play.js
- BundlePage
- .__init__
- Changelog
- Contributing
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- wordwending
- Mixed dialect spellings from copying history
- Reference Sound Terms

## God Nodes (most connected - your core abstractions)
1. `BundlePage` - 171 edges
2. `SchemaModel` - 134 edges
3. `AlternateCandidate` - 120 edges
4. `BundleLayoutService` - 96 edges
5. `cli()` - 94 edges
6. `MergePolicy` - 90 edges
7. `CoordinateSpace` - 90 edges
8. `PreparedPage` - 87 edges
9. `Settings` - 81 edges
10. `PageClass` - 79 edges

## Surprising Connections (you probably didn't know these)
- `DocumentBundle` --semantically_similar_to--> `Document bundle`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-08-02-spec-0006-exports-and-retrieval.md → CONTEXT.md
- `RagDocument` --semantically_similar_to--> `RAG JSON export contract`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-08-02-spec-0006-exports-and-retrieval.md → CONTEXT.md
- `Diplomatic vs Normalized Dual Fields` --semantically_similar_to--> `Dual Text Contract`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-07-31-spec-0008-text-normalization.md → doc/source/architecture/text_normalization_policy_v1.rst
- `Architecture review — wordwending` --conceptually_related_to--> `Phase 10 Operational Hardening (NOT COMPLETE)`  [AMBIGUOUS]
  Architecture review — wordwending.html → doc/source/architecture/spec_0004_v1_implementation_plan.rst
- `Architecture review — wordwending` --conceptually_related_to--> `Phase 6 PassRunner Protocol (COMPLETE)`  [AMBIGUOUS]
  Architecture review — wordwending.html → doc/source/architecture/spec_0004_v1_implementation_plan.rst

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Evidence-Preserving Text Pipeline** — doc_source_architecture_spec_0008_text_normalization_dual_text [INFERRED 0.85]
- **Spec Completion Sequence 0003→0007→0010→0012** — docs_superpowers_plans_2026_07_25_spec_0003_evaluation_schema_completion_document, docs_superpowers_plans_2026_07_25_spec_0007_preparation_completion_document, docs_superpowers_plans_2026_07_25_spec_0010_page_classification_cohorts_document, docs_superpowers_plans_2026_07_25_spec_0012_runner_execution_batching_document [EXTRACTED 1.00]
- **Text Normalization V1 Pipeline** — docs_superpowers_plans_2026_07_31_spec_0008_text_normalization_textnormalizationpolicy, docs_superpowers_plans_2026_07_31_spec_0008_text_normalization_textnormalizer, doc_source_architecture_text_normalization_policy_v1_text_norm_v1, doc_source_architecture_text_normalization_policy_v1_dual_text_contract, docs_superpowers_plans_2026_08_01_text_normalization_policy_v1_docs_only_contract [EXTRACTED 1.00]
- **V1 Retrieval Chunk Types** — docs_superpowers_plans_2026_08_02_spec_0006_exports_and_retrieval_region_chunk, docs_superpowers_plans_2026_08_02_spec_0006_exports_and_retrieval_footnote_chunk, docs_superpowers_plans_2026_08_02_spec_0006_exports_and_retrieval_stitched_chunk [EXTRACTED 1.00]
- **BT Witness Prep Through CLI Pipeline** — docs_superpowers_specs_2026_07_10_bt_ocr_witness_preparation_design_bt_witness_prep, docs_superpowers_specs_2026_07_10_bt_ocr_stage_b_live_pairing_and_clamp_regression_design_prepare_pages, docs_superpowers_specs_2026_07_12_wyrdcraeft_ocr_bosworth_toller_bosworth_toller_cli, docs_superpowers_specs_2026_07_12_wyrdcraeft_ocr_bosworth_toller_bt_witness_ocr [EXTRACTED 1.00]
- **Witness-preserving OCR-to-structure workflow** — teaching_machine_assistance_lessons_0004_seven_stage_pipeline, teaching_machine_assistance_lessons_0004_raw_witness_layer, teaching_machine_assistance_lessons_0004_overlay_layer, teaching_machine_assistance_lessons_0004_normalized_export_layer, teaching_machine_assistance_lessons_0004_review_by_exception, teaching_machine_assistance_lessons_0006_entry_block_unit [EXTRACTED 1.00]
- **PIE to OE sound-change layering timeline** — teaching_oe_grammar_lessons_0001_proto_indo_european, teaching_oe_grammar_lessons_0001_grimms_law, teaching_oe_grammar_lessons_0001_verners_law, teaching_oe_grammar_lessons_0001_proto_germanic, teaching_oe_grammar_lessons_0001_i_mutation, teaching_oe_grammar_reference_0001_sound_change_order [EXTRACTED 1.00]
- **OE dialect recognition cue system** — teaching_oe_grammar_lessons_0002_west_saxon, teaching_oe_grammar_lessons_0002_anglian, teaching_oe_grammar_lessons_0002_kentish, teaching_oe_grammar_lessons_0002_mercian, teaching_oe_grammar_lessons_0002_northumbrian, teaching_oe_grammar_reference_0004_dialect_cue_table [EXTRACTED 1.00]
- **Witness production pipeline** — adr_0001_workflow_acquire_to_export, context_document_bundle, context_page_graph, spec_0006_three_export_views [INFERRED 0.85]
- **Layered artifact stack** — context_raw_witness_artifact, context_page_graph, adr_0008_append_only_review, spec_0006_three_export_views [EXTRACTED 1.00]
- **Spec 0001 v1 core service cluster** — spec_0001_documentrunorchestrator, spec_0001_pagepreparationservice, spec_0001_passrunnerregistry, spec_0001_pagealignmentservice, spec_0001_pagegraphbuilder [EXTRACTED 1.00]
- **Runner Execution Policy and Persistence Schema Stack** — doc_source_architecture_spec_0012_runner_execution_and_batching_runner_execution_policy, doc_source_architecture_spec_0012_runner_execution_and_batching_batching_policy, doc_source_architecture_spec_0013_pass_runner_interface_schema_runner_capability, doc_source_architecture_spec_0013_pass_runner_interface_schema_runner_execution_batch [INFERRED 0.85]
- **Human Correction via Append-Only Review Overlays** — doc_source_architecture_spec_0014_review_overlay_schema_review_task, doc_source_architecture_spec_0014_review_overlay_schema_page_overlay, doc_source_architecture_spec_0014_review_overlay_schema_overlay_state, doc_source_architecture_wave_b_architecture_notes_custom_review_cli, doc_source_overview_usage_review_apply [EXTRACTED 1.00]
- **Operator End-to-End Spine** — doc_source_runbook_from_source_to_markdown_operator_spine, doc_source_overview_usage_assemble_command, doc_source_overview_usage_export_command, doc_source_architecture_spec_0016_concrete_export_models_document_bundle, doc_source_runbook_from_source_to_markdown_markdown_not_sot [EXTRACTED 1.00]
- **Document run machine path** — docs_superpowers_plans_2026_08_07_document_run_orchestrator_document_run_orchestrator, docs_superpowers_plans_2026_08_07_document_run_orchestrator_document_run_stage, docs_superpowers_plans_2026_08_07_hands_off_operator_path_assemble_manifest_builder, docs_superpowers_plans_2026_08_07_v1_spine_and_phase_completion_assemble_orchestrator, docs_superpowers_plans_2026_08_07_hands_off_operator_path_review_issue [EXTRACTED 1.00]
- **Hands-off operator path three gaps** — docs_superpowers_plans_2026_08_07_hands_off_operator_path_assemble_manifest_builder, docs_superpowers_plans_2026_08_07_hands_off_operator_path_review_issue, docs_superpowers_plans_2026_08_07_hands_off_operator_path_graph_rebase_service [EXTRACTED 1.00]
- **HF endpoint lifecycle service stack** — docs_superpowers_specs_2026_08_07_hf_endpoint_lifecycle_design_endpoint_lifecycle_service, docs_superpowers_plans_2026_08_07_hf_endpoint_lifecycle_hf_endpoint_client, docs_superpowers_specs_2026_08_07_hf_endpoint_lifecycle_design_endpoint_session_ledger, docs_superpowers_plans_2026_08_07_hf_endpoint_lifecycle_ensure_endpoints_flag [EXTRACTED 1.00]
- **Hands-Off Prepare Page-0001 Fixture Artifacts** — tests_fixtures_hands_off_prepare_pages_page_0001_prepared_prepared_page_1_image_prepared_page_image, tests_fixtures_hands_off_prepare_pages_page_0001_prepared_prepared_page_1_image_prepared_page_artifact_slot, tests_fixtures_hands_off_prepare_pages_page_0001_prepared_prepared_page_1_image_source_page_0001, tests_fixtures_hands_off_prepare_pages_page_0001_prepared_prepared_page_1_image_hands_off_prepare_fixture [INFERRED 0.85]

## Communities (143 total, 17 thin omitted)

### Community 0 - "BundleLayoutService"
Cohesion: 0.05
Nodes (82): Path, Document source digests are omitted from verification when not recorded., Prepared units without recorded digests are skipped honestly., Materialize a minimal bundle whose recorded digests match on-disk bytes., Recorded digests that match on-disk bytes report OK., Tampered prepared image bytes report FAIL against the recorded digest., _sha256_label(), test_verify_matching_checksums_ok() (+74 more)

### Community 1 - "test_ocr_models.py"
Cohesion: 0.03
Nodes (77): _bundle_page_payload(), capability_payload(), execution_batch_payload(), model_runner_payload(), _page_witness(), _prepared_unit_ref(), _provenance(), parametrize (+69 more)

### Community 2 - "services/preparation.py"
Cohesion: 0.05
Nodes (100): BundlePage carries graph-v0 by default for overlay binding., test_bundle_page_defaults_graph_revision(), _FakePreparation, Records prepare calls and seeds preparation.json under output_dir., Graph parent-child identifiers must resolve within the page., Prepared-unit identifiers must be unique on one prepared page., Prepared units must belong to the prepared page and known spaces., test_prepared_page_rejects_duplicate_prepared_unit_ids() (+92 more)

### Community 3 - "MergePolicy"
Cohesion: 0.06
Nodes (115): _aligned_text_witnesses(), _bounding_box(), _coordinate_space(), _line(), _load_merge_fixture(), _note(), _prepared_page(), _provenance() (+107 more)

### Community 4 - "QualitySignal"
Cohesion: 0.08
Nodes (43): AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _bleedthrough_signal(), _border_shadow_signal(), _colored_marking_signal() (+35 more)

### Community 5 - "test_merge_review.py"
Cohesion: 0.06
Nodes (45): Enum, _eval_flag(), _merge_flag(), _page_with_text_flags(), parametrize, Return one merge flag fixture., Return one evaluation flag with an explicit merge flag_type., Attach evaluation flags onto the text family only (legacy C3 shape). (+37 more)

### Community 6 - "SpanRecord"
Cohesion: 0.02
Nodes (164): _body_region_page(), _document_bundle(), _load_frozen_document_bundle_v1(), _load_minimal_bundle(), _markdown_style_page(), _merge_page_regions(), _minimal_document_bundle(), _object_provenance() (+156 more)

### Community 7 - "cli.py"
Cohesion: 0.05
Nodes (73): test_document_bundle_manifest_rejects_non_positive_page_count(), test_document_bundle_manifest_round_trip(), _minimal_document_bundle(), Records RunnerExecutionService.run invocations., Return a tiny DocumentBundle for stubbed assemble/export stages., Records AssembleManifestBuilder.build calls., Records assemble_document calls and writes document-bundle.json., _RecordingAssemble (+65 more)

### Community 8 - "services/merge.py"
Cohesion: 0.04
Nodes (101): _LayoutObject, NamedTuple, _apply_layout_merge_confidence(), _apply_note_link_resolution(), _apply_span_text_resolution(), _apply_span_typography_resolution(), _attach_alternates_to_objects(), _box_iou() (+93 more)

### Community 9 - "Path"
Cohesion: 0.05
Nodes (45): Multiple source/pages/NNNN.* files must not silently pick one., test_page_dir_name_is_zero_padded(), test_resolve_source_image_path_rejects_ambiguous_extensions(), page_dir_name(), Return the stable page directory name for one 1-based page number. Args:…, _atomic_write_json(), _executed_passes(), _needs_trailing_newline() (+37 more)

### Community 10 - "services/evaluation.py"
Cohesion: 0.05
Nodes (51): _box(), Build one axis-aligned box in the fixture prepared-page space., BoundingBox, GoldStyleSpan, Gold style target for one span or image-anchored area., Axis-aligned rectangle for page-relative geometry., Semantic role kept separate from visual typography., TextRole (+43 more)

### Community 11 - "SchemaModel"
Cohesion: 0.06
Nodes (87): _gold(), _prediction(), profile(), Path, Build one gold page annotation matching the prediction span., Schema defaults name real ADR 0007 candidates, not FakePassRunner., Matrix cells carry runner, page class, scores, latency, failure, license., Harness scores recorded (mocked) responses for both real candidates. (+79 more)

### Community 12 - "_build_document_run_orchestrator"
Cohesion: 0.06
Nodes (49): argument, PassRunnerClass, test_register_overrides_or_adds_runner_id(), test_resolve_unknown_runner_id_fails_clearly(), _build_document_run_endpoint_ensurer(), _build_document_run_orchestrator(), _build_document_run_runner_factory(), document_run() (+41 more)

### Community 13 - "ReviewCliService"
Cohesion: 0.10
Nodes (20): Path, Orchestrate review apply / materialize / issue / rebase for bundle pages. Keeps…, Validate an overlay, append new events, and rewrite overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, Rebuild pending review tasks from one page's evaluation flags. Args:…, Apply overlay corrections onto the page graph and write a successor overlay.…, Ensure overlay task targets exist on the accepted page graph. Validation is…, Validate one review task's targets against the page graph. Args: page: Accepted… (+12 more)

### Community 14 - "test_preparation_service.py"
Cohesion: 0.09
Nodes (66): MockerFixture, binary_recipe(), bundle_service(), dark_gutter_image(), dense_source_page(), dense_two_column_image(), note_heavy_image(), preparation_service() (+58 more)

### Community 15 - "models/__init__.py"
Cohesion: 0.03
Nodes (132): Runner, overlay, and gold contracts should fit the planned workflow., _event_base(), _polygon(), datetime, MonkeyPatch, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is… (+124 more)

### Community 16 - "_rag_chunk"
Cohesion: 0.07
Nodes (46): _minimal_rag_document(), _rag_chunk(), Return multi-page retrieval provenance with stable witness pointers., Return a page-local retrieval chunk with optional field overrides., Return a cross-page stitched chunk with optional field overrides., Return a document-level RAG export with optional chunk overrides., Page-local chunk ids must stay unique within a RagDocument., Stitched chunk ids must stay unique within a RagDocument. (+38 more)

### Community 17 - "PlannedRunnerBatch"
Cohesion: 0.03
Nodes (113): LookupError, MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., ConfigurationError, Raised when settings or configuration fails., Raised when a hosted runner endpoint is not ready for inference. (+105 more)

### Community 18 - "test_write_document_exports_frozen_contract_jsonl_validates"
Cohesion: 0.50
Nodes (4): load_frozen_document_bundle_v1(), Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the frozen document-bundle-v1 contract fixture., test_write_document_exports_frozen_contract_jsonl_validates()

### Community 19 - "test_document_run.py"
Cohesion: 0.08
Nodes (63): _absolute_prepare_run_config(), _FakeRegistry, _full_page_preparation_json(), _make_orchestrator(), Any, Path, Write preparation.json under the prepare-tree layout., PassRunnerRegistry stand-in returning a sentinel class. (+55 more)

### Community 20 - "test_evaluation_service.py"
Cohesion: 0.07
Nodes (66): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+58 more)

### Community 21 - "test_runner_execution.py"
Cohesion: 0.13
Nodes (41): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+33 more)

### Community 22 - "Path"
Cohesion: 0.07
Nodes (26): Path, inspect-bundle does not list export paths until export has run., inspect-bundle lists exports/* paths after assemble and export., inspect-bundle prints document and page summary., inspect-bundle surfaces OK after assemble seals prepared-image digests., inspect-bundle surfaces OK when layout digests match on-disk bytes., inspect-bundle prints merge flags after multi-witness disagreement., Assemble fails when manifest witness paths are absent under bundle_root. (+18 more)

### Community 23 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (43): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+35 more)

### Community 24 - "evaluation_cohorts.py"
Cohesion: 0.10
Nodes (38): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+30 more)

### Community 25 - "MergeOrchestrator"
Cohesion: 0.06
Nodes (27): _first_witness_by_runner_preference(), _flagged_object_ids(), MergeOrchestrator, Return a span flagged for missing witness text evidence. Args: span: Accepted…, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Initialize merge orchestration for one page. Args: policy: Versioned merge…, Collect object ids already referenced by merge flags. Args: flags: Merge flags…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph… (+19 more)

### Community 26 - "test_olmocr_runner.py"
Cohesion: 0.13
Nodes (40): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Any (+32 more)

### Community 27 - "test_kraken_runner.py"
Cohesion: 0.14
Nodes (39): hosted_runner(), kraken_response(), mock_client(), planned_batch(), policy(), policy_with_endpoint(), Any, BaseException (+31 more)

### Community 28 - "test_assemble.py"
Cohesion: 0.14
Nodes (47): _acquisition(), _bibliographic(), _coordinate_space(), _merge_policy(), _MergeWithExtraFlags, _orchestrator(), _prepared_page(), Path (+39 more)

### Community 29 - "RunnerThroughputSummary"
Cohesion: 0.06
Nodes (37): Persisted batch status must agree with submitted and failed items., test_throughput_summary_accepts_coherent_values(), test_throughput_summary_rejects_inconsistent_items_per_second(), Exact persisted record for one runner invocation., RunnerExecutionBatch, model_validator, Require one page number for every packaged batch item. Returns: The validated…, Measured throughput for one runner execution segment. (+29 more)

### Community 30 - "EndpointLifecycleService"
Cohesion: 0.08
Nodes (29): datetime, endpoints(), group, Ensure, pause, or inspect Hugging Face Inference Endpoints., EndpointLifecycleError, FileError, Raised when file I/O operations fail., Raised when Hugging Face endpoint lifecycle operations fail. (+21 more)

### Community 31 - "TestOcrModels"
Cohesion: 0.05
Nodes (27): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Return fields required by every review event., Return a valid review geometry bounding box., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events. (+19 more)

### Community 32 - "ReviewTask"
Cohesion: 0.07
Nodes (26): A review task should be actionable without undocumented context., Review tasks must bind to the prepared image the operator inspects., Related ids must not duplicate or overlap primary targets., Related object ids must be unique., Self-contained instructions and evidence binding for human review., ReviewTask, Project merge flags onto pages and build Spec 0005 pending tasks. Replaces…, Build a span-scoped diplomatic-text review task packet. Task identity is scoped… (+18 more)

### Community 33 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 34 - "From Source Material to Markdown"
Cohesion: 0.05
Nodes (43): Spec 0014: Review Task and Overlay Schema, OverlayState, PageOverlay, ReviewTask, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle, PreparedPage, RagChunk (+35 more)

### Community 35 - "BundleChecksumService"
Cohesion: 0.12
Nodes (20): BundleChecksumReport, ChecksumVerificationResult, ChecksumVerificationStatus, StrEnum, Outcome for one recorded checksum field verified against on-disk bytes., One bundle-relative path checked against a recorded digest label., Aggregate checksum verification results for one bundle root., Return whether every non-skipped verification succeeded. Returns: ``True`` when… (+12 more)

### Community 36 - "DocumentRunOrchestrator"
Cohesion: 0.10
Nodes (29): DocumentRunConfig, DocumentRunStage, StrEnum, Return whether gold and metric profile enable default eval. Returns: ``True``…, Stages in a full document run machine path., Configuration for one orchestrated document run., Return the stage order for this run. Returns: Explicit ``stages`` when set;…, Return the default machine path before ``skip_export`` filtering. Returns:… (+21 more)

### Community 37 - "TestConfiguration"
Cohesion: 0.06
Nodes (22): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+14 more)

### Community 38 - "BundlePaths"
Cohesion: 0.08
Nodes (25): test_bundle_paths_match_spec_0002_layout(), test_source_page_image_rejects_empty_extension(), BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:… (+17 more)

### Community 39 - "test_assemble_manifest.py"
Cohesion: 0.11
Nodes (39): _acquisition(), _bibliographic(), _build(), _load_batch(), _merge_policy(), Path, Single succeeded run yields one page with one copied witness., Two runner runs merge into one page with two witnesses. (+31 more)

### Community 40 - "test_graph_rebase.py"
Cohesion: 0.05
Nodes (54): _GraphNode, Text overrides rewrite span diplomatic text by object_id + scope., Text overrides rewrite note diplomatic text by object_id + scope., Typography and role overrides update the matching span., Unknown object_id raises ValueError naming the id., Returned page carries the caller-supplied graph_revision., Aside from applied overrides and revision, the page graph is equal., Geometry, region_kind, and note linkage overrides update targets. (+46 more)

### Community 41 - "BT Witness Preparation Slice"
Cohesion: 0.06
Nodes (38): correct_text Review Event, Text Normalization Policy v1, Dual Text Contract, text-norm-v1 Policy, TextNormalizer, Append-Only Review History, BundleLayoutService, BundlePaths (+30 more)

### Community 42 - "EndpointSessionLedgerStore"
Cohesion: 0.11
Nodes (29): Path, test_corrupt_ledger_loads_empty(), test_ledger_round_trip(), test_mark_down_records_pause_action(), test_missing_ledger_loads_empty(), test_save_persists_ledger(), test_touch_rejects_invalid_action(), test_touch_replaces_same_runner_id() (+21 more)

### Community 43 - "test_review_cli.py"
Cohesion: 0.09
Nodes (49): _eval_flag(), _gold_task(), _overlay_with_tasks(), Path, Return a span-scoped text review task for validation fixtures., Return a gold task packet (unsupported by review apply)., Return a minimal PageOverlay carrying the given review tasks., Return one evaluation flag for pending-task regeneration fixtures. (+41 more)

### Community 44 - "WitnessAdaptationService"
Cohesion: 0.06
Nodes (59): _coordinate_space(), _prepared_page(), Path, Two independent adapt_page calls yield identical ids and diplomatic texts. ADR…, Adapted span ids and texts match assemble gold-v1 target_object_ids., Empty artifact_paths list is rejected before reading., Non-chat.completion JSON is rejected as an invalid raw witness., Write a minimal chat.completion witness artifact for adaptation tests. (+51 more)

### Community 45 - "HfEndpointClient"
Cohesion: 0.10
Nodes (25): InferenceEndpoint, _FakeInferenceEndpoint, MonkeyPatch, test_constructor_requires_token(), test_create_omits_scale_to_zero_when_disabled(), test_create_passes_catalog_fields_and_scale_to_zero(), test_describe_maps_remote_state(), test_hub_errors_map_to_endpoint_lifecycle_error() (+17 more)

### Community 46 - "source_acquisition.py"
Cohesion: 0.10
Nodes (32): PdfPage, _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), _pdf_page_image(), Image (+24 more)

### Community 47 - "PageXmlInterchangeService"
Cohesion: 0.15
Nodes (14): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+6 more)

### Community 48 - "review_cli.py"
Cohesion: 0.11
Nodes (22): _bump_graph_revision(), _identity_object_id_map(), ReviewEvent, Outcome of appending overlay events and rewriting overlay state., Outcome of replaying append-only review history into overlay state., Return the next graph revision by bumping a trailing integer. Args: revision:…, Build an identity object-id map for leaf-only graph rebase. Args: page: Rebased…, Outcome of rebasing overlay corrections onto the accepted page graph. (+14 more)

### Community 49 - "model_validator"
Cohesion: 0.05
Nodes (25): _known_page_space_ids(), _known_preparation_space_ids(), model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Require provenance pointers to stay local to the owning page. Args: provenance:… (+17 more)

### Community 50 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 51 - "Settings"
Cohesion: 0.10
Nodes (31): BaseSettings, PydanticBaseSettingsSource, configured_settings(), ExplodingEndpointLifecycleService, fake_service(), FakeEndpointLifecycleService, fixture, patch (+23 more)

### Community 52 - "ResumeLedgerService"
Cohesion: 0.11
Nodes (22): Path, test_corrupt_ledger_is_treated_as_empty(), test_missing_ledger_is_empty(), test_record_completed_persists_and_reloads(), test_record_completed_replaces_same_batch_id(), One successfully completed runner batch recorded for resume., Persisted set of successfully completed runner batches under a bundle., ResumeLedger (+14 more)

### Community 53 - "EndpointRemoteState"
Cohesion: 0.10
Nodes (15): FakeHfEndpointClient, In-memory ``EndpointClient`` double for lifecycle unit tests., test_fake_satisfies_endpoint_client_protocol(), EndpointRemoteState, Remote Inference Endpoint snapshot from Hugging Face Hub., EndpointClient, Protocol, Scale one endpoint to zero replicas. Args: name: Inference Endpoint name in the… (+7 more)

### Community 54 - "cli"
Cohesion: 0.08
Nodes (26): _dense_two_column_image(), Image, patch, Test the document-run command., document-run --help exits zero and documents options., Invalid config JSON exits nonzero with a ClickException message., document-run loads config, calls orchestrator, and echoes result., --force sets force_rerun on the config passed to orchestrator.run. (+18 more)

### Community 55 - "Hands-Off Operator Path Implementation Plan"
Cohesion: 0.09
Nodes (28): DocumentRunOrchestrator Implementation Plan, DocumentRunConfig, DocumentRunOrchestrator, DocumentRunStage, Multi-runner execution run_id, Hands-Off Operator Path Implementation Plan, assemble --from-run CLI, AssembleManifestBuilder (+20 more)

### Community 56 - "PreparedArtifactRef"
Cohesion: 0.13
Nodes (31): Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), artifacts(), capability(), policy(), _prepared_unit(), Return a default multi-item runner capability with optional overrides., Return a default runner execution policy with optional overrides. (+23 more)

### Community 57 - "test_endpoint_lifecycle.py"
Cohesion: 0.30
Nodes (17): _assert_is_endpoint_client(), _catalog(), Path, _service(), _settings(), test_down_pauses_by_default_delete_flag_destroys(), test_ensure_up_already_running_skips_create_and_resume(), test_ensure_up_creates_missing_and_returns_https_url() (+9 more)

### Community 58 - "EndpointCatalogEntry"
Cohesion: 0.16
Nodes (15): test_catalog_entry_rejects_mutable_revision(), test_default_catalog_includes_olmocr_and_kraken(), test_default_catalog_revisions_are_immutable(), test_mutable_revision_rejected(), test_settings_idle_and_ledger_defaults(), default_endpoint_catalog(), EndpointCatalogEntry, mutable_revision_rejected() (+7 more)

### Community 59 - "SourceAcquisitionService"
Cohesion: 0.21
Nodes (21): pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe(), test_image_bounds_must_overlap_most_of_page_area(), test_image_folder_records_image_set_source_type() (+13 more)

### Community 60 - "Phase 2 Gold Evaluator Plan"
Cohesion: 0.12
Nodes (19): Phase 2 Gold Evaluator Plan, EvaluationService, GoldLineJoin, regex Unicode Grapheme Clusters, Phase 3 Acquisition Preparation Plan, PagePreparationService, Pillow and pypdfium2 Stack, SourceAcquisitionService (+11 more)

### Community 61 - "RunnerInputPackager"
Cohesion: 0.12
Nodes (30): bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests., test_direct_packaging_references_original_artifact(), test_direct_packaging_rejects_multi_item_batch() (+22 more)

### Community 62 - "Spec 0012: Runner Execution and Batch Policy"
Cohesion: 0.14
Nodes (17): Spec 0012: Runner Execution and Batch Policy, Batching Policy, Hugging Face Execution Boundary, Image-to-PDF Packaging, Input Packaging Policy, olmOCR V1 Execution Policy, Runner Execution Policy, Spec 0013: Pass-Runner Interface Schema (+9 more)

### Community 63 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 64 - "TestCLIReview"
Cohesion: 0.17
Nodes (9): Test review apply and materialize commands., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends overlay events and materializes current_state.json., Re-applying the same overlay must not rewrite prior JSONL bytes., Materialize replays JSONL history into current_state.json., Apply fails when --page-id does not match the overlay file., Apply fails when overlay tasks reference ids absent from the page., Materialize fails when the bundle has no matching page id. (+1 more)

### Community 65 - "RagChunk"
Cohesion: 0.16
Nodes (9): RagChunk, Page-local retrieval chunk., Build cross-page stitched chunks from contiguous BODY region runs. Args:…, Emit one stitched chunk when a BODY run spans multiple pages. Args:…, Collect ordered distinct page ids from component chunks. Args: chunks: Region…, Union source object ids from component region chunks. Args: chunks: Region…, Union provenance pointers from component region chunks. Args: chunks: Region…, Aggregate trust from one or more trust-state values. Args: trust_states: Trust… (+1 more)

### Community 66 - "Architecture review — wordwending"
Cohesion: 0.18
Nodes (17): acquire → prepare → run passes → align → evaluate → review → export, AssembleOrchestrator, DocumentRunOrchestrator, MergeOrchestrator, RunnerExecutionOrchestrator, Missing E2E seam (raw witness → PassWitnessPage → merge → bundle), PassWitnessPage adapter seam, Architecture review — wordwending (+9 more)

### Community 67 - "conftest.py"
Cohesion: 0.17
Nodes (14): Config, cli_context(), mock_console(), mock_settings(), fixture, pytest_configure(), Register custom markers used by optional live/external tests., Create a CLI runner for testing. (+6 more)

### Community 68 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Settings output must not expose the raw Hugging Face token., Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., TestCLISettings

### Community 69 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 70 - "build_endpoint_lifecycle_service"
Cohesion: 0.15
Nodes (20): test_overlay_endpoints_merges_runner_urls_immutably(), build_endpoint_lifecycle_service(), endpoints_down(), endpoints_status(), endpoints_up(), ensure_and_overlay_settings(), _handle_lifecycle_errors(), command (+12 more)

### Community 71 - "Architecture documentation index"
Cohesion: 0.22
Nodes (13): Append-only review history, Stable IDs for graph objects and exportable chunks, Layers 2–3 downstream transformation profiles, Trust state (machine/reviewed/corrected), ADR 0010: Structured Output Boundary, ADR 0008: Stable IDs and Append-Only Review History, Architecture documentation index, Spec 0005: Human Markup and Review (+5 more)

### Community 72 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.15
Nodes (13): Bundle JSON export contract, RAG JSON export contract, Raw witness artifact, ADR 0004: Raw Witness, Graph, Overlay, and Export Stay Split, Four artifact layers (raw witness, derived graph, overlay, export), Spec 0006: Exports and Retrieval Views, footnote_chunk (v1), RagDocument (+5 more)

### Community 73 - "i-mutation / i-umlaut"
Cohesion: 0.23
Nodes (13): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Lesson 0001 Sound Change and Reconstruction (+5 more)

### Community 74 - "test_cli_utils.py"
Cohesion: 0.21
Nodes (9): Tests for CLI utilities., Test info printing functions., Test basic info printing., Test info panel has correct styling., TestPrintInfo, print_info(), print_success(), Print success message. Args: message: Success message (+1 more)

### Community 75 - "main"
Cohesion: 0.23
Nodes (8): patch, Tests for the main module., Test the main function., Test that main function calls the CLI., Test that main function can be imported and called., Test that main function exists and is callable., TestMain, main()

### Community 76 - "ADR 0011: Hugging Face Endpoint Lifecycle"
Cohesion: 0.21
Nodes (14): Pass-runner common interface, EndpointLifecycleService, kraken runner, olmocr runner, Hosted inference boundary (Hugging Face endpoints only), Pass runner, wordwending Context, ADR 0011: Hugging Face Endpoint Lifecycle (+6 more)

### Community 77 - "Spec 0003: V1 Evaluation Schema"
Cohesion: 0.17
Nodes (12): Spec 0003: V1 Evaluation Schema, V1 Gold Data Expectations, Evaluation Review Flags, Evaluation Score Families, Spec 0008: Text and Normalization, Dual Diplomatic/Normalized Text, Historical Character Preservation, Retrieval Convenience Text Fields (+4 more)

### Community 78 - "Raw OCR witness layer"
Cohesion: 0.17
Nodes (12): Normalized structured export layer, Overlay correction layer, Raw OCR witness layer, Bosworth-Toller dense two-column page prep case, Page region/tile splitting for dense OCR, Two-stage text-plus-style OCR pipeline, Lesson 0006 BT Entry Structuring, Dictionary entry block as structuring unit (+4 more)

### Community 79 - "print_error"
Cohesion: 0.21
Nodes (8): Test error printing functions., Test basic error printing., Test error printing with suggestions., Test error printing without suggestions., Test error panel has correct styling., TestPrintError, print_error(), Print error message with optional suggestions. Args: message: Error message…

### Community 80 - "Image"
Cohesion: 0.07
Nodes (42): _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _column_ink_profile(), _crop_box(), _downsample_for_heuristics(), _fill_color() (+34 more)

### Community 81 - "_AssembleExecution"
Cohesion: 0.14
Nodes (16): _AssembleExecution, _bundle_ready_page(), Path, Per-run mutable assemble state and page loop. Args: adapter: Witness adaptation…, Initialize per-run assemble accumulators. Keyword Args: adapter: Witness…, Adapt, merge, and accumulate one page into run state. Args: page_request:…, Adapt every raw witness on one page with unique-id checks. Args: page_request:…, Reject duplicate ``witness_id`` within a page or across pages. Keyword Args:… (+8 more)

### Community 82 - "._coords"
Cohesion: 0.21
Nodes (6): Build one PAGE TextRegion from a canonical region record. Args: region:…, Build one PAGE TextLine from a canonical line record. Args: line: Canonical…, Convert one axis-aligned box to PAGE Coords. Args: bounding_box: Axis-aligned…, Convert one polygon to PAGE Coords. Args: polygon: Non-rectangular page…, Convert one baseline polyline to PAGE Baseline. Args: baseline: Ordered…, Serialize one PAGE coordinate as an importer-friendly integer. Args: value:…

### Community 83 - "Coordinate-Rich Kraken Adaptation Plan"
Cohesion: 0.13
Nodes (14): Coordinate-Rich Kraken Adaptation Plan, Execution Handoff, File Map, Global Constraints, Locked Decisions, Out of scope (later), Subagent Model Policy, Task 1: Fixture + structured parse unit tests (TDD) (+6 more)

### Community 84 - "create_progress"
Cohesion: 0.22
Nodes (8): Progress, Test progress creation., Test progress creation returns a Progress object., Test progress has spinner column., Test progress has text column., TestCreateProgress, create_progress(), Create a rich progress indicator for long-running operations. Returns:…

### Community 85 - "._write_page_xml"
Cohesion: 0.20
Nodes (6): Path, Merge PAGE-supported corrections into canonical sidecar data. Args:…, Serialize one bundle page to PAGE 2019-07-15 XML. Args: page: Canonical page…, Build one PAGE Word from a canonical span record. Args: span: Canonical span to…, Map supported typography facets to PAGE TextStyle. Args: typography: Canonical…, Write PAGE review ZIP and canonical JSON sidecar. Args: page: Canonical page…

### Community 86 - "Spec 0009: Merge and Alignment"
Cohesion: 0.22
Nodes (10): Layer 1 evidence-preserving OCR intermediate structure, Document bundle, Merge policy, Page bundle, Page graph (region/line/span/note), Page-local truth design principle, ADR 0002: Top-Level Artifact Is Document Bundle Per Run, Spec 0009: Merge and Alignment (+2 more)

### Community 87 - "._bbox_from_coords"
Cohesion: 0.21
Nodes (6): Merge PAGE geometry and reading order into one region record. Args: region:…, Merge PAGE geometry into one line record. Args: line: Canonical line from the…, Parse PAGE point strings into coordinate pairs. Args: points: Space-separated…, Derive one axis-aligned box from PAGE Coords. Args: coords: Optional PAGE…, Derive one polygon from PAGE Coords when enough points exist. Args: coords:…, Derive one point list from PAGE Baseline or Coords. Args: element: Optional…

### Community 88 - "_line_has_required_geometry"
Cohesion: 0.29
Nodes (7): _line_has_required_geometry(), BaseModel, Return whether a structured line meets accept rules for its type. Args: line:…, One region from a ``wordwending.kraken_segmentation/v1`` payload., One line from a ``wordwending.kraken_segmentation/v1`` payload., StructuredKrakenLine, StructuredKrakenRegion

### Community 89 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 90 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 91 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, field_validator, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…

### Community 92 - "TestCLIExport"
Cohesion: 0.25
Nodes (5): Test the export command., Export writes Spec 0006 derived artifacts under exports/., Export aborts when DocumentBundle JSON fails validation., Export requires --bundle-root., TestCLIExport

### Community 93 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 94 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 95 - "test_write_document_exports_writes_derived_views"
Cohesion: 0.50
Nodes (4): load_export_minimal_bundle(), Persisted document exports match renderer output and preserve overlays., Load the compact export-fixture DocumentBundle., test_write_document_exports_writes_derived_views()

### Community 96 - "Spec 0007: PDF-to-Image Preparation"
Cohesion: 0.33
Nodes (6): Preparation recipe, Spec 0007: PDF-to-Image Preparation, Spec 0010: Page Classification and Cohorts, PagePreparationService, Page subdivision (full-page/columns/fixed-tiles), Page class taxonomy (ordinary-prose, dense-dictionary, note-heavy, table-heavy, mixed-complex)

### Community 97 - "Python Coding Standards"
Cohesion: 0.33
Nodes (6): Python Coding Standards, Pydantic vs Dataclass vs TypedDict, Python 3.10+ Type Hints, Ruff and Mypy Linting Gate, Separation of Concerns and 60-line Methods, Sphinx Napoleon Docstrings

### Community 98 - "DocumentExportService"
Cohesion: 0.33
Nodes (6): BundleLayoutService, DocumentBundle, DocumentExportService, ExportSummary, Spec 0006 Exports and Retrieval Implementation Plan, Spec 0011 Boundary Constraint

### Community 99 - "Machine Assistance Mission"
Cohesion: 0.33
Nodes (6): Machine Assistance Mission, Dependable Machine Assistance for Old English, Machine Assistance Notes, Raw Witness Overlay Export Separation, Teaching Workspaces README, oe-grammar vs machine-assistance Split

### Community 100 - "Reference 0006 OCR Output Formats"
Cohesion: 0.33
Nodes (6): ALTO archival OCR XML, hOCR layout-bearing OCR format, Reference 0006 OCR Output Formats, PAGE XML layout-analysis format, TSV OCR output format, Tesseract OCR documentation

### Community 101 - "Prepared Page Image (page-0001)"
Cohesion: 0.53
Nodes (6): Fake PNG Placeholder Content, Hands-Off Prepare Test Fixture, Non-Decodable Raster File, Prepared Page Artifact Slot, Prepared Page Image (page-0001), Source Page page-0001

### Community 102 - "test_assemble_eval_export_wave_a_exit"
Cohesion: 0.47
Nodes (5): Path, Copy witness fixture and prepared image under ``bundle_root``., Assemble page graph scores against assemble gold, then export markdown., _stage_bundle_inputs(), test_assemble_eval_export_wave_a_exit()

### Community 103 - "TestCLIEval"
Cohesion: 0.50
Nodes (3): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., TestCLIEval

### Community 104 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 105 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 106 - "prepare_pages"
Cohesion: 0.50
Nodes (4): prepare_pages(), Acquire and prepare source pages into a reproducible output bundle. Args:…, Reject global CLI overrides when multiple recipes are requested. Args:…, _reject_multi_recipe_global_overrides()

### Community 108 - "V1 Engine Bake-Off"
Cohesion: 0.40
Nodes (5): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate

### Community 109 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.40
Nodes (5): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Normalized Page Graph, Review Overlays, V1 Typography and Role Vocabulary

### Community 110 - "Rename bochord to wordwending Implementation Plan"
Cohesion: 0.40
Nodes (5): Rename bochord to wordwending Implementation Plan, Big-bang rename on one branch, rg verification gate, Rename bochord to wordwending Design Spec, wordwending identity map

### Community 112 - "Lesson 0003 Pronouncing Old English Letters"
Cohesion: 0.40
Nodes (5): Macron recall metric, Micro-gold calibration workflow, OE fricative voicing between voiced sounds, Lesson 0003 Pronouncing Old English Letters, Four-step OE pronunciation reading routine

### Community 113 - "ADR 0009: Adapt OCR-D/PAGE and eScriptorium Boundaries"
Cohesion: 0.50
Nodes (4): eScriptorium, OCR-D, PAGE interchange, ADR 0009: Adapt OCR-D/PAGE and eScriptorium Boundaries

### Community 114 - "Phase 1 PAGE Interoperability Spike Plan"
Cohesion: 0.83
Nodes (4): BundlePage Canonical JSON, Phase 1 PAGE Interoperability Spike Plan, PageXmlInterchangeService, Reject ocrd-models for Spike

### Community 115 - "RunnerReference"
Cohesion: 0.50
Nodes (4): Mutable Model Revision Rejection, RunnerCapability, RunnerExecutionBatch, RunnerReference

### Community 116 - "TestConsole"
Cohesion: 0.50
Nodes (3): Test console objects., Test that console objects are properly initialized., TestConsole

### Community 118 - "Chris Malek"
Cohesion: 0.67
Nodes (3): AUTHORS Credits, Chris Malek, MIT License

### Community 119 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 120 - "test_live_hf_bakeoff_requires_integration_marker"
Cohesion: 0.67
Nodes (3): integration, Live HF bake-off stays behind pytest.mark.integration (not default suite)., test_live_hf_bakeoff_requires_integration_marker()

### Community 125 - "review.py"
Cohesion: 0.22
Nodes (14): command, group, option, Path, Regenerate pending review tasks from one page's evaluation flags. Args:…, Apply overlay corrections onto the page graph and write a successor overlay.…, Apply, materialize, issue, and rebase human review overlays on bundles., Append overlay review events and write materialized overlay state. Args:… (+6 more)

### Community 135 - "BundlePage"
Cohesion: 0.14
Nodes (30): _expected_evidence(), _flag(), parametrize, Return a minimal evaluation flag for queue fixtures., Return Spec 0005 evidence order with a dimension-specific item 3., test_adjudication_excludes_page_id_from_related_object_ids(), test_blank_target_object_id_routes_to_adjudication(), test_build_review_tasks_preserves_dimension_specific_coverage() (+22 more)

## Ambiguous Edges - Review These
- `i-mutation / i-umlaut` → `Ablaut (inherited vowel alternation)`  [AMBIGUOUS]
  teaching/oe-grammar/lessons/0001-sound-change-and-reconstruction.html · relation: semantically_similar_to
- `Architecture review — wordwending` → `Phase 10 Operational Hardening (NOT COMPLETE)`  [AMBIGUOUS]
  Architecture review — wordwending.html · relation: conceptually_related_to
- `Architecture review — wordwending` → `Phase 6 PassRunner Protocol (COMPLETE)`  [AMBIGUOUS]
  Architecture review — wordwending.html · relation: conceptually_related_to

## Knowledge Gaps
- **145 isolated node(s):** `release.sh script`, `wordwending`, `IPA_AUDIO`, `Locked Decisions`, `Witness content schema (lock)` (+140 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `i-mutation / i-umlaut` and `Ablaut (inherited vowel alternation)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Architecture review — wordwending` and `Phase 10 Operational Hardening (NOT COMPLETE)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Architecture review — wordwending` and `Phase 6 PassRunner Protocol (COMPLETE)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `BundlePage` connect `BundlePage` to `test_ocr_models.py`, `services/preparation.py`, `MergePolicy`, `test_merge_review.py`, `SpanRecord`, `cli.py`, `services/merge.py`, `Path`, `services/evaluation.py`, `SchemaModel`, `ReviewCliService`, `models/__init__.py`, `test_document_run.py`, `test_evaluation_service.py`, `test_text_normalization.py`, `MergeOrchestrator`, `ReviewTask`, `DocumentRunOrchestrator`, `test_assemble_manifest.py`, `test_graph_rebase.py`, `test_review_cli.py`, `PageXmlInterchangeService`, `review_cli.py`, `model_validator`, `test_page_interchange.py`, `RagChunk`, `_AssembleExecution`, `._write_page_xml`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `cli()` connect `cli` to `TestCLIReview`, `TestCLISettings`, `TestCLIGlobalOptions`, `test_assemble_eval_export_wave_a_exit`, `TestCLIEval`, `cli.py`, `SchemaModel`, `test_review_cli.py`, `_build_document_run_orchestrator`, `main`, `print_error`, `Settings`, `Path`, `TestCLIExport`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `SchemaModel` to `BundleLayoutService`, `test_ocr_models.py`, `services/preparation.py`, `MergePolicy`, `QualitySignal`, `test_merge_review.py`, `SpanRecord`, `cli.py`, `BundlePage`, `services/evaluation.py`, `models/__init__.py`, `PlannedRunnerBatch`, `test_document_run.py`, `test_evaluation_service.py`, `test_runner_execution.py`, `test_text_normalization.py`, `evaluation_cohorts.py`, `test_assemble.py`, `RunnerThroughputSummary`, `EndpointLifecycleService`, `ReviewTask`, `BundleChecksumService`, `DocumentRunOrchestrator`, `BundlePaths`, `test_graph_rebase.py`, `EndpointSessionLedgerStore`, `ResumeLedgerService`, `EndpointRemoteState`, `PreparedArtifactRef`, `EndpointCatalogEntry`, `RagChunk`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `BundlePage` (e.g. with `_FakePreparation` and `_FakeRegistry`) actually correct?**
  _`BundlePage` has 30 INFERRED edges - model-reasoned connections that need verification._