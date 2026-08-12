#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from pathlib import Path

TARGET_REL = Path("docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation")
INSTRUCTION_REL = TARGET_REL / "10_enhance_instruction"
LEDGER_REL = TARGET_REL / "00_enhance_background/80_contract_amendment_log.md"

DEFAULT_AMENDMENT_COMMIT = "6e9c59515abb8c5c5981f96df5ad87782a7cdfc7"
AMENDMENT_ID = "AMEND-001"
LOCAL_MARKER = "### 2026-08-12 — AMEND-001"
TRACE_FIX_HEADING = "## AMEND-001 Traceability Correction — TRACE-FIX-001"

SEMANTIC_RELS = {
    Path("G01/06_G01_P02_navigation_shell_ui.md"),
    Path("G01/07_Ariadne_ENH-E5_G01_test_instruction.md"),
}

METADATA_RELS = {
    Path("README.md"),
    Path("G00/06_Ariadne_ENH-E5_G00_implementation_instruction.md"),
    Path("G00/07_Ariadne_ENH-E5_G00_test_instruction.md"),
    Path("G00/README.md"),
    Path("G01/06_Ariadne_ENH-E5_G01_implementation_instruction.md"),
    Path("G01/06_G01_P00_work_package_plan.md"),
    Path("G01/06_G01_P01_route_and_navigation_state.md"),
    Path("G01/06_G01_P03_history_and_global_regression.md"),
    Path("G01/README.md"),
    Path("G02/06_Ariadne_ENH-E5_G02_implementation_instruction.md"),
    Path("G02/06_G02_P00_work_package_plan.md"),
    Path("G02/06_G02_P01_predictive_compatibility_inventory.md"),
    Path("G02/06_G02_P02_predictive_stage_recomposition.md"),
    Path("G02/06_G02_P03_predictive_regression_and_candidate.md"),
    Path("G02/07_Ariadne_ENH-E5_G02_test_instruction.md"),
    Path("G02/README.md"),
    Path("G03/06_Ariadne_ENH-E5_G03_implementation_instruction.md"),
    Path("G03/06_G03_P00_work_package_plan.md"),
    Path("G03/06_G03_P01_causal_stage_mapping.md"),
    Path("G03/06_G03_P02_identification_estimation_separation.md"),
    Path("G03/06_G03_P03_causal_regression_and_candidate.md"),
    Path("G03/07_Ariadne_ENH-E5_G03_test_instruction.md"),
    Path("G03/README.md"),
    Path("G04/06_Ariadne_ENH-E5_G04_implementation_instruction.md"),
    Path("G04/06_G04_P00_work_package_plan.md"),
    Path("G04/06_G04_P01_exploratory_stage_mapping.md"),
    Path("G04/06_G04_P02_visualization_and_findings_integration.md"),
    Path("G04/06_G04_P03_exploratory_regression_and_candidate.md"),
    Path("G04/07_Ariadne_ENH-E5_G04_test_instruction.md"),
    Path("G04/README.md"),
    Path("G05/06_Ariadne_ENH-E5_G05_implementation_instruction.md"),
    Path("G05/07_Ariadne_ENH-E5_G05_test_instruction.md"),
    Path("G05/README.md"),
}

EXPECTED_ALL_RELS = SEMANTIC_RELS | METADATA_RELS

assert len(SEMANTIC_RELS) == 2
assert len(METADATA_RELS) == 33
assert len(EXPECTED_ALL_RELS) == 35


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Repair AMEND-001 local traceability for all 35 ENH-E5 instruction documents."
    )
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    p.add_argument("--no-diff", action="store_true", help="suppress unified diff")
    p.add_argument(
        "--amendment-commit",
        default=DEFAULT_AMENDMENT_COMMIT,
        help="AMEND-001 application commit used as classification authority",
    )
    p.add_argument(
        "--allow-dirty-target",
        action="store_true",
        help="allow pre-existing uncommitted changes under the ENH-E5 target tree",
    )
    return p.parse_args()


def run_git(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and cp.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed ({cp.returncode}): {cp.stderr.strip()}")
    return cp


def require_git_baseline(root: Path, commit: str) -> None:
    run_git(root, ["cat-file", "-e", f"{commit}^{{commit}}"])
    cp = run_git(root, ["merge-base", "--is-ancestor", commit, "HEAD"], check=False)
    if cp.returncode != 0:
        raise RuntimeError(
            f"AMEND-001 authority commit {commit} is not an ancestor of HEAD; "
            "refusing to infer classification on unrelated history."
        )


def require_clean_target(root: Path) -> None:
    cp = run_git(root, ["status", "--porcelain", "--", TARGET_REL.as_posix()])
    if cp.stdout.strip():
        raise RuntimeError(
            "uncommitted changes exist under the ENH-E5 target tree. "
            "Commit/stash them first, or pass --allow-dirty-target.\n" + cp.stdout
        )


def amendment_changed_instruction_rels(root: Path, commit: str) -> set[Path]:
    cp = run_git(
        root,
        [
            "diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--",
            INSTRUCTION_REL.as_posix(),
        ],
    )
    prefix = INSTRUCTION_REL.as_posix() + "/"
    result: set[Path] = set()
    for raw in cp.stdout.splitlines():
        raw = raw.strip()
        if raw.endswith(".md") and raw.startswith(prefix):
            result.add(Path(raw[len(prefix):]))
    return result


def current_instruction_rels(root: Path) -> set[Path]:
    base = root / INSTRUCTION_REL
    if not base.is_dir():
        raise RuntimeError(f"missing instruction directory: {base}")
    return {p.relative_to(base) for p in base.rglob("*.md") if p.is_file()}


def diff_text(rel: Path, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=rel.as_posix(),
            tofile=rel.as_posix(),
        )
    )


def append_change_log_entry(text: str, entry: str, path: Path) -> tuple[str, bool]:
    if LOCAL_MARKER in text:
        if text.count(LOCAL_MARKER) != 1:
            raise RuntimeError(f"{path}: duplicate AMEND-001 local trace.")
        if "DOCUMENT_METADATA_NORMALIZATION" not in text:
            raise RuntimeError(
                f"{path}: existing AMEND-001 trace is not metadata-only; refusing to overwrite."
            )
        if "Normative semantic change: `NO`" not in text:
            raise RuntimeError(f"{path}: metadata-only AMEND trace lacks semantic-change=NO.")
        return text, False

    entry = entry.rstrip() + "\n"
    heading = "## Change Log\n"
    idx = text.find(heading)
    if idx >= 0:
        insert_at = idx + len(heading)
        suffix = text[insert_at:]
        out = text[:insert_at] + "\n" + entry
        if suffix and not suffix.startswith("\n"):
            out += "\n"
        out += suffix
        return out, True
    return text.rstrip() + "\n\n## Change Log\n\n" + entry, True


def metadata_entry(rel: Path, amendment_commit: str) -> str:
    return f"""### 2026-08-12 — AMEND-001

AMEND-001 application commit で本 instruction の current-state metadata が durable identifier へ正規化されたため、欠落していた local trace を追記する。

- Amendment role: `DOCUMENT_METADATA_NORMALIZATION`
- Normative semantic change: `NO`
- Requirement change: `NO`
- Behavior / acceptance criterion change: `NO`
- Implementation responsibility change: `NO`
- Current-state identifier: `APPROVED / FROZEN`
- Document: `{rel.as_posix()}`
- Classification authority commit: `{amendment_commit}`
- Trace correction record: `00_enhance_background/80_contract_amendment_log.md#amend-001-traceability-correction--trace-fix-001`
"""


def trace_fix_record(amendment_commit: str) -> str:
    semantic = "\n".join(
        f"- `10_enhance_instruction/{p.as_posix()}`" for p in sorted(SEMANTIC_RELS)
    )
    metadata = "\n".join(
        f"- `10_enhance_instruction/{p.as_posix()}`" for p in sorted(METADATA_RELS)
    )
    return f"""{TRACE_FIX_HEADING}

### Status

- Correction status: `APPROVED`
- Correction type: `TRACEABILITY_METADATA_CORRECTION`
- Normative semantic change: `NO`
- Applied date: `2026-08-12`

### Reason for correction

The initial AMEND-001 Traceability Classification Addendum recorded metadata-only instruction changes as `(none)`.
That classification was incorrect.

The AMEND-001 application commit `{amendment_commit}` changed all 35 Markdown documents under `10_enhance_instruction`.
The correct instruction-level classification is:

- normative semantic changes: `2`
- metadata-only changes: `33`
- total changed instruction documents: `35`

This correction does not alter ENH-E5 requirements, Gate semantics, acceptance criteria, implementation responsibilities, or the Operation Availability normative contract. It only repairs amendment traceability.

### Classification authority

- AMEND-001 application commit: `{amendment_commit}`
- Classification rule:
  - G01/P02 and G01/07 are normative semantic contract corrections.
  - The remaining 33 instruction documents were modified only for document-state / canonical-source metadata normalization.

### Normative semantic instruction changes — 2

{semantic}

Classification:

- Amendment role: `CONTRACT_DEFECT_CORRECTION`
- Normative semantic change: `YES`

### Metadata-only instruction changes — 33

{metadata}

Classification:

- Amendment role: `DOCUMENT_METADATA_NORMALIZATION`
- Normative semantic change: `NO`

### Local-trace convergence requirement

After TRACE-FIX-001 is applied:

- all 35 instruction Markdown documents MUST contain exactly one `AMEND-001` local trace;
- the 2 semantic documents MUST be classified as `CONTRACT_DEFECT_CORRECTION`;
- the 33 metadata-only documents MUST be classified as `DOCUMENT_METADATA_NORMALIZATION`;
- the original P02 Trial01 blocker evidence MUST remain unmodified.

### Historical note

The earlier `(none)` entry is retained as historical evidence of the traceability defect and is superseded by this correction record. It is not silently rewritten.
"""


def append_trace_fix_record(ledger: str, record: str, path: Path) -> tuple[str, bool]:
    if TRACE_FIX_HEADING in ledger:
        start = ledger.index(TRACE_FIX_HEADING)
        existing = ledger[start:].strip()
        if existing != record.strip():
            raise RuntimeError(
                f"{path}: existing TRACE-FIX-001 differs from expected; "
                "refusing to rewrite append-only history."
            )
        return ledger, False
    return ledger.rstrip() + "\n\n---\n\n" + record.rstrip() + "\n", True


def audit_semantic_doc(text: str, path: Path) -> None:
    if text.count(LOCAL_MARKER) != 1:
        raise RuntimeError(f"{path}: semantic document must have exactly one AMEND-001 trace.")
    if "CONTRACT_DEFECT_CORRECTION" not in text:
        raise RuntimeError(f"{path}: CONTRACT_DEFECT_CORRECTION missing.")
    if "Normative semantic change: `YES`" not in text:
        raise RuntimeError(f"{path}: semantic-change=YES missing.")


def audit_metadata_doc(text: str, path: Path) -> None:
    if text.count(LOCAL_MARKER) != 1:
        raise RuntimeError(f"{path}: metadata document must have exactly one AMEND-001 trace.")
    if "DOCUMENT_METADATA_NORMALIZATION" not in text:
        raise RuntimeError(f"{path}: DOCUMENT_METADATA_NORMALIZATION missing.")
    if "Normative semantic change: `NO`" not in text:
        raise RuntimeError(f"{path}: semantic-change=NO missing.")
    header = "\n".join(text.splitlines()[:60])
    if "APPROVED / FROZEN" not in header:
        raise RuntimeError(f"{path}: APPROVED / FROZEN missing from header region.")
    relevant = [
        line for line in header.splitlines()
        if "Canonical convergence source" in line and "10 / 21 / 22 / 23 / 30" in line
    ]
    for line in relevant:
        if "APPROVED" not in line:
            raise RuntimeError(f"{path}: canonical convergence source is not APPROVED: {line}")


def audit_ledger(ledger: str, amendment_commit: str) -> None:
    if "## AMEND-001: G01 Operation Availability Contract completion" not in ledger:
        raise RuntimeError("ledger: base AMEND-001 record missing.")
    if TRACE_FIX_HEADING not in ledger:
        raise RuntimeError("ledger: TRACE-FIX-001 missing.")
    section = ledger[ledger.index(TRACE_FIX_HEADING):]
    for rel in sorted(SEMANTIC_RELS | METADATA_RELS):
        needle = f"`10_enhance_instruction/{rel.as_posix()}`"
        if section.count(needle) != 1:
            raise RuntimeError(f"ledger TRACE-FIX-001 path missing/duplicated: {needle}")
    for token in (
        f"AMEND-001 application commit: `{amendment_commit}`",
        "normative semantic changes: `2`",
        "metadata-only changes: `33`",
        "total changed instruction documents: `35`",
        "Correction type: `TRACEABILITY_METADATA_CORRECTION`",
    ):
        if token not in section:
            raise RuntimeError(f"ledger TRACE-FIX-001 required token missing: {token}")


def build_plan(root: Path, amendment_commit: str) -> tuple[dict[Path, str], dict[Path, str]]:
    instruction_root = root / INSTRUCTION_REL
    ledger_path = root / LEDGER_REL
    if not ledger_path.is_file():
        raise RuntimeError(f"missing ledger: {ledger_path}")

    changed_at_amend = amendment_changed_instruction_rels(root, amendment_commit)
    if changed_at_amend != EXPECTED_ALL_RELS:
        missing = sorted(EXPECTED_ALL_RELS - changed_at_amend)
        extra = sorted(changed_at_amend - EXPECTED_ALL_RELS)
        raise RuntimeError(
            "AMEND-001 commit differs from audited 35-file set.\n"
            f"missing={[p.as_posix() for p in missing]}\n"
            f"extra={[p.as_posix() for p in extra]}"
        )

    current = current_instruction_rels(root)
    if current != EXPECTED_ALL_RELS:
        missing = sorted(EXPECTED_ALL_RELS - current)
        extra = sorted(current - EXPECTED_ALL_RELS)
        raise RuntimeError(
            "current instruction Markdown set differs from audited 35-file baseline.\n"
            f"missing={[p.as_posix() for p in missing]}\n"
            f"extra={[p.as_posix() for p in extra]}"
        )

    staged: dict[Path, str] = {}
    before: dict[Path, str] = {}

    for rel in sorted(SEMANTIC_RELS):
        path = instruction_root / rel
        audit_semantic_doc(path.read_text(encoding="utf-8"), path)

    for rel in sorted(METADATA_RELS):
        path = instruction_root / rel
        text = path.read_text(encoding="utf-8")
        after, changed = append_change_log_entry(
            text, metadata_entry(rel, amendment_commit), path
        )
        if changed:
            before[path] = text
            staged[path] = after

    ledger = ledger_path.read_text(encoding="utf-8")
    ledger_after, changed = append_trace_fix_record(
        ledger, trace_fix_record(amendment_commit), ledger_path
    )
    if changed:
        before[ledger_path] = ledger
        staged[ledger_path] = ledger_after

    for rel in sorted(SEMANTIC_RELS):
        path = instruction_root / rel
        audit_semantic_doc(staged.get(path, path.read_text(encoding="utf-8")), path)
    for rel in sorted(METADATA_RELS):
        path = instruction_root / rel
        audit_metadata_doc(staged.get(path, path.read_text(encoding="utf-8")), path)

    audit_ledger(staged.get(ledger_path, ledger), amendment_commit)

    all_local_traces = semantic_count = metadata_count = 0
    for rel in sorted(EXPECTED_ALL_RELS):
        path = instruction_root / rel
        text = staged.get(path, path.read_text(encoding="utf-8"))
        all_local_traces += int(text.count(LOCAL_MARKER) == 1)
        semantic_count += int(rel in SEMANTIC_RELS and "CONTRACT_DEFECT_CORRECTION" in text)
        metadata_count += int(rel in METADATA_RELS and "DOCUMENT_METADATA_NORMALIZATION" in text)

    if (all_local_traces, semantic_count, metadata_count) != (35, 2, 33):
        raise RuntimeError(
            "postcondition mismatch: "
            f"{(all_local_traces, semantic_count, metadata_count)} != (35, 2, 33)"
        )
    return staged, before


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    if not (root / ".git").exists():
        raise RuntimeError(f"not a Git repository root: {root}")
    if not (root / TARGET_REL).is_dir():
        raise RuntimeError(f"missing ENH-E5 target tree: {root / TARGET_REL}")

    require_git_baseline(root, args.amendment_commit)
    if not args.allow_dirty_target:
        require_clean_target(root)

    staged, before = build_plan(root, args.amendment_commit)

    print("ENH-E5 AMEND-001 trace repair summary")
    print(f"  classification authority commit: {args.amendment_commit}")
    print("  audited instruction files: 35")
    print("  semantic instruction files: 2")
    print("  metadata-only instruction files: 33")
    print(f"  files changed by this run: {len(staged)}")
    for path in sorted(staged):
        print(f"    - {path.relative_to(root).as_posix()}")

    if not args.no_diff:
        for path in sorted(staged):
            d = diff_text(path.relative_to(root), before[path], staged[path])
            if d:
                print(d, end="" if d.endswith("\n") else "\n")

    if args.apply:
        for path, text in staged.items():
            path.write_text(text, encoding="utf-8")
        print("APPLIED")
    else:
        print("DRY-RUN ONLY. Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
