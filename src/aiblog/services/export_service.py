"""Renders an Article to markdown or html and writes it to disk."""
from __future__ import annotations

from pathlib import Path

from markdown_it import MarkdownIt

from aiblog.config.settings import Settings
from aiblog.core.errors import ExportError
from aiblog.models.article import Article


class ExportService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._md = MarkdownIt("commonmark", {"html": False})

    def _frontmatter(self, article: Article) -> str:
        if not self._settings.export.frontmatter:
            return ""
        lines = [
            "---",
            f"title: {article.outline.title}",
            f"slug: {article.outline.slug}",
            f"provider: {article.meta.provider}",
            f"model: {article.meta.model}",
            f"generated_at: {article.meta.generated_at.isoformat()}",
        ]
        if article.meta_description:
            lines.append(f"description: {article.meta_description}")
        lines.append("---\n")
        return "\n".join(lines)

    def render(self, article: Article, fmt: str) -> str:
        body = article.body_markdown
        if fmt == "markdown":
            return self._frontmatter(article) + body
        if fmt == "html":
            return self._md.render(body)
        raise ExportError(f"unsupported format {fmt!r}")

    def save(self, article: Article, out_dir: Path | None, fmt: str) -> Path:
        target_dir = out_dir or Path(self._settings.app.output_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        ext = "md" if fmt == "markdown" else "html"
        path = target_dir / f"{article.outline.slug}.{ext}"
        try:
            path.write_text(self.render(article, fmt), encoding="utf-8")
        except OSError as exc:
            raise ExportError(f"failed to write {path}: {exc}") from exc
        return path