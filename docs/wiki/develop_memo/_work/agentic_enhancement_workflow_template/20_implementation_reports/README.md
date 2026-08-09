# 20_implementation_reports — Gate-local Implementation Evidence Specification v2

## 0. Purpose

Coding Agentが実際に行った実装を、Gate / Trial単位で再構成できる粒度で保存する。

```text
implementation completion report
  = 1 Gate / 1 Trialのtransaction record

implementation report detail
  = 1 Gateの累積implementation ledger
  = 未検証stateを含んでよい
```

**enhancement全体のverified current stateはここで管理しない。**
verified stateはroot Current State Control Sheetへ、final PASS evidenceだけをpromotionする。

## 1. Directory rule

```text
20_implementation_reports/{{GATE_ID}}/
```

10 / 20 / 30は同一Gate namespaceを使う。

## 2. Common rules

- commitは可能な限りfull SHA。
- pathはrepository root相対。
- blank fieldは禁止。`N/A / NONE / NOT_RUN / UNKNOWN`を使う。
- FactsとInterpretationを分離する。
- self-checkはGate PASS evidenceではない。
- report commitとimplementation commitを区別する。

## 3. Completion report

File:

```text
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_implementation_completion_report.md
```

MUST record:

- starting commit
- implementation commit
- applicable 06 / 08
- changed files
- implementation facts
- migrations/schema/API impact
- self-checks
- protected passed-Gate impact
- Transition Debt impact
- READY_FOR_TEST / BLOCKED status

## 4. Gate-local detail ledger

File:

```text
{{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md
```

MUST record:

- all Trials within this Gate
- current unverified implementation state
- unresolved Coding observations
- TD implementation actions
- protected-contract touches

MUST NOT claim:

- Gate PASS
- verified architecture promotion
- acceptance authority
