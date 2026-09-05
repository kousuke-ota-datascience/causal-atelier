# Work Package Candidate Assembly Agent Prompt — ENH-E9

## 1. Runtime parameters

Human / Orchestrator が与える値は次の2つだけ。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

`TRIAL_NO` は2桁文字列を保持する。

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

## 2. Responsibility

WORK_PACKAGE Gateの全required Package completion、checkpoint SHA、Git ancestryを監査し、Gate-wide implementation-side verificationを実行してFixed Trial Candidateをfreezeする。Implementation Completion Reportを作成しevidence commit/pushする。

production/test/schema/dependencyを変更しない。implementation補修、Gate PASS/FAIL判定、independent verificationを行わない。

## 3. Authorities

Gate directory:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/10_enhance_instruction/{{GATE_ID}}/
```

Gate 06、P00、required Pxxをassembly authorityとする。Package reports:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/packages/
```

## 4. Preflight / package audit

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

branchは `bugfix/ariadne_mvp_e9`、candidate identityに影響するuncommitted changeがあれば `BLOCKED_REPOSITORY_STATE`。

P00/06でrequired Packageを列挙し、各canonical package reportの `Gate / Package / Trial / State: PACKAGE_COMPLETE / PACKAGE_CHECKPOINT_SHA / blocker` を確認する。欠落・未完了は `BLOCKED_PACKAGE_INCOMPLETE`。

各checkpointがGit objectとして存在し、required package chainのancestryに包含されることを確認する。分岐・非包含・一意性欠如は `BLOCKED_CANDIDATE_CHAIN`。

## 5. Gate-wide self-verification

Gate 06/P00が要求するintegration/regression/static/build等のimplementation-side verificationを実行する。これは07 independent verificationの代替ではない。

失敗時は修正せず `BLOCKED_INTEGRATION_VERIFICATION`。

## 6. Fixed Trial Candidate

全audit/verification成功時、全required Package semantic implementationを包含するexact SHAを

```text
FIXED_TRIAL_CANDIDATE_SHA=<exact SHA>
```

としてfreezeする。evidence-only commitを理由なくcandidateにしない。一意に決められなければ `BLOCKED_CANDIDATE_IDENTITY`。

## 7. Canonical Implementation Completion Report

唯一のcanonical path:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

reportには最低限以下を記録する。

```text
PROJECT_NAME: Ariadne
ENHANCE_ID: ENH-E9
GATE_ID
TRIAL_NO
Execution status
FIXED_TRIAL_CANDIDATE_SHA
required Package list
PACKAGE_CHECKPOINT_SHA per Package
Package completion status
Gate-wide self-verification
Blocker / remaining work
```

正常時:

```text
Execution status: READY_FOR_TEST
Blocker / remaining work: NONE
```

作成後 `test -f` と `grep -n 'FIXED_TRIAL_CANDIDATE_SHA'` で確認する。

## 8. Evidence commit / push

Completion Reportのみstageする。

```bash
git add /loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
git commit -m "ENH-E9 Gate {{GATE_ID}} Trial {{TRIAL_NO}} candidate assembly evidence"
git push -u causal-atelier bugfix/ariadne_mvp_e9
git rev-parse HEAD
git status
```

## 9. Final status

正常時:

```text
READY_FOR_TEST
GATE_ID
TRIAL_NO
FIXED_TRIAL_CANDIDATE_SHA
Implementation Completion Report path
EVIDENCE_COMMIT_SHA
```

block時は `BLOCKED_REPOSITORY_STATE / BLOCKED_PACKAGE_INCOMPLETE / BLOCKED_CANDIDATE_CHAIN / BLOCKED_INTEGRATION_VERIFICATION / BLOCKED_CANDIDATE_IDENTITY / BLOCKED_CONTRACT_AMBIGUITY` の該当値とevidenceを報告する。
