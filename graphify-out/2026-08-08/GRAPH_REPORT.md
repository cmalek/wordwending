# Graph Report - wordwending  (2026-08-08)

## Corpus Check
- 202 files · ~250,758 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4074 nodes · 11609 edges · 166 communities (144 shown, 22 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1173 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7d2587f5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_bundle_layout.py
- test_ocr_models.py
- PreparationRecipe
- MergePolicy
- ._score_text_pair
- test_merge_flag_dimension_map_is_exhaustive
- CoordinateSpace
- MergeOrchestrator
- TestOcrModels
- Path
- _RateAccumulator
- GoldPageAnnotation
- cli.py
- .apply
- test_preparation_service.py
- test_review_overlay.py
- Image
- HuggingFaceKrakenRunner
- test_write_document_exports_frozen_contract_jsonl_validates
- test_document_run.py
- test_evaluation_service.py
- test_runner_execution.py
- Path
- SourcePageArtifact
- PageClass
- services/preparation.py
- test_olmocr_runner.py
- test_kraken_runner.py
- test_assemble.py
- models/__init__.py
- _AssembleExecution
- review_overlay.py
- AlternateCandidate
- check_napoleon_gate.py
- From Source Material to Markdown
- BundleChecksumService
- PreparedArtifactRef
- TestConfiguration
- BundlePaths
- test_assemble_manifest.py
- OverlayState
- BT Witness Preparation Slice
- EndpointSessionLedgerStore
- BundleLayoutService
- WitnessAdaptationService
- ._call_hub
- source_acquisition.py
- PageXmlInterchangeService
- SourceAcquisitionService
- model_validator
- Path
- test_cli_endpoints.py
- ResumeLedgerService
- EndpointRemoteState
- Settings
- Hands-Off Operator Path Implementation Plan
- RunnerBatchPlanner
- RagChunk
- EndpointCatalogEntry
- _pixel_access
- Phase 2 Gold Evaluator Plan
- PlannedRunnerBatch
- Spec 0012: Runner Execution and Batch Policy
- Machine Assistance Resources
- TestCLIReview
- test_coordinate_rich_merge.py
- Architecture review — wordwending
- conftest.py
- TestCLISettings
- test_text_normalization.py
- endpoints_down
- Architecture documentation index
- Spec 0006: Exports and Retrieval Views
- i-mutation / i-umlaut
- test_cli_utils.py
- main
- ADR 0011: Hugging Face Endpoint Lifecycle
- Spec 0003: V1 Evaluation Schema
- Raw OCR witness layer
- print_error
- QualitySignal
- test_endpoint_lifecycle.py
- ._coords
- Coordinate-Rich Kraken Adaptation Plan
- create_progress
- ._write_page_xml
- Spec 0009: Merge and Alignment
- HuggingFaceOlmocrRunner
- .extract_segmentation
- HfEndpointClient
- Anglian dialect group
- .validate_https_huggingface_endpoints
- Path
- Learner lacks stable conceptual map of sound-change order
- Lesson 0001 Sound Change and Reconstruction
- RunnerReference
- Spec 0007: PDF-to-Image Preparation
- Python Coding Standards
- DocumentExportService
- Machine Assistance Mission
- Reference 0006 OCR Output Formats
- Prepared Page Image (page-0001)
- cli
- test_page_interchange.py
- TestPrintSuccess
- TestConsoleQuietMode
- DocumentRunStage
- BoundingBox
- V1 Engine Bake-Off
- Spec 0002: V1 Bundle Layout and Data Shape
- Rename bochord to wordwending Implementation Plan
- .validate_item_page_alignment
- Lesson 0003 Pronouncing Old English Letters
- ADR 0009: Adapt OCR-D/PAGE and eScriptorium Boundaries
- Phase 1 PAGE Interoperability Spike Plan
- RunnerReference
- TestConsole
- TestCLIGlobalOptions
- Chris Malek
- Character Error Rate (CER)
- test_assemble_eval_export_wave_a_exit
- Any
- test_live_endpoint_lifecycle_smoke
- .score
- ._resolve_context
- services/evaluation.py
- release.sh
- Contributor Covenant 3.0
- ADR 0005 Evaluation First
- Domain Language
- Worked BT entry example: abbad
- Old English c/g palatalization
- OE tēon walk-back (Grimm + h-loss + contraction)
- ipa-play.js
- _pdf_page_image
- BundlePage
- .settings_customise_sources
- model_validator
- test_live_hf_bakeoff_requires_integration_marker
- _PreparedInputsManifest
- ._require_known_ids_for_scope
- Changelog
- Contributing
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- wordwending
- Mixed dialect spellings from copying history
- Reference Sound Terms
- .write_overlay_state
- ReviewTaskType
- .append_review_events
- test_write_document_exports_writes_derived_views
- recipe_payload
- GoldLineJoin
- review
- _expected_evidence
- .__init__
- _evidence_with_witness
- .__init__
- .__init__

## God Nodes (most connected - your core abstractions)
1. `BundlePage` - 171 edges
2. `SchemaModel` - 134 edges
3. `AlternateCandidate` - 120 edges
4. `BundleLayoutService` - 96 edges
5. `cli()` - 94 edges
6. `CoordinateSpace` - 93 edges
7. `MergePolicy` - 92 edges
8. `PreparedPage` - 89 edges
9. `Settings` - 81 edges
10. `PageClass` - 80 edges

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

## Communities (166 total, 22 thin omitted)

### Community 0 - "test_bundle_layout.py"
Cohesion: 0.06
Nodes (65): _accept_review_event(), load_minimal_bundle(), Path, Duplicate page_number values must fail before silent page overwrite., source_files keys must be bare basenames, not path segments., page_exports basenames must not escape the page exports directory., Append inserts a separator when prior JSONL lacks a trailing newline., Heal must not UnicodeDecodeError when prior JSONL ends on multi-byte UTF-8. (+57 more)

### Community 1 - "test_ocr_models.py"
Cohesion: 0.02
Nodes (127): _bundle_page_payload(), capability_payload(), execution_batch_payload(), _minimal_rag_document(), model_runner_payload(), _prepared_unit_ref(), parametrize, _rag_chunk() (+119 more)

### Community 2 - "PreparationRecipe"
Cohesion: 0.08
Nodes (65): _MergeWithExtraFlags, Wrap merge and append synthetic flags for assemble projection tests., test_document_bundle_manifest_rejects_non_positive_page_count(), test_document_bundle_manifest_round_trip(), _FakePreparation, _FakeRegistry, _minimal_document_bundle(), Records prepare calls and seeds preparation.json under output_dir. (+57 more)

### Community 3 - "MergePolicy"
Cohesion: 0.07
Nodes (114): _aligned_text_witnesses(), _bounding_box(), _coordinate_space(), _line(), _load_merge_fixture(), _note(), _prepared_page(), _provenance() (+106 more)

### Community 4 - "._score_text_pair"
Cohesion: 0.13
Nodes (12): _graphemes(), _is_ligature(), _is_macron_grapheme(), _is_thorn_eth(), Return whether ``grapheme`` carries a macron in NFC or NFD form. Args:…, Return whether ``grapheme`` is thorn or eth. Args: grapheme: One NFC grapheme…, Return whether ``grapheme`` is an OE ligature under watch. Args: grapheme: One…, Score one gold/prediction pair into shared accumulators. Args: gold_span: Gold… (+4 more)

### Community 6 - "CoordinateSpace"
Cohesion: 0.03
Nodes (162): _prediction(), Build one minimal BundlePage prediction for bake-off scoring., _body_region_page(), _document_bundle(), _load_frozen_document_bundle_v1(), _load_minimal_bundle(), _markdown_style_page(), _merge_page_regions() (+154 more)

### Community 7 - "MergeOrchestrator"
Cohesion: 0.05
Nodes (33): _first_witness_by_runner_preference(), _flagged_object_ids(), MergeOrchestrator, Return a span flagged for missing witness text evidence. Args: span: Accepted…, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Initialize merge orchestration for one page. Args: policy: Versioned merge…, Collect object ids already referenced by merge flags. Args: flags: Merge flags…, Execute the Spec 0009 merge sequence for one page. Returns: Accepted page graph… (+25 more)

### Community 8 - "TestOcrModels"
Cohesion: 0.06
Nodes (24): _minimal_page_overlay(), Gold text without a graph target or geometry cannot be scored., Model-backed evidence must be reproducible., OCR models must run on the required Hugging Face hosting boundary., Return fields required by every review event., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events., Contract checks for persisted OCR schema models. (+16 more)

### Community 9 - "Path"
Cohesion: 0.05
Nodes (39): Multiple source/pages/NNNN.* files must not silently pick one., test_resolve_source_image_path_rejects_ambiguous_extensions(), _atomic_write_json(), _atomic_write_text(), _executed_passes(), Any, Path, Overwrite ``overlays/pending_tasks.json`` as a JSON list. Side Effects:… (+31 more)

### Community 10 - "_RateAccumulator"
Cohesion: 0.10
Nodes (19): _facet_match(), _RateAccumulator, Score one gold style span into facet and marker accumulators. Args: gold_span:…, Score independent typography facets into shared accumulators. Args: gold_typo:…, Score footnote-marker retention when gold carries that role. Args: gold_span:…, Emit partial collapse when weight and slant XOR-match. Fires only when both…, Score one enum typography facet when gold is known. Args: rate: Target…, Score small-caps or letter-spacing when gold is known. Args: rate: Target… (+11 more)

### Community 11 - "GoldPageAnnotation"
Cohesion: 0.06
Nodes (79): _gold(), profile(), Path, Build one gold page annotation matching the prediction span., Schema defaults name real ADR 0007 candidates, not FakePassRunner., Matrix cells carry runner, page class, scores, latency, failure, license., Harness scores recorded (mocked) responses for both real candidates., Failed invocations populate failure and omit score families. (+71 more)

### Community 12 - "cli.py"
Cohesion: 0.05
Nodes (77): argument, assemble_document(), _assemble_manifest_from_run(), bakeoff_matrix(), _build_document_run_endpoint_ensurer(), _build_document_run_orchestrator(), _build_document_run_runner_factory(), _ClientClosingRunnerExecutionService (+69 more)

### Community 13 - ".apply"
Cohesion: 0.09
Nodes (20): _bump_graph_revision(), Path, ReviewEvent, Validate an overlay, append new events, and rewrite overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, Rebuild pending review tasks from one page's evaluation flags. Args:…, Apply overlay corrections onto the page graph and write a successor overlay.…, Reject overlay submissions whose page id does not match the CLI flag. Args:… (+12 more)

### Community 14 - "test_preparation_service.py"
Cohesion: 0.10
Nodes (52): binary_recipe(), dark_gutter_image(), dense_source_page(), dense_two_column_image(), note_heavy_image(), preparation_service(), Image, MonkeyPatch (+44 more)

### Community 15 - "test_review_overlay.py"
Cohesion: 0.07
Nodes (47): Tasks must bind to the same prepared image the overlay records., _event_base(), _polygon(), datetime, MonkeyPatch, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is… (+39 more)

### Community 16 - "Image"
Cohesion: 0.11
Nodes (29): CoordinateTransform, Replayable mapping between two recorded coordinate spaces., _adaptive_binary(), _apply_binarize(), _apply_color_mode(), _apply_recipe_transforms(), _crop_box(), _downsample_for_heuristics() (+21 more)

### Community 17 - "HuggingFaceKrakenRunner"
Cohesion: 0.05
Nodes (47): LookupError, PassRunnerClass, test_default_registry_resolves_kraken_adapter(), test_default_registry_resolves_olmocr_adapter(), test_register_overrides_or_adds_runner_id(), test_resolve_unknown_runner_id_fails_clearly(), _encode_png_base64(), _failed_item_result() (+39 more)

### Community 18 - "test_write_document_exports_frozen_contract_jsonl_validates"
Cohesion: 0.50
Nodes (4): load_frozen_document_bundle_v1(), Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the frozen document-bundle-v1 contract fixture., test_write_document_exports_frozen_contract_jsonl_validates()

### Community 19 - "test_document_run.py"
Cohesion: 0.11
Nodes (47): _absolute_prepare_run_config(), _full_page_preparation_json(), _make_orchestrator(), Any, Path, Write preparation.json under the prepare-tree layout., Copy provenance, merge policy, gold, and metric fixtures into directory., Build a prepare+run config with paths relative to ``config_dir``. (+39 more)

### Community 20 - "test_evaluation_service.py"
Cohesion: 0.12
Nodes (50): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+42 more)

### Community 21 - "test_runner_execution.py"
Cohesion: 0.14
Nodes (39): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), FakeOlmocrRunner, fixture_root(), hosted_result(), policy() (+31 more)

### Community 22 - "Path"
Cohesion: 0.06
Nodes (30): Path, inspect-bundle does not list export paths until export has run., inspect-bundle lists exports/* paths after assemble and export., inspect-bundle prints document and page summary., inspect-bundle surfaces OK after assemble seals prepared-image digests., inspect-bundle surfaces OK when layout digests match on-disk bytes., inspect-bundle prints merge flags after multi-witness disagreement., Assemble fails when manifest witness paths are absent under bundle_root. (+22 more)

### Community 23 - "SourcePageArtifact"
Cohesion: 0.13
Nodes (22): One acquired source page before preparation., SourcePageArtifact, _build_assessment(), _build_preparation_result(), _build_prepared_units(), _load_source_image(), _persist_prepared_page(), _persist_recipe() (+14 more)

### Community 24 - "PageClass"
Cohesion: 0.07
Nodes (56): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+48 more)

### Community 25 - "services/preparation.py"
Cohesion: 0.11
Nodes (22): _column_ink_profile(), _column_unit_boxes(), _column_valley_centers(), _ensure_supported_recipe(), _fixed_tile_boxes(), _index_page_overrides(), _normalize_page_overrides(), Format a SHA-256 digest label for ``payload``. Args: payload: Bytes to hash.… (+14 more)

### Community 26 - "test_olmocr_runner.py"
Cohesion: 0.16
Nodes (37): hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint(), Path (+29 more)

### Community 27 - "test_kraken_runner.py"
Cohesion: 0.13
Nodes (40): hosted_runner(), kraken_response(), mock_client(), planned_batch(), policy(), policy_with_endpoint(), Any, BaseException (+32 more)

### Community 28 - "test_assemble.py"
Cohesion: 0.12
Nodes (49): _acquisition(), _bibliographic(), _coordinate_space(), _merge_policy(), _orchestrator(), _prepared_page(), Path, Return a merge policy with optional multi-runner precedence. When ``kraken`` is… (+41 more)

### Community 29 - "models/__init__.py"
Cohesion: 0.04
Nodes (83): Enum, BundleChecksumReport, ChecksumVerificationStatus, StrEnum, Outcome for one recorded checksum field verified against on-disk bytes., Aggregate checksum verification results for one bundle root., Return whether every non-skipped verification succeeded. Returns: ``True`` when…, AcceptReviewEvent (+75 more)

### Community 30 - "_AssembleExecution"
Cohesion: 0.14
Nodes (16): _AssembleExecution, _bundle_ready_page(), Path, Per-run mutable assemble state and page loop. Args: adapter: Witness adaptation…, Initialize per-run assemble accumulators. Keyword Args: adapter: Witness…, Adapt, merge, and accumulate one page into run state. Args: page_request:…, Adapt every raw witness on one page with unique-id checks. Args: page_request:…, Reject duplicate ``witness_id`` within a page or across pages. Keyword Args:… (+8 more)

### Community 31 - "review_overlay.py"
Cohesion: 0.07
Nodes (33): Complete replayable structural definition for a corrected region., RegionRevision, _identity_object_id_map(), Build an ADR 0008 successor overlay bound to ``new_graph_revision``. Leaf-only…, Build an identity object-id map for leaf-only graph rebase. Args: page: Rebased…, _coordinate_space_ids(), _nested_object_ids(), _normalize_tasks() (+25 more)

### Community 32 - "AlternateCandidate"
Cohesion: 0.04
Nodes (113): _LayoutObject, NamedTuple, AlternateCandidate, One rejected or alternate merge interpretation kept in provenance., Semantic role kept separate from visual typography., TextRole, _apply_layout_merge_confidence(), _apply_note_link_resolution() (+105 more)

### Community 33 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 34 - "From Source Material to Markdown"
Cohesion: 0.05
Nodes (43): Spec 0014: Review Task and Overlay Schema, OverlayState, PageOverlay, ReviewTask, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle, PreparedPage, RagChunk (+35 more)

### Community 35 - "BundleChecksumService"
Cohesion: 0.10
Nodes (27): Path, Document source digests are omitted from verification when not recorded., Prepared units without recorded digests are skipped honestly., Materialize a minimal bundle whose recorded digests match on-disk bytes., Recorded digests that match on-disk bytes report OK., Tampered prepared image bytes report FAIL against the recorded digest., _sha256_label(), test_verify_matching_checksums_ok() (+19 more)

### Community 36 - "PreparedArtifactRef"
Cohesion: 0.12
Nodes (29): DocumentRunConfig, Configuration for one orchestrated document run., PreparedArtifactRef, Prepared image or packaged artifact ready for runner execution., _artifacts_from_preparation_result(), DocumentRunOrchestrator, _DocumentRunState, _load_json_model() (+21 more)

### Community 37 - "TestConfiguration"
Cohesion: 0.06
Nodes (22): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+14 more)

### Community 38 - "BundlePaths"
Cohesion: 0.08
Nodes (25): test_bundle_paths_match_spec_0002_layout(), test_source_page_image_rejects_empty_extension(), BundlePaths, Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:… (+17 more)

### Community 39 - "test_assemble_manifest.py"
Cohesion: 0.10
Nodes (41): _acquisition(), _bibliographic(), _build(), _load_batch(), _merge_policy(), Path, BundlePage carries graph-v0 by default for overlay binding., Single succeeded run yields one page with one copied witness. (+33 more)

### Community 40 - "OverlayState"
Cohesion: 0.08
Nodes (32): _GraphNode, Text overrides rewrite span diplomatic text by object_id + scope., Text overrides rewrite note diplomatic text by object_id + scope., Unknown object_id raises ValueError naming the id., Returned page carries the caller-supplied graph_revision., Aside from applied overrides and revision, the page graph is equal., Illegible applies trust/review only; text and BundlePage stay field-stable., test_rebase_applies_note_text_diplomatic_override() (+24 more)

### Community 41 - "BT Witness Preparation Slice"
Cohesion: 0.06
Nodes (38): correct_text Review Event, Text Normalization Policy v1, Dual Text Contract, text-norm-v1 Policy, TextNormalizer, Append-Only Review History, BundleLayoutService, BundlePaths (+30 more)

### Community 42 - "EndpointSessionLedgerStore"
Cohesion: 0.12
Nodes (23): Path, test_corrupt_ledger_loads_empty(), test_ledger_round_trip(), test_mark_down_records_pause_action(), test_missing_ledger_loads_empty(), test_save_persists_ledger(), test_touch_rejects_invalid_action(), test_touch_replaces_same_runner_id() (+15 more)

### Community 43 - "BundleLayoutService"
Cohesion: 0.08
Nodes (65): _eval_flag(), _gold_task(), _overlay_with_tasks(), Path, Return a span-scoped text review task for validation fixtures., Return a gold task packet (unsupported by review apply)., Return a minimal PageOverlay carrying the given review tasks., Return one evaluation flag for pending-task regeneration fixtures. (+57 more)

### Community 44 - "WitnessAdaptationService"
Cohesion: 0.11
Nodes (46): _coordinate_space(), _prepared_page(), parametrize, Path, Two independent adapt_page calls yield identical ids and diplomatic texts. ADR…, Adapted span ids and texts match assemble gold-v1 target_object_ids., Empty artifact_paths list is rejected before reading., Non-chat.completion JSON is rejected as an invalid raw witness. (+38 more)

### Community 45 - "._call_hub"
Cohesion: 0.13
Nodes (11): InferenceEndpoint, Any, Return the remote endpoint snapshot. Args: name: Inference Endpoint name in the…, Create one catalogued endpoint. Args: entry: Catalog pin describing the…, Resume one paused endpoint. Args: name: Inference Endpoint name in the hosting…, Pause one running endpoint. Args: name: Inference Endpoint name in the hosting…, Scale one endpoint to zero replicas. Args: name: Inference Endpoint name in the…, Delete one remote endpoint. Args: name: Inference Endpoint name in the hosting… (+3 more)

### Community 46 - "source_acquisition.py"
Cohesion: 0.11
Nodes (26): Print the some version info of this package,, version(), _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids(), Path (+18 more)

### Community 47 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 48 - "SourceAcquisitionService"
Cohesion: 0.26
Nodes (18): pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe(), test_image_folder_records_image_set_source_type(), test_image_folder_uses_natural_page_order() (+10 more)

### Community 49 - "model_validator"
Cohesion: 0.04
Nodes (27): _known_page_space_ids(), _known_preparation_space_ids(), model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Require provenance pointers to stay local to the owning page. Args: provenance:… (+19 more)

### Community 50 - "Path"
Cohesion: 0.13
Nodes (19): _export_note_page(), Path, Export should round PAGE coordinates to importer-friendly integers., PAGE corrections should update text while sidecar evidence stays intact., PAGE diplomatic corrections should regenerate normalized span text., Import should fail when PAGE XML drops a canonical region id., Import should fail when PAGE XML repeats a canonical line id., Import should fail when corrected PAGE points at a different image identity. (+11 more)

### Community 51 - "test_cli_endpoints.py"
Cohesion: 0.06
Nodes (45): configured_settings(), ExplodingEndpointLifecycleService, fake_service(), FakeEndpointLifecycleService, datetime, fixture, Path, ``bakeoff --ensure-endpoints`` aborts when lifecycle ensure fails. (+37 more)

### Community 52 - "ResumeLedgerService"
Cohesion: 0.11
Nodes (22): Path, test_corrupt_ledger_is_treated_as_empty(), test_missing_ledger_is_empty(), test_record_completed_persists_and_reloads(), test_record_completed_replaces_same_batch_id(), One successfully completed runner batch recorded for resume., Persisted set of successfully completed runner batches under a bundle., ResumeLedger (+14 more)

### Community 53 - "EndpointRemoteState"
Cohesion: 0.10
Nodes (15): FakeHfEndpointClient, In-memory ``EndpointClient`` double for lifecycle unit tests., test_fake_satisfies_endpoint_client_protocol(), EndpointRemoteState, Remote Inference Endpoint snapshot from Hugging Face Hub., EndpointClient, Protocol, Scale one endpoint to zero replicas. Args: name: Inference Endpoint name in the… (+7 more)

### Community 54 - "Settings"
Cohesion: 0.15
Nodes (19): patch, Test the eval command., Test CLI error handling., Test the run command., _run_cli_args(), _runner_reference_json(), test_eval_cohorts_writes_all_fixed_views(), TestCLIErrorHandling (+11 more)

### Community 55 - "Hands-Off Operator Path Implementation Plan"
Cohesion: 0.09
Nodes (28): DocumentRunOrchestrator Implementation Plan, DocumentRunConfig, DocumentRunOrchestrator, DocumentRunStage, Multi-runner execution run_id, Hands-Off Operator Path Implementation Plan, assemble --from-run CLI, AssembleManifestBuilder (+20 more)

### Community 56 - "RunnerBatchPlanner"
Cohesion: 0.14
Nodes (28): Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), test_endpoint_policy_rejects_estimate_above_run_cap(), artifacts(), capability(), policy(), _prepared_unit(), Return a default multi-item runner capability with optional overrides. (+20 more)

### Community 57 - "RagChunk"
Cohesion: 0.09
Nodes (14): RagChunk, Page-local retrieval chunk., Render an evidence-preserving Markdown reading view from accepted graphs. Args:…, Map linked marker span ids to owning note ids for one page. Args: page:…, Escape Markdown control characters in diplomatic text. Args: text: Raw…, Render one non-body region as an explicit labeled placeholder. Args: region:…, Build cross-page stitched chunks from contiguous BODY region runs. Args:…, Emit one stitched chunk when a BODY run spans multiple pages. Args:… (+6 more)

### Community 58 - "EndpointCatalogEntry"
Cohesion: 0.15
Nodes (15): test_catalog_entry_rejects_mutable_revision(), test_default_catalog_includes_olmocr_and_kraken(), test_default_catalog_revisions_are_immutable(), test_mutable_revision_rejected(), test_settings_idle_and_ledger_defaults(), default_endpoint_catalog(), EndpointCatalogEntry, mutable_revision_rejected() (+7 more)

### Community 59 - "_pixel_access"
Cohesion: 0.12
Nodes (19): _longest_dark_run(), _median_text_height_signal(), _pixel_access(), Any, Return Pillow pixel access for ``image``. Args: image: Image whose pixels will…, Warn when ``value`` falls below ``minimum``. Args: value: Measured value.…, Mark rows that contain enough ink to count as text. Args: gray: Grayscale…, Collect lengths of contiguous ``True`` runs. Args: mask: Boolean sequence.… (+11 more)

### Community 60 - "Phase 2 Gold Evaluator Plan"
Cohesion: 0.12
Nodes (19): Phase 2 Gold Evaluator Plan, EvaluationService, GoldLineJoin, regex Unicode Grapheme Clusters, Phase 3 Acquisition Preparation Plan, PagePreparationService, Pillow and pypdfium2 Stack, SourceAcquisitionService (+11 more)

### Community 61 - "PlannedRunnerBatch"
Cohesion: 0.08
Nodes (44): bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests., test_direct_packaging_references_original_artifact(), test_direct_packaging_rejects_multi_item_batch() (+36 more)

### Community 62 - "Spec 0012: Runner Execution and Batch Policy"
Cohesion: 0.14
Nodes (17): Spec 0012: Runner Execution and Batch Policy, Batching Policy, Hugging Face Execution Boundary, Image-to-PDF Packaging, Input Packaging Policy, olmOCR V1 Execution Policy, Runner Execution Policy, Spec 0013: Pass-Runner Interface Schema (+9 more)

### Community 63 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 64 - "TestCLIReview"
Cohesion: 0.17
Nodes (9): Test review apply and materialize commands., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends overlay events and materializes current_state.json., Re-applying the same overlay must not rewrite prior JSONL bytes., Materialize replays JSONL history into current_state.json., Apply fails when --page-id does not match the overlay file., Apply fails when overlay tasks reference ids absent from the page., Materialize fails when the bundle has no matching page id. (+1 more)

### Community 65 - "test_coordinate_rich_merge.py"
Cohesion: 0.17
Nodes (17): _adapt_olmocr_and_kraken(), _coordinate_space(), _kraken_preferring_policy(), _prepared_page(), Path, Return multi-witness merge policy with kraken-first structure scaffold., Structured kraken lines carry geometry; provisional olmOCR lines do not., Merge with kraken-first scaffold accepts distinct kraken line boxes. (+9 more)

### Community 66 - "Architecture review — wordwending"
Cohesion: 0.18
Nodes (17): acquire → prepare → run passes → align → evaluate → review → export, AssembleOrchestrator, DocumentRunOrchestrator, MergeOrchestrator, RunnerExecutionOrchestrator, Missing E2E seam (raw witness → PassWitnessPage → merge → bundle), PassWitnessPage adapter seam, Architecture review — wordwending (+9 more)

### Community 67 - "conftest.py"
Cohesion: 0.17
Nodes (14): Config, cli_context(), mock_console(), mock_settings(), fixture, pytest_configure(), Register custom markers used by optional live/external tests., Create a CLI runner for testing. (+6 more)

### Community 68 - "TestCLISettings"
Cohesion: 0.14
Nodes (8): Settings output must not expose the raw Hugging Face token., Test the settings command., Test the settings command with table output., Test the settings command with JSON output., Test the settings command with text output., Test the settings command with verbose flag., Test the settings command with custom config file., TestCLISettings

### Community 69 - "test_text_normalization.py"
Cohesion: 0.06
Nodes (44): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+36 more)

### Community 70 - "endpoints_down"
Cohesion: 0.26
Nodes (14): endpoints_down(), endpoints_status(), endpoints_up(), _handle_lifecycle_errors(), command, Context, option, pass_context (+6 more)

### Community 71 - "Architecture documentation index"
Cohesion: 0.22
Nodes (13): Append-only review history, Stable IDs for graph objects and exportable chunks, Layers 2–3 downstream transformation profiles, Trust state (machine/reviewed/corrected), ADR 0010: Structured Output Boundary, ADR 0008: Stable IDs and Append-Only Review History, Architecture documentation index, Spec 0005: Human Markup and Review (+5 more)

### Community 72 - "Spec 0006: Exports and Retrieval Views"
Cohesion: 0.15
Nodes (13): Bundle JSON export contract, RAG JSON export contract, Raw witness artifact, ADR 0004: Raw Witness, Graph, Overlay, and Export Stay Split, Four artifact layers (raw witness, derived graph, overlay, export), Spec 0006: Exports and Retrieval Views, footnote_chunk (v1), RagDocument (+5 more)

### Community 73 - "i-mutation / i-umlaut"
Cohesion: 0.25
Nodes (11): Ablaut (inherited vowel alternation), OE fæder walk-back (Grimm + Verner), OE fōt walk-back (Grimm + ablaut + i-mutation), Grimm's Law, i-mutation / i-umlaut, Proto-Germanic, Proto-Indo-European, Verner's Law (+3 more)

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

### Community 80 - "QualitySignal"
Cohesion: 0.11
Nodes (34): AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _bleedthrough_signal(), _border_shadow_signal(), _colored_marking_signal() (+26 more)

### Community 81 - "test_endpoint_lifecycle.py"
Cohesion: 0.30
Nodes (17): _assert_is_endpoint_client(), _catalog(), Path, _service(), _settings(), test_down_pauses_by_default_delete_flag_destroys(), test_ensure_up_already_running_skips_create_and_resume(), test_ensure_up_creates_missing_and_returns_https_url() (+9 more)

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

### Community 87 - "HuggingFaceOlmocrRunner"
Cohesion: 0.06
Nodes (33): _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _load_direct_image(), _load_image_from_pdf(), Any, Image, Path (+25 more)

### Community 88 - ".extract_segmentation"
Cohesion: 0.09
Nodes (22): _extract_openai_chat_completion_content(), _extract_openai_chat_completion_lines(), KrakenChatCompletionAdapter, _line_has_required_geometry(), OlmocrChatCompletionAdapter, BaseModel, Split assistant content into diplomatic text lines. Args: content: Assistant…, Extract newline-split assistant content from chat.completion bytes. Args:… (+14 more)

### Community 89 - "HfEndpointClient"
Cohesion: 0.25
Nodes (14): _FakeInferenceEndpoint, MonkeyPatch, test_constructor_requires_token(), test_create_omits_scale_to_zero_when_disabled(), test_create_passes_catalog_fields_and_scale_to_zero(), test_describe_maps_remote_state(), test_hub_errors_map_to_endpoint_lifecycle_error(), test_inference_endpoint_error_maps_to_lifecycle_error() (+6 more)

### Community 90 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 91 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, field_validator, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…

### Community 92 - "Path"
Cohesion: 0.22
Nodes (16): MockerFixture, bundle_service(), Path, Write a single-page source raster for bundle tests. Returns: Path to a…, Write a two-page image folder for multi-page bundle tests. Returns: Path to a…, Build a preparation bundle service wired to ``acquisition``. Args: acquisition:…, source_image(), test_only_target_page_is_forced() (+8 more)

### Community 93 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 94 - "Lesson 0001 Sound Change and Reconstruction"
Cohesion: 0.29
Nodes (8): Comparative method of reconstruction, Lesson 0001 Sound Change and Reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods, Lehmann A Grammar of Proto-Germanic

### Community 95 - "RunnerReference"
Cohesion: 0.07
Nodes (58): MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., Persisted batch status must agree with submitted and failed items., Runner, overlay, and gold contracts should fit the planned workflow., test_packaged_runner_input_rejects_mismatched_item_page_lengths(), test_runner_reference_accepts_immutable_digest_revision(), MockHttpxClient, Minimal httpx client stand-in for hosted runner tests. (+50 more)

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

### Community 102 - "cli"
Cohesion: 0.08
Nodes (25): _dense_two_column_image(), Image, Test the document-run command., document-run --help exits zero and documents options., Invalid config JSON exits nonzero with a ClickException message., document-run loads config, calls orchestrator, and echoes result., --force sets force_rerun on the config passed to orchestrator.run., Test eval writes deterministic PageEvaluationSummary JSON. (+17 more)

### Community 103 - "test_page_interchange.py"
Cohesion: 0.21
Nodes (15): _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Return the root element of one recorded eScriptorium PAGE export., Recorded native exports keep region/line ids and line-level corrections., Native eScriptorium PAGE export drops Word elements and span-* ids. (+7 more)

### Community 104 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 105 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 106 - "DocumentRunStage"
Cohesion: 0.12
Nodes (11): Test the version command., Test the version command displays version information., Test the version command with verbose flag., Test the version command with quiet flag., TestCLIVersion, DocumentRunStage, StrEnum, Return whether gold and metric profile enable default eval. Returns: ``True``… (+3 more)

### Community 107 - "BoundingBox"
Cohesion: 0.11
Nodes (21): _box(), Build one axis-aligned box in the fixture prepared-page space., Geometry, region_kind, and note linkage overrides update targets., test_rebase_applies_geometry_region_kind_and_note_links(), Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces. (+13 more)

### Community 108 - "V1 Engine Bake-Off"
Cohesion: 0.40
Nodes (5): ADR 0007 V1 Engine Strategy, V1 Engine Bake-Off, Hugging Face Hosted Endpoints, kraken Candidate, olmocr Candidate

### Community 109 - "Spec 0002: V1 Bundle Layout and Data Shape"
Cohesion: 0.40
Nodes (5): Spec 0002: V1 Bundle Layout and Data Shape, Document Bundle Layout, Normalized Page Graph, Review Overlays, V1 Typography and Role Vocabulary

### Community 110 - "Rename bochord to wordwending Implementation Plan"
Cohesion: 0.40
Nodes (5): Rename bochord to wordwending Implementation Plan, Big-bang rename on one branch, rg verification gate, Rename bochord to wordwending Design Spec, wordwending identity map

### Community 111 - ".validate_item_page_alignment"
Cohesion: 0.29
Nodes (4): model_validator, Require one page number for every packaged batch item. Returns: The validated…, Keep failure counts and derived throughput internally coherent. Returns: The…, Reject endpoint estimates that exceed the configured run cost cap. Returns: The…

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

### Community 117 - "TestCLIGlobalOptions"
Cohesion: 0.14
Nodes (8): Test global CLI options., Test verbose flag is properly set., Test quiet flag is properly set., Test default output format is table., Test JSON output format., Test text output format., Test invalid output format., TestCLIGlobalOptions

### Community 118 - "Chris Malek"
Cohesion: 0.67
Nodes (3): AUTHORS Credits, Chris Malek, MIT License

### Community 119 - "Character Error Rate (CER)"
Cohesion: 0.67
Nodes (3): Five-layer philology-aware metric stack, Character Error Rate (CER), Word Error Rate (WER)

### Community 120 - "test_assemble_eval_export_wave_a_exit"
Cohesion: 0.47
Nodes (5): Path, Copy witness fixture and prepared image under ``bundle_root``., Assemble page graph scores against assemble gold, then export markdown., _stage_bundle_inputs(), test_assemble_eval_export_wave_a_exit()

### Community 121 - "Any"
Cohesion: 0.47
Nodes (3): Any, BaseException, Response

### Community 123 - ".score"
Cohesion: 0.23
Nodes (7): Score structure metrics and provenance-backed structure flags. Covers region…, Aggregate region, order, join, and table metrics for one page. Args:…, Resolve scored gold regions under exhaustive STRUCTURE coverage. Args:…, Score adjacent gold reading-order pairs among covered regions. Args: matches:…, Score each non-excluded gold join against ``joins_to_line_id``. Semantics: when…, Emit provenance-backed flags for one matched region. Args: region: Matched…, _StructureScorer

### Community 124 - "._resolve_context"
Cohesion: 0.18
Nodes (10): _choose_preparation_mode(), Suggest a page class using the fixed priority heuristics. Args: signals:…, Read one signal value by id. Args: by_id: Signals indexed by ``signal_id``.…, Resolve assessment, class, and subdivision choices for one page. Args:…, Resolve final page class from automation or operator override. Args: suggested:…, Resolve subdivision mode from automation or operator override. Args:…, Choose subdivision mode from page class and quality signals. Args: page_class:…, _resolve_page_class() (+2 more)

### Community 125 - "services/evaluation.py"
Cohesion: 0.11
Nodes (24): AnchoredGoldAnnotation, GoldRegionAnnotation, GoldStyleSpan, GoldTextSpan, Gold annotation that resolves to graph evidence or prepared image geometry., Gold diplomatic and normalized text target., Gold style target for one span or image-anchored area., Gold region or structure target. (+16 more)

### Community 134 - "_pdf_page_image"
Cohesion: 0.25
Nodes (11): PdfPage, test_image_bounds_must_overlap_most_of_page_area(), _image_bounds_cover_page(), _pdf_page_image(), Image, Choose extract-or-render for one PDF page per ``recipe``. Args: page: Open…, Extract a full-page embedded raster when acquisition rules allow. Args: page:…, Check whether displayed image bounds cover enough of page bounds. Args: left:… (+3 more)

### Community 135 - "BundlePage"
Cohesion: 0.05
Nodes (86): _eval_flag(), _merge_flag(), _page_with_text_flags(), parametrize, Return one merge flag fixture., Return one evaluation flag with an explicit merge flag_type., Attach evaluation flags onto the text family only (legacy C3 shape)., Known merge flag types become Spec 0005 dimension packets even if mis-bucketed. (+78 more)

### Community 136 - ".settings_customise_sources"
Cohesion: 0.22
Nodes (6): BaseSettings, PydanticBaseSettingsSource, Path, Load settings from file with cascading configuration. Args: settings_cls:…, Resolve the endpoint session ledger path. Returns: Configured ledger path or…, Get list of configuration file paths that were loaded. Use this for debugging.…

### Community 137 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 138 - "test_live_hf_bakeoff_requires_integration_marker"
Cohesion: 0.67
Nodes (3): integration, Live HF bake-off stays behind pytest.mark.integration (not default suite)., test_live_hf_bakeoff_requires_integration_marker()

### Community 139 - "_PreparedInputsManifest"
Cohesion: 0.67
Nodes (3): _PreparedInputsManifest, BaseModel, Prepared artifact manifest accepted by ``wordwending run``.

### Community 140 - "._require_known_ids_for_scope"
Cohesion: 0.29
Nodes (4): Ensure overlay task targets exist on the accepted page graph. Validation is…, Validate one review task's targets against the page graph. Args: page: Accepted…, Validate task target ids against the page graph for one review scope. Args:…, Reject empty or unknown object identifiers for a review task. Args: object_ids:…

### Community 154 - ".write_overlay_state"
Cohesion: 0.29
Nodes (6): test_page_dir_name_is_zero_padded(), page_dir_name(), Return the stable page directory name for one 1-based page number. Args:…, Atomically rewrite one page manifest. Side Effects: Replaces ``pages/page-…, Overwrite ``overlays/current_state.json`` deterministically. Side Effects:…, _rewrite_page_manifest()

### Community 155 - "ReviewTaskType"
Cohesion: 0.33
Nodes (4): HumanMarkupService task types must certify only their exclusive dimension., Operator workflow represented by a review task packet., ReviewTaskType, Build a deterministic task id from page, type, and target ids. Identity is…

### Community 156 - ".append_review_events"
Cohesion: 0.40
Nodes (4): _needs_trailing_newline(), ReviewEvent, r""" Return True when ``path`` exists, is non-empty, and does not end with…, Append JSONL review events; never rewrite prior lines. Side Effects:…

### Community 157 - "test_write_document_exports_writes_derived_views"
Cohesion: 0.50
Nodes (4): load_export_minimal_bundle(), Persisted document exports match renderer output and preserve overlays., Load the compact export-fixture DocumentBundle., test_write_document_exports_writes_derived_views()

### Community 158 - "recipe_payload"
Cohesion: 0.67
Nodes (3): Return a valid preparation-recipe payload with optional overrides., recipe_payload(), test_recipe_rejects_overlap_not_smaller_than_tile()

### Community 159 - "GoldLineJoin"
Cohesion: 0.67
Nodes (3): test_excluded_line_join_requires_reason(), GoldLineJoin, Gold line-join annotation for hyphenation and continuation decisions.

### Community 160 - "review"
Cohesion: 0.67
Nodes (3): group, Apply, materialize, issue, and rebase human review overlays on bundles., review()

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
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `i-mutation / i-umlaut` and `Ablaut (inherited vowel alternation)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Architecture review — wordwending` and `Phase 10 Operational Hardening (NOT COMPLETE)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Architecture review — wordwending` and `Phase 6 PassRunner Protocol (COMPLETE)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `cli()` connect `cli` to `TestCLIReview`, `TestCLISettings`, `DocumentRunStage`, `GoldPageAnnotation`, `BundleLayoutService`, `cli.py`, `main`, `print_error`, `test_cli_endpoints.py`, `TestCLIGlobalOptions`, `Settings`, `Path`, `test_assemble_eval_export_wave_a_exit`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `BundlePage` connect `BundlePage` to `test_ocr_models.py`, `PreparationRecipe`, `MergePolicy`, `CoordinateSpace`, `MergeOrchestrator`, `Path`, `_RateAccumulator`, `GoldPageAnnotation`, `cli.py`, `._require_known_ids_for_scope`, `.apply`, `test_review_overlay.py`, `test_document_run.py`, `test_evaluation_service.py`, `PageClass`, `models/__init__.py`, `_AssembleExecution`, `review_overlay.py`, `AlternateCandidate`, `PreparedArtifactRef`, `test_assemble_manifest.py`, `OverlayState`, `BundleLayoutService`, `PageXmlInterchangeService`, `model_validator`, `RagChunk`, `test_text_normalization.py`, `._write_page_xml`, `test_page_interchange.py`, `.score`, `services/evaluation.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `test_bundle_layout.py`, `test_ocr_models.py`, `PreparationRecipe`, `MergePolicy`, `CoordinateSpace`, `BundlePage`, `GoldPageAnnotation`, `test_review_overlay.py`, `Image`, `test_document_run.py`, `test_evaluation_service.py`, `test_runner_execution.py`, `SourcePageArtifact`, `PageClass`, `GoldLineJoin`, `AlternateCandidate`, `review_overlay.py`, `BundleChecksumService`, `PreparedArtifactRef`, `BundlePaths`, `OverlayState`, `EndpointSessionLedgerStore`, `test_cli_endpoints.py`, `ResumeLedgerService`, `EndpointRemoteState`, `Settings`, `RagChunk`, `EndpointCatalogEntry`, `PlannedRunnerBatch`, `test_text_normalization.py`, `QualitySignal`, `RunnerReference`, `DocumentRunStage`, `BoundingBox`, `services/evaluation.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `BundlePage` (e.g. with `_FakePreparation` and `_FakeRegistry`) actually correct?**
  _`BundlePage` has 30 INFERRED edges - model-reasoned connections that need verification._