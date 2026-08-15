#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re
import subprocess
import sys

from readme_naming import readme_filename_for_directory
from workflow_metadata import (
    DependencySyntaxError,
    ExecutionModeSyntaxError,
    MetadataAmbiguityError,
    RequiredPackagesSyntaxError,
    metadata_field,
    normalize_token,
    normalize_trial,
    parse_dependencies,
    parse_execution_mode,
    parse_gate_dependencies,
    parse_required_packages,
    validate_dependency_ids,
)

PROMPT_BY_MODE = {
    "single": "10_normal_execution_01_single_execution_coding_agent_prompt.md",
    "package": "10_normal_execution_02_work_package_coding_agent_prompt.md",
    "assembly": "20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md",
    "test": "30_independent_verification_01_test_agent_prompt.md",
    "remediation": "40_fail_remediation_01_fail_rework_coding_agent_prompt.md",
    "orchestrator": "50_orchestration_01_gate_orchestrator_prompt.md",
}
RUNTIME_BY_MODE = {
    "single": ("GATE_ID", "TRIAL_NO"),
    "package": ("GATE_ID", "PACKAGE_ID", "TRIAL_NO"),
    "assembly": ("GATE_ID", "TRIAL_NO"),
    "test": ("GATE_ID", "TRIAL_NO"),
    "remediation": ("GATE_ID", "REMEDIATION_PACKAGE_ID", "TRIAL_NO"),
    "orchestrator": ("GATE_ID", "TRIAL_NO"),
}
FIXED = ("PROJECT_NAME", "ENHANCE_ID", "ENHANCE_SHORT_ID", "BRANCH_NAME", "REMOTE_NAME", "WORK_ROOT", "WORK_DIR_NAME")
UNRESOLVED_SEMANTIC_MARKERS = ("KEEP_THIS_SEMANTIC_SENTENCE",)
COMPLETE_STATES = {"PACKAGE_COMPLETE"}


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def fixed_assignments(text):
    out = {}
    for key in FIXED:
        m = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(.+?)\s*$", text)
        if m:
            out[key] = m.group(1).strip()
    return out


def safe_field(text, label, failures, source):
    try:
        return metadata_field(text, label)
    except MetadataAmbiguityError as exc:
        failures.append(("CONTENT_COMPLETENESS", f"{source}: {exc}"))
        return ""


def known_gate_ids(work_root):
    base = work_root / "10_enhance_instruction"
    return {p.name.upper() for p in base.glob("G??") if p.is_dir() and re.fullmatch(r"G\d{2}", p.name, re.I)} if base.is_dir() else set()


def known_package_ids(gate_dir):
    ids = set()
    if gate_dir.is_dir():
        for p in gate_dir.glob("06_*.md"):
            m = re.search(r"(?:^|_)(P\d{2})(?:_|\.)", p.name, re.I)
            if m:
                ids.add(m.group(1).upper())
    return ids


def resolve_gate_contracts(work_root, gate):
    gate_dir = work_root / "10_enhance_instruction" / gate
    if not gate_dir.is_dir():
        return gate_dir, [], []
    g06 = sorted(p for p in gate_dir.glob("06_*.md") if not re.search(r"(?:^|_)P\d{2}(?:_|\.)", p.name, re.I))
    g07 = sorted(gate_dir.glob("07_*.md"))
    return gate_dir, g06, g07


def package_report_candidates(work_root, gate, trial):
    base = work_root / "20_implementation_reports" / gate / f"Trial{trial}" / "packages"
    return sorted(base.glob("*.md")) if base.is_dir() else []


def check_package_dependency(work_root, gate, package, trial, failures):
    matches = []
    for report in package_report_candidates(work_root, gate, trial):
        text = report.read_text(encoding="utf-8")
        rg = safe_field(text, "Gate", failures, str(report))
        rp = safe_field(text, "Package", failures, str(report))
        rt = safe_field(text, "Trial", failures, str(report))
        state = safe_field(text, "State", failures, str(report))
        if normalize_token(rg) == gate and normalize_token(rp) == package and normalize_trial(rt) == trial:
            matches.append((report, normalize_token(state)))
    if len(matches) != 1:
        return False, f"{package}: canonical package report resolver count={len(matches)}"
    report, state = matches[0]
    if state not in COMPLETE_STATES:
        return False, f"{package}: dependency state is {state or 'missing'}, not PACKAGE_COMPLETE"
    return True, f"{package}: complete via {report.relative_to(work_root)}"


def gate_decision_records(work_root, gate, failures):
    base = work_root / "30_test_report" / gate
    records = []
    if not base.is_dir():
        return records
    for trial_dir in base.glob("Trial*"):
        m = re.fullmatch(r"Trial(\d{1,2})", trial_dir.name, re.I)
        if not m:
            continue
        trial_no = int(m.group(1))
        for report in trial_dir.glob("*999_gate_decision.md"):
            text = report.read_text(encoding="utf-8")
            decision = safe_field(text, "Gate decision", failures, str(report))
            report_gate = safe_field(text, "Gate", failures, str(report))
            if report_gate and normalize_token(report_gate) != gate:
                continue
            records.append((trial_no, report, normalize_token(decision)))
    return sorted(records, key=lambda x: (x[0], x[1].name))


def check_gate_pass_dependency(work_root, gate, failures):
    records = gate_decision_records(work_root, gate, failures)
    if not records:
        return False, f"{gate} PASS evidence missing"
    latest_trial = max(x[0] for x in records)
    latest = [x for x in records if x[0] == latest_trial]
    if len(latest) != 1:
        return False, f"{gate}: latest Trial{latest_trial:02d} 999 decision count={len(latest)}"
    _, report, decision = latest[0]
    if decision != "PASS":
        return False, f"{gate}: latest canonical Gate decision is {decision or 'missing'}, not PASS"
    return True, f"{gate} PASS via {report.relative_to(work_root)}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work-root", required=True, type=Path)
    p.add_argument("--mode", required=True, choices=sorted(RUNTIME_BY_MODE))
    p.add_argument("--gate-id")
    p.add_argument("--package-id")
    p.add_argument("--trial-no")
    p.add_argument("--remediation-package-id")
    args = p.parse_args()

    work_root = args.work_root.resolve()
    gate = (args.gate_id or "").upper()
    package = (args.package_id or "").upper()
    trial = normalize_trial(args.trial_no or "")
    prompts = work_root / "40_operator_workflows" / "agent_entry_prompts"
    failures, warns, infos = [], [], []

    if not work_root.is_dir():
        failures.append(("EXECUTION_RESOLVABILITY", f"WORK_ROOT does not exist: {work_root}"))

    if prompts.is_dir():
        prompt_readme = readme_filename_for_directory(work_root, prompts)
        required = set(PROMPT_BY_MODE.values()) | {"00_variable_conventions.md", prompt_readme}
        missing = sorted(name for name in required if not (prompts / name).is_file())
        if missing:
            failures.append(("ARTIFACT_COMPLETENESS", "missing prompt files: " + ", ".join(missing)))
        if (prompts / "README.md").exists():
            failures.append(("ARTIFACT_COMPLETENESS", "nested unqualified README.md is forbidden"))
    else:
        failures.append(("ARTIFACT_COMPLETENESS", f"missing prompt directory: {prompts}"))

    supplied = {"GATE_ID": args.gate_id, "PACKAGE_ID": args.package_id, "TRIAL_NO": args.trial_no, "REMEDIATION_PACKAGE_ID": args.remediation_package_id}
    missing_runtime = [key for key in RUNTIME_BY_MODE[args.mode] if not supplied.get(key)]
    if missing_runtime:
        failures.append(("EXECUTION_RESOLVABILITY", "missing runtime values: " + ", ".join(missing_runtime)))
    if gate and not re.fullmatch(r"G\d{2}", gate):
        failures.append(("EXECUTION_RESOLVABILITY", f"invalid GATE_ID format: {gate}"))
    if package and not re.fullmatch(r"P\d{2}", package):
        failures.append(("EXECUTION_RESOLVABILITY", f"invalid PACKAGE_ID format: {package}"))

    selected = prompts / PROMPT_BY_MODE[args.mode]
    selected_text = selected.read_text(encoding="utf-8") if selected.is_file() else ""
    assignments = fixed_assignments(selected_text)
    for key in FIXED:
        value = assignments.get(key, "")
        if not value:
            failures.append(("CONTENT_COMPLETENESS", f"selected prompt lacks explicit {key}"))
        elif "{{" in value:
            failures.append(("CONTENT_COMPLETENESS", f"selected prompt has unresolved {key}: {value}"))
    for marker in UNRESOLVED_SEMANTIC_MARKERS:
        if marker in selected_text:
            failures.append(("CONTENT_COMPLETENESS", f"selected prompt contains unresolved semantic-body marker: {marker}"))

    gids = known_gate_ids(work_root) if work_root.is_dir() else set()
    if gate and gate not in gids:
        failures.append(("EXECUTION_RESOLVABILITY", f"GATE_ID not derived from repository artifacts: {gate}"))

    execution_mode = None
    required_packages = ()
    if gate and re.fullmatch(r"G\d{2}", gate):
        gate_dir, g06, g07 = resolve_gate_contracts(work_root, gate)
        if not gate_dir.is_dir():
            failures.append(("ARTIFACT_COMPLETENESS", f"Gate directory missing: {gate_dir}"))
        if len(g06) != 1:
            failures.append(("EXECUTION_RESOLVABILITY", f"Gate 06 resolver count={len(g06)}"))
        if len(g07) != 1:
            failures.append(("EXECUTION_RESOLVABILITY", f"Gate 07 resolver count={len(g07)}"))

        if len(g06) == 1:
            six_text = g06[0].read_text(encoding="utf-8")
            six_gate = safe_field(six_text, "Gate", failures, str(g06[0]))
            status = safe_field(six_text, "Contract status", failures, str(g06[0]))
            raw_gate_dep = safe_field(six_text, "Depends on", failures, str(g06[0]))
            raw_mode = safe_field(six_text, "Execution mode", failures, str(g06[0]))
            raw_packages = safe_field(six_text, "Required packages", failures, str(g06[0]))
            if normalize_token(six_gate) != gate:
                failures.append(("CONTENT_COMPLETENESS", f"Gate 06 Gate must be {gate}; got {six_gate or 'missing'}"))
            if normalize_token(status) != "FROZEN":
                failures.append(("CONTENT_COMPLETENESS", f"Gate 06 Contract status must be FROZEN; got {status or 'missing'}"))
            try:
                gate_deps = parse_gate_dependencies(raw_gate_dep)
            except DependencySyntaxError as exc:
                failures.append(("EXECUTION_RESOLVABILITY", f"Gate 06 Depends on: {exc}"))
                gate_deps = ()
            id_errors = validate_dependency_ids(gate_deps, known_gate_ids=gids)
            for err in id_errors:
                failures.append(("EXECUTION_RESOLVABILITY", err))
            if not id_errors:
                for ref in gate_deps:
                    ok, evidence = check_gate_pass_dependency(work_root, ref.identifier, failures)
                    if ok:
                        infos.append(("GATE_DEPENDENCY_EVIDENCE", evidence))
                    else:
                        failures.append(("EXECUTION_RESOLVABILITY", evidence))
            try:
                execution_mode = parse_execution_mode(raw_mode)
            except ExecutionModeSyntaxError as exc:
                failures.append(("EXECUTION_RESOLVABILITY", str(exc)))
            try:
                required_packages = parse_required_packages(raw_packages)
            except RequiredPackagesSyntaxError as exc:
                failures.append(("EXECUTION_RESOLVABILITY", str(exc)))
                required_packages = ()
            if execution_mode == "SINGLE_EXECUTION" and required_packages:
                failures.append(("EXECUTION_RESOLVABILITY", "SINGLE_EXECUTION requires Required packages: NONE"))
            if execution_mode == "WORK_PACKAGE" and not required_packages:
                failures.append(("EXECUTION_RESOLVABILITY", "WORK_PACKAGE requires one or more Required packages"))
            existing_packages = known_package_ids(gate_dir)
            missing_required = sorted(set(required_packages) - existing_packages)
            if missing_required:
                failures.append(("ARTIFACT_COMPLETENESS", "required Pxx files missing: " + ", ".join(missing_required)))

        if len(g07) == 1:
            seven_text = g07[0].read_text(encoding="utf-8")
            status = safe_field(seven_text, "Verification contract status", failures, str(g07[0]))
            if normalize_token(status) != "FROZEN":
                failures.append(("CONTENT_COMPLETENESS", f"Gate 07 Verification contract status must be FROZEN; got {status or 'missing'}"))

    if args.mode == "single" and execution_mode and execution_mode != "SINGLE_EXECUTION":
        failures.append(("EXECUTION_RESOLVABILITY", f"requested single mode conflicts with Gate 06 Execution mode={execution_mode}"))
    if args.mode in {"package", "assembly"} and execution_mode and execution_mode != "WORK_PACKAGE":
        failures.append(("EXECUTION_RESOLVABILITY", f"requested {args.mode} mode requires Gate 06 Execution mode=WORK_PACKAGE; got {execution_mode}"))

    if args.mode == "package" and gate and package and trial:
        gate_dir = work_root / "10_enhance_instruction" / gate
        matches = sorted(gate_dir.glob(f"06_{gate}_{package}_*.md")) if gate_dir.is_dir() else []
        if package not in required_packages:
            failures.append(("EXECUTION_RESOLVABILITY", f"PACKAGE_ID {package} is not in Gate 06 Required packages={list(required_packages)}"))
        if len(matches) != 1:
            failures.append(("EXECUTION_RESOLVABILITY", f"assigned Pxx resolver count={len(matches)}"))
        if len(matches) == 1:
            pxx_text = matches[0].read_text(encoding="utf-8")
            self_contained = safe_field(pxx_text, "Self-containment", failures, str(matches[0]))
            info_isolation = safe_field(pxx_text, "Information isolation", failures, str(matches[0]))
            if normalize_token(self_contained) != "MUST":
                failures.append(("INFORMATION_ISOLATION", f"Self-containment must be MUST; got {self_contained or 'missing'}"))
            if normalize_token(info_isolation) != "MUST":
                failures.append(("INFORMATION_ISOLATION", f"Information isolation must be MUST; got {info_isolation or 'missing'}"))
            raw_dep = safe_field(pxx_text, "Depends on", failures, str(matches[0]))
            if not raw_dep:
                failures.append(("EXECUTION_RESOLVABILITY", "Pxx Depends on declaration missing or empty"))
            else:
                try:
                    refs = parse_dependencies(raw_dep)
                except DependencySyntaxError as exc:
                    failures.append(("EXECUTION_RESOLVABILITY", str(exc)))
                    refs = ()
                id_errors = validate_dependency_ids(refs, known_package_ids=required_packages, known_gate_ids=gids)
                for err in id_errors:
                    failures.append(("EXECUTION_RESOLVABILITY", err))
                if not id_errors:
                    for ref in refs:
                        if ref.kind == "package":
                            ok, evidence = check_package_dependency(work_root, gate, ref.identifier, trial, failures)
                        else:
                            ok, evidence = check_gate_pass_dependency(work_root, ref.identifier, failures)
                        if ok:
                            infos.append(("DEPENDENCY_EVIDENCE", evidence))
                        else:
                            failures.append(("EXECUTION_RESOLVABILITY", evidence))
            issuance = safe_field(pxx_text, "Status at issuance", failures, str(matches[0]))
            infos.append(("DECLARED_PXX_STATUS", f"{issuance or 'not declared'} (diagnostic only)"))

        if "assigned Pxxのみ" not in selected_text and "assigned Pxx only" not in selected_text:
            failures.append(("INFORMATION_ISOLATION", "package prompt does not state assigned-Pxx-only authority"))
        if "仕様補完目的で以下を読んではならない" not in selected_text:
            failures.append(("INFORMATION_ISOLATION", "package prompt lacks explicit forbidden-read guardrail"))

    branch = assignments.get("BRANCH_NAME", "")
    if branch and "{{" not in branch:
        rc, current, err = run(["git", "branch", "--show-current"], work_root)
        if rc == 0:
            if current != branch:
                failures.append(("EXECUTION_RESOLVABILITY", f"branch mismatch: expected={branch}, current={current}"))
        else:
            warns.append(("REPOSITORY_BRANCH", f"git branch check unavailable: {err or 'unknown error'}"))

    print("AGENT EXECUTION READINESS")
    axes = ["ARTIFACT_COMPLETENESS", "CONTENT_COMPLETENESS", "EXECUTION_RESOLVABILITY", "INFORMATION_ISOLATION"]
    for axis in axes:
        msgs = [m for c, m in failures if c == axis]
        print(f"{axis}: {'FAIL' if msgs else 'PASS'}")
        for msg in msgs:
            print(f"  - {msg}")
    for name, msg in warns:
        print(f"[WARN] {name}: {msg}")
    for name, msg in infos:
        print(f"[INFO] {name}: {msg}")

    if failures:
        print("OVERALL: BLOCKED")
        return 2
    print("OVERALL: READY_FOR_AGENT_EXECUTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
