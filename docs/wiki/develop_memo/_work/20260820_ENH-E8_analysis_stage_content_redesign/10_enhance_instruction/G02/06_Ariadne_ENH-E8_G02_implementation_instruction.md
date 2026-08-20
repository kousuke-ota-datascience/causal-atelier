# Ariadne ENH-E8 G02 Implementation Contract

- Document class: Primary Execution Contract
- Contract status: `FROZEN`
- Status: `FROZEN`
- Gate: `G02`
- Execution Mode: `WORK_PACKAGE`
- Baseline: `386521d18e9c5cc4d42fb99c97c212430908afc3`
- Entry prerequisite: canonical G01 `999` = PASS

## 1. Gate claim

current canonical Navigation StageをAnalysis Stage Contentsのprimary identityとし、Causal/Predictiveのpresentation responsibilityを分離する。

Predictive Setupでは、Dataset-schema-backed popup/dialog + checkbox multi-selectionによりfeature columnを選択できるようにし、existing Predictive analytical specification / validation semanticsを維持する。

## 2. Mandatory invariant

- canonical Stage catalog / routeを維持する。
- presentation groupingをroute/stage/runtime/persistent authorityにしない。
- Causal Identification / Estimation / Effects / Diagnostics / Sensitivityのmain surfaceを分離する。
- Sensitivity/Refutation controlはSensitivityのみが所有する。
- Predictive Setup / Train / Predict / Metrics / Explainability / Model Managementの責務を分離する。
- Predictive feature-column編集はSetupのみが所有し、selected Dataset Version schemaをcandidate authorityとする。
- Train/Predictでは該当feature setをread-only表示し、ad-hoc feature editingを提供しない。
- selector Confirmはexisting `predictive-analysis-spec/1 -> feature_spec.feature_columns` semanticsへmappingする。
- selector導入によってfeature validation、availability cutoff、target/excluded-column、split、model、execution semanticsを変えない。
- valid Predictive draftをStage切替で失わない。
- Causal Discovery selectorをshare/generalizeする場合、existing behaviorをprotected regressionとする。
- major semantic sectionは縦方向reading flowとする。
- LightGBM/LIME/SHAPをE8で実装しない。
- API/DB/backend/runtime semanticsを変更しない。

## 3. Package execution

`06_G02_P00_work_package_plan.md` に従う。

各Pxxはassigned Coding Agentに対してself-contained normative contextである。Agentは他workflow docを読んでassigned contractの不足を補ってはならない。

## 4. Candidate Assembly

P01/P02/P03 completion後、1つのintegrated Fixed Trial Candidateを組み立てる。

package-integrated/protected regressionを実行し、Implementation Completion Reportでcandidate identityを固定する。

`READY_FOR_TEST` はGate PASSではない。
