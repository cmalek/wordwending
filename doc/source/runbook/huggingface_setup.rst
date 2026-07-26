==================
Hugging Face Setup
==================

Purpose
=======

Deploy and operate every OCR model on Hugging Face Inference Endpoints while
preserving enough identity to reproduce every witness. The operator laptop is
not an inference host: it prepares inputs, submits jobs, validates responses,
stores artifacts, and supports review. Do not download full model weights or add
a local GPU fallback.

1. Activate the Project Environment
====================================

From the ``bochord`` repository root, always activate its environment before
Python work:

.. code-block:: bash

   source .venv/bin/activate

Install the official client as a declared project dependency when endpoint code
is implemented; do not rely on an undeclared global installation. Confirm the
active CLI and login:

.. code-block:: bash

   command -v python
   command -v hf
   hf auth whoami

2. Create Least-Privilege Credentials
======================================

Create a fine-grained Hugging Face token with only the model and endpoint access
required by the deployment. Use ``hf auth login`` for the operator account.
Store automation credentials in the deployment secret store, never in source,
config JSON, logs, provenance, shell history, or a bundle.

If a model is gated, accept its terms before provisioning. Record the model and
code licenses in the benchmark decision; access does not imply acceptable use.

3. Pin and Inspect the Model Remotely
=====================================

Choose the exact Hub repository and immutable commit hash. Do not deploy
``main``, a moving tag, or a bare model name as the reproducibility identity.

Inspect repository metadata and the download plan without fetching model
weights:

.. code-block:: bash

   hf download OWNER/MODEL --revision COMMIT_HASH --dry-run

Use the Hub UI/API to verify required weights/configuration and inspect the model
card, license, custom-code requirements, expected precision, and GPU memory.
Record repository, commit, and advertised file digests in the experiment record.
The endpoint downloads/mounts the model; the laptop does not.

4. Choose Managed Engine or Custom Container
=============================================

Use a managed inference engine only when it natively supports the exact
vision/document request and response contract. OCR pipelines with image/PDF
packaging, custom preprocessing, or nonstandard model code should use a pinned
custom container rather than disguising the workload as text generation.

For a custom container:

- load endpoint-mounted model files from ``/repository``; never fetch them from
  the laptop or at request time
- expose a readiness route such as ``/health`` that returns success only after
  model and tokenizer/processor initialization
- expose one versioned OCR route with validated request and response schemas
- set bounded request size, page count, output tokens, concurrency, and timeout
- run as a non-root user
- send no document pixels or text to logs
- pin all Python/system dependencies and the base-image digest
- build ``linux/amd64`` when building on Apple Silicon

Push the image to a registry Hugging Face can access and retain its immutable
image digest. Never use a mutable ``latest`` tag in recorded provenance.

5. Create the Endpoint
======================

In the Inference Endpoints UI:

1. Select the pinned model repository and commit revision.
2. Select cloud vendor and region permitted for the source material.
3. Choose the smallest GPU class that passes a representative peak-memory test.
4. Select authenticated or private access; do not make OCR endpoints public.
5. Choose managed engine or enter custom image digest, port, and health route.
6. Add ordinary configuration as environment variables and credentials as
   secret environment variables.
7. Set minimum/maximum replicas and decide whether scale-to-zero is acceptable.
8. Review displayed hourly cost and set the project budget/alert before Create.
9. Create the endpoint and wait with a finite deployment timeout.

The official CLI/API can automate the same lifecycle. Keep endpoint creation
configuration under version control without secret values. The API's
``revision``, hardware, replica, scale-to-zero, custom-image, and secret fields
must match the reviewed deployment record.

6. Prove Readiness and Correctness
==================================

Readiness is necessary but not sufficient:

1. Wait until endpoint state is ``running`` with a finite timeout.
2. Call ``/health`` and require a successful response after model load.
3. Submit one tiny non-sensitive fixture from the laptop and validate the complete response
   schema, model revision, and request id.
4. Submit one representative held-out OCR fixture and compare it with the local
   benchmark expectation. Do not tune from the held-out answer.
5. Confirm endpoint logs contain operational metadata but no source images,
   prompts containing document text, OCR output, or credentials.
6. Record the endpoint/runtime revision and container digest in
   ``RunnerReference``; record endpoint URL only in deployment config because it
   is location, not immutable identity.

7. Configure Cold Starts, Queueing, and Retries
===============================================

Scale-to-zero saves cost but introduces cold starts. Hugging Face may return a
temporary gateway error while a replica initializes and does not guarantee that
incoming OCR work is queued for the application. Therefore ``bochord`` must:

- use a durable client-side job queue
- give each batch an idempotency identity
- use a separate scale-up timeout and inference timeout
- retry only documented transient statuses and connection failures
- apply bounded exponential backoff with jitter
- never retry schema, authentication, license, or deterministic input failures
- persist a failed ``RunnerExecutionBatch`` even when no witness was produced
- avoid submitting a duplicate batch after the original result was persisted

Keep at least one replica when predictable latency matters. Use scale-to-zero for
intermittent research runs only when the queue and timeout policy handles cold
starts safely.

8. Benchmark Hosted Hardware and Batch Size
===========================================

Run controlled endpoint matrices by runner and page class. Hold model revision,
container, prompt, preparation, and input pages constant while varying one of:

- GPU class
- whole page versus prepared unit
- images versus packaged PDF
- batch size
- replica/concurrency setting

Separate warm-up from measured requests. Record latency distributions,
pages/units per minute, peak memory, timeout/failure rate, cost, and all gold
metric families. The fastest batch that degrades difficult characters,
typography, reading order, or note linkage does not win.

9. Operate and Shut Down
========================

Before a corpus run, verify endpoint revision, state, quota, queue depth, budget,
and one smoke fixture. During the run, watch endpoint logs/analytics, failure
rates, cold starts, latency, GPU utilization, and rejected requests.

After a finite research run, pause the endpoint or verify scale-to-zero occurred.
Retain run/batch records and raw witnesses according to artifact policy. Revoke
temporary tokens and rotate any credential exposed to output or logs.

Required Run Provenance
=======================

- model repository and immutable commit
- runner package/version
- runtime name and immutable container/endpoint revision
- non-secret configuration digest
- prompt/template digest, including a sentinel digest when no prompt is used
- hardware class and numeric precision in deployment metadata
- batch item ids, packaging artifact, batch size, timestamps, retries, failures,
  and item-to-output association

Local-Laptop Boundary
=====================

Allowed locally:

- PDF page extraction/rendering and image preparation
- quality assessment and subdivision
- image-to-PDF packaging for runners such as ``olmocr``
- request queueing, response validation, artifact storage, evaluation, exports,
  documentation, and human review
- lightweight unit tests using fixtures or mocked endpoint responses

Not allowed locally:

- OCR model inference, model fine-tuning, or GPU benchmark runs
- downloading full OCR model weights as an undocumented fallback
- changing output semantics because a hosted endpoint is temporarily unavailable

Endpoint unavailability produces a persisted failed/retryable batch. It never
causes silent local inference.

Official References
===================

- `Create an endpoint <https://huggingface.co/docs/inference-endpoints/guides/create_endpoint>`_
- `Endpoint configuration <https://huggingface.co/docs/inference-endpoints/en/guides/configuration>`_
- `Custom containers <https://huggingface.co/docs/inference-endpoints/engines/custom_container>`_
- `Autoscaling <https://huggingface.co/docs/inference-endpoints/guides/autoscaling>`_
- `Python endpoint lifecycle <https://huggingface.co/docs/huggingface_hub/guides/inference_endpoints>`_
