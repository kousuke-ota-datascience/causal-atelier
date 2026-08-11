`````
E4-G02 Trial 01 external PostgreSQL verification evidence の最終監査を再開せよ。

前回のBLOCKED理由であった、

* primary Supplemental evidenceが参照できない
* raw PostgreSQL evidence directoryが存在しない

という状態は解消済みである。

今回、implementationとverification evidenceは意図的に別commitとして管理する。

## Fixed Implementation Commit

```text
IMPLEMENTATION_COMMIT=
166e90cd1c2d0e523fb863795a88343403d8cc44
```

production source / automated tests / Product migration implementationの監査対象は、このcommitを正本とする。

このimplementation commitを変更してはならない。

## Fixed Evidence Commit

```text
EVIDENCE_COMMIT=
c856d80
```

Human Operatorによるexternal PostgreSQL verificationのraw evidenceは、このEvidence commitを正本とする。

したがって、

「implementation commit 166e90cd のdetached worktree内に後発Supplemental evidenceが存在しない」

ことをBLOCKED理由としてはならない。

implementationとtest evidenceは時間的に別commitになることが意図された構成である。

必要なら最初にremote refsを更新せよ。

```bash
git fetch --all --prune
```

implementation worktreeをEvidence commitへcheckoutしてはならない。

Evidence commitは `git show` 等によりread-onlyで監査すること。

## Primary Evidence

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
03_external_postgresql_verification_execution.md
```

## Raw Evidence

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
03_external_postgresql_verification_execution_evidence/
```

Evidence commit `c856d80` には以下16ファイルが存在する。

```text
00_implementation_commit.log
01_worktree_before.log
02_database_environment.log
03_sqlalchemy_preflight.log
04_alembic_heads.log
05_alembic_current_before.log
06_alembic_upgrade_head.log
07_alembic_current_after.log
08_product_migration_revision.log
09_postgres_contract_pytest.log
10_atomic_claim_pytest.log
11_g02_targeted_contract.log
12_ac002_targeted.log
13_ac005_lease_contract.log
14_worktree_after.log
15_evidence_inventory.log
```

Human Operatorのsummaryだけを採用せず、必ずEvidence commit上のraw logを自分で読んで監査せよ。

## Required Audit

### 1. Commit integrity

確認:

* raw evidenceのimplementation commitが `166e90cd1c2d0e523fb863795a88343403d8cc44`
* verification開始時のdetached worktreeが同commit
* verification終了後も同commit
* verification終了時にsource/test/migrationのworking-tree diffが存在しない

### 2. PostgreSQL environment

確認:

* ARIADNE_PRODUCT_DATABASE_URL が設定済み
* ARIADNE_PRODUCT_TEST_DATABASE_URL が設定済み
* PostgreSQL session preflightが成立
* database = `ariadne_g02_test`

### 3. Product migration

以下をraw evidenceから監査する。

* Product migration head
* empty PostgreSQL databaseへのupgrade
* migration exit code
* post-upgrade current revision
* `alembic_version_product`

Expected target:

```text
20260809_product_0007
```

root legacy migrationの結果を代用してはならない。

### 4. PostgreSQL contract suite

`09_postgres_contract_pytest.log` を監査する。

実際にpytestがDB assertionまで到達していること、skipやenvironment BLOCKEDではないこと、exit codeを確認する。

### 5. Atomic claim

`10_atomic_claim_pytest.log` を監査する。

concurrent worker claim testが実際に実行され、assertionまで到達していることを確認する。

これはE4-G02-AC-005の主要なreal PostgreSQL evidenceである。

### 6. G02 targeted contract

`11_g02_targeted_contract.log` を監査する。

### 7. AC-002

`12_ac002_targeted.log` および関連PostgreSQL evidenceを監査し、

E4-G02-AC-002:

* common claim/state contract
* PostgreSQL-backed lifecycle requirements

の判定に十分か独立評価する。

### 8. AC-005

`13_ac005_lease_contract.log`
および
`10_atomic_claim_pytest.log`

を併せて監査し、

E4-G02-AC-005:

* invalid transition rejection
* double claim rejection
* lease ownership semantics

の判定に十分か独立評価する。

### 9. Previously PASS evidence

初回Testで既にPASS済み:

* E4-G02-AC-001
* E4-G02-AC-003
* E4-G02-AC-004
* relevant regression: 41 passed

については、implementation commitが `166e90cd...` から不変であることを確認できた場合に限り、既存evidenceを再利用してよい。

## Decision Rule

以下が全て成立する場合のみ:

```text
E4-G02-AC-001 PASS
E4-G02-AC-002 PASS
E4-G02-AC-003 PASS
E4-G02-AC-004 PASS
E4-G02-AC-005 PASS
Product migration verification PASS
Relevant regression PASS
```

最終判定:

```text
E4-G02 = PASS
```

implementation defectがraw evidenceから確認された場合:

```text
E4-G02 = FAIL
```

evidence不足、commit真正性不明、またはAcceptance Criteriaを判定不能な場合:

```text
E4-G02 = BLOCKED
```

とする。

## Prohibited

* production source変更
* automated test変更
* migration変更
* dependency変更
* implementation commit変更
* external PostgreSQL test再実行を必須条件とすること
* Test Agent自身のnetwork isolationを理由に、既に固定されたexternal raw evidenceを無視すること
  -既存BLOCKED evidenceの削除

## Required Output

最終監査evidenceとGate Decisionを:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/
G02/
```

配下へ追加すること。

Gate Decisionでは最低限:

* IMPLEMENTATION_COMMIT
* EVIDENCE_COMMIT
* AC-001〜005
* Product migration verification
* relevant regression
* external evidence integrity
* final decision

を明記する。

Gate Decision作成後、G03には進まず停止せよ。
`````