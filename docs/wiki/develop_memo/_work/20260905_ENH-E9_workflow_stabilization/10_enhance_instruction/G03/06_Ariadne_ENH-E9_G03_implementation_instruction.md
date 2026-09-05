# Ariadne ENH-E9 G03 Implementation Instruction

**Contract status:** `DRAFT_NOT_FROZEN`  
**Execution mode:** `SINGLE_EXECUTION`

## Gate claim

Identification causal-question inputを、scientific semanticsを変更せず意味と候補を理解できるinteractionへ改善する。

## Allowed scope

baselineでresidual確認された場合のみ:

- Population meaning/help
- Comparator meaning/help
- Treatment candidate selection backed by selected Dataset Version schema

## Protected Outcome contract

```text
Discovery designated Outcome
 -> GraphVersion designated_outcome_node
 -> Identification read-only Outcome
 -> Estimation
```

Outcomeをeditable selector/free textへ戻してはならない。

## Other protected semantics

- FIXED Graph prerequisite
- Population/Treatment/Comparator/Outcome/Time/Estimand/Decision Use semantics
- identification strategy / adjustment set / assumptions
- backend validation authority

## Forbidden

- selector独自のscientific validation追加
- Treatment selectorを理由とするnew Dataset schema API
- Estimation input architecture変更
