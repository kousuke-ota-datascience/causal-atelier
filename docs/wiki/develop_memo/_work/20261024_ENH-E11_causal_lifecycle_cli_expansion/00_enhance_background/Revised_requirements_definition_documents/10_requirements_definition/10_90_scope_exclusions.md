# 10_90_scope_exclusions


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
- ENH-E10の承認範囲に含まれないexternal analytical engineを**ENH-E10へ無条件に追加すること**。ENH-E11のDEC09承認Method別Optional Capabilityに限る例外は後掲§11.1に規定する。
- Navigation stateのDB persistence / last-stage memory
- Overview / FlagshipをAnalytical Family peerとして追加すること
- 新規persistent Findings / Evidence domain modelの必須化

## 11.1. Local Scientific CLIのOptional Capabilityと対象外機能

- 旧ENH-E10の外部Engine除外は、E11においてDEC09が承認した**Local Scientific CLIのMethod別Optional Capability**の範囲に限り例外とする。DoWhy、EconML、Tigramite等の採用を既存Product Web/DBの強制依存にしない。
- 初期E11に含めないのは、ATC、汎用Mediation、Matching／汎用g-computation、Policy Value、Monitoring/drift、汎用Graph consensus、一般化された部分識別効果集合の自動数値推定。
- 初期E11に含めないのは、Simulated Confounder／Graph Perturbation、古典OLS以外の未観測交絡Sensitivity全面化、RPCMCI／J-PCMCI+、別審査の条件付きIV推定器C、SCM未承認CI。
- 新E11 MethodのProduct API/UI/Worker/DB/migration統合、既存Product GAP-C01〜04の暗黙の閉鎖は含めない。
- 外販、顧客向けBackend配布、受領者別法務審査、SBOM／Legal Release Workflowは初期E11の機能・必須Gateから除外する。社内利用に適用されるOSSライセンスおよび組織規程の遵守は、この除外により免除されない。
- 付録Aの**D-only Scope**はE11初期の必須提供対象ではない。**混合Disposition**ではR/Q/Nの承認部分のみ実装義務とし、D部分は追跡を維持する。

**Authority:** [DEC-SR04-09](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)。対象Scopeと正式要件の対応は [RD-03 Trace](../doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md)。
