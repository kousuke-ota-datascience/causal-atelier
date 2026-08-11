# ENH-E5 Architecture Discovery Prompt（アーキテクチャ調査プロンプト）

文書区分: Operator Artifact（運用資料）

## Objective

G00 freeze前に、Family/Navigation Stage ownershipに関係するcurrent `feature/ariadne_mvp_e5`の実装surfaceを確認する。

## Required observations

### Domain / workflow
Inspect:
- `src/ariadne/product/domain/enums.py` — AnalysisFamily
- `src/ariadne/product/domain/execution_plan.py` — StageType / StageDefinition
- `src/ariadne/product/domain/stage_execution.py` — StageExecution lifecycle
- `src/ariadne/product/workflow/` — planner/runner abstractions
- `src/ariadne/capabilities/{exploratory,predictive,causal}/`

Questions:
1. `AnalysisFamily`は現在もEXPLORATORY/CAUSAL/PREDICTIVEの3値であるか。
2. Execution Stage abstractionはgenericかつlifecycle-orientedであるか。
3. concrete execution plan Stage定義をcapability plannerが所有しているか。
4. target designを重複実装にする既存navigation descriptor modelが存在しないか。

### Frontend
Inspect:
- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

Inventory:
- 現行sidebarの全workspace/route;
- 現行analytical route parsing/history挙動;
- workspace-state fields;
- Predictiveの全visible control;
- Causal Discovery/Inference/Refutation/Sensitivityの全control/result;
- Exploreの全operation/chart/saved-result surface。

### Persistence/API
Family/Stage navigationが現在どこかへ永続化されているか、およびdescriptor endpointが既に存在するかを確認する。

## 既知のplanning観測事項（鵜呑みにせず検証する）

- AnalysisFamily values exist.
- Execution `StageType`/`StageDefinition`/`StageExecution`は別々に存在する。
- frontendでは現在global navigationとanalytical navigationが1つのsidebarに混在している。
- `/workspace-state`はresearch context/dataset/viewを永続化しているように見え、Family/Stageは対象外とみられる。
- Predictive full planはexecution Stageとしてsplit/prepare/train/evaluate/(explain)を使っており、desired Navigation Stageと1対1ではないことを示している。

## 必須出力

Record:
- exact local baseline SHAが`46122c68333df03680b97c253a7b5d32bf9393e7`と一致することを確認する;
- file/path inventory;
- known observationとの矛盾;
- architecture blockers;
- target ADRを変更なしでapprove可能か。

ownership/persistence factに重大な相違がある場合は`BLOCKED_ARCHITECTURE_REVIEW`とし、G00 freeze前にADRを改定する。
