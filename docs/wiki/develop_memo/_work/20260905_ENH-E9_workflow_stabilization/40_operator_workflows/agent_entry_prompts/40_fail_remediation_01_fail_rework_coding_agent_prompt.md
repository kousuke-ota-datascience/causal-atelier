# FAIL Rework Coding Agent Prompt — ENH-E9

formal FAIL後のrework専用entry prompt。

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
ENHANCE_SHORT_ID=ENH-E9
BRANCH_NAME=bugfix/ariadne_mvp_e9
REMOTE_NAME=causal-atelier
WORK_ROOT=/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization
WORK_DIR_NAME=20260905_ENH-E9_workflow_stabilization
```

`REMEDIATION_PACKAGE_ID` はHuman入力にしない。current Trialの08が `CONSOLIDATED / SINGLE_EXECUTION` であることをpreflightし、このpromptではGate単位reworkとして実行する。

## 2. Current Trial Remediation Contract

唯一のnormative contract:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/10_enhance_instruction/{{GATE_ID}}/08_ENH-E9_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
```

不存在は `BLOCKED_REMEDIATION_CONTRACT_MISSING`。

08が以下を満たすこと。

```text
Remediation Mode: CONSOLIDATED
Execution Mode: SINGLE_EXECUTION
```

満たさなければ `BLOCKED_REMEDIATION_CONTRACT_NOT_SELF_CONTAINED`。

current 08だけをnormative sourceとする。original 06/Pxx/07、旧Trial、他Gate、過去Enhancement、external Webで仕様補完しない。ambiguityは `BLOCKED_CONTRACT_AMBIGUITY`。

## 3. Rework

original Work Package chainを再実行しない。old checkpointを再利用しない。previous failed candidateを再提出しない。

Browser E2E formal FAILの場合、failed evidenceがproduct/contract violationをsupportしていることを確認する。test implementation/orchestration/environment defect/UNKNOWNだけならproduction reworkせず `BLOCKED_REMEDIATION_HANDOFF_INCOMPLETE`。

08のrequired correction/protected behaviorだけを実装し、mandatory Coding-side verificationを実行する。test削除、assertion弱体化、skip/xfail、original contract改変は禁止。

## 4. Semantic checkpoint / candidate

semantic changeをcommitし `IMPLEMENTATION_CHECKPOINT_SHA` を取得する。08の `PREVIOUS_FAILED_CANDIDATE_SHA` と比較し、08が要求するsemantic remediation diffが存在することを確認する。存在しなければ `BLOCKED_REMEDIATION_NOT_APPLIED`。

verification PASSかつsemantic diff存在時のみ:

```text
FIXED_TRIAL_CANDIDATE_SHA=<IMPLEMENTATION_CHECKPOINT_SHA>
```

とfreezeする。

## 5. Canonical completion report

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

最低限 `GATE_ID / TRIAL_NO / Execution status / PREVIOUS_FAILED_CANDIDATE_SHA / FIXED_TRIAL_CANDIDATE_SHA / changed production/test files / verification / blocker` を記録する。

`READY_FOR_TEST` には `new candidate != previous candidate / required semantic diff != empty / verification PASS / blocker NONE` が必要。

## 6. Evidence commit / push

Completion Reportをevidence-only commitとしてcommitし、

```bash
git push -u causal-atelier bugfix/ariadne_mvp_e9
```

する。candidateからevidence HEADまでsemantic implementation changeがないことを確認する。

## 7. Final status

成功時:

```text
READY_FOR_TEST
GATE_ID
TRIAL_NO
PREVIOUS_FAILED_CANDIDATE_SHA
FIXED_TRIAL_CANDIDATE_SHA
COMPLETION_REPORT
EVIDENCE_COMMIT_SHA
Working tree: clean
Push: completed
```

Gate PASS/FAIL、promotion可否は判定しない。
