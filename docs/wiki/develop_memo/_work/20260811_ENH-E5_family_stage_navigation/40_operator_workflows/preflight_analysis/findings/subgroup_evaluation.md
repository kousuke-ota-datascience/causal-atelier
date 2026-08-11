# Predictive Subgroup Evaluation

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

evaluation_spec.subgroupsが入力contractに存在する一方、subgroup output/uncertaintyが未実装であるgapを整理する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-067 | MISMATCH | 指定subgroupごとのperformanceとsample sizeを確認できる | Subgroups are accepted in evaluation_spec, but subgroup performance computation/output was not found. | capabilities/predictive/validation.py; planner.py; metrics.py; training/explanation runners |
| AR-016 | MISMATCH | subgroup metricはsample sizeと不確実性を併記する | Subgroup metrics/uncertainty output is not implemented. | family capability validation/runners; comparison/lineage/product closure services |

## 3. Confirmed remediation

D2。subgroup performance + sample size + uncertaintyを一体で実装する。uncertainty contractはCoding contract前にfreezeする。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-067 | **D2** | Subgroup performance + sample size | ENH-E5 |  |
| AR-016 | **D2** | Subgroup metric uncertainty | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
