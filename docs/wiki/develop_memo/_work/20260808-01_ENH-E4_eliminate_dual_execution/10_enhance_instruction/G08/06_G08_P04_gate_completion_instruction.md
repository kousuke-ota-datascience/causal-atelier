# ENH-E4 / G08 P04 — Gate Completion / Candidate Freeze

## 1. Objective

P01-P03 の成果を統合し、Independent Test に渡す **one fixed implementation/test candidate** を確定する。

P04 は formal G08 PASS を判定しない。

---

## 2. Inputs

必須:

```text
06_G08_P00_work_package_plan.md

E4-G08_01_P01_implementation_checkpoint_report.md
E4-G08_01_P02_implementation_checkpoint_report.md
E4-G08_01_P03_implementation_checkpoint_report.md

07_Ariadne_ENH-E4_G08_テスト指示書.md

current repository
```

---

## 3. Entry Check

```bash
git rev-parse HEAD
git status --short
uv run alembic -c alembic_product.ini heads
```

P01-P03 がすべて `COMPLETE` であることを確認する。

---

## 4. Completion Matrix

以下を一つの table に統合する。

| Gate AC | Implementation-side Evidence | Result |
|---|---|---|
| AC-001 | clean Product bootstrap + startup | PASS/FAIL |
| AC-002 | three-family canonical lifecycle | PASS/FAIL |
| AC-003 | mutation + lineage | PASS/FAIL |
| AC-004 | final authority audit | PASS/FAIL |
| AC-005 | shared science + zero debt candidate | PASS/FAIL |

各 row に P03 の exact command / evidence reference を紐づける。

---

## 5. Transition Debt Finalization Candidate

P01 final inventory と P02 disposition を統合する。

必要 state:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSURE_CANDIDATE

genuine active bounded transition = 0
OPEN TRANSITION DEBT = 0 candidate state
```

TD-006 の formal `CLOSED` は Independent Test に委ねる。

---

## 6. Final Verification

P03 で使用した Gate-wide verification selection を、candidate freeze 前の final repository state で再実行する。

目的:

```text
P03 後の documentation/test/implementation adjustment による regression がないこと
```

full repository pytest は必須ではない。

P03 AC matrix を再現する最小の selection を使用する。

DB semantics を含む selection は repository-managed PostgreSQL runner で実行する。

---

## 7. Repository Hygiene

確認:

```bash
git status --short
git diff --check
```

必要に応じて:

```bash
git diff --stat
git diff --name-only
```

candidate に含める implementation/test changes と documentation changes を区別する。

---

## 8. Independent Test Contract Identity

`07_Ariadne_ENH-E4_G08_テスト指示書.md` を含む commit SHA を記録する。

Candidate freeze 後に ancestor relation を確認する。

```bash
git merge-base --is-ancestor <TEST_CONTRACT_SHA> <CANDIDATE_SHA>
echo $?
```

期待:

```text
0
```

---

## 9. Candidate Freeze

全 completion condition が成立したら current implementation/test state を commit し、SHA を固定する。

記録:

```text
G08 Fixed Candidate SHA:
<40-char SHA>

G08 Independent Test Contract SHA:
<40-char SHA>

Candidate ancestor proof:
PASS
```

candidate 後の report/documentation commit は candidate identity と分離する。

---

## 10. Implementation Completion Report

出力:

```text
20_implementation_reports/G08/Trial01/
E4-G08_01_implementation_completion_report.md
```

最低構成:

```text
1. Metadata / candidate identity
2. P01-P04 summary
3. Final TD-006 inventory/disposition
4. AC-001..005 evidence matrix
5. Final verification commands/results
6. PostgreSQL evidence
7. Transition Debt state
8. Facts / Interpretation / Unknown
9. Independent Test handoff
```

---

## 11. READY_FOR_TEST

次をすべて満たす場合のみ:

```text
READY_FOR_TEST
```

とする。

```text
P01-P04 COMPLETE
AC-001..005 implementation-side PASS
final verification PASS
genuine active bounded transition = 0
OPEN TRANSITION DEBT = 0 candidate state
material Unknown = 0
fixed candidate SHA established
Independent Test Contract SHA established
ancestor proof PASS
```

それ以外は `READY_FOR_TEST` としない。

---

## 12. Exit

P04 完了後、Coding Agent は G08 の architecture/acceptance semantics を変更しない。

次工程:

```text
Independent Test
```

formal result は:

```text
PASS
FAIL
BLOCKED
```

のいずれかとする。
