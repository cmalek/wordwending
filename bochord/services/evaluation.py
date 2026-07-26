# Copyright (C) 2026 Chris Malek.
"""Gold-backed evaluation of diplomatic OCR page evidence."""

from __future__ import annotations

import unicodedata
from collections import Counter
from typing import TYPE_CHECKING

import regex  # type: ignore[import-untyped]

from bochord.models import (
    BoundingBox,
    BundlePage,
    EvaluationFamilySummary,
    EvaluationFlag,
    FlagSeverity,
    GoldCoverage,
    GoldPageAnnotation,
    GoldTextSpan,
    MetricProfile,
    MetricScore,
    PageEvaluationSummary,
    ReviewDimension,
    SpanRecord,
)

if TYPE_CHECKING:
    from collections.abc import Callable

#: Macron-bearing precomposed vowels retained in NFC diplomatic text.
_MACRON_GRAPHEMES = frozenset("āēīōūȳĀĒĪŌŪȲǣǢ")
#: Combining macron mark used to detect macron-bearing graphemes.
_COMBINING_MACRON = "\u0304"
#: Thorn and eth graphemes tracked by preservation metrics.
_THORN_ETH = frozenset("þðÞÐ")
#: Old English ligature graphemes tracked by preservation metrics.
_LIGATURES = frozenset("æœÆŒǣǢ")


def _graphemes(value: str) -> list[str]:
    """
    Split ``value`` into NFC extended grapheme clusters.

    Args:
        value: Raw diplomatic text.

    Returns:
        Ordered NFC grapheme clusters.

    """
    return regex.findall(r"\X", unicodedata.normalize("NFC", value))


def _edit_distance(left: list[str], right: list[str]) -> int:
    """
    Compute classic Levenshtein distance between token sequences.

    Args:
        left: Hypothesis sequence.
        right: Reference sequence.

    Returns:
        Minimum insert/delete/substitute count transforming ``left`` into
        ``right``.

    """
    previous = list(range(len(right) + 1))
    for left_index, left_item in enumerate(left, start=1):
        current = [left_index]
        for right_index, right_item in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1] + (left_item != right_item),
                )
            )
        previous = current
    return previous[-1]


def _box_iou(left: BoundingBox, right: BoundingBox) -> float:
    """
    Return intersection-over-union for two axis-aligned boxes.

    Args:
        left: First box.
        right: Second box.

    Returns:
        IoU in ``[0, 1]``.

    """
    x0 = max(left.x0, right.x0)
    y0 = max(left.y0, right.y0)
    x1 = min(left.x1, right.x1)
    y1 = min(left.y1, right.y1)
    if x1 <= x0 or y1 <= y0:
        return 0.0
    intersection = (x1 - x0) * (y1 - y0)
    left_area = (left.x1 - left.x0) * (left.y1 - left.y0)
    right_area = (right.x1 - right.x0) * (right.y1 - right.y0)
    return intersection / (left_area + right_area - intersection)


def _is_macron_grapheme(grapheme: str) -> bool:
    """
    Return whether ``grapheme`` carries a macron in NFC or NFD form.

    Args:
        grapheme: One NFC grapheme cluster.

    Returns:
        True when the cluster is macron-bearing.

    """
    if grapheme in _MACRON_GRAPHEMES:
        return True
    return _COMBINING_MACRON in unicodedata.normalize("NFD", grapheme)


def _is_thorn_eth(grapheme: str) -> bool:
    """
    Return whether ``grapheme`` is thorn or eth.

    Args:
        grapheme: One NFC grapheme cluster.

    Returns:
        True for þ/ð/Þ/Ð.

    """
    return grapheme in _THORN_ETH


def _is_ligature(grapheme: str) -> bool:
    """
    Return whether ``grapheme`` is an OE ligature under watch.

    Args:
        grapheme: One NFC grapheme cluster.

    Returns:
        True for æ/œ-family ligatures.

    """
    return grapheme in _LIGATURES


class EvaluationService:
    """Score one predicted page against a gold annotation slice."""

    def evaluate_page(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> PageEvaluationSummary:
        """
        Evaluate text fidelity for one page; other families stay empty.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy controlling transforms and exclusions.

        Returns:
            Page summary with a populated text family.

        """
        return PageEvaluationSummary(
            text=self._evaluate_text(prediction, gold, profile)
        )

    def _evaluate_text(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> EvaluationFamilySummary:
        """
        Aggregate diplomatic text metrics and watchlist flags.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy.

        Returns:
            Text-family metrics and flags.

        """
        rates = {
            "cer": _RateAccumulator(),
            "wer": _RateAccumulator(),
            "exact": _RateAccumulator(),
            "macron": _RateAccumulator(),
            "ligature": _RateAccumulator(),
            "thorn_eth": _RateAccumulator(),
        }
        flags: list[EvaluationFlag] = []
        for gold_span, predicted_text in self._scored_text_pairs(
            prediction, gold, profile
        ):
            flag = self._score_text_pair(gold_span, predicted_text, profile, rates)
            if flag is not None:
                flags.append(flag)
        return EvaluationFamilySummary(
            metrics=[
                rates["cer"].to_metric("character_error_rate"),
                rates["wer"].to_metric("word_error_rate"),
                rates["exact"].to_metric("exact_span_match_rate", as_error_rate=False),
                rates["macron"].to_metric("macron_recall", as_error_rate=False),
                rates["ligature"].to_metric(
                    "ligature_preservation_rate", as_error_rate=False
                ),
                rates["thorn_eth"].to_metric(
                    "thorn_eth_preservation_rate", as_error_rate=False
                ),
            ],
            flags=flags,
        )

    def _score_text_pair(
        self,
        gold_span: GoldTextSpan,
        predicted_text: str,
        profile: MetricProfile,
        rates: dict[str, _RateAccumulator],
    ) -> EvaluationFlag | None:
        """
        Score one gold/prediction pair into shared accumulators.

        Args:
            gold_span: Gold text annotation being scored.
            predicted_text: Matched predicted diplomatic text.
            profile: Frozen metric policy.
            rates: Shared page-level rate accumulators.

        Returns:
            A missing-watchlist flag when evidence is incomplete, else ``None``.

        Side Effects:
            Mutates ``rates`` accumulators.

        """
        reference = self._transform(gold_span.text_diplomatic, profile)
        hypothesis = self._transform(predicted_text, profile)
        self._accumulate_edit_rates(
            rates["cer"], rates["wer"], reference, hypothesis, profile
        )
        if reference or hypothesis:
            rates["exact"].add(1.0 if reference == hypothesis else 0.0, 1.0)
        ref_gs = _graphemes(reference)
        hyp_gs = _graphemes(hypothesis)
        missing = self._accumulate_watchlist(
            rates["macron"], ref_gs, hyp_gs, _is_macron_grapheme
        )
        missing |= self._accumulate_watchlist(
            rates["ligature"], ref_gs, hyp_gs, _is_ligature
        )
        missing |= self._accumulate_watchlist(
            rates["thorn_eth"], ref_gs, hyp_gs, _is_thorn_eth
        )
        if not missing:
            return None
        targets = (
            [gold_span.target_object_id]
            if gold_span.target_object_id is not None
            else []
        )
        return EvaluationFlag(
            flag_id=f"missing-watchlist-{gold_span.annotation_id}",
            flag_type="missing_watchlist_character",
            severity=FlagSeverity.WARNING,
            message=(
                "Predicted text is missing one or more watchlist "
                f"graphemes from gold span {gold_span.annotation_id}"
            ),
            target_object_ids=targets,
        )

    def _scored_text_pairs(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> list[tuple[GoldTextSpan, str]]:
        """
        Resolve scored gold text spans to predicted diplomatic strings.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy.

        Returns:
            Ordered ``(gold_span, predicted_text)`` pairs that enter denominators.

        """
        spans_by_id = {span.span_id: span for span in prediction.spans}
        pairs: list[tuple[GoldTextSpan, str]] = []
        for gold_span in gold.text_spans:
            if gold_span.do_not_score:
                continue
            if profile.exclude_illegible and gold_span.illegible:
                continue
            matched = self._resolve_span(gold_span, spans_by_id, profile)
            object_id = (
                matched.span_id if matched is not None else gold_span.target_object_id
            )
            if not self._has_exhaustive_text_coverage(gold, object_id):
                continue
            predicted_text = matched.text_diplomatic if matched is not None else ""
            pairs.append((gold_span, predicted_text))
        return pairs

    def _resolve_span(
        self,
        gold_span: GoldTextSpan,
        spans_by_id: dict[str, SpanRecord],
        profile: MetricProfile,
    ) -> SpanRecord | None:
        """
        Resolve a gold text span to a predicted span by id or box IoU.

        Args:
            gold_span: Gold text annotation to resolve.
            spans_by_id: Predicted spans keyed by id.
            profile: Metric policy supplying the IoU threshold.

        Returns:
            Matched predicted span, or ``None`` when unresolved.

        """
        if gold_span.target_object_id is not None:
            return spans_by_id.get(gold_span.target_object_id)
        if gold_span.bounding_box is None:
            return None
        best: SpanRecord | None = None
        best_iou = 0.0
        for span in spans_by_id.values():
            if span.bounding_box is None:
                continue
            iou = _box_iou(gold_span.bounding_box, span.bounding_box)
            if iou >= profile.region_iou_threshold and iou > best_iou:
                best = span
                best_iou = iou
        return best

    def _has_exhaustive_text_coverage(
        self,
        gold: GoldPageAnnotation,
        object_id: str | None,
    ) -> bool:
        """
        Return whether ``object_id`` lies in exhaustive TEXT coverage.

        Args:
            gold: Gold annotation slice.
            object_id: Predicted or gold target object id.

        Returns:
            True when an eligible coverage record includes the object.

        """
        for coverage in gold.coverage:
            if not self._coverage_allows_text(coverage):
                continue
            if coverage.whole_page:
                return True
            if object_id is not None and object_id in coverage.target_object_ids:
                return True
        return False

    @staticmethod
    def _coverage_allows_text(coverage: GoldCoverage) -> bool:
        """
        Return whether coverage may contribute TEXT denominators.

        Args:
            coverage: One gold coverage record.

        Returns:
            True for exhaustive, non-excluded TEXT coverage.

        """
        return (
            ReviewDimension.TEXT in coverage.dimensions
            and coverage.exhaustive
            and not coverage.do_not_score
        )

    @staticmethod
    def _transform(value: str, profile: MetricProfile) -> str:
        """
        Apply profile comparison transforms before splitting.

        Args:
            value: Diplomatic text.
            profile: Metric policy flags.

        Returns:
            Transformed comparison string.

        """
        text = value
        if not profile.line_breaks_significant:
            text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
        if not profile.whitespace_significant:
            text = " ".join(text.split())
        if not profile.punctuation_significant:
            text = "".join(
                char for char in text if not unicodedata.category(char).startswith("P")
            )
        if not profile.case_sensitive:
            text = text.casefold()
        return unicodedata.normalize("NFC", text)

    @staticmethod
    def _accumulate_edit_rates(
        cer: _RateAccumulator,
        wer: _RateAccumulator,
        reference: str,
        hypothesis: str,
        profile: MetricProfile,
    ) -> None:
        """
        Accumulate CER and WER contributions for one scored pair.

        Args:
            cer: Character-error accumulator.
            wer: Word-error accumulator.
            reference: Transformed gold text.
            hypothesis: Transformed predicted text.
            profile: Metric policy supplying the tokenizer pattern.

        Side Effects:
            Mutates ``cer`` and ``wer``.

        """
        ref_gs = _graphemes(reference)
        hyp_gs = _graphemes(hypothesis)
        cer.add_edit(_edit_distance(hyp_gs, ref_gs), len(ref_gs), bool(hyp_gs))
        ref_tokens = regex.findall(profile.tokenizer_pattern, reference)
        hyp_tokens = regex.findall(profile.tokenizer_pattern, hypothesis)
        wer.add_edit(
            _edit_distance(hyp_tokens, ref_tokens),
            len(ref_tokens),
            bool(hyp_tokens),
        )

    @staticmethod
    def _accumulate_watchlist(
        accumulator: _RateAccumulator,
        reference: list[str],
        hypothesis: list[str],
        predicate: Callable[[str], bool],
    ) -> bool:
        """
        Accumulate grapheme-count watchlist recall for one predicate.

        Args:
            accumulator: Preservation-rate accumulator.
            reference: Reference NFC graphemes.
            hypothesis: Predicted NFC graphemes.
            predicate: Watchlist membership test.

        Returns:
            True when reference evidence exists and recall is incomplete.

        Side Effects:
            Mutates ``accumulator``.

        """
        ref_counts = Counter(g for g in reference if predicate(g))
        if not ref_counts:
            return False
        hyp_counts = Counter(g for g in hypothesis if predicate(g))
        preserved = sum(min(count, hyp_counts[g]) for g, count in ref_counts.items())
        total = sum(ref_counts.values())
        accumulator.add(float(preserved), float(total))
        return preserved < total


class _RateAccumulator:
    """Mutable numerator/denominator accumulator for one page metric."""

    def __init__(self) -> None:
        """Initialize empty numerator and denominator totals."""
        #: Sum of successes or edit distances contributed so far.
        self.numerator = 0.0
        #: Sum of reference lengths or span counts contributed so far.
        self.denominator = 0.0
        #: Whether any empty-reference / non-empty-hypothesis case occurred.
        self.insertion_against_empty = False
        #: Explanatory note when empty-reference insertions force value 1.
        self.note: str | None = None

    def add(self, numerator: float, denominator: float) -> None:
        """
        Add a success-style contribution.

        Args:
            numerator: Success count for this unit.
            denominator: Opportunity count for this unit.

        Side Effects:
            Mutates accumulator totals.

        """
        self.numerator += numerator
        self.denominator += denominator

    def add_edit(
        self, distance: int, reference_length: int, hyp_nonempty: bool
    ) -> None:
        """
        Add an edit-distance contribution with empty-reference handling.

        Args:
            distance: Edit distance for this unit.
            reference_length: Reference token/grapheme count.
            hyp_nonempty: Whether the hypothesis sequence is non-empty.

        Side Effects:
            Mutates accumulator totals and optional note.

        """
        if reference_length == 0:
            if hyp_nonempty:
                self.insertion_against_empty = True
                self.note = (
                    "non-empty prediction against empty reference scored as unit error"
                )
            return
        self.numerator += float(distance)
        self.denominator += float(reference_length)

    def to_metric(self, metric_id: str, *, as_error_rate: bool = True) -> MetricScore:
        """
        Materialize an accumulated score.

        Args:
            metric_id: Stable metric identifier.

        Keyword Args:
            as_error_rate: When true, value is errors/denom; otherwise successes/denom.

        Returns:
            Frozen metric score with explicit numerator and denominator.
            Empty-reference unit-error notes attach only when the final
            denominator is zero.

        """
        if self.denominator == 0:
            value = 1.0 if (as_error_rate and self.insertion_against_empty) else 0.0
            return MetricScore(
                metric_id=metric_id,
                value=value,
                numerator=(
                    None if as_error_rate and self.insertion_against_empty else 0.0
                ),
                denominator=0.0,
                note=self.note if self.insertion_against_empty else None,
            )
        return MetricScore(
            metric_id=metric_id,
            value=self.numerator / self.denominator,
            numerator=self.numerator,
            denominator=self.denominator,
        )
