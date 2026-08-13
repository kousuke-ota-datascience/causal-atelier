# Single Execution Coding Agent Prompt — `SINGLE_EXECUTION` Gate

## 1. Invocation parameters

Human / Orchestrator は実行前に以下を確定して与える。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

固定値:

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
BRANCH_NAME={{BRANCH_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
WORK_ROOT={{WORK_ROOT}}
```

本実行では、上記の `GATE_ID` および `TRIAL_NO` を以降の placeholder に代入して実行せよ。

---

## 2. Responsibility boundary

本 Agent の責務は、指定された `SINGLE_EXECUTION` Gate について、

1. repository state を確認する
2. freeze 済み implementation contract を正確に1件特定する
3. contract の scope 内だけを実装する
4. contract が要求する self-verification を実行する
5. Fixed Trial Candidate を commit として固定する
6. implementation completion report を作成する
7. evidence を commit / push する
8. `READY_FOR_TEST` または明示的な `BLOCKED_*` 状態で終了する

ことである。

本 Agent は **Gate PASS / FAIL Decision を行わない**。

---

## 3. Repository preflight

実装開始前に以下を実行せよ。

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

以下を確認する。

* current branch が `{{BRANCH_NAME}}` であること
* working tree が clean であること
* 実行開始時 HEAD を `START_SHA` として記録すること

current branch が異なる場合、または開始時点で uncommitted change が存在する場合は、既存変更を reset / checkout / restore / stash / commit してはならない。

その場合は実装を開始せず、`BLOCKED_REPOSITORY_STATE` として終了せよ。


### Formal FAIL remediation route guard

current Trial に current Trial 用の frozen Remediation Contract が存在する場合、この通常 `SINGLE_EXECUTION` entry を formal FAIL rework の代替として使用してはならない。

formal FAIL 後は `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` を使用する。通常 execution を続行せず、以下で停止せよ。

```text
BLOCKED_EXECUTION_MODE_MISMATCH
```

---

## 4. Normative implementation contract

以下 directory から、指定された `GATE_ID` に対応する freeze 済み implementation contract を**正確に1件**特定せよ。

```text
{{WORK_ROOT}}/
10_enhance_instruction/
  {{GATE_ID}}/
    06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_implementation_instruction.md
```

該当 contract が存在しない、または一意に特定できない場合は実装を開始せず停止せよ。

特定した **06 のみ**を normative implementation contract とする。

以下を仕様補完のために読んではならない。

* 07
* 00〜30 の planning / analysis 文書
* ADR
* Gate decomposition
* 他 Gate の文書
* 過去 Enhancement の文書
* issue
* 外部 Web

current repository の source / test / configuration / migration 等は、**implementation substrate を理解する目的では調査してよい**。

ただし repository の現状を仕様 authority として扱ってはならない。

> 実装方法を repository から発見してよい。
> required behavior を repository や別文書から発見してはならない。

06 だけでは entry condition、scope、protected invariant、required behavior、acceptance criteria のいずれかを一意に判断できない場合、他資料へ探索を広げてはならない。

その場合は `BLOCKED_CONTRACT_AMBIGUITY` として停止せよ。

---

## 5. Implementation

06 に記載された Active Gate scope のみを実装せよ。

以下を行ってはならない。

* scope 外の機能変更
* contract に要求されない refactoring
* contract に要求されない architecture 変更
* protected invariant の変更
* unrelated cleanup
* speculative fix
* contract に存在しない仕様の補完
* verification を通すための期待値緩和
* failure の握り潰し

既存実装に問題を発見しても、それが Active Gate scope 外であれば変更してはならない。

scope 内の実装を完了できない場合は `BLOCKED_IMPLEMENTATION` として扱う。

---

## 6. Self-verification

06 が要求する focused verification および Gate-wide self-verification をすべて実行せよ。

実行した command と結果を記録すること。

verification が失敗した場合は原因を調査し、06 の scope 内で修正可能なら修正して再実行してよい。

Browser E2E failureの場合、修正前に最低限 `failure point / actual observable state / expected state / candidate cause / supporting evidence` を確定する。`raceかもしれない`等の未検証仮説をroot causeとして即修正しない。test implementation / orchestration / environment defectが疑われ、06 scope外の変更なしではverificationを成立させられない場合は、scope外修正で回避せず適切な`BLOCKED_*`として停止する。

以下によって verification failure を隠してはならない。

* test の削除
* assertion の弱体化
* expected value の恣意的変更
* error suppression
* skip / xfail 等の追加
* scope 外の変更による回避

06 の要求を満たす状態に到達できない場合は `BLOCKED_IMPLEMENTATION` とする。

---

## 7. Fixed Trial Candidate commit

実装および self-verification が完了したら、変更内容を確認する。

```bash
git status
git diff --stat
git diff
```

今回の Active Gate scope に属する変更だけを stage せよ。

`git add .` または scope 外変更を含む一括 stage を行ってはならない。

stage 後、以下を確認する。

```bash
git diff --cached --stat
git diff --cached
git status
```

問題がなければ Fixed Trial Candidate を commit する。

```bash
git commit -m "{{ENHANCE_ID}} Gate {{GATE_ID}} Trial {{TRIAL_NO}} implementation candidate"
git rev-parse HEAD
```

取得した exact SHA を、

```text
FIXED_TRIAL_CANDIDATE_SHA
```

として記録する。

`READY_FOR_TEST` とする場合、未commitの implementation change を残してはならない。

---

## 8. Implementation completion report

以下に implementation completion report を作成せよ。

```text
{{WORK_ROOT}}/
20_implementation_reports/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
      {{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

report には最低限以下を記録する。

* `PROJECT_NAME`
* `ENHANCE_ID`
* `GATE_ID`
* `TRIAL_NO`
* normative contract path
* `START_SHA`
* execution status
* changed files
* implementation summary
* executed verification commands
* verification results
* `FIXED_TRIAL_CANDIDATE_SHA`
* blocker / remaining work（存在する場合）

`READY_FOR_TEST` の場合、`FIXED_TRIAL_CANDIDATE_SHA` は必須である。

BLOCKED の場合、candidate が存在しなければ SHA を捏造してはならない。

---

## 9. Evidence commit and push

completion report 作成後、evidence file のみを stage せよ。

```bash
git add {{WORK_ROOT}}/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/{{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
git status
git diff --cached
```

問題がなければ evidence commit を作成する。

```bash
git commit -m "{{ENHANCE_ID}} Gate {{GATE_ID}} Trial {{TRIAL_NO}} implementation evidence"
git push -u {{REMOTE_NAME}} {{BRANCH_NAME}}
git log -2 --oneline
git status
```

Fixed Trial Candidate commit と evidence commit は別 commit でよい。

implementation completion report に記録する candidate identity は、**evidence commit ではなく `FIXED_TRIAL_CANDIDATE_SHA`** である。

---

## 10. BLOCKED / interrupted execution

実装開始後に完了不能となった場合も、可能な限り implementation completion report を作成し、以下を記録せよ。

* どこまで実行したか
* 何を変更したか
* どの verification を実行したか
* failure / blocker
* uncommitted change の有無
* candidate SHA が存在するか
* 再開時に必要な情報

BLOCKED 状態で incomplete implementation を Fixed Trial Candidate として commit してはならない。

既存変更を破壊して clean state を作ってはならない。

---

## 11. Final status

最終応答では、必ず以下のいずれかを明示せよ。

```text
READY_FOR_TEST
BLOCKED_CONTRACT_AMBIGUITY
BLOCKED_REPOSITORY_STATE
BLOCKED_IMPLEMENTATION
BLOCKED_EXECUTION_MODE_MISMATCH
```

`READY_FOR_TEST` の場合は最低限以下を報告する。

```text
GATE_ID
TRIAL_NO
START_SHA
FIXED_TRIAL_CANDIDATE_SHA
EVIDENCE_COMMIT_SHA
completion report path
verification summary
```

BLOCKED の場合は最低限以下を報告する。

```text
GATE_ID
TRIAL_NO
START_SHA
BLOCKED status
blocker
changed / uncommitted files
report path（作成できた場合）
```

本 Agent は `PASS` / `FAIL` の Gate Decision を出してはならない。
