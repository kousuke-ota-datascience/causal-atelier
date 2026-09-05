# Ariadne ENH-E9 G04 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `WORK_PACKAGE`  
**Entry:** G03 canonical `999_gate_decision = PASS`

## 1. Gate claim

Estimator/analysisにapplicableなcausal diagnosticsをstable structured `DIAGNOSTICS_RESULT`としてpersistし、Frontendがstring parsing・再計算・推測なしに表示できるbackend contractを成立させる。

## 2. Baseline facts

Baseline adapterはsample_size/design/unweighted balance/overlapをstructured diagnosticsとして保存する。`compute_balance_table`自体はoptional weightsを受けられるがadapterはweightなしで呼ぶ。IPW estimatorはanalysis weightsとESSを内部で計算するがstructured Resultへ公開しない。したがってFR-048 full conformance gapが存在する。

## 3. Required structured semantics

既存`sample_size`, `design`, `overlap`を互換維持し、次を追加/移行する。

- `balance.before`: unweighted covariate balance rows
- `balance.after`: applicable weight/component weightによるbalance rows。non-applicable/undefinedならnull
- `balance.after_applicability`: `ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE`
- `weighting.applicability`: 同上
- `weighting.estimand`
- `weighting.definition`
- `weighting.effective_sample_size.treated/control`
- applicableなtreated/control weight distribution: `count,min,mean,p50,p95,p99,max,extreme_count,extreme_rule`

Backward compatibilityが必要なcurrent consumerがある場合、migration期間だけlegacy `balance` projectionを維持してよいが、frontend新実装のauthorityはbefore/after contractとする。

## 4. Estimator applicability

### IPW

`ESTIMATOR_WEIGHT`。ATE/ATTで実際にeffect calculationに用いるarm-specific weightsをdiagnoseする。ESSは `(sum w)^2 / sum(w^2)` でestimator internal ESSと一致する。Weight scale/normalizationは`definition`で明示する。

### AIPW

`PROPENSITY_COMPONENT`。AIPW全体のsingle final weightとして表現しない。Propensity-derived componentに対し科学的に定義できるdiagnosticsのみ保存する。IPWと同一setを機械的に要求しない。

### OLS / difference-in-means

`NOT_APPLICABLE`。weight/ESSを架空値で埋めない。before balanceは保存可、afterはnullを許容する。

## 5. Extreme-weight rule

`extreme_count`は必ず`extreme_rule`と対で保存する。Ruleはscientific/configuration authorityとして実装時に一意に固定し、test fixtureで境界値を検証する。Propensity clipping countをweight extreme countとして流用しない。

## 6. Frontend boundary

Frontendはstructured fieldsをpresentationへ投影するだけとし、ESS、weights、weighted balanceを再計算しない。利用不能項目はnot applicable/unavailableとして表示する。

## 7. Protected semantics

Treatment Effect calculation、ResultType、Execution/Result lineage、existing API route grammar、Effects/Diagnostics Stage ownershipを維持する。

## 8. Work Packages

P01 contract/applicability + estimator exposure、P02 IPW ESS/weight persistence、P03 before/after balance + AIPW applicability、P04 frontend structured consumption/regression。Pxxは本06/07 semanticsを変更できない。
