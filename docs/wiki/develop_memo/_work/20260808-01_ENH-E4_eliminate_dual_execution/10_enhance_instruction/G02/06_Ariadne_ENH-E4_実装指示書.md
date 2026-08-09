# Ariadne ENH-E4 E4-G02 実装指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Baseline commit: `e70c6f7f1f63ce2568c85482bc20a355da66b7cf`
* Active Gate: `E4-G02`
* Gate name: Canonical Execution aggregate and claim
* Trial: `01`
* Expected starting Product migration head: `20260807_product_0006`
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

## 1. Source of Truth

本書は、E4-G02 Trial 01においてCoding Agentが従う唯一のimplementation contractである。

### 参照してよいもの

Coding Agentは以下を参照してよい。

* 本書
* current production source code
* current automated test code
* current Product migrations
* `pyproject.toml`
* Git status / diff / log / show
* repository内の既存schema / repository / UoW / worker implementation
* 自身が本Trialで生成するimplementation report
* 同一Gateのprevious Gate Decision report。ただしTrial 01ではN/A

### 通常参照してはならないもの

implementation判断のために以下を再探索してはならない。

* `00_enhance_background/**`
* Revised requirements snapshot
* Architecture Review 01〜08c
* 旧implementation instruction
* 旧test instruction
* 上位requirement/design document
* chat history

本書とcurrent production codeの間に、実装不能またはsemantic contradictionがある場合は勝手にarchitectureを再設計せず `DESIGN_BLOCKED` とする。

---

# 2. Coding Agent Role

Coding Agentの責務はE4-G02だけを実装することである。

実施する。

1. canonical Product Execution aggregateを実装する。
2. canonical Execution repository / Unit of Work boundaryを実装または既存実装から統合する。
3. canonical claim / lease ownershipを一つのrepository/service abstractionへ集約する。
4. canonical lifecycle state transitionを三family共通contractとして実装する。
5. retry / rerun / revise / cancelのExecution identity semanticsを実装する。
6. invalid transition、double claim、lease ownership violationを拒否する。
7. 必要なProduct migrationを追加する。
8. Active Gateに必要なautomated testsを追加・修正する。
9. implementation commitを作成する。
10. implementation completion reportと累積implementation report detailを作成する。
11. `READY_FOR_TEST` で停止する。

Coding AgentはGate PASSを判定しない。

---

# 3. Prohibited Work

以下は禁止する。

## 3.1 Gate越境

E4-G03以降へ先行してはならない。

特に以下を実装しない。

* persistent StageExecutionの全family cutover
* Causal stage persistence導入
* GenericExecutorのstage contract再編
* ExecutionResult / StageResult consolidation
* Artifact metadata ownership consolidation
* ArtifactStorePort再設計
* lineage writer authority切替
* structural generic lineage dual-write除去
* legacy source削除
* legacy migration削除
* Product-only clean bootstrap finalization
* frontend redesign
* CLI architecture変更

## 3.2 Architecture再設計

以下は禁止。

* GenericExecutorをcanonical lifecycle ownerにする
* familyごとに新しい別Execution lifecycleを追加する
* CausalとFamilyの双方を最終canonical authorityとして維持する設計に戻す
* scientific algorithmを変更する
* Result / Artifact / Lineage architectureをG02で先行決定する
* physical Artifact keyをExecution identityへ利用する
* root legacy migrationをProduct migration chainへ接続する

## 3.3 Test回避

禁止。

* `skip` / `xfail`追加によるfailure回避
* assertion緩和
* failing test削除
* expected valueをimplementation defectへ合わせる変更
* concurrency testをserial化してdouble-claim defectを隠す

## 3.4 Git

禁止。

```text
git add .
git add -A
git reset --hard
git restore .
git clean -fd
git stash
```

既存working tree差分を勝手に変更・削除してはならない。

既知のunrelated working-tree差分として、

```text
deploy/.nfs000000000076202f00000088
```

の削除状態が存在する可能性がある。

これはE4-G02 scope外であり、stage / restore / delete / recreateしてはならない。

---

# 4. Current State

## 4.1 Architecture checkpoint

E4-G01は独立レビュー済みでPASS。

確定済みcontract:

* one canonical persistent Product Execution identity
* family discriminator:

  * `CAUSAL`
  * `EXPLORATORY`
  * `PREDICTIVE`
* common lifecycle authority
* retry = same Execution ID
* rerun = new Execution ID
* revise = new Execution ID
* canonical claim authority
* GenericExecutor is not lifecycle owner
* persistent StageExecutionはG03で実装
* Result / Artifact ownershipはG04で実装
* full runtime convergenceはG05で実施

## 4.2 Baseline

Architecture / documentation baseline:

```text
e70c6f7f1f63ce2568c85482bc20a355da66b7cf
```

Coding Agent開始時のactual HEADはこれより後でもよい。

ただしbaseline以降にproduction source / test / migrationのENH-E4 implementationが既に存在する場合は、内容を確認し、本Trialとの重複・競合がないことを説明する。

予期しないproduction implementationが存在し、G02 starting stateを一意に確定できない場合は `DESIGN_BLOCKED` とする。

## 4.3 Migration

expected Product migration head:

```text
20260807_product_0006
```

開始時にactual Product migration headを静的に確認する。

actual headが異なる場合:

* 正当なbaseline以降変更であることをGit historyから説明できる → actual headを使用
* 説明不能またはbranch mismatch → `DESIGN_BLOCKED`

root legacy migration chainは使用しない。

---

# 5. Gate Status

Status values:

* `NOT_STARTED`
* `IN_PROGRESS`
* `READY_FOR_TEST`
* `PASS`
* `FAIL`
* `BLOCKED`
* `DESIGN_BLOCKED`

| Gate       | Purpose                                       |             Status at handoff |                 Latest Trial | Evidence            |
| ---------- | --------------------------------------------- | ----------------------------: | ---------------------------: | ------------------- |
| E4-G01     | Canonical contract/schema foundation          |                          PASS | special documentation review | commit `e70c6f7...` |
| **E4-G02** | **Canonical Execution aggregate and claim**   | **NOT_STARTED → IN_PROGRESS** |                       **01** | **本書**              |
| E4-G03     | Persistent StageExecution and runner boundary |                   NOT_STARTED |                          N/A | future Gate         |
| E4-G04     | Result/Artifact ownership boundary            |                   NOT_STARTED |                          N/A | future Gate         |
| E4-G05     | Product Execution Convergence                 |                   NOT_STARTED |                          N/A | future Gate         |
| E4-G06     | Lineage authority consolidation               |                   NOT_STARTED |                          N/A | future Gate         |
| E4-G07     | Legacy, CLI, migration boundary               |                   NOT_STARTED |                          N/A | future Gate         |
| E4-G08     | Final clean bootstrap and architecture audit  |                   NOT_STARTED |                          N/A | future Gate         |

---

# 6. Trial Rules

Active Trial:

```text
E4-G02 Trial 01
```

Rules:

1. 1 Coding execution = 1 Gate / 1 Trial。
2. Trial番号は2桁ゼロ埋め。
3. Trial番号を再利用しない。
4. Coding AgentはTrial 01完了時に `READY_FOR_TEST` または `DESIGN_BLOCKED` で停止する。
5. Independent Test AgentがFAILした場合のみ、次のCoding executionをE4-G02 Trial 02とする。
6. E4-G02がPASSするまでE4-G03へ進まない。
7. BLOCKED / DESIGN_BLOCKEDをfuture Gateの実装で迂回しない。
8. Coding Agent自身のself-test結果をGate PASSと扱わない。

---

# 7. Gate Implementation Contract

## 7.1 Objective

E4-G02終了時に、

```text
one canonical Execution identity
+
one family discriminator
+
one lifecycle state authority
+
one claim / lease authority
+
one mutation identity contract
```

がproduction codeとpersistenceで成立していること。

G02はfull Product runtime cutover Gateではない。

旧Causal / Family lifecycle implementationはG05まで一時的に存在してよい。

ただし、G02で導入するcanonical pathが旧claimerへclaim authorityを委譲してはならない。

---

## 7.2 Required Architecture After G02

```text
Product canonical execution service
        |
        +-- create canonical Execution
        |
        +-- persist through canonical repository/UoW
        |
        +-- atomic claim / lease ownership
        |
        +-- canonical state transition
        |
        +-- retry / rerun / revise / cancel mutation contract
```

family差は、

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

というworkflow discriminatorとして扱う。

family差を理由にclaim/repository/state authorityを分割してはならない。

---

## 7.3 Canonical Execution Identity Contract

全canonical Product Executionは一つのExecution ID namespaceを使用する。

MUST:

* Execution IDはfamilyを跨いでglobally uniqueである。
* Execution ID semanticsはCausal / Exploratory / Predictiveで同一。
* family discriminatorをExecution自身が持つ。
* family discriminatorの値は最低限:

  * `CAUSAL`
  * `EXPLORATORY`
  * `PREDICTIVE`
* family discriminatorはlifecycle authorityを切り替えるキーではない。
* project ownership / immutable execution snapshot等、既存canonical Product contractで必須のExecution metadataを失わない。

既存physical table/classを再利用するか、新physical representationを導入するかはimplementation detailである。

ただし最終semantic authorityは一つでなければならない。

---

## 7.4 Creation Contract

canonical creation service/repositoryは三familyすべてのExecutionを生成できなければならない。

G02では全user-facing routeをcanonical creationへcutoverする必要はない。

そのcutoverはG05。

ただしG02終了時点で、三familyのcanonical Executionを同一service/repository contractから作成し、claim/state lifecycleへ進められることをautomated testで実証する。

旧Causal / Family creation pathは `E4-TD-001` として一時残存してよい。

旧pathを「canonical implementation」として呼び出してはならない。

---

## 7.5 Canonical Lifecycle State Contract

最低限のcanonical lifecycle:

```text
QUEUED
  ↓
RUNNING
  ↓
SUCCEEDED | FAILED | CANCELLED
```

既存approved Product stateに追加状態が存在する場合、その意味を破壊せずcanonical contractへ整合させる。

MUST:

* state transitionはcanonical domain/application layerで検証する。
* persistence側の直接status updateだけでdomain validationを迂回しない。
* terminal stateから無条件にRUNNINGへ戻せない。
* family固有で許可されないoperationはexplicitにrejectする。
* successful prior outputをcancel/retry処理で暗黙に書き換えない。

G03以降のStage stateは本Gateで実装しない。

---

## 7.6 Claim / Lease Contract

claim authorityは一つのcanonical Execution repository/service abstractionへ集約する。

MUST:

* claimはatomic ownership acquisitionである。
* 同一Executionを同時に複数workerが正常claimできない。
* claim成功時にclaimant / ownershipを識別可能である。
* leaseを採用する場合、そのownershipとexpiryを永続化し監査可能にする。
* ownerでないworkerによるrenew / completion / mutationを拒否する。
* expired leaseの扱いは一意であり、silent double ownershipを許可しない。
* claimとstate transitionのtransaction boundaryを明示する。
* canonical claim operationが旧Causal / Family claimerをdelegate authorityとして呼ばない。

heartbeat interval等の運用値はcurrent worker conventionを優先してよい。

ただしlease ownership semanticをfamily別に分離してはならない。

---

## 7.7 Retry Contract

retryは同じExecution IDを維持する。

MUST:

```text
retry:
    execution_id = unchanged
    attempt/retry occurrence = distinguishable
```

G03のpersistent StageExecution attempt modelを先行実装してはならない。

G02ではExecution-levelで、

* retry occurrence
* retry reason / requested action
* relevant timestamps / ownership metadata

を既存modelと整合する最小形で識別できればよい。

retryでfamilyを変えてはならない。

retryでExecution IDを新規生成してはならない。

---

## 7.8 Rerun Contract

rerunはnew Executionである。

```text
source execution
        ↓ typed source/base relation
new execution_id
```

MUST:

* new Execution IDを生成する。
* source Executionとのtyped relationを保持する。
* generic lineage edgeをG02で新たなauthorityとして導入しない。
* physical output key等でsource relationを表現しない。

lineage projection/writerの最終整理はG06。

G02ではtyped Execution relationを正本とする。

---

## 7.9 Revise Contract

reviseはnew Executionである。

MUST:

* new Execution IDを生成する。
* base/source Executionとのtyped relationを保持する。
* change reason / revision context等、既存approved Product contractで必要なrevision metadataを保持する。
* in-place rewriteによって元Executionのidentity/historyを破壊しない。

rerunとのsemantic differenceを失わせない。

---

## 7.10 Cancel Contract

cancelはcanonical lifecycle mutationである。

MUST:

* queued/running Executionに対するcancel policyを一つのcanonical serviceで処理する。
* invalid cancelをrejectする。
* already terminal successful Executionをcancelによって別の成功履歴へ書き換えない。
* partial output semanticsを本GateでResult/Artifact redesignしない。

Result/Artifact cleanupの統一はG04。

---

## 7.11 Repository / UoW Contract

canonical Execution persistenceはProduct repository/UoW boundaryを使用する。

MUST:

* domain/applicationからraw family-specific persistence authorityを直接操作しない。
* creation / claim / state mutationのtransaction boundaryを一意にする。
* optimistic lock、row lock、conditional update等、同等のatomicity mechanismを使用する。
* double claim / stale ownershipをDB levelまたはrepository contractで防止する。
* Product project scopeを跨ぐExecution mutationを許さない。

exact ORM/class/table nameは本書では固定しない。

---

## 7.12 Worker Boundary

G02ではworker全体のworkflow executionをG05まで全面cutoverしない。

ただしcanonical worker claim boundaryを実装する。

MUST:

* canonical claim function/serviceはfamily-neutral。
* Causal / Exploratory / Predictiveを同一claim APIから扱える。
* old family-specific claimerをcanonical claim pathから呼び出さない。
* GenericExecutorはclaimを行わない。
* GenericExecutorはcanonical Execution commit authorityを持たない。

Stage orchestrationはG03。

---

# 8. Transition Debt

E4-G02では以下を正式にOPENする。

```text
E4-TD-001
```

意味:

```text
old Causal / Family Execution creation/write paths may remain temporarily
until Product Execution Convergence Gate E4-G05.
```

Authority rule:

* new canonical G02 pathのauthority = canonical Execution repository/service
* old path = temporary compatibility surface
* old claimer = canonical authorityではない
* coexistenceをfinal architectureとして扱わない

Exit Gate:

```text
E4-G05
```

Exit Criterion:

```text
No old Causal / Family lifecycle accepts new Product writes.
```

Coding AgentはE4-TD-001をG02で勝手にcloseしない。

旧lifecycleの全面撤去はG05の責務。

---

# 9. Migration Contract

Product migration変更はCONDITIONAL MUST。

canonical Execution persistenceにschema変更が必要ならProduct migrationを追加する。

Rules:

1. `alembic_product.ini` / `product_migrations/` のみ使用する。
2. starting headはactual repository stateで確認する。
3. expected baseline headは `20260807_product_0006`。
4. new revisionはactual Product headを`down_revision`とする。
5. root `alembic.ini` / legacy `migrations/` を変更・実行しない。
6. historical application data migrationを実装しない。
7. G02でold Causal / Family tablesをdropしない。
8. old tablesをfinal authorityとして再宣言しない。
9. downgrade pathをrepository policyに従い実装する。
10. migration testはactive user environmentを破壊しないisolated DBで実施可能な形にする。

schema変更不要と判断した場合は、implementation reportへ理由を記載する。

---

# 10. Automated Test Code Contract

Coding AgentはE4-G02 ACを独立Test Agentが再実行できるautomated test codeを用意する。

最低限、以下をtest node単位で識別可能にする。

### AC-001

* one canonical Execution identity authority
* family discriminator:

  * CAUSAL
  * EXPLORATORY
  * PREDICTIVE
* same repository/service contract

### AC-002

各familyについて:

```text
create
→ QUEUED
→ atomic claim
→ RUNNING
→ terminal
```

をcanonical contractで検証する。

### AC-003

* retry same ID
* retry occurrence distinguishable
* rerun new ID + typed source relation
* revise new ID + typed base relation

### AC-004

* canonical claim pathがold family-specific claimerを使用しない
* GenericExecutorがclaim/commit authorityを持たない

### AC-005

* invalid transition reject
* double claim reject
* non-owner lease mutation reject
* stale/expired lease behavior is deterministic

PostgreSQL-specific atomicity/concurrencyをunit mockだけで証明したことにしない。

必要箇所にはreal PostgreSQL testを用意する。

Implementation Completion Reportに、

```text
AC ID
→ automated test path
→ test node ID
```

mappingを必ず記載する。

---

# 11. Allowed / Forbidden Change Areas

## Allowed

Active Gateに必要な範囲で変更可:

```text
src/ariadne/product/domain/
src/ariadne/product/application/
src/ariadne/product/ports/
src/ariadne/product/persistence/
src/ariadne/interfaces/worker/
tests/product/
tests/integration/
product_migrations/
```

worker pathはclaim boundaryに直接必要な部分のみ。

## Conditionally Allowed

```text
src/ariadne/interfaces/web_api/
```

canonical Execution serviceをcompile/import可能にする最小wiringだけ。

user-facing全route cutoverはG05なので禁止。

```text
pyproject.toml
```

原則変更禁止。

import/package registration上どうしても必要な場合のみ変更し、implementation reportで理由を説明する。

新規dependency追加は禁止。

## Forbidden

```text
src/ariadne/product/workflow/
src/ariadne/product/domain/stage_execution.py
Result / Artifact consolidation areas
lineage writer / closure / export areas
src/ariadne/legacy/
frontend/
root migrations/
```

ただしcompile failure等、G02変更に直接起因するminimal compatibility editが必要な場合は、semantic scopeを拡張せずimplementation reportへ明示する。

---

# 12. G02 Acceptance Criteria

## E4-G02-AC-001

canonical Execution identityとfamily discriminatorが一つのauthorityで生成される。

PASS-ready implementation condition:

* three families supported
* one semantic Execution identity contract
* one canonical repository/service authority
* persistent family discriminator

## E4-G02-AC-002

Causal / Exploratory / Predictiveが同じclaim/state contractで

```text
QUEUED → RUNNING → terminal
```

を処理できる。

## E4-G02-AC-003

```text
retry  = same Execution ID
rerun  = new Execution ID + typed source relation
revise = new Execution ID + typed base relation
```

が成立する。

## E4-G02-AC-004

old family-specific claimerがcanonical new-write authorityとして使われない。

注意:

old lifecycle path自体はE4-TD-001としてG05まで存在してよい。

したがってG02では、

```text
old implementation exists
```

だけをfailureとしない。

failureなのは、

```text
canonical path delegates authority to old claimer
```

である。

## E4-G02-AC-005

以下が拒否される。

* invalid state transition
* double claim
* lease ownership violation
* non-owner completion/mutation
* invalid reclaim semantics

---

# 13. Negative Requirements

以下が一つでも起きた場合、Coding completion criteriaを満たさない。

* GenericExecutorがclaimする
* GenericExecutorがcanonical lifecycle commitする
* Causal / Exploratory / Predictiveごとにcanonical claimerを複製する
* retryがnew Execution IDを作る
* rerun/reviseが元Executionをin-place rewriteする
* canonical claimがatomicでない
* old claimerをcanonical repositoryの内部delegate authorityにする
* StageExecutionをG02で全面実装する
* Result/Artifact ownershipをG02でcutoverする
* lineage writerをG02でcutoverする
* legacy codeを削除する
* root legacy migrationへ依存する
* unrelated frontend/auth/dataset behaviorを変更する

---

# 14. Implementation Completion Conditions

Coding Agentが `READY_FOR_TEST` とできるのは全て満たした場合のみ。

1. E4-G02 scope実装完了。
2. AC-001〜005に対応するautomated test codeが存在。
3. canonical creation/claim/state/mutation pathが三familyを扱える。
4. old claimerがcanonical authorityとして呼ばれない。
5. E4-TD-001が明示的に残っている。
6. G03以降へ先行実装していない。
7. migrationが必要ならProduct migrationを追加済み。
8. root legacy migrationを変更していない。
9. Coding Agentによるtargeted self-checkを実行済み。
10. implementation commitを作成済み。
11. Implementation Completion Reportを作成済み。
12. cumulative implementation report detailを作成または更新済み。
13. reportにAC→test node mappingを記載済み。
14. unrelated working-tree差分をcommitしていない。

Coding Agentのself-checkがPASSしてもGate PASSではない。

---

# 15. Required Outputs

## 15.1 Implementation commit

production source / test / migration implementationを一つのimplementation commitとして固定する。

report-only commitとは区別する。

## 15.2 Completion report

作成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
E4-G02_01_implementation_completion_report.md
```

Template:

```text
20_implementation_reports/
TEMPLATE_implementation_completion_report.md
```

Status:

```text
READY_FOR_TEST
```

または

```text
DESIGN_BLOCKED
```

Gate PASS/FAILを記載しない。

## 15.3 Cumulative detail

作成または更新:

```text
20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

Template:

```text
20_implementation_reports/
TEMPLATE_implementation_report_detail.md
```

## 15.4 Mandatory report contents

最低限:

* baseline commit
* starting commit
* implementation commit full SHA
* migration previous/new head
* files added/modified/deleted
* G02 contract item → implementation mapping
* AC-001〜005 → automated test path/node mapping
* E4-TD-001 current state
* changes to PASS済みG01 contract: normally `NONE`
* known limitations
* out-of-scope areas not modified
* exact self-check commands/results
* `git status --short`

---

# 16. Coding Agent Self-check

Independent Gate testの代替ではないが、handoff前に最低限実行する。

1. changed/new G02 unit/component tests
2. changed/new worker tests
3. changed/new PostgreSQL tests when required and isolated environment exists
4. migration static/head check if migration added
5. relevant pre-existing execution/worker regression tests

full browser E2EはG02では不要。

scientific benchmarkはG02では不要。

active development databaseを破壊するtestは実行しない。

---

# 17. Stop Conditions

以下で必ず停止する。

## READY_FOR_TEST

全Implementation Completion Conditionsを満たした。

その場合:

* reportを作成
* implementation commitを固定
* Test Agentへhandoff可能な状態にする
* **Test Agent作業を自分で開始しない**
* **E4-G03へ進まない**

## DESIGN_BLOCKED

本書とcurrent production codeだけでは解消不能なsemantic contradictionがある。

reportへ以下を記録する。

* conflicting contract
* source evidence
* why implementation choice would require architecture decision
* minimum decision required

勝手に00 backgroundを読み直して解決しない。

## Other stop

* wrong branch
* unexpected source implementation after baseline
* Product migration graph inconsistency
* unrelated dirty stateを安全に分離できない
* required isolated PostgreSQL environmentなしでimplementation correctness自体を確認不能

---

# 18. Supplemental Implementation Context

## Target architecture summary

G02は、

```text
dual lifecycle
    ↓
canonical Execution infrastructure exists
```

まで進めるGate。

まだ、

```text
all runtime paths cut over
```

するGateではない。

full convergenceはE4-G05。

## Transition boundary

G02終了時には意図的に、

```text
canonical Execution path
+
temporary old Causal / Family paths
```

がRepository内に共存し得る。

この状態は `E4-TD-001` としてbounded。

「old codeがまだある」こと自体をG02 failureにしない。

一方、

```text
canonical path itself has multiple claim authorities
```

はG02 failure。

## Dependency policy

新規third-party dependencyを追加しない。

標準library、既存SQLAlchemy/Alembic/Product infrastructureを使用する。

## Scientific invariants

scientific algorithm / estimator / predictor / preprocessing semanticsを変更しない。

## Non-goals

* Stage persistence convergence
* Result/Artifact convergence
* Lineage convergence
* Legacy removal
* final migration/bootstrap cleanup
* UI redesign
* performance optimization
