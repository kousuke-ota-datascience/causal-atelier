# PREP-01 RD04 FR88 — Revised Requirement Text and Metadata Reconciliation

- Date: 2026-11-17 JST
- Source branch/commit: `prototype/ariadne_mvp` / `51ae5e0987c1c6f267b1b5566a817b7e47d929a3`
- Historical decision ledger: `doc01_review/rd04_review/95_rd04_fr_application_review.md` (blob `0cfc780530cb379f7bd0625642ae09d3954bd885`)
- Kind: FLOW / STATIC RECONCILIATION; **not** independent semantics approval
- Scope: RD04 revised existing FR **88** entries (SPLIT 69, MOVE_BD 16, REWRITE_RD 3); remaining KEEP_RD 107 unmodified are **not** audited here

## 1. Check definition

For each ID, resolve its single row in the Revised Requirement stock file and compare the complete RD requirement body with the RD04 ledger's revised body **as an exact string**, plus requirement status, implementation status and delivery classification. This is a deterministic transcription check, not an evaluation that migrated design clauses preserved their original semantics. Any mismatch remains explicit and cannot be waived by the aggregate count.

## 2. Per-ID results

| ID | Disposition | Revised RD file | Requirement text | Req status | Impl status | Delivery |
|---|---|---|---|---|---|---|
| FR-002 | SPLIT | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-006 | SPLIT | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-007 | SPLIT | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-008 | REWRITE_RD | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-011 | SPLIT | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-015 | SPLIT | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-020 | SPLIT | `10_10_fr_project_context_data.md` | MATCH | MATCH | MATCH | MATCH |
| FR-026a | REWRITE_RD | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-029 | SPLIT | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-032 | SPLIT | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-034 | SPLIT | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-147 | SPLIT | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-148 | SPLIT | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-175 | SPLIT | `10_11_fr_exploratory.md` | MATCH | MATCH | MATCH | MATCH |
| FR-059 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-061 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-067 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-068 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-069 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-071 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-072 | REWRITE_RD | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-150 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-151 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-161 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-176 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-178 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-180 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-181 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-182 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-183 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-184 | SPLIT | `10_12_fr_predictive.md` | MATCH | MATCH | MATCH | MATCH |
| FR-043 | SPLIT | `10_13_fr_causal.md` | MATCH | MATCH | MATCH | MATCH |
| FR-045 | MOVE_BD | `10_13_fr_causal.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-048 | SPLIT | `10_13_fr_causal.md` | MATCH | MATCH | MATCH | MATCH |
| FR-051 | SPLIT | `10_13_fr_causal.md` | MATCH | MATCH | MATCH | MATCH |
| FR-054 | SPLIT | `10_13_fr_causal.md` | MATCH | MATCH | MATCH | MATCH |
| FR-075 | MOVE_BD | `10_14_fr_workflow_execution.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-076 | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-077 | MOVE_BD | `10_14_fr_workflow_execution.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-078 | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-079 | MOVE_BD | `10_14_fr_workflow_execution.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-080 | MOVE_BD | `10_14_fr_workflow_execution.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-082 | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-084 | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-085 | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-086a | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-086b | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-087b | SPLIT | `10_14_fr_workflow_execution.md` | MATCH | MATCH | MATCH | MATCH |
| FR-089 | MOVE_BD | `10_14_fr_workflow_execution.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-143 | MOVE_BD | `10_14_fr_workflow_execution.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-090 | SPLIT | `10_15_fr_results_lineage.md` | MATCH | MATCH | MATCH | MATCH |
| FR-091 | SPLIT | `10_15_fr_results_lineage.md` | MATCH | MATCH | MATCH | MATCH |
| FR-092 | SPLIT | `10_15_fr_results_lineage.md` | MATCH | MATCH | MATCH | MATCH |
| FR-095 | SPLIT | `10_15_fr_results_lineage.md` | MATCH | MATCH | MATCH | MATCH |
| FR-099 | SPLIT | `10_15_fr_results_lineage.md` | MATCH | MATCH | MATCH | MATCH |
| FR-169 | SPLIT | `10_15_fr_results_lineage.md` | MATCH | MATCH | MATCH | MATCH |
| FR-107 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-108 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-109 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-130 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-132 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-133 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-136 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-140 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-141 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-144 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-145 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-157 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-158 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-159 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-160 | MOVE_BD | `10_16_fr_navigation_ui.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-163 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-164 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-165 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-171 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-174 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-177 | SPLIT | `10_16_fr_navigation_ui.md` | MATCH | MATCH | MATCH | MATCH |
| FR-113 | SPLIT | `10_17_fr_api_cli.md` | MATCH | MATCH | MATCH | MATCH |
| FR-114a | SPLIT | `10_17_fr_api_cli.md` | MATCH | MATCH | MATCH | MATCH |
| FR-114b | SPLIT | `10_17_fr_api_cli.md` | MATCH | MATCH | MATCH | MATCH |
| FR-115 | SPLIT | `10_17_fr_api_cli.md` | MATCH | MATCH | MATCH | MATCH |
| FR-120a | SPLIT | `10_17_fr_api_cli.md` | MATCH | MATCH | MATCH | MATCH |
| FR-120b | SPLIT | `10_17_fr_api_cli.md` | MATCH | MATCH | MATCH | MATCH |
| FR-121 | SPLIT | `10_18_fr_security_operations.md` | MATCH | MATCH | MATCH | MATCH |
| FR-124a | SPLIT | `10_18_fr_security_operations.md` | MATCH | MATCH | MATCH | MATCH |
| FR-124b | SPLIT | `10_18_fr_security_operations.md` | MATCH | MATCH | MATCH | MATCH |
| FR-128a | MOVE_BD | `10_18_fr_security_operations.md` | **MISMATCH** | MATCH | MATCH | MATCH |
| FR-128b | SPLIT | `10_18_fr_security_operations.md` | MATCH | MATCH | MATCH | MATCH |

## 3. Summary and limits

- Reconciled IDs: 88; unique IDs: 88; missing rows: 0.
- Full text mismatches: 16; Requirement status mismatches: 0; Implementation status mismatches: 0; Delivery mismatches: 0.
- **Overall static transcription check: FAIL**. This does NOT certify all 88 semantic transformations or downstream migration completeness.
- Each revised RD source file blob: `10_10_fr_project_context_data.md`=`08a1b8a4ae6cf32585e533e8b318625331d97ee8`; `10_11_fr_exploratory.md`=`4dd573a8992d8fbaeaca3cb12767d058a3c8b3af`; `10_12_fr_predictive.md`=`61c8f9e505b6a9ac6bee6cd15446060e36fc1683`; `10_13_fr_causal.md`=`07496a883afed1949968ae36fe846822e6a8f311`; `10_14_fr_workflow_execution.md`=`9865be6e10e7e4d35374c1caab4bcdd52666bd3e`; `10_15_fr_results_lineage.md`=`31692db6ae310207a9ffd77fb1467abd38c1944d`; `10_16_fr_navigation_ui.md`=`c298db4ffcbb993733f00f8df1e304a886ebe86a`; `10_17_fr_api_cli.md`=`957b1775a33b66e4c270feca2334fc5fb75f9d73`; `10_18_fr_security_operations.md`=`6922d444a48cf0f60deef63d68cf757978057fa5`.

## 4. Remaining semantic review obligations

For every SPLIT/MOVE_BD ID, verify that the original normative predicates (prohibitions, numerical thresholds, roles, versioning, negative cases) are captured in the designated 21/22/23/30 stock documents and that the RD's user-observable core is not weakened. For REWRITE_RD, verify the new wording preserves the externally observable obligation. Separately, evaluate any pre-existing scientific and compatibility constraints not visible from literal string comparison. **No Owner sign-off is implied.**

### Unresolved textual/metadata discrepancies

- FR-045: expected/observed revised text mismatch = true; observed `Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない`
- FR-075: expected/observed revised text mismatch = true; observed `Family別PlannerをRegistryから解決する`
- FR-077: expected/observed revised text mismatch = true; observed `Stage Typeをnamespace、name、versionで識別する`
- FR-079: expected/observed revised text mismatch = true; observed `Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない`
- FR-080: expected/observed revised text mismatch = true; observed `canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する`
- FR-089: expected/observed revised text mismatch = true; observed `Generic validationとFamily-specific validationを分離して実行する`
- FR-143: expected/observed revised text mismatch = true; observed `runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない`
- FR-133: expected/observed revised text mismatch = true; observed `FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する`
- FR-140: expected/observed revised text mismatch = true; observed `Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない`
- FR-141: expected/observed revised text mismatch = true; observed `Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない`
- FR-144: expected/observed revised text mismatch = true; observed `concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する`
- FR-145: expected/observed revised text mismatch = true; observed `generic application layerはFamily-specific Stage semanticsを集中所有しない`
- FR-157: expected/observed revised text mismatch = true; observed `既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない`
- FR-158: expected/observed revised text mismatch = true; observed `AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない`
- FR-160: expected/observed revised text mismatch = true; observed `Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない`
- FR-128a: expected/observed revised text mismatch = true; observed `Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する`