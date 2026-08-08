# Copyright (C) 2026 Chris Malek.
"""Review CLI orchestration: validate overlays, append events, materialize state."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path  # noqa: TC003

from pydantic import TypeAdapter

from wordwending.models import (
    BundlePage,
    DocumentBundle,
    OverlayState,
    PageOverlay,
    ReviewEvent,
    ReviewScope,
    ReviewTask,
    ReviewTaskType,
)
from wordwending.services.assemble import DOCUMENT_BUNDLE_JSON
from wordwending.services.bundle_layout import BundleLayoutService  # noqa: TC001
from wordwending.services.graph_rebase import GraphRebaseService
from wordwending.services.review_markup import HumanMarkupService
from wordwending.services.review_overlay import (
    ReviewOverlayService,
    _coordinate_space_ids,
    _nested_object_ids,
)

#: Parses one JSONL review-event payload into a validated event model.
_REVIEW_EVENT_ADAPTER: TypeAdapter[ReviewEvent] = TypeAdapter(ReviewEvent)

#: Human-readable labels for review target scopes used in validation errors.
_SCOPE_LABELS: dict[ReviewScope, str] = {
    ReviewScope.SPAN: "span ids",
    ReviewScope.REGION: "region ids",
    ReviewScope.NOTE: "note ids",
    ReviewScope.PAGE: "page ids",
}
#: Review guideline family stamped onto CLI-issued Spec 0005 packets.
_REVIEW_GUIDELINE_ID = "review-v1"
#: Review guideline revision stamped onto CLI-issued Spec 0005 packets.
_REVIEW_GUIDELINE_VERSION = "1.0.0"
#: Default run id when ``review issue`` has no ``--run-id`` and no bundle JSON.
_DEFAULT_ISSUE_RUN_ID = "run-review-issue"
#: Suffix stamped onto successor overlay / task / event ids after rebase.
_REBASED_ID_SUFFIX = "-rebased"


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


@dataclass(frozen=True)
class ReviewIssueResult:
    """
    Outcome of regenerating pending review tasks from evaluation flags.

    """

    #: Stable page identifier whose pending queue was rewritten.
    page_id: str
    #: Count of Spec 0005 review tasks written to ``pending_tasks.json``.
    task_count: int


@dataclass(frozen=True)
class ReviewRebaseResult:
    """
    Outcome of rebasing overlay corrections onto the accepted page graph.

    """

    #: Stable page identifier whose graph was rebased.
    page_id: str
    #: Graph revision before rebase.
    old_graph_revision: str
    #: Graph revision written after rebase.
    new_graph_revision: str


class ReviewCliService:
    """
    Orchestrate review apply / materialize / issue / rebase for bundle pages.

    Keeps Click handlers thin: load args, call this service, echo or raise.
    Append-only ``review_events.jsonl`` behavior is preserved (ADR 0008).

    Args:
        layout: Bundle layout reader/writer for manifests, graphs, and overlays.
        replay: Overlay replay service that materializes ``OverlayState`` rows.
        graph_rebase: Applies materialized overlay states onto page graphs.

    """

    def __init__(
        self,
        layout: BundleLayoutService,
        replay: ReviewOverlayService,
        graph_rebase: GraphRebaseService | None = None,
    ) -> None:
        """
        Bind layout and replay collaborators for one CLI session.

        Args:
            layout: Bundle layout reader/writer for manifests, graphs, and overlays.
            replay: Overlay replay service that materializes ``OverlayState`` rows.
            graph_rebase: Optional graph rebase collaborator; defaults to a new
                ``GraphRebaseService``.

        """
        #: Bundle layout reader/writer for manifests, graphs, and overlays.
        self.layout = layout
        #: Overlay replay service that materializes ``OverlayState`` rows.
        self.replay = replay
        #: Applies materialized overlay states onto accepted page graphs.
        self.graph_rebase = graph_rebase or GraphRebaseService()

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
        # Snapshot the applied Spec 0014 overlay for successor rebase (ADR 0008).
        # Does not rewrite append-only JSONL history.
        self.layout.write_page_overlay(
            bundle_root,
            page_number,
            overlay.model_copy(update={"current_state": states}),
        )
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

    def issue(
        self,
        bundle_root: Path,
        page_id: str,
        *,
        run_id: str | None = None,
    ) -> ReviewIssueResult:
        """
        Rebuild pending review tasks from one page's evaluation flags.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_id: Stable page identifier whose flags drive the queue.

        Keyword Args:
            run_id: Machine run stamped onto each task; defaults from bundle
                ``document-bundle.json`` when present, else ``run-review-issue``.

        Returns:
            Page id and task count for operator reporting.

        Side Effects:
            Overwrites ``overlays/pending_tasks.json`` for the page.

        Raises:
            ValueError: If the bundle has no page matching ``page_id``.
            OSError: If bundle reads or writes fail.
            ValidationError: If stored page graph JSON fails model validation.

        """
        page_number = self._resolve_page_number(bundle_root, page_id)
        page = self.layout.read_page_graph(bundle_root, page_number)
        resolved_run_id = self._resolve_issue_run_id(bundle_root, run_id)
        markup = HumanMarkupService(
            _REVIEW_GUIDELINE_ID,
            _REVIEW_GUIDELINE_VERSION,
        )
        tasks = markup.build_review_tasks(
            page,
            run_id=resolved_run_id,
            graph_revision=page.graph_revision,
        )
        self.layout.write_pending_review_tasks(bundle_root, page_number, tasks)
        return ReviewIssueResult(page_id=page_id, task_count=len(tasks))

    def rebase(
        self,
        bundle_root: Path,
        page_id: str,
        *,
        graph_revision: str | None = None,
    ) -> ReviewRebaseResult:
        """
        Apply overlay corrections onto the page graph and write a successor overlay.

        Materializes states from append-only ``review_events.jsonl`` without
        rewriting that history. Leaf overrides land on ``page_graph.json`` and
        ``document-bundle.json``; a Spec 0014 successor overlay is written to
        ``overlays/page_overlay.json`` with rebound ``base_graph_revision``.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_id: Stable page identifier to rebase.

        Keyword Args:
            graph_revision: Explicit successor graph revision; when omitted,
                bumps a trailing integer on the current revision.

        Returns:
            Old and new graph revisions for operator reporting.

        Side Effects:
            Overwrites page graph, document-bundle page entry (when present),
            ``overlays/page_overlay.json``, ``overlays/current_state.json``, and
            ``overlays/pending_tasks.json``. Does not rewrite
            ``review_events.jsonl``.

        Raises:
            ValueError: If the page, overlay snapshot, or rebase inputs fail.
            OSError: If bundle reads or writes fail.
            ValidationError: If stored JSON fails model validation.
            FileNotFoundError: If ``overlays/page_overlay.json`` is missing.

        """
        page_number = self._resolve_page_number(bundle_root, page_id)
        page = self.layout.read_page_graph(bundle_root, page_number)
        old_revision = page.graph_revision
        new_revision = graph_revision or _bump_graph_revision(old_revision)
        states = self._materialize_review_states(
            bundle_root,
            page_number,
            page_id,
        )
        rebased = self.graph_rebase.rebase_page(
            page,
            states,
            new_graph_revision=new_revision,
        )
        self.layout.write_page_graph(bundle_root, page_number, rebased)
        self.layout.update_document_bundle_page(bundle_root, rebased)

        predecessor = self.layout.read_page_overlay(bundle_root, page_number)
        successor = self._build_successor_overlay(
            predecessor,
            rebased,
            new_graph_revision=new_revision,
        )
        self.layout.write_page_overlay(bundle_root, page_number, successor)
        self.layout.write_overlay_state(
            bundle_root,
            page_number,
            successor.current_state,
        )
        self._rewrite_pending_tasks_for_rebased_page(
            bundle_root,
            page_number,
            rebased,
            new_graph_revision=new_revision,
        )
        return ReviewRebaseResult(
            page_id=page_id,
            old_graph_revision=old_revision,
            new_graph_revision=new_revision,
        )

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

    def _resolve_issue_run_id(
        self,
        bundle_root: Path,
        run_id: str | None,
    ) -> str:
        """
        Resolve the run id stamped onto regenerated pending review tasks.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            run_id: Explicit operator override from ``--run-id`` when set.

        Returns:
            Run id for ``ReviewTask.base_run_id``.

        """
        if run_id is not None:
            return run_id
        doc_bundle_path = bundle_root / DOCUMENT_BUNDLE_JSON
        if doc_bundle_path.is_file():
            bundle = DocumentBundle.model_validate_json(
                doc_bundle_path.read_text(encoding="utf-8")
            )
            return bundle.run.run_id
        return _DEFAULT_ISSUE_RUN_ID

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

    def _build_successor_overlay(
        self,
        predecessor: PageOverlay,
        page: BundlePage,
        *,
        new_graph_revision: str,
    ) -> PageOverlay:
        """
        Build an ADR 0008 successor overlay bound to ``new_graph_revision``.

        Leaf-only rebase keeps object ids stable (identity maps). Task and event
        ids gain a ``-rebased`` suffix so the successor is distinct.

        Args:
            predecessor: Current Spec 0014 overlay snapshot before rebase.
            page: Rebased page graph (object-id source for identity maps).

        Keyword Args:
            new_graph_revision: Successor ``base_graph_revision``.

        Returns:
            Successor overlay with rebound events and materialized state.

        """
        object_id_map = _identity_object_id_map(page, predecessor.review_events)
        resolvable_spaces = {page.prepared_page.coordinate_space.space_id}
        for event in predecessor.review_events:
            resolvable_spaces.update(_coordinate_space_ids(event))
        successor_tasks = [
            task.model_copy(
                update={
                    "task_id": f"{task.task_id}{_REBASED_ID_SUFFIX}",
                    "base_graph_revision": new_graph_revision,
                }
            )
            for task in predecessor.review_tasks
        ]
        task_id_map = {
            task.task_id: f"{task.task_id}{_REBASED_ID_SUFFIX}"
            for task in predecessor.review_tasks
        }
        event_id_map = {
            event.event_id: f"{event.event_id}{_REBASED_ID_SUFFIX}"
            for event in predecessor.review_events
        }
        return self.replay.create_successor(
            predecessor,
            new_overlay_id=f"{predecessor.overlay_id}{_REBASED_ID_SUFFIX}",
            successor_tasks=successor_tasks,
            task_id_map=task_id_map,
            object_id_map=object_id_map,
            resolvable_coordinate_space_ids=resolvable_spaces,
            event_id_map=event_id_map,
            conflict_tasks=[],
        )

    def _rewrite_pending_tasks_for_rebased_page(
        self,
        bundle_root: Path,
        page_number: int,
        page: BundlePage,
        *,
        new_graph_revision: str,
    ) -> None:
        """
        Rebind open pending tasks to the new revision; drop vanished targets.

        Args:
            bundle_root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.
            page: Rebased page graph used for target existence checks.

        Keyword Args:
            new_graph_revision: Revision stamped onto retained tasks.

        Side Effects:
            Overwrites ``overlays/pending_tasks.json`` (writes ``[]`` when the
            file was missing or every task is dropped).

        """
        try:
            pending = self.layout.read_pending_review_tasks(
                bundle_root,
                page_number,
            )
        except FileNotFoundError:
            pending = []
        rebound = [
            task.model_copy(update={"base_graph_revision": new_graph_revision})
            for task in pending
            if self._pending_task_targets_resolvable(page, task)
        ]
        self.layout.write_pending_review_tasks(bundle_root, page_number, rebound)

    def _pending_task_targets_resolvable(
        self,
        page: BundlePage,
        task: ReviewTask,
    ) -> bool:
        """
        Return whether every task target still exists on ``page``.

        Drop rule: keep a pending task only when all ``target_object_ids``
        resolve for ``task.target_scope`` and every ``related_object_id`` exists
        somewhere on the page graph.

        Args:
            page: Rebased page graph.
            task: Pending review task under consideration.

        Returns:
            ``True`` when the task should be retained and rebound.

        """
        try:
            known = self._known_ids_for_scope(page, task.target_scope)
        except ValueError:
            return False
        if any(object_id not in known for object_id in task.target_object_ids):
            return False
        all_ids = (
            {span.span_id for span in page.spans}
            | {region.region_id for region in page.regions}
            | {note.note_id for note in page.notes}
            | {line.line_id for line in page.lines}
            | {page.page_id}
        )
        return all(object_id in all_ids for object_id in task.related_object_ids)

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


def _bump_graph_revision(revision: str) -> str:
    """
    Return the next graph revision by bumping a trailing integer.

    Args:
        revision: Current ``BundlePage.graph_revision``.

    Returns:
        ``…N+1`` when ``revision`` ends in digits; otherwise ``{revision}-rebased``.

    """
    match = re.fullmatch(r"(.*?)(\d+)", revision)
    if match is None:
        return f"{revision}{_REBASED_ID_SUFFIX}"
    return f"{match.group(1)}{int(match.group(2)) + 1}"


def _identity_object_id_map(
    page: BundlePage,
    events: list[ReviewEvent],
) -> dict[str, str]:
    """
    Build an identity object-id map for leaf-only graph rebase.

    Args:
        page: Rebased page graph contributing stable graph object ids.
        events: Predecessor events whose targets/nested ids must also map.

    Returns:
        Mapping where every known id maps to itself.

    """
    ids: set[str] = {page.page_id}
    ids.update(span.span_id for span in page.spans)
    ids.update(region.region_id for region in page.regions)
    ids.update(note.note_id for note in page.notes)
    ids.update(line.line_id for line in page.lines)
    for event in events:
        ids.add(event.target_object_id)
        ids.update(_nested_object_ids(event))
    return {object_id: object_id for object_id in ids}
