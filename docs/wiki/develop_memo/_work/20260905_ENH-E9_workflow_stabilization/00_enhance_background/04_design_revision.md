# ENH-E9 Design Revision

- Status: `FROZEN`
- Authority: current 21/22/23/30 canonical reference snapshot + this E9 delta

## 1. Design intent

E9はE8で確立したInformation Architecture、Stage responsibility、Navigation/Execution separation、Result/Execution lineageを維持し、residual usabilityとDiagnostics backend conformanceだけを修正する。

## 2. Protected invariants

- `Navigation Stage != Execution operation`
- Project Management / Analysis Workspace ownershipを混在させない
- Analysis View lifecycleはData側resource ownershipを維持する
- Discovery Result / Graph Candidate / DRAFT-FIXED GraphVersion mutability semanticsを維持する
- FIXED Graphを直接mutationしない
- Identification / Estimation / Effects / Diagnostics責務を維持する
- UI convenienceだけを理由にnew API route / persistence / runtime Stageを追加しない
- Frontendはpersisted Resultをauthorityとし、新しいcausal estimate/diagnosticを推測生成しない

## 3. Identification Outcome inheritance

Canonical termとして`Outcome one-way ownership`は使用しない。Protected behaviorは次とする。

```text
Discovery designated Outcome
  -> GraphVersion designated_outcome_node
  -> Identification Outcome: read-only / automatic inheritance / input不要
  -> selected Identification Result lineage
  -> Estimation
```

Treatment selector改善はこのOutcome inheritanceを変更しない。

## 4. Frozen DIAGNOSTICS_RESULT contract direction

既存payload top-levelの`sample_size`, `design`, `overlap`は互換維持する。`balance`と`weighting`を次の意味でstable structured contract化する。

```text
balance:
  before: <balance row list>
  after: <balance row list | null>
  after_applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE

weighting:
  applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE
  estimand: ATE | ATT | null
  definition: <human-readable machine-stable semantics string>
  effective_sample_size:
    treated: <number | null>
    control: <number | null>
  treated: <weight stats object | null>
  control: <weight stats object | null>
```

Applicable weight stats object:

```text
count: <integer>
min: <number>
mean: <number>
p50: <number>
p95: <number>
p99: <number>
max: <number>
extreme_count: <integer>
extreme_rule: "weight > 10.0"
```

`balance.before`はunweighted balance。`balance.after`は実際に定義されたweight/component weightによるbalanceのみを格納する。存在しない場合は`null`とし、beforeをafterへコピーしない。

### 4.1 IPW

`weighting.applicability = ESTIMATOR_WEIGHT`。ATE/ATTでestimatorが実際に用いるtreated/control arm weightを対象とする。

Current estimator semantics:

```text
ATE:
  treated arm: 1 / e(x)
  control arm: 1 / (1 - e(x))

ATT:
  treated arm: 1
  control arm: e(x) / (1 - e(x))
```

ここで`e(x)`はconfigured propensity clipping後のpropensity scoreである。Persist/distribution summaryの対象は各armのobserved rowsに対応するpositive analysis weightsだけとし、反対arm用のzero placeholderをstatisticsへ含めない。

ESSは各armについて `(sum w)^2 / sum(w^2)` とし、TreatmentEffectEstimatorがstandard-error計算に用いるESSと一致させる。

Current estimatorのweighted meanは各arm weightのsumでnormalizeしてcontrastを計算するため、`definition`には次のstable semanticsを表現する。

```text
arm-specific IPW analysis weights computed from clipped propensity scores; weighted means normalize by each arm's weight sum
```

Combined one-vector final weightを捏造しない。

### 4.2 Extreme-weight rule

E9の初期stable ruleを次へ固定する。

```text
extreme_rule = "weight > 10.0"
extreme_count = number of diagnosed arm weights satisfying weight > 10.0
```

- `weight == 10.0`はextremeに含めない。
- propensity score clipping countをextreme_countへ流用しない。
- thresholdはun-normalized arm-specific analysis weightに適用する。
- p95/p99等のdata-relative thresholdをextreme ruleとして使用しない。
- later threshold/configuration変更が必要なら別contract amendmentで扱い、silent変更しない。

### 4.3 AIPW

`weighting.applicability = PROPENSITY_COMPONENT`。AIPW estimator全体の単一final weightは存在するものとして表現しない。

AIPWについては、propensity-derived componentの意味をwhole-estimator final weightと混同しないことを優先する。E9では以下を許容する。

- `weighting.definition`でpropensity componentでありfinal estimator weightではないことを明記する。
- 科学的に一意に定義できるcomponent weight statisticsのみ保存する。
- whole-estimator treated/control ESSを生成しない。`effective_sample_size.treated/control = null`を許容する。
- component balanceを一意に定義・説明できない場合、`balance.after = null`とする。

AIPWへIPWと同じweight distribution/ESS/post-weight balanceを機械的に要求しない。

### 4.4 OLS / difference-in-means

`weighting.applicability = NOT_APPLICABLE`。

```text
weighting.estimand = <current estimand or null as payload convention requires>
weighting.effective_sample_size.treated = null
weighting.effective_sample_size.control = null
weighting.treated = null
weighting.control = null
balance.before = <unweighted rows>
balance.after = null
balance.after_applicability = NOT_APPLICABLE
```

weight statistics/ESSを架空値で埋めない。

## 5. Quantile/statistics semantics

Applicable arm weight statisticsはdiagnosed positive arm weightsから計算する。

- `count`: diagnosed arm row count
- `min`, `mean`, `max`: standard numeric summaries
- `p50`, `p95`, `p99`: NumPy-compatible linear quantile semantics（default `numpy.quantile` / `numpy.percentile` linear interpolation）
- all persisted numbers must be finite JSON-compatible values; undefined values are represented by `null`, not NaN/Infinity

Testsはproduction helperの結果をそのままexpected valueへ流用せず、known fixture weightsから独立計算する。

## 6. Compatibility

Result type、existing API route grammar、Treatment Effect payload semantics、Execution/Result lineageを変更しない。新field追加はbackward-compatible structured diagnostics extensionとして実施する。

Legacy top-level `balance` listをmigration compatibilityのため残す場合、それは`balance.before`のprojectionとしてのみ扱い、新しいpost-weight authorityにしない。
