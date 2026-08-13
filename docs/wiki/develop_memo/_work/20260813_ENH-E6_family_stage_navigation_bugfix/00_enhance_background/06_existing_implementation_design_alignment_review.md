# ENH-E6 Existing Implementation / Design Alignment Review

- Status: `COMPLETE_SOURCE_INSPECTION / RUNTIME_REPRODUCTION_PENDING`
- Baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`

## 1. Evidence inventory

| Evidence | Observed fact |
|---|---|
| `frontend/index.html` | `analysis-family-tabs`, `analysis-stage-sidebar`, `causal-stage-presentation` が存在 |
| `frontend/index.html` | legacy navに `Causal Discovery` (`data-workspace=discovery`, `data-route=causal`) と `Causal Inference` (`data-workspace=inference`, `data-route=causal`) が並存 |
| `frontend/app.js` | `ANALYSIS_WORKSPACES={exploratory:'explore', predictive:'predictive', causal:'discovery'}` |
| `frontend/app.js` | `activateWorkspace()` が workspace active state とhistory/navigationContextを操作 |
| `frontend/app.js` | canonical `restoreProjectRoute()` は `renderAnalysisNavigation()` を呼ぶ |
| `frontend/app.js` | Family/Stage button handler はhistory push後に `restoreProjectRoute()` を呼ぶ |
| `frontend/app.js` | `renderAnalysisNavigation()` は catalog Family / current stages をrender |
| `tests/product/test_enh_e5_g01_navigation_shell.py` | Family tabs testにHTML/JS source string inspectionが存在 |
| ENH-E5 G01 P02 | Family tabs / Family-local sidebar / `(AnalysisFamily, navigation_stage_id)` presentation bindingを要求 |
| ENH-E5 G01 07 | browser layerでFamily click/default Stage/sidebar/deep link/reload/back-forwardを検証するarchitectureを要求 |
| ENH-E5 technical debt | `ANOM-E5-001` がfresh environment reproduction、actual UI、real Family tab operation、legacy nav boundaryをfuture evidenceとして要求 |

## 2. Alignment classification

### MATCH

- Family/Stage catalog model
- canonical route parse/serialize concept
- Family tab DOM shell
- catalog-driven tab/sidebar rendering logic
- Family/Stage button event handler existence

### PARTIAL / DEFECT

#### A-001 — Normal transition does not guarantee shell render

`activateWorkspace()` と `restoreProjectRoute()` の責務が非対称。Navigation Context/URLを変更するnormal pathがrender lifecycleへ収束していない。

#### A-002 — Family-only presentation selection

canonical route restore後の workspace activationが `ANALYSIS_WORKSPACES[familySlug]`。Causal全Stageが`discovery` surfaceへ固定され、`inference` workspaceとのStage-aware bindingがない。

#### A-003 — Legacy analytical nav has dual role

legacy nav buttonが workspace activationとroute semanticsの両方を持つ。Causal Discovery / Inferenceが同じ`data-route=causal`を持つため、NavigationContext defaultingとvisual workspace selectionが競合し得る。

#### A-004 — Test coverage mismatch

source contract inspectionは部品の存在を確認するが、normal entryでFamily tabがobservableかを保証しない。E5 07が要求したbrowser journeyをE6ではblocking evidenceへ引き上げる。

## 3. Root cause

### Direct cause

normal entry transitionが canonical analysis navigation renderer lifecycleを必ず通る設計になっていない。

### Structural root cause

`NavigationContext apply` がfirst-class operationとして設計されず、workspace selection、history、route restore、tab render、presentation selectionが別関数へ分散している。

### Process root cause

observable Family tab journeyをacceptanceのblocking proofとして固定できず、「実装要素の存在」と「ユーザーが操作可能」を区別できなかった。

## 4. Runtime reproduction status

本Planning Agent環境ではrepository clone / local stack起動が外向きDNS制限により実施できなかった。したがって actual browser screenshot / computed DOM visibility は未採証。

Gate coding開始前にHuman/local execution environmentで次をpreflightする。

1. baseline SHAをcheckout
2. fresh stack起動
3. Project選択
4. legacy/normal analysis entryをclick
5. reload前の Family tabs DOM child count / visibility / selected state / URLを記録
6. canonical URL direct open時との比較を記録

preflight結果がsource-derived hypothesisと異なる場合は、06/07 freeze前に本reviewをamendする。
