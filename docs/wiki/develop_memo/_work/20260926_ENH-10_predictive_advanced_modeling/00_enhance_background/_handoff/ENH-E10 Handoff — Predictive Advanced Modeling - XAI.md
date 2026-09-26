# ENH-E10 申し送り事項 — Predictive Advanced Modeling / XAI

- 文書状態: `HANDOFF_DRAFT`
- Enhancement ID: `ENH-E10`
- 仮称: `Predictive Advanced Modeling / XAI`
- 旧番号: `ENH-E9`
- 上流 Enhancement:
  - `ENH-E8 Analysis Stage Content Architecture Redesign`
  - operationally `ENH-E9 Post-E8 Workflow Stabilization`
- 最低開始条件:
  - ENH-E9 final PASS
- Baseline SHA:
  - **ENH-E10 kickoff 時点の latest accepted mainline SHA を固定する**
- historical input:
  - `20260820_ENH-E9_handoff_predictive_advanced_modeling_xai.md`

---

# 1. 結論

ENH-E10 は Predictive Analysis に advanced model / explanation capability を追加する独立 Enhancement とする。

対象:

1. LightGBM
   - Binary Classification
   - Regression
2. SHAP
3. LIME

ENH-E8 / E9 の usability correction と混ぜない。

E10 は:

- model backend
- fitted-model artifact
- prediction adapter
- explanation backend
- method compatibility
- optional dependency
- reproducibility
- provenance

を拡張する analytical capability enhancement である。

---

# 2. Re-numbering rule

historical handoff は `ENH-E9` として作成されている。

本Projectではその内容を:

> `ENH-E10 Predictive Advanced Modeling / XAI`

へ rebase する。

historical file内の旧番号は provenance として扱い、current Enhancement ID の authority にしない。

---

# 3. Upstream protected contracts

## ENH-E8

Predictive Navigation Stage:

- setup
- train
- predict
- metrics
- explainability
- model-management

Stage responsibility separationを維持する。

feature set editing は Setup が所有する。

Train / Predictではtraining feature setをread-only referenceとして扱う。

Dataset-schema-backed feature selection semanticsを維持する。

## ENH-E9

E9の workflow stabilization を壊さない。

E10の capability追加を理由に:

- Project Management
- Causal workflow
- Graph workflow
- Identification UX
- Causal diagnostics

を変更しない。

---

# 4. Current starting point hypothesis

E10 kickoff 時に必ず current baseline で再確認する。

historical baselineでは Model Registry は実質:

- `logistic_regression.v1`
- `linear_regression.v1`

Predictive explanation は:

- `LINEAR_COEFFICIENT_CONTRIBUTION`

中心だった。

E10ではこの architecture を generalize する。

ただし historical implementation fact を current baseline truth として流用しない。

---

# 5. Requirement revision

E10 kickoff の最初の重要判断。

## 5.1 External analytical engine scope

current requirementには external analytical engine を **mandatory dependency として追加しない**という制約がある。

したがって推奨原則:

```text
core Ariadne
    +
optional predictive-advanced dependency group
```

LightGBM / SHAP / LIME 未導入時:

- Ariadne全体を起動不能にしない。
- method/model選択時に明示的 capability error。
- silent fallback禁止。
- package/version availabilityを明示。

## 5.2 Named capability

LightGBM / SHAP / LIME は E10 の目的そのものなので、Enhancement acceptance authorityでは具体名を明示する。

Requirementで具体名をMUSTにするか、

> general registry extensibility requirement + E10 acceptance concretization

とするかはfreeze時に決める。

---

# 6. Architecture Review — 必須

Coding前に少なくとも以下をfreezeする。

1. Model capability interface
2. Model Registry semantics
3. fitted-model Artifact format/version
4. prediction adapter interface
5. Explanation Method capability interface
6. model × explanation compatibility
7. global / local explanation capability
8. optional dependency lifecycle
9. package/runtime provenance
10. deterministic seed policy
11. failure taxonomy
12. backward compatibility

---

# 7. G01 — Predictive Model Backend Contract

Acceptance claim:

> Ariadneが既存linear modelを壊さず、Binary Classification / RegressionでLightGBMをregistryから選択し、train → artifact → load → predict → provenance確認まで一貫して実行できる。

対象:

- LightGBM classifier
- LightGBM regressor
- registry integration
- parameter schema
- task compatibility
- model serialization
- model loading
- prediction
- feature identity/order
- optional dependency
- Model Card / provenance

---

# 8. LightGBM design decisions

freeze対象:

- model ID/version naming
- classification/regression compatibility
- parameter schema
- defaults
- random seed
- deterministic settings
- early stoppingをscopeに入れるか
- categorical feature handling
- missing value responsibility
- existing preprocessing vs native LightGBM handling
- fitted booster serialization
- feature order preservation
- feature name preservation
- package version metadata

禁止:

> frontendのmodel optionだけ追加し、backendでは既存linear model formatとして偽装する。

---

# 9. G02 — Predictive Explanation Backend Contract

Acceptance claim:

> model capabilityに応じて explanation methodを選択でき、SHAP / LIME / existing coefficient explanation の方法論差を保ったままResult / Artifactとして生成できる。

推奨 registry:

| Method | Global | Local | Compatibility |
|---|---:|---:|---|
| Linear coefficient contribution | Yes | Yes | linear |
| SHAP | Yes | Yes | capability-based |
| LIME | No / explicit | Yes | prediction-function based |

すべての explanation method に同じ output capability を強制しない。

---

# 10. SHAP decisions

freeze:

- TreeSHAP を LightGBM primary path にするか
- linear model SHAP support
- background/reference dataset
- global aggregation
- local explanation identity
- binary classification output scale
- regression output scale
- expected value
- additivity metadata
- artifact/result schema
- package version

MulticlassはE10 scope外。

---

# 11. LIME decisions

freeze:

- local explanation専用とするか
- perturbation policy
- discretization
- random seed
- number of samples
- number of features
- classification explain target
- regression explain target
- preprocessing前後のfeature representation
- reproducibility expectation

global explanationを提供しない場合、それを明示contractとする。

---

# 12. G03 — Predictive Product Integration Contract

Acceptance claim:

> Train / Explainability / Model Management が追加backend capabilityを適切に選択・表示し、E8で確立したStage responsibilityとexisting predictive workflowを壊さない。

対象:

- Train model selector
- model parameter presentation
- Explainability method selector
- compatibility feedback
- Result rendering
- Artifact references
- Model Card
- full browser journey

Protected:

- Setup feature editing ownership
- Train/Predict read-only feature identity
- TEST isolation
- predictive-vs-causal terminology
- existing `predictive-analysis-spec` compatibility unless explicit version revision

---

# 13. Scientific / reproducibility verification

## LightGBM

- classification synthetic data
- regression synthetic data
- deterministic seed
- task mismatch
- invalid parameter
- train→serialize→load→predict parity
- feature order mismatch rejection
- optional dependency unavailable
- model/version provenance
- logistic/linear regression protected regression

## SHAP

- LightGBM classification
- LightGBM regression
- global
- local
- feature mapping
- config-stable output
- output scale
- unsupported combination

## LIME

- classification local
- regression local
- fixed-seed reproducibility
- instance identity
- feature representation
- unsupported global request

## Cross-cutting

- TEST partition isolation
- preprocessing leakage prevention
- Result / Artifact lineage
- Model Card
- Predictive Explanation terminology
- browser workflow

---

# 14. Explicit non-goals

E10へ含めない。

- multiclass classification
- survival
- forecasting
- ranking
- recommendation
- deployment API
- online inference
- production model monitoring
- AutoML
- production model registry platform
- causal explanation
- causal interpretation of SHAP/LIME
- CATE / HTE
- EconML
- Causal Lifecycle changes

---

# 15. Open decisions

1. LightGBM / SHAP / LIME dependency group構成
2. package version bounds
3. categorical support
4. missing-value responsibility
5. SHAP output scale
6. LIME local-only contract
7. predictive specification schema version
8. model artifact schema version
9. backend capability metadata API
10. browser acceptance environment

---

# 16. Start checklist

- [ ] ENH-E9 final PASS
- [ ] latest accepted SHAをE10 baselineとして固定
- [ ] historical ENH-E9 handoffをE10 historical inputとして宣言
- [ ] current Predictive model/explanation implementation inventory
- [ ] current requirement snapshot確認
- [ ] external engine scope revision判断
- [ ] Architecture Review
- [ ] optional dependency policy
- [ ] compatibility matrix
- [ ] G01/G02/G03 semantic boundary freeze
- [ ] deterministic fixtures
- [ ] 06/07 self-contained化

---

# 17. Primary source paths

Requirements/design:

- `docs/wiki/requirement_definition/10_requirements_definition.md`
- `docs/wiki/requirement_definition/22_product_basic_design.md`
- `docs/wiki/requirement_definition/23_api_interface_design.md`
- `docs/wiki/requirement_definition/30_detailed_design.md`

Predictive implementation:

- `src/ariadne/capabilities/predictive/`
- model registry / modeling
- explanation runner
- artifact handling
- model card
- predictive API/application
- predictive frontend
- tests

Historical:

- original `ENH-E9 Predictive Advanced Modeling / XAI` handoff

---

# 18. 最初の作業

Codingから始めない。

最初に:

> current baseline の model / explanation capability inventory を作成し、historical handoffとの差分を確定する。

その後:

> Requirement revision + Architecture Review をfreezeする。

LightGBM実装はその後。