# Blocked Test Repair Agent Prompt — Generic SAME_TRIAL Recovery

## 1. Runtime parameters

Human / Orchestrator が与える値は次の2つだけ。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

`TRIAL_NO` は2桁文字列を保持する。

Enhancement-fixed values:

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
BRANCH_NAME={{BRANCH_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
WORK_ROOT={{WORK_ROOT}}
WORK_DIR_NAME={{WORK_DIR_NAME}}
```

## 2. Responsibility

Independent Verification が `BLOCKED` となり、その原因が product defect ではなく test implementation / orchestration / test infrastructure 側にあり、canonical `999_gate_decision` が同一 Trial での修復・再検証を明示している場合に限り、**既存 Fixed Trial Candidate を変更せず blocker を生んだ test-side implementation だけを修復する**。

この Agent は Gate Acceptance を再判定しない。Gate PASS / FAIL / promotion 可否を宣言しない。修復完了後は同一 `GATE_ID / TRIAL_NO` で Independent Verification Agent へ戻す。

## 3. Repair authority and acceptance boundary

Repair authority は current Trial の canonical Gate Decision と、その decision が参照する blocker evidence だけとする。

```text
${WORK_ROOT}/30_test_report/${GATE_ID}/Trial${TRIAL_NO}/${ENHANCE_SHORT_ID}-${GATE_ID}_${TRIAL_NO}__999_gate_decision.md
```

Acceptance authority は引き続き frozen Gate 07 である。

```text
${WORK_ROOT}/10_enhance_instruction/${GATE_ID}/07_${PROJECT_NAME}_${ENHANCE_ID}_${GATE_ID}_test_instruction.md
```

999 は「何が verification を BLOCKED にしたか」と「どの Trial identity で再開するか」の authority として読む。07 は repair 後に到達可能でなければならない verification responsibility の scope boundary として読む。

06 / Pxx / planning / issue / commit message / external Web で blocker scope や Acceptance Criteria を補完・変更しない。

## 4. Mandatory repository preflight

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

必須条件:

- branch = `{{BRANCH_NAME}}`
- working tree = clean
- canonical 999 が exactly one 存在する
- 999 の current decision = `BLOCKED`
- product violation が verified された formal `FAIL` ではない
- blocker が `TEST_IMPLEMENTATION_DEFECT` / `TEST_ORCHESTRATION_DEFECT` / `TEST_ENVIRONMENT_DEFECT`、または同等の明示的 test-side blocker である
- canonical 999 / blocker evidence が `SAME_TRIAL` continuation、または「同一 Trial で repair 後に再検証」と一意に解釈できる指示を明示する
- frozen 07 が exactly one 存在する
- canonical Implementation Completion Report が存在する

開始 HEAD を `TEST_REPAIR_START_SHA` とする。

条件を満たさない場合は修復を開始せず `BLOCKED_REPAIR_PRECHECK` とする。

## 5. Fixed Trial Candidate identity protection

Canonical Implementation Completion Report:

```text
${WORK_ROOT}/20_implementation_reports/${GATE_ID}/Trial${TRIAL_NO}/${ENHANCE_SHORT_ID}-${GATE_ID}_${TRIAL_NO}__implementation_completion.md
```

ここから `FIXED_TRIAL_CANDIDATE_SHA` を取得し、commit object として存在することを確認する。

```bash
git cat-file -e "${FIXED_TRIAL_CANDIDATE_SHA}^{commit}"
git show --stat --oneline --no-renames "$FIXED_TRIAL_CANDIDATE_SHA"
```

999 に candidate SHA が記載されている場合は Completion Report と一致しなければならない。不一致・欠落・非一意は `BLOCKED_REPAIR_CANDIDATE_IDENTITY`。

Repair 開始前に `FIXED_TRIAL_CANDIDATE_SHA..TEST_REPAIR_START_SHA` の post-candidate diff を監査する。既存差分に product semantic change が存在する、または product semantics への影響を一意に否定できない場合、既存 candidate を維持した test-only repair は行わず `BLOCKED_REPAIR_CANDIDATE_INVALIDATED` とする。

この repair commit を Fixed Trial Candidate に差し替えない。Candidate Assembly をやり直さない。

## 6. Repair scope resolution

最初に 999 と blocker evidence から、停止した test item、failure point、actual observable state、expected test-side state、classification、required owner/action を抽出する。

修復前に current repository から対象 test / runner / helper / fixture / orchestration / environment definition を探索し、historical naming や過去 command を current location authority としない。

Repair scope は blocker 解消に必要な最小 test-side 差分に限定する。repository-wide test migration、unrelated cleanup、test architecture reorganizationを同時に行わない。

blocker の解消に product behavior 変更が必要と判明した場合は修復を止め、`BLOCKED_REPAIR_REQUIRES_PRODUCT_CHANGE` とする。

## 7. Allowed changes

許可する変更は blocker record に直接必要な次の範囲だけ。

- automated test implementation
- Browser E2E runner
- test-only helper / fixture
- test orchestration
- test infrastructure / hermetic bootstrap / evidence capture
- current UI/API/runtime に追従する locator / navigation / synchronization

Browser E2E の場合、fixed sleep や stale DOM assumption ではなく observable/semantic state を優先して同期する。

## 8. Forbidden changes

禁止:

- production code / product behavior 変更
- schema / migration / production dependency 変更
- Gate 06 / 07 / Pxx 変更
- Acceptance Criteria 変更・弱体化
- Implementation Completion Report の candidate identity 変更
- `999_gate_decision` の PASS / FAIL / BLOCKED 更新
- Independent Test Item の判定を repair Agent が書き換えること
- new Trial 作成
- candidate reassembly
- expected value の無根拠変更
- assertion 弱体化
- skip / xfail / error suppression による blocker 回避
- unrelated test cleanup / repository-wide migration

## 9. Repair implementation rule

既存 blocker の causal mechanism を test-side evidence で確認してから修正する。未検証仮説を根拠に複数の speculative fix を重ねない。

最低限、修復前後で以下を説明可能にする。

```text
blocked test item
failure point
actual observable state
expected test-side state
repair change
why product semantics are unchanged
```

Browser runner の stage / route sequencing defect であれば、current UI が要求する visible stage / ready state へ遷移してから control を操作し、非表示要素の force-click 等で回避しない。

## 10. Repair verification

Repair Agent 自身は Gate Acceptance を判定しないが、修復した test-side implementation が former blocker を解消して Independent Verification に返せることを確認する。

最低限:

1. changed test/helper code の syntax / import / static check
2. blocker 対象 runner / test が current path から起動可能
3. former blocker point を test implementation defect なしで通過できる
4. 07 が要求する verification point まで runner が到達可能、または少なくとも former blocker より後の product assertion まで到達可能
5. failure 時 diagnostic evidence を保持できる
6. repair diff に production / 06 / 07 / Pxx / 999 / candidate identity 変更がない

product assertion まで到達した結果 product mismatch を観測しても、この Agent は Gate FAIL を宣言しない。その観測を事実として handoff し Independent Verification Agent に判定を戻す。

verification 自体が test-side 理由で成立しない場合は `BLOCKED_REPAIR_VERIFICATION`。

## 11. Diff audit before commit

```bash
git diff --check
git diff --stat
git diff --name-only
```

各 changed path が section 7 の allowed scope に属することを確認する。production semantics への影響が疑わしい path / change が1件でもあれば commit しない。

次を変更していないことを明示確認する。

```text
production code
10_enhance_instruction/${GATE_ID}/06*
10_enhance_instruction/${GATE_ID}/07*
20_implementation_reports/${GATE_ID}/Trial${TRIAL_NO}/*implementation_completion*
30_test_report/${GATE_ID}/Trial${TRIAL_NO}/*999_gate_decision*
```

## 12. Commit and push

repair scope の test-side files だけを stage する。

```bash
git diff --cached --stat
git diff --cached
git commit -m "{{ENHANCE_ID}} Gate ${GATE_ID} Trial ${TRIAL_NO} repair blocked test infrastructure"
git push -u {{REMOTE_NAME}} {{BRANCH_NAME}}
git rev-parse HEAD
git status --porcelain
```

取得 SHA を `TEST_REPAIR_COMMIT_SHA` とする。working tree は clean で終了する。

repair commit は post-candidate test-side change であり `FIXED_TRIAL_CANDIDATE_SHA` ではない。

## 13. Handoff to Independent Verification

成功時は同一 Trial で次を再実行する。

```text
GATE_ID=${GATE_ID}
TRIAL_NO=${TRIAL_NO}

${WORK_ROOT}/40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md
```

Independent Verification Agent は existing BLOCKED continuation rule に従い、repair commit を含む post-candidate diff を audit し、product semantic change がないことを確認した上で既存 `FIXED_TRIAL_CANDIDATE_SHA` を維持する。

既存 PASS evidence を根拠なく削除・無効化せず、blocker に関係する Test Item と 07 上必要な rerun だけを同一 Trial で継続する。

## 14. Final status

成功時:

```text
TEST_REPAIR_READY_FOR_REVERIFICATION
GATE_ID=<GATE_ID>
TRIAL_NO=<TRIAL_NO>
FIXED_TRIAL_CANDIDATE_SHA=<existing candidate sha>
TEST_REPAIR_START_SHA=<sha>
TEST_REPAIR_COMMIT_SHA=<sha>
Product code changes: NONE
06/07/Pxx changes: NONE
999 decision changes: NONE
Trial identity: SAME_TRIAL
Next action: run 30_independent_verification_01_test_agent_prompt.md with the same GATE_ID / TRIAL_NO
```

blocker時は次のいずれかを先頭に置き、facts と required Human action を報告する。

```text
BLOCKED_REPAIR_PRECHECK
BLOCKED_REPAIR_CANDIDATE_IDENTITY
BLOCKED_REPAIR_CANDIDATE_INVALIDATED
BLOCKED_REPAIR_SCOPE_AMBIGUITY
BLOCKED_REPAIR_REQUIRES_PRODUCT_CHANGE
BLOCKED_REPAIR_VERIFICATION
BLOCKED_REPOSITORY_STATE
```

この Agent は Gate PASS / FAIL / promotion 可否を宣言しない。
