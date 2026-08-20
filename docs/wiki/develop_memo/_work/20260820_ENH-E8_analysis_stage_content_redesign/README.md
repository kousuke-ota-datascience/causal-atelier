# ENH-E8 — 分析Stageコンテンツ構成の再設計

**Document class:** Enhancement Workflow Instance / Authoring Guide  
**Self-containment:** MUST  
**Workflow state:** `APPROVED/FROZEN`  
**Agent execution:** G01 contractはfreeze済み。実行開始前にrepository/worktree preflightを行う。G02 contractもfreeze済みだが、canonical G01 `999 PASS` が成立するまでdependency-blocked。

## 0. Identity

| 項目 | 値 |
|---|---|
| Project | Ariadne |
| Enhancement ID | `ENH-E8` |
| Working title | Analysis Stage Content Architecture Redesign |
| Baseline commit | `386521d18e9c5cc4d42fb99c97c212430908afc3` |
| Baseline branch | `prototype/ariadne_mvp` |
| Planned implementation branch | `feature/ariadne_mvp_e8` |
| Work root | `docs/wiki/develop_memo/_work/20260820_ENH-E8_analysis_stage_content_redesign` |
| Initial Trial | `01` |
| 使用言語 | 日本語を原則とする。専門用語、コード識別子、workflow status等は必要に応じて英語を維持する |

## 1. Enhancementの目的

ENH-E8 は、新しい分析アルゴリズム、API、persistence model、runtime execution stage、canonical Navigation Stage を追加しない。

目的は、既に承認されている Project Management / Analysis Workspace の責務を、frontendのInformation Architectureとpresentationで一貫して実現することである。

あわせて Predictive の特徴量入力を、カンマ区切りfree-text中心の操作から、**Dataset Versionのschemaを候補authorityとするpopup/dialog + checkbox複数選択**へ変更する。ただし `predictive-analysis-spec/1` の既存semanticsは変更しない。

Acceptance boundaryは2つとする。

1. **G01 — Project Return Navigation Contract**  
   Selected Project のどのlocal sectionからでも、browser historyの起点に依存せず、canonical Project List (`/projects`) へ明示的に遷移できる。
2. **G02 — Analysis Stage Content Architecture Contract**  
   Causal / Predictive の各 Navigation Stage が、そのStage固有の目的・操作・結果を主画面として提示し、別Stageの主surfaceをcurrent Stageとして誤提示しない。

## 2. Requirement revisionの判断

**New FR: NONE / New NFR: NONE / New AR: NONE**

ENH-E8 は既存Requirementへのdesign/implementation conformance enhancementである。

主なauthority:

- Predictive Navigation Stage: `FR-149`–`FR-152`
- Causal Navigation Stage: `FR-153`–`FR-156`
- Project/Analysis canonical navigation: `FR-163`, `FR-166`
- existing capability placement / UI-only compatibility boundary: `FR-174`, `FR-176`, `FR-177`
- navigation determinism / draft-state continuity: `NFR-022`, `NFR-026` 等
- Predictive feature-set semantics: 既存Predictive requirement（`FR-055`, `FR-057` 等）

`00_enhance_background/03_requirements_revision.md` を、「Requirement semantic deltaなし」の判断authorityとする。

## 3. Gate構成

| Gate | Semantic claim | Mode | Dependency |
|---|---|---|---|
| `G01` | Selected ProjectにProject Listへの明示的canonical parent navigationがある | `SINGLE_EXECUTION` | baselineのみ |
| `G02` | Analysis WorkspaceのStage ContentsがCausal/Predictive各Stage固有の意味を実現する | `WORK_PACKAGE` | `G01` final PASS |

G02 Work Package:

```text
P01 analysis_stage_presentation_framework
  -> P02 causal_stage_surface_separation
  -> P03 predictive_stage_surface_separation
  -> Candidate Assembly
  -> Independent Verification
```

`PACKAGE_COMPLETE` はGate PASSではない。Trial番号は、Fixed Trial Candidateに対するformal Independent Verificationが `FAIL` した場合にのみ次へ進める。

## 4. Core Design Invariant

- `E8-DI-01` Selected ProjectはProject Listへの明示的parent navigationを持つ。
- `E8-DI-02` Stage Contentsのprimary identityはcurrent canonical Navigation Stageである。
- `E8-DI-03` Stage固有のmain operation/result surfaceはそのStageが所有し、cross-stage情報はcompactなprerequisite/referenceに限定する。
- `E8-DI-04` Causalのpresentation groupingを導入しても、route / Navigation Stage / runtime Stage / persistent stateにはしない。
- `E8-DI-05` CausalのIdentification / Estimation / Effects / Diagnostics / Sensitivityの責務を分離する。
- `E8-DI-06` PredictiveのSetup / Train / Predict / Metrics / Explainability / Model Managementの責務を分離し、既存 `predictive-analysis-spec/1` semanticsを維持する。
- `E8-DI-07` 主要semantic sectionは縦方向のreading flowを基本とする。compactな関連controlにはlocal gridを許可し、table/chartにはcomponent-local overflowを許可する。
- `E8-DI-08` UI/IA変更によってcanonical Stage catalog、API、DB/persistence、backend analysis semantics、runtime lifecycleを変更しない。
- `E8-DI-09` Predictiveのfeature selectionはSetupでDataset-schema-backed popup/checkbox selectorにより編集する。Train/Predictでは該当feature setをread-only表示し、submission contractは既存 `feature_spec.feature_columns` を維持する。

## 5. Authority model

```text
00 background / design revision
  = なぜ変更するか、承認済みdesign basis

06 Gate Coding Contract
  = 実装が何を成立させる必要があるか

07 Gate Verification Contract
  = Acceptance Criteria authority

Pxx
  = Coding Agentのbounded execution contract

20 reports
  = implementation evidence
  != acceptance authority

30 reports / 999 Gate Decision
  = Independent Verification evidence + final Gate authority
```

Coding Agentはassigned contractの不足を補うために他workflow文書を探索してはならない。不足があれば推測実装せずcontract ambiguityとして停止する。

## 6. Baselineで確認済みの実装事実

- `frontend/project_navigation.js` はcollection route `/projects` を既にserializeできる。G01は新route追加ではなくUI/navigation wiringである。
- `frontend/analysis_presentation.js` はCausalの `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` をlegacy `inference` workspaceへbindしている。
- `frontend/index.html` にはvisibleな `Inference` headingとshared `Effects / Diagnostics` cardがある。
- Predictiveには一部Stage-specific fieldsetがある一方、複数Stageで同一Result presentationが共有されている。
- Predictive `feature_columns` はfree-text入力である一方、Causal DiscoveryはDataset schema由来のdialog/checkbox selectorを既に持つ。E8ではinteractionを揃えるがanalytical specificationは変えない。

これらはevidence/provenanceであり、新規Requirementではない。

## 7. 実行順序

1. Humanが `00_enhance_background/*` とrevised design snapshotをreviewする。
2. `G01/06` と `G01/07` をfreezeし、preflightを実行する。
3. G01 Trial01を実装し、Independent Verification後にcanonical `999` decisionを発行する。
4. G01 PASS後のみG02へ進む。
5. G02は P01 → P02 → P03 を実行し、Candidate Assemblyで1つのFixed Trial Candidateを作り、Independent Verification後にcanonical `999` decisionを発行する。
6. formal FAIL時のみ `08` remediation contractを作る。06/07自体のsemantic defectは `09` Gate Contract Amendmentで扱う。

## 8. Freeze後の実行前確認

Coding Agent実行前にHuman operatorが確認する。

- [x] G01/G02のsemantic claimとpackage splitを承認した。
- [x] `22_product_basic_design.md` のE8変更を承認した。
- [x] Detailed Designは、baseline commit `386521d...` のapproved canonical snapshotと本workflow内のapproved E8 addendumを一体のimmutable composite effective snapshotとしてfreezeした。
- [x] applicableな各 `07` にcanonical Browser E2E command/environmentをfreezeした。
- [ ] 実repository/worktree上で `40_operator_workflows/preflight/AGENT_EXECUTION_READINESS.md` のexecution-time項目を完了する。

## 9. Directory map

`TEMPLATE_STRUCTURE.md` を参照する。README命名は `README_NAMING_CONVENTION.md` に従う。
