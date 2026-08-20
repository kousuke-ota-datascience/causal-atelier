# ENH-E8 Enhancement Concept / Requirement Revision Plan

- Status: `APPROVED`
- Baseline: `386521d18e9c5cc4d42fb99c97c212430908afc3`

## 1. 目的

Ariadneのfrontend Information Architectureを是正し、Project ManagementからProject Listへ戻る明示的導線と、Analysis WorkspaceにおけるCausal/Predictive各Navigation Stage固有の画面責務を成立させる。

追加で、Predictiveの特徴量選択を、free-text中心の入力からDataset-schema-backed popup/dialog + checkbox複数選択へ変更する。これは入力interactionの再設計であり、Predictive analytical semanticsの変更ではない。

## 2. 現状課題

1. Selected ProjectからProject Listへ戻る明示的操作がない。
2. CausalのIdentification/Estimation/Effects/Diagnostics/Sensitivityがlegacy `Inference` workspaceに束ねられ、current Stage identityが弱い。
3. Causalで複数Stageの責務を共有するsurfaceがあり、Stageの目的が混在している。
4. 各Stageの日本語説明が不足し、他Stageのcontentが過剰に共通表示される。
5. Predictiveは一部Stage-specific入力を持つが、result surfaceの共有が大きくStage目的が不明瞭。
6. Predictive `feature_columns` はカンマ区切りfree-textである一方、選択Dataset Versionはschemaを持ち、Causal Discoveryにはschema-backed checkbox selectorが既に存在する。
7. 独立semantic sectionが横方向に密集し、可読性が低い。

## 3. Requirement revision判断

「変更があるため新規FR/NFRが必要」という判断は採用しない。

今回の要求は既存Product Concept / FR / NFRで既に要求されている能力のdesign/implementation conformance gapである。

Predictive feature selectorも、既存feature-set capabilityの入力interaction変更であるため、新規FR/NFRを作らない。

## 4. Design revision予定

- `22_product_basic_design.md`
  - Selected Project parent navigation
  - current Stage identity
  - Causal/Predictive responsibility matrix
  - Predictive feature selector interaction
  - presentation-only grouping
  - vertical semantic layout
- `30_detailed_design.md`
  - DOM/presentation binding
  - visibility matrix
  - Predictive selector state/interaction
  - draft preservation
  - navigation/history
  - layout/overflow
  - test seam
- `00`, `10`, `21`, `23`
  - semantic changeなし。provenanceのためsnapshotへ保持する。

## 5. Predictive feature selector設計意図

- 編集owner: Predictive `Setup`
- candidate authority: currently selected Dataset Versionのschema
- interaction: dialog open → checkbox multi-select → Confirm / Cancel
- Confirm後のcanonical value: 既存 `feature_spec.feature_columns`
- Train: selected draft/spec feature setをread-only表示
- Predict: selected/existing execution specificationのfeature setをread-only表示
- Dataset Version変更: 新schemaに存在しないfeatureをsilentに保持しない
- existing validationをauthorityとして維持
- Causal Discovery selectorを共通化する場合はDiscoveryをprotected regressionとする

## 6. Non-goals

- API変更
- persistence/schema変更
- backend analytical semantics変更
- runtime StageType / Execution lifecycle変更
- canonical Navigation Stage catalog変更
- LightGBM / LIME / SHAP追加
- historical causal lifecycle capability expansion
