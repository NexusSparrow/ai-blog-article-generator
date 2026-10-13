"""CLI entry point. Thin bootstrap: parse args, hand off to the app service."""
from __future__ import annotations

import argparse
import asyncio
import sys

from aiblog.bootstrap import build_container
from aiblog.utils.logging import configure_logging


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="aiblog", description="AI Blog Article Generator")
    parser.add_argument("brief", nargs="?", help="topic brief, or path to a .txt/.md brief")
    parser.add_argument("-o", "--out", default=None, help="output directory override")
    parser.add_argument("-p", "--provider", default=None, help="provider key override")
    parser.add_argument("--format", default="markdown", choices=["markdown", "html"])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    container = build_container()
    configure_logging(container.settings.app.log_level, container.settings.app.log_dir)
    if not args.brief:
        from aiblog.desktop.app import main as gui_main

        return gui_main()
    result = asyncio.run(
        container.generation_service.generate_from_brief(
            brief=args.brief,
            provider_key=args.provider,
            out_dir=args.out,
            fmt=args.format,
        )
    )
    print(result.saved_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())