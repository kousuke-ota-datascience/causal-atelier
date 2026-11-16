# 10_20_nfr_reproducibility

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## NFR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001a | 再現性 | current snapshot、code/runtime metadata、seed、schema identity等の再現性情報を保持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-001b | 再現性 | actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-002 | 追跡可能性 | canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-003 | 決定性 | Canonical JSONとhash生成はfield順やprocessに依存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-013 | Schema evolution | schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-016 | Scientific transparency | 仮定、warning、negative result、limitationを省略せず表示する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-019 | Documentation | `00/10/21/22/23/30`だけでcurrent product concept / requirement / logical model / design / interface contractを自己完結して理解できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
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
