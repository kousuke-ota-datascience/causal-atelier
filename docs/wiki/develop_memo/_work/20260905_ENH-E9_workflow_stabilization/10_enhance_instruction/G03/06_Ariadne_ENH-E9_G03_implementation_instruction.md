# Ariadne ENH-E9 G03 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `SINGLE_EXECUTION`  
**Entry:** G02 canonical `999_gate_decision = PASS`

## 1. Gate claim

Identification causal-question inputを、scientific semanticsを変更せず意味と候補を理解できるinteractionへ改善する。

## 2. Required behavior

- Populationにtarget populationとして何を記述するか分かるhelp/tooltipを提供する。
- ComparatorにTreatmentのcounterfactual/reference conditionとして何を記述するか分かるhelp/tooltipを提供する。
- Treatmentはselected Dataset Version schemaをcandidate authorityとするselectorで選択できる。既存causal-question serialization/backend validationを維持する。
- Dataset Version変更等でselected Treatmentがcandidateから消えた場合、stale valueをsilent保持しない。

## 3. Protected Identification Outcome behavior

2026-08-23 historical Enhance Requestの明示仕様をregression protectionとする。

`Outcome = 必須・入力不要 / FIXED Graphから自動継承`。

Implementation上はselected FIXED Graph / GraphVersionのdesignated OutcomeをIdentificationにread-onlyで投影し、独立editable selector/free textを追加しない。Estimationはselected Identification Result lineageをauthorityとし、独立Outcome overrideを追加しない。

`Outcome one-way ownership`という名称自体はcontract authorityではない。

## 4. Other protected semantics

FIXED Graph prerequisite、Population/Treatment/Comparator/Outcome/Time/Estimand/Decision Use、identification strategy、adjustment set、assumptions、backend validation authority。

## 5. Forbidden

selector独自scientific validation、新Dataset schema API、Estimation submission architecture変更。
