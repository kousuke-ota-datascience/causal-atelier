# ENH-E7 Work Package Coding Agent Prompt

**Role:** resolver + guardrail only  
**Enhancement:** ENH-E7  
**Branch:** feature/ariadne_mvp_e7  
**Work root:** docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation

Human provides exactly:

```text
GATE_ID=<G01|G02>
PACKAGE_ID=<Pxx>
TRIAL_NO=<NN>
```

## 1. Preflight first

Run:

```bash
python docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . --gate <GATE_ID> --package <PACKAGE_ID> --trial <TRIAL_NO>
```

If result is not PASS, stop and report `BLOCKED_PRECHECK`.

## 2. Resolve assigned Pxx

The only normative workflow implementation contract for this Coding execution is the exactly-one file:

```text
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/10_enhance_instruction/<GATE_ID>/06_<GATE_ID>_<PACKAGE_ID>_*.md
```

It must resolve to exactly one active Pxx and must not resolve to P00.

## 3. Information isolation — MUST

Read the assigned Pxx.

Do **not** read Gate 06, Gate 07, P00, other Pxx, 00 background, 20 reports, 30 reports, previous Enhancement workflow artifacts, ADR/issues or external Web to fill missing package specifications.

You may inspect source code, tests, config, migrations and runtime facts as implementation substrate, within the assigned Pxx scope.

If the Pxx is insufficient or conflicts with verified source facts, stop as `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`.

## 4. Execute

Implement only the assigned Pxx. Run its focused verification. Do not continue into another package.

## 5. Report

At completion or interruption, produce the package status/checkpoint reports required by the assigned Pxx.

Never declare Gate PASS/FAIL.
