# 20_implementation_reports — Execution Evidence Specification v3

## 0. Purpose

Coding Agent execution evidenceを、Gate / Trial / Work Package階層で保存する。

```text
package execution status report
  = 1 Agent executionの完了 / 中断 / blocker記録

implementation checkpoint report
  = 1 Work Packageのimplementation checkpoint evidence

implementation completion report
  = 1 TrialのFixed Trial Candidate transaction record

implementation report detail
  = 1 Gateの累積unverified implementation ledger
```

verified current stateはここで管理しない。

## 1. Directory

```text
20_implementation_reports/{{GATE_ID}}/
  {{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md
  Trial{{TRIAL_NO}}/
    packages/
    {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
```

## 2. Evidence identity

```text
Package Checkpoint SHA
  ↓ package chain
Fixed Trial Candidate SHA
  ↓ Independent Verification
Gate Decision
```

Report commit SHAとimplementation checkpoint SHAを分離する。

## 3. Package status report

Coding executionが完了・中断・継続不能になった時点で記録する。checkpoint reportとは別artifactである。

推奨file:

```text
{{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
```

## 4. Implementation Checkpoint Report

Work Package Modeで各Pxx/Rxxごとに作成する。

MUST:

- starting SHA
- package implementation checkpoint SHA
- report SHA if separate
- changed files
- focused verification
- dependency status
- completion / blocker state
- residual risk / next dependency

MUST NOT claim Gate PASS。

## 5. Implementation Completion Report

Trial candidate assembly後に作成する。

MUST:

- all required package checkpoints
- candidate assembly evidence
- Fixed Trial Candidate SHA
- candidate-affecting diff state
- Gate-wide self-check
- protected previous-Gate self-regression
- applicable remediation
- READY_FOR_TEST / BLOCKED

## 6. Gate-local Detail Ledger

Trial / package progressを累積記録してよい。未検証stateであることを明示する。
