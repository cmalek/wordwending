# Copyright (C) 2026 Chris Malek.
"""Thin wrapper around ``huggingface_hub`` Inference Endpoint APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from huggingface_hub import HfApi, InferenceEndpoint
from huggingface_hub.errors import InferenceEndpointError, InferenceEndpointTimeoutError
from huggingface_hub.utils import HfHubHTTPError

from wordwending.exc import ConfigurationError, EndpointLifecycleError
from wordwending.models.endpoint_lifecycle import (
    EndpointCatalogEntry,
    EndpointRemoteState,
)

if TYPE_CHECKING:
    from collections.abc import Callable

#: Default idle timeout passed to HF when catalog entries enable scale-to-zero.
DEFAULT_SCALE_TO_ZERO_TIMEOUT_SECONDS = 1800


@runtime_checkable
class EndpointClient(Protocol):
    """
    Common contract for Hugging Face endpoint lifecycle collaborators.

    ``HfEndpointClient`` is the production implementation; fakes may satisfy
    this Protocol in unit tests only.
    """

    def describe(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        """
        Return the remote endpoint snapshot.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint name, status, and URL when available.

        """

    def create(self, entry: EndpointCatalogEntry) -> EndpointRemoteState:
        """
        Create one catalogued endpoint.

        Args:
            entry: Catalog pin describing the endpoint deployment.

        Returns:
            Remote endpoint snapshot immediately after creation.

        """

    def resume(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        """
        Resume one paused endpoint.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint snapshot after resume is requested.

        """

    def pause(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        """
        Pause one running endpoint.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint snapshot after pause is requested.

        """

    def scale_to_zero(
        self,
        name: str,
        *,
        namespace: str | None,
    ) -> EndpointRemoteState:
        """
        Scale one endpoint to zero replicas.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint snapshot after scale-to-zero is requested.

        """

    def delete(self, name: str, *, namespace: str | None) -> None:
        """
        Delete one remote endpoint.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        """

    def wait_ready(
        self,
        name: str,
        *,
        namespace: str | None,
        timeout_seconds: int,
    ) -> EndpointRemoteState:
        """
        Block until the endpoint is ready for inference.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.
            timeout_seconds: Maximum seconds to wait for readiness.

        Returns:
            Remote endpoint snapshot once ready.

        """


class HfEndpointClient:
    """
    Hugging Face Inference Endpoint client with injected API token.

    Args:
        token: Hugging Face user access token for endpoint management.

    Raises:
        ConfigurationError: When ``token`` is missing or empty.

    """

    def __init__(self, token: str) -> None:
        """
        Bind a Hugging Face API token for endpoint management calls.

        Args:
            token: Hugging Face user access token for endpoint management.

        Raises:
            ConfigurationError: When ``token`` is missing or empty.

        """
        if not token:
            msg = "missing huggingface API token"
            raise ConfigurationError(msg)
        #: Hugging Face user access token for endpoint management calls.
        self._token = token
        #: Hub API client bound to the injected token.
        self._api = HfApi(token=token)

    def describe(
        self,
        name: str,
        *,
        namespace: str | None = None,
    ) -> EndpointRemoteState:
        """
        Return the remote endpoint snapshot.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint name, status, and URL when available.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        endpoint = self._call_hub(
            self._api.get_inference_endpoint,
            name,
            namespace=namespace,
            token=self._token,
        )
        return self._map_endpoint(endpoint)

    def create(self, entry: EndpointCatalogEntry) -> EndpointRemoteState:
        """
        Create one catalogued endpoint.

        Args:
            entry: Catalog pin describing the endpoint deployment.

        Returns:
            Remote endpoint snapshot immediately after creation.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        kwargs: dict[str, object] = {
            "repository": entry.repository,
            "framework": entry.framework,
            "accelerator": entry.accelerator,
            "instance_size": entry.instance_size,
            "instance_type": entry.instance_type,
            "region": entry.region,
            "vendor": entry.vendor,
            "revision": entry.revision,
            "task": entry.task,
            "type": entry.endpoint_type,
            "namespace": entry.namespace,
            "token": self._token,
        }
        if entry.scale_to_zero:
            kwargs["scale_to_zero_timeout"] = DEFAULT_SCALE_TO_ZERO_TIMEOUT_SECONDS
        endpoint = self._call_hub(
            self._api.create_inference_endpoint,
            entry.endpoint_name,
            **kwargs,
        )
        return self._map_endpoint(endpoint)

    def resume(
        self,
        name: str,
        *,
        namespace: str | None = None,
    ) -> EndpointRemoteState:
        """
        Resume one paused endpoint.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint snapshot after resume is requested.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        endpoint = self._call_hub(
            self._api.resume_inference_endpoint,
            name,
            namespace=namespace,
            token=self._token,
        )
        return self._map_endpoint(endpoint)

    def pause(
        self,
        name: str,
        *,
        namespace: str | None = None,
    ) -> EndpointRemoteState:
        """
        Pause one running endpoint.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint snapshot after pause is requested.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        endpoint = self._call_hub(
            self._api.pause_inference_endpoint,
            name,
            namespace=namespace,
            token=self._token,
        )
        return self._map_endpoint(endpoint)

    def scale_to_zero(
        self,
        name: str,
        *,
        namespace: str | None = None,
    ) -> EndpointRemoteState:
        """
        Scale one endpoint to zero replicas.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Returns:
            Remote endpoint snapshot after scale-to-zero is requested.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        endpoint = self._call_hub(
            self._api.scale_to_zero_inference_endpoint,
            name,
            namespace=namespace,
            token=self._token,
        )
        return self._map_endpoint(endpoint)

    def delete(self, name: str, *, namespace: str | None = None) -> None:
        """
        Delete one remote endpoint.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        self._call_hub(
            self._api.delete_inference_endpoint,
            name,
            namespace=namespace,
            token=self._token,
        )

    def wait_ready(
        self,
        name: str,
        *,
        namespace: str | None = None,
        timeout_seconds: int,
    ) -> EndpointRemoteState:
        """
        Block until the endpoint is ready for inference.

        Args:
            name: Inference Endpoint name in the hosting provider.

        Keyword Args:
            namespace: Hugging Face namespace override.
            timeout_seconds: Maximum seconds to wait for readiness.

        Returns:
            Remote endpoint snapshot once ready.

        Raises:
            EndpointLifecycleError: When waiting fails or times out.

        """
        endpoint = self._call_hub(
            self._api.get_inference_endpoint,
            name,
            namespace=namespace,
            token=self._token,
        )
        try:
            endpoint = endpoint.wait(timeout=timeout_seconds)
        except InferenceEndpointTimeoutError as exc:
            raise EndpointLifecycleError(str(exc)) from exc
        return self._map_endpoint(endpoint)

    def _call_hub(
        self,
        operation: Callable[..., Any],
        *args: object,
        **kwargs: object,
    ) -> Any:
        """
        Invoke one Hub API operation and map failures to lifecycle errors.

        Args:
            operation: Bound ``HfApi`` endpoint method to invoke.
            *args: Positional arguments forwarded to ``operation``.

        Keyword Args:
            **kwargs: Keyword arguments forwarded to ``operation``.

        Returns:
            Hub ``InferenceEndpoint`` returned by ``operation``.

        Raises:
            EndpointLifecycleError: When the Hub request fails.

        """
        try:
            return operation(*args, **kwargs)
        except (
            InferenceEndpointError,
            InferenceEndpointTimeoutError,
            HfHubHTTPError,
        ) as exc:
            raise EndpointLifecycleError(str(exc)) from exc

    def _map_endpoint(self, endpoint: InferenceEndpoint) -> EndpointRemoteState:
        """
        Map a Hub endpoint object to the local remote-state model.

        Args:
            endpoint: Hub endpoint object returned by the API.

        Returns:
            Normalized remote endpoint snapshot.

        """
        status = endpoint.status
        status_value = status.value if hasattr(status, "value") else status
        return EndpointRemoteState(
            name=endpoint.name,
            status=str(status_value),
            url=endpoint.url,
        )
