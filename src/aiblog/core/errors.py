"""Typed errors. Handlers catch these, not bare Exception."""
from __future__ import annotations


class AiblogError(Exception):
    """Base class for all application errors."""


class ConfigError(AiblogError):
    """Malformed or missing configuration."""


class ProviderError(AiblogError):
    """Upstream LLM call failed after retries."""

    def __init__(self, provider: str, status: int | None, detail: str) -> None:
        super().__init__(f"[{provider}] status={status} {detail}")
        self.provider = provider
        self.status = status
        self.detail = detail


class ExportError(AiblogError):
    """Rendering or writing the article to disk failed."""