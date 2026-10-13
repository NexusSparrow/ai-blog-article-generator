"""Typed settings model. Mirrors config/default.toml. Pydantic-validated."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    name: str = "AI Blog Article Generator"
    version: str = "0.6.3"
    log_level: str = "INFO"
    log_dir: str = "logs"
    output_dir: str = "generated_articles"


class ProviderEndpoint(BaseModel):
    model: str
    base_url: str
    keyring_service: str


class ProviderSettings(BaseModel):
    default: str = "openai"
    timeout_seconds: int = 90
    max_retries: int = 4
    openai: ProviderEndpoint
    anthropic: ProviderEndpoint
    local: ProviderEndpoint


class OutlineSettings(BaseModel):
    strategy: str = "howto"
    target_words: int = Field(default=1400, ge=200, le=8000)
    sections: int = Field(default=6, ge=2, le=20)


class SeoSettings(BaseModel):
    enabled: bool = True
    keyword_density_max: float = Field(default=0.028, ge=0.0, le=0.1)
    inject_meta_description: bool = True
    slug_max_len: int = Field(default=64, ge=8, le=120)


class ExportSettings(BaseModel):
    formats: list[str] = ["markdown", "html"]
    frontmatter: bool = True


class Settings(BaseModel):
    app: AppSettings
    provider: ProviderSettings
    outline: OutlineSettings
    seo: SeoSettings
    export: ExportSettings