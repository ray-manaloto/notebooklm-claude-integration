"""Run Ruff checks and write a cache stamp."""

from __future__ import annotations

import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = ROOT / ".pixi-cache" / "ruff.stamp"


def main() -> int:
    """Run Ruff in the repository root."""
    ruff = shutil.which("ruff")
    if not ruff:
        message = "ruff not found on PATH"
        raise RuntimeError(message)
    subprocess.run([ruff, "check", "."], check=True, cwd=ROOT)  # noqa: S603
    STAMP.parent.mkdir(parents=True, exist_ok=True)
    STAMP.write_text(f"ok {datetime.now(UTC).isoformat()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
