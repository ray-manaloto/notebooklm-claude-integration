"""Utility to keep Pixi environments current."""

from __future__ import annotations

import argparse
import subprocess


def run(cmd: list[str]) -> None:
    """Run a Pixi command with failure propagation."""
    subprocess.run(cmd, check=True)  # noqa: S603


def main() -> None:
    """Parse CLI args and run requested Pixi actions."""
    parser = argparse.ArgumentParser(description="Manage Pixi environment updates.")
    parser.add_argument("action", choices=["update", "install", "sync"])
    args = parser.parse_args()

    if args.action in {"update", "sync"}:
        run(["pixi", "update"])
    if args.action in {"install", "sync"}:
        run(["pixi", "install", "--locked"])


if __name__ == "__main__":
    main()
