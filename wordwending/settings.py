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
