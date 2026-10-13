"""The finished article plus generation metadata."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from aiblog.models.outline import Outline


class ArticleMeta(BaseModel):
    provider: str
    model: str
    generated_at: datetime
    word_count: int
    keyword_density: float = 0.0


class Article(BaseModel):
    outline: Outline
    body_markdown: str
    meta: ArticleMeta
    meta_description: str | None = None
    tags: list[str] = Field(default_factory=list)

    def word_count(self) -> int:
        return len(self.body_markdown.split())