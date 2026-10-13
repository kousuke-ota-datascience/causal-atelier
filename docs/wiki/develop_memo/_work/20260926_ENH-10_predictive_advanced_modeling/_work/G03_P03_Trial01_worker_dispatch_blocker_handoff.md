# ENH-E10 G03 P03 Trial 01 — worker dispatch blocker handoff

## 結論

P03 Trial 01 は引き続き `BLOCKED_IMPLEMENTATION` である。初回 blocker の Idempotency-Key 欠落は修復済みだが、再開後の scenario 100 が worker-side の `Causal Stage failed` で FAILED となるため、P03 の完了条件を満たせない。

## 解消済み blocker

```text
BLOCKER_FIX_SHA=3a4cbef4bb104550f5c24c61661f5dafe265d618
```

`frontend/app.js` の Predictive execution submission に既存 `idempotencyKey()` を `Idempotency-Key` として追加した。対象 POST は HTTP `202 Accepted` となり、execution 作成まで進むことを実ブラウザ経路で確認した。

回帰:

```text
node --check frontend/app.js
10 passed in 6.18s
```

## 新規 blocker の観測事実

scenario 100:

```text
Task: BINARY_CLASSIFICATION
Model: lightgbm_classifier.v1
Explanation: SHAP_TREE
```

観測結果:

- Analysis Specification: create / validate / fix 成功。
- Execution Plan: create / validate 成功。
- Execution submission: HTTP `202 Accepted`。
- Worker: execution を `PREDICTIVE/DISCOVERY` として claim。
- Terminal execution: `FAILED`。
- 正確な terminal error: `Causal Stage failed`。
- browser runner evidence: `AssertionError: Causal Stage failed`。

この failure は `test-results/browser_e2e/enh_e10/evidence.json`、trace、video、screenshot と API/worker log で確認した。runner は terminal status を先に検査するため、成功通知の timeout で failure を覆い隠さない。

## 判断

P03 の browser runner、Compose lifecycle、frontend Idempotency header の障害ではない。worker-side Predictive execution dispatch が generic Causal Stage に到達して失敗している。P03 の責務外であり、未確認の原因を仮定して修正しない。

scenario 100 が FAILED のため、scenario 110（`REGRESSION` + `lightgbm_regressor.v1` + `LIME_TABULAR`）は実行していない。P03 checkpoint は存在しない。

## 保全済み P03 実装

- `.dockerignore`
- `Dockerfile.browser-e2e`
- `Dockerfile.predictive-advanced`
- `compose.enh_e10.yaml`
- `tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`
- `tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py`

上記は `785e73b9e8d3c01d9f6130247654cae922b576a7` に保全済みである。この commit は working tree を保護するための記録であり、P03 `PACKAGE_CHECKPOINT_SHA`、`PACKAGE_COMPLETE`、または Gate 判定を意味しない。

## 再開条件

worker-side Predictive execution dispatch が actual Predictive workflow を実行できるよう責務 scope で修復された後、同じ G03/P03/Trial 01 の browser runner を clean hermetic lifecycle で再実行する。scenario 100 と 110 がともに `SUCCEEDED`、required Result/Artifact、UI explainability、Model Card/provenance evidence を満たすまで `PACKAGE_COMPLETE` としてはならない。
