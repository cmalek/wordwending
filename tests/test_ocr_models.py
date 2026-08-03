# Copyright (C) 2026 Chris Malek.
"""Tests for the canonical OCR schema models."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pydantic import TypeAdapter, ValidationError

from bochord.models import (
    AcquisitionProvenance,
    AssessmentThresholds,
    BaselineShift,
    BatchItemRef,
    BatchResultStatus,
    BatchUnitKind,
    BibliographicProvenance,
    BoundingBox,
    BundlePage,
    ChunkType,
    CoordinateSpace,
    CorrectGeometryReviewEvent,
    DecidePreparationReviewEvent,
    DecideSourceTriageReviewEvent,
    DocumentBundle,
    DocumentEvaluationSummary,
    EvaluationCohortKey,
    EvaluationCohortReport,
    EvaluationCohortSummary,
    EvaluationFamilySummary,
    ExportSummary,
    FlagReviewEvent,
    FlagSeverity,
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
    PackagedRunnerInput,
    PackagingStrategy,
    PageClass,
    PageEvaluationRecord,
    PageEvaluationSummary,
    PageOverlay,
    Point,
    Polygon,
    PreparationAssessment,
    PreparationDecision,
    PreparationMode,
    PreparationRecipe,
    PreparedArtifactRef,
    PreparedPage,
    RagChunk,
    RagDocument,
    RegionKind,
    RegionRecord,
    RegionRevision,
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
    RunnerExecutionPolicy,
    RunnerOutputArtifact,
    RunnerReference,
    RunnerThroughputSummary,
    SourceDescriptor,
    SourceTriageDecision,
    SourceType,
    SpanRecord,
    StyleEvaluationSummary,
    TextRole,
    TrustState,
    Typography,
)

if TYPE_CHECKING:
    from collections.abc import Callable

FIXTURES = Path(__file__).parent / "fixtures" / "runner"


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        machine_confidence=0.91,
        merge_confidence=0.84,
    )


def test_object_provenance_defaults_empty_alternate_candidates() -> None:
    """Existing provenance fixtures stay valid without alternate candidates."""
    provenance = _provenance()
    assert provenance.alternate_candidates == []


def test_object_provenance_accepts_alternate_candidates() -> None:
    """Alternate merge interpretations live in provenance, not duplicate nodes."""
    from bochord.models import AlternateCandidate

    alternate = AlternateCandidate(
        witness_id="wit-2",
        runner_id="other-runner",
        value_kind="text",
        value={"text_diplomatic": "variant reading"},
        machine_confidence=0.75,
    )
    provenance = ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        alternate_candidates=[alternate],
        disagreement_note="normalized text differed",
    )
    assert len(provenance.alternate_candidates) == 1
    assert provenance.alternate_candidates[0].value_kind == "text"
    assert provenance.alternate_candidates[0].value["text_diplomatic"] == (
        "variant reading"
    )


def valid_bundle_page() -> BundlePage:
    """Return a minimal valid page graph for join-reference tests."""
    provenance = _provenance()
    return BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=PreparedPage(
            prepared_page_id="prepared-page-1",
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
            preparation_recipe_digest="digest-prep-v1",
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


def _review_box(*, coordinate_space_id: str = "prepared-page-1") -> BoundingBox:
    """Return a valid review geometry bounding box."""
    return BoundingBox(
        x0=0,
        y0=0,
        x1=10,
        y1=10,
        coordinate_space_id=coordinate_space_id,
    )


def _review_polygon(*, coordinate_space_id: str = "prepared-page-1") -> Polygon:
    """Return a valid review geometry polygon."""
    return Polygon(
        coordinate_space_id=coordinate_space_id,
        points=[
            Point(x=0, y=0),
            Point(x=10, y=0),
            Point(x=10, y=10),
        ],
    )


def _text_review_task(**overrides: object) -> ReviewTask:
    """Return a minimal text-review task bound to the overlay defaults."""
    defaults: dict[str, object] = {
        "task_id": "task-1",
        "task_type": ReviewTaskType.TEXT,
        "dimensions": [ReviewDimension.TEXT],
        "target_scope": ReviewScope.SPAN,
        "target_object_ids": ["span-1"],
        "question": "Does the diplomatic text match?",
        "required_evidence": ["prepared-page", "text-witness"],
        "allowed_actions": ["accept", "correct_text", "correct_geometry", "flag"],
        "completion_criteria": ["graphemes inspected"],
        "guideline_id": "text-review",
        "guideline_version": "1.0.0",
        "base_run_id": "run-1",
        "base_graph_revision": "graph-1",
        "prepared_image_checksum": "sha256:prepared",
    }
    defaults.update(overrides)
    return ReviewTask(**defaults)  # type: ignore[arg-type]


def _minimal_page_overlay(**overrides: object) -> PageOverlay:
    """Return a minimal page overlay with one text task and no events."""
    defaults: dict[str, object] = {
        "schema_version": "1.0.0",
        "overlay_id": "overlay-1",
        "page_id": "page-1",
        "source_run_id": "run-1",
        "base_graph_revision": "graph-1",
        "prepared_image_checksum": "sha256:prepared",
        "review_tasks": [_text_review_task()],
        "review_events": [],
        "current_state": [],
    }
    defaults.update(overrides)
    return PageOverlay(**defaults)  # type: ignore[arg-type]


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

    def test_review_event_union_parses_source_triage_decision(self):
        """Source-triage events carry an explicit disposition and optional reason."""
        payload = {
            **_review_base(),
            "target_object_id": "page-1",
            "target_scope": "page",
            "review_dimensions": ["source-quality"],
            "action": "decide_source_triage",
            "decision": "usable-with-warning",
            "reason": "gutter shadow at left margin",
        }

        parsed = TypeAdapter(ReviewEvent).validate_python(payload)

        assert isinstance(parsed, DecideSourceTriageReviewEvent)
        assert parsed.decision is SourceTriageDecision.USABLE_WITH_WARNING
        assert parsed.reason == "gutter shadow at left margin"

    def test_review_event_union_parses_preparation_decision(self):
        """Preparation events carry full-page or subdivide plus optional reason."""
        payload = {
            **_review_base(),
            "target_object_id": "page-1",
            "target_scope": "page",
            "review_dimensions": ["preparation"],
            "action": "decide_preparation",
            "decision": "subdivide",
            "reason": None,
        }

        parsed = TypeAdapter(ReviewEvent).validate_python(payload)

        assert isinstance(parsed, DecidePreparationReviewEvent)
        assert parsed.decision is PreparationDecision.SUBDIVIDE
        assert parsed.reason is None

    @pytest.mark.parametrize(
        ("task_type", "wrong_dimension", "match"),
        [
            (ReviewTaskType.SOURCE_TRIAGE, ReviewDimension.TEXT, "source-quality"),
            (ReviewTaskType.PREPARATION, ReviewDimension.STRUCTURE, "preparation"),
            (ReviewTaskType.TEXT, ReviewDimension.TYPOGRAPHY, "text"),
            (ReviewTaskType.LAYOUT, ReviewDimension.TEXT, "structure"),
            (ReviewTaskType.TYPOGRAPHY, ReviewDimension.TEXT, "typography"),
            (ReviewTaskType.NOTE_LINKAGE, ReviewDimension.STRUCTURE, "note-linkage"),
        ],
        ids=[
            "source_triage",
            "preparation",
            "text",
            "layout",
            "typography",
            "note_linkage",
        ],
    )
    def test_page_overlay_rejects_task_with_wrong_exclusive_dimension(
        self,
        task_type: ReviewTaskType,
        wrong_dimension: ReviewDimension,
        match: str,
    ) -> None:
        """HumanMarkupService task types must certify only their exclusive dimension."""
        with pytest.raises(ValidationError, match=match):
            PageOverlay(
                schema_version="1.0.0",
                overlay_id="overlay-1",
                page_id="page-1",
                source_run_id="run-1",
                base_graph_revision="graph-1",
                prepared_image_checksum="sha256:prepared",
                review_tasks=[
                    ReviewTask(
                        task_id="task-1",
                        task_type=task_type,
                        dimensions=[wrong_dimension],
                        target_scope=ReviewScope.PAGE,
                        target_object_ids=["page-1"],
                        question="Is the exclusive dimension correct?",
                        required_evidence=["prepared-page"],
                        allowed_actions=["accept", "flag"],
                        completion_criteria=["dimension inspected"],
                        guideline_id="review",
                        guideline_version="1.0.0",
                        base_run_id="run-1",
                        base_graph_revision="graph-1",
                        prepared_image_checksum="sha256:prepared",
                    )
                ],
                review_events=[],
            )

    def test_page_overlay_rejects_task_with_mismatched_prepared_image_checksum(
        self,
    ) -> None:
        """Tasks must bind to the same prepared image the overlay records."""
        with pytest.raises(ValidationError, match="prepared image checksum"):
            PageOverlay(
                schema_version="1.0.0",
                overlay_id="overlay-1",
                page_id="page-1",
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
                        question="Does the diplomatic text match?",
                        required_evidence=["prepared-page", "text-witness"],
                        allowed_actions=["accept", "flag"],
                        completion_criteria=["graphemes inspected"],
                        guideline_id="review",
                        guideline_version="1.0.0",
                        base_run_id="run-1",
                        base_graph_revision="graph-1",
                        prepared_image_checksum="sha256:WRONG-IMAGE",
                    )
                ],
                review_events=[],
            )

    def test_correct_geometry_rejects_mismatched_coordinate_space_ids(self) -> None:
        """Box and polygon must share one coordinate space identity."""
        with pytest.raises(ValidationError, match="coordinate space"):
            CorrectGeometryReviewEvent(
                event_id="evt-geo-1",
                task_id="task-1",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.STRUCTURE],
                base_run_id="run-1",
                base_graph_revision="graph-1",
                guideline_version="1.0.0",
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.CORRECTED,
                operator_id="editor-1",
                timestamp_utc=datetime(2026, 7, 26, tzinfo=UTC),
                bounding_box=_review_box(coordinate_space_id="prepared-page-1"),
                polygon=_review_polygon(coordinate_space_id="prepared-unit-1"),
            )

    def test_region_revision_rejects_mismatched_coordinate_space_ids(self) -> None:
        """Region revisions must not mix geometry from different spaces."""
        with pytest.raises(ValidationError, match="coordinate space"):
            RegionRevision(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                bounding_box=_review_box(coordinate_space_id="prepared-page-1"),
                polygon=_review_polygon(coordinate_space_id="prepared-unit-1"),
            )

    def test_region_revision_rejects_missing_coordinate_space_geometry(self) -> None:
        """Region revisions must include at least one geometry form."""
        with pytest.raises(ValidationError, match="bounding box or polygon"):
            RegionRevision(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
            )

    def test_page_overlay_rejects_event_target_scope_mismatch_with_task(self) -> None:
        """Events must use the same target scope as their review task."""
        with pytest.raises(ValidationError, match="target scope"):
            _minimal_page_overlay(
                review_events=[
                    TypeAdapter(ReviewEvent).validate_python(
                        {
                            **_review_base(),
                            "target_object_id": "span-1",
                            "target_scope": "region",
                            "review_dimensions": ["text"],
                            "guideline_version": "1.0.0",
                            "action": "accept",
                        }
                    )
                ],
            )

    def test_page_overlay_rejects_event_guideline_version_mismatch_with_task(
        self,
    ) -> None:
        """Events must bind to the exact guideline revision shown in the task."""
        with pytest.raises(ValidationError, match="guideline version"):
            _minimal_page_overlay(
                review_events=[
                    TypeAdapter(ReviewEvent).validate_python(
                        {
                            **_review_base(),
                            "target_object_id": "span-1",
                            "target_scope": "span",
                            "review_dimensions": ["text"],
                            "guideline_version": "2.0.0",
                            "action": "accept",
                        }
                    )
                ],
            )

    def test_overlay_flag_review_event_rejects_trust_state_change(self) -> None:
        """Flag events record concern without changing trust state."""
        with pytest.raises(ValidationError, match="trust state"):
            FlagReviewEvent(
                event_id="evt-flag-1",
                task_id="task-1",
                target_object_id="span-1",
                target_scope=ReviewScope.SPAN,
                review_dimensions=[ReviewDimension.TEXT],
                base_run_id="run-1",
                base_graph_revision="graph-1",
                guideline_version="1.0.0",
                prior_trust_state=TrustState.MACHINE,
                new_trust_state=TrustState.REVIEWED,
                operator_id="editor-1",
                timestamp_utc=datetime(2026, 7, 26, tzinfo=UTC),
                flag_id="flag-1",
                flag_type="ambiguous-glyph",
                severity=FlagSeverity.WARNING,
                message="unclear character",
            )

    def test_page_overlay_rejects_overlay_state_applied_event_object_scope_mismatch(
        self,
    ) -> None:
        """Materialized state must only reference events for the same object."""
        with pytest.raises(ValidationError, match="another object or scope"):
            _minimal_page_overlay(
                review_events=[
                    TypeAdapter(ReviewEvent).validate_python(
                        {
                            **_review_base(),
                            "target_object_id": "span-1",
                            "target_scope": "span",
                            "review_dimensions": ["text"],
                            "guideline_version": "1.0.0",
                            "action": "accept",
                        }
                    )
                ],
                current_state=[
                    OverlayState(
                        object_id="span-2",
                        scope=ReviewScope.SPAN,
                        trust_state=TrustState.REVIEWED,
                        applied_event_ids=["evt-1"],
                    )
                ],
            )

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
            prepared_image_checksum="sha256:prepared",
            supports_abstention=True,
            status=ReviewTaskStatus.PENDING,
        )

        assert task.supports_abstention is True
        assert task.completion_criteria
        assert task.prepared_image_checksum == "sha256:prepared"

    def test_review_task_rejects_missing_prepared_image_checksum(self):
        """Review tasks must bind to the prepared image the operator inspects."""
        with pytest.raises(ValidationError):
            ReviewTask(
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
                base_run_id="run-1",
                base_graph_revision="graph-1",
            )

    def test_review_task_rejects_related_object_id_overlap(self):
        """Related ids must not duplicate or overlap primary targets."""
        with pytest.raises(ValidationError, match="overlap"):
            ReviewTask(
                task_id="task-1",
                task_type=ReviewTaskType.NOTE_LINKAGE,
                dimensions=[ReviewDimension.NOTE_LINKAGE],
                target_scope=ReviewScope.NOTE,
                target_object_ids=["note-1"],
                related_object_ids=["note-1"],
                question="Does the marker map to this note?",
                required_evidence=["prepared-page", "note-witness"],
                allowed_actions=["accept", "link_note", "unlink_note", "flag"],
                completion_criteria=["marker and note body inspected"],
                guideline_id="note-review",
                guideline_version="1.0.0",
                base_run_id="run-1",
                base_graph_revision="graph-1",
                prepared_image_checksum="sha256:prepared",
            )

    def test_review_task_rejects_duplicate_related_object_ids(self):
        """Related object ids must be unique."""
        with pytest.raises(ValidationError, match="duplicates"):
            ReviewTask(
                task_id="task-1",
                task_type=ReviewTaskType.NOTE_LINKAGE,
                dimensions=[ReviewDimension.NOTE_LINKAGE],
                target_scope=ReviewScope.NOTE,
                target_object_ids=["note-1"],
                related_object_ids=["span-1", "span-1"],
                question="Does the marker map to this note?",
                required_evidence=["prepared-page", "note-witness"],
                allowed_actions=["accept", "link_note", "unlink_note", "flag"],
                completion_criteria=["marker and note body inspected"],
                guideline_id="note-review",
                guideline_version="1.0.0",
                base_run_id="run-1",
                base_graph_revision="graph-1",
                prepared_image_checksum="sha256:prepared",
            )

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
            parent_prepared_page_id="prepared-page-1",
            checksum="sha256:col-1-part-1",
            order=1,
            bounding_box=BoundingBox(x0=0, y0=0, x1=1200, y1=3600),
        )
        page = BundlePage(
            page_id="page-0001",
            page_number=1,
            prepared_page=PreparedPage(
                prepared_page_id="prepared-page-1",
                preparation_mode=PreparationMode.COLUMNS,
                page_class=PageClass.DENSE_DICTIONARY,
                image_path="pages/page-0001/image/page.png",
                source_artifact_id="source-page-1",
                image_checksum="sha256:prepared",
                preparation_recipe_id="prep-v1",
                preparation_recipe_digest="digest-prep-v1",
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
                style=StyleEvaluationSummary(),
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
            hardware_class="nvidia-l40s",
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
            execution_policy_id="olmocr-hf-fixed-v1",
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
                    prepared_image_checksum="sha256:prepared",
                )
            ],
            review_events=[
                TypeAdapter(ReviewEvent).validate_python(
                    {
                        **_review_base(),
                        "target_object_id": "span-1",
                        "target_scope": "span",
                        "review_dimensions": ["text"],
                        "guideline_version": "1.0.0",
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
                execution_policy_id="olmocr-hf-fixed-v1",
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
                    prepared_page_id="prepared-page-1",
                    preparation_mode=PreparationMode.FULL_PAGE,
                    page_class=PageClass.ORDINARY_PROSE,
                    image_path="page.png",
                    source_artifact_id="source-1",
                    image_checksum="sha256:image",
                    preparation_recipe_id="prep-v1",
                    preparation_recipe_digest="digest-prep-v1",
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
                hardware_class="nvidia-l40s",
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


def model_runner_payload(**overrides: object) -> dict[str, object]:
    """Return a valid model-backed runner payload with optional overrides."""
    payload: dict[str, object] = {
        "runner_id": "olmocr",
        "runner_version": "0.4.27",
        "model_name": "allenai/olmOCR",
        "model_revision": "model-revision",
        "hardware_class": "nvidia-l40s",
        "runtime_name": "huggingface-endpoint",
        "runtime_revision": "container-digest",
        "config_digest": "sha256:runner-config",
        "prompt_digest": "sha256:prompt",
    }
    payload.update(overrides)
    return payload


def capability_payload(**overrides: object) -> dict[str, object]:
    """Return a valid runner capability payload with optional overrides."""
    payload: dict[str, object] = {
        "accepted_input_kinds": ["image", "pdf"],
        "preferred_input_kind": "pdf",
        "supports_multi_item_batching": True,
        "batch_unit_kind": "prepared-unit",
        "packaging_strategy": "unit-to-pdf-batch",
    }
    payload.update(overrides)
    return payload


def execution_batch_payload(**overrides: object) -> dict[str, object]:
    """Return a valid runner execution batch payload with optional overrides."""
    payload: dict[str, object] = {
        "schema_version": "1.0.0",
        "batch_id": "batch-spec-0013",
        "run_id": "run-spec-0013",
        "document_id": "doc-spec-0013",
        "execution_policy_id": "olmocr-hf-fixed-v1",
        "runner": model_runner_payload(model_revision="abcdef0123456789"),
        "capability": capability_payload(),
        "packaging_artifact_id": "pkg-spec-0013",
        "batch_size": 2,
        "items": [
            {
                "item_id": "item-1",
                "source_page_id": "page-0001",
                "artifact_id": "art-1",
            },
            {
                "item_id": "item-2",
                "source_page_id": "page-0002",
                "artifact_id": "art-2",
            },
        ],
        "started_at_utc": "2026-07-31T12:00:00+00:00",
        "finished_at_utc": "2026-07-31T12:05:00+00:00",
        "result_status": "succeeded",
        "failure_item_ids": [],
        "output_artifacts": [
            {
                "artifact_id": "wit-1",
                "artifact_kind": "text",
                "artifact_path": "pages/page-0001/witnesses/text/olmocr.json",
                "media_type": "application/json",
                "batch_item_ids": ["item-1", "item-2"],
            }
        ],
        "warnings": [],
        "warmup": False,
        "request_ids": ["req-spec-0013"],
    }
    payload.update(overrides)
    return payload


def runner_policy_payload(**overrides: object) -> dict[str, object]:
    """Return a valid runner execution policy payload with optional overrides."""
    payload: dict[str, object] = {
        "policy_id": "olmocr-hf-fixed-v1",
        "version": "1",
        "batch_size": 4,
        "target_longest_image_dim": 1024,
        "preserve_page_local_groups": True,
        "packaging_strategy": "unit-to-pdf-batch",
        "warmup_batch_count": 1,
        "retry_mode": "failed-items",
        "max_retries": 1,
        "endpoint": {
            "endpoint_name": "olmocr-production",
            "endpoint_key": "olmocr-production",
            "hardware_class": "nvidia-l40s",
            "cold_start_timeout_seconds": 600,
            "request_timeout_seconds": 180,
            "retryable_status_codes": [408, 429, 502, 503, 504],
            "scale_to_zero": True,
            "max_items_per_run": 100,
            "estimated_cost_per_item_usd": "0.01",
            "max_run_cost_usd": "1.00",
            "artifact_retention_days": 30,
        },
    }
    payload.update(overrides)
    return payload


@pytest.mark.parametrize(
    "model_revision",
    [
        pytest.param("main", id="main"),
        pytest.param("Master", id="Master"),
        pytest.param("LATEST", id="LATEST"),
        pytest.param("  HEAD  ", id="HEAD-whitespace"),
        pytest.param("head", id="head"),
    ],
)
def test_runner_reference_rejects_mutable_model_revision(
    model_revision: str,
) -> None:
    with pytest.raises(ValidationError, match="mutable"):
        RunnerReference.model_validate(
            model_runner_payload(model_revision=model_revision),
        )


def test_runner_reference_accepts_immutable_digest_revision() -> None:
    ref = RunnerReference(
        runner_id="olmocr",
        model_name="allenai/olmOCR-7B",
        model_revision="abcdef0123456789",
        hardware_class="nvidia-l40s",
        runtime_name="huggingface-endpoint",
        runtime_revision="ep-rev-1",
        config_digest="cfg",
        prompt_digest="prompt",
    )
    assert ref.model_revision == "abcdef0123456789"


def test_model_backed_runner_requires_hardware_class() -> None:
    payload = model_runner_payload(hardware_class=None)
    with pytest.raises(ValidationError):
        RunnerReference.model_validate(payload)


def test_endpoint_policy_rejects_estimate_above_run_cap() -> None:
    policy = runner_policy_payload(
        endpoint={
            **runner_policy_payload()["endpoint"],  # type: ignore[index]
            "max_items_per_run": 10,
            "estimated_cost_per_item_usd": "0.20",
            "max_run_cost_usd": "1.00",
        },
    )
    with pytest.raises(ValidationError):
        RunnerExecutionPolicy.model_validate(policy)


def test_packaged_runner_input_rejects_mismatched_item_page_lengths() -> None:
    with pytest.raises(ValidationError):
        PackagedRunnerInput(
            artifact_id="pkg-1",
            artifact_path="runner-inputs/batch-1.pdf",
            checksum="sha256:pkg",
            kind=InputKind.PDF,
            batch_item_ids=["item-1", "item-2"],
            page_numbers=[1],
        )


def test_runner_policy_fixture_validates() -> None:
    policy = RunnerExecutionPolicy.model_validate_json(
        FIXTURES.joinpath("olmocr-policy-v1.json").read_text()
    )
    assert policy.policy_id == "olmocr-hf-fixed-v1"
    assert policy.endpoint.hardware_class == "nvidia-l40s"


def test_spec_0013_capability_fixture_round_trips() -> None:
    payload = json.loads(FIXTURES.joinpath("capability-v1.json").read_text())
    capability = RunnerCapability.model_validate(payload)
    assert capability.model_dump(mode="json") == payload


def test_spec_0013_batch_fixtures_round_trip_by_status() -> None:
    for name in (
        "execution-batch-succeeded-v1.json",
        "execution-batch-partial-v1.json",
        "execution-batch-failed-v1.json",
    ):
        payload = json.loads(FIXTURES.joinpath(name).read_text())
        batch = RunnerExecutionBatch.model_validate(payload)
        assert batch.model_dump(mode="json") == payload
        assert batch.batch_size == len(batch.items)


@pytest.mark.parametrize(
    ("model", "make_payload", "overrides", "match"),
    [
        pytest.param(
            RunnerCapability,
            capability_payload,
            {"accepted_input_kinds": []},
            "accepted_input_kinds must not be empty",
            id="accepted_input_kinds-empty",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {
                "batch_size": 2,
                "items": [
                    {
                        "item_id": "item-1",
                        "source_page_id": "page-0001",
                        "artifact_id": "art-1",
                    },
                    {
                        "item_id": "item-1",
                        "source_page_id": "page-0002",
                        "artifact_id": "art-2",
                    },
                ],
            },
            "batch item ids must be unique",
            id="batch-item-ids-unique",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {
                "result_status": "succeeded",
                "failure_item_ids": ["item-1"],
            },
            "succeeded batches cannot contain failed items",
            id="succeeded-no-failures",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {
                "result_status": "partial",
                "failure_item_ids": ["missing-item"],
            },
            "failure_item_ids must identify submitted batch items",
            id="failure-item-ids-submitted",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {"result_status": "partial", "failure_item_ids": []},
            "partial batches require some but not all items to fail",
            id="partial-no-failures",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {
                "result_status": "partial",
                "failure_item_ids": ["item-1", "item-2"],
            },
            "partial batches require some but not all items to fail",
            id="partial-all-failures",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {"result_status": "failed", "failure_item_ids": ["item-1"]},
            "failed batches must identify every submitted item as failed",
            id="failed-partial-failures",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {
                "started_at_utc": "2026-07-31T12:05:00+00:00",
                "finished_at_utc": "2026-07-31T12:00:00+00:00",
            },
            "finished_at_utc cannot precede started_at_utc",
            id="finished-before-started",
        ),
        pytest.param(
            RunnerExecutionBatch,
            execution_batch_payload,
            {
                "output_artifacts": [
                    {
                        "artifact_id": "wit-1",
                        "artifact_kind": "text",
                        "artifact_path": "pages/page-0001/witnesses/text/olmocr.json",
                        "media_type": "application/json",
                        "batch_item_ids": ["item-1", "unknown-item"],
                    }
                ],
            },
            "output artifacts must identify submitted batch items",
            id="output-artifacts-submitted",
        ),
    ],
)
def test_spec_0013_runner_invariants_reject_invalid_payloads(
    model: type[RunnerCapability | RunnerExecutionBatch],
    make_payload: Callable[..., dict[str, object]],
    overrides: dict[str, object],
    match: str,
) -> None:
    with pytest.raises(ValidationError, match=match):
        model.model_validate(make_payload(**overrides))


def test_throughput_summary_rejects_inconsistent_items_per_second() -> None:
    with pytest.raises(ValidationError, match="items_per_second must equal"):
        RunnerThroughputSummary(
            measured_item_count=10,
            failed_item_count=2,
            measured_duration_seconds=5.0,
            items_per_second=999.0,
        )


def test_throughput_summary_accepts_coherent_values() -> None:
    summary = RunnerThroughputSummary(
        measured_item_count=10,
        failed_item_count=2,
        measured_duration_seconds=5.0,
        items_per_second=2.0,
    )
    assert summary.items_per_second == 2.0


def recipe_payload(**overrides: object) -> dict[str, object]:
    """Return a valid preparation-recipe payload with optional overrides."""
    payload: dict[str, object] = {
        "recipe_id": "historical-print-v1",
        "pdf_page_image_mode": "auto",
        "render_dpi": 400,
        "color_mode": "grayscale",
        "deskew": False,
        "denoise": False,
        "crop_mode": "none",
        "binarize_mode": "none",
        "dewarp_mode": "none",
        "subdivision_overlap_px": 64,
        "fixed_tile_height_px": 1600,
        "thresholds": AssessmentThresholds().model_dump(),
        "notes": "Initial deterministic profile; calibrate from held-out gold.",
    }
    payload.update(overrides)
    return payload


@pytest.mark.parametrize(
    ("parent_prepared_page_id", "checksum"),
    [
        (None, "sha256:abc"),
        ("prepared-page-1", None),
        ("", "sha256:abc"),
        ("prepared-page-1", ""),
        ("   ", "sha256:abc"),
        ("prepared-page-1", "   "),
    ],
)
def test_prepared_unit_rejects_missing_or_empty_lineage_fields(
    parent_prepared_page_id: str | None,
    checksum: str | None,
) -> None:
    with pytest.raises(ValidationError, match="prepared units require"):
        PreparedArtifactRef(
            artifact_id="prep-unit-1",
            kind=InputKind.PREPARED_UNIT,
            page_id="page-0001",
            prepared_unit_id="col-1-part-1",
            artifact_path="pages/page-0001/image/col-1-part-1.png",
            parent_prepared_page_id=parent_prepared_page_id,
            checksum=checksum,
            order=1,
            bounding_box=BoundingBox(x0=0, y0=0, x1=1200, y1=3600),
        )


def test_page_override_requires_choice_and_reason() -> None:
    from bochord.models import PagePreparationOverride

    with pytest.raises(ValidationError):
        PagePreparationOverride(source_page_id="page-0002", reason=" ")


def test_operator_override_requires_reason() -> None:
    with pytest.raises(ValidationError):
        PreparationAssessment(
            assessment_id="assessment-page-1",
            source_page_id="page-0001",
            prepared_page_id=None,
            signals=[],
            flags=[],
            recommended_actions=[],
            warnings=[],
            page_class_suggested=PageClass.ORDINARY_PROSE,
            page_class_final=PageClass.DENSE_DICTIONARY,
            page_class_source="operator",
            operator_override_reason=None,
        )


def test_recipe_rejects_overlap_not_smaller_than_tile() -> None:
    payload = recipe_payload(subdivision_overlap_px=500, fixed_tile_height_px=500)
    with pytest.raises(ValidationError):
        PreparationRecipe.model_validate(payload)


def test_page_evaluation_has_exactly_three_top_level_families() -> None:
    summary = PageEvaluationSummary()
    assert set(summary.model_dump()) == {"text", "structure", "style"}
    assert set(summary.style.model_dump()) == {"typography", "note_linkage"}


def test_page_evaluation_record_carries_comparison_context() -> None:
    record = PageEvaluationRecord(
        run_id="run-1",
        document_id="bt",
        page_id="page-0001",
        page_class=PageClass.DENSE_DICTIONARY,
        preparation_mode=PreparationMode.COLUMNS,
        prepared_page_id="prepared-a",
        runner_id="olmocr",
        summary=PageEvaluationSummary(),
    )
    assert record.page_class is PageClass.DENSE_DICTIONARY
    assert record.preparation_mode is PreparationMode.COLUMNS


def test_cohort_records_fixture_validates() -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "evaluation" / "cohort-records.json"
    )
    records = TypeAdapter(list[PageEvaluationRecord]).validate_python(
        json.loads(fixture_path.read_text())
    )
    assert len(records) >= 2
    document_ids = {record.document_id for record in records}
    page_classes = {record.page_class for record in records}
    preparation_modes = {record.preparation_mode for record in records}
    runner_ids = {record.runner_id for record in records}
    assert len(document_ids) >= 2
    assert PageClass.ORDINARY_PROSE in page_classes
    assert PageClass.DENSE_DICTIONARY in page_classes
    assert PreparationMode.FULL_PAGE in preparation_modes
    assert PreparationMode.COLUMNS in preparation_modes
    assert "olmocr" in runner_ids
    assert "kraken" in runner_ids
    metrics = [
        metric
        for record in records
        for family in (
            record.summary.text,
            record.summary.structure,
            record.summary.style.typography,
            record.summary.style.note_linkage,
        )
        for metric in family.metrics
    ]
    assert any(
        metric.denominator is not None and metric.denominator > 1 for metric in metrics
    )


def test_evaluation_cohort_models_accept_fixed_report_shape() -> None:
    summary = PageEvaluationSummary()
    cohort_summary = EvaluationCohortSummary(
        key=EvaluationCohortKey(page_class=PageClass.ORDINARY_PROSE),
        document_ids=["doc-a"],
        page_ids=["page-0001"],
        summary=summary,
    )
    report = EvaluationCohortReport(
        by_page_class=[cohort_summary],
        by_page_class_and_preparation_mode=[
            EvaluationCohortSummary(
                key=EvaluationCohortKey(
                    page_class=PageClass.ORDINARY_PROSE,
                    preparation_mode=PreparationMode.FULL_PAGE,
                ),
                document_ids=["doc-a"],
                page_ids=["page-0001"],
                summary=summary,
            )
        ],
        by_page_class_and_runner=[
            EvaluationCohortSummary(
                key=EvaluationCohortKey(
                    page_class=PageClass.ORDINARY_PROSE,
                    runner_id="olmocr",
                ),
                document_ids=["doc-a"],
                page_ids=["page-0001"],
                summary=summary,
            )
        ],
    )
    assert report.by_page_class[0].key.page_class is PageClass.ORDINARY_PROSE
    assert (
        report.by_page_class_and_preparation_mode[0].key.preparation_mode
        is PreparationMode.FULL_PAGE
    )
    assert report.by_page_class_and_runner[0].key.runner_id == "olmocr"
