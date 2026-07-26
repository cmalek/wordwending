# Copyright (C) 2026 Chris Malek.
"""Evaluation policy and metric contract models."""

from pydantic import BaseModel, ConfigDict, Field


class MetricProfile(BaseModel):
    """Versioned, deterministic evaluation policy."""

    #: Forbid unknown keys so persisted metric profiles stay stable.
    model_config = ConfigDict(extra="forbid")
    #: Stable profile identifier for persisted evaluation policy.
    profile_id: str
    #: Semantic version of the profile contract.
    version: str
    #: Whether whitespace differences affect token comparison.
    whitespace_significant: bool = True
    #: Whether punctuation differences affect token comparison.
    punctuation_significant: bool = True
    #: Whether character case affects token comparison.
    case_sensitive: bool = True
    #: Whether line-break placement affects comparison.
    line_breaks_significant: bool = True
    #: Regex pattern used to tokenize diplomatic text for scoring.
    tokenizer_pattern: str = r"\w+(?:['’]\w+)*|[^\w\s]"  # noqa: RUF001
    #: Minimum IoU for region geometry to count as a match.
    region_iou_threshold: float = Field(default=0.5, gt=0, le=1)
    #: Exclude illegible gold targets from metric denominators.
    exclude_illegible: bool = True
    #: Treat unknown style facets as incorrect rather than ignored.
    unknown_style_is_incorrect: bool = True
