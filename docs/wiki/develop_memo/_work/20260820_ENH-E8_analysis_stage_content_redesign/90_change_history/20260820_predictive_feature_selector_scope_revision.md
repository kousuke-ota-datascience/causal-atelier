# 2026-08-20 Predictive Feature Selector Scope Revision

- Status: `RECORDED`
- Affects: ENH-E8 G02 / P03
- Requirement semantic delta: `NONE`

## E8へ追加した内容

Predictive feature-column selectionを、comma-delimited free-text中心の入力からDataset-schema-backed popup/dialog + checkbox multi-selectionへ変更する。

ownership:

- Setup: editable feature selection
- Train: selected draft/spec feature setをread-only表示
- Predict: relevant execution specificationのfeature setをread-only表示

Confirm後のselector valueはexisting `predictive-analysis-spec/1 -> feature_spec.feature_columns` contractへmappingする。

## E8へ追加しない内容

- LightGBM
- LIME
- SHAP
- causal lifecycle analytical capability expansion

これらはlater Enhancementへ送る。

## Workflow impact

更新対象:

- root README
- `00_enhance_background/01`〜`05`
- revised Basic/Detailed Design addendum
- `G02/06`
- `G02/P00`
- `G02/P03`
- `G02/07`
- G02 README

candidateがIndependent Verificationへ入る前であり、06/07も未freezeのためTrialは増やさず、`09` Amendmentも使用しない。
