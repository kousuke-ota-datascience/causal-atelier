# Ariadne ENH-E7 — Project Management / Analysis Workspace IA Redesign

**Workflow instance:** `20260813_ENH-E7_project_analysis_workspace_separation`  
**Branch:** `feature/ariadne_mvp_e7`  
**Execution mode:** WORK_PACKAGE  
**Gate count:** 2  
**Current status:** G01 P01 PRE-EXECUTION BASELINE / EXECUTION ELIGIBILITY DERIVED BY PREFLIGHT

## Purpose

This is an instantiated Agentic Enhancement Workflow for ENH-E7.

It separates:

- semantic acceptance boundary: Gate
- Coding execution unit: Work Package
- candidate verification attempt: Trial
- verified current state: final PASS only

## Gates

```text
G01 — Project Management Surface Contract
  -> PASS establishes Project routes, ownership and Project resource surfaces.

G02 — Analysis Workspace Contract
  -> PASS establishes Analysis Context, Family/Stage workspace, existing surface migration,
     cross-surface navigation and compatibility.
```

G02 depends on G01 final PASS.

## Operator Quick HowToUse

Do **not** point Agents at the shared template directory.

### Run one Work Package

Give the Coding Agent:

```text
Read and execute:
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/
10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime identity:
- GATE_ID=G01
- PACKAGE_ID=P01
- TRIAL_NO=01
```

Before execution, run the local readiness check:

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . --gate G01 --package P01 --trial 01
```

Preflightは実行対象・current branch・Architecture/Gate blocking state・required dependency evidenceから実行可否を導出する。remote alias、declared package status、説明用placeholder等のdiagnostic差異だけではBLOCKしない。

## Important information isolation rule

For a Work Package Coding Agent:

```text
normative workflow implementation contract = assigned Pxx only
```

06 / 07 / P00 / other Pxx are Human/operator/audit traceability and must not be used by the Coding Agent to complete its package specification.

## Execution-control principles

- `READY_TO_EXECUTE` 等のdeclared status literalをworkflow cursorにしない。
- required dependency completionはpackage execution status reportから導出する。
- Work Packageはbounded implementation + focused verificationの単位とし、package単位のFixed Candidate SHAを要求しない。
- Fixed Trial Candidate identityと正式なquality verificationはGate boundaryで扱う。
- preflightは`FAIL / WARN / INFO`を区別し、非本質的不一致によるfalse-positive blockを避ける。

## Evidence semantics

```text
PACKAGE_COMPLETE
  != READY_FOR_TEST
  != Gate PASS

final Gate PASS authority = 999 Gate Decision
```
