# 10_90_scope_exclusions

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## 11. 対象外要件

- Multi-class classification
- survival analysis、forecasting、ranking、recommendation
- online inference endpoint
- model deployment / registry / monitoring
- arbitrary Python execution
- arbitrary SQL query
- dashboard layout editor
- causal effectの自動保証
- unbounded AutoML
- automatic business decision
- LightGBM / SHAP / LIMEのmandatory core dependency化
- DoWhy / EconML等、ENH-E10でapprovedされていないexternal analytical engine追加
- Navigation stateのDB persistence / last-stage memory
- Overview / FlagshipをAnalytical Family peerとして追加すること
- 新規persistent Findings / Evidence domain modelの必須化
