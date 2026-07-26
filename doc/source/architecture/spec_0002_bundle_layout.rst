============================================
Spec 0002: V1 Bundle Layout and Data Shape
============================================

Purpose
=======

Define the on-disk structure for one document bundle.

Top-Level Layout
================

::

   <document-bundle>/
     manifest.json
     source/
       source.pdf
       pages/
         0001.jp2
         0002.png
       provenance.json
     pages/
       page-0001/
         manifest.json
         image/
           page.png
         witnesses/
           text/
           layout/
           style/
           table/
         graph/
           page_graph.json
         evaluation/
           scores.json
           flags.json
         overlays/
           review_events.jsonl
           current_state.json
         exports/
           page.md
           page.txt
       page-0002/
         ...
     evaluation/
       summary.json
     exports/
       document.md
       document.txt

Naming Rules
============

- Page identities must be deterministic and stable across reruns.
- Pass artifacts must record pass name and pass instance identity.
- Recomputable files should be overwritten deterministically.
- Human-authored overlays must remain separate from generated artifacts.
- Review history must be append-only.
- Source page-image filenames should retain the input extension actually
  supplied. ``.jp2`` is one common case, not a required one.

Required Manifests
==================

Document manifest should record:

- source document identity
- bibliographic provenance
- acquisition provenance
- run timestamp
- run configuration digest
- pass runner set
- page count
- bundle schema version

Page manifest should record:

- page identity and page number
- source image path
- executed passes
- generated raw witness artifacts
- graph artifact path
- evaluation artifact paths
- overlay presence
- review event log path

Minimum Graph Model
===================

The normalized page graph should include:

- page dimensions
- region nodes with boxes/polygons and reading-order indices
- line nodes with boxes/polygons/baselines and parent region ids
- span nodes with text, orthogonal typography, semantic roles, geometry, and
  parent line ids
- note nodes with boxes, text, and marker linkage
- provenance edges or references to contributing witness artifacts

V1 Typography and Role Vocabulary
=================================

Typography is not mutually exclusive. Spans record weight
(``regular``/``bold``/``unknown``), slant
(``upright``/``italic``/``unknown``), baseline shift
(``baseline``/``superscript``/``subscript``/``unknown``), optional family/size,
small capitals, and letter spacing. Semantic roles such as
``footnote-marker`` are recorded independently.

Allowed v1 note kinds:

- ``footnote-block``
