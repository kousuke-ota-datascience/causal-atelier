# Test Architecture

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

current core testsと、D2/D3裁定に由来するverification surfacesを分離する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| D22-013 | PARTIAL_MATCH | all listed test seams/benchmarks are present as implemented test architecture | Core domain/workflow/API/scientific tests exist, but the full approved target test architecture (including all browser/accessibility/performance surfaces) is not completely evidenced. | tests/; prior E4 verification artifacts |
| D30-018 | PARTIAL_MATCH | tests covering current domain/runtime/API contracts | Detailed design includes target verification surfaces beyond what can be established as complete E4 implementation; current core contract tests exist but full set is not evidenced. | tests/; E4 verification artifacts |

## 3. Confirmed remediation

current tests D1。D2 requirementのverificationは07へ追加。D3 scopeのacceptanceはENH-E5から外す。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| D22-013a | **D1** | Existing core test architecture | BASELINE |  |
| D22-013b | **D2** | Verification surfaces for D2 requirements | ENH-E5 |  |
| D22-013c | **D3** | Verification surfaces owned by D3 requirements | FUTURE |  |
| D30-018a | **D1** | Existing detailed contract tests | BASELINE |  |
| D30-018b | **D2** | Detailed verification for D2 requirements | ENH-E5 |  |
| D30-018c | **D3** | Detailed verification owned by D3 requirements | FUTURE |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
