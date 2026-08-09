# E4-G05 Trial 01 — Phase A Completion Instruction

E4-G05 Trial 01を継続せよ。

Baseline checkpoint:

```text
0bc9ce5f3ea66f862f088c2246082aedfd0d83e4
```

Trial番号は変更しない。

今回は **Phase Aのみを完了すること**。Phase B / C / D / Eには進まないこと。

---

## 1. 開始時確認

最初に以下を実行し、actual repository stateを確認すること。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -5 --oneline
git diff HEAD
```

Baseline `0bc9ce5f3ea66f862f088c2246082aedfd0d83e4` 以降に変更がある場合は、その内容を確認してから継続する。

既にPhase Aで実装済みの変更を巻き戻したり、ゼロから再実装したりしない。

---

## 2. 今回の唯一の目的

family-specific Result / Artifact semanticsを、G04で成立したcanonical Result / Artifact ownership contract上で **losslessに永続化可能な状態まで完成させる**。

Phase Aの完了は、enumを追加したことではなく、

```text
Domain
→ Validation
→ ORM
→ Product migration
→ Repository persistence
→ PostgreSQL round-trip
```

が一貫して成立したことを意味する。

---

## 3. 完成させるResult semantics

Exploratory Result:

```text
DATA_PROFILE_RESULT
DISTRIBUTION_RESULT
ASSOCIATION_RESULT
GROUP_SUMMARY_RESULT
CHART_RESULT
```

Predictive Result:

```text
SPLIT_RESULT
TRAINING_RESULT
EVALUATION_RESULT
ERROR_ANALYSIS_RESULT
PREDICTIVE_EXPLANATION_RESULT
MODEL_CARD_RESULT
```

について、以下を全て完成させる。

```text
ResultType enum
domain validation
serialization / deserialization
ORM check constraint
Product migration constraint
canonical Result writer
repository load / round-trip
```

`DIAGNOSTICS_RESULT` へのgeneric fallbackによってfamily-specific result typeを失ってはならない。

---

## 4. 完成させるScientificStatus

少なくとも現在追加済みの:

```text
TRAINED
TRAINED_WITH_WARNINGS
EVALUATED
INSUFFICIENT_TEST_SAMPLE
NOT_APPLICABLE
```

について、

```text
domain validation
Result type/status compatibility
ORM constraint
Product migration
repository round-trip
```

を整合させる。

family固有statusを単に `PASS` へ圧縮してはならない。

---

## 5. 完成させるArtifact semantics

少なくとも現在追加済みの:

```text
CHART_SPECIFICATION
PARTITION_INDEX
FITTED_PREPROCESSOR
FITTED_MODEL
PREDICTION
PREDICTIVE_EXPLANATION
MODEL_CARD
```

について、

```text
ArtifactType enum
domain validation
ORM constraint where applicable
Product migration constraint where applicable
canonical Artifact writer
repository round-trip
```

を完成させる。

G04 contract:

```text
artifact_id   = semantic Product identity
object_key    = physical locator
content_hash  = integrity evidence
```

を維持する。

---

## 6. Lossless canonical representation

canonical Result / Artifact persistenceで以下を失ってはならない。

```text
family-specific result type
scientific status
schema_version
payload
diagnostics
warnings
artifact type
artifact metadata
Execution ownership
StageExecution ownership
Result ↔ Artifact association
```

特に、現在未完成とされている以下を閉じること。

```text
Result ↔ Artifact association preservation
schema_version preservation
family-specific result/status typed persistence
```

original family output semanticsをgeneric envelopeへ押し込んで情報を失う実装は修正すること。

---

## 7. Product migration

現在のcheckpointには:

```text
20260809_product_0010
down_revision = 20260809_product_0009
```

が含まれている。

このmigrationをactual domain / ORM constraintsと一致させる。

以下3層が同じallowed set / compatibility ruleを表すこと。

```text
Domain validation
SQLAlchemy ORM constraint
PostgreSQL migration constraint
```

不一致があれば修正する。

新しいrevisionを追加する必要がなければ `0010` 自体を完成させる。

既にpush済みcheckpoint後のmigration revisionを書き換えることがrepository運用上不適切な場合は、`0010` のdirect childとしてcorrective Product migrationを追加する。

root legacy migrationは変更しない。

---

## 8. Mandatory automated tests

Phase A専用testを追加・完成させ、最低限以下を証明する。

### Result

```text
Exploratory ResultType PostgreSQL round-trip
Predictive ResultType PostgreSQL round-trip
Predictive ScientificStatus PostgreSQL round-trip
schema_version preservation
payload preservation
diagnostics preservation
warnings preservation
Result level preservation
StageExecution ownership preservation
```

### Artifact

```text
family ArtifactType PostgreSQL round-trip
artifact_id preservation
object_key preservation
Result association preservation
StageExecution association preservation
metadata preservation
```

### Negative

```text
invalid ResultType rejected
invalid ScientificStatus rejected
invalid ResultType / ScientificStatus combination rejected
invalid ArtifactType rejected where constrained
cross-execution ownership remains rejected
```

---

## 9. Constraint equivalence test

Domain / ORM / migration constraint driftを再発させないため、automated testまたは明示的contract testで少なくとも以下を検証すること。

```text
Domain allowed ResultTypes
==
ORM allowed ResultTypes
==
PostgreSQL migration allowed ResultTypes
```

同様にScientificStatus / ArtifactTypeについて必要な範囲で整合を検証する。

文字列の重複実装が避けられない場合でも、driftを検出できるtestを持つこと。

---

## 10. PostgreSQL verification

Phase A completionにはreal PostgreSQL evidenceを必須とする。

唯一のentry point:

```bash
scripts/test/run_product_postgres_tests.sh <actual-test-path-or-node> [...]
```

manual Docker / DSN / psql / Alembic workaroundは禁止。

少なくとも:

```text
Product migration upgrade head
Phase A Result round-trip
Phase A Artifact round-trip
constraint negative tests
relevant G04 Result/Artifact regression
PostgreSQL contract
```

を実行する。

test failureがcorrect testによるproduction defectであれば修正して再実行する。

---

## 11. Phase A completion criteria

以下が全て `DONE` になるまで停止しない。

```text
[ ] family ResultType canonical persistence complete
[ ] ScientificStatus canonical persistence complete
[ ] family ArtifactType canonical persistence complete
[ ] Result type/status compatibility complete
[ ] domain validation complete
[ ] ORM constraints complete
[ ] Product migration complete
[ ] schema_version preservation complete
[ ] payload/diagnostics/warnings preservation complete
[ ] Result ↔ Artifact association preservation complete
[ ] repository serialization/deserialization complete
[ ] PostgreSQL Result round-trip PASS
[ ] PostgreSQL Artifact round-trip PASS
[ ] invalid constraint negatives PASS
[ ] G04 relevant regression PASS
[ ] PostgreSQL contract PASS
[ ] git diff --check PASS
```

---

## 12. Phase A checkpoint commit

上記が全て完了したら、Phase A checkpoint commitを作成する。

例:

```text
E4-G05 Trial 01 Phase A complete
```

このcommitはG05 final implementation commitではない。

commit前に:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

を確認する。

commit後に:

```bash
git rev-parse HEAD
git status --short
```

を確認する。

Phase Aに無関係な変更をcommitへ混入させない。

---

## 13. 今回作成しないもの

今回はまだ以下を作成しない。

```text
E4-G05_01_implementation_completion_report.md
G05 final implementation commit
READY_FOR_TEST declaration
TD-001/002/003 closure declaration
Gate Decision
```

これらはPhase B〜E完了後に作成する。

---

## 14. 今回進めないもの

Phase A完了後も、このrunでは以下へ進まない。

```text
Phase B Exploratory read convergence
Phase C Predictive read/mutation convergence
Phase D old authority shutdown
Phase E Golden Path / final regression
G06 lineage work
```

Phase A checkpointを作成したところで停止する。

---

## 15. Allowed stop conditions

今回turnを終了してよいのは以下のみ。

### PHASE_A_COMPLETE

以下を全て満たした場合。

```text
Phase A completion criteria all DONE
standard PostgreSQL verification PASS
Phase A checkpoint commit created
```

その場合、最後に:

```text
PHASE_A_COMPLETE
Checkpoint SHA: <full SHA>
```

を報告して停止する。

### DESIGN_BLOCKED

approved G02/G03/G04/G05 architectureとactual family semanticsの間に、minimal typed extension / Product migrationでは解消不能なsemantic contradictionがある場合のみ。

その場合は:

```text
exact contradiction
actual source/schema evidence
why permitted implementation choices cannot resolve it
required human architecture decision
```

を示す。

---

## 16. 停止理由として認めないもの

以下を理由に途中停止してはならない。

```text
まだtestを書いていない
PostgreSQL runnerをまだ実行していない
migration修正が必要
constraint mismatchを発見した
repository writer修正が必要
testがFAILした
追加production defectを発見した
Phase B以降がまだ残っている
G05全体がまだ未完了
```

今回はG05全体ではなく **Phase Aを閉じることだけが目的**である。

E4-G05 Trial 01 Phase Aを `PHASE_A_COMPLETE` まで完遂せよ。
