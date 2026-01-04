"""Run NotebookLM MCP tools via Codex CLI using Pixi tasks."""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
from typing import Any

logger = logging.getLogger("nlm_tasks")

CONFIRM_REQUIRED = {
    "notebook_delete",
    "source_sync_drive",
    "source_delete",
    "audio_overview_create",
    "video_overview_create",
    "infographic_create",
    "slide_deck_create",
    "studio_delete",
}


def _configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _load_args(args_json: str) -> dict[str, Any]:
    if not args_json:
        return {}
    try:
        parsed = json.loads(args_json)
    except json.JSONDecodeError as exc:
        message = f"Invalid JSON for args: {exc}"
        raise ValueError(message) from exc
    if not isinstance(parsed, dict):
        message = "Args JSON must decode to an object"
        raise ValueError(message)
    return parsed


def _build_prompt(tool: str, args: dict[str, Any]) -> str:
    tool_name = f"mcp__notebooklm-rpc__{tool}"
    if args:
        args_json = json.dumps(args, sort_keys=True)
        return (
            "Use the notebooklm-patterns skill with the notebooklm-rpc server. "
            f"Call {tool_name} with arguments: {args_json}."
        )
    return (
        "Use the notebooklm-patterns skill with the notebooklm-rpc server. "
        f"Call {tool_name} with no arguments."
    )


def _run_codex(prompt: str) -> None:
    subprocess.run(
        ["codex", "--enable", "skills", "exec", prompt],
        check=True,
    )  # noqa: S603


def main() -> int:
    _configure_logging()
    parser = argparse.ArgumentParser(
        description="Run a NotebookLM MCP tool via Codex CLI.",
    )
    parser.add_argument("tool", help="NotebookLM tool name (e.g. notebook_list)")
    parser.add_argument(
        "--args",
        dest="args_json",
        default=None,
        help="Optional JSON object of tool arguments.",
    )
    parsed = parser.parse_args()

    tool = parsed.tool
    if tool in CONFIRM_REQUIRED and os.environ.get("NLM_CONFIRM") != "1":
        logger.error(
            "Tool %s requires confirmation. Re-run with NLM_CONFIRM=1.",
            tool,
        )
        return 2

    args_json = parsed.args_json or os.environ.get("NLM_ARGS_JSON", "")
    try:
        tool_args = _load_args(args_json)
    except ValueError as exc:
        logger.error(str(exc))
        return 2

    prompt = _build_prompt(tool, tool_args)
    _run_codex(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
