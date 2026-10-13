"""Abstract contracts. Everything pluggable implements one of these."""
from __future__ import annotations

from abc import ABC, abstractmethod

from aiblog.models.article import Article
from aiblog.models.brief import Brief
from aiblog.models.outline import Outline


class ArticleProvider(ABC):
    """LLM-backed text generation. One call = one completion."""

    @abstractmethod
    async def complete(self, system: str, prompt: str) -> str:
        """Return the raw completion text. Raises ProviderError on failure."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable provider key, e.g. 'openai'."""


class OutlineStrategy(ABC):
    """Turns a Brief into a structured Outline."""

    @abstractmethod
    def build(self, brief: Brief, sections: int, target_words: int) -> Outline: ...


class PostProcessor(ABC):
    """Transforms an Article in place or returns a new one."""

    @abstractmethod
    def apply(self, article: Article) -> Article: ...