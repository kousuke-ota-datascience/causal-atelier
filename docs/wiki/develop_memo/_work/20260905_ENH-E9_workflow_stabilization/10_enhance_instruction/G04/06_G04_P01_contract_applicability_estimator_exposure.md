# ENH-E9 G04 P01 — Diagnostics Contract / Applicability / Estimator Exposure

**Document class:** Work Package Execution Contract  
**Self-containment:** `MUST`  
**Assigned Coding Agent normative context:** `THIS DOCUMENT ONLY`  
**Status:** `FROZEN`  
**Gate:** `G04`  
**Package:** `P01`  
**Depends on:** G03 canonical `999_gate_decision = PASS`

## 1. Objective

Later G04 packagesがstring parsing・estimator internals推測なしに利用できるよう、structured diagnostics applicability contractと、scientifically defined estimator/component weight exposure boundaryを実装する。

P01はTreatment Effectの数値を変更するPackageではない。診断対象として利用するweight/component semanticsをstable interfaceへ公開し、`DIAGNOSTICS_RESULT` contractを後続Packageが安全に構築できる前提を作る。

## 2. Entry criteria

- branch=`bugfix/ariadne_mvp_e9`
- clean working tree
- G03 canonical `999_gate_decision = PASS`
- current Trialにformal 08 remediation contractなし
- 本P01がexactly one解決されFROZEN

package reportやcandidate assemblyはdependency PASSの代替authorityではない。

## 3. Baseline facts

Current baselineでは:

- Estimation adapterは`sample_size`, `design`, unweighted `balance`, propensityがある場合の`overlap`をstructured diagnosticsへ保存する。
- adapterは`compute_balance_table(..., weights=None)`相当でbalanceを計算しており、current balanceはpost-weighting balanceではない。
- `TreatmentEffectEstimator.ipw()`はATE/ATTのanalysis weightsとtreated/control ESSを内部計算するがstable diagnostics contractへ公開しない。
- `TreatmentEffectEstimator.aipw()`はpropensity augmentation componentを利用するが、estimator全体を表すsingle final weight vectorは存在しない。
- `compute_balance_table`はoptional weightsを受けられる。

Source/testsはimplementation substrate調査に利用してよいが、このP01とverified source factが矛盾する場合はsilent reinterpretせず停止する。

## 4. Required applicability contract

Exactly these stable valuesを使用する。

```text
ESTIMATOR_WEIGHT
PROPENSITY_COMPONENT
NOT_APPLICABLE
```

Meaning:

- `ESTIMATOR_WEIGHT`: effect calculationに実際に用いるanalysis weightをdiagnoseできる estimator。E9ではIPW。
- `PROPENSITY_COMPONENT`: estimator全体のfinal weightではないが、propensity-derived component diagnosticを科学的に定義できる estimator。E9ではAIPW。
- `NOT_APPLICABLE`: analysis weight/ESSを作るべきでない estimator。E9ではOLS / difference-in-means。

Unknown estimatorを推測でいずれかへ分類しない。current supported estimator mappingと不整合があればBLOCKED。

## 5. IPW authoritative weight semantics

`e(x)` = configured propensity clipping後のpropensity score。

```text
ATE:
  treated observed rows: 1 / e(x)
  control observed rows: 1 / (1 - e(x))

ATT:
  treated observed rows: 1
  control observed rows: e(x) / (1 - e(x))
```

Distribution/ESS対象は各armのobserved rowsに対応するpositive weightsだけ。反対arm用zero placeholderをstatisticsへ含めない。

Effect calculationとの同一性を保証するため、diagnostic用weight formulaを別実装してdriftさせない。Estimator側からactual weightsまたは同一authoritative componentを安全に露出できるinterfaceを設計する。

## 6. AIPW boundary

AIPWは`PROPENSITY_COMPONENT`。

- whole-estimator single final weightとして公開しない。
- propensity-derived componentを公開する場合、definitionでfinal estimator weightではないことを明記できる形にする。
- whole-estimator treated/control ESSを要求しない。
- component semanticsがcurrent AIPW implementationから一意に定義できない場合、P01で架空interfaceを作らずBLOCKED_CONTRACT_AMBIGUITYとする。

## 7. NOT_APPLICABLE boundary

OLS / difference-in-means:

- analysis weight vectorを生成しない。
- ESSを生成しない。
- downstream contractが`null`を表現できるようにする。

## 8. Extreme-weight rule — frozen choice

E9 stable rule:

```text
extreme_rule = "weight > 10.0"
extreme_count = count(weight > 10.0)
```

Rules:

- `weight == 10.0`はextremeではない。
- un-normalized arm-specific analysis weightに適用。
- propensity clipping countを流用しない。
- p95/p99等data-relative ruleへsilent変更しない。

## 9. Structured contract target exposed by P01

P01自身が全部persistする必要はないが、後続が次を一意に構築できるtyped/stable semanticsを提供する。

```text
balance.after_applicability:
  ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE

weighting.applicability:
  ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE
weighting.estimand:
  ATE | ATT | null
weighting.definition:
  stable human-readable semantics
weighting.effective_sample_size:
  treated: number | null
  control: number | null
weighting.treated:
  stats object | null
weighting.control:
  stats object | null
```

## 10. Protected invariants

- Treatment Effect estimate / standard error / confidence interval / p-value semantics
- ResultType
- Execution/Result lineage
- existing API route grammar
- propensity clipping behavior
- estimator selection semantics
- AIPWをsingle final weightとして表現しない

## 11. Explicitly forbidden

- diagnostic目的でeffect calculation formulaを変更
- fabricated weight/ESS
- propensity clipping countをextreme_countとして再利用
- frontendへscientific calculationを移動
- new ResultType / route grammar
- P02以降のpersistence/frontend scope先行実装（P01 contract成立に不可欠な最小interface変更を除く）

## 12. Implementation substrate hints

Likely responsibility（仕様authorityではない）:

- `src/ariadne/causal/inference/estimators/treatment_effect.py`
- estimator inference/weight helper modules
- `src/ariadne/scientific/inference/adapter.py`とのinterface boundary
- relevant scientific/unit/contract fixtures

## 13. Focused verification — mandatory

Browser E2Eは実行しない。

Required tests:

1. applicability enum/value serializationがexactly three stable values。
2. IPW ATE actual treated/control positive weightsが§5 formulaと一致。
3. IPW ATT actual treated/control positive weightsが§5 formulaと一致。
4. exposed diagnostics inputとeffect calculationに使うweight semanticsがdriftしない。
5. extreme boundary: `10.0`はcountしない、`>10.0`はcountする。
6. propensity clipping countとweight extreme_countが独立。
7. OLS/difference-in-meansはNOT_APPLICABLEでweights/ESSを作らない。
8. AIPWはPROPENSITY_COMPONENTでありfinal-weight interfaceとして誤表現されない。
9. existing Treatment Effect numeric regressionがPASS。

## 14. Completion boundary

P01 completeは、§4–§9 contractをdownstreamがconsume可能な形で成立させ、§13がPASSし、Treatment Effect semanticsにregressionがなく、checkpoint/reportが存在する場合のみ。

## 15. Stop rule

以下は推測せずBLOCKED:

- actual IPW effect weightsとdiagnostic weightを同一authorityから露出できない
- AIPW componentの意味を一意に定義できないのにfieldを埋める必要がある
- current estimator mappingが§4と矛盾
- Gate AC/semantic changeが必要

Gate semantic defectなら09 amendmentへ戻す。
