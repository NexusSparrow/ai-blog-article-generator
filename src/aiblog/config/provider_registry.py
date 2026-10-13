"""Maps a provider key to a concrete ArticleProvider adapter."""
from __future__ import annotations

from aiblog.config.settings import Settings
from aiblog.core.interfaces import ArticleProvider
from aiblog.providers.anthropic_provider import AnthropicProvider
from aiblog.providers.local_provider import LocalProvider
from aiblog.providers.openai_provider import OpenAIProvider

_BUILDERS: dict[str, type] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "local": LocalProvider,
}


def build_provider(settings: Settings, key: str | None = None) -> ArticleProvider:
    provider_key = key or settings.provider.default
    try:
        cls = _BUILDERS[provider_key]
    except KeyError as exc:
        raise ValueError(
            f"unknown provider {provider_key!r}; known: {sorted(_BUILDERS)}"
        ) from exc
    endpoint = getattr(settings.provider, provider_key)
    return cls(
        endpoint=endpoint,
        timeout_seconds=settings.provider.timeout_seconds,
        max_retries=settings.provider.max_retries,
    )