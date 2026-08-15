#!/usr/bin/env python3
"""Run the exact ENH-E7 G04 Trial02 protected-regression manifest.

This is a verification asset, not Product code.  The manifest deliberately lists
node IDs so a directory-wide pytest invocation cannot silently change Gate scope.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
MANIFEST = REPOSITORY / "tests/product/manifests/enh_e7_g04_trial02_cprs.json"


def _run(command: list[str]) -> int:
    print("+", " ".join(command), flush=True)
    return subprocess.run(command, cwd=REPOSITORY, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--regular-only", action="store_true")
    parser.add_argument("--postgres-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.regular_only and arguments.postgres_only:
        parser.error("--regular-only and --postgres-only are mutually exclusive")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not arguments.postgres_only:
        regular = _run([sys.executable, "-m", "pytest", "-q", *manifest["regular_pytest_node_ids"]])
        if regular:
            return regular
        browser = _run(manifest["browser_command"])
        if browser:
            return browser
    if not arguments.regular_only:
        return _run([
            "scripts/test/run_product_postgres_tests.sh",
            *manifest["postgres_runner_node_ids"],
        ])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
