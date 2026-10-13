"""Wraps outline strategies behind a single entry point."""
from __future__ import annotations

from aiblog.config.settings import Settings
from aiblog.core.interfaces import OutlineStrategy
from aiblog.models.brief import Brief
from aiblog.models.outline import Outline
from aiblog.outline.howto_strategy import HowToStrategy
from aiblog.outline.listicle_strategy import ListicleStrategy

_STRATEGIES: dict[str, type] = {
    "howto": HowToStrategy,
    "listicle": ListicleStrategy,
}


class OutlineService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def build(self, brief: Brief, strategy_key: str | None = None) -> Outline:
        key = strategy_key or self._settings.outline.strategy
        try:
            strategy_cls = _STRATEGIES[key]
        except KeyError as exc:
            raise ValueError(f"unknown outline strategy {key!r}") from exc
        strategy: OutlineStrategy = strategy_cls()
        return strategy.build(
            brief,
            sections=self._settings.outline.sections,
            target_words=self._settings.outline.target_words,
        )