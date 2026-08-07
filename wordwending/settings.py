# Copyright (C) 2026 Chris Malek.
"""
Settings management for wordwending.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl, Field, SecretStr, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from wordwending.exc import ConfigurationError
from wordwending.models.endpoint_lifecycle import (
    EndpointCatalogEntry,
    default_endpoint_catalog,
)


class Settings(BaseSettings):
    """
    Application settings with cascading configuration support.

    Note:
        The app_name and app_version fields are readonly (frozen=True) and
        cannot be overridden via configuration files or environment variables.
        Other fields remain configurable as normal.

    """

    #: Pydantic settings configuration for env prefix and extra-field policy.
    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="WORDWENDING_",
    )

    #: Readonly application name exposed by the CLI and logs.
    app_name: str = Field(
        default="wordwending",
        description="Application name",
        frozen=True,
    )
    #: Readonly application version exposed by the CLI and logs.
    app_version: str = Field(
        default="0.1.0", description="Application version", frozen=True
    )

    #: Default CLI output format when the user does not override it.
    default_output_format: Literal["table", "json", "text"] = Field(
        default="table", description="Default output format"
    )
    #: Whether Rich-style colored terminal output is enabled.
    enable_colors: bool = Field(default=True, description="Enable colored output")
    #: Whether the CLI suppresses non-essential output.
    quiet_mode: bool = Field(default=False, description="Enable quiet mode")

    #: Root logging level for application diagnostics.
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Logging level"
    )
    #: Optional filesystem path for persistent log output.
    log_file: str | None = Field(default=None, description="Log file path")

    #: Hugging Face API token for hosted inference endpoints.
    huggingface_api_key: SecretStr | None = Field(
        default=None,
        description="Hugging Face API token for hosted inference endpoints",
    )
    #: Named Hugging Face endpoint URLs keyed by endpoint identifier.
    huggingface_model_endpoints: dict[str, AnyHttpUrl] = Field(
        default_factory=dict,
        description="Named Hugging Face endpoint URLs keyed by endpoint identifier",
    )
    #: Hugging Face Inference Endpoint namespace override for catalog entries.
    huggingface_endpoint_namespace: str | None = Field(
        default=None,
        description="Hugging Face Inference Endpoint namespace override",
    )
    #: Minutes of inactivity before the idle watchdog pauses endpoints.
    huggingface_endpoint_idle_minutes: int = Field(
        default=30,
        ge=1,
        description="Idle minutes before endpoint lifecycle watchdog pauses",
    )
    #: Maximum seconds to wait for endpoint create or resume readiness.
    huggingface_endpoint_wait_timeout_seconds: int = Field(
        default=900,
        ge=1,
        description="Seconds to wait for endpoint readiness during ensure",
    )
    #: Optional path for the endpoint session ledger JSON file.
    huggingface_endpoint_ledger_path: Path | None = Field(
        default=None,
        description=(
            "Path to endpoint session ledger; defaults to "
            "~/.config/wordwending/endpoint-session-ledger.json"
        ),
    )
    #: Catalog entries keyed by runner_id; empty list uses built-in defaults.
    huggingface_endpoint_catalog: list[EndpointCatalogEntry] = Field(
        default_factory=list,
        description="Endpoint catalog entries keyed by runner_id",
    )

    @field_validator("huggingface_model_endpoints")
    @classmethod
    def validate_https_huggingface_endpoints(
        cls,
        endpoints: dict[str, AnyHttpUrl],
    ) -> dict[str, AnyHttpUrl]:
        """
        Require HTTPS for every configured Hugging Face endpoint URL.

        Args:
            endpoints: Endpoint name to URL mapping from settings input.

        Returns:
            The validated endpoint mapping.

        Raises:
            ValueError: If any endpoint URL does not use HTTPS.

        """
        for endpoint_name, endpoint_url in endpoints.items():
            if endpoint_url.scheme != "https":
                msg = (
                    f"huggingface_model_endpoints[{endpoint_name!r}] "
                    "must use an https URL"
                )
                raise ValueError(msg)
        return endpoints

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Load settings from file with cascading configuration.

        Args:
            settings_cls: Settings model class used to build TOML sources.
            init_settings: Initializer-provided settings source.
            env_settings: Environment-variable settings source.
            dotenv_settings: Dotenv-file settings source.
            file_secret_settings: Secrets-directory settings source.

        Returns:
            Ordered settings sources with the highest-precedence config file,
            when one exists.

        """
        # Define configuration file paths in order of precedence
        config_paths = []

        # Global configuration
        if os.name == "nt":  # Windows
            global_config = (
                Path(os.environ.get("PROGRAMDATA", "C:/ProgramData"))
                / "wordwending.toml"
            )
        else:  # Unix-like
            global_config = Path("/etc/wordwending.toml")

        if global_config.exists():
            config_paths.append(global_config)

        # User home configuration
        user_config = Path.home() / ".wordwending.toml"
        if user_config.exists():
            config_paths.append(user_config)

        # Local configuration
        local_config = Path.cwd() / ".wordwending.toml"
        if local_config.exists():
            config_paths.append(local_config)

        config_file = os.environ.get("WORDWENDING_CONFIG_FILE")
        # Explicit configuration file (highest precedence)
        if config_file:
            explicit_config = Path(config_file)
            if explicit_config.exists():
                config_paths.append(explicit_config)

        # Load settings with file configuration
        if config_paths:
            # Use the last (highest precedence) config file
            config_file_path = config_paths[-1]
            return (
                init_settings,
                TomlConfigSettingsSource(settings_cls, config_file_path.resolve()),
                env_settings,
                dotenv_settings,
                file_secret_settings,
            )

        # Preserve the default Pydantic source order when no config file exists.
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    def resolved_endpoint_ledger_path(self) -> Path:
        """
        Resolve the endpoint session ledger path.

        Returns:
            Configured ledger path or the default under the user config dir.

        """
        if self.huggingface_endpoint_ledger_path is not None:
            return self.huggingface_endpoint_ledger_path
        return (
            Path.home()
            / ".config"
            / "wordwending"
            / "endpoint-session-ledger.json"
        )

    def effective_endpoint_catalog(self) -> list[EndpointCatalogEntry]:
        """
        Return configured catalog entries or the built-in defaults.

        Returns:
            Non-empty catalog entries for endpoint lifecycle operations.

        """
        if self.huggingface_endpoint_catalog:
            return self.huggingface_endpoint_catalog
        return default_endpoint_catalog()

    def get_config_paths(self) -> list[Path]:
        """
        Get list of configuration file paths that were loaded.
        Use this for debugging.

        Returns:
            List of configuration file paths

        """
        paths = []

        # Global configuration
        if os.name == "nt":  # Windows
            global_config = (
                Path(os.environ.get("PROGRAMDATA", "C:/ProgramData"))
                / "wordwending.toml"
            )
        else:  # Unix-like
            global_config = Path("/etc/wordwending.toml")

        if global_config.exists():
            paths.append(global_config)

        # User home configuration
        user_config = Path.home() / ".wordwending.toml"
        if user_config.exists():
            paths.append(user_config)

        # Local configuration
        local_config = Path.cwd() / ".wordwending.toml"
        if local_config.exists():
            paths.append(local_config)

        return paths

    def validate_settings(self) -> None:
        """
        Validate settings and ensure required directories exist.

        Raises:
            ConfigurationError: If settings are invalid

        """
        # Validate output format
        if self.default_output_format not in ["table", "json", "text"]:
            msg = f"Invalid output format: {self.default_output_format}"
            raise ConfigurationError(msg)
