# Copyright (C) 2026 Chris Malek.
"""
Tests for review CLI orchestration service (apply / materialize / issue).

Includes default ``--run-id`` resolution for ``review issue``: bundle run id
when ``document-bundle.json`` exists, else ``run-review-issue``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wordwending.cli.cli import cli
from wordwending.models import (
    BundlePage,
    BundlePaths,
    CoordinateSpace,
    CorrectTextReviewEvent,
    DocumentBundle,
    EvaluationFamilySummary,
    EvaluationFlag,
    FlagSeverity,
    LineRecord,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PageEvaluationSummary,
    PageOverlay,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewAction,
    ReviewDimension,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
    SpanRecord,
    TrustState,
    WitnessReference,
)
from wordwending.models.merge import MergeFlagType
from wordwending.services.bundle_layout import BundleLayoutService
from wordwending.services.review_cli import ReviewCliService
from wordwending.services.review_overlay import ReviewOverlayService

_OVERLAY_FIXTURE = Path("tests/fixtures/review_overlay/page-overlay-v1.json")
_MINIMAL_BUNDLE_FIXTURE = Path(
    "tests/fixtures/bundle_layout/minimal_document.json"
)


def _provenance() -> ObjectProvenance:
    """Return minimal provenance for page-graph fixtures."""
    return ObjectProvenance(
        source_page_id="page-1",
        witness_ids=["wit-1"],
        runner_ids=["runner-1"],
    )


@pytest.fixture
def page() -> BundlePage:
    """Return a page graph with regions, spans, and a note for task targeting."""
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
        witnesses=[
            WitnessReference(
                witness_id="wit-1",
                witness_kind="text",
                artifact_path="pages/page-1/witnesses/text/runner-1.json",
                runner_id="runner-1",
                page_id="page-1",
            )
        ],
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                note_ids=["note-1"],
                provenance=provenance,
            ),
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
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
        ],
        notes=[
            NoteRecord(
                note_id="note-1",
                note_kind=NoteKind.FOOTNOTE_BLOCK,
                region_id="region-1",
                text_diplomatic="note body",
                linked_marker_span_ids=["span-1"],
                provenance=provenance,
            )
        ],
    )


def _text_task(*, target_object_ids: list[str]) -> ReviewTask:
    """Return a span-scoped text review task for validation fixtures."""
    return ReviewTask(
        task_id="task-text",
        task_type=ReviewTaskType.TEXT,
        dimensions=[ReviewDimension.TEXT],
        target_scope=ReviewScope.SPAN,
        target_object_ids=target_object_ids,
        related_object_ids=[],
        question="Inspect the target.",
        required_evidence=["prepared-page", "witness"],
        allowed_actions=[ReviewAction.ACCEPT, ReviewAction.CORRECT_TEXT],
        completion_criteria=["evidence inspected"],
        guideline_id="review",
        guideline_version="1.0.0",
        base_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
    )


def _gold_task() -> ReviewTask:
    """Return a gold task packet (unsupported by review apply)."""
    return ReviewTask(
        task_id="task-gold",
        task_type=ReviewTaskType.GOLD,
        dimensions=[ReviewDimension.TEXT],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        related_object_ids=[],
        question="Annotate gold.",
        required_evidence=["prepared-page"],
        allowed_actions=[ReviewAction.ACCEPT],
        completion_criteria=["coverage certified"],
        guideline_id="review",
        guideline_version="1.0.0",
        base_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
    )


def _overlay_with_tasks(tasks: list[ReviewTask]) -> PageOverlay:
    """Return a minimal PageOverlay carrying the given review tasks."""
    return PageOverlay(
        schema_version="1.0.0",
        overlay_id="overlay-test",
        page_id="page-1",
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:prepared",
        review_tasks=tasks,
        review_events=[],
        current_state=[],
    )


def _eval_flag(
    flag_type: str,
    target_object_ids: list[str],
    *,
    flag_id: str = "eval-1",
) -> EvaluationFlag:
    """Return one evaluation flag for pending-task regeneration fixtures."""
    return EvaluationFlag(
        flag_id=flag_id,
        flag_type=flag_type,
        severity=FlagSeverity.WARNING,
        message=f"{flag_type} on {target_object_ids}",
        target_object_ids=target_object_ids,
    )


def _write_page_graph(bundle_root: Path, page: BundlePage) -> None:
    """Overwrite one bundle page graph artifact on disk."""
    graph_path = BundlePaths(bundle_root).page_graph(page.page_number)
    graph_path.write_text(page.model_dump_json(indent=2), encoding="utf-8")


def _stage_minimal_bundle(bundle_root: Path, tmp_path: Path) -> None:
    """Write a minimal Spec 0002 bundle tree under ``bundle_root``."""
    inputs = tmp_path / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    source_pdf = inputs / "sample.pdf"
    source_pdf.write_bytes(b"%PDF-1.4 minimal")
    source_page = inputs / "page1.jp2"
    source_page.write_bytes(b"fake-jp2-bytes")
    prepared_image = inputs / "prepared.jp2"
    prepared_image.write_bytes(b"fake-prepared-bytes")
    witness_src = inputs / "olmocr-response.json"
    witness_src.write_text('{"text": "hello"}', encoding="utf-8")

    bundle = json.loads(_MINIMAL_BUNDLE_FIXTURE.read_text(encoding="utf-8"))
    BundleLayoutService().write_document_bundle(
        DocumentBundle.model_validate(bundle),
        bundle_root,
        source_files={"sample.pdf": source_pdf},
        source_page_images={1: source_page},
        page_images={"page-0001": prepared_image},
        witness_files={"wit-1": witness_src},
    )


def test_validate_overlay_tasks_rejects_unknown_object_ids(
    page: BundlePage,
) -> None:
    """Dedicated validation rejects text tasks whose span ids are absent."""
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    overlay = _overlay_with_tasks(
        [_text_task(target_object_ids=["span-missing"])]
    )

    with pytest.raises(ValueError, match="unknown"):
        service.validate_overlay_tasks(page, overlay)


def test_validate_overlay_tasks_rejects_gold_task_type(page: BundlePage) -> None:
    """GOLD tasks are not supported by review apply validation."""
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    overlay = _overlay_with_tasks([_gold_task()])

    with pytest.raises(ValueError, match="gold"):
        service.validate_overlay_tasks(page, overlay)


def test_validate_overlay_tasks_accepts_known_text_targets(
    page: BundlePage,
) -> None:
    """Known span ids pass dedicated overlay-task validation."""
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )
    overlay = _overlay_with_tasks([_text_task(target_object_ids=["span-1"])])

    service.validate_overlay_tasks(page, overlay)


def test_apply_appends_events_and_writes_state(tmp_path: Path) -> None:
    """Apply appends new events and materializes overlay state on disk."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    overlay = PageOverlay.model_validate_json(
        _OVERLAY_FIXTURE.read_text(encoding="utf-8")
    )
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )

    result = service.apply(bundle_root, overlay, page_id="page-0001")

    assert result.page_id == "page-0001"
    assert result.events_appended == len(overlay.review_events)
    assert len(result.states) == len(
        ReviewOverlayService().materialize(overlay)
    )
    review_path = (
        bundle_root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    )
    state_path = (
        bundle_root / "pages" / "page-0001" / "overlays" / "current_state.json"
    )
    assert review_path.exists()
    assert state_path.exists()


def test_apply_rejects_unknown_task_object_ids(tmp_path: Path) -> None:
    """Apply refuses overlays whose task targets are missing from the page."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    overlay = PageOverlay.model_validate_json(
        _OVERLAY_FIXTURE.read_text(encoding="utf-8")
    )
    text_task = next(
        task
        for task in overlay.review_tasks
        if task.task_type == ReviewTaskType.TEXT
    )
    bad_task = text_task.model_copy(
        update={"target_object_ids": ["span-does-not-exist"]}
    )
    # Clear events so PageOverlay event/task binding does not preempt the
    # apply-time page-graph check for unknown task target ids.
    bad_overlay = overlay.model_copy(
        update={
            "review_tasks": [bad_task],
            "review_events": [],
            "current_state": [],
        }
    )
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )

    with pytest.raises(ValueError, match="unknown"):
        service.apply(bundle_root, bad_overlay, page_id="page-0001")


def test_issue_rebuilds_pending_tasks_from_evaluation_flags(
    tmp_path: Path,
) -> None:
    """Issue regenerates pending_tasks.json from the page evaluation flags."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    flagged = page.model_copy(
        update={
            "graph_revision": "graph-v0",
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[
                        _eval_flag(
                            str(MergeFlagType.TEXT_DISAGREEMENT),
                            ["span-1"],
                        )
                    ]
                )
            ),
        }
    )
    _write_page_graph(bundle_root, flagged)
    service = ReviewCliService(
        layout=layout,
        replay=ReviewOverlayService(),
    )

    result = service.issue(bundle_root, "page-0001", run_id="run-test")

    assert result.page_id == "page-0001"
    assert result.task_count == 1
    tasks = layout.read_pending_review_tasks(bundle_root, 1)
    assert len(tasks) == 1
    assert tasks[0].task_type == ReviewTaskType.TEXT
    assert tasks[0].target_object_ids == ["span-1"]
    assert tasks[0].base_run_id == "run-test"
    assert tasks[0].base_graph_revision == "graph-v0"


def test_issue_writes_empty_pending_tasks_when_no_flags(
    tmp_path: Path,
) -> None:
    """Issue writes an empty pending_tasks.json list when flags are absent."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    cleared = page.model_copy(
        update={"evaluation_summary": PageEvaluationSummary()}
    )
    _write_page_graph(bundle_root, cleared)
    service = ReviewCliService(
        layout=layout,
        replay=ReviewOverlayService(),
    )

    result = service.issue(bundle_root, "page-0001", run_id="run-test")

    assert result.task_count == 0
    assert layout.read_pending_review_tasks(bundle_root, 1) == []


def test_issue_rejects_unknown_page_id(tmp_path: Path) -> None:
    """Issue fails when the bundle has no matching page id."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    service = ReviewCliService(
        layout=BundleLayoutService(),
        replay=ReviewOverlayService(),
    )

    with pytest.raises(ValueError, match="page-9999"):
        service.issue(bundle_root, "page-9999", run_id="run-test")


def test_review_issue_cli_echoes_task_count(runner, tmp_path: Path) -> None:
    """CLI review issue writes pending tasks and echoes the task count."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    flagged = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[
                        _eval_flag(
                            str(MergeFlagType.TEXT_DISAGREEMENT),
                            ["span-1"],
                        )
                    ]
                )
            ),
        }
    )
    _write_page_graph(bundle_root, flagged)

    result = runner.invoke(
        cli,
        [
            "review",
            "issue",
            "--bundle-root",
            str(bundle_root),
            "--page-id",
            "page-0001",
            "--run-id",
            "run-cli-test",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "page_id: page-0001" in result.output
    assert "tasks: 1" in result.output
    tasks = layout.read_pending_review_tasks(bundle_root, 1)
    assert len(tasks) == 1
    assert tasks[0].base_run_id == "run-cli-test"


def test_review_issue_cli_defaults_run_id_from_document_bundle(
    runner, tmp_path: Path
) -> None:
    """Omitting --run-id uses document-bundle.json run id for task base_run_id."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    (bundle_root / "document-bundle.json").write_text(
        _MINIMAL_BUNDLE_FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    flagged = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[
                        _eval_flag(
                            str(MergeFlagType.TEXT_DISAGREEMENT),
                            ["span-1"],
                        )
                    ]
                )
            ),
        }
    )
    _write_page_graph(bundle_root, flagged)

    result = runner.invoke(
        cli,
        [
            "review",
            "issue",
            "--bundle-root",
            str(bundle_root),
            "--page-id",
            "page-0001",
        ],
    )

    assert result.exit_code == 0, result.output
    tasks = layout.read_pending_review_tasks(bundle_root, 1)
    assert len(tasks) == 1
    assert tasks[0].base_run_id == "run-minimal"


def test_review_issue_cli_defaults_run_id_when_bundle_json_absent(
    runner, tmp_path: Path
) -> None:
    """Omitting --run-id without document-bundle.json uses run-review-issue."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    assert not (bundle_root / "document-bundle.json").exists()
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    flagged = page.model_copy(
        update={
            "evaluation_summary": PageEvaluationSummary(
                text=EvaluationFamilySummary(
                    flags=[
                        _eval_flag(
                            str(MergeFlagType.TEXT_DISAGREEMENT),
                            ["span-1"],
                        )
                    ]
                )
            ),
        }
    )
    _write_page_graph(bundle_root, flagged)

    result = runner.invoke(
        cli,
        [
            "review",
            "issue",
            "--bundle-root",
            str(bundle_root),
            "--page-id",
            "page-0001",
        ],
    )

    assert result.exit_code == 0, result.output
    tasks = layout.read_pending_review_tasks(bundle_root, 1)
    assert len(tasks) == 1
    assert tasks[0].base_run_id == "run-review-issue"


def _text_correction_overlay(
    *,
    page_id: str = "page-0001",
    graph_revision: str = "graph-v0",
    run_id: str = "run-minimal",
    text_diplomatic: str = "emended",
) -> PageOverlay:
    """Return a one-event overlay that corrects span-1 diplomatic text."""
    task = ReviewTask(
        task_id="task-text",
        task_type=ReviewTaskType.TEXT,
        dimensions=[ReviewDimension.TEXT],
        target_scope=ReviewScope.SPAN,
        target_object_ids=["span-1"],
        related_object_ids=[],
        question="Correct the span text.",
        required_evidence=["prepared-page", "witness"],
        allowed_actions=[ReviewAction.ACCEPT, ReviewAction.CORRECT_TEXT],
        completion_criteria=["evidence inspected"],
        guideline_id="review",
        guideline_version="1.0.0",
        base_run_id=run_id,
        base_graph_revision=graph_revision,
        prepared_image_checksum="sha256:prepared",
    )
    event = CorrectTextReviewEvent(
        event_id="evt-text-correct",
        task_id="task-text",
        target_object_id="span-1",
        target_scope=ReviewScope.SPAN,
        review_dimensions=[ReviewDimension.TEXT],
        base_run_id=run_id,
        base_graph_revision=graph_revision,
        guideline_version="1.0.0",
        prior_trust_state=TrustState.MACHINE,
        new_trust_state=TrustState.CORRECTED,
        operator_id="editor-1",
        timestamp_utc="2026-08-07T00:00:00Z",
        action=ReviewAction.CORRECT_TEXT,
        text_diplomatic=text_diplomatic,
    )
    return PageOverlay(
        schema_version="1.0.0",
        overlay_id="overlay-correct-v1",
        page_id=page_id,
        source_run_id=run_id,
        base_graph_revision=graph_revision,
        prepared_image_checksum="sha256:prepared",
        review_tasks=[task],
        review_events=[event],
        current_state=[],
    )


def _write_document_bundle_json(bundle_root: Path, page: BundlePage) -> None:
    """Persist document-bundle.json with one accepted page for export."""
    fixture = json.loads(_MINIMAL_BUNDLE_FIXTURE.read_text(encoding="utf-8"))
    fixture["pages"] = [json.loads(page.model_dump_json())]
    (bundle_root / "document-bundle.json").write_text(
        json.dumps(fixture, indent=2),
        encoding="utf-8",
    )


def test_rebase_apply_export_sees_corrected_text(tmp_path: Path, runner) -> None:
    """
    Apply text correction, rebase into the page graph, then export sees it.

    JSONL history stays append-only; successor overlay binds the new revision.
    """
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    page = page.model_copy(update={"graph_revision": "graph-v0"})
    assert page.spans[0].text_diplomatic == "hello"
    _write_page_graph(bundle_root, page)
    _write_document_bundle_json(bundle_root, page)

    overlay = _text_correction_overlay()
    service = ReviewCliService(
        layout=layout,
        replay=ReviewOverlayService(),
    )
    apply_result = service.apply(bundle_root, overlay, page_id="page-0001")
    assert apply_result.events_appended == 1

    review_events_path = BundlePaths(bundle_root).review_events(1)
    jsonl_before = review_events_path.read_bytes()

    rebase_result = service.rebase(bundle_root, "page-0001")

    assert rebase_result.old_graph_revision == "graph-v0"
    assert rebase_result.new_graph_revision == "graph-v1"
    assert review_events_path.read_bytes() == jsonl_before

    rebased_page = layout.read_page_graph(bundle_root, 1)
    assert rebased_page.spans[0].text_diplomatic == "emended"
    assert rebased_page.graph_revision == "graph-v1"

    successor_path = BundlePaths(bundle_root).page_overlay_path(1)
    assert successor_path.exists()
    successor = PageOverlay.model_validate_json(
        successor_path.read_text(encoding="utf-8")
    )
    assert successor.base_graph_revision == "graph-v1"
    assert successor.predecessor_overlay_id == "overlay-correct-v1"

    doc_bundle = DocumentBundle.model_validate_json(
        (bundle_root / "document-bundle.json").read_text(encoding="utf-8")
    )
    assert doc_bundle.pages[0].spans[0].text_diplomatic == "emended"
    assert doc_bundle.pages[0].graph_revision == "graph-v1"

    export = runner.invoke(
        cli,
        [
            "export",
            str(bundle_root / "document-bundle.json"),
            "--bundle-root",
            str(bundle_root),
        ],
    )
    assert export.exit_code == 0, export.output
    markdown = (bundle_root / "exports" / "document.md").read_text(encoding="utf-8")
    assert "emended" in markdown
    assert "hello" not in markdown.split("## Notes")[0]


def test_rebase_drops_pending_tasks_whose_targets_vanished(
    tmp_path: Path,
) -> None:
    """Pending tasks rebound to the new revision; vanished targets are dropped."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    page = page.model_copy(update={"graph_revision": "graph-v0"})
    _write_page_graph(bundle_root, page)
    _write_document_bundle_json(bundle_root, page)

    keep = _text_task(target_object_ids=["span-1"]).model_copy(
        update={
            "task_id": "task-keep",
            "base_graph_revision": "graph-v0",
            "base_run_id": "run-minimal",
            "prepared_image_checksum": "sha256:prepared",
        }
    )
    drop = _text_task(target_object_ids=["span-gone"]).model_copy(
        update={
            "task_id": "task-drop",
            "base_graph_revision": "graph-v0",
            "base_run_id": "run-minimal",
            "prepared_image_checksum": "sha256:prepared",
        }
    )
    layout.write_pending_review_tasks(bundle_root, 1, [keep, drop])

    overlay = _text_correction_overlay()
    service = ReviewCliService(
        layout=layout,
        replay=ReviewOverlayService(),
    )
    service.apply(bundle_root, overlay, page_id="page-0001")
    service.rebase(bundle_root, "page-0001")

    pending = layout.read_pending_review_tasks(bundle_root, 1)
    assert len(pending) == 1
    assert pending[0].task_id == "task-keep"
    assert pending[0].base_graph_revision == "graph-v1"
    assert pending[0].target_object_ids == ["span-1"]


def test_review_rebase_cli_echoes_revision_bump(runner, tmp_path: Path) -> None:
    """CLI review rebase echoes old → new graph revision."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_minimal_bundle(bundle_root, tmp_path)
    layout = BundleLayoutService()
    page = layout.read_page_graph(bundle_root, 1)
    page = page.model_copy(update={"graph_revision": "graph-v0"})
    _write_page_graph(bundle_root, page)
    _write_document_bundle_json(bundle_root, page)

    service = ReviewCliService(
        layout=layout,
        replay=ReviewOverlayService(),
    )
    service.apply(bundle_root, _text_correction_overlay(), page_id="page-0001")

    result = runner.invoke(
        cli,
        [
            "review",
            "rebase",
            "--bundle-root",
            str(bundle_root),
            "--page-id",
            "page-0001",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "page_id: page-0001" in result.output
    assert "graph_revision: graph-v0 -> graph-v1" in result.output
