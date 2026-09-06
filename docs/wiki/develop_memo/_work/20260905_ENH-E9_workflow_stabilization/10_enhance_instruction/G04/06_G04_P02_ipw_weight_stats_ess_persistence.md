# ENH-E9 G04 P02 — IPW Actual-Weight Statistics / ESS Persistence

**Document class:** Work Package Execution Contract  
**Self-containment:** `MUST`  
**Assigned Coding Agent normative context:** `THIS DOCUMENT ONLY`  
**Status:** `FROZEN`  
**Gate:** `G04`  
**Package:** `P02`  
**Depends on:** G04 P01 canonical package report `State: PACKAGE_COMPLETE`

## 1. Objective

IPW ATE/ATTでeffect calculationに実際に使用するarm-specific analysis weightsをdiagnoseし、stable structured `DIAGNOSTICS_RESULT.weighting`へweight statisticsとtreated/control ESSをpersistする。

P02はTreatment Effectの数値・uncertainty semanticsを変更しない。Diagnosticsはexisting estimator calculationを観測可能にするものであり、別のweight systemを作らない。

## 2. Entry criteria

- branch=`bugfix/ariadne_mvp_e9`
- clean working tree
- P01 canonical package reportがexactly one存在し`State: PACKAGE_COMPLETE`
- 本P02がexactly one解決されFROZEN
- current Trialにformal 08 remediation contractなし

P01のsource implementationを仕様補完目的で読まない。本P02だけで必要semanticsを判断する。

## 3. IPW authoritative analysis weights

`e(x)` = configured propensity clipping後のpropensity score。

```text
ATE:
  treated observed rows: 1 / e(x)
  control observed rows: 1 / (1 - e(x))

ATT:
  treated observed rows: 1
  control observed rows: e(x) / (1 - e(x))
```

Statistics/ESS対象は各armのobserved rowsに対応するpositive weightsだけ。反対arm用zero placeholderを含めない。

Persist対象はeffect calculationに実際に使ったweight semanticsと同一でなければならない。diagnostics側で類似formulaを再実装してdriftさせない。

## 4. Required `weighting` payload for IPW

```text
weighting:
  applicability: ESTIMATOR_WEIGHT
  estimand: ATE | ATT
  definition: "arm-specific IPW analysis weights computed from clipped propensity scores; weighted means normalize by each arm's weight sum"
  effective_sample_size:
    treated: <finite number>
    control: <finite number>
  treated:
    count: <integer>
    min: <finite number>
    mean: <finite number>
    p50: <finite number>
    p95: <finite number>
    p99: <finite number>
    max: <finite number>
    extreme_count: <integer>
    extreme_rule: "weight > 10.0"
  control: <same stats object>
```

Top-level existing `sample_size`, `design`, `overlap`等を壊さない。

## 5. ESS semantics

各arm positive weightsについて独立に:

```text
ESS = (sum(w) ** 2) / sum(w ** 2)
```

Persisted ESSはestimator standard-error calculationが使用するarm ESSと一致する。

0 denominatorや非finite値を架空値へ置換しない。valid IPW executionでESSを一意に生成できない場合はBLOCKED/estimation error semanticsへ従う。

## 6. Weight statistics semantics

Diagnosed arm weightsから:

- `count`: arm observed row count
- `min`, `mean`, `max`: ordinary numeric summaries
- `p50`, `p95`, `p99`: NumPy-compatible linear quantile semantics
- `extreme_count`: `weight > 10.0` の件数
- `extreme_rule`: exactly `weight > 10.0`

`weight == 10.0`はextremeに含めない。propensity clipping countをextreme_countへ流用しない。

Persisted JSONにNaN/Infinityを出さない。

## 7. Required ATE / ATT behavior

### ATE

- treated arm: inverse clipped propensity
- control arm: inverse one-minus-clipped-propensity
- both arms actual positive analysis weightsをsummary

### ATT

- treated arm weightは全observed treated rowsで`1`
- control armはclipped propensity odds `e/(1-e)`
- ATT treated statistics/ESSも実際のunit weightsから計算する。special-caseで省略しない。

## 8. Protected invariants

- Treatment Effect estimate / SE / CI / p-value
- propensity clipping semantics
- estimator method/estimand selection
- Result/Execution lineage
- existing ResultType/API route grammar
- overlap diagnostic semantics

## 9. Explicitly forbidden

- combined fake final-weight vectorをpersist
- stabilized weightと称してnumerator stabilizationを新導入
- effect calculationをdiagnostics都合で変更
- propensity clipping countをweight extreme_countとして保存
- frontendでESS/statisticsを再計算させる
- AIPW/OLS/difference-in-means scopeを先行実装

## 10. Implementation substrate hints

Likely responsibility（仕様authorityではない）:

- estimator-side actual weight exposure/helper
- `src/ariadne/scientific/inference/adapter.py`
- diagnostics serialization/result payload creation
- scientific/unit/integration tests

## 11. Focused verification — mandatory

Browser E2Eは実行しない。

Known fixtureを用いてtest側でproduction helperとは独立にexpected weightsを構築し、最低限:

1. IPW ATE treated/control actual weights一致
2. IPW ATT treated/control actual weights一致
3. ATE treated/control ESS独立再計算一致
4. ATT treated/control ESS独立再計算一致
5. count/min/mean/p50/p95/p99/max独立再計算一致
6. `10.0` boundary / `>10.0` extreme_count一致
7. persisted definition/applicability/estimandがexact semantics
8. DIAGNOSTICS_RESULT persistence/serialization
9. existing Treatment Effect numeric regression PASS
10. existing overlap diagnostic regression PASS

Expected値生成でproduction statistics helperを呼ばない。

## 12. Completion boundary

P02 completeは、IPW ATE/ATTのactual weight statisticsとESSがstable structured payloadへpersistされ、independent numeric testsがPASSし、Treatment Effect semantics/regressionsがgreen、checkpoint/reportが存在する場合のみ。

## 13. Stop rule

- actual effect weightsを同一authorityから取得できない
- persisted ESSとestimator ESSを一致させられない
- JSON finite/null semanticsが一意でない
- Gate claim/AC変更が必要

上記は推測で埋めずBLOCKED。Gate semantic defectなら09 amendmentへ戻す。
