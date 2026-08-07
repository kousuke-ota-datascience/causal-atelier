# ENH-E3 G3 Trial 001 Implementation Completion Report

- Gate: G3 — Predictive Specification + Split
- Trial: 001
- Status: READY_FOR_TEST
- Implementation base commit: `f4faffc0afdec2abc6b0952bd4762952774de92a`
- Implementation completed commit: `73a92c1b5899bc0d072df0faf8621b5171b00e5a`
- Handoff report commit: 省略（本報告commit自身を自己参照できないため）
- Migration head: `20260807_product_0004`
- Test execution by Coding Agent: NOT PERFORMED

## 1. Working tree summary

implementation commit直後のtracked working treeはcleanである。

未追跡のcontrol documentとして以下の2ファイルが存在するが、implementation commitにはstageしていない。

- `00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`
- `00_enhance_plan_documents/07b_Ariadne_ENH-E3_テスト指示書.md`

## 2. Implemented scope

- `predictive-analysis-spec/1`のtop-levelおよび既知nested fieldをstrict validationした。
- `BINARY_CLASSIFICATION` / `REGRESSION`とtask-compatible metricを検証した。
- feature availability descriptorへ任意の`derived_from`を追加し、target derivativeを明示的かつ機械可読にreject可能にした。
- target、future availability、group key、partition overlap、group intersection、population mismatch、non-TRAIN fit、TEST selection leakageを専用code/path付きでrejectした。
- RANDOM / STRATIFIED / GROUP / TIME_BASED splitのstrategy、ratio、seed、target/group/time値を厳密化した。
- Binary Classification source targetの2 class制約と欠損拒否をsplit runnerで検証した。
- partition artifactへrow ordinal、counts、class/group/time summary、source snapshot/hash、specification hash、TEST isolation contractを保持した。
- split生成を`PredictivePlanner -> GenericExecutor -> predictive.split.v1 runner`経由に維持した。
- Generic Executorがfamily非依存にexceptionの`code` / `path` metadataをStage failureへ保持するようにした。
- split runner内のvalidation failureをAPIのHTTP 422 machine-readable errorへ復元した。
- Dataset Version / optional Analysis View -> Execution -> Artifact lineageのautomated test contractを追加した。
- capabilitiesはG3 split-onlyおよび`training_available=false`を維持した。
- G3用のmigrationは追加していない。

## 3. Changed production files

- `src/ariadne/capabilities/predictive/split_runner.py`
- `src/ariadne/capabilities/predictive/splitting.py`
- `src/ariadne/capabilities/predictive/validation.py`
- `src/ariadne/interfaces/web_api/routers/predictive.py`
- `src/ariadne/product/application/predictive_split_service.py`
- `src/ariadne/product/workflow/executor.py`

## 4. Changed test files

- `tests/product/test_predictive_leakage_e3.py`
- `tests/product/test_predictive_spec_e3.py`
- `tests/product/test_predictive_split_api_e3.py`
- `tests/product/test_predictive_split_e3.py`

## 5. Added migration

なし。既存のgeneric persistenceとmigration head `20260807_product_0004`を使用する。

## 6. Architecture guard check

- Product DomainからWeb Framework / ORM / ML library / legacy packageへの依存追加なし。
- Product / Web APIから`ariadne.legacy`への依存追加なし。
- family-specific validationは`capabilities/predictive`に保持した。
- Generic ExecutorへPredictive固有のif/elifを追加していない。
- Generic Executorの変更は、任意exceptionが持つ`code` / `path`をfamily非依存にfailure metadataへ保存する処理だけである。
- Plannerは実行せず、一段のimmutable split planを構築する。
- canonical JSON validationによりNaN / Infinity / external objectのSpecification保存を拒否する。
- model fitting、Training、Evaluation、Explain、Predictive UIは追加していない。

### G1/G2確定ファイルの変更

- 変更ファイル: `src/ariadne/product/workflow/executor.py`
- 不可避な理由: runner内で検出されたG3専用validation errorのmachine-readable code/pathを、Generic Executor境界を越えてAPIへ返す必要があるため。
- 既存契約を変えていない根拠: 既存の`type` / `message`はそのまま保持し、exceptionに属性が存在する場合だけmetadata fieldをadditiveに追加する。Family分岐、retry、commit、compensation、stage status遷移は変更していない。
- Test Agent回帰範囲: Generic Workflow Core、Causal workflow regression、Exploratory execution/API worker。

## 7. Known deviations

implementation base commit `f4faffc0afdec2abc6b0952bd4762952774de92a`には、本trial開始前から以下のG3完成物外ファイルが履歴上含まれていた。

- `src/ariadne/capabilities/predictive/metrics.py`
- `src/ariadne/product/domain/research_context.py`
- `src/ariadne/product/domain/lineage.py`
- 承認文書・inventory等

本trialでは履歴改変または削除を行わず、上記ファイルを変更・stageしていない。implementation commit `73a92c1b5899bc0d072df0faf8621b5171b00e5a`の変更対象はG3 production/test codeだけである。

## 8. Known limitations

- G3はSpecification保存共通lifecycleを実装しない。split validation executionはfamily specification snapshotを既存generic execution persistenceへ保存する。
- `preprocessing_spec` / `model_spec` / `tuning_spec` / `explanation_spec`はG3ではopaque JSON envelopeとして保持し、実行しない。
- Test Agentによる独立監査前であり、Gate G3のDecisionは未作成である。

## 9. Files intentionally excluded

- `src/ariadne/capabilities/predictive/metrics.py`
- `src/ariadne/product/domain/research_context.py`
- `src/ariadne/product/domain/lineage.py`
- `00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`
- `00_enhance_plan_documents/07b_Ariadne_ENH-E3_テスト指示書.md`
- 承認文書backup、`document_inventory.json`、G4以降のdraft

## 10. Required Test Agent focus

- canonical G3 test files 4件の全contract
- unknown/missing/duplicate field、task/metric、target derivative、future/group leakage
- 4 split strategyの決定性、partition overlap/union、group intersection、temporal boundary
- split runner failureのHTTP 422 `code` / `details.path`保持
- Dataset VersionおよびFIXED Analysis Viewからのsource hashとlineage
- `PREDICTIVE` Family Execution、`predictive.split.v1` Stage、`PARTITION_INDEX` Artifact persistence
- TESTの`selection_allowed=false` / `final_evaluation_only=true`
- Generic Workflow Core、Causal、Exploratoryに対する`executor.py`変更の回帰
- full active suiteおよび必要なPostgreSQL contract

## 11. Coding Agent decision

`READY_FOR_TEST`。Coding AgentはGate Decisionを判定していない。
