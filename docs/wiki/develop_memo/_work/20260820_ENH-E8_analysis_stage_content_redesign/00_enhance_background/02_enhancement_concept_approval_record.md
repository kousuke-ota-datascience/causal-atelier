# ENH-E8 Enhancement Concept Approval Record

- Status: `APPROVED`
- Approval authority: Human operator
- Baseline: `386521d18e9c5cc4d42fb99c97c212430908afc3`

## 承認対象

- Enhancement ID: `ENH-E8`
- Gate: `G01`, `G02`
- G01 Mode: `SINGLE_EXECUTION`
- G02 Mode: `WORK_PACKAGE`
- G02 packages: `P01 -> P02 -> P03`
- Requirement semantic delta: `NONE`
- API/DB/backend/runtime semantic delta: `NONE`

## 追加scope

Predictiveのfeature-column selectionをE8へ追加する。

- SetupでDataset-schema-backed popup/dialog + checkboxにより編集する。
- Train/Predictでは該当feature setをread-only表示する。
- `predictive-analysis-spec/1` semanticsは変更しない。

## 別Enhancementへの申し送り

- LightGBM / LIME / SHAP: ENH-E9
- causal lifecycle foundation expansion: ENH-E10以降

CodingとTestはworkflow templateを介して別Agentへ委譲する。
