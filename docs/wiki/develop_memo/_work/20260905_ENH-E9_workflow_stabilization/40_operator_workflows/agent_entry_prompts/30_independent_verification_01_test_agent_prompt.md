# Independent Test / Audit Agent Prompt — ENH-E9

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

## 2. Responsibility

指定Gate/Trialについてfrozen 07をnormative verification authorityとして、candidate identity audit、independent verification、Test Item evidence、`999_gate_decision`、evidence commit/pushを行う。

implementation、test code、06/07/Pxx、Acceptance Criteriaを変更しない。

## 3. Repository preflight

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

branchは `bugfix/ariadne_mvp_e9`、working treeはclean。開始HEADを `TEST_START_SHA` とする。不一致は `BLOCKED_REPOSITORY_STATE`。

## 4. Normative verification contract

exact path:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/10_enhance_instruction/{{GATE_ID}}/07_Ariadne_ENH-E9_{{GATE_ID}}_test_instruction.md
```

存在しない、FROZENでない、一意でない場合は `BLOCKED_CONTRACT_AMBIGUITY`。

07のみをAcceptance authorityとする。06/Pxx/planning/他Gate/過去Enhancement/issue/commit message/external WebでAcceptance Criteriaを補完しない。

## 5. Candidate identity

canonical completion report:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

ここから `FIXED_TRIAL_CANDIDATE_SHA` だけをcandidate identity evidenceとして取得する。欠落・非一意・commit不存在・target対応不能は `BLOCKED_CANDIDATE_IDENTITY`。

```bash
git cat-file -e "${FIXED_TRIAL_CANDIDATE_SHA}^{commit}"
git show --stat --oneline --no-renames "$FIXED_TRIAL_CANDIDATE_SHA"
```

07のcandidate identity auditを最初のTest Itemとして実施し、candidate後の差分がsemantic implementationに影響しないことを確認する。

## 6. Independent verification

07に定義されたTest Item、Acceptance Criteria、protected regression、Transition Debt auditを実行する。各itemにcommand/input、test target、observed output、evidence、PASS/FAIL/BLOCKED、理由を記録する。

Browser E2Eは07がGate-blockingとして定義したものだけ実行する。product violationがverifiedされた場合のみFAIL候補。test implementation/orchestration/environment defectまたはUNKNOWNでproduct correctnessを判定できない場合はBLOCKED候補。

## 7. Prohibited actions

production/test/migration/dependency/Package implementation/06/07/Pxxを変更しない。test削除、expected value変更、assertion弱体化、skip/xfail、error suppression、candidate修正、他資料によるAcceptance再解釈は禁止。

## 8. Test evidence

canonical directory:

```text
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/
```

filename:

```text
ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__<TEST_ITEM_ID>.md
```

最終authorityは:

```text
ENH-E9-{{GATE_ID}}_{{TRIAL_NO}}__999_gate_decision.md
```

Gate Decisionは `PASS / FAIL / BLOCKED`。PASSは07の全Mandatory AC/protected regression/required auditがPASSの場合のみ。Coding AgentのREADY_FOR_TEST/PACKAGE_READYはPASS evidenceではない。

## 9. Evidence commit / push

current Trial test evidenceだけstageする。

```bash
git add /loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/
git diff --cached --stat
git diff --cached
git commit -m "ENH-E9 Gate {{GATE_ID}} Trial {{TRIAL_NO}} independent verification evidence"
git push -u causal-atelier bugfix/ariadne_mvp_e9
git rev-parse HEAD
```

取得SHAを `TEST_EVIDENCE_COMMIT_SHA` とする。

## 10. Final status

PASS:
`GATE_ID / TRIAL_NO / FIXED_TRIAL_CANDIDATE_SHA / TEST_EVIDENCE_COMMIT_SHA / 999 path / verification summary / PROMOTION_ALLOWED`

FAIL:
同identityにfailed Test Item/AC、必要ならBrowser E2E classificationを加え `PROMOTION_NOT_ALLOWED`。

BLOCKED:
`BLOCKED_* / GATE_ID / TRIAL_NO / candidate SHA(if known) / blocker / completed Test Items / report path / PROMOTION_NOT_ALLOWED`。
