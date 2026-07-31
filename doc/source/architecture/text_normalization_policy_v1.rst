=====================================
Text Normalization Policy v1
=====================================

Purpose
=======

Document the deterministic rules implemented by
``bochord.services.text_normalization.TextNormalizer`` under policy id
``text-norm-v1``.

Default Policy
==============

``DEFAULT_TEXT_NORMALIZATION_POLICY`` uses:

- ``policy_id``: ``text-norm-v1``
- ``version``: ``1``
- Unicode form: NFC
- collapse internal whitespace: enabled
- strip leading and trailing whitespace: enabled
- note markers: retain
- superscript: retain
- historical characters: preserve (required in v1)

Unicode Normalization
=====================

Apply ``unicodedata.normalize("NFC", text)`` to diplomatic input.

Whitespace
==========

When ``collapse_whitespace`` is enabled, replace every run of Unicode
whitespace with a single ASCII space. When ``strip`` is enabled, remove leading
and trailing whitespace from the result.

Historical Characters
=====================

V1 never rewrites historical graphemes such as ``æ``, ``ǣ``, ``þ``, ``ð``,
``œ``, or macron vowels. Normalization may compose or decompose Unicode forms,
but it must not modernize or expand ligatures.

Note Markers
============

``RETAIN`` keeps note-marker graphemes unchanged in normalized note text.

``PLACEHOLDER`` replaces only these documented marker codepoints with ``[n]``:

- ``*``
- ``†``
- ``‡``
- ``¹``
- ``²``
- ``³``

Span normalization never rewrites note markers; only ``normalize_note_text``
applies this policy.

Superscript
===========

``RETAIN`` keeps superscript characters unchanged.

``FLATTEN`` maps only the fixed Unicode superscript digit and letter table
implemented in ``TextNormalizer`` to baseline equivalents. Unknown superscript
codepoints are left unchanged.

Line Joins
==========

Line joining is a convenience helper for chunk and region callers via
``join_line_texts``. It does not mutate span line provenance on ``BundlePage``.

Hyphen removal at a line boundary occurs only when ``join_kind`` is
``hyphen-join`` or ``human-corrected`` and the left diplomatic text ends with
ASCII hyphen-minus (``-``) or soft hyphen (U+00AD). All other join kinds keep
boundary hyphens unchanged.

``LineJoinRecord`` is returned for audit purposes and is not persisted onto
page graph objects in v1.

Dual Text Contract
==================

``text_diplomatic`` remains evidence-preserving. ``text_normalized`` is always
regenerated deterministically from diplomatic text; operators must not edit both
fields independently.
