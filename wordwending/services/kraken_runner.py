# Copyright (C) 2026 Chris Malek.
"""
Hosted Hugging Face kraken batch execution without local inference.

Provisional second hosted adapter (ADR 0007). Request shape is OpenAI-
compatible ``chat/completions`` against a Hugging Face endpoint; raw witnesses
are exact response bytes (ADR 0004). ``runner_id`` is ``kraken``.
"""

from __future__ import annotations

import base64
import io
from pathlib import Path  # noqa: TC003
from typing import Any, TypedDict

import httpx
import pypdfium2 as pdfium  # type: ignore[import-untyped]
from PIL import Image

from wordwending.exc import ConfigurationError, RunnerEndpointUnavailable
from wordwending.models.ocr import (
    BatchUnitKind,
    InputKind,
    PackagingStrategy,
    RunnerCapability,
    RunnerOutputArtifact,
    RunnerReference,
)
from wordwending.models.runner_execution import (
    HostedInvocationResult,
    PackagedRunnerInput,
    PlannedRunnerBatch,
    RunnerExecutionPolicy,
)

#: Provisional transcription prompt for OpenAI-compatible kraken HF endpoints.
KRAKEN_TRANSCRIPTION_PROMPT = (
    "Transcribe all readable text in this image. Preserve line breaks and "
    "historical characters when present. Do not add commentary."
)

#: Declared kraken runner input and batching contract for hosted execution.
KRAKEN_CAPABILITY = RunnerCapability(
    accepted_input_kinds=[
        InputKind.IMAGE,
        InputKind.PREPARED_UNIT,
        InputKind.PDF,
    ],
    preferred_input_kind=InputKind.PDF,
    supports_multi_item_batching=True,
    batch_unit_kind=BatchUnitKind.PREPARED_UNIT,
    packaging_strategy=PackagingStrategy.UNIT_TO_PDF_BATCH,
)


class _ItemInvokeResult(TypedDict):
    """Per-item hosted invocation outcome."""

    #: Output witness artifact when the hosted request succeeded.
    artifact: RunnerOutputArtifact | None
    #: Hosted request identifier when the provider returned one.
    request_id: str | None
    #: Non-fatal warning text when the hosted request failed.
    warning: str | None


def _resize_if_needed(image: Image.Image, target_longest: int) -> Image.Image:
    """
    Downscale ``image`` when its longest edge exceeds ``target_longest``.

    Args:
        image: Source RGB image.
        target_longest: Maximum allowed longest edge in pixels.

    Returns:
        Resized image or the original when already within bounds.

    """
    width, height = image.size
    longest = max(width, height)
    if longest <= target_longest:
        return image
    scale = target_longest / longest
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return image.resize(new_size, Image.Resampling.LANCZOS)


def _encode_png_base64(image: Image.Image) -> str:
    """
    Encode ``image`` as deterministic PNG bytes and return Base64 text.

    Args:
        image: RGB image to encode.

    Returns:
        Base64-encoded PNG payload without data-url prefix.

    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _load_image_from_pdf(pdf_path: Path, page_number: int) -> Image.Image:
    """
    Render one PDF page to an RGB Pillow image.

    Side Effects:
        Opens and closes PDFium document and page handles.

    Args:
        pdf_path: Packaged PDF input path.
        page_number: One-based page index within the PDF.

    Returns:
        Rendered RGB image that the caller must close.

    Raises:
        ValueError: If ``page_number`` is out of range.

    """
    document = pdfium.PdfDocument(pdf_path)
    try:
        if page_number < 1 or page_number > len(document):
            msg = f"page {page_number} is out of range for {pdf_path}"
            raise ValueError(msg)
        page = document[page_number - 1]
        try:
            bitmap = page.render(scale=1.0)
            try:
                image = bitmap.to_pil().convert("RGB")
                image.load()
                return image
            finally:
                bitmap.close()
        finally:
            page.close()
    finally:
        document.close()


def _transport_failure_warning(item_id: str, exc: httpx.RequestError) -> str:
    """
    Build a warning message for one hosted transport-layer failure.

    Args:
        item_id: Batch item identifier for the failed request.
        exc: Transport or network error raised by httpx.

    Returns:
        Non-fatal warning text for the hosted invocation result.

    """
    if isinstance(exc, httpx.TimeoutException):
        return f"hosted request for {item_id} timed out"
    return f"hosted request for {item_id} failed: {exc}"


def _failed_item_result(
    *,
    request_id: str | None,
    warning: str,
) -> _ItemInvokeResult:
    """
    Build one failed hosted item result.

    Keyword Args:
        request_id: Hosted request identifier when present.
        warning: Non-fatal warning describing the failure.

    Returns:
        Failed per-item invocation outcome.

    """
    return {
        "artifact": None,
        "request_id": request_id,
        "warning": warning,
    }


def _load_direct_image(image_path: Path) -> Image.Image:
    """
    Open one direct image input as RGB.

    Args:
        image_path: Packaged image artifact path.

    Returns:
        Open RGB image that the caller must close.

    """
    with Image.open(image_path) as opened:
        image = opened.convert("RGB")
        image.load()
        return image


class HuggingFaceKrakenRunner:
    """
    Execute planned batches against one hosted OpenAI-compatible kraken endpoint.

    Provisional ADR 0007 candidate adapter. Uses OpenAI-compatible
    ``chat/completions`` as the Hugging Face request shape; persists exact
    response bytes as raw witnesses (ADR 0004).

    Args:
        runner: Model-backed runner identity for hosted requests.
        policy: Frozen execution policy controlling timeouts and retries.
        endpoint_url: OpenAI-compatible hosted endpoint base URL.
        token: Hugging Face bearer token for hosted inference.
        client: Shared HTTP client used for health checks and invocations.

    """

    def __init__(
        self,
        runner: RunnerReference,
        policy: RunnerExecutionPolicy,
        endpoint_url: str,
        token: str,
        client: httpx.Client,
    ) -> None:
        """
        Bind one hosted kraken runner to endpoint settings and an HTTP client.

        Args:
            runner: Model-backed runner identity for hosted requests.
            policy: Frozen execution policy controlling timeouts and retries.
            endpoint_url: OpenAI-compatible hosted endpoint base URL.
            token: Hugging Face bearer token for hosted inference.
            client: Shared HTTP client used for health checks and invocations.

        Raises:
            ConfigurationError: If ``token`` is missing.

        """
        if not token:
            msg = "missing hosted inference token"
            raise ConfigurationError(msg)
        #: Model-backed runner identity sent to the hosted endpoint.
        self._runner = runner
        #: Frozen execution policy controlling timeouts and retry classification.
        self._policy = policy
        #: OpenAI-compatible hosted endpoint base URL without trailing slash.
        self._endpoint_url = endpoint_url.rstrip("/")
        #: Hugging Face bearer token used for hosted inference requests.
        self._token = token
        #: Shared HTTP client used for health checks and invocations.
        self._client = client

    @property
    def policy(self) -> RunnerExecutionPolicy:
        """
        Return the frozen execution policy bound to this runner.

        Returns:
            Runner execution policy for hosted invocations.

        """
        return self._policy

    @property
    def runner_ref(self) -> RunnerReference:
        """
        Return the runner identity used for hosted requests.

        Returns:
            Model-backed runner reference metadata.

        """
        return self._runner

    @property
    def capability(self) -> RunnerCapability:
        """
        Return the declared kraken input and batching contract.

        Returns:
            Hosted kraken runner capability metadata.

        """
        return KRAKEN_CAPABILITY

    def health_check(self) -> None:
        """
        Verify the hosted endpoint reports model readiness.

        Side Effects:
            Issues one GET request to the hosted ``/models`` endpoint.

        Raises:
            RunnerEndpointUnavailable: If the endpoint is not ready or unreachable.

        """
        try:
            response = self._client.get(
                f"{self._endpoint_url}/models",
                headers=self._auth_headers(),
                timeout=self._policy.endpoint.request_timeout_seconds,
            )
        except httpx.RequestError as exc:
            msg = f"hosted endpoint models check failed: {exc}"
            raise RunnerEndpointUnavailable(msg) from exc
        if response.status_code != httpx.codes.OK:
            msg = (
                "hosted endpoint models check failed with status "
                f"{response.status_code}"
            )
            raise RunnerEndpointUnavailable(msg)

    def invoke(
        self,
        batch: PlannedRunnerBatch,
        packaged: PackagedRunnerInput,
        output_dir: Path,
    ) -> HostedInvocationResult:
        """
        Execute one packaged batch against the hosted kraken endpoint.

        Side Effects:
            Writes raw response witnesses under ``output_dir/witnesses/`` and
            issues one hosted completion request per batch item.

        Args:
            batch: Planned batch whose items will be invoked.
            packaged: Packaged input artifact metadata and page mapping.
            output_dir: Output root containing packaged inputs and witnesses.

        Returns:
            Hosted invocation result with per-item failures and artifacts.

        """
        failure_item_ids: list[str] = []
        output_artifacts: list[RunnerOutputArtifact] = []
        request_ids: list[str] = []
        warnings: list[str] = []

        for item_id, page_number in zip(
            packaged.batch_item_ids,
            packaged.page_numbers,
            strict=True,
        ):
            item_result = self._invoke_item(
                batch=batch,
                packaged=packaged,
                output_dir=output_dir,
                item_id=item_id,
                page_number=page_number,
            )
            if item_result["request_id"] is not None:
                request_ids.append(item_result["request_id"])
            if item_result["warning"] is not None:
                warnings.append(item_result["warning"])
            if item_result["artifact"] is not None:
                output_artifacts.append(item_result["artifact"])
            else:
                failure_item_ids.append(item_id)

        return HostedInvocationResult(
            failure_item_ids=failure_item_ids,
            output_artifacts=output_artifacts,
            request_ids=request_ids,
            warnings=warnings,
        )

    def _invoke_item(
        self,
        *,
        batch: PlannedRunnerBatch,
        packaged: PackagedRunnerInput,
        output_dir: Path,
        item_id: str,
        page_number: int,
    ) -> _ItemInvokeResult:
        """
        Invoke one batch item and persist its raw hosted response witness.

        Keyword Args:
            batch: Planned batch metadata for idempotency headers.
            packaged: Packaged input artifact for the whole batch.
            output_dir: Output root for witness files.
            item_id: Batch item identifier for this invocation.
            page_number: One-based page index within the packaged input.

        Returns:
            Mapping with optional artifact, request id, and warning text.

        """
        image: Image.Image | None = None
        try:
            image = self._load_item_image(
                packaged=packaged,
                output_dir=output_dir,
                page_number=page_number,
            )
            resized = _resize_if_needed(
                image,
                self._policy.target_longest_image_dim,
            )
            image_base64 = _encode_png_base64(resized)
            payload = self._completion_payload(image_base64)
            response = self._client.post(
                f"{self._endpoint_url}/chat/completions",
                headers=self._request_headers(batch.batch_id, item_id),
                json=payload,
                timeout=self._policy.endpoint.request_timeout_seconds,
            )
            return self._result_from_response(
                response=response,
                output_dir=output_dir,
                batch_id=batch.batch_id,
                item_id=item_id,
            )
        except FileNotFoundError as exc:
            warning = f"hosted request for {item_id} failed: {exc}"
            return _failed_item_result(request_id=None, warning=warning)
        except httpx.RequestError as exc:
            warning = _transport_failure_warning(item_id, exc)
            return _failed_item_result(request_id=None, warning=warning)
        finally:
            if image is not None:
                image.close()

    def _result_from_response(
        self,
        *,
        response: httpx.Response,
        output_dir: Path,
        batch_id: str,
        item_id: str,
    ) -> _ItemInvokeResult:
        """
        Classify one hosted response and persist a witness on success.

        Keyword Args:
            response: Raw hosted completion response.
            output_dir: Output root for witness files.
            batch_id: Planned batch identifier.
            item_id: Batch item identifier for this invocation.

        Returns:
            Per-item hosted invocation outcome.

        """
        request_id = response.headers.get("x-request-id")
        warning = self._response_failure_warning(response, item_id)
        if warning is not None:
            return _failed_item_result(request_id=request_id, warning=warning)
        return self._success_witness_result(
            response=response,
            output_dir=output_dir,
            batch_id=batch_id,
            item_id=item_id,
            request_id=request_id,
        )

    def _response_failure_warning(
        self,
        response: httpx.Response,
        item_id: str,
    ) -> str | None:
        """
        Return a warning when ``response`` represents a hosted item failure.

        Args:
            response: Raw hosted completion response.
            item_id: Batch item identifier for this invocation.

        Returns:
            Warning text when the response failed, otherwise ``None``.

        """
        if response.status_code in self._policy.endpoint.retryable_status_codes:
            return (
                f"hosted request for {item_id} failed with retryable "
                f"status {response.status_code}"
            )
        if response.status_code != httpx.codes.OK:
            return (
                f"hosted request for {item_id} failed with status "
                f"{response.status_code}"
            )
        return None

    def _success_witness_result(
        self,
        *,
        response: httpx.Response,
        output_dir: Path,
        batch_id: str,
        item_id: str,
        request_id: str | None,
    ) -> _ItemInvokeResult:
        """
        Persist one successful hosted response witness.

        Side Effects:
            Writes raw response bytes under ``output_dir/witnesses/``.

        Keyword Args:
            response: Successful hosted completion response.
            output_dir: Output root for witness files.
            batch_id: Planned batch identifier.
            item_id: Batch item identifier for this invocation.
            request_id: Hosted request identifier when present.

        Returns:
            Successful per-item hosted invocation outcome.

        """
        witness_path = self._witness_path(output_dir, batch_id, item_id)
        witness_path.parent.mkdir(parents=True, exist_ok=True)
        witness_path.write_bytes(response.content)
        rel_path = witness_path.relative_to(output_dir).as_posix()
        return {
            "artifact": RunnerOutputArtifact(
                artifact_id=f"witness-{item_id}",
                artifact_kind="text",
                artifact_path=rel_path,
                media_type="application/json",
                batch_item_ids=[item_id],
            ),
            "request_id": request_id,
            "warning": None,
        }

    def _load_item_image(
        self,
        *,
        packaged: PackagedRunnerInput,
        output_dir: Path,
        page_number: int,
    ) -> Image.Image:
        """
        Load one invocation image from the packaged runner input.

        Keyword Args:
            packaged: Packaged input metadata.
            output_dir: Output root containing packaged artifact bytes.
            page_number: One-based page number for PDF inputs.

        Returns:
            Open RGB image that the caller must close.

        Raises:
            FileNotFoundError: If the packaged artifact path is missing.

        """
        artifact_path = output_dir / packaged.artifact_path
        if not artifact_path.is_file():
            msg = f"missing packaged input at {artifact_path}"
            raise FileNotFoundError(msg)
        if packaged.kind is InputKind.PDF:
            return _load_image_from_pdf(artifact_path, page_number)
        return _load_direct_image(artifact_path)

    def _completion_payload(self, image_base64: str) -> dict[str, Any]:
        """
        Build one OpenAI-compatible kraken completion request body.

        Args:
            image_base64: Base64-encoded PNG page image.

        Returns:
            JSON-serializable completion request payload.

        """
        return {
            "model": self._runner.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": KRAKEN_TRANSCRIPTION_PROMPT,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 8000,
            "temperature": 0.0,
        }

    def _auth_headers(self) -> dict[str, str]:
        """
        Return authorization headers for hosted endpoint requests.

        Returns:
            Bearer authorization header map.

        """
        return {"Authorization": f"Bearer {self._token}"}

    def _request_headers(self, batch_id: str, item_id: str) -> dict[str, str]:
        """
        Return hosted invocation headers for one batch item.

        Args:
            batch_id: Planned batch identifier.
            item_id: Batch item identifier.

        Returns:
            Header map including auth, idempotency, and scale-up timeout.

        """
        return {
            **self._auth_headers(),
            "Idempotency-Key": f"{batch_id}:{item_id}",
            "X-Scale-Up-Timeout": str(
                int(self._policy.endpoint.cold_start_timeout_seconds),
            ),
        }

    @staticmethod
    def _witness_path(output_dir: Path, batch_id: str, item_id: str) -> Path:
        """
        Resolve the witness path for one hosted item response.

        Args:
            output_dir: Output root for witness files.
            batch_id: Planned batch identifier.
            item_id: Batch item identifier.

        Returns:
            Absolute witness JSON path.

        """
        return output_dir / "witnesses" / batch_id / f"{item_id}.json"
