"""Keyword density check, slug enforcement, and meta description synthesis."""
from __future__ import annotations

from collections import Counter

from aiblog.config.settings import Settings
from aiblog.models.article import Article
from aiblog.utils.text import normalize_whitespace


class SeoService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def keyword_density(self, article: Article, keywords: list[str]) -> float:
        if not keywords:
            return 0.0
        words = normalize_whitespace(article.body_markdown).lower().split()
        if not words:
            return 0.0
        counts = Counter(words)
        hits = sum(counts[kw.lower()] for kw in keywords)
        return hits / len(words)

    def enforce(self, article: Article, keywords: list[str]) -> Article:
        if not self._settings.seo.enabled:
            return article
        density = self.keyword_density(article, keywords)
        article.meta.keyword_density = round(density, 5)
        if self._settings.seo.inject_meta_description and not article.meta_description:
            words = normalize_whitespace(article.body_markdown).split()
            article.meta_description = " ".join(words[:32]).rstrip(",.") + "…"
        return article