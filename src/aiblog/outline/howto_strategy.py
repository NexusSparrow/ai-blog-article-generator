"""How-to outline: intro, prerequisites, N steps, pitfalls, conclusion."""
from __future__ import annotations

from aiblog.core.interfaces import OutlineStrategy
from aiblog.models.brief import Brief
from aiblog.models.outline import Outline, Section
from aiblog.utils.slug import slugify


class HowToStrategy(OutlineStrategy):
    def build(self, brief: Brief, sections: int, target_words: int) -> Outline:
        step_count = max(2, sections - 3)
        per_section = max(120, target_words // (step_count + 3))
        built: list[Section] = [
            Section(
                heading=f"Why {brief.topic} matters in 2026",
                intent="Hook the reader and state the payoff.",
                target_words=per_section,
            ),
            Section(
                heading="Prerequisites and setup",
                intent="List what the reader needs before starting.",
                target_words=per_section,
            ),
        ]
        for i in range(1, step_count + 1):
            built.append(
                Section(
                    heading=f"Step {i}: {brief.topic} in practice",
                    intent=f"Walk through step {i} of {step_count} concretely.",
                    target_words=per_section,
                )
            )
        built.append(
            Section(
                heading="Common pitfalls",
                intent="Name the mistakes readers make and how to avoid them.",
                target_words=per_section,
            )
        )
        built.append(
            Section(
                heading="Where to go next",
                intent="Close with forward momentum, not a summary.",
                target_words=per_section,
            )
        )
        return Outline(
            title=f"{brief.topic.title()}: A Practical Guide",
            slug=slugify(brief.topic),
            sections=built,
            strategy="howto",
        )