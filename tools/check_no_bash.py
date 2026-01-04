"""Reject bash scripts and non-Pixi calls in the repo."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {".git", "node_modules", ".pixi", "__pycache__"}


def find_bash_scripts() -> list[Path]:
    """Collect bash script files under the repo."""
    scripts = []
    for path in ROOT.rglob("*.sh"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        scripts.append(path)
    return scripts


def scan_docs() -> list[str]:
    """Scan docs for references to bash or make usage."""
    issues: list[str] = []
    doc_exts = {".md", ".txt"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in doc_exts:
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT)
        for idx, line in enumerate(path.read_text().splitlines(), start=1):
            stripped = line.strip()
            if ".sh" in stripped and "scripts/" in stripped:
                issues.append(f"{rel}:{idx}: references a .sh script -> {stripped}")
            if stripped.startswith("make "):
                issues.append(f"{rel}:{idx}: uses make; use pixi run -> {stripped}")
            if stripped.startswith(("bash ", "/bin/bash", "/bin/sh")):
                issues.append(f"{rel}:{idx}: uses bash/sh; use pixi run -> {stripped}")
    return issues


def main() -> int:
    """Run checks and emit failures."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    failures = []
    scripts = find_bash_scripts()
    if scripts:
        failures.append("Bash scripts are not allowed:")
        failures.extend([f"- {p.relative_to(ROOT)}" for p in scripts])

    failures.extend(scan_docs())

    if failures:
        logger.error("\n".join(failures))
        return 1

    logger.info("No bash scripts or non-pixi calls detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
