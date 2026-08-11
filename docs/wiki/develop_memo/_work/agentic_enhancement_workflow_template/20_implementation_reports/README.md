# 20_implementation_reports — 実装証跡の作成ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけで各implementation reportの目的・作成時点・記載事項・authority boundaryが分かること。

## 1. Purpose

`20_implementation_reports/`には、Coding Agentが何を実装し、どのcheckpointを作り、どのcandidateをIndependent Verificationへ提出したかを記録する。

20層は**implementation evidence / unverified ledger**であり、Gate PASS authorityやverified current stateを持たない。

## 2. Evidence self-containment rule

各reportは、そのreportだけで「何を実施したか / 何が観測されたか / 現在statusは何か / 次に何が必要か」を理解できるようにする。

外部参照してよいもの:

- commit SHA / diff
- source / migration / test path
- command output / log
- package instruction / Completion Report / Gate Decisionのtraceability path

外部へ委譲してはいけないもの:

- report自身のstatus意味
- 実施内容summary
- observed facts
- completion / blocker rationale
- candidate identity / checkpoint identity

## 3. Directory

```text
20_implementation_reports/{{GATE_ID}}/
  {{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md
  Trial{{TRIAL_NO}}/
    packages/                       # WORK_PACKAGE only
    {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
```

## 4. Artifact responsibilities

### Package Execution Status Report
1 Agent executionの完了 / 中断 / blockerを記録する。Checkpoint Reportとは別artifact。

### Implementation Checkpoint Report
1 Work Packageのimplementation checkpoint evidence。Gate acceptanceを主張しない。

### Implementation Completion Report
1 TrialのCandidate AssemblyとFixed Trial Candidate identityを記録する。`READY_FOR_TEST`はCoding-side handoff statusでありPASSではない。

### Gate-local Implementation Detail
Gate内部の累積unverified ledger。Trial / package progress、open observation、TD implementation factsを記録する。

## 5. Evidence identity

```text
Package Checkpoint SHA
  ↓ package chain / Candidate Assembly
Fixed Trial Candidate SHA
  ↓ Independent Verification
999 Gate Decision
```

implementation checkpoint SHA、Fixed Candidate SHA、report-only commit SHA、Test artifact commit SHAを混同しない。

## 6. Required content summary

Package status report:
- execution status / completed / remaining / blocker / verification / relevant SHA / next action

Checkpoint report:
- starting SHA / checkpoint SHA / changed files / focused verification / dependency state / limitations

Completion report:
- package chain or single-execution evidence / Candidate Assembly / Fixed Candidate SHA / Gate-wide self-check / protected regression / post-candidate diff state

Detail ledger:
- Trial history / package history / current unverified implementation state / candidate assembly state / open observations / final Gate Decision link after completion
