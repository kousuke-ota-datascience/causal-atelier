# ENH-E10 G02 Trial 01 — 修正済みテストレポート一覧

## 対象範囲

以下は、G02 Trial 01 の current independent verification output（`reverification_03`）として新規作成または記載を詳細化した Markdown 一覧である。過去の FAIL / BLOCKED evidence は履歴証跡として保持し、修正対象に含めない。

出力ディレクトリ:

```text
docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/
30_test_report/G02/Trial01/
```

## Test Item 別レポート

| Test Item | ファイル | 主な補強内容 |
| --- | --- | --- |
| 001 candidate identity | `ENH-E10_G02_01_001_candidate_identity_reverification_03.md` | canonical candidate 取得元、preflight、object / ancestry / previous-failure guard、post-candidate diff 分類、再現条件 |
| 010 coefficient protected regression | `ENH-E10_G02_01_010_coefficient_protected_regression_reverification_03.md` | AC、command、raw suite result、coefficient / terminology 保護範囲、判定境界 |
| 020 compatibility registry | `ENH-E10_G02_01_020_compatibility_registry_reverification_03.md` | model × method × scope の error taxonomy、fallback 不在、再現条件 |
| 030 SHAP binary | `ENH-E10_G02_01_030_shap_binary_reverification_03.md` | binary fixture、raw LOG_ODDS、global/local mapping、provider warning の扱い |
| 040 SHAP regression | `ENH-E10_G02_01_040_shap_regression_reverification_03.md` | fixture、PREDICTION scale、additivity tolerance と residual raw evidence |
| 050 LIME binary local | `ENH-E10_G02_01_050_lime_binary_local_reverification_03.md` | positive-class probability、provider contribution、TEST instance / TRAIN reference、frozen parameter set |
| 060 LIME regression local | `ENH-E10_G02_01_060_lime_regression_local_reverification_03.md` | five-stage runtime outcome、PREDICTION scale、reference hash/count/seed、isolation boundary |
| 070 optional dependency absence | `ENH-E10_G02_01_070_optional_dependency_absence_reverification_03.md` | isolated `python -S` environment、SHAP/LIME absence raw output、explicit error taxonomy |
| 080 provenance and Model Card | `ENH-E10_G02_01_080_provenance_and_model_card_reverification_03.md` | missing Model Card fields の complete key set、AC-09 violation、failure classification / reproduction |
| 090 G01 protected regression | `ENH-E10_G02_01_090_g01_protected_regression_reverification_03.md` | exact failing command、stage execution record、`KeyError: 'sampling'` root cause、failure classification |
| 999 Gate Decision | `ENH-E10_G02_01_999_gate_decision_reverification_03.md` | Test Item summary、independent FAIL rationale、promotion boundary、remediation re-entry condition |

## 横断詳細レポート

| ファイル | 内容 |
| --- | --- |
| `ENH-E10_G02_01_reverification_03_execution_detail.md` | 全 Test Item の AC mapping、identity、exact commands、raw outputs、fixtures、FAIL classification、Gate Decision rationale を日本語で集約した詳細実行報告 |

## Evidence commits

| Commit | 内容 |
| --- | --- |
| `78966609bec74355746caebed6a5edd16495438b` | reverification 03 の初回 Test Item evidence |
| `68e7f1926a4f1a7c1ed697e30b21ad377d037640` | 個別 report の詳細 evidence 補強 |
| `eab80c281e769ecf92cc9518a30b2b9e900ca33b` | 日本語の横断詳細実行報告と 999 参照 |
| `127bcf8d4b90729db55b94c3b913334e378d7c7a` | 001 candidate identity report の全面詳細化 |
| `077134281426a808fe10875037b4e33713e95deb` | 010–090 と 999 の記載粒度・再現条件の補強 |

## 現在の判定

current Gate Decision は **FAIL**。FAIL evidence は item 080（AC-09: Model Card provenance）と item 090（AC-12: G01 protected regression）に記録されている。G02 promotion は許可されない。
