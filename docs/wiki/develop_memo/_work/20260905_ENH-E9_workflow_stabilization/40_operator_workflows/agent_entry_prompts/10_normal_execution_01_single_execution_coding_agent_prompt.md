# Single Execution Coding Agent Prompt — ENH-E9

## 1. Runtime parameters

Human / Orchestrator が実行時に与える値は次の2つだけとする。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

Enhancement fixed values:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E9
ENHANCE_SHORT_ID=ENH-E9
BRANCH_NAME=bugfix/ariadne_mvp_e9
REMOTE_NAME=causal-atelier
WORK_ROOT=/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization
WORK_DIR_NAME=20260905_ENH-E9_workflow_stabilization
```

本実行では `GATE_ID` と `TRIAL_NO` だけをplaceholderへ代入して実行せよ。

## 2. Responsibility

指定された `SINGLE_EXECUTION` Gateについて、repository state確認、freeze済み06 contractの特定、scope内実装、self-verification、Fixed Trial Candidate commit、implementation completion report、evidence commit/pushまでを行い、`READY_FOR_TEST` または明示的な `BLOCKED_*` で終了する。

本AgentはGateの `PASS / FAIL` を判定しない。

## 3. Repository preflight

実装開始前に以下を確認する。

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

- branchは `bugfix/ariadne_mvp_e9`
- working treeはclean
- 開始時HEADを `START_SHA` として記録

不一致や既存uncommitted changeがある場合、reset / restore / stash / commitで処理せず `BLOCKED_REPOSITORY_STATE` で停止する。

current Trial用のfrozen Remediation Contractが存在する場合は通常executionを行わず `BLOCKED_EXECUTION_MODE_MISMATCH` とする。

## 4. Normative implementation contract

次の06 contractをnormative implementation authorityとする。

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/
10_enhance_instruction/
  {{GATE_ID}}/
    06_Ariadne_ENH-E9_{{GATE_ID}}_implementation_instruction.md
```

該当06が存在しない、FROZENでない、または一意に特定できない場合は `BLOCKED_CONTRACT_AMBIGUITY` で停止する。

required behavior / scope / protected invariantは06から取得する。source / test / configurationはimplementation substrateを理解するために調査してよいが、repository現状を仕様authorityとして扱わない。

通常Coding Agentは07、他Gate、過去Enhancement、issue、外部Webを仕様補完のために使用しない。06だけでは実装判断が一意にできない場合は推測せず `BLOCKED_CONTRACT_AMBIGUITY` とする。

## 5. Implementation

06のActive Gate scopeだけを実装する。scope外機能変更、不要refactoring、architecture変更、unrelated cleanup、speculative fix、protected invariant変更を行わない。

scope内で完了できない場合は `BLOCKED_IMPLEMENTATION` とする。

## 6. Self-verification

06が要求するfocused verification / regression verificationを実行し、commandと結果を記録する。

failureは原因を確認し、06 scope内で修正可能な場合だけ修正する。assertion弱体化、test削除、skip/xfail、error suppression、scope外変更による回避は禁止する。

## 7. Fixed Trial Candidate

実装とself-verification完了後、変更を確認する。

```bash
git status
git diff --stat
git diff
```

Active Gate scopeの変更だけをstageし、確認後にcommitする。

```bash
git commit -m "ENH-E9 Gate {{GATE_ID}} Trial {{TRIAL_NO}} implementation candidate"
git rev-parse HEAD
```

取得したSHAを `FIXED_TRIAL_CANDIDATE_SHA` とする。`READY_FOR_TEST` ではimplementation changeをuncommittedで残さない。

## 8. Implementation completion report

以下にreportを作成する。

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/
20_implementation_reports/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
      ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

最低限、`GATE_ID / TRIAL_NO / normative contract path / START_SHA / execution status / changed files / implementation summary / verification commands and results / FIXED_TRIAL_CANDIDATE_SHA / blocker or remaining work` を記録する。

## 9. Evidence commit and push

reportだけを追加stageし、evidence commitを作成してpushする。

```bash
git add /loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
git commit -m "ENH-E9 Gate {{GATE_ID}} Trial {{TRIAL_NO}} implementation evidence"
git push -u causal-atelier bugfix/ariadne_mvp_e9
git log -2 --oneline
git status
```

reportに記録するcandidate identityはevidence commitではなく `FIXED_TRIAL_CANDIDATE_SHA` とする。

## 10. Final status

最終応答では次のいずれかを明示する。

```text
READY_FOR_TEST
BLOCKED_CONTRACT_AMBIGUITY
BLOCKED_REPOSITORY_STATE
BLOCKED_IMPLEMENTATION
BLOCKED_EXECUTION_MODE_MISMATCH
```

`READY_FOR_TEST` の場合は `GATE_ID / TRIAL_NO / START_SHA / FIXED_TRIAL_CANDIDATE_SHA / EVIDENCE_COMMIT_SHA / completion report path / verification summary` を報告する。

BLOCKEDの場合は `GATE_ID / TRIAL_NO / START_SHA / blocker / changed or uncommitted files / report path` を報告する。
