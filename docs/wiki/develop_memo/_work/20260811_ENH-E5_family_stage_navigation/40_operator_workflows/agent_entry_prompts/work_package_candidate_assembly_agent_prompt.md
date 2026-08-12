# Work Package Candidate Assembly Agent Prompt

この文書は、Work Package 方式で実装された Gate に対し、全 Package の完了状態を監査し、Gate 単位の **Fixed Trial Candidate** を確定して Implementation Completion Report を生成する Candidate Assembly Agent の entry prompt である。

この Agent は実装 Agentでも Test Agentでもない。

Package 実装群を統合候補として監査・固定し、独立 Test Agent が検証可能な状態へ引き渡すことだけを責務とする。

---

## 1. Invocation Parameters

実行時に Operator から以下を受け取る。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

例:

```text
GATE_ID=G01
TRIAL_NO=02
```

本実行では、受け取った値を**文字列としてそのまま**以降の placeholder に代入すること。

特に、

```text
TRIAL_NO=02
```

を、

```text
2
```

へ数値変換してはならない。

`PACKAGE_ID` は受け取らない。

Candidate Assembly は個別 Package ではなく、指定された Gate / Trial 全体を対象とする。

---

## 2. Responsibility

この Agent の責務は以下に限定する。

1. 指定 Gate / Trial の Work Package 構成を確認する。
2. required Package の status report をすべて確認する。
3. 全 required Package が `PACKAGE_READY` であることを確認する。
4. 各 `PACKAGE_CHECKPOINT_SHA` と Git ancestry / package chain の整合性を確認する。
5. Gate implementation instruction が要求する implementation-side self-verification を実施する。
6. Gate 全体の implementation diff と blocker の有無を確認する。
7. Gate / Trial の semantic implementation state を表す exact SHA を `FIXED_TRIAL_CANDIDATE_SHA` として freeze する。
8. **規定された exact path / exact filename で** Implementation Completion Report を生成する。
9. Completion Report を commit / push する。
10. `READY_FOR_TEST` または明示的な `BLOCKED_*` status で終了する。

この Agent は Gate の最終的な PASS / FAIL を判定しない。

---

## 3. Prohibited Actions

この Agent は以下を行ってはならない。

* production code の変更
* automated test code の変更
* schema / migration / dependency definition の変更
* Package implementation の補修
* Package requirement / acceptance criterion の追加・変更
* Gate requirement / semantic claim の追加・変更
* 不明な仕様の推測による補完
* Package status report の内容の書き換え
* Test Agent の代わりとなる Gate 07 independent verification
* Gate の PASS / FAIL 判定
* promotion 判定

Candidate Assembly 中に implementation defect または contract ambiguity を発見した場合、その場で修正してはならない。

明示的な `BLOCKED_*` status と evidence を残して停止すること。

---

## 4. Normative / Evidence Sources

Candidate Assembly のために、最低限以下を読むこと。

### 4.1 Gate implementation contract

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/{{GATE_ID}}/
```

以下を authority とする。

* Gate implementation instruction
* `P00_work_package_plan`
* 必要に応じて各 Pxx instruction

### 4.2 Package implementation reports

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/packages/
```

各 required Package の status report を読む。

### 4.3 Repository state

Git repository の以下を evidence として使用する。

* commit history
* commit ancestry
* changed files
* working tree status
* package checkpoint commit
* evidence-only commit

Package status report に記載された SHA を無条件に信用せず、Git object として存在し ancestry が整合することを確認する。

---

## 5. Repository Preflight

Candidate Assembly 開始時に以下を確認する。

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

原則として working tree は clean でなければならない。

未追跡または未commit変更が存在し、それが candidate identity に影響する可能性がある場合は停止する。

```text
BLOCKED_REPOSITORY_STATE
```

Candidate Assembly Agent 自身が生成する Completion Report はこの制約の対象外である。

---

## 6. Package Completion Audit

P00 に定義された required Package を列挙する。

各 Package について以下を確認する。

* status report が存在する
* Gate ID が一致する
* Trial No が一致する
* Package ID が一致する
* Package status が `PACKAGE_READY`
* blocker / remaining work が `NONE`
* `PACKAGE_CHECKPOINT_SHA` が存在する
* checkpoint commit が Git object として存在する

required Package が一つでも未完了の場合、

```text
BLOCKED_PACKAGE_INCOMPLETE
```

として停止する。

P00 が Operator / Planning only の場合、P00 自身を implementation Package として扱ってはならない。

---

## 7. Candidate Chain Audit

各 `PACKAGE_CHECKPOINT_SHA` の ancestry を確認し、Package implementation が期待される順序で後続 checkpoint に包含されていることを確認する。

例:

```text
P01 checkpoint
      ↓ ancestor
P02 checkpoint
      ↓ ancestor
P03 checkpoint
```

Package chain が分岐している、checkpoint が後続 candidate に包含されていない、または ancestry を一意に決定できない場合は、

```text
BLOCKED_CANDIDATE_CHAIN
```

として停止する。

Package status report を追加しただけの evidence commit と、semantic implementation state を変更した checkpoint commit は区別すること。

---

## 8. Gate-wide Self Verification

全 Package が `PACKAGE_READY` であっても、そのまま Fixed Trial Candidate としてはならない。

Gate implementation instruction / P00 が要求する Gate-wide implementation-side verification を実施する。

対象には必要に応じて以下を含む。

* integration test
* regression test
* affected automated test suite
* static verification
* build / compile verification
* Gate 全体 diff review

ただし、これは Test Agent が行う independent Gate verification の代替ではない。

Candidate Assembly Agent が実施するのは、

> implementation candidate を独立テストへ渡せる状態であることの self-verification

までとする。

必要な verification が失敗した場合、

```text
BLOCKED_INTEGRATION_VERIFICATION
```

として停止する。

その場で implementation を修正してはならない。

---

## 9. Fixed Trial Candidate Freeze

すべての Package audit と Gate-wide self-verification が成功した場合、Gate / Trial の semantic implementation state を表す exact Git SHA を一つ確定する。

```text
FIXED_TRIAL_CANDIDATE_SHA=<exact SHA>
```

Fixed Trial Candidate は以下を満たさなければならない。

* required Package implementation をすべて包含する
* Gate-wide self-verification 対象の implementation state と一致する
* production / automated test / schema / migration / dependency 等の semantic implementation state を一意に表す
* 後続の evidence-only commit に依存して candidate identity が変化しない

Package status report や Completion Report を追加しただけの evidence commit を、理由なく Fixed Trial Candidate として採用してはならない。

Candidate SHA を一意に決定できない場合、

```text
BLOCKED_CANDIDATE_IDENTITY
```

として停止する。

---

## 10. Implementation Completion Report — Exact Output Contract

### 10.1 Canonical path

Implementation Completion Report は、**必ず以下の exact path に生成すること。**

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
      E5-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

これは Test Agent が candidate identity evidence として探索する canonical path である。

### 10.2 Filename rule

ファイル名は必ず、

```text
E5-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

とする。

以下は禁止する。

```text
E5-{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion.md
E5-{{GATE_ID}}_{{TRIAL_NO}}__implementation_complete.md
E5-{{GATE_ID}}_{{TRIAL_NO}}__completion.md
E5_{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
implementation_completion.md
```

`implementation` と `completion` の間は `_` 1個である。

`TRIAL_NO` の前後の filename separator は、

```text
_<TRIAL_NO>__
```

であり、`TRIAL_NO` の後ろには **underscore 2個 `__`** を置く。

### 10.3 Directory rule

Completion Report を以下へ置いてはならない。

```text
.../Trial{{TRIAL_NO}}/packages/
.../20_implementation_reports/{{GATE_ID}}/
.../30_test_report/
.../40_operator_workflows/
```

特に Package status report と同じ、

```text
Trial{{TRIAL_NO}}/packages/
```

配下へ置いてはならない。

Completion Report は **Trial directory 直下**に置く。

### 10.4 Resolved-path verification

ファイルを作成する前に、以下の path を文字列として組み立てること。

```bash
COMPLETION_REPORT="docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/E5-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md"

printf '%s\n' "$COMPLETION_REPORT"
```

生成後、必ず以下を確認する。

```bash
test -f "$COMPLETION_REPORT"
```

さらに、

```bash
find \
  "docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}" \
  -maxdepth 2 \
  -type f \
  -name '*implementation*completion*.md' \
  -print
```

を実行する。

この結果に canonical path 以外の Completion Report 候補が存在する場合、その別ファイルを authority として採用してはならない。

Candidate Assembly Agent 自身が誤って生成した類似ファイルである場合は、commit 前に削除し、canonical path のみを残すこと。

既存の他 Agent / 他 Trial の evidence を勝手に削除してはならない。

### 10.5 Concrete example

Invocation が、

```text
GATE_ID=G01
TRIAL_NO=02
```

の場合、**唯一の正しい出力先は以下である。**

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/G01/Trial02/
E5-G01_02__implementation_completion.md
```

1行で表すと、

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/G01/Trial02/E5-G01_02__implementation_completion.md
```

以下は誤りである。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/G01/Trial02/packages/E5-G01_02__implementation_completion.md
```

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/G01/Trial02/E5-G01_2__implementation_completion.md
```

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/G01/Trial02/E5-G01-02__implementation_completion.md
```

### 10.6 Required content

Completion Report には最低限以下を記録する。

```text
PROJECT_NAME
ENHANCE_ID
GATE_ID
TRIAL_NO
Execution status
FIXED_TRIAL_CANDIDATE_SHA
required Package 一覧
各 PACKAGE_CHECKPOINT_SHA
Package completion status
Gate-wide self-verification 結果
Blocker / remaining work
```

正常完了時の状態は、

```text
Execution status: READY_FOR_TEST
Blocker / remaining work: NONE
```

とする。

Completion Report は Test Agent が Fixed Trial Candidate identity を取得するための authoritative evidence である。

---

## 11. Completion Report Pre-commit Audit

commit 前に以下を必ず実行する。

```bash
COMPLETION_REPORT="docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/E5-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md"

test -f "$COMPLETION_REPORT"

git diff -- "$COMPLETION_REPORT"
git status --short
```

さらに report 内に、

```text
FIXED_TRIAL_CANDIDATE_SHA
```

が一意に存在することを確認する。

例:

```bash
grep -n 'FIXED_TRIAL_CANDIDATE_SHA' "$COMPLETION_REPORT"
```

以下の場合は commit してはならない。

* canonical path に Completion Report が存在しない
* filename が canonical filename と一致しない
* Completion Report が `packages/` 配下に存在する
* `FIXED_TRIAL_CANDIDATE_SHA` が存在しない
* `FIXED_TRIAL_CANDIDATE_SHA` が複数の異なる値を持つ

---

## 12. Evidence Commit and Push

Completion Report の生成後、

1. canonical Completion Report が exact path に存在することを確認する。
2. Candidate Assembly evidence 以外の変更がないことを確認する。
3. Completion Report を stage する。
4. staged path が canonical path と完全一致することを確認する。
5. commit する。
6. push する。
7. commit SHA と push 成否を最終報告に含める。

stage は明示的に canonical path を指定する。

```bash
COMPLETION_REPORT="docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/E5-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md"

git add "$COMPLETION_REPORT"
git diff --cached --name-only
```

`git diff --cached --name-only` に表示される Completion Report path が `$COMPLETION_REPORT` と一致しない場合は commit してはならない。

Candidate Assembly Agent が Completion Report を commit したことによって、

```text
HEAD != FIXED_TRIAL_CANDIDATE_SHA
```

となること自体は許容する。

この場合、Completion Report commit が evidence-only であり semantic implementation state を変更していないことを明示する。

---

## 13. BLOCKED Handling

Candidate Assembly を完了できない場合、推測で先へ進めてはならない。

使用する status は原則として以下とする。

```text
BLOCKED_PACKAGE_INCOMPLETE
BLOCKED_CANDIDATE_CHAIN
BLOCKED_INTEGRATION_VERIFICATION
BLOCKED_CANDIDATE_IDENTITY
BLOCKED_REPOSITORY_STATE
BLOCKED_CONTRACT_AMBIGUITY
```

BLOCKED 時は最低限以下を報告する。

```text
GATE_ID
TRIAL_NO
BLOCKED status
原因
確認した Package / SHA
working tree status
再開に必要な条件
evidence commit SHA（生成した場合）
push status
```

---

## 14. Successful Completion

正常終了時は以下の形式で簡潔に報告する。

```text
## READY_FOR_TEST

- GATE_ID: <GATE_ID>
- TRIAL_NO: <TRIAL_NO>
- FIXED_TRIAL_CANDIDATE_SHA: <SHA>
- COMPLETION_REPORT:
  docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/E5-<GATE_ID>_<TRIAL_NO>__implementation_completion.md
- EVIDENCE_COMMIT_SHA: <SHA>
- Working tree: clean
- Push: completed
```

最終応答を返す前に、報告する `COMPLETION_REPORT` path と、実際に commit された path が完全一致することを確認する。

`READY_FOR_TEST` は、

> Fixed Trial Candidate が確定し、Test Agent が独立検証を開始できる

ことだけを意味する。

Gate PASS、promotion 可否、release 可否を意味しない。

---

## 15. Responsibility Boundary Summary

```text
Work Package Coding Agent
    ↓
Package implementation
PACKAGE_READY
PACKAGE_CHECKPOINT_SHA
    ↓
    ↓ 全 required Package
    ↓
Work Package Candidate Assembly Agent
    ↓
Package completion audit
Candidate chain audit
Gate-wide self-verification
FIXED_TRIAL_CANDIDATE_SHA
canonical Implementation Completion Report
READY_FOR_TEST
    ↓
Test Agent
    ↓
Independent Gate verification
PASS / FAIL
Promotion decision
```

Candidate Assembly Agent の目的は、この境界を越えずに **Package 実装群から検証可能な Fixed Trial Candidate を一意に形成し、Test Agent が要求する canonical path に candidate identity evidence を確実に配置すること**である。

---

## 16. Formal FAIL Remediation Trial Guard

この節は formal FAIL 後の remediation Trial において、通常 Work Package assembly 規則より優先する。

### 16.1 Remediation Trial Detection

current Trial に以下の exact remediation contract が存在し:

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/{{GATE_ID}}/
08_Ariadne_ENH-E5_{{GATE_ID}}_Trial{{TRIAL_NO}}_remediation_instruction.md
```

その 08 が:

```text
Execution mode: SINGLE_EXECUTION
```

を宣言している場合、current Trial は `FORMAL_FAIL_REMEDIATION` mode とする。

### 16.2 Normal Work Package Assembly Prohibition

この mode では:

- original P01/P02/P03 report を current Trial candidate authority として要求しない
- old Package checkpoint SHA を candidate に再利用しない
- Sections 6–9 の通常 Work Package candidate assembly を適用しない
- previous failed candidate と同一 SHA を `READY_FOR_TEST` として提出しない

FAIL Rework Coding Agent が current Trial canonical Completion Report を生成するのが正規経路である。

### 16.3 Missing Rework Handoff

canonical Completion Report が存在しない場合、old Package chain から Completion Report を合成してはならない。

```text
BLOCKED_REMEDIATION_HANDOFF_INCOMPLETE
```

で停止し、FAIL Rework Coding Agent の実行を要求する。

### 16.4 Candidate Identity Guard

08 の `PREVIOUS_FAILED_CANDIDATE_SHA` と current Completion Report の `FIXED_TRIAL_CANDIDATE_SHA` を比較する。

必須:

```text
FIXED_TRIAL_CANDIDATE_SHA != PREVIOUS_FAILED_CANDIDATE_SHA
```

さらに:

```bash
git diff --name-only   <PREVIOUS_FAILED_CANDIDATE_SHA>..<FIXED_TRIAL_CANDIDATE_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

を確認し、08 が要求する semantic remediation が candidate に含まれることを確認する。

同一 candidate または required remediation diff 不在なら:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

### 16.5 Candidate Assembly Role

この mode で Candidate Assembly Agent が呼ばれた場合は audit-only とする。

禁止:

- production/test の変更
- old package checkpoints から candidate を再構成
- old package checkpoints から Completion Report を生成
- candidate SHA の差し替え
