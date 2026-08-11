# Command Idempotency

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

create API一律ではなく、重複side effectを生むCommandへidempotencyを適用する方針へ整理する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-114 | MISMATCH | 作成系APIでidempotency keyを受け付ける | Some create endpoints accept Idempotency-Key, but Project creation and other create APIs do not. | frontend/app.js; frontend/index.html; interfaces/web_api/app.py; routers |
| FR-082 | PARTIAL_MATCH | 同一idempotency keyと同一bodyのCommandを重複実行しない | Idempotency exists on selected command endpoints, not every Command universally. | product/workflow/*; domain/execution_plan.py; execution.py; stage_execution.py; worker |

## 3. Confirmed remediation

FR-114a D1 correction、FR-114b D2、FR-082 D2。Command inventory/scope/conflict semanticsはpreflightでfreezeする。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-114a | **D1** | Create APIであること自体をidempotency applicability基準にする要求 | BASELINE |  |
| FR-114b | **D2** | Idempotency-required Command APIでIdempotency-Keyを受理 | ENH-E5 |  |
| FR-082 | **D2** | Command idempotency semantics/coverage | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
