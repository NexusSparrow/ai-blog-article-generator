# Contributing to ai-blog-article-generator

Thanks for wanting to help build the generator. This project is a Windows desktop
tool that turns a topic brief into a full blog article using pluggable LLM
providers, outline strategies, and SEO post-processors.

## Ground rules

1. Python 3.11+ is required. We target CPython on Windows 10/11 x64.
2. Every PR must pass `pytest`, `ruff`, and `mypy --strict` on the touched modules.
3. New providers, outline strategies, or post-processors go behind their
   respective interfaces in `src/aiblog/core/interfaces.py`. Do not fork logic
   into handlers.
4. Handlers stay thin. Business logic belongs in `src/aiblog/services/`.
5. No new top-level dependencies without a note in the PR description explaining
   the size and license.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

## Branch / commit style

- Branches: `feat/<area>-<slug>`, `fix/<area>-<slug>`, `chore/<slug>`.
- Commits: conventional commits (`feat(providers): add anthropic adapter`).

## Adding a provider adapter

1. Create `src/aiblog/providers/<name>_provider.py`.
2. Subclass `ArticleProvider` from `src/aiblog/core/interfaces.py`.
3. Register it in `src/aiblog/config/provider_registry.py`.
4. Add a fixture-backed test in `tests/test_providers.py`.

## Adding an outline strategy

1. Create `src/aiblog/outline/<name>_strategy.py`.
2. Implement `OutlineStrategy.build(brief) -> Outline`.
3. Add the strategy key to `config/default.toml` under `[outline]`.

## Reporting bugs

Open an issue with the app version (Help → About), the provider used, the brief
text if it is not sensitive, and the last 60 lines of `logs/aiblog.log`.