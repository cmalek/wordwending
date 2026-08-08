# Graph Report - wordwending  (2026-08-08)

## Corpus Check
- 202 files · ~250,883 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4078 nodes · 11620 edges · 163 communities (138 shown, 25 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1173 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `151e70c8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- BundleLayoutService
- test_ocr_models.py
- CoordinateSpace
- MergePolicy
- Typography
- _bundle_page_payload
- SpanRecord
- MergeOrchestrator
- TestOcrModels
- BundlePaths
- MetricProfile
- GoldPageAnnotation
- cli.py
- ReviewCliService
- test_preparation_service.py
- test_merge_review.py
- _prediction
- HuggingFaceKrakenRunner
- test_write_document_exports_frozen_contract_jsonl_validates
- test_document_run.py
- test_evaluation_service.py
- test_runner_execution.py
- Path
- PageClass
- PageEvaluationSummary
- _normalize_page_overrides
- test_olmocr_runner.py
- test_kraken_runner.py
- test_assemble.py
- models/__init__.py
- bakeoff_matrix
- OverlayState
- services/merge.py
- check_napoleon_gate.py
- From Source Material to Markdown
- BundleChecksumService
- DocumentRunOrchestrator
- TestConfiguration
- Path
- test_assemble_manifest.py
- test_graph_rebase.py
- BT Witness Preparation Slice
- EndpointSessionLedgerStore
- test_review_cli.py
- WitnessAdaptationService
- HfEndpointClient
- source_acquisition.py
- PageXmlInterchangeService
- SourceAcquisitionService
- model_validator
- test_page_interchange.py
- EndpointLifecycleService
- ResumeLedgerService
- ConfigurationError
- graph_rebase.py
- Hands-Off Operator Path Implementation Plan
- RunnerBatchPlanner
- DocumentExportService
- EndpointCatalogEntry
- valid_bundle_page
- Phase 2 Gold Evaluator Plan
- RunnerInputPackager
- Spec 0012: Runner Execution and Batch Policy
- Machine Assistance Resources
- ReviewOverlayService
- AbstainingMergeService
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
- services/preparation.py
- test_endpoint_lifecycle.py
- ._coords
- Coordinate-Rich Kraken Adaptation Plan
- create_progress
- ._write_page_xml
- Spec 0009: Merge and Alignment
- HuggingFaceOlmocrRunner
- witness_adaptation.py
- ReviewSummary
- Anglian dialect group
- .validate_https_huggingface_endpoints
- _minimal_page_overlay
- Learner lacks stable conceptual map of sound-change order
- OE Grammar Resources
- PreparedArtifactRef
- Spec 0007: PDF-to-Image Preparation
- Python Coding Standards
- DocumentExportService
- Machine Assistance Mission
- Reference 0006 OCR Output Formats
- Prepared Page Image (page-0001)
- cli
- _review_base
- TestPrintSuccess
- TestConsoleQuietMode
- DocumentRunStage
- _review_polygon
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
- ResumeLedger
- test_live_endpoint_lifecycle_smoke
- TestCLIExport
- .create_successor
- ._scored_text_pairs
- release.sh
- Contributor Covenant 3.0
- ADR 0005 Evaluation First
- Domain Language
- Worked BT entry example: abbad
- Old English c/g palatalization
- OE tēon walk-back (Grimm + h-loss + contraction)
- ipa-play.js
- _witness_skip_reason
- BundlePage
- Settings
- model_validator
- test_live_hf_bakeoff_requires_integration_marker
- _attach_alternates_to_objects
- .read_review_events
- Changelog
- Contributing
- Layered On-Disk Bundle Layout
- Update Requirements Workflow
- wordwending
- Mixed dialect spellings from copying history
- Reference Sound Terms
- .test_gold_annotation_requires_graph_or_image_anchor
- .test_model_backed_runner_requires_revision_and_digests
- .test_overlay_flag_review_event_rejects_trust_state_change
- .test_review_task_rejects_related_object_id_overlap
- .test_bounding_box_rejects_empty_or_reversed_geometry
- .__init__
- review.py
- .__init__
- .__init__

## God Nodes (most connected - your core abstractions)
1. `BundlePage` - 171 edges
2. `SchemaModel` - 134 edges
3. `AlternateCandidate` - 120 edges
4. `BundleLayoutService` - 96 edges
5. `cli()` - 94 edges
6. `MergePolicy` - 93 edges
7. `CoordinateSpace` - 93 edges
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

## Communities (163 total, 25 thin omitted)

### Community 0 - "BundleLayoutService"
Cohesion: 0.05
Nodes (85): Path, Document source digests are omitted from verification when not recorded., Prepared units without recorded digests are skipped honestly., Materialize a minimal bundle whose recorded digests match on-disk bytes., Recorded digests that match on-disk bytes report OK., Tampered prepared image bytes report FAIL against the recorded digest., _sha256_label(), test_verify_matching_checksums_ok() (+77 more)

### Community 1 - "test_ocr_models.py"
Cohesion: 0.04
Nodes (80): capability_payload(), execution_batch_payload(), _minimal_rag_document(), model_runner_payload(), parametrize, _rag_chunk(), Alternate merge interpretations live in provenance, not duplicate nodes., Return a valid model-backed runner payload with optional overrides. (+72 more)

### Community 2 - "CoordinateSpace"
Cohesion: 0.05
Nodes (94): BundlePage carries graph-v0 by default for overlay binding., test_bundle_page_defaults_graph_revision(), test_document_bundle_manifest_rejects_non_positive_page_count(), test_document_bundle_manifest_round_trip(), _FakePreparation, _FakeRegistry, _minimal_document_bundle(), Records prepare calls and seeds preparation.json under output_dir. (+86 more)

### Community 3 - "MergePolicy"
Cohesion: 0.07
Nodes (99): _aligned_text_witnesses(), _bounding_box(), _coordinate_space(), _line(), _note(), _prepared_page(), _provenance(), Empty precedence with differing text flags disagreement and abstains. (+91 more)

### Community 4 - "Typography"
Cohesion: 0.08
Nodes (37): Orthogonal visual typography facets for one text span., Typography, Collect distinct known typography signals from included spans. Args: spans:…, Report whether typography carries at least one known facet. Args: typography:…, _apply_span_text_resolution(), _first_candidate_by_runner_precedence(), Any, Collect unique witness ids from span candidates in input order. Args:… (+29 more)

### Community 5 - "_bundle_page_payload"
Cohesion: 0.12
Nodes (16): _bundle_page_payload(), Return a mutable dump of a valid bundle page with optional overrides., Graph boxes and polygons must name a known page coordinate space., Non-empty baselines require an explicit baseline coordinate space id., Baseline coordinate spaces must resolve to a known page space., Every span listed by a line must claim that line as parent., Line order values must be positive and unique within a parent region., Provenance source/witness/runner ids must belong to the owning page. (+8 more)

### Community 6 - "SpanRecord"
Cohesion: 0.05
Nodes (74): _markdown_style_page(), _object_provenance(), _page_provenance(), _page_witness(), _prepared_page(), Document export filenames stay fixed under exports/., Return valid single-page provenance for programmatic graph tests., Return provenance for one accepted page graph. (+66 more)

### Community 7 - "MergeOrchestrator"
Cohesion: 0.06
Nodes (30): _collect_span_candidates(), _first_witness_by_runner_preference(), _flagged_object_ids(), MergeOrchestrator, Gather matched span candidates from all eligible witnesses. Args:…, Return a span flagged for missing witness text evidence. Args: span: Accepted…, Per-page mutable merge state and step runner. Args: policy: Versioned merge…, Collect object ids already referenced by merge flags. Args: flags: Merge flags… (+22 more)

### Community 8 - "TestOcrModels"
Cohesion: 0.12
Nodes (9): OCR models must run on the required Hugging Face hosting boundary., Contract checks for persisted OCR schema models., Tasks must bind to the same prepared image the overlay records., Region revisions must include at least one geometry form., A review task should be actionable without undocumented context., Review tasks must bind to the prepared image the operator inspects., Related object ids must be unique., Preferred input must be one of the runner's accepted inputs. (+1 more)

### Community 9 - "BundlePaths"
Cohesion: 0.05
Nodes (58): Multiple source/pages/NNNN.* files must not silently pick one., test_page_bundle_manifest_round_trip(), test_resolve_source_image_path_rejects_ambiguous_extensions(), _page_witness(), Return a witness owned by the given page., _page_witnesses(), Return page-local witnesses matching fixture provenance., BundlePaths (+50 more)

### Community 10 - "MetricProfile"
Cohesion: 0.04
Nodes (67): test_metric_profile_rejects_invalid_iou_threshold(), MetricProfile, BaseModel, Versioned, deterministic evaluation policy., GoldRegionAnnotation, GoldStyleSpan, Gold style target for one span or image-anchored area., Gold region or structure target. (+59 more)

### Community 11 - "GoldPageAnnotation"
Cohesion: 0.09
Nodes (52): profile(), Schema defaults name real ADR 0007 candidates, not FakePassRunner., Matrix cells carry runner, page class, scores, latency, failure, license., Harness scores recorded (mocked) responses for both real candidates., Failed invocations populate failure and omit score families., Scoring exceptions become per-cell failures instead of aborting the run., Harness writes bakeoff-matrix-v1.json under the output directory., Fake invoker exercises plumbing; must not appear as a matrix candidate id. (+44 more)

### Community 12 - "cli.py"
Cohesion: 0.06
Nodes (57): argument, _build_document_run_endpoint_ensurer(), _build_document_run_orchestrator(), document_run(), _echo_checksum_results(), _echo_document_run_result(), _echo_export_paths(), _echo_page_flags() (+49 more)

### Community 13 - "ReviewCliService"
Cohesion: 0.06
Nodes (42): _bump_graph_revision(), _identity_object_id_map(), Path, ReviewEvent, Orchestrate review apply / materialize / issue / rebase for bundle pages. Keeps…, Validate an overlay, append new events, and rewrite overlay state. Args:…, Replay append-only review history into ``overlays/current_state.json``. Args:…, Rebuild pending review tasks from one page's evaluation flags. Args:… (+34 more)

### Community 14 - "test_preparation_service.py"
Cohesion: 0.08
Nodes (69): MockerFixture, test_page_override_requires_choice_and_reason(), binary_recipe(), bundle_service(), dark_gutter_image(), dense_source_page(), dense_two_column_image(), note_heavy_image() (+61 more)

### Community 15 - "test_merge_review.py"
Cohesion: 0.05
Nodes (52): _eval_flag(), _page_with_text_flags(), parametrize, Return one evaluation flag with an explicit merge flag_type., Attach evaluation flags onto the text family only (legacy C3 shape)., Known merge flag types become Spec 0005 dimension packets even if mis-bucketed., Every MergeFlagType has a Spec 0005 dimension mapping entry., Note-scoped text disagreement has no Spec 0005 text packet; use adjudication. (+44 more)

### Community 16 - "_prediction"
Cohesion: 0.21
Nodes (13): _box(), _gold(), _prediction(), Path, Build one gold page annotation matching the prediction span., Loaded prediction BundlePage.page_id must match the prediction ref., CLI/offline path loads recorded BundlePage JSON via BakeoffManifest., Thin bakeoff CLI writes matrix JSON and echoes Phase 5 NOT COMPLETE. (+5 more)

### Community 17 - "HuggingFaceKrakenRunner"
Cohesion: 0.06
Nodes (35): _encode_png_base64(), _failed_item_result(), HuggingFaceKrakenRunner, _load_direct_image(), _load_image_from_pdf(), Any, Client, Image (+27 more)

### Community 18 - "test_write_document_exports_frozen_contract_jsonl_validates"
Cohesion: 0.50
Nodes (4): load_frozen_document_bundle_v1(), Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL., Load the frozen document-bundle-v1 contract fixture., test_write_document_exports_frozen_contract_jsonl_validates()

### Community 19 - "test_document_run.py"
Cohesion: 0.10
Nodes (49): _absolute_prepare_run_config(), _full_page_preparation_json(), _make_orchestrator(), Any, Path, Write preparation.json under the prepare-tree layout., Copy provenance, merge policy, gold, and metric fixtures into directory., Build a prepare+run config with paths relative to ``config_dir``. (+41 more)

### Community 20 - "test_evaluation_service.py"
Cohesion: 0.11
Nodes (52): bold_but_not_italic_prediction(), bold_italic_gold(), _box(), note_link_gold(), _page_witnesses(), _prepared_page(), profile(), _provenance() (+44 more)

### Community 21 - "test_runner_execution.py"
Cohesion: 0.14
Nodes (39): InvokeResult, execution_service(), _fail_all_items(), _fail_second_item(), fixture_root(), hosted_result(), policy(), prepared_artifacts() (+31 more)

### Community 22 - "Path"
Cohesion: 0.07
Nodes (26): Path, inspect-bundle does not list export paths until export has run., inspect-bundle lists exports/* paths after assemble and export., inspect-bundle prints document and page summary., inspect-bundle surfaces OK after assemble seals prepared-image digests., inspect-bundle surfaces OK when layout digests match on-disk bytes., inspect-bundle prints merge flags after multi-witness disagreement., Assemble fails when manifest witness paths are absent under bundle_root. (+18 more)

### Community 23 - "PageClass"
Cohesion: 0.05
Nodes (83): test_operator_override_requires_reason(), CoordinateTransform, FlagSeverity, PageClass, PreparationMode, Page-level layout cohorts used by preparation and evaluation., Prepared-page subdivision modes., Supported top-level source kinds. (+75 more)

### Community 24 - "PageEvaluationSummary"
Cohesion: 0.10
Nodes (43): metric(), Return one metric from a family summary by id., Build one page evaluation record with a single macron_recall metric., record(), test_empty_input_returns_three_empty_lists(), test_page_class_summary_sums_metric_denominators(), test_reports_split_same_class_by_mode_and_runner(), test_zero_denominator_unit_error_aggregates_as_unit_error() (+35 more)

### Community 25 - "_normalize_page_overrides"
Cohesion: 0.50
Nodes (4): _index_page_overrides(), _normalize_page_overrides(), Index page overrides and reject duplicate or inconsistent ids. Args:…, Index page overrides by ``source_page_id``. Args: overrides: Validated page…

### Community 26 - "test_olmocr_runner.py"
Cohesion: 0.09
Nodes (49): PassRunnerClass, hosted_runner(), mock_client(), olmocr_response(), packaged_input(), planned_batch(), policy(), policy_with_endpoint() (+41 more)

### Community 27 - "test_kraken_runner.py"
Cohesion: 0.12
Nodes (43): hosted_runner(), kraken_response(), mock_client(), MockHttpxClient, planned_batch(), policy(), policy_with_endpoint(), Any (+35 more)

### Community 28 - "test_assemble.py"
Cohesion: 0.10
Nodes (51): _acquisition(), _bibliographic(), _coordinate_space(), _merge_policy(), _MergeWithExtraFlags, _orchestrator(), _prepared_page(), Path (+43 more)

### Community 29 - "models/__init__.py"
Cohesion: 0.03
Nodes (147): Enum, _event_base(), _polygon(), datetime, Return polygon-only replacement geometry., Return orthogonal typography facets for style correction., Build one overlay covering every replay assertion path. current_state is…, Replay builds OverlayState solely from ordered append-only events. (+139 more)

### Community 30 - "bakeoff_matrix"
Cohesion: 0.19
Nodes (11): bakeoff_matrix(), _ensure_catalogued_bakeoff_endpoints(), Score recorded candidate predictions into bakeoff-matrix-v1.json. Thin offline…, Ensure catalogued real bakeoff candidates and overlay HTTPS URLs. Fake / non-…, _outcome_from_prediction_ref(), Path, Write ``bakeoff-matrix-v1.json`` under ``output_dir``. Side Effects: Creates…, Load an offline bake-off request and recorded invoker from a manifest. Args:… (+3 more)

### Community 31 - "OverlayState"
Cohesion: 0.18
Nodes (10): OverlayState, Current overlay state for one reviewable object., Apply one append-only event onto a mutable overlay state. Args: state:…, Record trust, applied event id, and reviewed/corrected dimensions. Args: state:…, Apply event-specific override fields named by the event contract. Structural…, Append novel review dimensions while preserving first-seen order. Args:…, Replay ``overlay.review_events`` into per-object overlay state. Ignores any…, Append novel string ids while preserving first-seen order. Args: existing: Ids… (+2 more)

### Community 32 - "services/merge.py"
Cohesion: 0.06
Nodes (67): NamedTuple, _apply_note_link_resolution(), _apply_span_typography_resolution(), _box_iou(), _collect_note_candidates(), _detect_structure_conflict(), _geometry_alternates_for_regions(), _map_marker_span_ids() (+59 more)

### Community 33 - "check_napoleon_gate.py"
Cohesion: 0.08
Nodes (41): AsyncFunctionDef, _check_file(), _check_function_doc(), _constructor_has_args(), _first_doc_line(), _function_has_args(), _function_has_keyword_args(), _function_uses_return_or_yield() (+33 more)

### Community 34 - "From Source Material to Markdown"
Cohesion: 0.05
Nodes (43): Spec 0014: Review Task and Overlay Schema, OverlayState, PageOverlay, ReviewTask, Spec 0016: Concrete Bundle and RAG Models, DocumentBundle, PreparedPage, RagChunk (+35 more)

### Community 35 - "BundleChecksumService"
Cohesion: 0.14
Nodes (18): ChecksumVerificationResult, ChecksumVerificationStatus, StrEnum, Outcome for one recorded checksum field verified against on-disk bytes., One bundle-relative path checked against a recorded digest label., BundleChecksumService, Path, Verify prepared-page and prepared-unit digests from one page graph. Args:… (+10 more)

### Community 36 - "DocumentRunOrchestrator"
Cohesion: 0.10
Nodes (27): DocumentRunConfig, Return whether gold and metric profile enable default eval. Returns: ``True``…, Configuration for one orchestrated document run., Return the stage order for this run. Returns: Explicit ``stages`` when set;…, Return the default machine path before ``skip_export`` filtering. Returns:…, DocumentRunOrchestrator, _DocumentRunState, _load_json_model() (+19 more)

### Community 37 - "TestConfiguration"
Cohesion: 0.06
Nodes (22): Exception, patch, Unit tests for configuration settings. Tests the new OpenAI and summary…, Test that settings fields have proper descriptions., Test that model_config is properly configured., Test output format validation., Test valid output format validation., Test settings loading from environment variables. This test is a placeholder… (+14 more)

### Community 38 - "Path"
Cohesion: 0.07
Nodes (21): Path, Return the source page image path for one page number and extension. Args:…, Return the page bundle directory for one page number. Args: page_number:…, Return the page manifest path for one page number. Args: page_number: 1-based…, Return the prepared page image directory for one page number. Args:…, Return the witness artifact directory for one page and family. Args:…, Return the normalized page graph artifact path. Args: page_number: 1-based page…, Return the page evaluation scores artifact path. Args: page_number: 1-based… (+13 more)

### Community 39 - "test_assemble_manifest.py"
Cohesion: 0.11
Nodes (39): _acquisition(), _bibliographic(), _build(), _load_batch(), _merge_policy(), Path, Single succeeded run yields one page with one copied witness., Two runner runs merge into one page with two witnesses. (+31 more)

### Community 40 - "test_graph_rebase.py"
Cohesion: 0.15
Nodes (22): _page(), _provenance(), Text overrides rewrite span diplomatic text by object_id + scope., Text overrides rewrite note diplomatic text by object_id + scope., Typography and role overrides update the matching span., Unknown object_id raises ValueError naming the id., Returned page carries the caller-supplied graph_revision., Geometry, region_kind, and note linkage overrides update targets. (+14 more)

### Community 41 - "BT Witness Preparation Slice"
Cohesion: 0.06
Nodes (38): correct_text Review Event, Text Normalization Policy v1, Dual Text Contract, text-norm-v1 Policy, TextNormalizer, Append-Only Review History, BundleLayoutService, BundlePaths (+30 more)

### Community 42 - "EndpointSessionLedgerStore"
Cohesion: 0.11
Nodes (29): Path, test_corrupt_ledger_loads_empty(), test_ledger_round_trip(), test_mark_down_records_pause_action(), test_missing_ledger_loads_empty(), test_save_persists_ledger(), test_touch_rejects_invalid_action(), test_touch_replaces_same_runner_id() (+21 more)

### Community 43 - "test_review_cli.py"
Cohesion: 0.13
Nodes (33): _eval_flag(), Path, Return one evaluation flag for pending-task regeneration fixtures., Overwrite one bundle page graph artifact on disk., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends new events and materializes overlay state on disk., Apply refuses overlays whose task targets are missing from the page., Issue regenerates pending_tasks.json from the page evaluation flags. (+25 more)

### Community 44 - "WitnessAdaptationService"
Cohesion: 0.09
Nodes (52): _coordinate_space(), _prepared_page(), parametrize, Path, Two independent adapt_page calls yield identical ids and diplomatic texts. ADR…, Adapted span ids and texts match assemble gold-v1 target_object_ids., Empty artifact_paths list is rejected before reading., Non-chat.completion JSON is rejected as an invalid raw witness. (+44 more)

### Community 45 - "HfEndpointClient"
Cohesion: 0.11
Nodes (24): InferenceEndpoint, _FakeInferenceEndpoint, MonkeyPatch, test_constructor_requires_token(), test_create_omits_scale_to_zero_when_disabled(), test_create_passes_catalog_fields_and_scale_to_zero(), test_describe_maps_remote_state(), test_hub_errors_map_to_endpoint_lifecycle_error() (+16 more)

### Community 46 - "source_acquisition.py"
Cohesion: 0.09
Nodes (34): PdfPage, PdfPageImageMode, PDF page rasterization strategy during source acquisition., _artifact_from_raster(), _image_dpi(), _image_paths_in_directory(), _natural_key(), _page_ids() (+26 more)

### Community 47 - "PageXmlInterchangeService"
Cohesion: 0.11
Nodes (20): PageXmlInterchangeService, Element, Apply PAGE-supported field updates onto the canonical sidecar. Args: root:…, Return the PAGE Page element, raising when it is absent. Args: root: Parsed…, Reject PAGE corrections for a different prepared image identity. Args: page_el:…, Index TextLine and Word elements by stable id. Args: region_elements: PAGE…, Merge PAGE region geometry and reading order. Args: regions: Canonical region…, Round-trip canonical page evidence through PAGE review packages. Exports a… (+12 more)

### Community 48 - "SourceAcquisitionService"
Cohesion: 0.21
Nodes (21): pdf_fixture(), Path, Load the Phase 3 recipe fixture with optional field overrides. Keyword Args:…, Build a one-page blank PDF for acquisition tests. Args: tmp_path: Optional…, Write a tiny RGB PNG/JPEG/TIFF image to ``path``. Args: path: Destination image…, recipe(), test_image_bounds_must_overlap_most_of_page_area(), test_image_folder_records_image_set_source_type() (+13 more)

### Community 49 - "model_validator"
Cohesion: 0.04
Nodes (29): _known_page_space_ids(), _known_preparation_space_ids(), model_validator, Require baseline_coordinate_space_id exactly when baseline is present. Returns:…, Collect coordinate-space ids declared by preparation context. Args:…, Collect coordinate-space ids usable by page-graph geometry. Args:…, Reject duplicate ids and dangling page-graph references. Returns: The validated…, Require provenance pointers to stay local to the owning page. Args: provenance:… (+21 more)

### Community 50 - "test_page_interchange.py"
Cohesion: 0.10
Nodes (34): _export_note_page(), _line_unicode(), _page_element(), _parse_native_corrected(), Element, parametrize, Path, Export should round PAGE coordinates to importer-friendly integers. (+26 more)

### Community 51 - "EndpointLifecycleService"
Cohesion: 0.10
Nodes (24): ExplodingEndpointLifecycleService, Service that raises on ensure_up for fail-closed CLI tests., test_overlay_endpoints_merges_runner_urls_immutably(), EndpointLifecycleError, Raised when Hugging Face endpoint lifecycle operations fail., EndpointDownResult, EndpointEnsureResult, EndpointStatusReport (+16 more)

### Community 52 - "ResumeLedgerService"
Cohesion: 0.13
Nodes (16): Path, test_corrupt_ledger_is_treated_as_empty(), test_missing_ledger_is_empty(), test_record_completed_persists_and_reloads(), test_record_completed_replaces_same_batch_id(), _atomic_write_text(), Path, Load the on-disk ledger, returning empty on missing or corrupt data. Returns:… (+8 more)

### Community 53 - "ConfigurationError"
Cohesion: 0.07
Nodes (26): _overlay_ensure_endpoints(), Ensure runners and store an in-process Settings URL overlay on ``ctx``. Args:…, build_endpoint_lifecycle_service(), endpoints(), ensure_and_overlay_settings(), group, Ensure, pause, or inspect Hugging Face Inference Endpoints., Construct an ``EndpointLifecycleService`` from effective settings. Args:… (+18 more)

### Community 54 - "graph_rebase.py"
Cohesion: 0.26
Nodes (10): _GraphNode, _apply_leaf_overrides(), _apply_trust_and_review(), _indexes(), Copy overlay trust and review audit fields onto the target node. Args: target:…, Apply leaf override fields present on ``state`` onto ``target``. Illegible does…, Return a new page with leaf overlay overrides and a bumped revision. Structural…, Index page graph nodes by scope and stable object id. Args: page: Page whose… (+2 more)

### Community 55 - "Hands-Off Operator Path Implementation Plan"
Cohesion: 0.09
Nodes (28): DocumentRunOrchestrator Implementation Plan, DocumentRunConfig, DocumentRunOrchestrator, DocumentRunStage, Multi-runner execution run_id, Hands-Off Operator Path Implementation Plan, assemble --from-run CLI, AssembleManifestBuilder (+20 more)

### Community 56 - "RunnerBatchPlanner"
Cohesion: 0.25
Nodes (21): Return a valid runner execution policy payload with optional overrides., runner_policy_payload(), artifacts(), capability(), policy(), _prepared_unit(), Return a default multi-item runner capability with optional overrides., Return a default runner execution policy with optional overrides. (+13 more)

### Community 57 - "DocumentExportService"
Cohesion: 0.04
Nodes (49): _body_region_page(), _document_bundle(), _load_frozen_document_bundle_v1(), _load_minimal_bundle(), _merge_page_regions(), _minimal_document_bundle(), Bold+italic spans use ***text*** with bold outside italic., Notes without a parent region still appear in the Notes section. (+41 more)

### Community 58 - "EndpointCatalogEntry"
Cohesion: 0.14
Nodes (16): test_catalog_entry_rejects_mutable_revision(), test_default_catalog_includes_olmocr_and_kraken(), test_default_catalog_revisions_are_immutable(), test_mutable_revision_rejected(), test_settings_idle_and_ledger_defaults(), default_endpoint_catalog(), EndpointCatalogEntry, mutable_revision_rejected() (+8 more)

### Community 59 - "valid_bundle_page"
Cohesion: 0.18
Nodes (11): _provenance(), Return valid single-page object provenance., Existing provenance fixtures stay valid without alternate candidates., Document page ids must stay unique., Source page_count must remain exact versus exported pages., Return a minimal valid page graph for join-reference tests., test_bundle_rejects_unknown_line_join_target(), test_document_bundle_rejects_duplicate_page_ids() (+3 more)

### Community 60 - "Phase 2 Gold Evaluator Plan"
Cohesion: 0.12
Nodes (19): Phase 2 Gold Evaluator Plan, EvaluationService, GoldLineJoin, regex Unicode Grapheme Clusters, Phase 3 Acquisition Preparation Plan, PagePreparationService, Pillow and pypdfium2 Stack, SourceAcquisitionService (+11 more)

### Community 61 - "RunnerInputPackager"
Cohesion: 0.11
Nodes (30): bundle_root(), planned_batch(), fixture, Path, Build a planned batch aligned with ``prepared-inputs.json``., Create a bundle root with PNG inputs for packaging tests., test_direct_packaging_references_original_artifact(), test_direct_packaging_rejects_multi_item_batch() (+22 more)

### Community 62 - "Spec 0012: Runner Execution and Batch Policy"
Cohesion: 0.14
Nodes (17): Spec 0012: Runner Execution and Batch Policy, Batching Policy, Hugging Face Execution Boundary, Image-to-PDF Packaging, Input Packaging Policy, olmOCR V1 Execution Policy, Runner Execution Policy, Spec 0013: Pass-Runner Interface Schema (+9 more)

### Community 63 - "Machine Assistance Resources"
Cohesion: 0.13
Nodes (16): OCR Learning Goal Record, Witness-first OCR to structured data learning goal, Lesson 0004 Lossless OCR Pipeline, OCR produces evidence; structured data produces claims, Lower CER can still reduce trustworthiness via silent normalization, Review by exception, Seven-stage OCR-to-structured-data pipeline, Lesson 0005 Input Quality and Page Preparation (+8 more)

### Community 64 - "ReviewOverlayService"
Cohesion: 0.12
Nodes (16): Test review apply and materialize commands., Write a minimal Spec 0002 bundle tree under ``bundle_root``., Apply appends overlay events and materializes current_state.json., Re-applying the same overlay must not rewrite prior JSONL bytes., Materialize replays JSONL history into current_state.json., Apply fails when --page-id does not match the overlay file., Apply fails when overlay tasks reference ids absent from the page., Materialize fails when the bundle has no matching page id. (+8 more)

### Community 65 - "AbstainingMergeService"
Cohesion: 0.07
Nodes (39): _adapt_olmocr_and_kraken(), _coordinate_space(), _kraken_preferring_policy(), _olmocr_preferring_policy(), _prepared_page(), Path, Return multi-witness merge policy with kraken-first structure scaffold., Return multi-witness merge policy with olmOCR-first structure scaffold. (+31 more)

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
Cohesion: 0.07
Nodes (31): _load_cases(), _page_witnesses(), _policy_from_overrides(), _provenance(), Any, parametrize, Return valid single-page object provenance., Return page-local witnesses matching fixture provenance. (+23 more)

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

### Community 80 - "services/preparation.py"
Cohesion: 0.06
Nodes (80): AssessmentThresholds, BaseModel, QualitySignal, One measured image-quality signal from preparation assessment., Calibratable limits for deterministic image-quality heuristics., _adaptive_binary(), _apply_binarize(), _bleedthrough_signal() (+72 more)

### Community 81 - "test_endpoint_lifecycle.py"
Cohesion: 0.16
Nodes (22): _assert_is_endpoint_client(), _catalog(), FakeHfEndpointClient, Path, In-memory ``EndpointClient`` double for lifecycle unit tests., _service(), _settings(), test_down_pauses_by_default_delete_flag_destroys() (+14 more)

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
Cohesion: 0.05
Nodes (38): LookupError, _encode_png_base64(), _failed_item_result(), HuggingFaceOlmocrRunner, _load_direct_image(), _load_image_from_pdf(), Any, Client (+30 more)

### Community 88 - "witness_adaptation.py"
Cohesion: 0.09
Nodes (28): _bbox_from_xyxy(), _extract_openai_chat_completion_content(), _extract_openai_chat_completion_lines(), KrakenChatCompletionAdapter, _line_has_required_geometry(), _points_from_pairs(), _polygon_from_boundary(), BaseModel (+20 more)

### Community 89 - "ReviewSummary"
Cohesion: 0.20
Nodes (10): Aside from applied overrides and revision, the page graph is equal., test_rebase_preserves_unrelated_page_fields(), Every line listed by a region must claim that region as parent., Every note listed by a region must claim that region as parent., Region reading_order_index values must be positive and unique., test_bundle_page_rejects_line_not_owned_by_listing_region(), test_bundle_page_rejects_non_positive_or_duplicate_reading_order(), test_bundle_page_rejects_note_not_owned_by_listing_region() (+2 more)

### Community 90 - "Anglian dialect group"
Cohesion: 0.22
Nodes (9): Anglian dialect group, Kentish dialect, Mercian dialect, Northumbrian dialect, Lesson 0002 Recognizing OE Dialects, West Saxon dialect, High-value OE dialect spelling cue table, Reference OE Dialect Cues (+1 more)

### Community 91 - ".validate_https_huggingface_endpoints"
Cohesion: 0.50
Nodes (3): AnyHttpUrl, field_validator, Require HTTPS for every configured Hugging Face endpoint URL. Args: endpoints:…

### Community 92 - "_minimal_page_overlay"
Cohesion: 0.20
Nodes (8): _minimal_page_overlay(), Bundle pages store review event ids, not an embedded overlay graph., Return a minimal text-review task bound to the overlay defaults., Return a minimal page overlay with one text task and no events., Events must use the same target scope as their review task., Events must bind to the exact guideline revision shown in the task., test_bundle_page_keeps_review_overlay_as_external_references(), _text_review_task()

### Community 93 - "Learner lacks stable conceptual map of sound-change order"
Cohesion: 0.29
Nodes (7): Learner lacks stable conceptual map of sound-change order, OE Grammar Starting Point, OE Grammar Mission, Read and translate Old English with grammatical confidence, OCR and engineering workflows out of scope for OE grammar workspace, OE Grammar Notes, Do not let engineering or OCR topics bleed into OE grammar workspace

### Community 94 - "OE Grammar Resources"
Cohesion: 0.33
Nodes (6): Comparative method of reconstruction, Cognate, Reference Reconstruction Glossary, Reflex (descended later form), OE Grammar Resources, Proto-Germanic Introduction: Linguistic Methods

### Community 95 - "PreparedArtifactRef"
Cohesion: 0.04
Nodes (100): Persisted batch status must agree with submitted and failed items., Runner, overlay, and gold contracts should fit the planned workflow., MockHttpxClient, Minimal httpx client stand-in for hosted runner tests., FakeOlmocrRunner, Stub hosted runner for offline execution orchestration tests., _invoke_hosted_run(), Delegate to the wrapped service and always close the HTTP client. Args: run_id:… (+92 more)

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
Cohesion: 0.12
Nodes (19): _dense_two_column_image(), Image, patch, Test the document-run command., document-run --help exits zero and documents options., Invalid config JSON exits nonzero with a ClickException message., document-run loads config, calls orchestrator, and echoes result., --force sets force_rerun on the config passed to orchestrator.run. (+11 more)

### Community 103 - "_review_base"
Cohesion: 0.20
Nodes (6): Return fields required by every review event., Review-event schema should discriminate on ``action``., Source-triage events carry an explicit disposition and optional reason., Preparation events carry full-page or subdivide plus optional reason., Materialized state must only reference events for the same object., _review_base()

### Community 104 - "TestPrintSuccess"
Cohesion: 0.33
Nodes (4): Test success panel has correct styling., Test success printing functions., Test basic success printing., TestPrintSuccess

### Community 105 - "TestConsoleQuietMode"
Cohesion: 0.33
Nodes (4): Test console quiet mode functionality., Test that console can be set to quiet mode., Test that stderr console can be set to quiet mode., TestConsoleQuietMode

### Community 106 - "DocumentRunStage"
Cohesion: 0.10
Nodes (15): Test the eval command., Test eval writes deterministic PageEvaluationSummary JSON., Test CLI error handling., Test CLI without arguments shows help., Test invalid command shows error., Test the version command., Test the version command displays version information., Test the version command with verbose flag. (+7 more)

### Community 107 - "_review_polygon"
Cohesion: 0.29
Nodes (6): Return a valid review geometry bounding box., Return a valid review geometry polygon., Box and polygon must share one coordinate space identity., Region revisions must not mix geometry from different spaces., _review_box(), _review_polygon()

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

### Community 121 - "ResumeLedger"
Cohesion: 0.33
Nodes (6): One successfully completed runner batch recorded for resume., Persisted set of successfully completed runner batches under a bundle., ResumeLedger, ResumeLedgerEntry, datetime, Record one successfully completed batch and persist the ledger. Side Effects:…

### Community 123 - "TestCLIExport"
Cohesion: 0.25
Nodes (5): Test the export command., Export writes Spec 0006 derived artifacts under exports/., Export aborts when DocumentBundle JSON fails validation., Export requires --bundle-root., TestCLIExport

### Community 124 - ".create_successor"
Cohesion: 0.25
Nodes (7): _normalize_tasks(), Normalize a successor task map or list into a task-id dictionary. Args:…, Reject task maps that point at missing successor tasks. Args: task_id_map:…, Derive successor run, graph, and checksum from caller-supplied tasks. Args:…, Build a rebased successor overlay without mutating the predecessor. Copies only…, _require_mapped_tasks(), _successor_bindings()

### Community 134 - "_witness_skip_reason"
Cohesion: 0.33
Nodes (6): Return whether a witness coordinate space aligns with the prepared page. Args:…, Return whether every present bounding box uses the expected coordinate space.…, Return the skip reason for a witness excluded from merge eligibility. Args:…, _witness_bounding_box_spaces_match(), _witness_coordinate_space_matches(), _witness_skip_reason()

### Community 135 - "BundlePage"
Cohesion: 0.06
Nodes (55): _merge_flag(), Return one merge flag fixture., Assemble projection places each merge flag into its Spec 0005 family., Service API: MergeFlag list → ReviewTask packets via HumanMarkupService., test_project_merge_flags_routes_into_evaluation_families(), test_tasks_from_merge_flags_builds_spec_0005_packets(), _expected_evidence(), _flag() (+47 more)

### Community 136 - "Settings"
Cohesion: 0.10
Nodes (30): BaseSettings, PydanticBaseSettingsSource, configured_settings(), fake_service(), FakeEndpointLifecycleService, datetime, fixture, patch (+22 more)

### Community 137 - "model_validator"
Cohesion: 0.22
Nodes (5): model_validator, Keep tile overlap strictly smaller than tile height. Returns: The validated…, Require a non-empty reason for operator page-class overrides. Returns: The…, Require at least one override choice and a non-empty reason. Returns: The…, Require a non-empty reason for operator preparation overrides. Returns: The…

### Community 138 - "test_live_hf_bakeoff_requires_integration_marker"
Cohesion: 0.67
Nodes (3): integration, Live HF bake-off stays behind pytest.mark.integration (not default suite)., test_live_hf_bakeoff_requires_integration_marker()

### Community 139 - "_attach_alternates_to_objects"
Cohesion: 0.40
Nodes (5): _LayoutObject, _apply_layout_merge_confidence(), _attach_alternates_to_objects(), Stamp merge confidence onto accepted layout objects. Args: objects: Accepted…, Attach the same alternate payloads to every layout object. Args: objects:…

### Community 140 - ".read_review_events"
Cohesion: 0.30
Nodes (3): Any, Read append-only review events for one page. Args: root: Filesystem root for…, Serialize JSON objects as JSONL with a trailing newline when nonempty. Args:…

### Community 160 - "review.py"
Cohesion: 0.22
Nodes (14): command, group, option, Path, Regenerate pending review tasks from one page's evaluation flags. Args:…, Apply overlay corrections onto the page graph and write a successor overlay.…, Apply, materialize, issue, and rebase human review overlays on bundles., Append overlay review events and write materialized overlay state. Args:… (+6 more)

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
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `i-mutation / i-umlaut` and `Ablaut (inherited vowel alternation)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Architecture review — wordwending` and `Phase 10 Operational Hardening (NOT COMPLETE)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Architecture review — wordwending` and `Phase 6 PassRunner Protocol (COMPLETE)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `cli()` connect `cli` to `ReviewOverlayService`, `TestCLISettings`, `Settings`, `DocumentRunStage`, `GoldPageAnnotation`, `test_review_cli.py`, `cli.py`, `main`, `print_error`, `_prediction`, `TestCLIGlobalOptions`, `Path`, `test_assemble_eval_export_wave_a_exit`, `TestCLIExport`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `BundlePage` connect `BundlePage` to `test_ocr_models.py`, `CoordinateSpace`, `MergePolicy`, `SpanRecord`, `MergeOrchestrator`, `BundlePaths`, `MetricProfile`, `GoldPageAnnotation`, `cli.py`, `ReviewCliService`, `test_merge_review.py`, `_prediction`, `test_document_run.py`, `test_evaluation_service.py`, `models/__init__.py`, `services/merge.py`, `DocumentRunOrchestrator`, `test_assemble_manifest.py`, `test_graph_rebase.py`, `test_review_cli.py`, `PageXmlInterchangeService`, `model_validator`, `test_page_interchange.py`, `graph_rebase.py`, `DocumentExportService`, `valid_bundle_page`, `test_text_normalization.py`, `._write_page_xml`, `cli`, `._scored_text_pairs`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `SchemaModel` connect `models/__init__.py` to `CoordinateSpace`, `MergePolicy`, `Typography`, `SpanRecord`, `BundlePage`, `BundlePaths`, `MetricProfile`, `GoldPageAnnotation`, `test_preparation_service.py`, `test_merge_review.py`, `test_document_run.py`, `test_evaluation_service.py`, `PageClass`, `PageEvaluationSummary`, `OverlayState`, `BundleChecksumService`, `DocumentRunOrchestrator`, `test_graph_rebase.py`, `EndpointSessionLedgerStore`, `source_acquisition.py`, `EndpointLifecycleService`, `EndpointCatalogEntry`, `test_text_normalization.py`, `services/preparation.py`, `test_endpoint_lifecycle.py`, `ReviewSummary`, `PreparedArtifactRef`, `DocumentRunStage`, `ResumeLedger`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `BundlePage` (e.g. with `_FakePreparation` and `_FakeRegistry`) actually correct?**
  _`BundlePage` has 30 INFERRED edges - model-reasoned connections that need verification._