# Database Reinitialization — Completion Summary / Decision Record

## 1. Document Purpose

本書は、

```text
ENH-E4 eliminate dual execution
```

の一環として実施した database reinitialization について、

* 何を確認したか
* 何を削除したか
* 何を再構築したか
* 何が実証されたか
* どの判断を採用したか
* 何を未解決事項として残したか

を記録する完了サマリ兼 Decision Record である。

詳細なoperator promptおよびcommand execution logは、同ディレクトリ内の各 `*_prompt.md` / `*_result.md` を一次証跡とする。

本書はそれらを置き換えるものではなく、最終判断を集約するものである。

---

# 2. Context

今回のdatabase reinitializationは、単独のDB保守作業ではない。

上位作業:

```text
20260808-01_ENH-E4_eliminate_dual_execution
```

において、

> Execution / Result / Lineage 等について存在する二重実行・二重管理構造を解消する

ための事前作業として実施した。

開発環境は本運用前であり、既存application dataには保持要件がない。

そのため、

> 既存データとの後方互換性を維持する

のではなく、

> 空の永続領域から、現在の正規アーキテクチャだけでシステムを再構築できることを確認する

ことを優先した。

---

# 3. Operating Policy

本作業では以下を優先した。

1. システムを壊さない
2. 破壊対象を実測してから操作する
3. Agent自身による推論・対象選択を最小化する
4. 実行commandとstdout / stderrをGit管理下へ残す
5. 不可逆操作の前にcheckpointを設ける
6. failure時に自動retry・自動修復しない
7. active environmentとstale environmentを混同しない
8. DB初期化とENH-E4本体のarchitecture変更を混同しない

実行モデルは原則として以下とした。

```text
fixed prompt
    |
    v
fixed commands
    |
    v
raw result
    |
    v
human review
    |
    v
next fixed prompt
```

---

# 4. Environment Identified

## 4.1 Active Compose Project

実測の結果、現在使用中のCompose projectは以下であった。

```text
ariadne-e1a
```

active service:

```text
database
migrate
api
worker
frontend
```

---

## 4.2 Active Persistence

active PostgreSQL persistence:

```text
ariadne-e1a_metadata-data
```

active artifact persistence:

```text
ariadne-e1a_artifact-data
```

artifact volumeは以下で共有されていた。

```text
api
worker
```

mount path:

```text
/state
```

artifact object root:

```text
/state/objects
```

---

## 4.3 Stale Compose Persistence

別のCompose projectに由来する以下のvolumeも存在した。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

ただし、これらにはactive container consumerが存在しなかった。

本作業ではactive environmentのreinitializationとstale environment cleanupを分離し、この2volumeは削除しなかった。

---

# 5. Pre-reset Database State

reset前のactive PostgreSQL databaseをread-onlyで確認した。

## 5.1 Schema

active databaseにはProduct schemaが存在した。

Product migration version table:

```text
alembic_version_product
```

Product revision:

```text
20260807_product_0006
```

legacy migration version table:

```text
alembic_version
```

は存在しなかった。

また、public schemaにはProduct系tableのみが存在し、legacy schemaとの物理的共存は確認されなかった。

### Conclusion

active databaseについて、

> legacy schema と Product schema が同一DB上で物理的に二重管理されている

という仮説は棄却された。

---

## 5.2 Existing Application Data

reset前にはProduct application dataが存在した。

主要な例:

```text
product_execution   > 0
product_result      > 0
product_artifact    > 0
```

全体として多数のExecution / Result / Artifact等が保存されていた。

これらについて保持要件はないため、reinitialization対象とした。

---

# 6. Pre-reset Artifact State

active artifact volume:

```text
ariadne-e1a_artifact-data
```

には実データが存在した。

確認時点:

```text
/state:
  approximately 4.6 MB

files:
  458

directories:
  700
```

したがって、

> DBだけを初期化しartifact storageを残す

方式は採用しなかった。

DB metadataとartifact storage間で孤児データを残さないため、active DB persistenceとactive artifact persistenceを同一reinitialization scopeに含めた。

---

# 7. Destructive Reset Performed

不可逆操作の前に以下を実施した。

1. active stack停止
2. 全active containerが停止したことを確認
3. containerを削除
4. active volume consumerが0であることを確認
5. volume identityをCompose labelで再確認

その後、以下のみを明示的に削除した。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

削除後、両volumeが存在しないことを確認した。

以下は削除しなかった。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

---

# 8. Database Rebuild

完全に空のactive persistenceからdatabaseを再構築した。

使用したmigration系統:

```text
alembic_product.ini
product_migrations/
```

legacy migration:

```text
alembic.ini
migrations/
```

は実行していない。

manual SQLによるschema補正も実施していない。

---

## 8.1 Product Migration Result

Product migrationはbaselineから順番に正常適用された。

最終revision:

```text
20260807_product_0006
```

migration container:

```text
exit code 0
```

database:

```text
running / healthy
```

---

## 8.2 Schema After Rebuild

再構築後:

```text
alembic_version_product:
  present

alembic_version:
  absent
```

public schemaにはProduct tableのみが存在した。

### Decision

現行database rebuild pathの正規migrationは、

```text
Product migration
```

とする。

database reinitializationのためにlegacy migrationを追加実行する必要はない。

---

# 9. Clean-state Verification Before Application Startup

Product migration完了直後、application serviceを起動する前に全Product application tableを確認した。

結果:

```text
Product application rows:
  0
```

存在する管理dataはmigration version informationのみであった。

### Conclusion

Product migration自体は、

* seed
* old execution data
* application state

を暗黙に生成しない。

---

# 10. Application Restore

database rebuild後に以下を復旧した。

```text
api
worker
frontend
```

同時にartifact volume:

```text
ariadne-e1a_artifact-data
```

が新規作成された。

---

## 10.1 Runtime State

復旧後:

```text
database:
  running / healthy

api:
  running / healthy

worker:
  running

frontend:
  running
```

API readiness:

```text
HTTP 200
```

frontend:

```text
HTTP 200
```

---

## 10.2 Artifact Initial State

再生成されたartifact volumeは初期状態で、

```text
state_files=0
object_files=0
```

であった。

---

## 10.3 Database State After Application Startup

application startup後も、

```text
Product application rows:
  0
```

を維持した。

legacy migration stateも出現しなかった。

### Conclusion

application startupそのものによって、

* Execution
* Result
* Artifact
* その他Product application data

が暗黙生成されることはない。

---

# 11. Functional Verification

clean rebuild後のシステムに対して、機能検証を実施した。

---

## 11.1 Isolated Active Product Tests

実PostgreSQL contract testを除外したActive Product testsを、active Compose persistenceから隔離した状態で実行した。

結果:

```text
131 passed
```

isolated testによってactive DB / artifact storageが変更されていないことも確認した。

---

## 11.2 Compose Golden Path

稼働中のclean Compose stackに対し、既存のProduct Golden Pathを実行した。

結果:

```text
PASS
```

Golden Pathによって実際に、

* Execution
* Result
* Artifact
* Lineage API
* export/download等

が動作することを確認した。

Golden Path実行後、active persistenceにはverification dataが生成された。

これは意図した一時データである。

---

# 12. Lineage Observation

functional verification中、重要なarchitecture observationが得られた。

Golden Path後:

```text
product_lineage_edge:
  0 rows
```

であった一方、Result lineage APIは正常動作した。

追加read-only evidence:

```text
lineage API:
  node_count = 11
  edge_count = 13

required node types:
  all present
```

したがって、

```text
lineage API works
```

と

```text
product_lineage_edge contains persisted rows
```

は同義ではない。

---

## 12.1 Current Observed Lineage Representations

現行コード上では少なくとも以下の2表現が存在する。

### A. Derived Result Lineage

Result / Execution / DatasetVersion / GraphVersion / Artifact / Annotation等のrelationshipから、query時にlineage graphを構築する。

概念的には:

```text
stored entities
    |
    v
LineageQueryService
    |
    v
nodes + edges generated at query time
```

### B. Persisted LineageEdge

```text
product_lineage_edge
```

として明示的に永続化されるlineage edge。

一部Product serviceから利用されていることが確認された。

---

## 12.2 Decision

database reinitializationでは、これら2表現について変更しない。

理由:

1. DB初期化のscope外である
2. `product_lineage_edge` が単純なobsolete tableとは断定できない
3. query-time lineageとpersisted lineageには異なる責務が存在する可能性がある
4. ENH-E4本体でarchitectureとして評価すべきである

したがって、本件は以下として引き渡す。

```text
ENH-E4 architecture review item:
  clarify responsibilities and lifecycle of
  derived lineage vs persisted product_lineage_edge
```

---

# 13. Verification Predicate Correction

最初のfunctional verification wrapperでは、

```text
product_lineage_edge > 0
```

をGolden Path成功条件として追加していた。

しかし追加調査により、このpredicateはGolden PathのResult lineage成功条件として不適切であることが判明した。

したがって、Phase 06aについては以下のように再評価する。

```text
Isolated Active Product tests:
  PASS

Compose Golden Path:
  PASS

Execution:
  VERIFIED

Result:
  VERIFIED

Artifact:
  VERIFIED

Result lineage API:
  VERIFIED

wrapper predicate product_lineage_edge > 0:
  INVALID
```

この誤predicateによるABORTはsystem failureとは扱わない。

---

# 14. Final Clean Reinitialization

Golden Pathによって生成されたverification dataを残さないため、functional verification後に再度active persistenceを完全初期化した。

実施経路:

```text
record temporary verification state
        |
        v
stop active stack
        |
        v
remove active containers
        |
        v
verify volume consumers = 0
        |
        v
delete active DB + artifact volumes
        |
        v
rebuild PostgreSQL
        |
        v
Product migration
        |
        v
restore application stack
        |
        v
final clean-state verification
```

この経路は、前段階で個別に成功確認済みの操作のみから構成した。

---

# 15. Final State

最終確認結果:

```text
Database:
  RUNNING / HEALTHY

API:
  RUNNING / HEALTHY

Worker:
  RUNNING

Frontend:
  RUNNING

API readiness:
  HTTP 200

Frontend:
  HTTP 200

Product migration:
  20260807_product_0006

legacy alembic_version:
  ABSENT

Product application rows:
  0

Artifact state files:
  0

Artifact object files:
  0
```

active persistence:

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

は新規clean stateとして再生成済みである。

repository-local:

```text
.ariadne
```

についてもfile count:

```text
0
```

を確認した。

---

# 16. Main Decisions

## DR-01: Active DBとArtifactを同時に初期化する

**Decision**

以下を同一reinitialization scopeとした。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

**Reason**

DB metadataだけを削除してartifact filesを残すと、orphan persistenceを残す可能性があるため。

---

## DR-02: Product migrationのみを正規rebuild pathとする

**Decision**

空DBからのrebuildには、

```text
alembic_product.ini
product_migrations/
```

のみを使用した。

legacy migrationは使用しない。

**Evidence**

Product migrationのみで、

* schema rebuild
* application startup
* Product tests
* Compose Golden Path

まで成功した。

---

## DR-03: Stale `causal-atelier_*` volumeを今回削除しない

**Decision**

以下は保持した。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

**Reason**

active environment:

```text
ariadne-e1a
```

とは異なるstale Compose projectに属しているため。

active reinitializationとstale environment cleanupを分離し、障害時の切り分けとauditabilityを維持する。

---

## DR-04: Lineage二表現をDB初期化では変更しない

**Decision**

以下の併存について、本作業では変更しない。

```text
derived lineage
persisted product_lineage_edge
```

**Reason**

両者の責務差が存在する可能性があり、単純なduplicate / obsoleteとはまだ断定できないため。

ENH-E4本体のarchitecture review itemとして扱う。

---

## DR-05: Golden Path後に再度clean resetする

**Decision**

functional verification dataを最終環境に残さない。

**Reason**

最終状態として、

> 動作検証済み、かつapplication dataは0件

を両立させるため。

---

# 17. What Has Been Demonstrated

本作業によって、以下は実測で確認された。

## 17.1 Database

```text
empty persistence
    |
    v
Product migration only
    |
    v
valid Product schema
```

が成立する。

legacy migrationへの依存は確認されなかった。

---

## 17.2 Runtime

clean Product databaseから、

```text
database
api
worker
frontend
```

を正常起動できる。

---

## 17.3 Persistence

clean startup後:

```text
Product application rows = 0
artifact files           = 0
```

を維持できる。

---

## 17.4 Functional Behavior

clean rebuildされた環境上で、

```text
Execution
Result
Artifact
Lineage API
```

を含むProduct Golden Pathが正常動作する。

---

# 18. What Has NOT Been Demonstrated

本作業から以下は結論しない。

1. ENH-E4全体の二重実行問題が解消済みである
2. legacy execution codeがすべて削除可能である
3. `product_lineage_edge` が不要である
4. derived lineageだけを唯一のlineage表現にすべきである
5. stale `causal-atelier_*` volumesが安全に削除可能である
6. production environmentでも同じreset操作を行うべきである

これらは別途検討対象である。

---

# 19. Remaining Work

## 19.1 Stale Compose Persistence Cleanup

対象候補:

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

status:

```text
PRESERVED
```

active environmentとは分離したcleanupとして扱う。

---

## 19.2 Lineage Architecture Review

確認すべき論点:

```text
derived Result lineage
vs
persisted product_lineage_edge
```

具体的には以下を明確化する。

* semantic responsibility
* producer
* consumer
* lifecycle
* source of truth
* persistence necessity
* overlap
* consistency guarantee

ENH-E4本体へ引き渡す。

---

## 19.3 NFS Temporary File Hygiene

working treeには以下の既知差分が存在した。

```text
D deploy/.nfs000000000076202f00000088
```

確認結果:

* HEAD上の内容は `deploy/nginx.conf` と同一
* runtimeからfilename参照なし
* Composeは `deploy/nginx.conf` を使用
* `.gitignore` にNFS temporary file除外なし

database reinitializationへのruntime影響はないと判断した。

ただしGit hygiene上は別cleanup候補である。

---

# 20. Completion Decision

## Decision

Database reinitializationを以下の状態で完了とする。

```text
DATABASE REINITIALIZATION:
  COMPLETE

FUNCTIONAL VERIFICATION:
  PASS

FINAL CLEAN STATE:
  VERIFIED
```

## Basis

* active database persistenceを完全削除した
* active artifact persistenceを完全削除した
* Product migrationのみでDBを再構築した
* legacy schemaは再生成されなかった
* application stackは正常復旧した
* Active Product testsは成功した
* Compose Golden Pathは成功した
* functional verification dataを再度削除した
* 最終Product application rowsは0
* 最終artifact filesは0
* systemはrunning / healthyである

---

# 21. Audit Trail

詳細なcommand-level evidenceは、同ディレクトリ内の以下のprompt / result系列を参照する。

```text
01_environment_inventory_*

02_database_configuration_*

03_pre_reset_state_*
03a_docker_access_diagnosis_*
03b_host_pre_reset_state_*
03c_compose_project_inventory_*
03d_active_database_inventory_*
03e_active_artifact_inventory_*

04a_quiesce_active_stack_*
04b_remove_active_containers_*
04c_delete_active_persistence_*

05a_rebuild_database_*
05b_restore_application_stack_*
05b1_runtime_diff_assessment_*
05b2_restore_application_stack_*

06a_post_reset_functional_verification_*
06a1_lineage_semantics_assessment_*
06a2_lineage_api_evidence_*

06b0_final_clean_reinitialization_*
```

各 `*_result.md` を実行事実の一次証跡とする。

---

# 22. Final Handoff to ENH-E4

database reinitializationからENH-E4本体へ引き渡す主要事項は以下の2点である。

### Handoff A — Database Rebuild

```text
Product migration chain alone is sufficient
to rebuild the active Product database
from empty persistence.
```

現行active databaseの再構築にlegacy migrationは不要であることを実測確認済み。

### Handoff B — Lineage Architecture

```text
Result lineage can be derived dynamically
while product_lineage_edge may also persist
explicit lineage relationships.
```

両者の責務・source of truth・重複範囲をENH-E4本体で明確化すること。

---

**Database reinitialization operator work is closed.**
