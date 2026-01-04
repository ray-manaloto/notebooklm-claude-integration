"""Install MCP server configurations for Claude Desktop and Code."""

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "mcp-config"
SOURCE_FILE = CONFIG_DIR / "servers.json"


def _load_servers() -> dict[str, dict[str, object]]:
    """Load MCP server definitions from the repo."""
    if not SOURCE_FILE.exists():
        message = f"Source file not found: {SOURCE_FILE}"
        raise FileNotFoundError(message)
    return json.loads(SOURCE_FILE.read_text())


def _run(cmd: list[str]) -> None:
    """Run a CLI command."""
    subprocess.run(cmd, check=True)  # noqa: S603


def _desktop_config_path() -> Path:
    """Return the Claude Desktop config path for the current OS."""
    if sys.platform == "darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "Claude"
            / "claude_desktop_config.json"
        )
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            message = "APPDATA not set"
            raise RuntimeError(message)
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def install_desktop() -> None:
    """Write MCP configs to the Claude Desktop config file."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    servers = _load_servers()
    config_path = _desktop_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        backup = config_path.with_suffix(f".backup.{stamp}")
        shutil.copy2(config_path, backup)
        logger.info("Created backup: %s", backup)

    payload = {"mcpServers": servers}
    config_path.write_text(json.dumps(payload, indent=2))
    logger.info("Installed %s MCP servers to %s", len(servers), config_path)


def install_code() -> None:
    """Register MCP servers with the Claude Code CLI."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    servers = _load_servers()
    claude_path = shutil.which("claude")
    if claude_path is None:
        message = "Claude Code CLI not found. Install with: npm install -g @anthropic/claude-code"
        raise RuntimeError(message)

    for name, server_config in servers.items():
        config_payload = dict(server_config)
        config_payload.pop("description", None)
        with contextlib.suppress(subprocess.CalledProcessError):
            _run([claude_path, "mcp", "remove", name])
        _run(
            [
                claude_path,
                "mcp",
                "add-json",
                name,
                json.dumps(config_payload),
                "--scope",
                "user",
            ],
        )
        desc = servers.get(name, {}).get("description", "No description")
        logger.info("Installed %s: %s", name, desc)


def update_all() -> None:
    """Install MCP configs for both Desktop and Code."""
    install_desktop()
    install_code()


def main() -> int:
    """Parse CLI args and execute the requested task."""
    parser = argparse.ArgumentParser(description="MCP config tasks")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("install-desktop")
    sub.add_parser("install-code")
    sub.add_parser("update-all")

    args = parser.parse_args()
    if args.command == "install-desktop":
        install_desktop()
    elif args.command == "install-code":
        install_code()
    elif args.command == "update-all":
        update_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
