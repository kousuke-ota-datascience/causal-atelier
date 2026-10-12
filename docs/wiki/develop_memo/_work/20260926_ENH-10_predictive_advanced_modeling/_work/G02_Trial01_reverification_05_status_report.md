# ENH-E10 G02 Trial 01 — Independent Reverification 05 状況報告

## 状態

- Gate: `G02` / Trial: `01`
- Independent reverification: `05`
- Fixed Trial Candidate: `fbd97c5b7a95084affe5e2381d85d86d0dfa2558`
- Tested SHA: `1bf3026ba1918c8ca74af64318bdd42e90d7ed67`
- Gate Decision: **PASS**
- promotion: **未実施**
- G03: **未開始**
- evidence commit: `51ece275a683df3fde3b679e9a640bcbfeefe625`
- report-expansion commit: `319bd73c8dcc363e7b1a5b5a9a5a46c65beb42bf`
- test-path migration commit: `c46db7adcba206f317925ee7d250411327e7124b`
- test-path migration addendum commit: `04bd75bf9d536618fff58d4338aa1dc7a1cb179e`

## 実施内容

1. canonical implementation completion report からのみ Fixed Trial Candidate SHA を取得した。
2. candidate object の存在、previous failed candidate `e9a5b412349b10ced45d822aa08a54b6d9df00ba` からの ancestry、非空の production/test remediation diff、candidate 後の semantic diff 不在、検証開始時 working tree clean を確認した。
3. frozen G02 Test Item `001, 010, 020, 030, 040, 050, 060, 070, 080, 090, 999` を独立に評価した。
4. actual predictive full DAG で、`lightgbm_classifier.v1 + SHAP_TREE` と `lightgbm_regressor.v1 + SHAP_TREE` を検証した。双方について SPLIT/PREPARE/TRAIN/EVALUATE/EXPLAIN 成功、`GENERATED`、非空 global/local SHAP、raw output scale、frozen additivity、Result/Artifact/Model Card provenance 一致を確認した。
5. linear coefficient、LIME binary/regression、TRAIN reference sampling、one-hot categorical LIME configuration、optional dependency absence、unsupported model/method error、G01 protected regression を検証した。
6. 全 test report を、検証境界・assertion/AC 対応・実行コマンド・raw output・警告・限界・判定理由を含む粒度へ拡充した。
7. ENH-E10 固有 test 6 件を `tests/product/` から `tests/enhancement/enh_e10/<gate>/<layer>/` へ移設した。G01 は `contract/unit/integration`、G02 は `contract/integration` に整理した。
8. 移設後に collection `34 tests`、G01 capability isolation `7 passed`、G01/G02 および protected regression `43 passed, 2 non-failing SHAP warnings` を確認した。
9. historical evidence の実行時 path を改変せず、current rerun path と移設後検証を `30_test_report/ENH-E10_test_path_migration_addendum.md` に追記した。

## 作成/変更ファイル

reverification_05 の independent evidence と Gate Decision を作成・拡充した。

- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_001_candidate_identity_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_010_coefficient_protected_regression_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_020_compatibility_registry_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_030_shap_binary_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_040_shap_regression_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_050_lime_binary_local_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_060_lime_regression_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_070_optional_dependency_absence_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_080_provenance_and_model_card_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_090_g01_protected_regression_reverification_05.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision_reverification_05.md`

本報告ファイル:

- `_tmp_work/20260927_ENH-10/G02_Trial01_reverification_05_status_report.md`

製品コード、テストコード、依存関係、凍結 instruction は本報告作成・Reverification 05 証跡拡充では変更していない。

ただしその後の test architecture correction で、ENH-E10 固有の**テストコードのみ**を移設・共有 helper/fixture 化した。production code、依存関係、凍結 instruction、過去の Gate Decision は変更していない。

## 検証結果

| 検証 | 結果 | 根拠 |
| --- | --- | --- |
| candidate identity | PASS | object / ancestry / semantic remediation / clean tree を確認 |
| frozen G02 independent suite | PASS | `43 passed, 2 non-failing SHAP warnings in 18.97s` |
| G01 capability isolation suite | PASS | `7 passed in 2.18s` |
| SHAP binary actual full DAG | PASS | `GENERATED`、LOG_ODDS、global/local、additivity、provenance |
| SHAP regression actual full DAG | PASS | `GENERATED`、PREDICTION、global/local、additivity、provenance |
| LIME binary/regression | PASS | local output、TRAIN reference、effective seed、one-hot categorical configuration |
| optional dependency absence | PASS | SHAP/LIME とも `EXPLANATION_DEPENDENCY_UNAVAILABLE` |
| G01 protected regression | PASS | empty `explanation_spec`、artifact/load/predict、TRAIN/TEST isolation |
| AC-01〜AC-12 | PASS | 999 Gate Decision の acceptance synthesis を参照 |
| test-path migration collection | PASS | `34 tests collected in 4.31s` |
| test-path migration regression | PASS | G01 `7 passed`、G01/G02＋protected regression `43 passed, 2 warnings` |

runtime versions: Python `3.12.3`、LightGBM `4.7.0`、SHAP `0.52.0`、LIME `0.2.0.1`。

SHAP の warning 2 件は LightGBM binary array-shape に関する upstream provider notification である。test exit は `0` で、frozen scale、additivity、canonical output、provenance assertion の failure はなかったため、product contract failure とは判定していない。

### Current test-path authority

Reverification 05 当時の test report が示す `tests/product/test_enh_e10_*.py` は historical execution path である。移設後の current rerun authority は次である。

| Gate | Layer | current path |
| --- | --- | --- |
| G01 | contract | `tests/enhancement/enh_e10/g01/contract/test_model_capability.py` |
| G01 | unit | `tests/enhancement/enh_e10/g01/unit/test_lightgbm_adapters.py` |
| G01 | integration | `tests/enhancement/enh_e10/g01/integration/test_model_artifacts.py` |
| G02 | contract | `tests/enhancement/enh_e10/g02/contract/test_explanation_capabilities.py` |
| G02 | integration | `tests/enhancement/enh_e10/g02/integration/test_shap_backend.py` |
| G02 | integration | `tests/enhancement/enh_e10/g02/integration/test_lime_backend.py` |

旧→新 path の対応、移設根拠、移設後の exact command / raw output は `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/ENH-E10_test_path_migration_addendum.md` を authority とする。

## 残存制約

- 本作業は independent Gate verification と evidence recording に限定した。G02 promotion と G03 開始は実施していない。
- SHAP support は frozen compatibility matrix に従い LightGBM classifier/regressor に限定される。unsupported model/method は fallback せず explicit error となる。
- LIME は local-only であり、one-hot categorical feature の perturbation は無効な元カテゴリ組合せを形成し得る。この limitation は canonical output に記録され、因果的解釈はしない。
- SHAP/LIME の再現性は、記録済み provider/runtime version、sampling、parameters、fixture/identity の範囲で検証した。将来の provider version 変更に対する数値同一性までは主張しない。
- 過去の FAIL / BLOCKED evidence は削除・上書きしていない。reverification_05 PASS は新しい remediation candidate に対する独立判断である。
- test-path migration は Reverification 05 candidate `fbd97c5` 後の test-only change である。candidate の production semantics を変更しないが、過去 report の command は current rerun command としては用いない。
