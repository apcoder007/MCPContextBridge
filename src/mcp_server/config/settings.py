"""Application configuration.

Configuration is loaded from environment variables and, when present,
from a local .env file.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = Field(
        default="production-mcp-server",
        description="Application name.",
    )

    app_version: str = Field(
        default="0.1.0",
        description="Application version.",
    )

    environment: str = Field(
        default="development",
        description="Runtime environment.",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode.",
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    log_level: str = Field(
        default="INFO",
        description="Application log level.",
    )

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    database_url: str | None = Field(
        default=None,
        description="Database connection URL.",
    )

    # ------------------------------------------------------------------
    # Redis
    # ------------------------------------------------------------------

    redis_url: str | None = Field(
        default=None,
        description="Redis connection URL.",
    )

    # ------------------------------------------------------------------
    # MCP
    # ------------------------------------------------------------------

    mcp_host: str = Field(
        default="127.0.0.1",
        description="MCP server host.",
    )

    mcp_port: int = Field(
        default=8000,
        description="MCP server port.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MCP_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()


settings = get_settings()