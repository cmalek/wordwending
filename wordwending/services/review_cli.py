# Copyright (C) 2026 Chris Malek.
"""Review CLI orchestration: validate overlays, append events, materialize state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path  # noqa: TC003

from pydantic import TypeAdapter

from wordwending.models import (
    BundlePage,
    OverlayState,
    PageOverlay,
    ReviewEvent,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
)
from wordwending.services.bundle_layout import BundleLayoutService  # noqa: TC001
from wordwending.services.review_overlay import ReviewOverlayService  # noqa: TC001

#: Parses one JSONL review-event payload into a validated event model.
_REVIEW_EVENT_ADAPTER: TypeAdapter[ReviewEvent] = TypeAdapter(ReviewEvent)

#: Human-readable labels for review target scopes used in validation errors.
_SCOPE_LABELS: dict[ReviewScope, str] = {
    ReviewScope.SPAN: "span ids",
    ReviewScope.REGION: "region ids",
    ReviewScope.NOTE: "note ids",
    ReviewScope.PAGE: "page ids",
}


@dataclass(frozen=True)
class ReviewApplyResult:
    """
    Outcome of appending overlay events and rewriting overlay state.

    """

    #: Stable page identifier that was updated.
    page_id: str
    #: Count of newly appended JSONL review events.
    events_appended: int
    #: Materialized overlay states written for the page.
    states: list[OverlayState]


@dataclass(frozen=True)
class ReviewMaterializeResult:
    """
    Outcome of replaying append-only review history into overlay state.

    """

    #: Stable page identifier whose history was replayed.
    page_id: str
    #: Materialized overlay states written for the page.
    states: list[OverlayState]


class ReviewCliService:
    """
    Orchestrate review apply / materialize for document bundle pages.

    Keeps Click handlers thin: load args, call this service, echo or raise.
    Append-only ``review_events.jsonl`` behavior is preserved (ADR 0008).

    Args:
        layout: Bundle layout reader/writer for manifests, graphs, and overlays.
        replay: Overlay replay service that materializes ``OverlayState`` rows.

    """

    def __init__(
        self,
        layout: BundleLayoutService,
        replay: ReviewOverlayService,
    ) -> None:
        """
        Bind layout and replay collaborators for one CLI session.

        Args:
            layout: Bundle layout reader/writer for manifests, graphs, and overlays.
            replay: Overlay replay service that materializes ``OverlayState`` rows.

        """
        #: Bundle layout reader/writer for manifests, graphs, and overlays.
        self.layout = layout
        #: Overlay replay service that materializes ``OverlayState`` rows.
        self.replay = replay

    def apply(
        self,
        bundle_root: Path,
        overlay: PageOverlay,
        page_id: str,
    ) -> ReviewApplyResult:
        """
        Validate an overlay, append new events, and rewrite overlay state.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            overlay: Validated PageOverlay submission from the operator.
            page_id: Stable page identifier that must match ``overlay.page_id``.

        Returns:
            Append counts and materialized states for operator reporting.

        Side Effects:
            Appends new events to ``overlays/review_events.jsonl`` and overwrites
            ``overlays/current_state.json`` from the full append-only history.

        Raises:
            ValueError: If page id, task targets, or bundle membership fail checks.
            OSError: If bundle reads or writes fail.
            ValidationError: If stored JSONL events fail model validation.

        """
        self._ensure_overlay_page_id(overlay, page_id)
        page_number = self._resolve_page_number(bundle_root, page_id)
        page = self.layout.read_page_graph(bundle_root, page_number)
        self.validate_overlay_tasks(page, overlay)
        events_appended = self._append_new_review_events(
            bundle_root,
            page_number,
            overlay.review_events,
        )
        states = self._materialize_review_states(
            bundle_root,
            page_number,
            page_id,
        )
        self.layout.write_overlay_state(bundle_root, page_number, states)
        return ReviewApplyResult(
            page_id=page_id,
            events_appended=events_appended,
            states=states,
        )

    def materialize(
        self,
        bundle_root: Path,
        page_id: str,
    ) -> ReviewMaterializeResult:
        """
        Replay append-only review history into ``overlays/current_state.json``.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_id: Stable page identifier whose review history is replayed.

        Returns:
            Materialized states for operator reporting.

        Side Effects:
            Overwrites ``overlays/current_state.json`` from ``review_events.jsonl``.

        Raises:
            ValueError: If the bundle has no page matching ``page_id``.
            OSError: If bundle reads or writes fail.
            ValidationError: If stored JSONL events fail model validation.

        """
        page_number = self._resolve_page_number(bundle_root, page_id)
        states = self._materialize_review_states(
            bundle_root,
            page_number,
            page_id,
        )
        self.layout.write_overlay_state(bundle_root, page_number, states)
        return ReviewMaterializeResult(page_id=page_id, states=states)

    def validate_overlay_tasks(
        self,
        page: BundlePage,
        overlay: PageOverlay,
    ) -> None:
        """
        Ensure overlay task targets exist on the accepted page graph.

        Validation is dedicated (not a ``HumanMarkupService.create_*``
        side-channel): each task type maps to the same id kind rules the
        packet factories enforce, plus an explicit GOLD rejection.

        Args:
            page: Accepted page graph for the bundle page.
            overlay: Overlay whose task packets are being applied.

        Raises:
            ValueError: If a task is unsupported or a target id is absent.

        """
        for task in overlay.review_tasks:
            self.validate_task_targets(page, task)

    def validate_task_targets(self, page: BundlePage, task: ReviewTask) -> None:
        """
        Validate one review task's targets against the page graph.

        Args:
            page: Accepted page graph for the bundle page.
            task: Review task whose target ids must resolve on ``page``.

        Raises:
            ValueError: If ``task`` is unsupported or references unknown ids.

        """
        if task.task_type == ReviewTaskType.GOLD:
            msg = (
                f"review task type {task.task_type.value!r} is not supported "
                "by review apply; gold annotation is out of band for overlay apply"
            )
            raise ValueError(msg)

        if (
            task.task_type == ReviewTaskType.LAYOUT
            and task.target_scope != ReviewScope.REGION
        ):
            self._require_known_ids_for_scope(page, task)
            return

        if task.task_type == ReviewTaskType.TEXT:
            self._require_known_ids(
                task.target_object_ids,
                {span.span_id for span in page.spans},
                "text review targets must be span ids",
            )
            return

        if task.task_type == ReviewTaskType.LAYOUT:
            self._require_known_ids(
                task.target_object_ids,
                {region.region_id for region in page.regions},
                "layout review targets must be region ids",
            )
            return

        if task.task_type == ReviewTaskType.TYPOGRAPHY:
            self._require_known_ids(
                task.target_object_ids,
                {span.span_id for span in page.spans},
                "typography review targets must be span ids",
            )
            return

        if task.task_type == ReviewTaskType.NOTE_LINKAGE:
            self._require_known_ids(
                task.target_object_ids,
                {note.note_id for note in page.notes},
                "note-linkage review targets must be note ids",
            )
            if task.related_object_ids:
                self._require_known_ids(
                    task.related_object_ids,
                    {span.span_id for span in page.spans},
                    "note-linkage related_object_ids must be span ids",
                )
            return

        if task.task_type in {
            ReviewTaskType.SOURCE_TRIAGE,
            ReviewTaskType.PREPARATION,
            ReviewTaskType.ADJUDICATION,
        }:
            self._require_known_ids_for_scope(page, task)
            return

        msg = f"unsupported review task type {task.task_type.value!r}"
        raise ValueError(msg)

    def _ensure_overlay_page_id(self, overlay: PageOverlay, page_id: str) -> None:
        """
        Reject overlay submissions whose page id does not match the CLI flag.

        Args:
            overlay: Overlay loaded from the operator submission file.
            page_id: Page id supplied on the command line.

        Raises:
            ValueError: If ``overlay.page_id`` differs from ``page_id``.

        """
        if overlay.page_id != page_id:
            msg = (
                f"overlay page_id {overlay.page_id!r} "
                f"does not match --page-id {page_id!r}"
            )
            raise ValueError(msg)

    def _resolve_page_number(self, bundle_root: Path, page_id: str) -> int:
        """
        Resolve one bundle page number from its stable page id.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_id: Stable page identifier to locate.

        Returns:
            1-based page index within the document bundle.

        Raises:
            ValueError: If no page manifest matches ``page_id``.

        """
        document = self.layout.read_document_manifest(bundle_root)
        for page_number in range(1, document.page_count + 1):
            manifest = self.layout.read_page_manifest(bundle_root, page_number)
            if manifest.page_id == page_id:
                return page_number
        msg = f"bundle has no page with page_id {page_id!r}"
        raise ValueError(msg)

    def _append_new_review_events(
        self,
        bundle_root: Path,
        page_number: int,
        events: list[ReviewEvent],
    ) -> int:
        """
        Append only review events whose ids are not already recorded.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.
            events: Candidate review events from one overlay submission.

        Returns:
            Count of events appended to ``review_events.jsonl``.

        Side Effects:
            Appends new events to the page's append-only JSONL history.

        """
        existing_ids = {
            event["event_id"]
            for event in self.layout.read_review_events(bundle_root, page_number)
            if "event_id" in event
        }
        new_events = [event for event in events if event.event_id not in existing_ids]
        self.layout.append_review_events(bundle_root, page_number, new_events)
        return len(new_events)

    def _materialize_review_states(
        self,
        bundle_root: Path,
        page_number: int,
        page_id: str,
    ) -> list[OverlayState]:
        """
        Replay append-only review history for one page.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.
            page_id: Stable page identifier used for replay scaffolding.

        Returns:
            Materialized overlay states for reviewed objects.

        """
        events = [
            _REVIEW_EVENT_ADAPTER.validate_python(item)
            for item in self.layout.read_review_events(bundle_root, page_number)
        ]
        # model_construct bypasses task-binding validators: JSONL-only replay
        # has no task packets, and events were validated on original apply.
        overlay = PageOverlay.model_construct(
            schema_version="1.0.0",
            overlay_id="cli-replay",
            page_id=page_id,
            source_run_id="cli-replay",
            base_graph_revision="cli-replay",
            prepared_image_checksum="cli-replay",
            review_events=events,
            review_tasks=[],
            current_state=[],
        )
        return self.replay.materialize(overlay)

    def _require_known_ids_for_scope(
        self,
        page: BundlePage,
        task: ReviewTask,
    ) -> None:
        """
        Validate task target ids against the page graph for one review scope.

        Args:
            page: Accepted page graph for the bundle page.
            task: Review task whose target ids must resolve on ``page``.

        Raises:
            ValueError: If any target id is absent from ``page``.

        """
        known = self._known_ids_for_scope(page, task.target_scope)
        label = _SCOPE_LABELS[task.target_scope]
        self._require_known_ids(task.target_object_ids, known, label)

    @staticmethod
    def _known_ids_for_scope(page: BundlePage, scope: ReviewScope) -> set[str]:
        """
        Return page-graph identifiers for one review target scope.

        Args:
            page: Accepted page graph for the bundle page.
            scope: Review target scope whose id set is requested.

        Returns:
            Identifier set present on ``page`` for ``scope``.

        Raises:
            ValueError: If ``scope`` is not a supported review target scope.

        """
        if scope == ReviewScope.SPAN:
            return {span.span_id for span in page.spans}
        if scope == ReviewScope.REGION:
            return {region.region_id for region in page.regions}
        if scope == ReviewScope.NOTE:
            return {note.note_id for note in page.notes}
        if scope == ReviewScope.PAGE:
            return {page.page_id}
        msg = f"unsupported review target scope {scope.value!r}"
        raise ValueError(msg)

    @staticmethod
    def _require_known_ids(
        object_ids: list[str],
        known_ids: set[str],
        message_prefix: str,
    ) -> None:
        """
        Reject empty or unknown object identifiers for a review task.

        Args:
            object_ids: Candidate identifiers supplied by the task packet.
            known_ids: Identifiers present on the accepted page graph.
            message_prefix: Human-readable prefix for validation errors.

        Raises:
            ValueError: If the id list is empty or contains unknown ids.

        """
        if not object_ids:
            msg = f"{message_prefix}; must not be empty"
            raise ValueError(msg)
        unknown = sorted(
            {object_id for object_id in object_ids if object_id not in known_ids}
        )
        if unknown:
            msg = f"{message_prefix}; unknown: {unknown}"
            raise ValueError(msg)
