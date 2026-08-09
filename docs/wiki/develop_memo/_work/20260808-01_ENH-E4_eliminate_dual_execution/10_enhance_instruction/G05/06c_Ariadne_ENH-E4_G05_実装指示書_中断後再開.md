# 背景

`06b_Ariadne_ENH-E4_G05_実装指示書_中断後再開.md` に従い E4-G05 Trial 01 を再開した後、以下の実装状態で再び作業が中断した。

## 事実：保持されている Trial 01 の未コミット実装

以下は前回までに実装され、現在の working tree に保持されている。

- Web API dependency injection で Exploratory / Predictive service に canonical `ExecutionService` を注入した。
- Exploratory submit は canonical `Execution` と persistent canonical `StageExecution` を作成する経路へ切り替えた。
- Predictive submit に canonical submission を呼ぶ経路を追加した。
- worker runner から Exploratory / Predictive の旧 `claim_next()` polling を除去し、canonical `uow.executions.claim_next()` を唯一の claim entrypoint とした。
- `ExecutionProcessor` に Causal / Exploratory / Predictive の family runner dispatch を追加した。
- canonical cancel 時、未終端の canonical `StageExecution` を同一 UoW で `CANCELLED` に遷移させる変更を追加した。
- Exploratory submit が canonical row を作り、`FamilyExecutionOrm` を作らないことを確認する test を追加した。

さらに、Phase A の inventory により、既存 canonical `ResultType`、`ScientificStatus`、`ArtifactType` と PostgreSQL check constraint が Exploratory / Predictive の既存 scientific output type を許容しない事実を確認した。これを受け、`src/ariadne/product/domain/enums.py` に以下の enum 値を追加したが、対応する domain validation、ORM constraint、Product migration は未実装である。

- Exploratory Result: `DATA_PROFILE_RESULT`、`DISTRIBUTION_RESULT`、`ASSOCIATION_RESULT`、`GROUP_SUMMARY_RESULT`、`CHART_RESULT`
- Predictive Result: `SPLIT_RESULT`、`TRAINING_RESULT`、`EVALUATION_RESULT`、`ERROR_ANALYSIS_RESULT`、`PREDICTIVE_EXPLANATION_RESULT`、`MODEL_CARD_RESULT`
- Predictive status: `TRAINED`、`TRAINED_WITH_WARNINGS`、`EVALUATED`、`INSUFFICIENT_TEST_SAMPLE`、`NOT_APPLICABLE`
- family Artifact: `CHART_SPECIFICATION`、`PARTITION_INDEX`、`FITTED_PREPROCESSOR`、`FITTED_MODEL`、`PREDICTION`、`PREDICTIVE_EXPLANATION`、`MODEL_CARD`

## 事実：直近の検証

- enum 追加前の `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m compileall -q src tests/product/test_enh_e4_g05_submission_convergence.py` は exit `0`。
- enum 追加前の `git diff --check` は exit `0`。enum 追加後も `git diff --check` は exit `0`。
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e4_g05_submission_convergence.py` は `1 passed`。
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py` は `12 passed`。
- enum 追加後の compile/test と、standard PostgreSQL runner による G05 / G02 / G03 / G04 verification は未実行である。

## 事実：未達の implementation completion conditions

以下は `TODO` または `IN_PROGRESS` であり、`READY_FOR_TEST` の根拠にはならない。

- `IN_PROGRESS`: family 固有 Result / Artifact semantics の lossless canonical representation。現在の `DIAGNOSTICS_RESULT` / `PASS` envelope は family type/status を canonical typed metadata として保持していない。
- `TODO`: enum に対応する `Result` validation、SQLAlchemy ORM check constraint、Product migration。
- `TODO`: Exploratory canonical Result / Artifact read projection、`get_result`、`list_results`、`create_analysis_draft`。
- `TODO`: Predictive canonical execution/stage/result/artifact/lineage read projection。
- `TODO`: Predictive cancel / retry / rerun / revise の canonical lifecycle delegation。
- `TODO`: old Exploratory / Predictive `claim_next()`、`process_execution()`、direct Family ORM persistence を canonical delegate または explicit reject に変更すること。
- `TODO`: Causal / Exploratory / Predictive canonical Golden Path、cross-family authority、old Family table row-count negative、canonical failure no-fallback、mutation、read projection の automated coverage。
- `TODO`: standard PostgreSQL runner による G05 coverage、G02/G03/G04 regression、PostgreSQL contract。
- `TODO`: TD-001 / TD-002 / TD-003 closure evidence、TD-004 inventory。
- `TODO`: fixed implementation commit、template-compliant completion report、enhancement-wide detail ledger update。

## 判断

中断原因は `DESIGN_BLOCKED` でも environment failure でもない。approved architecture は G05 06 が許容する minimal typed extension と Product migration により、family semantics を canonical ownership に収束できる。

したがって、Trial 01 は番号を変えず、現在の未コミット diff を保持したまま次の順序で継続する。

1. Phase A を完了し、family-specific Result / Artifact type、status、schema version、payload、diagnostics を canonical owner で lossless に永続化できるようにする。
2. Phase B / C で Exploratory / Predictive の read projection と lifecycle mutation を canonical repositories / `ExecutionService` へ移す。
3. Phase D で旧 family lifecycle write/claim/process authority を delegate または explicit reject にし、fallback に使えないことを保証する。
4. Phase E で canonical E2E、old-table runtime negative、failure fallback negative、G02/G03/G04 regression を standard PostgreSQL runner で検証する。
5. 全 Implementation Completion Conditions が `DONE` になった後だけ fixed implementation commit、completion report、detail ledger を作成し、`READY_FOR_TEST` として handoff する。

# 指示
`````
# E4-G05 Trial 01 — 06c 中断後再開・Phase A完遂優先指示

E4-G05 Trial 01を現在の未コミットworking treeから継続せよ。

Trial番号は変更しない。

現在の状態は `DESIGN_BLOCKED` でもenvironment failureでもない。既にinventory済みのremaining workは、G05 Trial 01の実装対象として最後まで完遂すること。

## 1. Working Tree

現在保持されているG05の未コミット変更を破棄・巻き戻し・再実装しない。

開始時にactual diffを確認し、現在の各変更を以下へ分類する。

```text
VALID_AND_KEEP
NEEDS_COMPLETION
NEEDS_CORRECTION
UNRELATED_DO_NOT_TOUCH
```

既知のControl Sheet編集、`.nfs` artifact、G05 instruction directory等のunrelated changesには触れない。

---

## 2. 最優先：Phase Aを完全に閉じる

他のread projectionやGolden Pathを先行させる前に、family-specific scientific output semanticsのlossless canonical representationを完成させること。

現在追加済みのenum値は「途中実装」であり、enum追加だけではPhase A完了としない。

### 2.1 Result semantics

Exploratory:

```text
DATA_PROFILE_RESULT
DISTRIBUTION_RESULT
ASSOCIATION_RESULT
GROUP_SUMMARY_RESULT
CHART_RESULT
```

Predictive:

```text
SPLIT_RESULT
TRAINING_RESULT
EVALUATION_RESULT
ERROR_ANALYSIS_RESULT
PREDICTIVE_EXPLANATION_RESULT
MODEL_CARD_RESULT
```

について、少なくとも以下を整合させる。

```text
domain enum
domain validation
serialization/deserialization
ORM mapping
PostgreSQL check constraint
repository round-trip
canonical Result owner
```

### 2.2 ScientificStatus

追加済み:

```text
TRAINED
TRAINED_WITH_WARNINGS
EVALUATED
INSUFFICIENT_TEST_SAMPLE
NOT_APPLICABLE
```

についても同様に:

```text
domain validation
ORM constraint
migration
round-trip test
```

まで完成させる。

既存status semanticsを無理に`PASS`へ圧縮してはならない。

### 2.3 Artifact semantics

追加済み:

```text
CHART_SPECIFICATION
PARTITION_INDEX
FITTED_PREPROCESSOR
FITTED_MODEL
PREDICTION
PREDICTIVE_EXPLANATION
MODEL_CARD
```

について:

```text
artifact_id = semantic identity
ArtifactType = typed scientific/artifact kind
object_key = physical locator
```

というG04 contractを維持する。

### 2.4 Payload preservation

canonicalizationにより以下を失ってはならない。

```text
family result type
scientific status
schema version
payload
diagnostics
warnings
artifact type
relevant metadata
```

現在のような:

```text
DIAGNOSTICS_RESULT
PASS
```

へのgeneric envelopeだけでは、original family semanticsを失う場合は不適合である。

### 2.5 Product migration

enum/check constraint変更に必要なProduct migrationを追加する。

開始head:

```text
20260809_product_0009
```

actual headを再確認し、そのdirect childとする。

root legacy migrationは変更しない。

---

## 3. Phase A completion test

Phase A完了時点で、最低限以下をautomated testで証明する。

```text
Exploratory Result type round-trip
Predictive Result type round-trip
Predictive ScientificStatus round-trip
family ArtifactType round-trip
invalid enum/status rejection
Result level semantics preserved
Execution/Stage ownership preserved
schema version / payload / diagnostics preservation
```

少なくともpersistent constraint/round-tripはstandard PostgreSQL runnerで検証可能なtestとして実装する。

Phase Aが完了する前に、generic fallback valueを利用したままPhase B/Cを完成扱いしてはならない。

---

## 4. Phase B — Exploratory convergence

Phase A完了後、Exploratoryのnew canonical dataについて:

```text
get execution
list execution
get result
list results
artifact projection
create_analysis_draft
その他existing supported read surface
```

をcanonical repositoriesからprojectionする。

historical Family ORM readが必要な場合はread-only compatibilityとして明示的に分離する。

new canonical executionのauthorityとしてFamily ORMを参照してはならない。

---

## 5. Phase C — Predictive convergence

Predictiveについて:

```text
execution
stage
result
artifact
current lineage-facing projection
```

のreadをcanonical repositoriesへ移す。

さらにactual exposed:

```text
cancel
retry
rerun
revise
```

をcanonical lifecycleへdelegateする。

G06 lineage final consolidationは行わない。

---

## 6. Phase D — old authority shutdown

Exploratory / Predictiveのold:

```text
claim_next()
process_execution()
direct Family ORM writes
family lifecycle mutation
```

をProduct write authorityとして使用不能にする。

sourceを残す場合は:

```text
canonical delegate
```

または:

```text
explicit reject
```

のどちらか。

canonical failure時にold authorityへfallbackする経路を残してはならない。

---

## 7. Phase E — mandatory verification

以下をautomated coverageとして全て完成させる。

```text
Causal canonical Golden Path
Exploratory canonical Golden Path
Predictive canonical Golden Path

cross-family common claim authority

canonical Result/Artifact owner for all families

old FamilyExecution row-count negative
old FamilyStageExecution row-count negative
old FamilyResult row-count negative
old FamilyArtifact row-count negative

canonical failure -> no old-authority fallback

Exploratory/Predictive mutation delegation

Exploratory/Predictive canonical read projection

G02 regression
G03 regression
G04 regression
PostgreSQL contract
```

real PostgreSQL verificationには必ず:

```bash
scripts/test/run_product_postgres_tests.sh ...
```

を使用する。

途中でtest failureを発見した場合、正しいtestかつenvironment正常ならproduction defectとして修正し、続行する。

---

## 8. Existing E3 tests

old Family lifecycleをauthorityとして期待するE3 testが失敗しても、それだけで停止しない。

次のいずれかに分類する。

```text
PRESERVE
    passed architecture contractを検証している

REPLACE
    G05で廃止されるold authorityを正としている

REMOVE_ONLY_IF_REDUNDANT
    canonical testで同等以上のcoverageが明示的に存在する
```

old testを削除してcoverage holeを作らない。

---

## 9. Completion-condition management

G05 06のImplementation Completion Conditionsを全件チェックリスト化する。

状態:

```text
TODO
IN_PROGRESS
DONE
DESIGN_BLOCKED
```

`TODO` または `IN_PROGRESS` が一件でも残る間は作業を継続する。

途中報告を行ってもよいが、途中報告をturn終了条件としてはならない。

---

## 10. Transition Debt

verification完了後のみ:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
```

をevidence付きで記録する。

TD-004はG06 handoff用にactual remaining structural generic lineage duplicate writerをinventoryする。

存在しない場合:

```text
NONE observed
```

と記録する。

G06 implementationには進まない。

---

## 11. Fixed Commit and Reports

全production/test/migration workとrequired verificationが完了した後にfixed implementation commitを作成する。

そのfixed SHAに対して最終verificationを行う。

その後のみ:

```text
20_implementation_reports/G05/
E4-G05_01_implementation_completion_report.md
```

をrepository templateへfield-by-field準拠して作成する。

さらに:

```text
20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

を更新する。

required fieldを省略・merge・短縮してはならない。

---

## 12. Allowed Stop Conditions

turnを終了してよいのは原則以下のみ。

### READY_FOR_TEST

```text
全Implementation Completion Conditions = DONE
required PostgreSQL verification = PASS
G02/G03/G04 regression = PASS
TD-001/002/003 closure evidence complete
TD-004 inventory complete
fixed implementation commit complete
completion report template-compliant
detail ledger updated
```

の場合。

### DESIGN_BLOCKED

approved ENH-E4 architectureとactual repository semanticsに、minimal typed extension / Product migrationでは解消不能なcontradictionが存在する場合のみ。

その場合は必ず:

```text
exact contradiction
actual source/schema facts
why current permitted extension cannot solve it
required new human decision
```

を示す。

以下は停止理由として認めない。

```text
migrationが必要
enum/constraint追加が必要
read projectionがまだ多い
既存E3 testが旧architecture依存
production defectを新たに発見
testが途中でFAIL
PostgreSQL検証未実施
report未作成
commit未作成
```

E4-G05 Trial 01をREADY_FOR_TESTまたは真正のDESIGN_BLOCKEDまで完遂せよ。
`````