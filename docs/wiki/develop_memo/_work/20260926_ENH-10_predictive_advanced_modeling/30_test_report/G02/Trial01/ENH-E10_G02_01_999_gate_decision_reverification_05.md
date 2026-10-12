# ENH-E10 G02 Trial 01 — Test Item 999: Independent Gate Decision（reverification 05）

## 決定

**PASS**

| 項目 | 値 |
| --- | --- |
| Fixed Trial Candidate | `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` |
| Tested SHA | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` |
| 実行環境 | Python `3.12.3`; LightGBM `4.7.0`; SHAP `0.52.0`; LIME `0.2.0.1` |
| Independent suite | `43 passed, 2 non-failing SHAP warnings in 18.97s` |
| G01 isolated capability suite | `7 passed in 2.18s` |
| Promotion | **本検証では実施しない** |

## MUST acceptance synthesis

| AC | 対応 item | 結果 | 独立観測の要約 |
| --- | --- | --- | --- |
| AC-01 | 010 | PASS | coefficient global/local・scale・feature order を保護 |
| AC-02 | 020 | PASS | compatibility / explicit unsupported errors、fallback なし |
| AC-03 | 030 | PASS | actual classifier SHAP DAG、raw LOG_ODDS、global/local、additivity |
| AC-04 | 040 | PASS | actual regressor SHAP DAG、raw PREDICTION、global/local、additivity |
| AC-05 | 050 | PASS | binary LIME local、positive probability、one-hot categorical config |
| AC-06 | 060 | PASS | regression LIME local、TRAIN reference / effective seeds |
| AC-07 | 020 | PASS | global LIME は explicit scope error、pseudo-global なし |
| AC-08 | 070 | PASS | SHAP/LIME absence は explicit dependency error |
| AC-09 | 030/040/050/060/080 | PASS | Result / Artifact / Model Card provenance 一致 |
| AC-10 | 030/040/050/060 | PASS | immutable TEST explanation と training isolation |
| AC-11 | 010/030/040/050/060/080 | PASS | predictive-not-causal limitation 一貫 |
| AC-12 | 090 | PASS | G01 full flow / artifact-load-predict compatibility |

## 根拠と範囲

candidate identity (001) は object existence、previous-failed ancestry、non-empty semantic remediation、post-candidate semantic state、clean tree をすべて満たした。前回 reverification 04 の実証済み FAIL（SHAP stage が `NOT_APPLICABLE`）に対し、今回の candidate は binary と regression の双方で actual EXPLAIN stage を `GENERATED` にし、Result / Artifact / Model Card まで provenance を到達させた。direct backend test だけを根拠にしていない。

SHAP binary provider warning 2 件は LightGBM array-shape の upstream notification であり、test exit は 0、frozen scale / additivity / output / provenance assertion に失敗はない。したがって product contract violation ではない。

全 MUST criterion と protected regression が独立実行で PASS したため Gate Decision は **PASS**。ただしユーザー指示に従い、本報告は G02 promotion を自動実行せず、G03 も開始しない。過去の FAIL / BLOCKED evidence は保存されている。
