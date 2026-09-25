# Controlled Runbook Workflow — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでstep prompt / result / final decision recordの作成・実行境界が分かること。

## 1. Purpose

Destructive / irreversible / infrastructure-sensitive operationをHuman-controlled sequential executionとして実行・記録する。

## 2. 使用する場面

- DB reset / destructive cleanup
- migration reset / rebuild
- infrastructure-sensitive operation
- stepごとのHuman判定が必要な作業

## 3. Pattern

```text
NN_step_prompt.md
  ↓ Agent executes exactly bounded action
NN_step_result.md
  ↓ Human reviews
next NN prompt or stop
...
99_completion_summary_decision_record.md
```

## 4. Authoring rules

- step promptはexact command / allowed action / prohibited action / precondition / expected result / abort condition / **result schema**を自身に含む。
- Agentへ別result templateを読ませなければ結果を書けない構造にしない。
- step resultはcommand、exit code、raw relevant output、facts、deviation、conclusionを本文内に記録する。
- previous resultは次stepのfact inputとして参照してよい。
- step result自体はnext stepをauthorizeしない。Human / workflow ownerが次promptを確定する。
- final summaryはobjective、executed steps、final state、destructive changes、residual risks、decision、next allowed actionを本文内に持つ。

このworkflowのresult自体はGate PASS authorityを持たない。
