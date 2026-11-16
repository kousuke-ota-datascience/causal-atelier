# 10_14_fr_workflow_execution

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-074 | Workflow | Analysis FamilyをEXPLORATORY、CAUSAL、PREDICTIVEとして識別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-075 | Workflow | Family別PlannerをRegistryから解決する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-076 | Workflow | Plannerはversionedで不変なExecution Planを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-077 | Workflow | Stage Typeをnamespace、name、versionで識別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-078 | Workflow | PlanはStage dependencyとinput/output bindingをDAGとして保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-079 | Workflow | Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-080 | Workflow | canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-081 | Workflow | Stage ExecutionとAttemptのstatus、開始・終了時刻、errorを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-082 | Workflow | idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-083 | Workflow | 技術retryは同一Execution、条件変更は新Executionとする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-084 | Workflow | 上流Artifactを下流Stage inputへ型付きでbindingする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-085 | Workflow | 未登録Runner、cycle、missing output、schema mismatchをPlan受付時に拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-086a | Workflow | stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する | SHOULD | ACTIVE | PARTIAL | ENH-E5 |
| FR-086b | Workflow | Stageごとのtimeout / operational resource limitをpersistent/configurable policyとして保持する | SHOULD | DEFERRED | PARTIAL | FUTURE |
| FR-087a | Workflow | Execution snapshotにcurrent code/runtime/schema再現性metadataを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-087b | Workflow | Execution `runtime_version_json`にAriadne code、Python、platform、machineおよび実際に利用したscientific library versionを保持する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-088 | Workflow | Execution StatusとResult analytical statusを分離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-089 | Workflow | Generic validationとFamily-specific validationを分離して実行する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-143 | Workflow | runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
