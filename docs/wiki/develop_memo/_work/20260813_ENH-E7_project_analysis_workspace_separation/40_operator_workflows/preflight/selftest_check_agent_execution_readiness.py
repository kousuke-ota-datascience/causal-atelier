#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import tempfile
import re
import sys

WORK_DIR_NAME = "20260813_ENH-E7_project_analysis_workspace_separation"
SCRIPT_REL = Path(
    "docs/wiki/develop_memo/_work"
) / WORK_DIR_NAME / "40_operator_workflows/preflight/check_agent_execution_readiness.py"

SOURCE_WORK = Path(__file__).resolve().parents[2]

def run(cmd, cwd):
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

def setup_repo():
    td = Path(tempfile.mkdtemp(prefix="enh_e7_preflight_selftest_"))
    repo = td / "repo"
    target = repo / "docs/wiki/develop_memo/_work" / WORK_DIR_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_WORK, target)

    run(["git", "init", "-q", "-b", "feature/ariadne_mvp_e7"], repo)
    run(["git", "config", "user.email", "selftest@example.invalid"], repo)
    run(["git", "config", "user.name", "ENH-E7 Selftest"], repo)
    run(["git", "remote", "add", "causal-atelier", "https://example.invalid/causal-atelier.git"], repo)
    run(["git", "add", "."], repo)
    run(["git", "commit", "-qm", "fixture"], repo)
    return td, repo, target

def report_path(work, package, trial="01"):
    return (
        work
        / "20_implementation_reports/G01"
        / f"Trial{trial}"
        / "packages"
        / f"ENH-E7_G01_{package}_Trial{trial}_package_execution_status.md"
    )

def write_report(work, package, state="PACKAGE_COMPLETE", trial="01", gate="G01",
                 report_package=None, report_trial=None, head="NOT_RECORDED"):
    p = report_path(work, package, trial)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f"""# ENH-E7 {gate} {package} Package Execution Status

- Enhancement: ENH-E7
- Gate: {gate}
- Trial: {report_trial or trial}
- Package: {report_package or package}
- State: {state}
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: {head}

## Focused verification
- result: PASS

## Remaining / blocker
none
""",
        encoding="utf-8",
    )
    return p

def write_gate_decision(work, gate="G01", trial="01", decision="PASS"):
    p = (
        work
        / "30_test_report"
        / gate
        / f"Trial{trial}"
        / f"ENH-E7_{gate}_Trial{trial}_999_gate_decision.md"
    )
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f"""# ENH-E7 {gate} Trial{trial} Test Item 999 — Gate Decision

- Gate decision: {decision}
- Enhancement: ENH-E7
- Gate: {gate}
- Trial: {trial}
""",
        encoding="utf-8",
    )
    return p

def preflight(repo, package, trial="01", gate="G01"):
    return run(
        [
            sys.executable,
            str(repo / SCRIPT_REL),
            "--repo-root", ".",
            "--gate", gate,
            "--package", package,
            "--trial", trial,
        ],
        repo,
    )

def assert_pass(name, result, contains=None):
    ok = result.returncode == 0 and "Agent Execution Readiness: PASS" in result.stdout
    if contains:
        ok = ok and contains in result.stdout
    if not ok:
        raise AssertionError(f"{name}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

def assert_block(name, result, contains=None):
    ok = result.returncode == 2 and "Agent Execution Readiness: BLOCKED" in result.stdout
    if contains:
        ok = ok and contains in result.stdout
    if not ok:
        raise AssertionError(f"{name}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

def mutate(path, fn):
    text = path.read_text(encoding="utf-8")
    path.write_text(fn(text), encoding="utf-8")

def main():
    cases = []

    # 1. Clean pre-P01 baseline: no dependency evidence exists, P01 still starts.
    td, repo, work = setup_repo()
    try:
        assert_pass("01 P01 no dependencies", preflight(repo, "P01"))
        cases.append("01 PASS: P01 starts from clean pre-execution baseline")
    finally:
        shutil.rmtree(td)

    # 2. P02 cannot start before P01 completion evidence.
    td, repo, work = setup_repo()
    try:
        assert_block("02 P02 missing P01", preflight(repo, "P02"), "completion report missing")
        cases.append("02 PASS: P02 blocks when P01 evidence is missing")
    finally:
        shutil.rmtree(td)

    # 3. P02 starts after P01 complete.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01")
        assert_pass("03 P02 after P01", preflight(repo, "P02"))
        cases.append("03 PASS: P02 starts after P01 complete")
    finally:
        shutil.rmtree(td)

    # 4. P03 still blocks if only P01 is complete.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01")
        assert_block("04 P03 missing P02", preflight(repo, "P03"), "P02: completion report missing")
        cases.append("04 PASS: P03 blocks until both P01/P02 complete")
    finally:
        shutil.rmtree(td)

    # 5. P03 starts after P01+P02 complete.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01")
        write_report(work, "P02")
        assert_pass("05 P03 chain", preflight(repo, "P03"))
        cases.append("05 PASS: P03 starts after P01/P02 complete")
    finally:
        shutil.rmtree(td)

    # 6-8. Fan-out packages start when P01+P03 are complete.
    for idx, package in enumerate(("P04", "P05", "P06"), start=6):
        td, repo, work = setup_repo()
        try:
            write_report(work, "P01")
            write_report(work, "P03")
            assert_pass(f"{idx:02d} {package} fanout", preflight(repo, package))
            cases.append(f"{idx:02d} PASS: {package} starts after P01/P03 complete")
        finally:
            shutil.rmtree(td)

    # 9. P07 blocks if one required dependency is missing.
    td, repo, work = setup_repo()
    try:
        for package in ("P02", "P03", "P05", "P06"):
            write_report(work, package)
        assert_block("09 P07 missing P04", preflight(repo, "P07"), "P04: completion report missing")
        cases.append("09 PASS: P07 blocks when one required package is missing")
    finally:
        shutil.rmtree(td)

    # 10. P07 starts when all required dependencies are complete.
    td, repo, work = setup_repo()
    try:
        for package in ("P02", "P03", "P04", "P05", "P06"):
            write_report(work, package)
        assert_pass("10 P07 complete chain", preflight(repo, "P07"))
        cases.append("10 PASS: P07 starts after all required packages complete")
    finally:
        shutil.rmtree(td)

    # 11. Explicit blocked dependency is a real blocker.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01", state="PACKAGE_BLOCKED")
        assert_block("11 blocked upstream", preflight(repo, "P02"), "dependency state is not complete")
        cases.append("11 PASS: upstream PACKAGE_BLOCKED remains a Hard Fail")
    finally:
        shutil.rmtree(td)

    # 12. Declared package status is diagnostic only.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01")
        p02 = next((work / "10_enhance_instruction/G01").glob("06_G01_P02_*.md"))
        mutate(
            p02,
            lambda t: t.replace(
                "**Package:** P02",
                "**Package:** P02\n**Status at issuance:** DRAFT_NOT_FROZEN",
                1,
            ),
        )
        result = preflight(repo, "P02")
        assert_pass("12 declared status diagnostic", result, "[INFO] DIAG-01 declared Pxx status")
        cases.append("12 PASS: DRAFT_NOT_FROZEN literal does not block real readiness")
    finally:
        shutil.rmtree(td)

    # 13. Package SHA is traceability only; no exact-match lock exists.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01", head="0" * 40)
        assert_pass("13 package SHA diagnostic only", preflight(repo, "P02"))
        cases.append("13 PASS: package HEAD SHA does not act as dependency lock")
    finally:
        shutil.rmtree(td)

    # 14. Remote mismatch is WARN, not BLOCK.
    td, repo, work = setup_repo()
    try:
        run(["git", "remote", "remove", "causal-atelier"], repo)
        result = preflight(repo, "P01")
        assert_pass("14 remote warning", result, "[WARN] PRE-12 remote")
        cases.append("14 PASS: remote alias mismatch is diagnostic")
    finally:
        shutil.rmtree(td)

    # 15. Template-like placeholder is WARN, not BLOCK.
    td, repo, work = setup_repo()
    try:
        example = "{" * 2 + "EXAMPLE_ONLY" + "}" * 2
        (work / "placeholder_example.md").write_text(example + "\n", encoding="utf-8")
        result = preflight(repo, "P01")
        assert_pass("15 placeholder warning", result, "[WARN] PRE-02 template-like placeholders")
        cases.append("15 PASS: explanatory/template placeholder does not block")
    finally:
        shutil.rmtree(td)

    # 16. Wrong evidence identity remains a Hard Fail.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01", report_package="P99")
        assert_block("16 identity mismatch", preflight(repo, "P02"), "report identity mismatch")
        cases.append("16 PASS: dependency evidence identity mismatch blocks")
    finally:
        shutil.rmtree(td)

    # 17. Wrong branch remains a Hard Fail.
    td, repo, work = setup_repo()
    try:
        run(["git", "checkout", "-qb", "wrong-branch"], repo)
        assert_block("17 wrong branch", preflight(repo, "P01"), "[FAIL] PRE-11 branch")
        cases.append("17 PASS: wrong branch blocks")
    finally:
        shutil.rmtree(td)

    # 18. Explicit Architecture draft remains a Hard Fail.
    td, repo, work = setup_repo()
    try:
        arch = work / "40_operator_workflows/architecture_review/02_target_architecture_decision_record.md"
        mutate(arch, lambda t: re.sub(r"\*\*Status:\*\*\s*\S+", "**Status:** DRAFT", t, count=1))
        assert_block("18 architecture draft", preflight(repo, "P01"), "[FAIL] PRE-13 architecture readiness")
        cases.append("18 PASS: explicit architecture DRAFT blocks")
    finally:
        shutil.rmtree(td)

    # 19. Trial "1" is normalized to "01" rather than rejected for formatting.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01", trial="01")
        result = preflight(repo, "P02", trial="1")
        assert_pass("19 trial normalization", result, "normalized=01")
        cases.append("19 PASS: Trial 1 is semantically normalized to Trial01")
    finally:
        shutil.rmtree(td)

    # 20. G02 remains blocked while its Gate contracts explicitly say DRAFT.
    td, repo, work = setup_repo()
    try:
        write_gate_decision(work, gate="G01", trial="01", decision="PASS")
        assert_block(
            "20 G02 explicit draft gate",
            preflight(repo, "P01", gate="G02"),
            "[FAIL] PRE-14 Gate contract readiness",
        )
        cases.append("20 PASS: G02 explicit Gate DRAFT remains a substantive blocker")
    finally:
        shutil.rmtree(td)

    # 21. After Gate freeze, G02 P01 readiness derives from G01 PASS even if
    # its declared package status still says DRAFT_NOT_FROZEN.
    td, repo, work = setup_repo()
    try:
        write_gate_decision(work, gate="G01", trial="01", decision="PASS")
        g02_06 = work / "10_enhance_instruction/G02/06_Ariadne_ENH-E7_G02_implementation_instruction.md"
        g02_07 = work / "10_enhance_instruction/G02/07_Ariadne_ENH-E7_G02_test_instruction.md"
        mutate(g02_06, lambda t: t.replace("**Contract status:** DRAFT_NOT_FROZEN", "**Contract status:** FROZEN", 1))
        mutate(g02_07, lambda t: t.replace("**Verification contract status:** DRAFT_NOT_FROZEN", "**Verification contract status:** FROZEN", 1))
        result = preflight(repo, "P01", gate="G02")
        assert_pass("21 G02 derived readiness", result, "DRAFT_NOT_FROZEN (diagnostic only")
        cases.append("21 PASS: G02 package declared DRAFT does not block after real Gate/dependency readiness")
    finally:
        shutil.rmtree(td)

    # 22. Semantically equivalent complete state is accepted.
    td, repo, work = setup_repo()
    try:
        write_report(work, "P01", state="DONE")
        assert_pass("22 semantic complete state", preflight(repo, "P02"))
        cases.append("22 PASS: semantic complete state DONE is accepted")
    finally:
        shutil.rmtree(td)

    print("ENH-E7 preflight self-test: PASS")
    for case in cases:
        print(case)
    print(f"Total: {len(cases)} cases")

if __name__ == "__main__":
    main()
