#!/usr/bin/env python3
from pathlib import Path
import argparse, re, subprocess, sys

WORK_DIR_NAME = "20260813_ENH-E7_project_analysis_workspace_separation"
EXPECTED_BRANCH = "feature/ariadne_mvp_e7"
UNRESOLVED_SENTINEL = "REQUIRES_LOCAL_VERIFICATION"

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

ap = argparse.ArgumentParser()
ap.add_argument("--repo-root", default=".")
ap.add_argument("--gate", required=True)
ap.add_argument("--package", required=True)
ap.add_argument("--trial", required=True)
args = ap.parse_args()

repo = Path(args.repo_root).resolve()
work = repo / "docs/wiki/develop_memo/_work" / WORK_DIR_NAME
checks = []

def add(name, ok, evidence):
    checks.append((name, bool(ok), evidence))

add("PRE-01 prompts", (work/"40_operator_workflows/agent_entry_prompts").is_dir(),
    str(work/"40_operator_workflows/agent_entry_prompts"))

# Double-curly placeholders are forbidden in instantiated artifacts.
double_curly = []
if work.exists():
    for p in work.rglob("*"):
        if not p.is_file() or p.name == "MANIFEST.json":
            continue
        rel = p.relative_to(work)
        # Provenance is copied source evidence and may legitimately contain
        # illustrative template placeholders. It is never an execution contract.
        if rel.parts[:2] == ("00_enhance_background", "provenance"):
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if re.search(r"\x7b\x7b[^\n]+?\x7d\x7d", t):
            double_curly.append(str(rel))
add("PRE-02 fixed placeholders", len(double_curly)==0,
    "none" if not double_curly else ", ".join(double_curly[:10]))

add("PRE-03 WORK_ROOT exists", work.is_dir(), str(work))
add("PRE-04 root identity", work.name == WORK_DIR_NAME and (work/"README.md").exists(), work.name)

pattern = work / "10_enhance_instruction" / args.gate
matches = []
if pattern.is_dir():
    matches = list(pattern.glob(f"06_{args.gate}_{args.package}_*.md"))
add("PRE-05 exactly one Pxx", len(matches)==1, ", ".join(str(x.name) for x in matches) or "none")

coding_prompt = work/"40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md"
prompt_text = coding_prompt.read_text(encoding="utf-8") if coding_prompt.exists() else ""
# Prompt may mention forbidden docs only as explicit prohibitions. Disallow directive forms that tell the Agent to open them.
bad_directives = re.findall(r"(?im)^\s*(read|open|load|参照|読む)\b.*\b(07|P00|other Pxx|Gate 06)\b", prompt_text)
add("PRE-06 prompt isolation", not bad_directives, "no forbidden positive read directive" if not bad_directives else str(bad_directives))

if len(matches)==1:
    pxx_text = matches[0].read_text(encoding="utf-8")
    # self-contained marker and explicit isolation rule are required.
    pxx_ok = ("Self-containment:** MUST" in pxx_text and
              "must not read Gate 06" in pxx_text.lower().replace("**","").replace("`",""))
    # fall back to explicit phrase as generated.
    if not pxx_ok:
        pxx_ok = ("Self-containment:** MUST" in pxx_text and
                  "must not read Gate 06 / Gate 07 / P00 / other Pxx" in pxx_text)
    add("PRE-07 Pxx self-contained/isolation", pxx_ok, matches[0].name)
else:
    add("PRE-07 Pxx self-contained/isolation", False, "Pxx unresolved")

add("PRE-08 GATE_ID", args.gate in ("G01","G02"), args.gate)
add("PRE-09 PACKAGE_ID", bool(re.fullmatch(r"P\d{2}", args.package)), args.package)
add("PRE-10 TRIAL_NO", bool(re.fullmatch(r"\d{2}", args.trial)), args.trial)

rc, branch, err = run(["git","branch","--show-current"], repo)
add("PRE-11 branch", rc==0 and branch==EXPECTED_BRANCH, branch or err)

rc, remotes, err = run(["git","remote"], repo)
remote_list = remotes.splitlines() if rc==0 else []
vars_path = work/"40_operator_workflows/agent_entry_prompts/00_variable_conventions.md"
vars_text = vars_path.read_text(encoding="utf-8") if vars_path.exists() else ""
m = re.search(r"^REMOTE_NAME=(.+)$", vars_text, re.M)
configured_remote = m.group(1).strip() if m else ""
remote_ok = configured_remote and configured_remote != UNRESOLVED_SENTINEL and configured_remote in remote_list
add("PRE-12 remote", remote_ok, f"configured={configured_remote} local={remote_list}")

arch = work/"40_operator_workflows/architecture_review/02_target_architecture_decision_record.md"
arch_text = arch.read_text(encoding="utf-8") if arch.exists() else ""
add("PRE-13 architecture approved", "Status:** APPROVED" in arch_text, "architecture record status")

gate06 = work/"10_enhance_instruction"/args.gate/f"06_Ariadne_ENH-E7_{args.gate}_implementation_instruction.md"
gate07 = work/"10_enhance_instruction"/args.gate/f"07_Ariadne_ENH-E7_{args.gate}_test_instruction.md"
g06 = gate06.read_text(encoding="utf-8") if gate06.exists() else ""
g07 = gate07.read_text(encoding="utf-8") if gate07.exists() else ""
add("PRE-14 Gate 06/07 frozen",
    ("Contract status:** FROZEN" in g06 and "Verification contract status:** FROZEN" in g07),
    f"06={'FROZEN' if 'Contract status:** FROZEN' in g06 else 'not frozen'}, 07={'FROZEN' if 'Verification contract status:** FROZEN' in g07 else 'not frozen'}")

if len(matches)==1:
    ptxt = matches[0].read_text(encoding="utf-8")
    add("PRE-15 Pxx executable status", "Status at issuance:** READY_TO_EXECUTE" in ptxt, matches[0].name)
else:
    add("PRE-15 Pxx executable status", False, "Pxx unresolved")

all_ok = all(ok for _,ok,_ in checks)
print(f"Agent Execution Readiness: {'PASS' if all_ok else 'BLOCKED'}")
for name,ok,evidence in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {evidence}")

sys.exit(0 if all_ok else 2)
