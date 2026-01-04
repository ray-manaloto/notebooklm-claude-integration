"""Run simulation tests and write a cache stamp."""

from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = ROOT / ".pixi-cache" / "simulation.stamp"


def main() -> int:
    """Run simulation tests."""
    subprocess.run([sys.executable, "tests/run_simulation.py"], check=True, cwd=ROOT)  # noqa: S603
    STAMP.parent.mkdir(parents=True, exist_ok=True)
    STAMP.write_text(f"ok {datetime.now(UTC).isoformat()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
