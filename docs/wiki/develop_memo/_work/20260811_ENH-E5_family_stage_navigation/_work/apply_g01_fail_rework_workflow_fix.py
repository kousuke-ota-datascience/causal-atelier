#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from pathlib import Path

BASE = Path("docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation")

FAIL_REWORK = BASE / "40_operator_workflows/agent_entry_prompts/fail_rework_coding_agent_prompt.md"
ASSEMBLY = BASE / "40_operator_workflows/agent_entry_prompts/work_package_candidate_assembly_agent_prompt.md"
TRIAL04_08 = BASE / "10_enhance_instruction/G01/08_Ariadne_ENH-E5_G01_Trial04_remediation_instruction.md"

TRIAL03_COMPLETION = BASE / "20_implementation_reports/G01/Trial03/E5-G01_03__implementation_completion.md"
TRIAL03_GATE = BASE / "30_test_report/G01/Trial03/E5-G01_03__999_gate_decision.md"
TRIAL03_OPERATION = BASE / "30_test_report/G01/Trial03/E5-G01_03__003_operation_availability.md"

PREVIOUS_FAILED_CANDIDATE = "27e87faecd2b5dac0da6a688201931456c1a6077"

FAIL_REWORK_CONTENT = r"""# FAIL Rework Coding Agent Prompt — ENH-E5

この文書は formal FAIL 後の rework 専用 entry prompt である。

実行時に Operator から以下を受け取る。

```text
GATE_ID=<Gate ID>
TRIAL_NO=<two-digit Trial number>
```

## 1. Current Trial Remediation Contract

current Trial の normative remediation contract は、必ず以下の exact path で解決する。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/<GATE_ID>/
08_Ariadne_ENH-E5_<GATE_ID>_Trial<TRIAL_NO>_remediation_instruction.md
```

この exact file が存在しない場合:

```text
BLOCKED_REMEDIATION_CONTRACT_MISSING
```

旧 Trial の 08、別名の 08、original 06/Pxx/07 を代用してはならない。

## 2. Normative Source Isolation

freeze 済み current Trial 08 だけを normative source とする。
repository は implementation substrate として調査してよい。

original 06/Pxx/07、旧 Trial report、ADR、他 Gate、過去 Enhancement、external Web を仕様補完に使わない。

required correction が current 08 だけで一意に決まらない場合:

```text
BLOCKED_CONTRACT_AMBIGUITY
```

## 3. SINGLE_EXECUTION Rework Rule

08 が:

```text
Execution mode: SINGLE_EXECUTION
```

を宣言している場合、original Work Package chain を再実行してはならない。

禁止:

- current Trial P01/P02/P03 の再実行
- old Package checkpoint SHA の再利用
- previous failed candidate の再提出
- normal Work Package Candidate Assembly を rework implementation の代替として使用すること

## 4. Implementation and Verification

08 の required correction と protected behavior を実装し、mandatory Coding-side verification をすべて実行する。

禁止:

- failing test の削除
- assertion の弱体化
- skip / xfail
- original contract の改変
- literal input だけを hard-code して拒否する workaround

## 5. Semantic Implementation Checkpoint

semantic change を commit し、exact SHA を implementation checkpoint として固定する。

08 に `PREVIOUS_FAILED_CANDIDATE_SHA` が定義されている場合:

```bash
git diff --name-only   <PREVIOUS_FAILED_CANDIDATE_SHA>..<IMPLEMENTATION_CHECKPOINT_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

を必ず実行する。

08 が要求する semantic remediation が diff に存在しない場合:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

previous failed candidate と同一 SHA を採用してはならない。

## 6. Fixed Trial Candidate

required verification が PASS し required semantic remediation diff が存在する場合のみ:

```text
FIXED_TRIAL_CANDIDATE_SHA=<IMPLEMENTATION_CHECKPOINT_SHA>
```

として freeze する。

formal FAIL / SINGLE_EXECUTION Trial では FAIL Rework Coding Agent 自身が candidate freeze を行う。

## 7. Canonical Implementation Completion Report

以下の exact path に生成する。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
E5-<GATE_ID>_<TRIAL_NO>__implementation_completion.md
```

最低限以下を記録する。

```text
GATE_ID
TRIAL_NO
Execution status
PREVIOUS_FAILED_CANDIDATE_SHA
FIXED_TRIAL_CANDIDATE_SHA
changed production files
changed automated test files
executed verification
Blocker / remaining work
```

`READY_FOR_TEST` の場合:

- fixed candidate != previous failed candidate
- required semantic diff != empty
- required verification = PASS
- blocker = NONE

を満たす。

## 8. Evidence Commit / Push

Completion Report を evidence-only commit として commit / push する。

Completion Report commit 後 `HEAD != FIXED_TRIAL_CANDIDATE_SHA` は許容するが、candidate から evidence HEAD まで semantic implementation change がないことを確認する。

## 9. Final Status

成功時:

```text
## READY_FOR_TEST

- GATE_ID: <GATE_ID>
- TRIAL_NO: <TRIAL_NO>
- PREVIOUS_FAILED_CANDIDATE_SHA: <SHA>
- FIXED_TRIAL_CANDIDATE_SHA: <new SHA>
- COMPLETION_REPORT: <canonical exact path>
- EVIDENCE_COMMIT_SHA: <SHA>
- Working tree: clean
- Push: completed
```

Gate PASS / FAIL、promotion 可否は判定しない。
"""

ASSEMBLY_GUARD = r"""
---

## 16. Formal FAIL Remediation Trial Guard

この節は formal FAIL 後の remediation Trial において、通常 Work Package assembly 規則より優先する。

### 16.1 Remediation Trial Detection

current Trial に以下の exact remediation contract が存在し:

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/{{GATE_ID}}/
08_Ariadne_ENH-E5_{{GATE_ID}}_Trial{{TRIAL_NO}}_remediation_instruction.md
```

その 08 が:

```text
Execution mode: SINGLE_EXECUTION
```

を宣言している場合、current Trial は `FORMAL_FAIL_REMEDIATION` mode とする。

### 16.2 Normal Work Package Assembly Prohibition

この mode では:

- original P01/P02/P03 report を current Trial candidate authority として要求しない
- old Package checkpoint SHA を candidate に再利用しない
- Sections 6–9 の通常 Work Package candidate assembly を適用しない
- previous failed candidate と同一 SHA を `READY_FOR_TEST` として提出しない

FAIL Rework Coding Agent が current Trial canonical Completion Report を生成するのが正規経路である。

### 16.3 Missing Rework Handoff

canonical Completion Report が存在しない場合、old Package chain から Completion Report を合成してはならない。

```text
BLOCKED_REMEDIATION_HANDOFF_INCOMPLETE
```

で停止し、FAIL Rework Coding Agent の実行を要求する。

### 16.4 Candidate Identity Guard

08 の `PREVIOUS_FAILED_CANDIDATE_SHA` と current Completion Report の `FIXED_TRIAL_CANDIDATE_SHA` を比較する。

必須:

```text
FIXED_TRIAL_CANDIDATE_SHA != PREVIOUS_FAILED_CANDIDATE_SHA
```

さらに:

```bash
git diff --name-only   <PREVIOUS_FAILED_CANDIDATE_SHA>..<FIXED_TRIAL_CANDIDATE_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

を確認し、08 が要求する semantic remediation が candidate に含まれることを確認する。

同一 candidate または required remediation diff 不在なら:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

### 16.5 Candidate Assembly Role

この mode で Candidate Assembly Agent が呼ばれた場合は audit-only とする。

禁止:

- production/test の変更
- old package checkpoints から candidate を再構成
- old package checkpoints から Completion Report を生成
- candidate SHA の差し替え
"""

TRIAL04_08_CONTENT = r"""# Ariadne ENH-E5 G01 Trial04 Remediation Instruction

- Contract status: `APPROVED / FROZEN`
- GATE_ID: `G01`
- TRIAL_NO: `04`
- PREVIOUS_FAILED_CANDIDATE_SHA: `27e87faecd2b5dac0da6a688201931456c1a6077`
- Remediation mode: `CONSOLIDATED`
- Execution mode: `SINGLE_EXECUTION`

## 1. Failure classification

Trial03 formal FAIL is an implementation defect, not a Gate contract defect.

Original G01 semantic claim and Acceptance Criteria remain unchanged.

Trial03 did not contain the required remediation implementation. Trial04 MUST create a new semantic implementation candidate.

## 2. Required correction

Current Operation Availability route handling accepts:

```text
/projects/p1/analysis/causal/unknown-stage
```

and returns:

```text
RESOURCE_REQUIRED
```

This is incorrect.

Unknown or malformed canonical routes MUST fail before resource / operation projection with:

```text
OperationAvailabilityError
code = INVALID_NAVIGATION_ROUTE
status = 422
```

## 3. Canonical navigation authority

Canonical Family / Stage membership MUST use:

```text
src/ariadne/product/application/navigation_catalog.py
```

Do not duplicate the full Family/Stage catalog inside `ProductClosureService`.

A structural regex may parse route shape, but regex acceptance alone MUST NOT establish canonical route validity.

## 4. Required validation

For:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

validate before resource/authorization/projection:

1. canonical route shape
2. route project ID == endpoint project ID
3. canonical Family exists
4. Stage belongs to that Family

For resource deep routes, also validate route resource type is one of:

```text
analysis-specification
execution
result
graph-version
```

Required ordering:

```text
unknown/malformed route
    -> INVALID_NAVIGATION_ROUTE

valid canonical route + missing concrete resource
    -> existing RESOURCE_REQUIRED behavior where applicable
```

## 5. Required backend regression coverage

Add automated backend regression coverage for:

- valid canonical Family/Stage route
- unknown Stage -> `INVALID_NAVIGATION_ROUTE`
- unknown Family -> `INVALID_NAVIGATION_ROUTE`
- malformed route -> `INVALID_NAVIGATION_ROUTE`
- unknown route resource type -> `INVALID_NAVIGATION_ROUTE`
- endpoint project / route project mismatch -> `INVALID_NAVIGATION_ROUTE`

At least one test MUST directly call `ProductClosureService.operation_availability(...)` and assert:

```text
error.code == "INVALID_NAVIGATION_ROUTE"
error.status == 422
```

Frontend-only parser tests are insufficient.

## 6. Protected behavior

Preserve unrelated G01 semantics, including:

- `RUN / EDIT / EXPORT`
- query resource-pair semantics
- authorization behavior
- lifecycle/domain reason codes
- persistence/schema/migration state
- navigation UI behavior
- predictive regression behavior

Do not weaken/delete/skip/xfail existing tests.

## 7. Expected change surfaces

Expected minimal surfaces:

```text
src/ariadne/product/application/product_closure_service.py
tests/product/
```

## 8. Mandatory verification

Run compileall, affected G00/G01/predictive tests including the new backend Operation Availability regression, and:

```bash
git diff --check
```

All required checks MUST pass.

## 9. New candidate invariant

Trial04 candidate MUST NOT equal:

```text
27e87faecd2b5dac0da6a688201931456c1a6077
```

Before `READY_FOR_TEST`:

```bash
git diff --name-only   27e87faecd2b5dac0da6a688201931456c1a6077..<FIXED_TRIAL_CANDIDATE_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

The diff MUST include:

- production source change under `src/`
- automated regression change under `tests/`

Otherwise:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

## 10. Execution / handoff

Use only:

```text
fail_rework_coding_agent_prompt.md
GATE_ID=G01
TRIAL_NO=04
```

Do NOT run Trial04 P01/P02/P03 Work Package agents.

The FAIL Rework Coding Agent owns:

```text
implementation correction
-> regression tests
-> implementation checkpoint
-> FIXED_TRIAL_CANDIDATE_SHA
-> canonical Completion Report
-> evidence commit/push
-> READY_FOR_TEST
```

Canonical Completion Report:

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/G01/Trial04/
E5-G01_04__implementation_completion.md
```

Trial02/Trial03 evidence remains immutable.
"""

def run_git(root: Path, *args: str) -> str:
    cp = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{cp.stderr}")
    return cp.stdout

def read_required(root: Path, rel: Path) -> str:
    p = root / rel
    if not p.is_file():
        raise RuntimeError(f"missing required file: {rel}")
    return p.read_text(encoding="utf-8")

def ensure_target_files_clean(root: Path) -> None:
    for rel in (FAIL_REWORK, ASSEMBLY, TRIAL04_08):
        status = run_git(root, "status", "--porcelain", "--", str(rel))
        if status.strip():
            raise RuntimeError(f"target has uncommitted changes: {rel}\n{status}")

def verify_trial03_evidence(root: Path) -> None:
    completion = read_required(root, TRIAL03_COMPLETION)
    gate = read_required(root, TRIAL03_GATE)
    operation = read_required(root, TRIAL03_OPERATION)

    if PREVIOUS_FAILED_CANDIDATE not in completion:
        raise RuntimeError("Trial03 completion does not contain expected failed candidate SHA")
    if "FAIL" not in gate:
        raise RuntimeError("Trial03 gate decision is not FAIL")
    if "unknown-stage" not in operation or "RESOURCE_REQUIRED" not in operation:
        raise RuntimeError("Trial03 operation evidence does not match audited defect")

def unified(rel: Path, before: str, after: str) -> str:
    return "".join(difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=str(rel),
        tofile=str(rel),
    ))

def main() -> int:
    ap = argparse.ArgumentParser(description="Apply G01 formal-FAIL rework workflow guard and Trial04 remediation contract.")
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--no-diff", action="store_true")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    if not (root / ".git").exists():
        raise RuntimeError(f"not a Git repository root: {root}")

    ensure_target_files_clean(root)
    verify_trial03_evidence(root)

    changes = []

    current = read_required(root, FAIL_REWORK)
    desired = FAIL_REWORK_CONTENT.rstrip() + "\n"
    if current != desired:
        if not current.startswith("# FAIL Rework Coding Agent Prompt — ENH-E5"):
            raise RuntimeError("unexpected fail_rework_coding_agent_prompt.md header")
        changes.append((FAIL_REWORK, current, desired))

    current = read_required(root, ASSEMBLY)
    marker = "## 16. Formal FAIL Remediation Trial Guard"
    if marker not in current:
        desired = current.rstrip() + "\n" + ASSEMBLY_GUARD.rstrip() + "\n"
        changes.append((ASSEMBLY, current, desired))
    elif current.count(marker) != 1:
        raise RuntimeError("duplicate Formal FAIL Remediation Trial Guard detected")

    p = root / TRIAL04_08
    desired = TRIAL04_08_CONTENT.rstrip() + "\n"
    if p.exists():
        current = p.read_text(encoding="utf-8")
        if current != desired:
            raise RuntimeError(f"{TRIAL04_08} already exists with different content; refusing overwrite")
    else:
        changes.append((TRIAL04_08, "", desired))

    print("Planned changes:")
    if not changes:
        print("  none (already applied)")
    for rel, before, after in changes:
        print(f"  - {rel}")
        if not args.no_diff:
            print(unified(rel, before, after), end="")

    if not args.apply:
        print("\nDRY-RUN ONLY. Re-run with --apply.")
        return 0

    for rel, _, after in changes:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(after, encoding="utf-8")

    if read_required(root, FAIL_REWORK) != FAIL_REWORK_CONTENT.rstrip() + "\n":
        raise RuntimeError("postcondition failed: FAIL rework prompt")

    assembly = read_required(root, ASSEMBLY)
    for token in (
        "## 16. Formal FAIL Remediation Trial Guard",
        "BLOCKED_REMEDIATION_HANDOFF_INCOMPLETE",
        "BLOCKED_REMEDIATION_NOT_APPLIED",
        "FIXED_TRIAL_CANDIDATE_SHA != PREVIOUS_FAILED_CANDIDATE_SHA",
    ):
        if token not in assembly:
            raise RuntimeError(f"postcondition failed: missing {token}")

    if (root / TRIAL04_08).read_text(encoding="utf-8") != TRIAL04_08_CONTENT.rstrip() + "\n":
        raise RuntimeError("postcondition failed: Trial04 remediation contract")

    print("\nAPPLIED")
    print("Next action after review/commit/push:")
    print("  fail_rework_coding_agent_prompt.md")
    print("  GATE_ID=G01")
    print("  TRIAL_NO=04")
    print("  DO NOT run Trial04 P01/P02/P03 Work Package agents.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
