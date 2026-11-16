# 10_02_use_cases_e2e


---

## 4. E2Eシナリオ

| ID | シナリオ | 完了条件 |
| --- | --- | --- |
| E2E-01 | Research Workspaceを作成する | ProjectとResearch Contextを作成し、Dataset Versionを登録してProject-global surfaceと三つのAnalytical Familyへ遷移できる |
| E2E-02 | 探索・可視化を保存する | Datasetの品質・分布・関連を確認し、ChartとAnalysis Viewを保存できる |
| E2E-03 | 探索から分析draftを作る | 探索ResultからCausalまたはPredictive Specification draftを作成し、source relationを保持できる |
| E2E-04 | 因果効果を評価する | Graph、Question、Design、Identification、Eligibility、Estimation、Diagnostics、Refutation、Sensitivityを実行できる |
| E2E-05 | 分類モデルを評価する | Binary Classificationをsplit、train、evaluate、explainし、test isolationを確認できる |
| E2E-06 | 回帰モデルを評価する | Regressionをsplit、train、evaluate、error analysisし、複数modelを比較できる |
| E2E-07 | 条件変更を比較する | base ExecutionからRERUNまたはREVISEDを作成し、changed dimensionsと結果差分を確認できる |
| E2E-08 | 横断来歴を確認する | ReviewerがResearch ContextからExploratory、Causal、PredictiveのResultと判断理由へ遡れる |
| E2E-09 | Analysis Familyを横断する | Family tabでExploratory / Predictive / Causalを切り替え、selected FamilyのNavigation Stageだけを左navigationから選択できる |
| E2E-10 | UIを経由せずanalysisを実行する | CLI / Python library / backend use caseからCurrent Navigation Stageを指定せず既存analysis executionを開始できる |
| E2E-11 | Project resourceを管理する | Project List / RegisterからProjectを選択し、Overview / Research Context / Data / Resultsへroute-backedに遷移できる |
| E2E-12 | Analysis Workspaceでcontextを保持して分析する | Current Projectをread-onlyで確認し、Research Context / Dataset Version / Analysis Viewを選択してFamily / Stageを操作でき、context変更だけでFamily / Stage routeが失われない |

### 4.1. E2E共通受入条件

- Command受付時にProject権限、Resource状態、SchemaおよびFamily固有validationが実行される
- すべてのExecutionがResearch Context Version、Dataset VersionまたはAnalysis Viewを固定する
- ResultとArtifactがExecution / Stageへ紐付く
- UI表示とAPI payloadが同じ保存済み正本を参照する
- 失敗時にtechnical failure、validation rejection、analytical negative resultを区別する
- Navigation Stageの存在・順序をruntime Execution Stageやworkflow completionへ読み替えない
