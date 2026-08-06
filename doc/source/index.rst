=======
wordwending
=======

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   overview/installation
   overview/quickstart
   runbook/from_source_to_markdown
   overview/domain_language
   runbook/huggingface_setup

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   overview/usage
   overview/configuration
   overview/faq

.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   architecture/index
   runbook/ocr_process
   runbook/gold_annotation
   runbook/operator_notes
   runbook/contributing
   runbook/coding_standards

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   changelog

Current version is |release|.

``wordwending`` is a Python CLI for high-fidelity OCR of Old English / Anglo-Saxon
source material. It is
built for scholars first: preserve philological signal in the page image, keep
rebuildable witnesses, then derive structured and Markdown views. Agent-ready
RAG exports are a payoff of that fidelity, not a substitute for it.

Problem
-------

OCR that “works” still fails twice: it drops typography, notes, and layout that
philologists need, and it leaves agents without citable evidence of what the
page actually showed.

How
---

Multi-pass, image-first OCR → witness-preserving bundles → structured JSON, RAG
chunks, and evidence-preserving Markdown. Hosted runners do inference; the
laptop prepares, validates, stores, evaluates, and exports.

Why
---

Fidelity before cleverness. Raw pass artifacts stay intact so derived graphs and
exports remain rebuildable. Humans correct via overlays and review tasks—not by
silently editing OCR text into a new “truth.”

Core Features
-------------

**Image-first OCR orchestration**
    - Multi-pass workflows for difficult historical PDFs and page images
    - Separate text, structure, typography, note-linkage, and evaluation concerns

**Witness-preserving bundle outputs**
    - Raw pass artifacts remain intact
    - Derived page graphs, overlays, and exports remain rebuildable

**Reviewable structured exports**
    - Full-fidelity JSON for deterministic software
    - Evidence-preserving Markdown and RAG-oriented JSON for agents

Getting Started
---------------

1. **Installation**: :doc:`/overview/installation` (source + ``uv``; Python 3.13+)
2. **Quick Start**: :doc:`/overview/quickstart`
3. **From source to Markdown**: :doc:`/runbook/from_source_to_markdown` (end-to-end)
4. **Usage**: :doc:`/overview/usage`
5. **Configuration**: :doc:`/overview/configuration`
6. **Domain language**: :doc:`/overview/domain_language`
7. **Hugging Face setup**: :doc:`/runbook/huggingface_setup`
8. **FAQ**: :doc:`/overview/faq`

Published docs: https://wordwending.readthedocs.io

For developers, see :doc:`/runbook/contributing` and
:doc:`/runbook/coding_standards`.

Requirements
------------

- Python **3.13** or later

Common Use Cases
----------------

**Research and compare OCR passes**
    - Run competing hosted engines on difficult pages
    - Evaluate text, structure, typography, and note linkage separately

**Produce reviewable bundle artifacts**
    - Preserve footnotes, italic, bold, and superscript signals
    - Hand off evidence-rich outputs to downstream Old English tooling

**Export provisional Markdown and RAG views**
    - When a ``DocumentBundle`` exists, ``wordwending export`` writes derived
      ``document.md`` and retrieval artifacts (Markdown is not the SoT)
