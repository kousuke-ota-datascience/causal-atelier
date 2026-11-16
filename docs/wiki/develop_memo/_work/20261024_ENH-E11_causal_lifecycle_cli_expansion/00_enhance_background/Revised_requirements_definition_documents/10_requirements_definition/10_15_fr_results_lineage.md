# 10_15_fr_results_lineage

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-090 | Result / Lineage | canonical Resultはexecution/stage relation、result type、scientific status、summary/payload/diagnostics/warningsを保持する。family/generic schema_versionをResult direct fieldへ重複保持しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-091 | Result / Lineage | Result payloadはFamily・Type別Schemaで検証する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-092 | Result / Lineage | canonical Artifactはproject/execution/stage/result relation、artifact type/scope、object_key、media type、hash、size、metadataを保持する。family/generic schema_versionをdirect fieldへ重複保持しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-093 | Result / Lineage | 同一または明示的に互換なResult Typeのみ定量比較する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-094 | Result / Lineage | Project単位でExplore、Causal、Predictiveのsummaryを横断表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-095 | Result / Lineage | ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion、AnalysisView、GraphVersion、input Result、base Execution、Artifactへ遡れるcanonical lineage read modelを提供する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-096 | Result / Lineage | 探索Resultから分析draft等のcross-analysis relationを明示保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-097 | Result / Lineage | Result、Graph、Analysis SpecificationまたはProjectへAnnotationできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-098 | Result / Lineage | 採用判断、仮定、適用範囲、限界、次ActionをAnnotationへ記録できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-099 | Result / Lineage | Manifest、Result summary、Specification、Artifact参照をexportできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-100 | Result / Lineage | 保存済みResultを上書きせず、訂正は新ResultまたはAnnotationで行う | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-101 | Result / Lineage | 改訂Executionとbase ExecutionのedgeをLineage表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-102 | Result / Lineage | AUC等とATE等を単一Scoreへ正規化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-103 | Result / Lineage | Viewerがread-onlyで全来歴を確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-169 | Result / Lineage | Results / Lineageはpersisted cross-analysis aggregation、comparison、Artifact、Lineage、Annotationを所有し、Analysis Workspaceはexecution-local / stage-local presentationを担う | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
