# ENH-E10 G02 Trial 01 — Test Item 001: Candidate Identity Audit（reverification 03）

| 項目 | 値 |
| --- | --- |
| Gate / Trial | `G02` / `01` |
| Test Item | `001_candidate_identity` |
| Frozen contract | `10_enhance_instruction/G02/07_Ariadne_ENH-E10_G02_test_instruction.md` |
| Canonical completion report | `20_implementation_reports/G02/Trial01/E10-G02_01__implementation_completion.md` |
| Fixed Trial Candidate SHA | `d2d87e074338b06fc740252506ae1dba2b2a5c04` |
| Previous failed candidate SHA | `67f1c4ef1281700a14b5a9acd0eacf00b5c904e0` |
| TEST_START_SHA / tested HEAD | `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb` |
| Branch | `feature/ariadne_mvp_e10` |
| Result | **PASS** |

## 検証目的と PASS 条件

本 Test Item は、後続の product verification が canonical completion report に固定された candidate、または candidate と同一の semantic implementation state に対して行われることを確認する。

PASS 条件は、(1) candidate commit の存在、(2) candidate が tested HEAD の祖先であること、(3) candidate 後に production/test/dependency/migration/frontend semantic change がないこと、(4) formal remediation candidate が previous failed candidate と異なること、(5) working tree clean のすべてである。いずれかが不成立なら Test Item 010–090 は開始不可である。

## Repository preflight

```bash
git branch --show-current
git status --porcelain=v1
git rev-parse HEAD
git remote get-url causal-atelier
```

```text
feature/ariadne_mvp_e10
# git status --porcelain=v1: output なし（clean）
7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb
git@github.com:kousuke-ota-datascience/causal-atelier.git
```

事実: branch、remote、clean tree は preflight を満たす。`7de36e4…` を TEST_START_SHA とした。

## Candidate identity の取得と object / ancestry audit

canonical completion report から、Human input や HEAD から推測せず、以下の exact field を取得した。

```text
PREVIOUS_FAILED_CANDIDATE_SHA = 67f1c4ef1281700a14b5a9acd0eacf00b5c904e0
FIXED_TRIAL_CANDIDATE_SHA    = d2d87e074338b06fc740252506ae1dba2b2a5c04
Execution status             = READY_FOR_TEST
```

実行コマンド:

```bash
git cat-file -e d2d87e074338b06fc740252506ae1dba2b2a5c04^{commit}
git show --stat --oneline --decorate --no-renames d2d87e074338b06fc740252506ae1dba2b2a5c04
git merge-base --is-ancestor d2d87e074338b06fc740252506ae1dba2b2a5c04 HEAD
git log --oneline d2d87e074338b06fc740252506ae1dba2b2a5c04..HEAD
```

raw evidence:

```text
git cat-file -e …^{commit}: exit 0

d2d87e0 ENH-E10 G02 Trial 01 LIME remediation candidate
 src/ariadne/capabilities/predictive/explanation_runner.py  | 14 +++++++-
 src/ariadne/capabilities/predictive/lime_backend.py        | 38 ++++++++++++++++++----
 src/ariadne/capabilities/predictive/planner.py             |  3 ++
 src/ariadne/capabilities/predictive/training_runners.py    |  2 ++
 tests/product/test_enh_e10_g02_p03_lime_backend.py         | 22 +++++++++++++
 tests/product/test_predictive_explanation_e3.py             |  3 +-
 6 files changed, 74 insertions(+), 8 deletions(-)

git merge-base --is-ancestor … HEAD: exit 0
7de36e4 ENH-E10 G02 Trial 01 remediation candidate identity
800bbe2 ENH-E10 Gate G02 Trial 01 independent verification evidence
a9cb222 ENH-E10 G02 Trial 01 remediation evidence
```

事実: candidate object は存在し、tested HEAD の祖先である。candidate 自体は previous failed candidate に対する non-empty remediation diff（production 4 files、test 2 files、74 additions / 8 deletions）を持つ。

## Previous-failed-candidate guard

```bash
test d2d87e074338b06fc740252506ae1dba2b2a5c04 != 67f1c4ef1281700a14b5a9acd0eacf00b5c904e0
```

結果: exit `0`。

解釈: previous failed candidate の再提出ではない。formal remediation の distinct-candidate guard を満たす。

## Post-candidate diff audit

```bash
git diff --name-status d2d87e074338b06fc740252506ae1dba2b2a5c04..7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb
git diff --check d2d87e074338b06fc740252506ae1dba2b2a5c04..7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb
```

```text
M  docs/.../20_implementation_reports/G02/Trial01/E10-G02_01__implementation_completion.md
A  docs/.../20_implementation_reports/G02/Trial01/E10-G02_01__remediation_completion.md
A  docs/.../30_test_report/G02/Trial01/ENH-E10_G02_01_001_candidate_identity_reverification_02.md
A  docs/.../30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision_reverification_02.md
git diff --check: exit 0
```

| 差分分類 | 観測 | identity への影響 |
| --- | --- | --- |
| completion/remediation reports | candidate / remediation execution evidence | documentation-only |
| prior test evidence | 過去の independent verification records | documentation-only |
| `src/`, `tests/`, dependency, migration, frontend | post-candidate diff なし | semantic state は candidate と同一 |

## 判定と再現条件

**結果: PASS。** Candidate identity は一意で、Git object として存在し、previous failed candidate と異なり、tested HEAD はその descendant である。candidate 後の差分は documentation/evidence のみであり product semantic state を変更しない。従って Test Item 010–090 をこの candidate の同一 semantic state に対して実行してよい。

再現時は、本 report の preflight、object/ancestry、distinct-candidate guard、post-candidate diff audit を順に実行する。SHA または semantic diff classification が一致しない場合は、この PASS を流用せず `BLOCKED_CANDIDATE_IDENTITY` として停止する。
