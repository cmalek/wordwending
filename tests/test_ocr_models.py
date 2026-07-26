# Copyright (C) 2026 Chris Malek.
"""Tests for the canonical OCR schema models."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import TypeAdapter, ValidationError

from bochord.models import (
    AcquisitionProvenance,
    BaselineShift,
    BatchItemRef,
    BatchResultStatus,
    BatchUnitKind,
    BibliographicProvenance,
    BoundingBox,
    BundlePage,
    ChunkType,
    CoordinateSpace,
    DocumentBundle,
    DocumentEvaluationSummary,
    EvaluationFamilySummary,
    ExportSummary,
    FontSlant,
    FontWeight,
    GoldCoverage,
    GoldDocument,
    GoldLineJoin,
    GoldPageAnnotation,
    GoldTextSpan,
    InputKind,
    LineRecord,
    LinkNoteReviewEvent,
    MetricProfile,
    ObjectProvenance,
    OverlayState,
    PackagingStrategy,
    PageClass,
    PageEvaluationSummary,
    PageOverlay,
    PreparationMode,
    PreparedArtifactRef,
    PreparedPage,
    RagChunk,
    RagDocument,
    RegionKind,
    RegionRecord,
    RetrievalProvenance,
    ReviewDimension,
    ReviewEvent,
    ReviewScope,
    ReviewSummary,
    ReviewTask,
    ReviewTaskStatus,
    ReviewTaskType,
    RunMetadata,
    RunnerCapability,
    RunnerExecutionBatch,
    RunnerOutputArtifact,
    RunnerReference,
    SourceDescriptor,
    SourceType,
    SpanRecord,
    TextRole,
    TrustState,
    Typography,
)


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        machine_confidence=0.91,
        merge_confidence=0.84,
    )


def valid_bundle_page() -> BundlePage:
    """Return a minimal valid page graph for join-reference tests."""
    provenance = _provenance()
    return BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=PreparedPage(
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
            coordinate_space=CoordinateSpace(
                space_id="prepared-page-1",
                width_px=100,
                height_px=100,
            ),
        ),
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1", "line-2"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
                provenance=provenance,
            ),
            LineRecord(
                line_id="line-2",
                region_id="region-1",
                line_order=2,
                span_ids=["span-2"],
                provenance=provenance,
            ),
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic="a",
                text_normalized="a",
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-2",
                line_id="line-2",
                text_diplomatic="b",
                text_normalized="b",
                provenance=provenance,
            ),
        ],
    )


def _review_base() -> dict[str, object]:
    """Return fields required by every review event."""
    return {
        "event_id": "evt-1",
        "task_id": "task-1",
        "target_object_id": "note-1",
        "target_scope": "note",
        "review_dimensions": ["note-linkage"],
        "base_run_id": "run-1",
        "base_graph_revision": "graph-1",
        "guideline_version": "review-v1",
        "prior_trust_state": "machine",
        "new_trust_state": "reviewed",
        "operator_id": "editor-1",
        "timestamp_utc": "2026-07-26T00:00:00Z",
    }


class TestOcrModels:
    """Contract checks for persisted OCR schema models."""

    def test_review_event_union_parses_link_note_payload(self):
        """Review-event schema should discriminate on ``action``."""
        payload = {
            **_review_base(),
            "action": "link_note",
            "marker_span_ids": ["span-1"],
            "note_id": "note-1",
        }

        parsed = TypeAdapter(ReviewEvent).validate_python(payload)

        assert isinstance(parsed, LinkNoteReviewEvent)
        assert parsed.review_dimensions == [ReviewDimension.NOTE_LINKAGE]

    def test_review_task_tells_operator_what_to_inspect_and_certify(self):
        """A review task should be actionable without undocumented context."""
        task = ReviewTask(
            task_id="task-1",
            task_type=ReviewTaskType.TYPOGRAPHY,
            dimensions=[ReviewDimension.TYPOGRAPHY],
            target_scope=ReviewScope.SPAN,
            target_object_ids=["span-1"],
            question="Is this span bold, italic, or superscript?",
            required_evidence=["prepared-page", "style-witness"],
            allowed_actions=["accept", "correct_style", "flag"],
            completion_criteria=["weight, slant, and baseline shift inspected"],
            guideline_id="typography-review",
            guideline_version="1.0.0",
            calibration_example_ids=["style-example-1"],
            base_run_id="run-1",
            base_graph_revision="graph-1",
            supports_abstention=True,
            status=ReviewTaskStatus.PENDING,
        )

        assert task.supports_abstention is True
        assert task.completion_criteria

    def test_document_bundle_and_rag_models_round_trip(self):
        """Bundle and RAG contracts should round-trip one valid page graph."""
        timestamp = datetime(2026, 7, 26, tzinfo=UTC)
        provenance = _provenance()
        prepared_unit = PreparedArtifactRef(
            artifact_id="prep-unit-1",
            kind=InputKind.PREPARED_UNIT,
            page_id="page-0001",
            prepared_unit_id="col-1-part-1",
            artifact_path="pages/page-0001/image/col-1-part-1.png",
        )
        page = BundlePage(
            page_id="page-0001",
            page_number=1,
            prepared_page=PreparedPage(
                preparation_mode=PreparationMode.COLUMNS,
                page_class=PageClass.DENSE_DICTIONARY,
                image_path="pages/page-0001/image/page.png",
                source_artifact_id="source-page-1",
                image_checksum="sha256:prepared",
                preparation_recipe_id="prep-v1",
                coordinate_space=CoordinateSpace(
                    space_id="prepared-page-1",
                    width_px=2400,
                    height_px=3600,
                    dpi=400,
                ),
                prepared_units=[prepared_unit],
            ),
            regions=[
                RegionRecord(
                    region_id="region-1",
                    region_kind=RegionKind.BODY,
                    reading_order_index=1,
                    line_ids=["line-1"],
                    provenance=provenance,
                )
            ],
            lines=[
                LineRecord(
                    line_id="line-1",
                    region_id="region-1",
                    line_order=1,
                    span_ids=["span-1"],
                    provenance=provenance,
                )
            ],
            spans=[
                SpanRecord(
                    span_id="span-1",
                    line_id="line-1",
                    text_diplomatic="andgit",
                    text_normalized="andgit",
                    typography=Typography(
                        weight=FontWeight.REGULAR,
                        slant=FontSlant.ITALIC,
                        baseline_shift=BaselineShift.BASELINE,
                    ),
                    roles=[TextRole.TEXT],
                    trust_state=TrustState.REVIEWED,
                    provenance=provenance,
                    review=ReviewSummary(
                        reviewed_dimensions=[
                            ReviewDimension.TEXT,
                            ReviewDimension.TYPOGRAPHY,
                        ],
                        corrected_dimensions=[],
                        last_event_id="evt-1",
                        event_ids=["evt-1"],
                    ),
                )
            ],
            notes=[],
            evaluation_summary=PageEvaluationSummary(),
            review_event_ids=["evt-1"],
        )
        bundle = DocumentBundle(
            document_id="bosworth-demo",
            bundle_schema_version="1.0.0",
            source=SourceDescriptor(
                source_id="src-1",
                source_type=SourceType.IMAGE_SET,
                source_label="dictionary-pages.zip",
                original_path="sources/dictionary-pages.zip",
                page_count=1,
            ),
            bibliographic_provenance=BibliographicProvenance(
                title="A Concise Anglo-Saxon Dictionary",
                authors=["John R. Clark Hall"],
            ),
            acquisition_provenance=AcquisitionProvenance(
                acquisition_kind="archive-org",
                acquired_from="archive.org",
                source_uri="https://archive.org/",
            ),
            run=RunMetadata(
                run_id="run-1",
                run_timestamp_utc=timestamp,
                preparation_recipe_id="prep-v1",
                config_digest="sha256:config",
                runner_set=[RunnerReference(runner_id="fixture")],
                bundle_schema_version="1.0.0",
            ),
            pages=[page],
            evaluation_summary=DocumentEvaluationSummary(
                text=EvaluationFamilySummary(),
                structure=EvaluationFamilySummary(),
                typography=EvaluationFamilySummary(),
                note_linkage=EvaluationFamilySummary(),
            ),
            exports=ExportSummary(
                bundle_json_path="exports/bundle.json",
                rag_jsonl_path="exports/rag.jsonl",
            ),
        )
        retrieval_provenance = RetrievalProvenance(
            source_page_ids=["page-0001"],
            witness_ids=["wit-1"],
            runner_ids=["olmocr"],
        )
        rag = RagDocument(
            document_id="bosworth-demo",
            schema_version="1.0.0",
            chunking_recipe_id="page-regions-v1",
            chunks=[
                RagChunk(
                    chunk_id="chunk-1",
                    chunk_type=ChunkType.REGION,
                    document_id="bosworth-demo",
                    page_ids=["page-0001"],
                    text="andgit",
                    trust_state=TrustState.REVIEWED,
                    source_object_ids=["region-1", "span-1"],
                    provenance=retrieval_provenance,
                    typography_summary=[
                        Typography(slant=FontSlant.ITALIC)
                    ],
                )
            ],
        )

        restored = DocumentBundle.model_validate_json(bundle.model_dump_json())

        assert restored == bundle
        assert rag.model_dump(mode="json")["chunks"][0]["chunk_type"] == "region_chunk"

    def test_runner_batch_overlay_and_gold_models_accept_realistic_shapes(self):
        """Runner, overlay, and gold contracts should fit the planned workflow."""
        timestamp = datetime(2026, 7, 26, tzinfo=UTC)
        runner = RunnerReference(
            runner_id="olmocr",
            runner_version="0.4.27",
            model_name="allenai/olmOCR",
            model_revision="model-revision",
            runtime_name="huggingface-endpoint",
            runtime_revision="container-digest",
            config_digest="sha256:runner-config",
            prompt_digest="sha256:prompt",
        )
        batch = RunnerExecutionBatch(
            schema_version="1.0.0",
            batch_id="batch-1",
            run_id="run-1",
            document_id="wright-demo",
            runner=runner,
            capability=RunnerCapability(
                accepted_input_kinds=[InputKind.IMAGE, InputKind.PDF],
                preferred_input_kind=InputKind.PDF,
                supports_multi_item_batching=True,
                batch_unit_kind=BatchUnitKind.PAGE,
                packaging_strategy=PackagingStrategy.IMAGE_TO_PDF,
            ),
            batch_size=1,
            items=[
                BatchItemRef(
                    item_id="item-1",
                    source_page_id="page-0001",
                    artifact_id="prepared-1",
                )
            ],
            started_at_utc=timestamp,
            result_status=BatchResultStatus.SUCCEEDED,
            output_artifacts=[
                RunnerOutputArtifact(
                    artifact_id="wit-1",
                    artifact_kind="text",
                    artifact_path="pages/page-0001/witnesses/text/olmocr.json",
                    media_type="application/json",
                    batch_item_ids=["item-1"],
                )
            ],
        )
        overlay = PageOverlay(
            schema_version="1.0.0",
            overlay_id="overlay-1",
            page_id="page-0001",
            source_run_id="run-1",
            base_graph_revision="graph-1",
            prepared_image_checksum="sha256:prepared",
            review_tasks=[
                ReviewTask(
                    task_id="task-1",
                    task_type=ReviewTaskType.TEXT,
                    dimensions=[ReviewDimension.TEXT],
                    target_scope=ReviewScope.SPAN,
                    target_object_ids=["span-1"],
                    question="Does the diplomatic text match the image?",
                    required_evidence=["prepared-page", "text-witness"],
                    allowed_actions=["accept", "correct_text", "flag"],
                    completion_criteria=["every grapheme checked"],
                    guideline_id="text-review",
                    guideline_version="1.0.0",
                    base_run_id="run-1",
                    base_graph_revision="graph-1",
                )
            ],
            review_events=[
                TypeAdapter(ReviewEvent).validate_python(
                    {
                        **_review_base(),
                        "target_object_id": "span-1",
                        "target_scope": "span",
                        "review_dimensions": ["text"],
                        "action": "correct_text",
                        "text_diplomatic": "sittan",
                    }
                )
            ],
            current_state=[
                OverlayState(
                    object_id="span-1",
                    scope=ReviewScope.SPAN,
                    trust_state=TrustState.CORRECTED,
                    reviewed_dimensions=[ReviewDimension.TEXT],
                    corrected_dimensions=[ReviewDimension.TEXT],
                    applied_event_ids=["evt-1"],
                    text_diplomatic_override="sittan",
                )
            ],
        )
        gold = GoldDocument(
            schema_version="1.0.0",
            document_id="mitchell-demo",
            guideline_id="gold-v1",
            guideline_version="1.0.0",
            annotators=["editor-1"],
            pages=[
                GoldPageAnnotation(
                    page_id="page-0003",
                    page_number=3,
                    source_run_id="run-1",
                    base_graph_revision="graph-1",
                    prepared_image_checksum="sha256:prepared",
                    coverage=[
                        GoldCoverage(
                            coverage_id="coverage-1",
                            dimensions=[ReviewDimension.TEXT],
                            target_object_ids=["span-1"],
                            exhaustive=True,
                        )
                    ],
                    text_spans=[
                        GoldTextSpan(
                            annotation_id="gold-span-1",
                            target_object_id="span-1",
                            text_diplomatic="ic",
                            text_normalized="ic",
                        )
                    ],
                )
            ],
        )

        assert batch.capability.packaging_strategy == "image-to-pdf"
        assert overlay.current_state[0].reviewed_dimensions == [ReviewDimension.TEXT]
        assert gold.pages[0].coverage[0].exhaustive is True

    @pytest.mark.parametrize(
        "values",
        [
            {"x0": 10, "y0": 0, "x1": 5, "y1": 20},
            {"x0": 0, "y0": 20, "x1": 5, "y1": 20},
        ],
    )
    def test_bounding_box_rejects_empty_or_reversed_geometry(self, values):
        """Boxes must represent a positive-area rectangle."""
        with pytest.raises(ValidationError):
            BoundingBox(**values)

    def test_runner_capability_rejects_unaccepted_preferred_input(self):
        """Preferred input must be one of the runner's accepted inputs."""
        with pytest.raises(ValidationError):
            RunnerCapability(
                accepted_input_kinds=[InputKind.IMAGE],
                preferred_input_kind=InputKind.PDF,
                supports_multi_item_batching=False,
                batch_unit_kind=BatchUnitKind.PAGE,
                packaging_strategy=PackagingStrategy.IMAGE_TO_PDF,
            )

    def test_runner_batch_rejects_count_and_failure_inconsistency(self):
        """Persisted batch status must agree with submitted and failed items."""
        with pytest.raises(ValidationError):
            RunnerExecutionBatch(
                schema_version="1.0.0",
                batch_id="batch-1",
                run_id="run-1",
                document_id="doc-1",
                runner=RunnerReference(runner_id="fixture"),
                capability=RunnerCapability(
                    accepted_input_kinds=[InputKind.IMAGE],
                    preferred_input_kind=InputKind.IMAGE,
                    supports_multi_item_batching=True,
                    batch_unit_kind=BatchUnitKind.PAGE,
                    packaging_strategy=PackagingStrategy.DIRECT,
                ),
                batch_size=2,
                items=[],
                started_at_utc=datetime(2026, 7, 26, tzinfo=UTC),
                result_status=BatchResultStatus.SUCCEEDED,
                failure_item_ids=["missing-item"],
            )

    def test_bundle_page_rejects_dangling_graph_references(self):
        """Graph parent-child identifiers must resolve within the page."""
        with pytest.raises(ValidationError):
            BundlePage(
                page_id="page-1",
                page_number=1,
                prepared_page=PreparedPage(
                    preparation_mode=PreparationMode.FULL_PAGE,
                    page_class=PageClass.ORDINARY_PROSE,
                    image_path="page.png",
                    source_artifact_id="source-1",
                    image_checksum="sha256:image",
                    preparation_recipe_id="prep-v1",
                    coordinate_space=CoordinateSpace(
                        space_id="prepared-page-1",
                        width_px=100,
                        height_px=100,
                    ),
                ),
                regions=[
                    RegionRecord(
                        region_id="region-1",
                        region_kind=RegionKind.BODY,
                        reading_order_index=1,
                        line_ids=["missing-line"],
                        provenance=_provenance(),
                    )
                ],
            )

    def test_gold_annotation_requires_graph_or_image_anchor(self):
        """Gold text without a graph target or geometry cannot be scored."""
        with pytest.raises(ValidationError):
            GoldTextSpan(annotation_id="gold-1", text_diplomatic="ic")

    def test_model_backed_runner_requires_revision_and_digests(self):
        """Model-backed evidence must be reproducible."""
        with pytest.raises(ValidationError):
            RunnerReference(runner_id="olmocr", model_name="allenai/olmOCR")

    def test_model_backed_runner_rejects_local_inference_runtime(self):
        """OCR models must run on the required Hugging Face hosting boundary."""
        with pytest.raises(ValidationError):
            RunnerReference(
                runner_id="olmocr",
                model_name="allenai/olmOCR",
                model_revision="model-revision",
                runtime_name="local-gpu",
                runtime_revision="container-digest",
                config_digest="sha256:runner-config",
                prompt_digest="sha256:prompt",
            )


def test_metric_profile_rejects_invalid_iou_threshold() -> None:
    with pytest.raises(ValidationError):
        MetricProfile(
            profile_id="diplomatic-v1",
            version="1.0.0",
            whitespace_significant=True,
            punctuation_significant=True,
            case_sensitive=True,
            line_breaks_significant=True,
            tokenizer_pattern=r"\w+(?:['’]\w+)*|[^\w\s]",  # noqa: RUF001
            region_iou_threshold=1.1,
            exclude_illegible=True,
            unknown_style_is_incorrect=True,
        )


def test_excluded_line_join_requires_reason() -> None:
    with pytest.raises(ValidationError):
        GoldLineJoin(
            annotation_id="join-1",
            left_line_id="line-1",
            right_line_id="line-2",
            joined=True,
            do_not_score=True,
        )


def test_bundle_rejects_unknown_line_join_target() -> None:
    page = valid_bundle_page()
    page.lines[0].joins_to_line_id = "missing-line"
    with pytest.raises(ValidationError, match="unknown joined line"):
        BundlePage.model_validate(page.model_dump())
