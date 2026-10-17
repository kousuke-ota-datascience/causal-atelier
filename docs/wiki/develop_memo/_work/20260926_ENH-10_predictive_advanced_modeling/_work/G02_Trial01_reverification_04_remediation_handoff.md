# ENH-E10 G02 Trial 01 — Reverification 04 Remediation Handoff

## 状態

`READY_FOR_TEST`。独立 gate verification、PASS 判定、promotion は未実施。

- Previous failed candidate: `e9a5b412349b10ced45d822aa08a54b6d9df00ba`
- New FIXED_TRIAL_CANDIDATE_SHA: `fbd97c5b7a95084affe5e2381d85d86d0dfa2558`
- Evidence commit: `1bf3026ba1918c8ca74af64318bdd42e90d7ed67`
- Push: `causal-atelier/feature/ariadne_mvp_e10`

## 実施内容

- `PredictiveExplainRunner` から、互換性のある LightGBM モデルの
  `SHAP_TREE` を `explain_shap_tree` へ dispatch するよう修正。
- SHAP binary は raw `LOG_ODDS`、regression は `PREDICTION`、binary の
  prediction は `PROBABILITY` を維持。
- Explanation Result／JSON Artifact／Model Card に、SHAP の method/provider
  version、model/task/preprocessor/feature identity、TEST identity、
  tree-path-dependent background、sampling、runtime、predictive-not-causal
  limitation を保持。

## 変更ファイル

- `src/ariadne/capabilities/predictive/explanation_runner.py`
- `src/ariadne/capabilities/predictive/shap_backend.py`
- `tests/product/test_enh_e10_g02_p02_shap_backend.py`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/10_enhance_instruction/G02/09_ENH-E10_G02_01_Reverification_04_Remediation_Instruction.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/20_implementation_reports/G02/Trial01/E10-G02_01__implementation_completion.md`

## 検証結果

- SHAP binary full DAG: PASS — `GENERATED`、raw `LOG_ODDS`、PROBABILITY
  prediction、global/local、additivity、result/artifact/Model Card provenance。
- SHAP regression full DAG: PASS — `GENERATED`、`PREDICTION`、global/local、
  additivity、result/artifact/Model Card provenance。
- Protected regression: `43 passed`、SHAP provider warning 2件のみ。
- G01 import-order-isolated capability regression: `7 passed`。

## 残存制約

SHAP は LightGBM 専用かつ provider runtime 依存、LIME は local-only。

次の作業は、`fbd97c5b7a95084affe5e2381d85d86d0dfa2558` を対象とした新規の
独立 G02 Trial 01 verification である。独立検証による canonical gate
decision が PASS となるまで、G02 を promotion してはならない。
