# ENH-E10 Agent Entry Prompts — 使用ガイド

**Document class:** Enhancement-side Execution Guide  
**Enhancement:** `ENH-E10`  
**Status:** `MATERIALIZED`  
**Canonical work root:** `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling`

このdirectoryはgeneric templateではなく、ENH-E10用にmaterialize済みのAgent execution entry pointを保持する。Enhancement-fixed identityは再推測せず、各promptに残されたRuntime variableだけをexecution時に解決する。

## 1. Prompt selection

| Current state | Prompt |
|---|---|
| Normal `SINGLE_EXECUTION` Gate | `10_normal_execution_01_single_execution_coding_agent_prompt.md` |
| Normal `WORK_PACKAGE` assigned Pxx | `10_normal_execution_02_work_package_coding_agent_prompt.md` |
| Normal `WORK_PACKAGE` — all required Pxx completed | `20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` |
| Independent Gate verification | `30_independent_verification_01_test_agent_prompt.md` |
| formal product FAIL — next Trial `CONSOLIDATED + SINGLE_EXECUTION` remediation | `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Work Package Gate control-plane | `50_orchestration_01_gate_orchestrator_prompt.md` |

### ENH-E10-specific exclusion

`31_blocked_test_repair_01_test_infrastructure_agent_prompt.md` はENH-E10 standard workflowでは使用しない。

ENH-E10 test architecture handoffでは、Independent Test Agentはtest implementation / orchestration / environment defectを修復しない。product correctnessを判定できない場合は `BLOCKED` としてevidenceを残し、Operatorへ返す。test-side BLOCKEDをproduct FAILへ変換せず、formal FAIL remediation promptも自動起動しない。

このため、ENH-E9 G02で使用されたSAME_TRIAL blocked-test-repair routeは本directoryから除外する。

## 2. Enhancement-fixed identity

以下は全promptで固定済みである。

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E10
ENHANCE_SHORT_ID=E10
BRANCH_NAME=feature/ariadne_mvp_e10
REMOTE_NAME=origin
WORK_ROOT=docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling
WORK_DIR_NAME=20260926_ENH-10_predictive_advanced_modeling
```

Enhancement-side promptにこれらの未解決placeholderが残っている場合、execution readinessは `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED` とする。

## 3. Runtime identity

Human / Orchestratorがexecutionごとに指定する値はprompt種別に応じて次だけである。

| Prompt | Runtime values |
|---|---|
| Single Execution Coding | `GATE_ID`, `TRIAL_NO` |
| Work Package Coding | `GATE_ID`, `PACKAGE_ID`, `TRIAL_NO` |
| Candidate Assembly | `GATE_ID`, `TRIAL_NO` |
| Independent Verification | `GATE_ID`, `TRIAL_NO` |
| Formal FAIL Remediation | `GATE_ID`, `REMEDIATION_PACKAGE_ID`, `TRIAL_NO` |
| Gate Orchestrator | `GATE_ID`, `TRIAL_NO` |

SHA valuesはHuman-supplied variableではない。repository state / canonical reportから導出する。

主なruntime-derived values:

- `START_SHA`
- `PACKAGE_CHECKPOINT_SHA`
- `FIXED_TRIAL_CANDIDATE_SHA`
- `EVIDENCE_COMMIT_SHA`
- `TEST_START_SHA`
- `TEST_EVIDENCE_COMMIT_SHA`
- `PREVIOUS_FAILED_CANDIDATE_SHA`

架空SHA、過去Trial SHA、別Gate SHAをprompt placeholderとして事前入力してはならない。

## 4. Routing rules

Normal executionではGate 06のmetadataをrouting authorityとする。

```text
Gate dependency declaration -> Gate 06 "Depends on"
Execution mode              -> Gate 06 "Execution mode"
Required package set        -> Gate 06 "Required packages"
Verification authority      -> Gate 07
Gate decision evidence      -> canonical 999
```

Rules:

- `SINGLE_EXECUTION` の場合はsingle execution coding promptを使用する。
- `WORK_PACKAGE` の場合はrequired Pxxを順に実行し、全required package completion後にCandidate Assemblyを行う。
- formal FAIL後はnormal Work Package promptへ戻らず、current Trialの08 remediation contractが要求するnext Trial remediation routeを使用する。
- Independent Verificationのtest-side `BLOCKED` はproduct FAILではない。
- ENH-E10ではtest-side `BLOCKED` を修復する専用31 promptを持たない。
- Gate dependencyやrequired packageが未freezeならexecutionを開始しない。

## 5. Information isolation

### Coding Agent

- `SINGLE_EXECUTION`: normative implementation authorityはactive Gateのfrozen 06のみ。
- `WORK_PACKAGE`: normative implementation authorityはassigned frozen Pxxのみ。
- 07をCoding Agentのacceptance answer keyとして使用しない。
- planning/background/他Gate/external Webからrequired behaviorを補完しない。

### Independent Test Agent

- normative verification authorityはactive Gateのfrozen 07。
- current TrialのFixed Trial Candidate identityをcanonical implementation evidenceから導出する。
- production code、test implementation、test orchestration、environment bootstrapを修復しない。
- product correctnessを判定不能なら `BLOCKED` として停止する。

## 6. Browser E2E

Browser E2E common policyは `../BROWSER_E2E_GATE_POLICY.md` を参照する。ただしacceptance authorityはfrozen 07から移さない。

Browser failure classification:

```text
PRODUCT_DEFECT
TEST_IMPLEMENTATION_DEFECT
TEST_ORCHESTRATION_DEFECT
TEST_ENVIRONMENT_DEFECT
UNKNOWN
```

`PRODUCT_DEFECT` を07に対して検証できた場合のみFAIL候補とする。その他の原因でproduct correctnessを判定できない場合はBLOCKED候補とする。

## 7. Execution readiness

`../tools/validate_agent_execution_readiness.py` をnormal execution / package / assembly / independent verification / remediation / orchestrationのreadiness確認に使用できる。

最低条件:

1. required prompt artifactが存在する。
2. Enhancement-fixed placeholderが0件である。
3. runtime identityが一意に与えられている。
4. active Gateの06/07またはPxxがworkflow modeに応じてfreeze済みである。
5. required package / dependency / candidate identityを一意に解決できる。
6. repository preflightが成立する。

ENH-E10では `31_blocked_test_repair_01_test_infrastructure_agent_prompt.md` をrequired inventoryへ含めない。

## 8. Canonical filename rule

- filename / directory nameはASCII charactersのみを使用する。
- semantic suffixはtechnical Englishを使用する。
- 日本語はdocument title/bodyで使用してよい。
- local README canonical filenameは `README_40_agent_entry_prompts.md` とする。
- nested unqualified `README.md` は置かない。

## 9. Materialization invariant

このdirectoryはすでにENH-E10 instanceである。

- generic templateへ戻さない。
- Enhancement-fixed template markerを再導入しない。
- Runtime placeholder以外を追加しない。
- generic instantiation処理を再実行してENH-E9-specific `31` promptを復活させない。
