=======
bochord
=======

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   overview/installation
   overview/quickstart
   overview/domain_language

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
   runbook/operator_notes
   runbook/contributing
   runbook/coding_standards

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   changelog

Current version is |release|.

``bochord`` (from *bōchord*, "book treasure-hoard") is a Python command-line tool which provides a high-fidelity OCR framework for Old English/Anglo-Saxon texts.

Core Features
-------------

bochord provides the following key features:

**Image-first OCR orchestration**
    - Multi-pass workflows for difficult historical PDFs
    - Separate text, structure, style, and evaluation concerns

**Witness-preserving bundle outputs**
    - Raw pass artifacts remain intact
    - Derived page graphs, overlays, and exports remain rebuildable

**Reviewable structured exports**
    - Full-fidelity JSON for deterministic software
    - Evidence-preserving Markdown and RAG-oriented JSON for agents


Getting Started
---------------

To get started with bochord:

1. **Installation**: Follow the :doc:`/overview/installation` guide
2. **Quick Start**: See the :doc:`/overview/quickstart` guide for basic usage
3. **Usage Guide**: Learn about commands and options in :doc:`/overview/usage`
4. **Configuration**: Learn about configuration options in :doc:`/overview/configuration`
5. **Domain Language**: Use the shared vocabulary in :doc:`/overview/domain_language`
6. **FAQ**: Check the :doc:`/overview/faq` section for common questions and troubleshooting

For developers, see the :doc:`/runbook/contributing` and :doc:`/runbook/coding_standards` guides.

Requirements
------------

- Python 3.11 or later

Common Use Cases
----------------

**Research and compare OCR passes**
    - Run competing engines on difficult pages
    - Evaluate text, structure, and style separately

**Produce reviewable bundle artifacts**
    - Preserve footnotes, italic, bold, and superscript signals
    - Hand off evidence-rich outputs to downstream Old English tooling
