#!/usr/bin/env python3
"""Run minimal acceptance checks for dashboard build."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    run(["python", "scripts/validate_public_inputs.py"])
    run(["python", "scripts/build_dashboard.py"])

    expected = [
        ROOT / "assets" / "plots" / "ok_rate.png",
        ROOT / "assets" / "plots" / "mix_over_time.png",
        ROOT / "assets" / "plots" / "suite_hardening.png",
        ROOT / "assets" / "plots" / "quality_gates.png",
        ROOT / "dashboard" / "index.md",
    ]

    missing = [path for path in expected if not path.exists()]
    if missing:
        missing_str = ", ".join(str(path) for path in missing)
        raise SystemExit(f"Missing expected outputs: {missing_str}")

    print("Acceptance checks passed.")


if __name__ == "__main__":
    main()
