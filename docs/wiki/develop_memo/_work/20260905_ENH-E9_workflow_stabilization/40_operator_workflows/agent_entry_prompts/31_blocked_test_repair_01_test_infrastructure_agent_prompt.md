# Blocked Test Repair Agent Prompt — ENH-E9 G02 Trial01 Special Handling

> **Special handling notice:** このpromptは、ENH-E9 G02 Trial01 のIndependent Verificationが `BLOCKED` となり、そのblockerが `TEST_IMPLEMENTATION_DEFECT` と分類され、かつ `SAME_TRIAL` continuationが明示されたことへの限定的な対処専用である。
>
> 本promptはrepository-wide test architecture migrationの一般実行promptではない。formal `FAIL` remediationでもない。G03以降や他Trialへ自動適用してはならない。将来同種の一般routeが必要になった場合は、別途generic workflowとして設計する。

## 1. Runtime parameters

Human / Orchestrator が与える値は次の2つだけ。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

Fixed values:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E9
BRANCH_NAME=bugfix/ariadne_mvp_e9
REMOTE_NAME=causal-atelier
WORK_ROOT=/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization
```

このpromptの有効なruntime identityはexactly次だけである。

```text
GATE_ID=G02
TRIAL_NO=01
```

異なる値が与えられた場合は実行せず `BLOCKED_SPECIAL_REPAIR_SCOPE_MISMATCH` とする。

## 2. Purpose and authority boundary

目的は、G02 Trial01の既存Fixed Trial Candidateを変更せず、既存Independent VerificationをBLOCKEDにしたBrowser E2E test implementation / orchestration defectだけを修正し、同一TrialのIndependent Verification再開を可能にすることである。

このpromptでproduct correctnessやGate PASS/FAILを判定しない。

Repair authorityは既存canonical Gate Decisionのblocker recordとする。

```text
${WORK_ROOT}/30_test_report/G02/Trial01/ENH-E9-G02_01__999_gate_decision.md
```

Acceptance authorityは引き続きfrozen G02 07である。

```text
${WORK_ROOT}/10_enhance_instruction/G02/07_Ariadne_ENH-E9_G02_test_instruction.md
```

999は「何がBLOCKEDを生んだか」のrepair inputとして読む。07はrepair後に満たすべきBrowser verification responsibilityのscope boundaryとして読む。06/Pxx/他Gate/過去EnhancementでAcceptance Criteriaを補完・変更しない。

## 3. Mandatory preflight

次を確認する。

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

必須条件:

- branch = `bugfix/ariadne_mvp_e9`
- working tree = clean
- `GATE_ID=G02`
- `TRIAL_NO=01`
- canonical 999が存在する
- 999 status = `BLOCKED`
- blocker classification = `TEST_IMPLEMENTATION_DEFECT` または明示的なtest-side implementation/orchestration blocker
- Trial identity handling = `SAME_TRIAL`
- Fixed Trial Candidate SHA = `8cf70523093efa53b59a7de2c655f9755dbceb8d`
- frozen G02 07が存在する

上記が満たされない場合は修正を開始しない。

formal product `FAIL` が成立している場合、このpromptを使用せずformal FAIL remediation routeへ戻す。

## 4. Protected identities

このrepairでは以下を変更しない。

```text
GATE_ID=G02
TRIAL_NO=01
FIXED_TRIAL_CANDIDATE_SHA=8cf70523093efa53b59a7de2c655f9755dbceb8d
07 verification contract
Acceptance Criteria
```

新しいTrialを作成しない。Candidate reassemblyを行わない。Implementation Completion ReportのFixed Trial Candidateをtest repair commitへ置き換えない。

## 5. Repair scope

既存999が記録したblockerを解消するため、Browser E2E test implementation / orchestrationだけを修正または追加する。

既存blockerの核心は、historical `tests/browser_e2e/run_enh_e1a.py` がcurrent UI navigationより古いlocator / flowを前提とし、G02 scenarioへ到達する前に停止したことである。

repair後のBrowser E2Eは、G02 07が要求するcross-layer connectivityをcurrent UIで確認できなければならない。

対象journey:

```text
Project List
-> New Project
-> current Analysis route/context
-> Discovery execution
-> Graph Candidate review
-> Graph Comparison
-> adopt / FIXED Graph
```

Browser E2EはG02の詳細Graph correctnessやscientific semanticsのprimary proofにしない。それらはnon-browser testsの責務である。

## 6. Test architecture placement

ENH-E9 minimum migration policyに従い、新規またはmaterially rebuiltなG02 Browser E2Eは原則として次へ配置する。

```text
tests/enhancement/enh_e9/g02/browser_e2e/
```

推奨例:

```text
tests/enhancement/enh_e9/g02/browser_e2e/run_discovery_candidate_adoption.py
```

filenameは実装内容に応じて変更してよいが、Enhancement / Gate / layer authorityがpathから明確であること。

historical `run_enh_e1a.py` 全体をcurrent canonical regressionへ昇格させる目的で全面修復しない。G02 07に必要なjourneyをcurrent UI/runtimeへ合わせて最小実装する。

既存current helper/fixtureを再利用してよい。ただしhistorical runnerへの不要なdependency chainを持ち込まない。

## 7. Allowed changes

許可する変更:

- `tests/enhancement/enh_e9/g02/browser_e2e/` 配下のBrowser E2E test implementation
- 必要最小限のtest-only helper / fixture / orchestration code
- current UI locator / navigation / synchronizationへの追従
- Browser evidence captureのtest-side改善
- M02 execution evidenceの追記

既存test fileの移動・再利用が必要な場合は、current test architecture migration policyと整合させ、path/import/fixture dependencyを同じcommit範囲で解消する。

## 8. Forbidden changes

禁止:

- production code変更
- `frontend/` や `src/` のproduct behavior変更
- 06 / 07 / Pxx変更
- Acceptance Criteria変更
- Fixed Trial Candidate変更
- new Trial作成
- 999 Gate DecisionのPASS/FAIL/BLOCKED更新
- Independent Test Itemの判定変更
- test assertion弱体化
- skip / xfailによるblocker回避
- expected valueのproduct側に合わせた無根拠変更
- Browser failureの握り潰し
- repository-wide comprehensive test migration

product changeなしではrepair不能と判明した場合は修正を止め、`BLOCKED_REPAIR_REQUIRES_PRODUCT_CHANGE` として報告する。

## 9. Current UI / runner investigation

実装前に、current repositoryから以下を確認する。

- Project List / New Projectのcurrent DOM / route
- project作成後のcurrent route
- Analysis family / Stage navigation
- Discovery execution entry
- candidate review / comparison UI
- adopt / FIXED操作
- current Browser runner / helperのうち再利用可能なもの

historical namingだけでrunnerをauthorityとしない。current codeとobservable UI stateをauthorityとしてtest implementationを組み立てる。

fixed sleepをprimary synchronization mechanismにしない。route、visible element、enabled state、network/output condition等のobservable conditionを優先する。

## 10. Repair verification

repair Agent自身はGate Acceptanceを判定しないが、修正したtest implementationが少なくともrunnerとして成立することを確認する。

最低限:

1. syntax / import check
2. target Browser runnerがcurrent test pathから起動可能
3. stale initial locatorで停止しない
4. G02 journeyの各required checkpointへ到達する
5. screenshot/log/current route/last successful checkpoint等、失敗時diagnostic evidenceを残せる
6. product code diffがないことを確認する

Browser journeyがproduct assertionまで到達した結果product behavior mismatchを観測しても、このAgentはGate FAILを宣言しない。repair自体が成立したことと観測事実を分離して記録し、Independent Test Agentへhandoffする。

## 11. M02 execution record

次へM02を追記する。

```text
${WORK_ROOT}/00_enhance_background/08_test_architecture_migration/05_execution_record.md
```

最低限記録する。

```text
Batch ID: M02
Purpose: G02 Trial01 BLOCKED test implementation repair
Before SHA
After SHA
Changed test/test-infrastructure paths
Product code changes: NONE
Fixed Trial Candidate impact: NONE
Trial identity: SAME_TRIAL / G02 Trial01
Repair verification commands/results
Remaining blocker
Next action: Independent Verification continuation
```

M02はrepository-wide migration batchではなく、ENH-E9 minimum migration方針下で必要になったG02 Trial01のblocker correctionとして記録する。

## 12. Commit and push

修正対象とM02 execution evidenceだけをstageする。

```bash
git diff --stat
git diff --check
git status --porcelain
```

product code、06/07/Pxx、30_test_reportのGate Decisionがstagedされていないことを確認する。

repair commitを作成しpushする。

```bash
git commit -m "ENH-E9 G02 Trial01 repair blocked browser test implementation"
git push -u causal-atelier bugfix/ariadne_mvp_e9
git rev-parse HEAD
```

取得SHAを `TEST_REPAIR_COMMIT_SHA` とする。

## 13. Final status

成功時:

```text
TEST_REPAIR_READY_FOR_REVERIFICATION
GATE_ID=G02
TRIAL_NO=01
FIXED_TRIAL_CANDIDATE_SHA=8cf70523093efa53b59a7de2c655f9755dbceb8d
TEST_REPAIR_COMMIT_SHA=<sha>
M02_EXECUTION_RECORD=<path>
Product code changes: NONE
07 changes: NONE
Trial identity: SAME_TRIAL
Next action: run 30_independent_verification_01_test_agent_prompt.md with GATE_ID=G02 / TRIAL_NO=01
```

blocker時:

```text
BLOCKED_TEST_REPAIR
GATE_ID=G02
TRIAL_NO=01
FIXED_TRIAL_CANDIDATE_SHA=8cf70523093efa53b59a7de2c655f9755dbceb8d
BLOCKER=<classification>
DETAIL=<facts>
Product code changes: NONE unless explicitly reported as prohibited requirement
Next action: operator review
```

このAgentはGate PASS/FAIL、promotion可否を宣言しない。
