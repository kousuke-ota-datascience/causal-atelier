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

## 判定手順

Gate PASS は test count の多さではなく、frozen Test Item の blocking coverage と MUST AC の全充足によって決めた。以下の順に判断した。

1. item 001 が candidate identity を確立し、以降の実行対象が canonical candidate の意味状態であることを確認した。
2. item 010 / 020 で baseline と capability failure boundary を確認した。
3. item 030 / 040 は前回の failure point だった actual SHAP EXPLAIN stage を、binary と regression で別々に検証した。
4. item 050 / 060 / 070 で LIME、reference sampling、provider absence を検証した。
5. item 080 / 090 で durable provenance と G01 protected contract を検証した。
6. 一つでも MUST failure なら FAIL、実行不能なら BLOCKED とする frozen decision rule を適用した。該当はない。

## 前回 FAIL との差分

reverification 04 は backend unit success に対して stage output が `NOT_APPLICABLE`、global/local null、SHAP provenance null であり、AC-03 / AC-04 を FAIL とした。reverification 05 では同じ full-DAG boundaryで `GENERATED`、非空 global/local、raw scales、frozen additivity、Result/Artifact/Model Card equality を binary と regression で確認した。従って過去 FAIL を上書き・削除せず、修正 candidate に対する新しい独立 evidence として PASS を記録する。

## 検証後の状態

evidence-only commit は `51ece275a683df3fde3b679e9a640bcbfeefe625`。production source、test source、dependency、frozen instruction は変更していない。Gate の promotion state を変更する操作、および G03 着手は行っていない。
