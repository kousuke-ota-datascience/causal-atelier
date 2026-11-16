# 30_50_persistence_artifacts


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

### 20.5. `StoredArtifact` — Product DTO（EXISTING / Owner 7区分）

#### 20.5.1. 識別情報・責務
`ariadne.product.ports.artifact_store.StoredArtifact`、`src/ariadne/product/ports/artifact_store.py` blob `e5bb990f9b69ef68df46a1559560ffb67b64caaf`。単一Artifactの物理Key、bytes digest、size、media typeを保持する。E11 multi-file transactionと科学的Artifact lineageの責任を持たない。

#### 20.5.2. フィールド
| Field | Python type | Default / mutability | Source constraints |
| --- | --- | --- | --- |
| `object_key` | `str` | required / frozen | このDTO自体の安全なrelative path検証はSourceにない |
| `content_hash` | `str` | required / frozen | このDTOはSHA256検証を実装しない |
| `size_bytes` | `int` | required / frozen | サイズの正値検査はAdapter責務 |
| `media_type` | `str` | required / frozen | MediaType検証はAdapter責務 |

#### 20.5.3. Constructor / Factory
`@dataclass(frozen=True)`が生成する`__init__(object_key: str, content_hash: str, size_bytes: int, media_type: str)`。**N/A:** 明示Factory／追加`__post_init__`は現行Sourceにない。Nested mutable objectは持たない。

#### 20.5.4. メソッド
Sourceにはユーザー定義の業務メソッドがない（**N/A**）。Dataclass標準の生成メソッドのみ。

#### 20.5.5. 処理仕様
入力4 Fieldを構築時に保存する。frozenによってField再代入は拒否されるが、`content_hash`と実ファイル内容の一致、Key閉じ込め、size bytes一致、情報機密区分はこのDTOの成立条件で**自動的に検証されない**。安全性は呼出元AdapterとContract Testの責務とする。

#### 20.5.6. I/O・連携・失敗処理
`ArtifactStorePort.store`の戻り値。**N/A:** DTO自体にFS/DB/HTTP／Transaction/Retry/Rollbackなし。Source固有の例外はなし（生成標準エラーを除く）。E11 Local `ArtifactDescriptor`と同型・同権威には扱わない。

#### 20.5.7. 検証
DTO構築／値保持／frozen属性、誤ったHashでも自動検査しないことをUnit確認。Adapter側ではreal bytes/hash/size/media、安全なRootをContract/Negative Testで検証する。ProductのNFR-020a/FR Artifact境界、E11 BD01-F03/F04との非同一性を照合。テスト実行**NOT_RUN**。

### 20.6. `ArtifactStorePort` — Product Protocol（EXISTING / Owner 7区分）

#### 20.6.1. 識別情報・責務
`ariadne.product.ports.artifact_store.ArtifactStorePort`、同Source blob `e5bb990f9b69ef68df46a1559560ffb67b64caaf`。Productの単体Artifact storage interfaceを提供する`Protocol`。local multi-file atomic visibility、commit marker、privacy releaseを保証しない。

#### 20.6.2. フィールド
**N/A理由：** Protocol Sourceにはproperty/instance fieldの宣言がない。実AdapterのRoot/connection/fsync stateは各Adapter実装で定義する。Product persistent Artifact metaをこのPortへ暗黙に保持させない。

#### 20.6.3. Constructor / Factory
**N/A理由：** Protocolは実体Instance生成のFactoryを持たない。具象Adapterのconstructorをこの契約から捏造しない。

#### 20.6.4. メソッド
| Method signature | Return | Observable obligation / failure |
| --- | --- | --- |
| `store(source_path: Path, object_key: str, media_type: str="application/octet-stream") -> StoredArtifact` | DTO | one artifactを保存、hash/size等はDTOで報告。完全性・atomic rename等はAdapterごとに要検証 |
| `retrieve(object_key: str, dest_path: Path) -> None` | None | targetに取得。existing path conflictとno-clobberはPort Sourceに規定なし |
| `exists(object_key: str) -> bool` | bool | key存在判定。TOCTOU排除の保証はない |
| `delete(object_key: str) -> None` | None | 指定key削除。論理認可/削除可否は別Domain責務 |

#### 20.6.5. 処理仕様
CallerはProductのApplication Service等。Key identity、Project boundary、source file bytes/hashの正しさと、error時の処置は具体Adapter／Application Contractで保証する。Source Protocolのsignatureだけから`exactly once`、transaction rollback、atomic multi-file bundleは導けない。

#### 20.6.6. I/O・連携・失敗処理
**I/O:** External Storage Adapterが実行する。**Transaction:** Port自体はUoWやDBのTransaction scopeを持たない。**Failure/Retry:** `Protocol`に例外Class、retry/backoff、rollbackは宣言されていないため**NOT_SPECIFIED**。E11の`LocalPublicationPort`に必要なMarker/Manifest、no-clobber、secure pathは別Spec（30_62）に定義する。

#### 20.6.7. 検証
Signature Contractと各Adapterのstored hash/readback／missing key／invalid key／permission、no silent overwrite、Product E9/E10 regression、NFR-020a。未提供のmulti-file guaranteeは`N/A`ではなく**別新Portの必須検証**。テスト実行**NOT_RUN**。

### 20.7. Persistence & Artifact requirement trace

- `NFR-007`（DEFERRED）：Metadata transactionとArtifact writeのcross-store failure compensationを定義する。
- `NFR-020a`：Artifact storageを`ArtifactStore` Port abstraction越しに利用する。
