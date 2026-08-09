# G03 Preflight — Test PostgreSQL Infrastructure Independent Verification Prompt

## 1. Task

G03開始前に実装された **Test PostgreSQL Infrastructure Standardization** を独立監査する。

本Taskはread-only verificationである。

Test/Audit Agentはproduction source、test infrastructure source、tests、migration、compose、dependencyを修正してはならない。

目的は、G03〜G08でreal PostgreSQL verificationがG02のような複数手動手順へ戻らず、
repository-managedな標準経路で再現可能であることを確認することである。

---

## 2. Required Inputs

作業指示者から以下を受け取る。

```text
INFRA_IMPLEMENTATION_COMMIT=<full SHA>
```

参照:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G03_Preflight/
01_test_postgresql_infrastructure_standardization_result.md
```

Audit Agentはimplementation commitをfull SHAで固定する。

---

## 3. Source of Truth

本書がverification contractである。

参照してよいもの:

- 本書
- standardization result
- INFRA_IMPLEMENTATION_COMMITのactual source
- compose/test runner/scripts
- Product migrations
- current automated tests
- Git diff/log/show
- 自身が生成するaudit evidence

Architecture backgroundを再設計のために読み直さない。

---

## 4. Prohibited

禁止:

- source変更
- compose変更
- Dockerfile変更
- scripts変更
- tests変更
- migration変更
- dependency変更
- `.gitignore`変更
- production DB操作
- development DBをtestに利用
- assertion緩和
- skip/xfail追加
- G03 implementation開始

---

## 5. Verification Model

次を独立確認する。

```text
repository-managed command
        ↓
database_test
        ↓ same compose network
test_runner
        ↓
clean DB reset
        ↓
Product migration
        ↓
real PostgreSQL pytest
        ↓
evidence + exit status
```

host loopback / docker0 gatewayへの接続が成功することをPASS条件にしてはならない。

標準経路はDocker service networking等のrepository-defined stable routeを使用すること。

---

## 6. Mandatory Audit Items

### IA-001 Change boundary

implementation commit diffを確認する。

PASS条件:

- test infrastructure scopeのみ
- G03 production implementationなし
- StageExecution/Result/Artifact/Lineage変更なし
- Product migration history rewriteなし
- unrelated refactorなし

---

### IA-002 Development DB isolation

確認:

- development `database` とtest DBが別service/DB
- persistent development volume共有なし
- test resetがdevelopment DBを対象にしない
- test URLがdevelopment `database:5432/ariadne` 等を指していない

PASSには構造証拠が必要。

---

### IA-003 Test runner dependency isolation

確認:

- pytest/dev dependencyはtest runnerへ存在
- production runtime imageへ不要なdev dependencyが恒久混入していない
- current lockfileに基づく再現可能install

---

### IA-004 Stable Docker networking

確認:

- test runner → database_test がstable service/network routeを使用
- `172.17.0.1` 等のmachine-specific addressをhard-codeしていない
- localhost-host namespace依存を通常経路にしていない

---

### IA-005 Cold start

test DB service/containerが存在しない状態から標準one-commandを実行する。

PASS条件:

- service自動起動
- readiness成功
- reset成功
- migration成功
- requested pytest成功

Audit AgentがDockerを利用できない場合は、
implementation resultに保存されたcold-start raw evidenceを監査してよい。
ただしevidence commit / tested commitを固定し真正性を確認すること。

---

### IA-006 Warm reuse

database_testが既にhealthyな状態でも同じ標準commandが成功する。

手作業で別command sequenceへ切り替えない。

---

### IA-007 Dirty DB reset

test DBに既存stateがある状態からrunnerを再実行し、
clean reset後にmigration/testが成功すること。

既存stateによるunique collisionやmigration driftが次runへ残らないこと。

---

### IA-008 Product migration

確認:

```text
alembic_product.ini
product_migrations/
alembic_version_product
```

のみを使用。

clean DBからactual Product headまで到達する。

root legacy migrationを実行していない。

---

### IA-009 Real PostgreSQL contract

標準runnerから最低限:

```text
tests/product/test_postgres_contract.py
```

を実行。

PASS条件:

- skipではない
- real DB assertionsまで到達
- exit 0

---

### IA-010 Atomic claim regression

標準runnerから:

```text
tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers
```

を実行。

PASS条件:

- real PostgreSQLで実行
- exit 0
- environment skipなし

---

### IA-011 G02 targeted regression

最低限:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
```

を実行またはimplementation self-test evidenceを独立監査。

G02 PASS済みcontractをtest infrastructure変更が壊していないこと。

---

### IA-012 Failure propagation

標準runnerへinvalid pytest node等を与え、
non-zero exitが呼出元まで返ることを確認する。

runnerがfailureを0へ変換してはならない。

---

### IA-013 Evidence output

確認:

- tested commit記録
- migration result
- pytest command
- exit code
- stdout/stderr
- evidence location

raw evidenceが必要な場合にcommit/共有できる運用が成立する。

`.log` ignore問題等でevidenceが再び消失する設計でないこと。

---

### IA-014 Human fallback

Agent環境からDockerを利用できない場合のfallbackを確認する。

PASS条件:

Human Operatorが行うのは原則:

```text
one repository-managed command
```

だけ。

Humanが個別に:

- docker run
- network IP特定
- export DSN
- manual alembic
- manual pytest

を繰り返す設計ならFAIL。

---

### IA-015 Cleanup

test stackのcleanup commandがdocumentedである。

cleanupがdevelopment stack/volumeを削除しないこと。

---

## 7. Required Execution Strategy

Audit Agent自身がDockerを利用できる場合:

1. fixed implementation commitのclean worktreeを使用
2. cold start
3. warm reuse
4. dirty DB reset
5. postgres contract
6. concurrent claim
7. failure propagation
8. cleanup
9. git integrity check

を実行する。

Audit Agent自身がDockerを利用できない場合:

- 自分のnetwork制約を理由に即BLOCKEDしない
- implementation result / raw evidenceがrepository/ref上に固定されているか確認
- evidenceが十分ならread-only independent auditを行う
- evidence不足ならBLOCKED

G02のようにAgent自身からDBへ再接続することを唯一の合格条件にしてはならない。

---

## 8. Evidence Integrity Rules

external/self-test evidenceを利用する場合、最低限:

```text
TESTED_COMMIT
EVIDENCE_COMMIT
```

を別々に固定できること。

証跡がimplementation後のcommitに存在すること自体をfailureとしない。

Audit Agentは:

```bash
git show <ref>:<path>
```

等を用いてread-only監査してよい。

---

## 9. PASS / FAIL / BLOCKED

### PASS

全Mandatory Audit Itemが成立。

### FAIL

test infrastructure implementation defectを確認。

例:

- development DBをreset
- host-specific IP hard-code
- runnerがfailureを0で返す
- migrationを実行しない
- postgres testsがskip
- warm runでstate leak
- G03 production codeへ越境

### BLOCKED

evidence真正性/必要実行結果が不足し、
PASS/FAILを判定できない。

Agent自身がDockerを利用できないだけで、
十分な固定evidenceがある場合はBLOCKEDにしない。

---

## 10. Required Result

生成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G03_Preflight/
02_test_postgresql_infrastructure_verification_result.md
```

構造:

```markdown
# Test PostgreSQL Infrastructure Independent Verification Result

## 1. Metadata
## 2. Implementation Commit
## 3. Evidence Commit
## 4. Change Boundary Audit
## 5. Development Isolation
## 6. Test Runner Architecture
## 7. Docker Networking
## 8. Cold Start
## 9. Warm Reuse
## 10. Dirty DB Reset
## 11. Product Migration
## 12. PostgreSQL Contract Test
## 13. Atomic Claim Test
## 14. G02 Regression
## 15. Failure Propagation
## 16. Evidence Contract
## 17. Human Fallback Audit
## 18. Cleanup Audit
## 19. Repository Integrity
## 20. Audit Matrix
## 21. Remaining Risks
## 22. Decision
```

Audit Matrix:

| ID | Status | Evidence |
|---|---|---|
| IA-001 | PASS/FAIL/BLOCKED | ... |
| ... | ... | ... |
| IA-015 | PASS/FAIL/BLOCKED | ... |

---

## 11. Final Decision Values

以下のみ。

```text
PASS_READY_FOR_G03
FAIL_FIX_TEST_INFRASTRUCTURE
BLOCKED_TEST_INFRASTRUCTURE_AUDIT
```

`PASS_READY_FOR_G03` の場合でもG03 implementationを自動開始しない。

---

## 12. PASS Criteria

`PASS_READY_FOR_G03` には全て必要。

1. development DB isolation PASS
2. stable test Docker networking PASS
3. one-command workflow PASS
4. cold start PASS
5. warm reuse PASS
6. dirty DB reset PASS
7. Product migration PASS
8. real PostgreSQL contract PASS
9. concurrent claim PASS
10. failure propagation PASS
11. evidence output PASS
12. Human fallback one-command PASS
13. cleanup isolation PASS
14. production source semantics unchanged
15. G03 implementation未着手

---

## 13. Stop Condition

Gate Decision作成後に停止する。

PASSなら:

```text
G03 contract authoring may begin.
```

FAIL/BLOCKEDならG03へ進まない。
