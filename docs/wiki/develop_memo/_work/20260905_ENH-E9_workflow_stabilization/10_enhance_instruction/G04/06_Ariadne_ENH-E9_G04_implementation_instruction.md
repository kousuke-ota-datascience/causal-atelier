# Ariadne ENH-E9 G04 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `WORK_PACKAGE`  
**Required packages:** `P01, P02, P03, P04`  
**First executable package:** `P01`  
**P00 role:** `PLANNING_ONLY / NON_EXECUTABLE`  
**Entry:** G03 canonical `999_gate_decision = PASS`

## 1. Gate claim

Estimator/analysisにapplicableなcausal diagnosticsをstable structured `DIAGNOSTICS_RESULT`としてpersistし、Frontendがstring parsing・再計算・推測なしに表示できるbackend contractを成立させる。

## 2. Baseline facts

Baseline adapterはsample_size/design/unweighted balance/overlapをstructured diagnosticsとして保存する。`compute_balance_table`自体はoptional weightsを受けられるがadapterはweightなしで呼ぶ。IPW estimatorはanalysis weightsとESSを内部で計算するがstructured Resultへ公開しない。AIPWはpropensity-derived augmentation componentを用いるがwhole-estimator single final weightは存在しない。したがってFR-048 full conformance gapが存在する。

## 3. Required structured semantics

既存`sample_size`, `design`, `overlap`を互換維持し、次をstable contractとする。

```text
balance:
  before: <balance row list>
  after: <balance row list | null>
  after_applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE

weighting:
  applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE
  estimand: ATE | ATT | null
  definition: <stable human-readable semantics>
  effective_sample_size:
    treated: <number | null>
    control: <number | null>
  treated: <stats object | null>
  control: <stats object | null>
```

Applicable stats object:

```text
count, min, mean, p50, p95, p99, max, extreme_count, extreme_rule
```

`balance.before`はunweighted。`balance.after`はscientifically defined actual estimator/component weightsによる場合だけ保存し、undefined/non-applicableならnull。beforeをafterへコピーしない。

## 4. Applicability semantics

### IPW — `ESTIMATOR_WEIGHT`

`e(x)`はconfigured clipping後のpropensity score。

```text
ATE:
  treated observed rows = 1 / e(x)
  control observed rows = 1 / (1 - e(x))

ATT:
  treated observed rows = 1
  control observed rows = e(x) / (1 - e(x))
```

Statistics/ESSは各arm observed rowsのpositive actual analysis weightsだけを対象とする。反対arm zero placeholderを含めない。

ESS:

```text
(sum w)^2 / sum(w^2)
```

`definition`は次のsemanticsを表現する。

```text
arm-specific IPW analysis weights computed from clipped propensity scores; weighted means normalize by each arm's weight sum
```

### AIPW — `PROPENSITY_COMPONENT`

AIPW全体をsingle final weightとして表現しない。Propensity-derived componentについてscientifically一意に定義できるdiagnosticsだけ保存する。

- whole-estimator treated/control ESSをfabricateしない。null可。
- component after-balanceを一意に定義できない場合`balance.after = null`。
- IPWと同じdiagnostic setを機械的に要求しない。

### OLS / difference-in-means — `NOT_APPLICABLE`

weight statistics/ESSを架空値で埋めない。`balance.before`は保存可、`balance.after = null`。

## 5. Extreme-weight rule — frozen

```text
extreme_rule = "weight > 10.0"
extreme_count = number of diagnosed arm weights satisfying weight > 10.0
```

- `weight == 10.0`はextremeではない。
- un-normalized arm-specific actual analysis weightへ適用。
- propensity clipping countを流用しない。
- thresholdをsilent変更しない。

## 6. Statistics semantics

Applicable arm weights:

- `count`: diagnosed arm row count
- `min`, `mean`, `max`: numeric summaries
- `p50`, `p95`, `p99`: NumPy-compatible linear quantiles
- undefined/non-applicable: null。NaN/Infinityをstable JSON fieldとしてpersistしない。

## 7. Frontend boundary

Frontendはpersisted structured fieldsをpresentationへ投影するだけとし、ESS、weights、quantiles、extreme_count、weighted balanceを再計算しない。`definition`/notes string parsingでscientific valuesを復元しない。利用不能項目はnot applicable/unavailableとして表示する。

Legacy top-level`balance`をmigration compatibilityで残す場合、それはunweighted before projectionとしてのみ扱い、new after-weight authorityにしない。

## 8. Protected semantics

- Treatment Effect estimate/uncertainty calculation
- ResultType
- Execution/Result lineage
- existing API route grammar
- Effects/Diagnostics Stage ownership
- propensity clipping behavior
- E8 Stage separation / Navigation Stage != Execution state

## 9. Forbidden

- fabricated weights/ESS
- AIPW whole-estimator final weight捏造
- propensity clipping countのextreme_count流用
- before→after copy
- frontend scientific recomputation/string parsing
- new ResultType / unnecessary route/persistence redesign
- Pxx内でGate claim/ACを変更

## 10. Work Packages

- P01: applicability contract + estimator/component exposure + extreme rule boundary
- P02: IPW actual-weight stats + treated/control ESS structured persistence
- P03: before/after balance + estimator applicability semantics
- P04: frontend structured consumption + compatibility/regression

各Pxxはassigned Coding Agentにとってself-contained normative contractでなければならず、parent 06/07/P00/other Pxxを仕様補完目的で参照させない。必要semantic fragmentはPxxへ明示的に複製する。

全Pxx complete後にCandidate Assemblyを行う。Pxx completionはGate PASSではない。

## 11. Browser E2E

G04 Package executionおよびG04 Independent VerificationではBrowser E2Eをnumeric/scientific proofとして実行しない。G04 correctnessはscientific/unit/backend integration/frontend integrationをprimary authorityとする。Integrated Browser E2EはG05 final verificationへ委譲する。
