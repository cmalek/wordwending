# Copyright (C) 2026 Chris Malek.
"""Gold-backed evaluation of diplomatic OCR page evidence."""

from __future__ import annotations

import unicodedata
from collections import Counter
from typing import TYPE_CHECKING

import regex  # type: ignore[import-untyped]

from bochord.models import (
    BaselineShift,
    BoundingBox,
    BundlePage,
    EvaluationFamilySummary,
    EvaluationFlag,
    FlagSeverity,
    FontSlant,
    FontWeight,
    GoldCoverage,
    GoldNoteLink,
    GoldPageAnnotation,
    GoldRegionAnnotation,
    GoldStyleSpan,
    GoldTextSpan,
    LineRecord,
    MetricProfile,
    MetricScore,
    NoteRecord,
    PageEvaluationSummary,
    RegionKind,
    RegionRecord,
    ReviewDimension,
    SpanRecord,
    TextRole,
    Typography,
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
#: Merge confidence below this emits ``low_confidence_merged_graph_region``.
_LOW_MERGE_CONFIDENCE = 0.5


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


def _boxes_intersect(left: BoundingBox, right: BoundingBox) -> bool:
    """
    Return whether two axis-aligned boxes share positive area.

    Args:
        left: First box.
        right: Second box.

    Returns:
        True when the rectangles overlap.

    """
    return min(left.x1, right.x1) > max(left.x0, right.x0) and min(
        left.y1, right.y1
    ) > max(left.y0, right.y0)


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


def _coverage_allows(coverage: GoldCoverage, dimension: ReviewDimension) -> bool:
    """
    Return whether coverage may contribute denominators for ``dimension``.

    Args:
        coverage: One gold coverage record.
        dimension: Required review dimension.

    Returns:
        True for exhaustive, non-excluded coverage that includes ``dimension``.

    """
    return (
        dimension in coverage.dimensions
        and coverage.exhaustive
        and not coverage.do_not_score
    )


def _has_exhaustive_coverage(
    gold: GoldPageAnnotation,
    object_id: str | None,
    dimension: ReviewDimension,
    *,
    bounding_box: BoundingBox | None = None,
) -> bool:
    """
    Return whether an object lies in exhaustive coverage for ``dimension``.

    An object qualifies when an eligible coverage record is whole-page, lists
    ``object_id`` in ``target_object_ids``, or declares an image
    ``bounding_box`` that intersects the object's ``bounding_box``.

    Args:
        gold: Gold annotation slice.
        object_id: Predicted or gold target object id.
        dimension: Required review dimension.

    Keyword Args:
        bounding_box: Object geometry used for image-scoped coverage.

    Returns:
        True when an eligible coverage record includes the object.

    """
    for coverage in gold.coverage:
        if not _coverage_allows(coverage, dimension):
            continue
        if coverage.whole_page:
            return True
        if object_id is not None and object_id in coverage.target_object_ids:
            return True
        if (
            coverage.bounding_box is not None
            and bounding_box is not None
            and _boxes_intersect(coverage.bounding_box, bounding_box)
        ):
            return True
    return False


def _resolve_anchored_span(
    gold_span: GoldTextSpan | GoldStyleSpan,
    spans_by_id: dict[str, SpanRecord],
    profile: MetricProfile,
) -> SpanRecord | None:
    """
    Resolve a gold span annotation to a predicted span by id or box IoU.

    Args:
        gold_span: Gold text or style annotation to resolve.
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


def _resolve_region(
    gold_region: GoldRegionAnnotation,
    regions: list[RegionRecord],
    profile: MetricProfile,
) -> RegionRecord | None:
    """
    Resolve a gold region by id or same-kind highest IoU.

    Args:
        gold_region: Gold region annotation.
        regions: Predicted page regions.
        profile: Metric policy supplying the IoU threshold.

    Returns:
        Matched predicted region, or ``None`` when unresolved.

    """
    if gold_region.target_object_id is not None:
        by_id = {region.region_id: region for region in regions}
        matched = by_id.get(gold_region.target_object_id)
        if matched is not None and matched.region_kind == gold_region.region_kind:
            return matched
        return None
    if gold_region.bounding_box is None:
        return None
    best: RegionRecord | None = None
    best_iou = 0.0
    for region in regions:
        if region.region_kind != gold_region.region_kind:
            continue
        if region.bounding_box is None:
            continue
        iou = _box_iou(gold_region.bounding_box, region.bounding_box)
        if iou >= profile.region_iou_threshold and iou > best_iou:
            best = region
            best_iou = iou
    return best


def _facet_match(
    gold_value: object,
    predicted_value: object,
    *,
    unknown: object,
    unknown_is_incorrect: bool,
) -> bool | None:
    """
    Compare one non-unknown gold facet to a prediction.

    Args:
        gold_value: Gold facet value (caller skips true unknowns).
        predicted_value: Predicted facet value.

    Keyword Args:
        unknown: Sentinel meaning unknown for this facet type.
        unknown_is_incorrect: Profile policy for unknown predictions.

    Returns:
        True/False when scored, or ``None`` when the prediction is unknown
        and unknown predictions are ignored.

    """
    if predicted_value == unknown or predicted_value is None:
        if unknown_is_incorrect:
            return False
        return None
    return predicted_value == gold_value


class EvaluationService:
    """
    Score one predicted page against a gold annotation slice.

    Orchestrates text, structure, typography, and note-linkage scorers under a
    frozen :class:`~bochord.models.MetricProfile`. Gold coverage defines every
    denominator; ``do_not_score`` never enters one. No blended page score is
    produced.
    """

    def evaluate_page(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> PageEvaluationSummary:
        """
        Evaluate text, structure, typography, and note-linkage families.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy controlling transforms and exclusions.

        Returns:
            Page summary with populated evidence families.

        """
        return PageEvaluationSummary(
            text=self._evaluate_text(prediction, gold, profile),
            structure=_StructureScorer().score(prediction, gold, profile),
            typography=_TypographyScorer().score(prediction, gold, profile),
            note_linkage=_NoteLinkageScorer().score(prediction, gold, profile),
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
            box = (
                matched.bounding_box if matched is not None else gold_span.bounding_box
            )
            if not _has_exhaustive_coverage(
                gold,
                object_id,
                ReviewDimension.TEXT,
                bounding_box=box,
            ):
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
        return _resolve_anchored_span(gold_span, spans_by_id, profile)

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
    """
    Mutable numerator/denominator accumulator for one page metric.

    Tracks success or edit-distance contributions plus the empty-reference
    insertion case that forces error-rate value ``1`` with an explanatory note.
    """

    def __init__(self) -> None:
        """
        Initialize empty numerator and denominator totals.

        Side Effects:
            Creates mutable accumulator fields on ``self``.

        """
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


class _StructureScorer:
    """
    Score structure metrics and provenance-backed structure flags.

    Covers region coverage, adjacent reading-order pairs, line-join fidelity,
    and table-region detection under exhaustive STRUCTURE coverage.
    """

    def score(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> EvaluationFamilySummary:
        """
        Aggregate region, order, join, and table metrics for one page.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy.

        Returns:
            Structure-family metrics and flags.

        """
        lines_by_id = {line.line_id: line for line in prediction.lines}
        matches = self._matched_regions(prediction, gold, profile)
        coverage = _RateAccumulator()
        tables = _RateAccumulator()
        flags: list[EvaluationFlag] = []
        for gold_region, matched in matches:
            coverage.add(1.0 if matched is not None else 0.0, 1.0)
            if gold_region.region_kind == RegionKind.TABLE:
                tables.add(1.0 if matched is not None else 0.0, 1.0)
            if matched is not None:
                flags.extend(self._provenance_flags(matched))
        return EvaluationFamilySummary(
            metrics=[
                coverage.to_metric("region_coverage", as_error_rate=False),
                self._order_rate(matches).to_metric(
                    "line_ordering_correctness", as_error_rate=False
                ),
                self._join_rate(gold, lines_by_id).to_metric(
                    "line_join_fidelity", as_error_rate=False
                ),
                tables.to_metric("table_region_detection", as_error_rate=False),
            ],
            flags=flags,
        )

    def _matched_regions(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> list[tuple[GoldRegionAnnotation, RegionRecord | None]]:
        """
        Resolve scored gold regions under exhaustive STRUCTURE coverage.

        Args:
            prediction: Accepted page graph.
            gold: Gold annotation slice.
            profile: Metric policy.

        Returns:
            Ordered ``(gold_region, matched_prediction)`` pairs.

        """
        pairs: list[tuple[GoldRegionAnnotation, RegionRecord | None]] = []
        for gold_region in gold.regions:
            if gold_region.do_not_score:
                continue
            object_id = gold_region.target_object_id
            matched = _resolve_region(gold_region, prediction.regions, profile)
            if matched is not None:
                object_id = matched.region_id
            box = (
                matched.bounding_box
                if matched is not None
                else gold_region.bounding_box
            )
            if not _has_exhaustive_coverage(
                gold,
                object_id,
                ReviewDimension.STRUCTURE,
                bounding_box=box,
            ):
                continue
            pairs.append((gold_region, matched))
        return pairs

    @staticmethod
    def _order_rate(
        matches: list[tuple[GoldRegionAnnotation, RegionRecord | None]],
    ) -> _RateAccumulator:
        """
        Score adjacent gold reading-order pairs among covered regions.

        Args:
            matches: Covered gold/prediction region pairs.

        Returns:
            Accumulator for ``line_ordering_correctness``.

        """
        rate = _RateAccumulator()
        ordered = [
            (gold_region, matched)
            for gold_region, matched in matches
            if gold_region.reading_order_index is not None
        ]
        ordered.sort(key=lambda item: item[0].reading_order_index or 0)
        for index in range(len(ordered) - 1):
            left_gold, left_pred = ordered[index]
            right_gold, right_pred = ordered[index + 1]
            del left_gold, right_gold
            correct = (
                left_pred is not None
                and right_pred is not None
                and left_pred.reading_order_index < right_pred.reading_order_index
            )
            rate.add(1.0 if correct else 0.0, 1.0)
        return rate

    @staticmethod
    def _join_rate(
        gold: GoldPageAnnotation,
        lines_by_id: dict[str, LineRecord],
    ) -> _RateAccumulator:
        """
        Score each non-excluded gold join against ``joins_to_line_id``.

        Semantics: when ``joined`` is true, the left predicted line must set
        ``joins_to_line_id`` to the gold right line id. When ``joined`` is
        false, the left line must not point at that right line id. Scoring is
        one-directional (left → right); mutual joins are not required.

        Args:
            gold: Gold annotation slice.
            lines_by_id: Predicted lines keyed by id.

        Returns:
            Accumulator for ``line_join_fidelity``.

        """
        rate = _RateAccumulator()
        for join in gold.line_joins:
            if join.do_not_score:
                continue
            left = lines_by_id.get(join.left_line_id)
            box = left.bounding_box if left is not None else None
            if not _has_exhaustive_coverage(
                gold,
                join.left_line_id,
                ReviewDimension.STRUCTURE,
                bounding_box=box,
            ):
                continue
            # Missing left line is a miss: do not treat absent joins_to as
            # success for joined=false (None != right_line_id).
            if left is None:
                correct = False
            elif join.joined:
                correct = left.joins_to_line_id == join.right_line_id
            else:
                correct = left.joins_to_line_id != join.right_line_id
            rate.add(1.0 if correct else 0.0, 1.0)
        return rate

    @staticmethod
    def _provenance_flags(region: RegionRecord) -> list[EvaluationFlag]:
        """
        Emit provenance-backed flags for one matched region.

        Args:
            region: Matched predicted region.

        Returns:
            Zero or more structure flags grounded in provenance fields.

        """
        flags: list[EvaluationFlag] = []
        merge = region.provenance.merge_confidence
        if merge is not None and merge < _LOW_MERGE_CONFIDENCE:
            flags.append(
                EvaluationFlag(
                    flag_id=f"low-merge-{region.region_id}",
                    flag_type="low_confidence_merged_graph_region",
                    severity=FlagSeverity.WARNING,
                    message=(
                        f"Region {region.region_id} has low merge confidence ({merge})"
                    ),
                    target_object_ids=[region.region_id],
                )
            )
        note = region.provenance.disagreement_note
        if note is not None:
            flags.append(
                EvaluationFlag(
                    flag_id=f"disagreement-{region.region_id}",
                    flag_type="raw_pass_disagreement",
                    severity=FlagSeverity.WARNING,
                    message=(
                        f"Region {region.region_id} carries raw-pass "
                        f"disagreement: {note}"
                    ),
                    target_object_ids=[region.region_id],
                )
            )
        return flags


class _TypographyScorer:
    """
    Score independent typography facets and footnote role/object metrics.

    Facets are scored separately; bold italic is never one mutually exclusive
    class. Footnote-marker retention and footnote-block detection use
    TYPOGRAPHY / STRUCTURE coverage respectively.
    """

    def score(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> EvaluationFamilySummary:
        """
        Aggregate per-facet style accuracy and footnote role metrics.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy.

        Returns:
            Typography-family metrics and flags.

        """
        rates = {
            "font_weight_accuracy": _RateAccumulator(),
            "font_slant_accuracy": _RateAccumulator(),
            "baseline_shift_accuracy": _RateAccumulator(),
            "small_caps_accuracy": _RateAccumulator(),
            "letter_spacing_accuracy": _RateAccumulator(),
            "footnote_marker_retention": _RateAccumulator(),
            "footnote_block_detection": _RateAccumulator(),
        }
        flags: list[EvaluationFlag] = []
        spans_by_id = {span.span_id: span for span in prediction.spans}
        for gold_span in gold.style_spans:
            if gold_span.do_not_score:
                continue
            matched = _resolve_anchored_span(gold_span, spans_by_id, profile)
            object_id = (
                matched.span_id if matched is not None else gold_span.target_object_id
            )
            box = (
                matched.bounding_box if matched is not None else gold_span.bounding_box
            )
            if not _has_exhaustive_coverage(
                gold,
                object_id,
                ReviewDimension.TYPOGRAPHY,
                bounding_box=box,
            ):
                continue
            pred_typo = matched.typography if matched is not None else Typography()
            pred_roles = matched.roles if matched is not None else []
            flag = self._score_style_span(
                gold_span, pred_typo, pred_roles, profile, rates
            )
            if flag is not None:
                flags.append(flag)
        self._score_footnote_blocks(prediction, gold, profile, rates)
        return EvaluationFamilySummary(
            metrics=[
                rates[metric_id].to_metric(metric_id, as_error_rate=False)
                for metric_id in rates
            ],
            flags=flags,
        )

    def _score_style_span(
        self,
        gold_span: GoldStyleSpan,
        predicted: Typography,
        predicted_roles: list[TextRole],
        profile: MetricProfile,
        rates: dict[str, _RateAccumulator],
    ) -> EvaluationFlag | None:
        """
        Score one gold style span into facet and marker accumulators.

        Args:
            gold_span: Gold style annotation.
            predicted: Predicted typography facets.
            predicted_roles: Predicted semantic roles.
            profile: Metric policy.
            rates: Shared page-level rate accumulators.

        Returns:
            A partial style-family-collapse flag when warranted, else ``None``.

        Side Effects:
            Mutates ``rates`` accumulators.

        """
        weight_ok, slant_ok = self._accumulate_style_facets(
            gold_span.typography, predicted, profile, rates
        )
        self._score_footnote_marker(gold_span, predicted_roles, rates)
        return self._style_collapse_flag(gold_span, weight_ok, slant_ok)

    def _accumulate_style_facets(
        self,
        gold_typo: Typography,
        predicted: Typography,
        profile: MetricProfile,
        rates: dict[str, _RateAccumulator],
    ) -> tuple[bool | None, bool | None]:
        """
        Score independent typography facets into shared accumulators.

        Args:
            gold_typo: Gold typography facets.
            predicted: Predicted typography facets.
            profile: Metric policy.
            rates: Shared page-level rate accumulators.

        Returns:
            ``(weight_ok, slant_ok)`` match results, or ``None`` per unscored
            facet.

        Side Effects:
            Mutates ``rates`` accumulators.

        """
        unknown_wrong = profile.unknown_style_is_incorrect
        weight_ok = self._score_enum_facet(
            rates["font_weight_accuracy"],
            gold_typo.weight,
            predicted.weight,
            FontWeight.UNKNOWN,
            unknown_wrong,
        )
        slant_ok = self._score_enum_facet(
            rates["font_slant_accuracy"],
            gold_typo.slant,
            predicted.slant,
            FontSlant.UNKNOWN,
            unknown_wrong,
        )
        self._score_enum_facet(
            rates["baseline_shift_accuracy"],
            gold_typo.baseline_shift,
            predicted.baseline_shift,
            BaselineShift.UNKNOWN,
            unknown_wrong,
        )
        self._score_optional_bool(
            rates["small_caps_accuracy"],
            gold_typo.small_caps,
            predicted.small_caps,
            unknown_wrong,
        )
        self._score_optional_bool(
            rates["letter_spacing_accuracy"],
            gold_typo.letter_spaced,
            predicted.letter_spaced,
            unknown_wrong,
        )
        return weight_ok, slant_ok

    @staticmethod
    def _score_footnote_marker(
        gold_span: GoldStyleSpan,
        predicted_roles: list[TextRole],
        rates: dict[str, _RateAccumulator],
    ) -> None:
        """
        Score footnote-marker retention when gold carries that role.

        Args:
            gold_span: Gold style annotation.
            predicted_roles: Predicted semantic roles.
            rates: Shared page-level rate accumulators.

        Side Effects:
            Mutates ``footnote_marker_retention`` when gold has the role.

        """
        if TextRole.FOOTNOTE_MARKER not in gold_span.roles:
            return
        retained = TextRole.FOOTNOTE_MARKER in predicted_roles
        rates["footnote_marker_retention"].add(1.0 if retained else 0.0, 1.0)

    @staticmethod
    def _style_collapse_flag(
        gold_span: GoldStyleSpan,
        weight_ok: bool | None,
        slant_ok: bool | None,
    ) -> EvaluationFlag | None:
        """
        Emit partial collapse when weight and slant XOR-match.

        Fires only when both facets are scored (gold non-unknown) and exactly
        one matches. Both correct, both wrong, or a single scored facet do
        not emit the flag.

        Args:
            gold_span: Gold style annotation supplying ids for the flag.
            weight_ok: Weight match result, or ``None`` if unscored.
            slant_ok: Slant match result, or ``None`` if unscored.

        Returns:
            A ``style_family_collapse`` flag, or ``None``.

        """
        if weight_ok is None or slant_ok is None:
            return None
        if weight_ok == slant_ok:
            return None
        targets = (
            [gold_span.target_object_id]
            if gold_span.target_object_id is not None
            else []
        )
        return EvaluationFlag(
            flag_id=f"style-collapse-{gold_span.annotation_id}",
            flag_type="style_family_collapse",
            severity=FlagSeverity.WARNING,
            message=(
                "Predicted style partially collapses independent "
                f"weight/slant facets for gold style {gold_span.annotation_id}"
            ),
            target_object_ids=targets,
        )

    @staticmethod
    def _score_enum_facet(
        rate: _RateAccumulator,
        gold_value: FontWeight | FontSlant | BaselineShift,
        predicted_value: FontWeight | FontSlant | BaselineShift,
        unknown: FontWeight | FontSlant | BaselineShift,
        unknown_is_incorrect: bool,
    ) -> bool | None:
        """
        Score one enum typography facet when gold is known.

        Args:
            rate: Target accumulator.
            gold_value: Gold facet value.
            predicted_value: Predicted facet value.
            unknown: Unknown sentinel for this enum.
            unknown_is_incorrect: Profile unknown-prediction policy.

        Returns:
            Match result when scored, else ``None`` when gold is unknown.

        Side Effects:
            Mutates ``rate`` when the gold facet is scorable.

        """
        if gold_value == unknown:
            return None
        result = _facet_match(
            gold_value,
            predicted_value,
            unknown=unknown,
            unknown_is_incorrect=unknown_is_incorrect,
        )
        if result is None:
            return None
        rate.add(1.0 if result else 0.0, 1.0)
        return result

    @staticmethod
    def _score_optional_bool(
        rate: _RateAccumulator,
        gold_value: bool | None,
        predicted_value: bool | None,
        unknown_is_incorrect: bool,
    ) -> None:
        """
        Score small-caps or letter-spacing when gold is known.

        Args:
            rate: Target accumulator.
            gold_value: Gold boolean facet, or ``None`` when unknown.
            predicted_value: Predicted boolean facet.
            unknown_is_incorrect: Profile unknown-prediction policy.

        Side Effects:
            Mutates ``rate`` when the gold facet is scorable.

        """
        if gold_value is None:
            return
        result = _facet_match(
            gold_value,
            predicted_value,
            unknown=None,
            unknown_is_incorrect=unknown_is_incorrect,
        )
        if result is None:
            return
        rate.add(1.0 if result else 0.0, 1.0)

    @staticmethod
    def _score_footnote_blocks(
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
        rates: dict[str, _RateAccumulator],
    ) -> None:
        """
        Score gold FOOTNOTE regions under exhaustive STRUCTURE coverage.

        Args:
            prediction: Accepted page graph.
            gold: Gold annotation slice.
            profile: Metric policy.
            rates: Shared typography rate accumulators.

        Side Effects:
            Mutates ``footnote_block_detection`` in ``rates``.

        """
        rate = rates["footnote_block_detection"]
        for gold_region in gold.regions:
            if (
                gold_region.do_not_score
                or gold_region.region_kind != RegionKind.FOOTNOTE
            ):
                continue
            matched = _resolve_region(gold_region, prediction.regions, profile)
            object_id = (
                matched.region_id
                if matched is not None
                else gold_region.target_object_id
            )
            box = (
                matched.bounding_box
                if matched is not None
                else gold_region.bounding_box
            )
            if not _has_exhaustive_coverage(
                gold,
                object_id,
                ReviewDimension.STRUCTURE,
                bounding_box=box,
            ):
                continue
            rate.add(1.0 if matched is not None else 0.0, 1.0)


class _NoteLinkageScorer:
    """
    Score exact marker-to-note edges and emit linkage flags.

    Gold ``note_target_id`` may be a predicted note id or a gold region
    ``annotation_id`` that resolves to a note body. Coverage is checked on the
    marker span and the resolved note target.
    """

    def score(
        self,
        prediction: BundlePage,
        gold: GoldPageAnnotation,
        profile: MetricProfile,
    ) -> EvaluationFamilySummary:
        """
        Aggregate note-linkage success for covered gold edges.

        Args:
            prediction: Accepted page graph under evaluation.
            gold: Gold annotation slice for the same page.
            profile: Frozen metric policy (unused; retained for API symmetry).

        Returns:
            Note-linkage metrics and flags.

        """
        del profile
        predicted_edges = self._predicted_edges(prediction.notes, gold)
        rate = _RateAccumulator()
        flags: list[EvaluationFlag] = []
        for gold_link in gold.note_links:
            for marker_span_id in gold_link.marker_span_ids:
                if not self._edge_in_coverage(
                    gold, marker_span_id, gold_link, prediction.notes
                ):
                    continue
                edge = (marker_span_id, gold_link.note_target_id)
                correct = edge in predicted_edges
                rate.add(1.0 if correct else 0.0, 1.0)
                if not correct:
                    flags.append(
                        EvaluationFlag(
                            flag_id=(
                                f"note-link-{gold_link.annotation_id}-{marker_span_id}"
                            ),
                            flag_type="ambiguous_note_linkage",
                            severity=FlagSeverity.WARNING,
                            message=(
                                "Predicted note linkage misses gold edge "
                                f"({marker_span_id} -> "
                                f"{gold_link.note_target_id})"
                            ),
                            target_object_ids=[
                                marker_span_id,
                                gold_link.note_target_id,
                            ],
                        )
                    )
        return EvaluationFamilySummary(
            metrics=[rate.to_metric("note_linkage_success", as_error_rate=False)],
            flags=flags,
        )

    @staticmethod
    def _note_annotation_aliases(
        gold: GoldPageAnnotation,
        notes: list[NoteRecord],
    ) -> dict[str, set[str]]:
        """
        Map predicted note ids to gold region annotation ids that name them.

        Args:
            gold: Gold annotation slice.
            notes: Predicted note records.

        Returns:
            ``note_id`` → gold region ``annotation_id`` aliases.

        """
        note_ids = {note.note_id for note in notes}
        aliases: dict[str, set[str]] = {}
        for region in gold.regions:
            target = region.target_object_id
            if target is None:
                continue
            if target in note_ids:
                aliases.setdefault(target, set()).add(region.annotation_id)
                continue
            for note in notes:
                if note.region_id == target:
                    aliases.setdefault(note.note_id, set()).add(region.annotation_id)
        return aliases

    @staticmethod
    def _predicted_edges(
        notes: list[NoteRecord],
        gold: GoldPageAnnotation,
    ) -> set[tuple[str, str]]:
        """
        Expand predicted notes into marker→note edges under gold aliases.

        Emits ``(marker_span_id, note_id)`` and also
        ``(marker_span_id, annotation_id)`` when a gold region annotation names
        that note body, so gold ``note_target_id`` may be either form.

        Args:
            notes: Predicted note records.
            gold: Gold annotation slice supplying annotation-id aliases.

        Returns:
            Exact predicted linkage edges keyed by note id and annotation id.

        """
        aliases = _NoteLinkageScorer._note_annotation_aliases(gold, notes)
        edges: set[tuple[str, str]] = set()
        for note in notes:
            keys = {note.note_id} | aliases.get(note.note_id, set())
            for marker_span_id in note.linked_marker_span_ids:
                for key in keys:
                    edges.add((marker_span_id, key))
        return edges

    @staticmethod
    def _edge_in_coverage(
        gold: GoldPageAnnotation,
        marker_span_id: str,
        gold_link: GoldNoteLink,
        notes: list[NoteRecord],
    ) -> bool:
        """
        Return whether a gold note edge is in exhaustive NOTE_LINKAGE coverage.

        Args:
            gold: Gold annotation slice.
            marker_span_id: Marker side of the gold edge.
            gold_link: Gold note-link annotation.
            notes: Predicted notes used to resolve annotation-id targets.

        Returns:
            True when the marker or note target is covered.

        """
        if _has_exhaustive_coverage(gold, marker_span_id, ReviewDimension.NOTE_LINKAGE):
            return True
        if _has_exhaustive_coverage(
            gold, gold_link.note_target_id, ReviewDimension.NOTE_LINKAGE
        ):
            return True
        aliases = _NoteLinkageScorer._note_annotation_aliases(gold, notes)
        for note_id, annotation_ids in aliases.items():
            if gold_link.note_target_id not in annotation_ids:
                continue
            if _has_exhaustive_coverage(gold, note_id, ReviewDimension.NOTE_LINKAGE):
                return True
        return False
