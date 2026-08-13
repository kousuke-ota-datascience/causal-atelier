# Lineage / Traceability

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

既存lineageをContext/Spec/Plan/Stage/upstream Resultまで意味的に辿れる形へ完成させる。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-008 | PARTIAL_MATCH | Contextの履歴、利用Analysisおよび関連Resultを確認できる | Context usage covers AnalysisSpecification plus historical/compatibility family execution/result projections; it is not a complete canonical Execution/Result usage index. | product/domain/analysis_specification.py; product/persistence/orm_models.py; workspace lifecycle/query services |
| FR-054 | PARTIAL_MATCH | Causal ResultからQuestion、Design、Graph、Eligibility、上流Resultへ遡れる | Canonical lineage covers major upstream entities, but the full Question/Design/Graph/Eligibility/upstream Result chain as one complete contract is not fully represented. | product/application/scientific_validation_service.py; capabilities/causal/workflow.py; graph services/domain |
| FR-095 | PARTIAL_MATCH | ResultからContext、Dataset、View、Spec、Plan、Stage、Artifactへ遡る | Lineage covers Project/Dataset/View/Execution/Result/Artifact/Graph/Annotation relationships, but does not expose the full Spec/Plan/Stage chain requested. | product/persistence/orm_models.py; product/application/product_closure_service.py; comparison/lineage services; results router |
| NFR-002 | PARTIAL_MATCH | すべてのResultがProject、Context、Dataset、Spec、Execution、Artifactへ遡れる | Lineage is substantial but does not provide the full Project/Context/Dataset/Spec/Execution/Artifact trace for every Result as stated. | cross-cutting source/tests: domain/workflow/persistence/web API/worker/frontend/adapters |

## 3. Confirmed remediation

D2。直接FK追加を前提にせずcanonical relation/read modelでtrace可能性を成立させる。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-008 | **D2** | Canonical Context usage index to Analysis/Result | ENH-E5 |  |
| FR-054 | **D2** | Causal upstream lineage completeness | ENH-E5 |  |
| FR-095 | **D2** | Result lineage to Context/Dataset/View/Spec/Plan/Stage/Artifact | ENH-E5 |  |
| NFR-002 | **D2** | Complete Result traceability to Project/Context/Dataset/Spec/Execution/Artifact | ENH-E5 |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
