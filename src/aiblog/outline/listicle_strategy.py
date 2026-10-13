"""Listicle outline: intro, N numbered items, closing takeaway."""
from __future__ import annotations

from aiblog.core.interfaces import OutlineStrategy
from aiblog.models.brief import Brief
from aiblog.models.outline import Outline, Section
from aiblog.utils.slug import slugify


class ListicleStrategy(OutlineStrategy):
    def build(self, brief: Brief, sections: int, target_words: int) -> Outline:
        item_count = max(3, sections)
        per_item = max(100, target_words // (item_count + 2))
        built: list[Section] = [
            Section(
                heading=f"{item_count} things to know about {brief.topic}",
                intent="Frame the list and set reader expectations.",
                target_words=per_item,
            )
        ]
        for i in range(1, item_count + 1):
            built.append(
                Section(
                    heading=f"{i}. {brief.topic.title()} angle #{i}",
                    intent=f"Deliver a self-contained take on item {i}.",
                    target_words=per_item,
                )
            )
        built.append(
            Section(
                heading="The one that actually matters",
                intent="Pick a favorite and argue for it.",
                target_words=per_item,
            )
        )
        return Outline(
            title=f"{item_count} Things About {brief.topic.title()}",
            slug=slugify(brief.topic),
            sections=built,
            strategy="listicle",
        )