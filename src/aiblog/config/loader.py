"""Loads default.toml, merges config.local.toml if present, validates to Settings."""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from aiblog.config.settings import Settings

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_CONFIG = _REPO_ROOT / "config" / "default.toml"
_LOCAL_CONFIG = _REPO_ROOT / "config.local.toml"


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_settings(config_path: Path | None = None, overrides: Path | None = None) -> Settings:
    primary = config_path or _DEFAULT_CONFIG
    raw = tomllib.loads(primary.read_text(encoding="utf-8"))
    local = overrides if overrides is not None else _LOCAL_CONFIG
    if local.exists():
        raw = _deep_merge(raw, tomllib.loads(local.read_text(encoding="utf-8")))
    return Settings.model_validate(raw)