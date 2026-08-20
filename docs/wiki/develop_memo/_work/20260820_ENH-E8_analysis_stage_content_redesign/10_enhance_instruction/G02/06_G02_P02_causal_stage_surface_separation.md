# G02 P02 — Causal Stage Surface Separation

- Status: `FROZEN`
**Assigned Coding Agent normative context: この文書のみ。**

## Objective

Causal presentationを分離し、Identification / Estimation / Effects / Diagnostics / Sensitivityが、それぞれ正しい目的・操作・結果surfaceを持つようにする。

## Baseline fact

- identification/estimation/effects/diagnostics/sensitivityはlegacy `inference` workspaceへbindされている。
- visible workspace headingは `Inference`。
- `Effects / Diagnostics` はshared main card。
- Refutation / Sensitivity formは`sensitivity`用surface markerを持つ。

## Required Stage ownership

### Identification

primary表示:

- 日本語の目的説明
- Dataset / FIXED Graph prerequisite
- causal question / estimand / strategy / adjustment / assumptions
- Identification / Eligibility action
- Gate/status/warnings

表示しない:

- estimator tuning
- Sensitivity / Refutation control

### Estimation

primary表示:

- 日本語の目的説明
- selected Identification Result prerequisite/reference
- estimator / nuisance / uncertainty / revision / override control
- Estimation action/status/linkage

Identification / Data Eligibility explanationをpage purposeとして表示しない。

### Effects

primary表示:

- 日本語の目的説明
- saved treatment-effect result
- uncertainty / interval
- ATE / ATT / CATE / heterogeneity / comparison

Diagnosticsとprimary heading/surfaceを共有しない。

### Diagnostics

primary表示:

- 日本語の目的説明
- balance / overlap / ESS / weights
- scientific warning

Effectsをreferenceしてよいが、Effects comparisonをpage purposeにしない。

### Sensitivity

primary表示:

- 日本語の目的説明
- Treatment Effect Result target reference
- Refutation control/result
- Sensitivity control/result

Identification / Data Eligibilityのmain explanationを表示しない。

## Visibility invariant

Stage-specific main control/resultはowning Stage以外ではhiddenかつnon-interactiveとする。

特に `refutation-form` / `sensitivity-form` はIdentification/Estimation/Effects/Diagnosticsで操作できないこと。

## Layout

semantic sectionを縦方向に分割する。compactな関連fieldはlocal grid可。独立sectionの横配置によるpage-level horizontal scrollを避ける。

## Preserve

- canonical Causal Stage catalog/route
- backend Causal execution semantics/result
- existing request field semantics
- FIXED Graph / Identification / Estimation scientific gate

## Likely files

- `frontend/index.html`
- `frontend/app.js`
- `frontend/causal_stage_presentation.js`
- `frontend/analysis_presentation.js`
- `frontend/styles.css`
- relevant frontend/product tests

## Browser E2E script ownership

P02は、G02のCausal critical journeyを検証する次のscriptをcandidateへ追加・維持する。

`tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py`

real Chromiumで Identification -> Estimation -> Effects -> Diagnostics -> Sensitivity のcurrent heading、wrong-stage primary control absence、route/historyの主要checkpointを検証し、evidenceを保存する。

## Focused self-check

identification/estimation/effects/diagnostics/sensitivityについてpositive/negative visibility testを作成・更新する。

日本語Stage purposeを確認し、Causal route/catalog/runtime semanticsが変わっていないことを確認する。

package checkpointのみ記録する。
