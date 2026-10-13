"""Structured article skeleton produced before generation."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Section(BaseModel):
    heading: str
    intent: str
    target_words: int = Field(ge=50, le=1200)


class Outline(BaseModel):
    title: str
    slug: str
    sections: list[Section]
    strategy: str

    @property
    def total_words(self) -> int:
        return sum(section.target_words for section in self.sections)