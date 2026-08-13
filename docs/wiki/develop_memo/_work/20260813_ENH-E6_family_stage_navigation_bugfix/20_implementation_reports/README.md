# 20_implementation_reports — ENH-E6 実装証跡

**Document class:** Authoring Guide  
**Self-containment:** MUST.

## 1. Purpose

Coding Agent/Package executionとCandidate Assemblyが生成するimplementation evidenceを保存する。ここはGate acceptance authorityではない。Package checkpoint、candidate identity、Gate PASSを分離する。

## 2. Evidence self-containment rule

各reportは自身が観測/実行した事実、command/result、identity、status、blockerを本文内に持つ。source/diff/logはevidence参照可。Pxxを再定義したり07 Acceptance Criteriaを補完しない。

## 3. Directory

```text
20_implementation_reports/
  G01/
    ENH-E6_G01_implementation_report_detail.md
    Trial01/
      README.md
      packages/
        README.md
        <P01/P02/P03 reports created by execution>
      <candidate completion report created by Candidate Assembly>
```

## 4. Artifact responsibilities

### Package Execution Status Report

Assigned Pxxのexecution status、START_SHA、progress/blocker、changed/uncommitted stateを記録する。Coding Agentがoperator workflowに従い作成する。事前にfake reportを作らない。

### Implementation Checkpoint Report

Package implementation + focused verification完了時のcheckpoint identity/commands/resultsを記録する。Gate PASS authorityなし。

### Implementation Completion Report

Candidate Assemblyがpackage checkpointsを統合してFixed Trial Candidate identityを記録する。Coding Agent individual packageが勝手に作成しない。

### Gate-local Implementation Detail

G01のTrial/package/candidate historyを継続的に記録するHuman/audit ledger。未検証実装状態を含むためCurrent State verified stateとは別。

## 5. Evidence identity

`START_SHA`, `PACKAGE_CHECKPOINT_SHA`, `EVIDENCE_COMMIT_SHA`, `FIXED_TRIAL_CANDIDATE_SHA`を別identityとして記録する。Planning baseline SHAをpackage start SHAとして代入しない。

## 6. Required content summary

各runtime reportは、scope、changed files、commands/results、status、identity、remaining work、blocker、prohibited work absenceを必要に応じて記録する。Package status=`PACKAGE_READY`はGate PASSではない。

## 7. Canonical Completion Report responsibility

P01-P03 required checkpoints後のCandidate AssemblyのみがTrial01 Implementation Completion Report/Fixed Candidateを生成する。その後Independent Verificationへhandoffする。
