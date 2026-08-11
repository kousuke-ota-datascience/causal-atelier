# 背景

`06a_Ariadne_ENH-E4_G05_実装指示書_中断後再開.md` を実行したところ、以下の状況となり実装が中断した

```
• ## 結論

  G05 Trial 01 は未完了です。現在の変更は部分実装であり、READY_FOR_TEST、implementation report、implementation commit は未作成です。

  ## 事実：現在の実装済み部分

  - API DI では Exploratory / Predictive service に canonical ExecutionService を注入済み。
  - Exploratory submit は canonical Execution / persistent StageExecution を生成する経路へ切替済み。
  - Predictive submit も canonical submission を呼ぶ経路を追加済み。
  - worker runner から Exploratory / Predictive の旧 claim_next() polling を削除し、canonical uow.executions.claim_next() だけを使う形へ変更済み。
  - ExecutionProcessor に Causal / Exploratory / Predictive の runner registry dispatch を追加済み。
  - canonical cancel 時に未終端の canonical StageExecution を CANCELLED に遷移させる変更を追加済み。
  - exploratory submit のみを対象に、canonical row 作成・FamilyExecutionOrm 非作成を確認するテストを追加済み。

  直近の確認結果:

  - compileall：成功
  - git diff --check：成功
  - tests/product/test_enh_e4_g05_submission_convergence.py：1 passed
  - G03 GenericExecutor / G04 Result/Artifact contract の unit tests：12 passed

  ## 事実：未達・production defect

  以下は source inventory で確認済みです。

   項目                                         状態      根拠
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Exploratory canonical read projection        未実装    list_results / get_result / create_analysis_draft が FamilyResultOrm を参照
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   Predictive canonical read projection         未実装    list/get/stages/results/artifacts/lineage が Family*Orm を参照
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   Predictive mutation delegation               未実装    cancel/retry/rerun/revise が FamilyExecutionOrm / FamilyStageExecutionOrm を変更
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   旧 family worker methods shutdown            未実装    Exploratory / Predictive service に claim_next / process_execution が残り、旧 ORM を authority として使用
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   canonical Result/Artifact ownership          不完全    family runner output を DIAGNOSTICS_RESULT/PASS envelope に変換しており、family 固有の result type/status を canonical typed
                                                          metadata として表現していない
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   PostgreSQL Golden Path                       未実施    Exploratory / Predictive / Cross-family / old-table-count negative の標準 runner evidence がない
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   failure → old authority fallback negative    未実装    専用 test がない
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   G02/G03/G04 PostgreSQL regression            未実施    前回の unit test 以外の今回の変更に対する実行証跡がない
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   TD-001/002/003 closure evidence              未作成    runtime negative が未実施
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   TD-004 inventory                             未作成    report/ledger 未作成
  ───────────────────────────────────────────  ────────  ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   completion report / ledger / fixed commit    未作成    20_implementation_reports/G05/ に report がない。HEAD は開始時の 9038404 のまま

  ## 作業ツリー

  G05 による未コミット変更は以下です。

  - src/ariadne/interfaces/web_api/dependencies.py
  - src/ariadne/interfaces/web_api/routers/exploration.py
  - src/ariadne/interfaces/worker/execution_processor.py
  - src/ariadne/interfaces/worker/runner.py
  - src/ariadne/product/application/execution_service.py
  - src/ariadne/product/application/exploratory_service.py
  - src/ariadne/product/application/predictive_workflow_service.py
  - tests/product/test_enh_e4_g05_submission_convergence.py

  また、既存の unrelated changes として Control Sheet 編集、.nfs 削除、G05 instruction directory の未追跡があります。これらには変更を加えていません。

  ## 判断

  「canonical submit/claim への部分切替」は進んでいますが、G05 の本質である全 Product path の authority convergence は未達です。次の実装は、旧 family service の read/mutation を
  canonical projection/delegation に置換し、family 固有 Result/Artifact metadata を canonical schema で表現できる最小拡張を行う必要があります。

```

# 指示文

以下を支持文として、実装を再開させた

`````
# E4-G05 Trial 01 — 中断後再開・完遂指示

G05 Trial 01を現在の未コミット作業ツリーから継続し、`06_Ariadne_ENH-E4_G05_実装指示書.md` の全Implementation Completion Conditionsを満たすまで実装を続行せよ。

## 1. 現在状態の扱い

現在の部分実装は破棄しない。

まずactual working tree diffを確認し、既に実装済みの変更を再実装しないこと。

現在確認されている以下の変更は、G05 Trial 01の継続中の実装として扱う。

* Exploratory / Predictive serviceへのcanonical `ExecutionService` injection
* Exploratory canonical submit
* Predictive canonical submission path
* canonical `uow.executions.claim_next()` へのworker claim convergence
* family runner dispatch
* canonical cancellation時のStageExecution cancellation
* Exploratory submit convergence test

Trial番号を変更してはならない。

---

## 2. 今回停止した理由は停止条件ではない

前回列挙した以下は、作業停止理由ではなく、**今から実装して閉じるべきremaining work**である。

* Exploratory canonical Result/Artifact read projection未実装
* Predictive canonical read projection未実装
* Predictive mutation delegation未実装
* old family worker methods shutdown未実装
* family固有Result/Artifact metadataのcanonical representation不完全
* PostgreSQL Golden Path未実施
* old authority fallback negative未実装
* G02/G03/G04 PostgreSQL regression未実施
* TD-001/002/003 closure evidence未作成
* TD-004 inventory未作成
* completion report / ledger / fixed implementation commit未作成

これらを再度列挙して停止してはならない。

---

## 3. 作業管理方法

`06_Ariadne_ENH-E4_G05_実装指示書.md` のImplementation Completion Conditions 1〜36を内部チェックリストとして管理すること。

各項目を次のいずれかで管理する。

```text
TODO
IN_PROGRESS
DONE
DESIGN_BLOCKED
```

`TODO` または `IN_PROGRESS` が残っている間は作業を続行する。

途中で新しいproduction defectを発見した場合も、approved architecture内で解決可能なら修正して続行する。

---

## 4. 実装順序

以下の順で完遂する。

### Phase A — canonical family semantic representation

Exploratory / Predictiveの既存scientific semanticsをinventoryし、canonical Result/Artifact ownershipへlosslessに変換できるようにする。

現在のようにfamily outputを一律:

```text
DIAGNOSTICS_RESULT
PASS
```

へ押し込むことで既存family固有semanticを失ってはならない。

必要ならG04 contractを維持したまま、minimal typed extensionを行う。

例:

```text
result_type
scientific_status
metadata_json
payload_json
schema/version
```

等の既存canonical contractを利用する。

既存canonical schemaでsemantic lossなく表現できないことが実証された場合は、G05 06で許可されているminimal Product migrationを追加してよい。

これはmigrationが必要という理由だけでは`DESIGN_BLOCKED`ではない。

---

### Phase B — Exploratory convergence completion

以下をcanonical authorityへ置換する。

```text
list_results
get_result
create_analysis_draft
その他new canonical executionを読むuser-visible surface
```

new Exploratory executionsについて:

```text
Execution
StageExecution
Result
Artifact
```

をcanonical repositoriesからprojectionする。

historical old-row read compatibilityが必要ならread-only compatibilityとして分離する。

old Family ORMをnew executionのauthorityとして使用しない。

---

### Phase C — Predictive convergence completion

Predictiveについて以下をcanonical projection/delegationへ置換する。

```text
execution get/list
stages
results
artifacts
lineage-facing projection where required for current API
cancel
retry
rerun
revise
```

lifecycle mutationはG02 canonical semanticsへdelegateする。

old `FamilyExecutionOrm` / `FamilyStageExecutionOrm`をmutation authorityとして使用しない。

G06 lineage final consolidationは行わない。

---

### Phase D — old family lifecycle shutdown

Exploratory / Predictiveの旧:

```text
claim_next()
process_execution()
direct Family ORM persistence
```

について、Product write authorityを停止する。

sourceをG05で削除する必要はない。

残す場合は:

```text
canonical authorityへdelegate
```

または:

```text
explicitly reject non-canonical write
```

のどちらかにする。

旧authorityをfailure fallbackとして残してはならない。

---

### Phase E — mandatory automated coverage

以下を全て実装する。

#### Causal Golden Path

```text
submit
-> canonical Execution
-> persistent StageExecution
-> canonical claim
-> Result/Artifact
-> terminal state
```

#### Exploratory Golden Path

同上。

#### Predictive Golden Path

同上。

#### Cross-family authority

三familyが:

```text
same Execution repository
same claim authority
same StageExecution persistence
same Result owner
same Artifact owner
```

を使用すること。

#### Old-write runtime negative

real PostgreSQLでold tablesのbefore/after row countを取得する。

対象:

```text
FamilyExecution
FamilyStageExecution
FamilyResult
FamilyArtifact
```

G05 Golden Paths実行後にnew lifecycle/output rowが増えてはならない。

#### Failure fallback negative

canonical processing/submission failureをinjectし:

```text
old Family authorityへfallbackしない
```

ことを検証する。

#### Mutation

actual exposed:

```text
cancel
retry
rerun
revise
```

をcanonical authorityで検証する。

#### Read projection

new canonical Exploratory / Predictive execution/outputがexisting supported family-facing API/serviceから読めること。

---

## 5. 既存E3テストの扱い

旧`FamilyExecution` authorityを直接claim/processする前提のE3テストがG05 architectureと衝突する場合、それを理由に停止してはならない。

次のように分類する。

### A. passed architecture contractを表すtest

G02/G03/G04等の既に保護されたcontractなら壊さず通す。

### B. G05で廃止されるold authorityを正としているtest

canonical worker / canonical lifecycleを検証するtestへ更新または置換する。

ただし単にtestを削除してcoverageを失ってはならない。

old behaviorを削除した場合、新canonical behaviorを同等以上のautomated coverageで置き換える。

---

## 6. PostgreSQL verification

required test code完成後、repository標準runnerだけを使用する。

```bash
scripts/test/run_product_postgres_tests.sh ...
```

manual Docker / DSN / psql / Alembic workaroundは禁止。

少なくとも:

```text
G05 Causal Golden Path
G05 Exploratory Golden Path
G05 Predictive Golden Path
G05 cross-family authority
G05 old-table negative
G05 no-fallback negative
G02 regression
G03 regression
G04 regression
PostgreSQL contract
```

をactual required nodesで実行する。

途中failureがproduction defectなら修正して再実行する。

---

## 7. Transition Debt

実装とverificationが完了したら、証拠に基づいて:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
```

をCompletion Reportへ記録する。

TD-004についてはG06へ渡すremaining structural generic lineage duplicate writesをactual sourceからinventoryする。

存在する場合:

```text
file
function
relation kind
reason deferred
```

を記録する。

存在しない場合は:

```text
NONE observed
```

と事実を記録する。

G06 implementationは行わない。

---

## 8. Commit / Report

全mandatory implementation/testが完了した後にfixed implementation commitを作成する。

そのfixed SHAに対して最終self-checkを行う。

次にrepository templateへ完全準拠して:

```text
20_implementation_reports/G05/
E4-G05_01_implementation_completion_report.md
```

を作成する。

さらに:

```text
20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

を更新する。

Reportはrequired section/fieldを省略、merge、short-form化してはならない。

値がないfieldは:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使用する。

---

## 9. 停止条件

この継続作業でturnを終了してよいのは、原則として以下の2条件だけである。

### READY_FOR_TEST

以下を全て完了した場合。

```text
全Implementation Completion Conditions DONE
required PostgreSQL verification DONE
G02/G03/G04 regression DONE
TD-001/002/003 closure evidence DONE
TD-004 inventory DONE
fixed implementation commit DONE
template-compliant completion report DONE
detail ledger update DONE
```

その場合:

```text
READY_FOR_TEST
```

としてTest Agentへhandoffして停止する。

### DESIGN_BLOCKED

approved ENH-E4 architectureから論理的に解決不能なsemantic contradictionがあり、人間による新しいarchitecture decisionが必要な場合のみ。

その場合は:

```text
exact contradiction
actual source/schema facts
why permitted minimal extension cannot solve it
required human decision
```

を示す。

---

## 10. 明示的に停止理由として認めないもの

以下は作業停止理由ではない。

```text
まだ実装量が多い
既存E3 testがold architecture前提
read projectionが未実装
mutationが未実装
migrationが必要そう
新しいproduction defectを発見した
testが途中でFAILした
PostgreSQL testをまだ実行していない
reportをまだ作っていない
commitをまだ作っていない
```

これらはすべて、G05 Trial 01を継続して閉じる対象である。

---

G05 Trial 01を最後まで完遂せよ。

`````
