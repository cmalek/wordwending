======================================================
ADR 0010: Structured Output Boundary
======================================================

:Status: Accepted
:Date: 2026-08-02

Context
=======

``wordwending`` serves many structurally different downstream targets—dictionaries,
grammars, readers, and bilingual source texts. OCR orchestration and evidence
preservation must complete before domain-specific structural commitments are
safe.

Spec 0011 defines how standard OCR output relates to those targets. ADR 0008
requires stable ids across rebuilds; downstream work must also retain
bibliographic and acquisition provenance.

Decision
========

V1 standardizes on ``wordwending``'s own evidence-preserving OCR intermediate
structure as layer 1. That canonical output comprises prepared source artifacts,
raw witness artifacts, accepted page graph, review and evaluation metadata, and
standard export families.

Layers 2 and 3—optional transformation profiles and target-domain consumer
models—belong in downstream packages. Dictionary, grammar, and reader packages
transform layer 1 into document-specific structures they own.

TEI P5 dictionary guidance is a structural reference for downstream lexical
work. It is not a v1 requirement to emit TEI XML. Downstream packages may
express TEI-inspired concepts as Python or Pydantic models when useful.

Downstream transformations must preserve stable ids (per ADR 0008) and
bibliographic and acquisition provenance so target-domain models retain source
identity and citation context.

``wordwending`` may later define a shared optional transformation profile only after
demonstrated repeated use across multiple OCR tasks—not by speculative design.

Rejected Alternative
====================

A universal target schema or XML-first workflow that forces all consumers into
one downstream ontology or TEI vocabulary regardless of document genre.

Consequences
============

- ``wordwending`` stays reusable across dictionary, grammar, and reader workflows
  without distorting non-lexical material.
- Domain models (entries, senses, grammar sections, translation structures) live
  outside the core package until broad reuse is proven.
- TEI-informed modeling remains available downstream without binding v1 exports
  to XML serialization.
