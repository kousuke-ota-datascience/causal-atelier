# 10_20_nfr_reproducibility


---

## NFR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001a | 再現性 | current snapshot、code/runtime metadata、seed、schema identity等の再現性情報を保持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-001b | 再現性 | 解析結果を再現するため実効ライブラリ版・乱数条件を取得できる | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-002 | 追跡可能性 | 研究条件から入力・計画・実行・結果・成果物までの追跡が可能である | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-003 | 決定性 | 同一内容から環境に依存しない同一性識別値を生成できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-013 | Schema evolution | 変化するデータ契約を識別し後方互換を制御できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-016 | Scientific transparency | 仮定、warning、negative result、limitationを省略せず表示する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-019 | Documentation | 現行Productの要件・データ・設計・Interface契約を整合した正式資料で追跡・理解できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-029 | Reproducibility | ローカル分析の入力・実行条件・実効Backend／Library版・乱数／分割条件・出力の同一性と来歴を第三者が検証できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-033 | Environment Reproducibility | 採用された科学Methodを再現可能な依存関係と検証済み実行Profileで導入・実行でき、導入前後の互換性を確認できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |

## 7.2. Canonical Lineage / Reproducibility / Retry Safety

Canonical lineage read modelは最低限次を接続する。

```text
ResearchContextVersion
  ↓
AnalysisSpecification
  ↓
ExecutionPlan
  ↓
Execution
  ↓
StageExecution
  ↓
Result
  ↓
Artifact
```

加えて`DatasetVersion / AnalysisView / GraphVersion / input Result / base Execution`を接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric `LineageEdge`へ重複persistしない。`MOTIVATED`等のsemantic relationだけをgeneric LineageEdgeで保持する。

Current contractでは`StageAttempt.effective_random_seed: int | null`を追加し、stochastic Stageのactual seedをattempt単位で保存する。同一logical Stageのretryは同じseedを再利用し、deterministic Stageは`null`とする。

`runtime_version_json`は最低限`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保持する。これはbit-for-bit numerical identity保証ではなくenvironment再構築情報である。

Idempotencyはduplicate durable side effectを生成し得るCommandに適用し、scopeを`(project_id, command_scope, idempotency_key)`とする。exactly-once executionは保証しないが、retryで同一successful Stage outputのdurable Artifactを重複materializeしてはならない。
