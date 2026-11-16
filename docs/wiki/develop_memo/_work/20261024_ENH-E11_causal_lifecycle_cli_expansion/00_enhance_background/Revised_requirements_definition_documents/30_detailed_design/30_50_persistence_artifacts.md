# 30_50_persistence_artifacts

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 20. Persistence / transaction / idempotency

### 20.1 Persistence rule

Project Management / Analysis Workspace分離やStage presentation再編に伴う新DB migrationを要求しない。

current persistent entitiesとrelationをauthorityとする。

- Project
- Research Context Version
- Dataset / Dataset Version
- Analysis View
- Analysis Specification
- Execution / StageExecution / StageAttempt
- Result
- Artifact
- Lineage
- Annotation
- Workspace Selection等のselection state

Navigation state / Analysis Context composite / presentation grouping / current Stage presentation stateを新しいpersistent aggregateにしない。

### 20.2 Transaction boundary

Application commandはUnit of Workでdomain mutationとpersistenceを一貫させる。external scientific executionはtransactionを不必要に長時間保持しない。

### 20.3 Command idempotency

Idempotency keyを全POSTへ一律要求せず、duplicate durable side effectを作り得るcommandを対象とする。

logical scope:

```text
(project_id, command_scope, idempotency_key)
```

behavior:

```text
same scope/key + same semantic request
  → stored result/response replay
  → duplicate side effectなし

same scope/key + different semantic request
  → conflict
```

path上のsemantic resource IDもrequest hash inputへ含める。

browser route/history/presentation stateはidempotent command hashのsemantic inputに含めない。

### 20.4 Artifact materialization

retryでduplicate artifactを生成しない。Artifactのcontent identity / lineage / idempotency contractを用いてsingle durable outcomeへ収束させる。

---

## 6. `StoredArtifact` / `ArtifactStorePort`

**Responsibility:** Existing Product Artifact Port; exact semantics of `store/retrieve/exists/delete` are API obligations, not proof of E11 atomic multi-file delivery.

| Symbol | Fields / Signature |
|---|---|
| `StoredArtifact` frozen dataclass | `object_key: str`, `content_hash: str`, `size_bytes: int`, `media_type: str` |
| `ArtifactStorePort.store` | `(source_path: Path, object_key: str, media_type: str="application/octet-stream") -> StoredArtifact` |
| `ArtifactStorePort.retrieve` | `(object_key: str, dest_path: Path) -> None` |
| `ArtifactStorePort.exists` | `(object_key: str) -> bool` |
| `ArtifactStorePort.delete` | `(object_key: str) -> None` |

**E11 gap:** Local staging, atomic set commit, relative path sanitation and private CATE export constraints require separate reviewed design; existing Port alone does not guarantee these.
