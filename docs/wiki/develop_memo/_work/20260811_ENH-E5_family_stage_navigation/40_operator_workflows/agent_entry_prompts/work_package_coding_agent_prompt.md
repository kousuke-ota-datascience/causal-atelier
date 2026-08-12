# Work Package Coding Agent Prompt — ENH-E5

## 1. Invocation parameters

Human / Orchestrator は実行前に以下を確定して与える。

```text
GATE_ID={{GATE_ID}}
PACKAGE_ID={{PACKAGE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

固定値:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E5
BRANCH_NAME=feature/ariadne_mvp_e5
REMOTE_NAME=causal-atelier
```

本実行では、上記の `GATE_ID`、`PACKAGE_ID`、`TRIAL_NO` を以降の placeholder に代入して実行せよ。

---

## 2. Responsibility boundary

本 Agent の責務は、指定された Work Package について、

1. repository state を確認する
2. assigned freeze 済み Pxx contract を正確に1件特定する
3. assigned Package scope のみを実装する
4. assigned Pxx が要求する focused verification を実行する
5. Package checkpoint を commit として固定する
6. Package checkpoint/status report を作成する
7. evidence を commit / push する
8. `PACKAGE_READY` または明示的な `BLOCKED_*` 状態で終了する

ことである。

本 Agent は以下を行わない。

* 他 Package の実行
* 次 Package の選択
* Gate orchestration
* Fixed Trial Candidate の assembly
* Gate PASS / FAIL Decision

ただし assigned Pxx が明示的に別の責務を要求する場合は、その Pxx の記載を優先する。

---

## 3. Repository preflight

実装開始前に以下を実行せよ。

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

以下を確認する。

* current branch が `feature/ariadne_mvp_e5` であること
* working tree が clean であること
* 実行開始時 HEAD を `START_SHA` として記録すること

current branch が異なる場合、または開始時点で uncommitted change が存在する場合は、既存変更を reset / checkout / restore / stash / commit してはならない。

その場合は実装を開始せず `BLOCKED_REPOSITORY_STATE` として終了せよ。

---

## 4. Assigned Work Package contract

以下 directory から、指定された `GATE_ID` および `PACKAGE_ID` に対応する freeze 済み Work Package contract を**正確に1件**特定せよ。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/
  {{GATE_ID}}/
    06_{{GATE_ID}}_{{PACKAGE_ID}}_*.md
```

semantic match が0件または複数存在する場合、任意のファイルを選択してはならない。

その場合は実装を開始せず停止せよ。

特定した **assigned Pxx のみ**を normative implementation contract とする。

以下を仕様補完のために読んではならない。

* Gate-level 06 Contract
* 07
* P00
* 他 Pxx
* 00〜30 の planning / analysis 文書
* ADR
* 過去 Enhancement
* issue
* 外部 Web

current repository の source / test / configuration / migration 等は、**implementation substrate を理解する目的では調査してよい**。

ただし repository の現状を仕様 authority として扱ってはならない。

> 実装方法を repository から発見してよい。
> required behavior を repository や別文書から発見してはならない。

assigned Pxx だけでは entry condition、scope、protected invariant、required behavior、acceptance criteria のいずれかを一意に判断できない場合、他資料へ探索を広げてはならない。

その場合は `BLOCKED_CONTRACT_AMBIGUITY` として停止せよ。

---

## 5. Package implementation

assigned Pxx に記載された Package scope のみを実装せよ。

以下を行ってはならない。

* 他 Package scope の実装
* contract に要求されない refactoring
* contract に要求されない architecture 変更
* protected invariant の変更
* unrelated cleanup
* speculative fix
* contract に存在しない仕様の補完
* verification を通すための期待値緩和
* failure の握り潰し

他 Package に関係する問題を発見しても、assigned Pxx が要求しない限り変更してはならない。

Package scope 内の実装を完了できない場合は `BLOCKED_IMPLEMENTATION` とする。

---

## 6. Focused verification

assigned Pxx が要求する focused verification をすべて実行せよ。

実行した command と結果を記録すること。

verification が失敗した場合は原因を調査し、assigned Package scope 内で修正可能なら修正して再実行してよい。

以下によって verification failure を隠してはならない。

* test の削除
* assertion の弱体化
* expected value の恣意的変更
* error suppression
* skip / xfail 等の追加
* 他 Package scope の変更による回避

assigned Pxx の acceptance criteria を満たす状態に到達できない場合は `BLOCKED_IMPLEMENTATION` とする。

---

## 7. Package checkpoint commit

Package implementation と focused verification が完了したら、変更内容を確認する。

```bash
git status
git diff --stat
git diff
```

今回の assigned Package scope に属する変更だけを stage せよ。

`git add .` または scope 外変更を含む一括 stage を行ってはならない。

stage 後、以下を確認する。

```bash
git diff --cached --stat
git diff --cached
git status
```

問題がなければ Package checkpoint を commit する。

```bash
git commit -m "ENH-E5 Gate {{GATE_ID}} Trial {{TRIAL_NO}} {{PACKAGE_ID}} implementation checkpoint"
git rev-parse HEAD
```

取得した exact SHA を、

```text
PACKAGE_CHECKPOINT_SHA
```

として記録する。

`PACKAGE_READY` とする場合、未commitの Package implementation change を残してはならない。

---

## 8. Package checkpoint/status report

以下に Package checkpoint/status report を作成せよ。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
      packages/
        E5-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}__status.md
```

必要な directory が存在しない場合は作成してよい。

report には最低限以下を記録する。

* `PROJECT_NAME`
* `ENHANCE_ID`
* `GATE_ID`
* `PACKAGE_ID`
* `TRIAL_NO`
* normative Pxx contract path
* `START_SHA`
* Package status
* changed files
* implementation summary
* executed verification commands
* verification results
* `PACKAGE_CHECKPOINT_SHA`
* blocker / remaining work（存在する場合）

`PACKAGE_READY` の場合、`PACKAGE_CHECKPOINT_SHA` は必須である。

BLOCKED の場合、checkpoint が存在しなければ SHA を捏造してはならない。

---

## 9. Evidence commit and push

Package checkpoint/status report 作成後、evidence file のみを stage せよ。

```bash
git add docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/packages/E5-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}__status.md
git status
git diff --cached
```

問題がなければ evidence commit を作成する。

```bash
git commit -m "ENH-E5 Gate {{GATE_ID}} Trial {{TRIAL_NO}} {{PACKAGE_ID}} implementation evidence"
git push -u causal-atelier feature/ariadne_mvp_e5
git log -2 --oneline
git status
```

Package checkpoint commit と evidence commit は別 commit でよい。

Package report に記録する checkpoint identity は、**evidence commit ではなく `PACKAGE_CHECKPOINT_SHA`** である。

---

## 10. Fixed Trial Candidate boundary

本 Agent は、assigned Pxx に明示されない限り Fixed Trial Candidate を assemble してはならない。

特に以下を行ってはならない。

* 全 Package 完了を推測する
* 他 Package の checkpoint を検証・統合する
* Gate-wide verification を独自に追加する
* Fixed Trial Candidate SHA を生成する
* implementation completion report を Gate completion として作成する
* Test Agent を起動する
* 次 Package を自律的に開始する

`PACKAGE_READY` は **assigned Package の実装と focused verification が完了したことだけ**を意味する。

`PACKAGE_READY` を Gate PASS、Gate complete、READY_FOR_TEST と表現してはならない。

---

## 11. BLOCKED / interrupted execution

実装開始後に完了不能となった場合も、可能な限り Package checkpoint/status report を作成または更新し、以下を記録せよ。

* どこまで実行したか
* 何を変更したか
* どの verification を実行したか
* failure / blocker
* uncommitted change の有無
* checkpoint SHA が存在するか
* 再開時に必要な情報

BLOCKED 状態で incomplete implementation を Package checkpoint として commit してはならない。

既存変更を破壊して clean state を作ってはならない。

---

## 12. Final status

最終応答では、必ず以下のいずれかを明示せよ。

```text
PACKAGE_READY
BLOCKED_CONTRACT_AMBIGUITY
BLOCKED_REPOSITORY_STATE
BLOCKED_IMPLEMENTATION
```

`PACKAGE_READY` の場合は最低限以下を報告する。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
START_SHA
PACKAGE_CHECKPOINT_SHA
EVIDENCE_COMMIT_SHA
Package report path
verification summary
```

BLOCKED の場合は最低限以下を報告する。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
START_SHA
BLOCKED status
blocker
changed / uncommitted files
report path（作成できた場合）
```

本 Agent は Package complete を Gate PASS と表現してはならない。
