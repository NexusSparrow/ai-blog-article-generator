"""The user's input: a topic brief plus optional constraints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Brief(BaseModel):
    topic: str = Field(min_length=3, max_length=300)
    audience: str = "general readers"
    tone: str = "informative"
    keywords: list[str] = Field(default_factory=list)
    notes: str | None = None

    @classmethod
    def from_input(cls, raw: str) -> "Brief":
        """Accepts either a plain topic string or a 'topic :: audience' shorthand."""
        if "::" in raw:
            topic, audience = (part.strip() for part in raw.split("::", 1))
            return cls(topic=topic, audience=audience)
        return cls(topic=raw.strip())