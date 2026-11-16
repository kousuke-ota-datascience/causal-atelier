# 10_13_fr_causal

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-035 | Causal | 複数algorithm / parameterでcausal discoveryを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-036 | Causal | User-definedまたはImported GraphをDiscoveryなしで登録できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-037 | Causal | DAG、CPDAG、PAGおよびendpoint semanticsを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-038 | Causal | Graph Candidateの共通条件、変更条件およびedge差分を比較できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-039 | Causal | FIXED Graphからchild DRAFTを作成し、編集理由を記録して再固定できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-040 | Causal | Population、Treatment、Comparator、Outcome、Time、Estimand、Decision UseをCausal Questionに固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-041 | Causal | assignment、time zero、eligibility、strategy、adjustment set、assumptionsをCausal Designに固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-042 | Causal | Graph、Question、DesignからIdentification Resultを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-043 | Causal | Identificationは全reasonを収集後、確定的不整合をreview statusより優先してstatus決定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-044 | Causal | 型、欠測、post-treatment、sample size、overlapをData Eligibilityとして評価する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-045 | Causal | Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-046 | Causal | Identification、Eligibility、Estimator互換性を満たす場合のみEstimationを受け付ける | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-047 | Causal | ATEまたはATTと区間推定を生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-048 | Causal | estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存する。全estimatorへ同一diagnostic setを強制しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-049 | Causal | Placebo TreatmentおよびData SubsetによるRefutationを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-050 | Causal | Adjustment SetおよびPropensity ClippingのSensitivityを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-051 | Causal | 同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-052 | Causal | 同一条件のRERUNと条件変更のREVISEDを区別し、changed dimensionsとreasonを保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-053 | Causal | 科学的負結果をExecution failureと区別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-054 | Causal | Causal ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion/AnalysisView、GraphVersion、上流Result、Artifactへcanonical lineageで遡れる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-153 | Causal | Causalは`setup / discovery / identification / estimation / effects / diagnostics / sensitivity`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-154 | Causal | IdentificationとEstimationを別Navigation Stageとして扱い、識別可能性と有限標本推定を混同しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-155 | Causal | EstimationとEffectsを別Navigation Stageとして扱い、推定設定と推定結果の閲覧・利用を混同しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-156 | Causal | DiagnosticsとSensitivityを別Navigation Stageとして扱う | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
