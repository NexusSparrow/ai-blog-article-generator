"""Composition root. Wires settings, adapters, and services into one container.

Kept deliberately small: this module knows *how* to assemble the graph, not
*what* any node does. Services receive their collaborators by constructor.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aiblog.config.loader import load_settings
from aiblog.config.provider_registry import build_provider
from aiblog.config.settings import Settings
from aiblog.core.clock import SystemClock
from aiblog.services.export_service import ExportService
from aiblog.services.generation_service import GenerationService
from aiblog.services.outline_service import OutlineService
from aiblog.services.seo_service import SeoService


@dataclass(slots=True)
class Container:
    settings: Settings
    generation_service: GenerationService
    outline_service: OutlineService
    seo_service: SeoService
    export_service: ExportService


def build_container(config_path: Path | None = None, overrides: Path | None = None) -> Container:
    settings = load_settings(config_path=config_path, overrides=overrides)
    provider = build_provider(settings)
    clock = SystemClock()

    outline_service = OutlineService(settings=settings)
    seo_service = SeoService(settings=settings)
    export_service = ExportService(settings=settings)
    generation_service = GenerationService(
        provider=provider,
        outline_service=outline_service,
        seo_service=seo_service,
        export_service=export_service,
        clock=clock,
        settings=settings,
    )
    return Container(
        settings=settings,
        generation_service=generation_service,
        outline_service=outline_service,
        seo_service=seo_service,
        export_service=export_service,
    )