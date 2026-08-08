# Copyright (C) 2026 Chris Malek.
"""Document run configuration and stage contracts."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from wordwending.models.ocr import SchemaModel


class DocumentRunStage(StrEnum):
    """Stages in a full document run machine path."""

    #: Prepare source pages and bundle layout.
    PREPARE = "prepare"
    #: Execute configured OCR runners.
    RUN = "run"
    #: Merge runner outputs into the document bundle.
    ASSEMBLE = "assemble"
    #: Score assembled pages against gold annotations.
    EVAL = "eval"
    #: Write document exports from the assembled bundle.
    EXPORT = "export"
    #: Issue pending human review tasks for the bundle.
    ISSUE_REVIEW_TASKS = "issue_review_tasks"


class DocumentRunnerSpec(SchemaModel):
    """One runner invocation configured for a document run."""

    #: Registry key for the runner implementation (for example ``olmocr``).
    runner_id: str
    #: Path to JSON ``RunnerReference`` for this runner.
    runner_reference_path: str
    #: Path to JSON ``RunnerExecutionPolicy`` for this runner.
    policy_path: str


class DocumentRunConfig(SchemaModel):
    """Configuration for one orchestrated document run."""

    #: Stable run identifier referenced across stage outputs.
    run_id: str
    #: Document identifier written into the assembled bundle.
    document_id: str
    #: Bundle root path, relative or absolute; resolved by the orchestrator.
    bundle_root: str
    #: Source file path for preparation.
    source_path: str
    #: One or more preparation recipe JSON paths.
    recipe_paths: list[str] = Field(min_length=1)
    #: Path to source provenance JSON.
    source_json: str
    #: Path to bibliographic provenance JSON.
    bibliographic_json: str
    #: Path to acquisition provenance JSON.
    acquisition_json: str
    #: Path to merge policy JSON.
    merge_policy_path: str
    #: One or more runner specs executed during the run stage.
    runners: list[DocumentRunnerSpec] = Field(min_length=1)
    #: Explicit stage order; ``None`` selects the default machine path.
    stages: list[DocumentRunStage] | None = None
    #: Force rerunning stages that would otherwise resume from ledger state.
    force_rerun: bool = False
    #: Ensure hosted endpoints are up before runner invocation.
    ensure_endpoints: bool = False
    #: Optional page-id to gold-annotation JSON path map for evaluation.
    gold_page_paths: dict[str, str] = Field(default_factory=dict)
    #: Optional metric profile JSON path; required with gold for default eval.
    metric_profile_path: str | None = None
    #: Omit export from default stages when ``stages`` is ``None``.
    skip_export: bool = False

    def resolved_stages(self) -> list[DocumentRunStage]:
        """
        Return the stage order for this run.

        Returns:
            Explicit ``stages`` when set; otherwise the default machine path.
            ``skip_export`` applies only when ``stages`` is ``None``.

        """
        if self.stages is not None:
            return list(self.stages)
        stages = list(self._default_stages())
        if self.skip_export:
            stages = [stage for stage in stages if stage is not DocumentRunStage.EXPORT]
        return stages

    def _default_stages(self) -> list[DocumentRunStage]:
        """
        Return the default machine path before ``skip_export`` filtering.

        Returns:
            Ordered default stages for this config.

        """
        stages = [
            DocumentRunStage.PREPARE,
            DocumentRunStage.RUN,
            DocumentRunStage.ASSEMBLE,
        ]
        if self._includes_eval():
            stages.append(DocumentRunStage.EVAL)
        stages.extend(
            [
                DocumentRunStage.ISSUE_REVIEW_TASKS,
                DocumentRunStage.EXPORT,
            ]
        )
        return stages

    def _includes_eval(self) -> bool:
        """
        Return whether gold and metric profile enable default eval.

        Returns:
            ``True`` when both gold paths and a metric profile are configured.

        """
        return bool(self.gold_page_paths) and self.metric_profile_path is not None
