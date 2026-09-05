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
  treated:
    count: <integer>
    min: <number>
    mean: <number>
    p50: <number>
    p95: <number>
    p99: <number>
    max: <number>
    extreme_count: <integer>
    extreme_rule: <string>
  control: <same fields>
```

`balance.before`はunweighted balance。`balance.after`は実際に定義されたweight/component weightによるbalanceのみを格納する。存在しない場合は`null`とし、beforeをafterへコピーしない。

### 4.1 IPW

`weighting.applicability = ESTIMATOR_WEIGHT`。ATE/ATTでestimatorが実際に用いるtreated/control arm weightを対象とする。ESSは各armについて `(sum w)^2 / sum(w^2)` とし、TreatmentEffectEstimatorがstandard-error計算に用いるESSと一致させる。

Current estimatorのweighted meanは各arm weightのsumでnormalizeしてcontrastを計算するため、`definition`に「arm-specific analysis weights; normalization occurs through weighted-mean denominator」を明示する。Combined one-vector final weightを捏造しない。

Extreme ruleはpropensity clippingとは別概念である。初期contractでは `weight > p99` 等のdata-relative ruleを固定せず、実装で採用するruleを06/07 fixtureと同時に明示する。ruleなしでextreme_countだけを保存してはならない。

### 4.2 AIPW

`weighting.applicability = PROPENSITY_COMPONENT`。AIPW estimator全体の単一final weightは存在するものとして表現しない。Propensity-derived componentについてscientifically definedなdiagnosticsを保存してよいが、IPWと同じweight distribution/ESSを機械的に要求しない。`balance.after`もcomponent definitionが明確な場合のみ保存する。

### 4.3 OLS / difference-in-means

`weighting.applicability = NOT_APPLICABLE`。weight statistics/ESSを架空値で埋めない。`balance.before`は利用可能、`balance.after = null`を許容する。

## 5. Compatibility

Result type、existing API route grammar、Treatment Effect payload semantics、Execution/Result lineageを変更しない。新field追加はbackward-compatible structured diagnostics extensionとして実施する。
