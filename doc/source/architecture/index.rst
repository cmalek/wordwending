============
Architecture
============

This section captures the ordered architecture decisions and build specs for
``bochord``.

Read in this order:

1. ADRs for stable product and architecture boundaries
2. Specs for concrete v1 implementation details

.. toctree::
   :maxdepth: 1
   :caption: ADRs

   adr_0001_package_boundary
   adr_0002_bundle_model
   adr_0003_page_graph
   adr_0004_layered_artifacts
   adr_0005_evaluation_first
   adr_0006_pass_runner_plugins
   adr_0007_v1_engine_strategy
   adr_0008_stable_ids_and_review_history
   adr_0009_ocrd_page_escriptorium

.. toctree::
   :maxdepth: 1
   :caption: Spikes

   spike_0001_page_escriptorium

.. toctree::
   :maxdepth: 1
   :caption: Specs

   spec_0004_v1_implementation_plan
   spec_0001_system_architecture
   spec_0015_gold_annotation_schema
   spec_0003_evaluation_schema
   spec_0007_preparation
   spec_0010_page_classification
   spec_0012_runner_execution_and_batching
   spec_0013_pass_runner_interface_schema
   spec_0008_text_normalization
   text_normalization_policy_v1
   spec_0009_merge_policy
   spec_0002_bundle_layout
   spec_0005_human_markup
   spec_0014_review_overlay_schema
   spec_0011_structured_output_strategy
   spec_0006_exports_and_retrieval
   spec_0016_concrete_export_models
