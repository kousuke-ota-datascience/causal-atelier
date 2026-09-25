# ENH-E9 G04 P04 — Frontend Structured Diagnostics Consumption

**Document class:** Work Package Execution Contract  
**Self-containment:** `MUST`  
**Assigned Coding Agent normative context:** `THIS DOCUMENT ONLY`  
**Status:** `FROZEN`  
**Gate:** `G04`  
**Package:** `P04`  
**Depends on:** G04 P03 canonical package report `State: PACKAGE_COMPLETE`

## 1. Objective

Frontend Diagnostics surfaceを、persisted structured `DIAGNOSTICS_RESULT`のpresentation projectionとして成立させる。FrontendはESS、weights、weighted balance、applicabilityを再計算・推測しない。

## 2. Entry criteria

- branch=`bugfix/ariadne_mvp_e9`
- clean working tree
- P03 canonical package reportがexactly one存在し`State: PACKAGE_COMPLETE`
- 本P04がexactly one解決されFROZEN
- current Trialにformal 08 remediation contractなし

## 3. Persisted structured contract to consume

Existing top-level `sample_size`, `design`, `overlap`を互換表示する。新authorityは次。

```text
balance:
  before: <balance row list>
  after: <balance row list | null>
  after_applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE

weighting:
  applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE
  estimand: ATE | ATT | null
  definition: <stable semantics string>
  effective_sample_size:
    treated: <number | null>
    control: <number | null>
  treated: <stats object | null>
  control: <stats object | null>
```

Applicable stats object:

```text
count
min
mean
p50
p95
p99
max
extreme_count
extreme_rule
```

E9 frozen extreme rule string:

```text
weight > 10.0
```

Frontendはこのstringをdisplayしてよいが、string parsingでscientific logicを再構成しない。

## 4. Required rendering semantics

### 4.1 `ESTIMATOR_WEIGHT`

IPW等。Persisted valuesが利用可能なら:

- weighting definition / estimand
- treated/control ESS
- treated/control weight summary
- unweighted `balance.before`
- weighted `balance.after`

をhuman-readableに表示する。

### 4.2 `PROPENSITY_COMPONENT`

AIPW等。

- whole-estimator final weightではなくpropensity componentであることを表示上区別する。
- ESSがnullなら`N/A`/not applicable相当として扱い、0やcomputed fallbackを表示しない。
- `balance.after = null`ならunavailable/not providedとして扱い、beforeをafterとして表示しない。

### 4.3 `NOT_APPLICABLE`

OLS / difference-in-means等。

- weighting/ESS/after-balanceを未実装エラー扱いにしない。
- not applicableとして明示する。
- `balance.before`は利用可能なら表示する。

### 4.4 Missing / legacy payload

Backward compatibilityとしてlegacy payloadを読む必要がある場合:

- legacy top-level `balance` listはunweighted/before相当としてのみ扱う。
- legacy balanceをnew `balance.after` authorityへ昇格させない。
- new structured fieldsがない場合、frontendでweight/ESS/post-weight balanceを再計算しない。
- unavailable stateを明示する。

## 5. Authority boundary

Frontendが行ってよいのはpresentation formattingのみ。

Forbidden computation:

- ESS formula
- weight generation
- quantile calculation
- extreme_count calculation
- weighted balance calculation
- estimator applicability inference from estimator name when persisted applicability is available
- `definition` string parsingによるbranching

Persisted structured fieldをprimary authorityとする。

## 6. Protected invariants

- Effects / Diagnostics are distinct Stage-owned surfaces
- Treatment Effect display remains sourced from persisted `TREATMENT_EFFECT_RESULT`
- Diagnostics display remains sourced from persisted `DIAGNOSTICS_RESULT`
- Result/Execution lineage
- route grammar / Navigation Stage semantics
- frontend does not create scientific Result semantics

## 7. Explicitly forbidden

- frontend-side scientific recomputation
- legacy string notesからESS等をregex抽出
- after missing時にbeforeを代入
- nullを0へcoerce
- Diagnostics修正のためbackend treatment-effect semanticsを変更
- unrelated Stage refactor

## 8. Implementation substrate hints

Likely responsibility（仕様authorityではない）:

- Diagnostics rendering/state logic in `frontend/app.js`
- relevant Diagnostics markup/CSS
- frontend/product tests
- persisted result payload integration fixtures

## 9. Focused verification — mandatory

Browser E2Eは実行しない。

Required deterministic cases:

1. ESTIMATOR_WEIGHT payloadをstructured fieldsから表示する。
2. treated/control ESS/statsをpersisted numberから表示し、recomputeしない。
3. before/afterをdistinct fieldsとして表示する。
4. PROPENSITY_COMPONENT + ESS nullをN/Aとして安全に表示する。
5. PROPENSITY_COMPONENT + after nullでbefore fallbackをpost-weightとして表示しない。
6. NOT_APPLICABLEでweights/ESS/after balanceをfabricateしない。
7. legacy balance-only payloadはbefore compatibilityとしてのみ表示する。
8. `definition`/notes string parsingでscientific fieldsを生成しない。
9. Effects surface / Result lineage / route regression PASS。
10. touched JS syntax/static check PASS。

## 10. Completion boundary

P04 completeは、frontendがpersisted structured diagnosticsを直接consumeし、all mandatory non-browser verificationがPASSし、scientific recomputation/string parsingがなく、checkpoint/reportが存在する場合のみ。

P04 completion後、all required G04 packages complete evidenceに基づきCandidate Assemblyへ進む。P04自身はGate PASSを宣言しない。

## 11. Stop rule

- persisted payload shapeが本contractと矛盾しfrontendで推測補完が必要になる
- backend structured contract変更が必要
- Stage ownership変更が必要
- Gate claim/AC変更が必要

これらはP04内でsilent修正せずBLOCKED。Gate semantic defectなら09 amendmentへ戻す。
