#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import subprocess
import sys

WORK_DIR_NAME = "20260813_ENH-E7_project_analysis_workspace_separation"
EXPECTED_BRANCH = "feature/ariadne_mvp_e7"
UNRESOLVED_SENTINEL = "REQUIRES_LOCAL_VERIFICATION"

COMPLETE_STATES = {"PACKAGE_COMPLETE", "COMPLETE", "DONE", "PASS", "PASSED"}
BLOCKING_STATUS_TOKENS = {
    "DRAFT",
    "DRAFT_NOT_FROZEN",
    "NOT_FROZEN",
    "BLOCKED",
    "REJECTED",
    "NOT_APPROVED",
    "UNAPPROVED",
}

def run(cmd, cwd):
    p = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def normalize_token(value):
    value = value.strip().strip("`").upper()
    value = re.sub(r"[\s\-]+", "_", value)
    return value

def field(text, label):
    m = re.search(
        rf"(?im)^\s*-\s*{re.escape(label)}\s*:\s*(.+?)\s*$",
        text,
    )
    return m.group(1).strip() if m else ""

def bold_field(text, label):
    m = re.search(
        rf"(?im)^\s*\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$",
        text,
    )
    return m.group(1).strip() if m else ""

def has_explicit_blocking_status(value):
    if not value:
        return False
    token = normalize_token(value)
    if token in BLOCKING_STATUS_TOKENS:
        return True
    return any(part in token for part in ("DRAFT", "NOT_FROZEN", "BLOCKED", "REJECTED"))

def normalize_trial(value):
    if not re.fullmatch(r"\d{1,2}", value):
        return None
    return value.zfill(2)

def parse_dependencies(pxx_text):
    raw = bold_field(pxx_text, "Depends on")
    if not raw:
        return None, "missing **Depends on:** declaration"

    raw = raw.strip()
    if normalize_token(raw) in {"NONE", "NO_DEPENDENCY", "NO_DEPENDENCIES"}:
        return [], raw

    dependencies = []
    for part in [x.strip() for x in raw.split(",") if x.strip()]:
        gate_pass = re.fullmatch(r"(G\d{2})\s+PASS", part, re.I)
        if gate_pass:
            dependencies.append(("gate_pass", gate_pass.group(1).upper()))
            continue
        package = re.fullmatch(r"P\d{2}", part, re.I)
        if package:
            dependencies.append(("package", part.upper()))
            continue
        return None, f"unrecognized dependency expression: {part}"
    return dependencies, raw

def check_package_dependency(work, gate, package, trial):
    report = (
        work
        / "20_implementation_reports"
        / gate
        / f"Trial{trial}"
        / "packages"
        / f"ENH-E7_{gate}_{package}_Trial{trial}_package_execution_status.md"
    )
    if not report.is_file():
        return False, f"{package}: completion report missing: {report.relative_to(work)}"

    text = report.read_text(encoding="utf-8")
    report_gate = field(text, "Gate")
    report_package = field(text, "Package")
    report_trial = field(text, "Trial")
    state = field(text, "State")

    identity_ok = (
        normalize_token(report_gate) == gate
        and normalize_token(report_package) == package
        and normalize_trial(report_trial) == trial
    )
    if not identity_ok:
        return False, (
            f"{package}: report identity mismatch "
            f"(Gate={report_gate or 'missing'}, "
            f"Package={report_package or 'missing'}, "
            f"Trial={report_trial or 'missing'})"
        )

    if normalize_token(state) not in COMPLETE_STATES:
        return False, f"{package}: dependency state is not complete: {state or 'missing'}"

    return True, f"{package}: complete via {report.relative_to(work)}"

def check_gate_pass_dependency(work, gate):
    base = work / "30_test_report" / gate
    candidates = sorted(
        base.glob(f"Trial*/ENH-E7_{gate}_Trial*_999_gate_decision.md")
    ) if base.is_dir() else []

    pass_reports = []
    for report in candidates:
        text = report.read_text(encoding="utf-8")
        decision = field(text, "Gate decision")
        report_gate = field(text, "Gate")
        if normalize_token(decision) not in {"PASS", "PASSED", "APPROVED"}:
            continue
        if report_gate and normalize_token(report_gate) != gate:
            continue
        pass_reports.append(report)

    if not pass_reports:
        return False, f"{gate} PASS evidence missing"
    rels = ", ".join(str(p.relative_to(work)) for p in pass_reports[-3:])
    return True, f"{gate} PASS via {rels}"

ap = argparse.ArgumentParser()
ap.add_argument("--repo-root", default=".")
ap.add_argument("--gate", required=True)
ap.add_argument("--package", required=True)
ap.add_argument("--trial", required=True)
args = ap.parse_args()

repo = Path(args.repo_root).resolve()
work = repo / "docs/wiki/develop_memo/_work" / WORK_DIR_NAME
checks = []

def add_blocking(name, ok, evidence):
    checks.append(("PASS" if ok else "FAIL", name, evidence))

def add_diagnostic(name, ok, evidence):
    checks.append(("PASS" if ok else "WARN", name, evidence))

def add_info(name, evidence):
    checks.append(("INFO", name, evidence))

trial = normalize_trial(args.trial)
gate = args.gate.upper()
package = args.package.upper()

add_blocking(
    "PRE-01 prompts",
    (work / "40_operator_workflows/agent_entry_prompts").is_dir(),
    str(work / "40_operator_workflows/agent_entry_prompts"),
)

# Template-like placeholders are diagnostic unless they are actual runtime inputs.
# Runtime identity is validated directly below, so prose/examples do not block execution.
placeholder_hits = []
if work.exists():
    for p in work.rglob("*"):
        if not p.is_file() or p.name == "MANIFEST.json":
            continue
        rel = p.relative_to(work)
        if rel.parts[:2] == ("00_enhance_background", "provenance"):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if re.search(r"\{\{[^\n]+?\}\}", text):
            placeholder_hits.append(str(rel))
add_diagnostic(
    "PRE-02 template-like placeholders",
    len(placeholder_hits) == 0,
    "none" if not placeholder_hits else ", ".join(placeholder_hits[:10]),
)

add_blocking("PRE-03 WORK_ROOT exists", work.is_dir(), str(work))
add_blocking(
    "PRE-04 root identity",
    work.name == WORK_DIR_NAME and (work / "README.md").exists(),
    work.name,
)

pattern = work / "10_enhance_instruction" / gate
matches = []
if pattern.is_dir() and re.fullmatch(r"P\d{2}", package):
    matches = list(pattern.glob(f"06_{gate}_{package}_*.md"))
add_blocking(
    "PRE-05 exactly one Pxx",
    len(matches) == 1,
    ", ".join(str(x.name) for x in matches) or "none",
)

coding_prompt = (
    work
    / "40_operator_workflows/agent_entry_prompts"
    / "10_normal_execution_02_work_package_coding_agent_prompt.md"
)
prompt_text = coding_prompt.read_text(encoding="utf-8") if coding_prompt.exists() else ""
bad_directives = re.findall(
    r"(?im)^\s*(read|open|load|参照|読む)\b.*\b(07|P00|other Pxx|Gate 06)\b",
    prompt_text,
)
add_blocking(
    "PRE-06 prompt isolation",
    coding_prompt.is_file() and not bad_directives,
    "no forbidden positive read directive" if coding_prompt.is_file() and not bad_directives
    else ("coding prompt missing" if not coding_prompt.is_file() else str(bad_directives)),
)

pxx_text = ""
if len(matches) == 1:
    pxx_text = matches[0].read_text(encoding="utf-8")
    self_contained = "**Self-containment:** MUST" in pxx_text
    information_isolation = "**Information isolation:** MUST" in pxx_text
    add_diagnostic(
        "PRE-07 Pxx contract metadata",
        self_contained and information_isolation,
        (
            f"{matches[0].name}; "
            f"self_containment={'present' if self_contained else 'missing'}; "
            f"information_isolation={'present' if information_isolation else 'missing'}"
        ),
    )
else:
    add_diagnostic("PRE-07 Pxx contract metadata", False, "Pxx unresolved")

add_blocking(
    "PRE-08 GATE_ID",
    bool(re.fullmatch(r"G\d{2}", gate)),
    gate,
) ## add_blocking("PRE-08 GATE_ID", gate in ("G01", "G02"), gate) からの変更
add_blocking("PRE-09 PACKAGE_ID", bool(re.fullmatch(r"P\d{2}", package)), package)
add_blocking(
    "PRE-10 TRIAL_NO",
    trial is not None,
    f"input={args.trial}; normalized={trial or 'invalid'}",
)

rc, branch, err = run(["git", "branch", "--show-current"], repo)
add_blocking(
    "PRE-11 branch",
    rc == 0 and branch == EXPECTED_BRANCH,
    branch or err,
)

rc, remotes, err = run(["git", "remote"], repo)
remote_list = remotes.splitlines() if rc == 0 else []
vars_path = work / "40_operator_workflows/agent_entry_prompts/00_variable_conventions.md"
vars_text = vars_path.read_text(encoding="utf-8") if vars_path.exists() else ""
m = re.search(r"^REMOTE_NAME=(.+)$", vars_text, re.M)
configured_remote = m.group(1).strip() if m else ""
remote_ok = (
    configured_remote
    and configured_remote != UNRESOLVED_SENTINEL
    and configured_remote in remote_list
)
add_diagnostic(
    "PRE-12 remote",
    remote_ok,
    f"configured={configured_remote or 'missing'} local={remote_list}",
)

arch = work / "40_operator_workflows/architecture_review/02_target_architecture_decision_record.md"
arch_text = arch.read_text(encoding="utf-8") if arch.exists() else ""
arch_status = bold_field(arch_text, "Status")
arch_ok = arch.is_file() and not has_explicit_blocking_status(arch_status)
add_blocking(
    "PRE-13 architecture readiness",
    arch_ok,
    f"status={arch_status or 'unspecified'}",
)

gate06 = work / "10_enhance_instruction" / gate / f"06_Ariadne_ENH-E7_{gate}_implementation_instruction.md"
gate07 = work / "10_enhance_instruction" / gate / f"07_Ariadne_ENH-E7_{gate}_test_instruction.md"
g06 = gate06.read_text(encoding="utf-8") if gate06.exists() else ""
g07 = gate07.read_text(encoding="utf-8") if gate07.exists() else ""
g06_status = bold_field(g06, "Contract status")
g07_status = bold_field(g07, "Verification contract status")
gate_contracts_ok = (
    gate06.is_file()
    and gate07.is_file()
    and not has_explicit_blocking_status(g06_status)
    and not has_explicit_blocking_status(g07_status)
)
add_blocking(
    "PRE-14 Gate contract readiness",
    gate_contracts_ok,
    f"06={g06_status or 'unspecified'}, 07={g07_status or 'unspecified'}",
)

# Execution eligibility is derived from real dependencies, not from a package
# status literal such as READY_TO_EXECUTE.
dependency_ok = False
dependency_evidence = "Pxx unresolved"
declared_status = ""
if len(matches) == 1 and trial is not None:
    declared_status = bold_field(pxx_text, "Status at issuance")
    dependencies, raw_dependencies = parse_dependencies(pxx_text)
    if dependencies is None:
        dependency_ok = False
        dependency_evidence = raw_dependencies
    else:
        results = []
        dependency_ok = True
        for kind, dep in dependencies:
            if kind == "package":
                ok, evidence = check_package_dependency(work, gate, dep, trial)
            else:
                ok, evidence = check_gate_pass_dependency(work, dep)
            results.append(evidence)
            dependency_ok = dependency_ok and ok
        dependency_evidence = (
            "NONE"
            if not dependencies
            else "; ".join(results)
        )
add_blocking(
    "PRE-15 dependency-derived execution eligibility",
    dependency_ok,
    dependency_evidence,
)
add_info(
    "DIAG-01 declared Pxx status",
    f"{declared_status or 'not declared'} (diagnostic only; not execution control)",
)

report_path = (
    f"20_implementation_reports/{gate}/Trial{trial}/packages/"
    f"ENH-E7_{gate}_{package}_Trial{trial}_package_execution_status.md"
    if trial is not None
    else "unresolved"
)
reporting_prompt_ok = (
    coding_prompt.is_file()
    and "_package_execution_status.md" in prompt_text
    and "20_implementation_reports/" in prompt_text
)
add_diagnostic(
    "PRE-16 package reporting resolvability",
    reporting_prompt_ok,
    report_path,
)

blocking = [x for x in checks if x[0] == "FAIL"]
print(f"Agent Execution Readiness: {'BLOCKED' if blocking else 'PASS'}")
for result, name, evidence in checks:
    print(f"[{result}] {name}: {evidence}")

sys.exit(2 if blocking else 0)
