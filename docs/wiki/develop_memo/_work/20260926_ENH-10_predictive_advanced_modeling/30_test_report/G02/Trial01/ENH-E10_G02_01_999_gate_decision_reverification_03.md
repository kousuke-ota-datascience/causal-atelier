# ENH-E10 G02 Trial 01 — Test Item 999: Gate Decision（reverification 03）

## 実行 identity と最終判定

**FAIL**

- Fixed Trial Candidate SHA: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- Tested Repository State: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb`
- Promotion eligibility: **PROMOTION_NOT_ALLOWED**

candidate identity は item 001 で PASS した。従って本 decision は candidate ambiguity や environment blocker ではなく、Fixed Trial Candidate の executable product behavior に基づく。

## Test Item 別の判定一覧

| Test Item | AC | Result | Independent evidence |
| --- | --- | --- | --- |
| 001 candidate identity | META | PASS | candidate ancestry and documentation-only post-candidate diff audited |
| 010 coefficient protected regression | 01, 11 | PASS | G02 suite: 13 passed |
| 020 compatibility registry | 02, 07 | PASS | explicit unavailable/inapplicable/scope errors |
| 030 SHAP binary | 03 | PASS | raw LOG_ODDS global/local adapter assertions |
| 040 SHAP regression | 04 | PASS | raw PREDICTION; max residual about `1.1e-14` |
| 050 LIME binary local | 05 | PASS | provider contribution / probability / TRAIN reference assertions |
| 060 LIME regression local | 06 | PASS | full five-stage run; PREDICTION / TRAIN reference |
| 070 dependency absence | 08 | PASS | isolated unavailable-provider explicit errors |
| 080 provenance and Model Card | 09, 11 | FAIL | Model Card omits LIME method-specific provenance |
| 090 G01 protected regression | 12 | FAIL | baseline PREPARE raises `KeyError: 'sampling'` |

## FAIL 根拠

Candidate identity passed. SHAP, binary/regression LIME provider execution, capability boundaries, dependency absence, and several protected tests passed. However, two mandatory product contracts fail:

1. AC-09 / item 080: Model Card does not retain required LIME explanation/provenance fields.
2. AC-12 / item 090: baseline G01 predictive flows fail in PREPARE with `KeyError: 'sampling'` when `explanation_spec` is empty.

二つの failure は独立しており、いずれか一つでも G02 PASS を禁止する。いずれも executable candidate の product failure であり、test orchestration / environment defect ではない。全 G02 blocking item を評価済みであり、frozen contract は G02 Browser E2E blocking item を `0` 件と定義する。Independent Test Agent は production code、test code、frozen contract を変更していない。

## 再現条件と remediation boundary

item 080 の regression LIME probe で result / Model Card payload を取得し、item 090 の isolated G01 command で protected regression を再現する。remediation candidate は両方の condition を修正し、同時に item 001–070 の PASS boundary を保持しなければならない。distinct Fixed Trial Candidate SHA と canonical completion report を作成した後に限り、新しい independent verification が promotion eligibility を判定できる。

詳細な command、raw output、fixture、identity audit、PASS/FAIL classification は `ENH-E10_G02_01_reverification_03_execution_detail.md` を参照すること。
