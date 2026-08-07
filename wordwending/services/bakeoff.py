# Copyright (C) 2026 Chris Malek.
"""Bake-off harness: score real candidates into bakeoff-matrix-v1.json."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from wordwending.models.bakeoff import (
    BAKEOFF_MATRIX_FILENAME,
    BakeoffCandidate,
    BakeoffInvocationOutcome,
    BakeoffManifest,
    BakeoffMatrix,
    BakeoffMatrixCell,
    BakeoffPageCase,
    BakeoffPredictionRef,
    BakeoffRequest,
)
from wordwending.models.evaluation import MetricProfile  # noqa: TC001
from wordwending.models.ocr import BundlePage, GoldPageAnnotation
from wordwending.services.evaluation import EvaluationService  # noqa: TC001


class BakeoffCandidateInvoker(Protocol):
    """
    Produce one prediction (or failure) for a bake-off cell.

    Product invokers use recorded responses or real hosted adapters
    (``olmocr``, ``kraken``). Fake doubles are allowed only in unit tests of
    harness plumbing — never as Phase 5 exit evidence.
    """

    def invoke(self, *, runner_id: str, page_id: str) -> BakeoffInvocationOutcome:
        """
        Invoke one candidate for one page.

        Keyword Args:
            runner_id: Stable logical runner id.
            page_id: Page identifier under evaluation.

        Returns:
            Prediction and latency on success, or a failure message.

        """


class RecordedBakeoffInvoker:
    """
    Resolve bake-off cells from an in-memory map of recorded outcomes.

    Used by default unit tests and offline CLI manifests. Outcomes should come
    from real endpoint response shapes (or fixtures matching them), not from
    FakePassRunner Phase-exit claims.

    Args:
        outcomes: Mapping of ``(runner_id, page_id)`` to recorded outcomes.

    """

    def __init__(
        self,
        outcomes: dict[tuple[str, str], BakeoffInvocationOutcome],
    ) -> None:
        """
        Bind recorded outcomes for offline bake-off cells.

        Args:
            outcomes: Mapping of ``(runner_id, page_id)`` to recorded outcomes.

        """
        #: Recorded outcomes keyed by runner and page.
        self._outcomes = outcomes

    def invoke(self, *, runner_id: str, page_id: str) -> BakeoffInvocationOutcome:
        """
        Return the recorded outcome for ``runner_id`` x ``page_id``.

        Keyword Args:
            runner_id: Stable logical runner id.
            page_id: Page identifier under evaluation.

        Returns:
            Recorded outcome, or a missing-recording failure.

        """
        key = (runner_id, page_id)
        outcome = self._outcomes.get(key)
        if outcome is None:
            return BakeoffInvocationOutcome(
                failure=f"no recorded outcome for runner_id={runner_id!r} "
                f"page_id={page_id!r}"
            )
        return outcome


class BakeoffService:
    """
    Run a reproducible bake-off matrix using EvaluationService metrics.

    Does **not** mark Spec 0004 Phase 5 COMPLETE. Cost/license/operability
    scoring and full corpus held-out slices remain deferred placeholders.

    Args:
        evaluation: Page evaluation service for score families.
        invoker: Candidate invoker (recorded fixtures or hosted adapters).

    """

    def __init__(
        self,
        *,
        evaluation: EvaluationService,
        invoker: BakeoffCandidateInvoker,
    ) -> None:
        """
        Initialize evaluation and invoker collaborators.

        Keyword Args:
            evaluation: Page evaluation service for score families.
            invoker: Candidate invoker (recorded fixtures or hosted adapters).

        """
        #: Page evaluation collaborator for score families.
        self._evaluation = evaluation
        #: Candidate invoker for predictions, latency, and failures.
        self._invoker = invoker

    def run(self, request: BakeoffRequest, profile: MetricProfile) -> BakeoffMatrix:
        """
        Score every candidate x page cell into a bake-off matrix.

        Args:
            request: Candidates and held-out page cases.
            profile: Frozen metric profile for EvaluationService.

        Returns:
            Matrix with score families, latency, failure, and license
            placeholders per cell.

        """
        cells: list[BakeoffMatrixCell] = [
            self._score_cell(candidate, page, profile)
            for page in request.pages
            for candidate in request.candidates
        ]
        return BakeoffMatrix(candidates=list(request.candidates), cells=cells)

    def write_matrix(self, matrix: BakeoffMatrix, output_dir: Path) -> Path:
        """
        Write ``bakeoff-matrix-v1.json`` under ``output_dir``.

        Side Effects:
            Creates ``output_dir`` when missing and writes the matrix JSON.

        Args:
            matrix: Completed bake-off matrix.
            output_dir: Directory that will contain the matrix file.

        Returns:
            Absolute path to the written matrix file.

        """
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / BAKEOFF_MATRIX_FILENAME
        path.write_text(matrix.model_dump_json(indent=2), encoding="utf-8")
        return path

    @classmethod
    def load_recorded_manifest(
        cls,
        manifest: BakeoffManifest,
        *,
        bundle_root: Path,
    ) -> tuple[BakeoffRequest, RecordedBakeoffInvoker]:
        """
        Load an offline bake-off request and recorded invoker from a manifest.

        Args:
            manifest: Operator manifest with gold and prediction path refs.

        Keyword Args:
            bundle_root: Filesystem root for relative path resolution.

        Returns:
            In-memory request plus a recorded invoker for those predictions.

        Raises:
            FileNotFoundError: If a resolved gold or prediction path is missing.
            ValueError: If gold or prediction ``page_id`` does not match the
                corresponding manifest ref.

        """
        pages: list[BakeoffPageCase] = []
        for page_ref in manifest.pages:
            gold_path = _resolve_against_root(bundle_root, page_ref.gold_path)
            gold = GoldPageAnnotation.model_validate_json(
                gold_path.read_text(encoding="utf-8")
            )
            if gold.page_id != page_ref.page_id:
                msg = (
                    f"gold page_id {gold.page_id!r} does not match "
                    f"manifest page_id {page_ref.page_id!r}"
                )
                raise ValueError(msg)
            pages.append(
                BakeoffPageCase(
                    page_id=page_ref.page_id,
                    page_class=page_ref.page_class,
                    gold=gold,
                )
            )
        outcomes: dict[tuple[str, str], BakeoffInvocationOutcome] = {}
        for prediction_ref in manifest.predictions:
            outcomes[(prediction_ref.runner_id, prediction_ref.page_id)] = (
                _outcome_from_prediction_ref(prediction_ref, bundle_root)
            )
        return (
            BakeoffRequest(candidates=list(manifest.candidates), pages=pages),
            RecordedBakeoffInvoker(outcomes),
        )

    def _score_cell(
        self,
        candidate: BakeoffCandidate,
        page: BakeoffPageCase,
        profile: MetricProfile,
    ) -> BakeoffMatrixCell:
        """
        Score one runner x page cell.

        Args:
            candidate: Runner candidate with deferred scoring placeholders.
            page: Held-out page case with gold.
            profile: Frozen metric profile.

        Returns:
            Matrix cell with scores or failure populated.

        """
        outcome = self._invoker.invoke(
            runner_id=candidate.runner_id,
            page_id=page.page_id,
        )
        if outcome.failure is not None or outcome.prediction is None:
            return _cell_from_failure(
                candidate,
                page,
                latency_ms=outcome.latency_ms,
                failure=outcome.failure or "missing prediction",
            )
        try:
            summary = self._evaluation.evaluate_page(
                outcome.prediction, page.gold, profile
            )
        except Exception as exc:  # noqa: BLE001 - isolate scoring failures per cell
            return _cell_from_failure(
                candidate,
                page,
                latency_ms=outcome.latency_ms,
                failure=f"evaluation failed: {exc}",
            )
        return BakeoffMatrixCell(
            runner_id=candidate.runner_id,
            page_id=page.page_id,
            page_class=page.page_class,
            score_families=summary,
            latency_ms=outcome.latency_ms,
            failure=None,
            license_placeholder=candidate.license_placeholder,
            cost_placeholder=candidate.cost_placeholder,
            operability_placeholder=candidate.operability_placeholder,
        )


def _cell_from_failure(
    candidate: BakeoffCandidate,
    page: BakeoffPageCase,
    *,
    latency_ms: float | None,
    failure: str,
) -> BakeoffMatrixCell:
    """
    Build a matrix cell that records a per-cell failure without scores.

    Args:
        candidate: Runner candidate with deferred scoring placeholders.
        page: Held-out page case for this cell.

    Keyword Args:
        latency_ms: Optional latency from the invoker.
        failure: Human-readable failure message.

    Returns:
        Matrix cell with ``score_families`` unset and ``failure`` set.

    """
    return BakeoffMatrixCell(
        runner_id=candidate.runner_id,
        page_id=page.page_id,
        page_class=page.page_class,
        score_families=None,
        latency_ms=latency_ms,
        failure=failure,
        license_placeholder=candidate.license_placeholder,
        cost_placeholder=candidate.cost_placeholder,
        operability_placeholder=candidate.operability_placeholder,
    )


def _resolve_against_root(bundle_root: Path, path_str: str) -> Path:
    """
    Resolve one path string against ``bundle_root`` when relative.

    Args:
        bundle_root: Bake-off root used as the relative base.
        path_str: Absolute or bundle-relative posix path string.

    Returns:
        Absolute filesystem path for reading the artifact.

    """
    path = Path(path_str)
    if path.is_absolute():
        return path
    return bundle_root / path


def _outcome_from_prediction_ref(
    prediction_ref: BakeoffPredictionRef,
    bundle_root: Path,
) -> BakeoffInvocationOutcome:
    """
    Build one recorded outcome from a manifest prediction ref.

    Args:
        prediction_ref: Manifest prediction path and optional failure/latency.
        bundle_root: Filesystem root for relative path resolution.

    Returns:
        Recorded invocation outcome.

    Raises:
        FileNotFoundError: If the prediction path is missing when required.
        ValueError: If prediction ``page_id`` does not match the prediction ref.

    """
    if prediction_ref.failure is not None:
        return BakeoffInvocationOutcome(
            latency_ms=prediction_ref.latency_ms,
            failure=prediction_ref.failure,
        )
    prediction_path = _resolve_against_root(bundle_root, prediction_ref.prediction_path)
    prediction = BundlePage.model_validate_json(
        prediction_path.read_text(encoding="utf-8")
    )
    if prediction.page_id != prediction_ref.page_id:
        msg = (
            f"prediction page_id {prediction.page_id!r} does not match "
            f"manifest page_id {prediction_ref.page_id!r}"
        )
        raise ValueError(msg)
    return BakeoffInvocationOutcome(
        prediction=prediction,
        latency_ms=prediction_ref.latency_ms,
    )
