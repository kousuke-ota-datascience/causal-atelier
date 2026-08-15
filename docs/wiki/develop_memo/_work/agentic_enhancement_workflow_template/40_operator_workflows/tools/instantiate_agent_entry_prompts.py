#!/usr/bin/env python3
"""Instantiate template agent entry prompts into one Enhancement work root."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from readme_naming import readme_filename_for_directory

FIXED = [
    "PROJECT_NAME", "ENHANCE_ID", "ENHANCE_SHORT_ID", "BRANCH_NAME",
    "REMOTE_NAME", "WORK_ROOT", "WORK_DIR_NAME",
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--template-root", required=True, type=Path)
    p.add_argument("--work-root", required=True, type=Path)
    for key in FIXED:
        if key == "WORK_ROOT":
            continue
        p.add_argument("--" + key.lower().replace("_", "-"), required=True)
    args = p.parse_args()

    template_root = args.template_root.resolve()
    work_root = args.work_root.resolve()
    src = template_root / "40_operator_workflows" / "agent_entry_prompts"
    dst = work_root / "40_operator_workflows" / "agent_entry_prompts"
    if not src.is_dir():
        raise SystemExit(f"template prompt directory not found: {src}")
    if src.resolve() == dst.resolve():
        raise SystemExit("refusing to instantiate into template source directory")

    src_readme = readme_filename_for_directory(template_root, src)
    dst_readme = readme_filename_for_directory(work_root, dst)
    if src_readme != dst_readme:
        raise SystemExit(
            f"README naming invariant mismatch between template and Enhancement instance: {src_readme} != {dst_readme}"
        )
    if not (src / src_readme).is_file():
        raise SystemExit(f"canonical prompt README missing: {src / src_readme}")
    if (src / "README.md").exists():
        raise SystemExit("nested unqualified README.md is forbidden in template prompt directory")

    values = {key: getattr(args, key.lower()) for key in FIXED if key != "WORK_ROOT"}
    values["WORK_ROOT"] = str(args.work_root)
    values["WORK_DIR_NAME"] = args.work_dir_name

    dst.mkdir(parents=True, exist_ok=True)
    for path in src.iterdir():
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        out_name = dst_readme if path.name == src_readme else path.name
        (dst / out_name).write_text(text, encoding="utf-8")

    # A nested README.md must never be produced by instantiation.
    stale = dst / "README.md"
    if stale.exists():
        print(f"BLOCKED_README_NAMING: nested unqualified README produced: {stale}", file=sys.stderr)
        return 2

    unresolved = []
    fixed_re = re.compile(r"\{\{(" + "|".join(map(re.escape, FIXED)) + r")\}\}")
    for path in dst.glob("*.md"):
        if fixed_re.search(path.read_text(encoding="utf-8")):
            unresolved.append(str(path))
    if unresolved:
        print("BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED", file=sys.stderr)
        for item in unresolved:
            print(item, file=sys.stderr)
        return 2

    print(dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
