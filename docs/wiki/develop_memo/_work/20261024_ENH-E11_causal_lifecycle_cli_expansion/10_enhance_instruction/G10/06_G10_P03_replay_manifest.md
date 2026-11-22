# ENH-E11 G10 P03 — replay_manifest

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G10 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G10_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G10_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** JCS semantic hash/Graph self hash/ContentRef bytes/Manifest marker bytes別値、readback/atomic no-clobber。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 41 Method/10 UCの有効独立科学証拠を全件照合し、影響分のみ再実行してManifest/依存/旧v2互換を統合する。

**科学/Designの必須制約:** 各GateのScience999を省略しない。GPLの顧客配布時の手動License審査は内部分析Gate外。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** JCS semantic hash/Graph self hash/ContentRef bytes/Manifest marker bytes別値、readback/atomic no-clobber。

### 2A. 41 Method横断Reuseと既存ABIの実在確認（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter`は`run_discovery(DiscoveryInput, Path)`、`run_identification(IdentificationInput, Path)`、`run_estimation(EstimationInput, Path)`、`run_refutation(RefutationInput, Path)`、`run_sensitivity(SensitivityInput, Path)`の公開ABI（返値はいずれも`list[ScientificResultDescriptor]`）。対応実体は`scientific/discovery|identification|inference|refutation|sensitivity/adapter.py`の各`run(input_, output_dir)`。これらは旧Product Path APIであり、E11の`Discovery/Identification/Estimator/DiagnosticPort`のtyped Request/Outcomeとは互換性を自動仮定しない。
- **横断責務:** G10は41 Method×Operation/Estimand/Backend/Result/Manifestの科学証拠を全件検証し、影響閉包内の変更/不明分だけ再実行して統合検証を所有するが、科学計算Kernel、G01 Registry、GraphVersion writer、Publisher、Reader、G05 local executor Study-only row eligibilityを複製しない。旧ABI・Product v2を変更せず、既存upstream Gateの同一Class・Method profileを参照する。Sourceに存在しないE11新規Classを「導入済み」と呼ばない。
- **科学的Boundary:** G10の横断テストには全41 MethodのDGP/NEG/独立REF、実効Backend/lock/fixture SHA、Source/Environment/seed、preregistered K/R/MC-SE/coverage/threshold、FWER=.05とMethod別Inference profileが必要。未決は該当MethodのBLOCKED、G10全体のGate PASS禁止。

### 2B. Standalone Operation/Result/Manifest契約
| Operation | 必須Artifact | 禁止・Negative |
|---|---|---|
| DISCOVER | `study.json`・`status.json`・Graph成功なら`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`と理由必須、`schema_dispatch.graph=null`。Backend失敗との混同禁止 |
| IDENTIFY | `study.json`・`status.json`・`identification.json` | Effect `result.json`禁止。非識別もtypedでGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`・`status.json`・`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、科学PASSと混同禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`・`status.json`・`diagnostics.json` | Effectの再発行禁止、元Effect/Graph/Design hash、seed/適用条件の照合 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）、ただし両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key、実bytes SHA256/size/MediaType/Privacyを網羅。 `request_hash=SHA256(JCS(validated typed Study JSON))`。Manifestに自己hashを格納せず、Markerの`manifest_sha256`にManifest実bytes hashを保存。ReaderはMarker→Manifest→実File→Operation/Profile→上流hashをTrustedRootで検証し、一致しない未コミット/破損データを拒否。Outputは既存G01のStaging→同一FS atomic no-clobber publish、個票bytesはG05のStudy単独opt-in（`row_export_requested=true`）/OS適格性確認以前に生成禁止。各Methodのpoint/uncertainty/science_acceptance/statusを別軸で保持し、計算成功はScience PASSでない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | Port/Value/Facade integration (no duplicate implementation) | to_canonical_bytes() |
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | Port/Value/Facade integration (no duplicate implementation) | begin(self)->StagingArtifactSink; stage_bytes(self,key:RelativeArtifactKey,data:bytes,media_type:str,classification:PrivacyClass)->ArtifactDescriptor; validate(self,manifest:LocalRunManifest)->ValidatedBundle; commit(self,validated:ValidatedBundle)->CommittedRunRef; abort(self,reason:str)->None |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) |
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence.GraphEvidence` | Port/Value/Facade integration (no duplicate implementation) | from_canonical_json(raw:bytes) / canonical_payload() |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降に埋め込んだClass Field/Constructor/Public Methodが実装の一次規範。外部DDは履歴/Provenanceのみであり、unknown Concrete型/Backend/Runtime値を補完しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent source)

以下のInstance Fields/Constructor/Method/Failureは本Packageの規範。外部DD参照はProvenanceのみ。Designed Classが実在する証拠ではないのでSource/ABIを実行時検証する。

### 3.1. `LocalRunManifest` — complete Class method protocol

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`、immutable typed DTO。
- **責務:** 1 Local runのidentity、lineage、Method/Science/Runtime、artifact inventoryをversioned schemaで保持し、canonical bytesのauthorityを定義する。
- **責務外:** file open、hash verificationのI/O、実効科学計算、Local OS permission enforcement。
- **参照:** IF `23_42` §6、`23_41` §5。Existing Product CliManifestとは別schema。

#### フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| `manifest_version` | `Literal["e11-local-manifest/1"]` | Schema | mandatory, no v2 fallback |
| `run_id, operation, request_hash` | `str, LocalOperation, str` | validated Study | fixed identity, digest hex64 |
| `lineage` | typed refs + hashes | Question/Design/Graph/Dataset/Identification | graph/estimand/adapter provenance lossless |
| `execution_status` | typed technical + scientific axes | LocalRunOutcome | actual facts, independent science not faked |
| `runtime` | `RuntimeEvidence` | effective probe | Python/backend/lock/seed/fold/BLAS explicit |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | Publisher stage validation | relative keys, size, hash, media, privacy |
| `review` | science evidence refs; customer legal delivery state is outside local Manifest | SCI + policy | absent proof remains null / NOT_EVALUATED |

この表は論理的なField groupingであり、wireの厳格なversion/Schema検証は23_42に従う。

#### Constructor / Factory

- **Factory:** `from_payload(payload: Mapping[str, JsonValue]) -> LocalRunManifest`、`from_run_evidence(evidence: ValidatedRunEvidence) -> LocalRunManifest`。
- **Precondition:** strict schema/version + no unknown critical keys; content hash references are normalized; `Manifest` must **not** include its own bytes hash; marker is outside Artifact list. Factories do not read the filesystem.
- **N/A:** runtime backend import is not part of this DTO. Factoryはstrict Schema違反を型付きErrorとして返す。

#### メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `validate_invariants(self) -> tuple[Reason,...]` | typed reasons | pure; reject broken cross-refs, privacy and science axis inconsistency |
| `to_canonical_bytes(self) -> bytes` | canonical versioned JSON bytes | pure deterministic encoding; reject NaN/Infinity/raw credentials |
| `from_payload(payload) -> LocalRunManifest` | immutable DTO | pure strict decode; unsupported version rejected |

#### 処理仕様

1. Normalize schema version and all typed scientific statuses without collapsing negative outcomes.
2. Validate artifact keys unique and safe relative; no absolute input path/secret/row data in Manifest.
3. Validate lineage digest/target and effective runtime evidence with missing values distinguished from fabricated defaults.
4. Produce canonical bytes deterministically, independent of map insertion order or local time display. Result identity is a logical run identity, **not** evidence of successful file publication.

#### I/O・連携・失敗処理

- `LocalArtifactPublisher` creates Manifest bytes; Reader consumes those same canonical bytes. Marker stores SHA256 of Manifest bytes, not a self-reference.
- **I/O:** N/A in DTO; byte serialization is pure. Actual file I/O/permission, partial bundle, crash and retry belong to Publisher/Reader.
- **Failure:** `SCHEMA_INVALID`, `VERSION_UNSUPPORTED`, `HASH_INVALID`, `PRIVACY_POLICY_CONFLICT`; no automatic v2 upgrade.

#### 検証

`DD-E11-MAN01` canonical bytes roundtrip; `MAN02` unknown version/unknown critical; `MAN03` marker outside artifact list; `MAN04` science negative vs technical outcome independent; `MAN05` absolute path/raw secret/row data rejection; `MAN06` legacy v2 readback isolation。関連要件：FR-201/202/203、NFR-029/030/032、AR-040、BD01-F06/F07/F12。

### 3.2. `LocalArtifactPublisher` — complete Class method protocol

#### 識別情報・責務

- **Module / Class:** `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher`
- **責務:** 同一local filesystem上の複数Artifactをrun単位で検証・原子的に公開し、readback成功を確認する。Local File Bundleのpublication authorityでありProductの`ArtifactStorePort`ではない。
- **責務外:** Scientific Estimator、HTTP/DB、顧客配布Legal、外部FSのcross-device atomicity。
- **関連設計:** 23_42 §2/6/7。Product ArtifactStorePortは別のauthorityである。

#### フィールド

| Field | Type | 生成元 | 可変性・制約 |
| --- | --- | --- | --- |
| `root` | `TrustedLocalRoot` | OS検証済みdirfd Capability | Immutable root handle。所有者・owner-only mode・local ext4/XFS/同一FSを検証し、commit時にもFD/owner/modeを確認 |
| `run_id` | `str` | 正規化済LocalStudySpec | Immutable。23_42のsafe grammar |
| `request_hash` | `str` | canonical LocalStudySpec bytes | Immutable。小文字SHA256 hex64 |
| `state` | `PublishState` | FactoryでPREPARING | PREPARING→STAGING→VALIDATING→PUBLISHING→COMMITTED/INDETERMINATE、公開前のみABORTED |
| `staging_handle` | `StagingHandle|None` | begin | State依存。Trusted FS descriptorを閉鎖管理 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | stage_bytes | Commitまで追加、公開後immutable |
| `permission_policy` | `LocalPrivacyPolicy` | 注入Policy | Resultのrelease policyと一致を要求 |

#### Constructor / Factory

- **Constructor:** `__init__(self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`。rootはOS/owner/mode/FS/dirfdを検証済みのCapability（任意Pathではない）。random staging tokenは`begin`時に生成する。実装時にRootの変更をcommit境界まで検出する。
- **前提:** `run_id`にseparator/「.」「..」を含まない、request hashはcanonical versionと一致。Trusted Root所有者／同一FS／OS principalの確認に失敗したらstaging生成しない。

#### メソッド

| Signature | Return | 責務・副作用 | Failure / retry |
| --- | --- | --- | --- |
| `begin(self) -> StagingArtifactSink` | staging sink | 0700 staging dir作成、state遷移 | 重複begin/権限不一致拒否。未公開ならabort可 |
| `stage_bytes(self, key: RelativeArtifactKey, data: bytes, media_type: str, classification: PrivacyClass) -> ArtifactDescriptor` | descriptor | dirfd相当のroot閉じ込めで0600 file作成/追加 | traversal/symlink/サイズ/重複key拒否 |
| `validate(self, manifest: LocalRunManifest) -> ValidatedBundle` | readback済み候補 | 各Artifact→Manifest→markerのhash/Schema/Privacy検証 | missing/hash mismatch/個票漏洩ならfail-closed |
| `commit(self, validated: ValidatedBundle) -> CommittedRunRef` | published run ref | PUBLISHING状態でno-clobber rename、親dir fsync、独立Reader readbackを終えた場合にだけCOMMITTED | rename実施後の失敗・判定不能はINDETERMINATE。既存runは削除・上書きしない |
| `abort(self, reason: str) -> None` | None | 未公開stagingを隔離しHandle解放 | rename後は既公開の可能性があるため破壊的abort禁止 |

#### 処理仕様（Preconditions／状態／Postconditions）

1. `PREPARING`でroot/safe run ID・output policy・同一FSを検査する。
2. `begin`で`root/.staging/{random-token}`を0700作成。Path文字列チェックだけでなく、全componentをtrusted dirfd下に開くか同等のanti-symlink手法を適用。
3. `STAGING`でArtifactを0600でcreate。全bytesのhash/size/schema/Parquet列/Privacyを検証し、同じkeyの二重書込を拒否。
4. `VALIDATING`でManifestを作り、Artifactリストを走査。Manifest自体のhashを外側の`_COMMITTED.json`へ格納し、Readerと同一アルゴリズムでstagingをreadbackする。File・Directoryをfsync。
5. `commit`は`runs/{run_id}`未存在を**非原子的exists判定に依存せず**保証するLinux `renameat2(RENAME_NOREPLACE)`（同mount/FSの実効対応を確認）を要求。Process lock、排他FS lockのみ、check-then-rename、通常の`Path.rename()`は代替として**禁止**。未対応FSはfail-closed。
6. 同一FSで一括公開後、親directory fsyncと公開版の完全readbackが成功して初めて`COMMITTED`。再試行は既存runのrequest hash一致かつ全readback PASSのときのみ同じrefを返す。
7. Renameの成否が不明、またはRename後のfsync/readbackで異常がある場合は`PublishState=INDETERMINATE`（error `PUBLICATION_INDETERMINATE`）を返し、`COMMITTED`と断定しない。後続の再照合はReaderによる全検査が前提で、既存runを削除・上書きしない。異なるrequest hashは`RUN_ID_CONFLICT`。科学計算のexactly-onceは保証しない。

**Postconditions:** `COMMITTED`ではMarker→Manifest→全Artifactが検証可能、output runはimmutable。失敗時に誤った部分成果物を「成功」へ昇格させない。External store/NFS/cross-deviceは同等のatomicityを自動主張しない。

#### I/O・連携・失敗処理

- **Caller:** LocalCausalUseCase。`StagingArtifactSink`はScientific Adapterにのみ渡し、final `runs` pathを渡さない。
- **Artifact schema:** 23_42のResult、Graph、Parquet、Manifest、commit marker。それぞれrelative POSIX key＋media_type＋size＋SHA256＋Privacy class。
- **Transaction:** local same-FS staging → validate → no-clobber directory publication → durable parent sync → readback。DB UoWやProduct ArtifactStoreのtransactionとは無関係。
- **Failure classes（意味）:** Invalid path、Permission、HASH_MISMATCH、SCHEMA_INVALID、RUN_ID_CONFLICT、NON_ATOMIC_FILESYSTEM、PUBLICATION_FAILED、READBACK_FAILED。
- **Rollback:** 公開前は未公開stagingを隔離。公開後は既存成果物を勝手に削除しない。Concurrent writers／crashはstagingとrunを混同しない。

#### 検証

| Test ID | Unit / Contract / Negative | 判定 |
| --- | --- | --- |
| DD-E11-PUB01〜04 | disk full、commit marker前後、rename前後、fsync例外 | Partial bundleをsuccessとしない |
| DD-E11-PUB05 | Concurrent same run_id／異request hash | no-clobber、同hash readback only |
| DD-E11-PUB06 | path traversal、intermediate symlink、TOCTOU | root外read/write拒否 |
| DD-E11-PUB07〜09 | corruption、private 0700/0600、Reader roundtrip | 全bytes/hash/privacy/readback |
| DD-E11-PUB10 | Legacy Product Portと旧v2 CLIの回帰 | E11 publicationをProductの永続authorityへ混入しない |

**関連ID:** FR-185/201/203、NFR-029/031/032/036、BD01-F03/F05/F06/F12、IF IO-E11-01〜09。実FS Fault Injectionと科学的受入は、恒久的な検証義務として別に確認する。

### 3.3. `LocalManifestReader` — complete Class method protocol

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader`。
- **責務:** committed runをMarker→Manifest→Artifactの順に検証し、`VerifiedLocalRun`を返す。存在だけでCOMMITTEDと判断しない。
- **責務外:** publish、legacy v2の無断E11解釈、科学的Oracle計算、実Artifactの編集。
- **参照:** IF `23_42` §6〜8。

#### フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| Instance fields | N/A（stateless Reader） | N/A | trusted root/run IDはper-call引数。Cacheが必要なら原本Root・run IDとhash一致を保持し、未検証値の再利用を禁止 |

#### Constructor / Factory

- `__init__()`は特別な依存なし（read_runへ検証済み`TrustedLocalRoot`を明示注入するstateless API）。共通`LocalManifestReaderPort.verify(root,run_id)`はConcrete `read_run`へ委譲するAdapter。`Path`単独をTrustedRootに昇格しない。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

#### メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | secure read only; marker/hash/version/root/permissions fail-closed |

#### 処理仕様

1. Trusted root・run_idとlocal execution principalを検証し、run directoryにsecure open。
2. `_COMMITTED.json`存在/strict schema/version/request hashを確認。
3. `manifest.json`を同一安全dirfd scopeでopen、markerに保存されたManifest SHA256と照合し、`LocalRunManifest`をstrict decode。
4. Artifactの相対key重複、SHA256/size/MediaType、privacy class、必要なLineage Refの一致を検査。
5. Private Parquetには出力Policy/OS principalの許可なしでrow-level bytesを返さない。
6. 未検証・partial・legacy・corruptのいずれでも`VerifiedLocalRun`を返さない。

#### I/O・連携・失敗処理

- **Caller:** Local causal UseCaseのReadback／CLI status command、publisherのpublication verification。
- **I/O:** Trusted Rootからread-only。symlink/TOCTOUとstale marker防止のためopenされた同一File Descriptorに対しhashを確認。
- **Errors:** `NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`等を区分。
- **Retry:** 不完全runを勝手に修復／削除しない。既存同hash runの再利用は完全Readback PASSに限定。

#### 検証

`DD-E11-READ01` valid; `READ02` marker missing; `READ03` corrupted bytes/size; `READ04` wrong version; `READ05` individual export suppression; `READ06` old v2 not E11; `READ07` symlink/path race。関連要件：IF IO-E11-01〜09、FR-201〜203、NFR-031/032、BD01-F03/F05/F06/F12。

### 3.4. `GraphEvidence` — complete Class method protocol

#### 識別情報・責務

**Class / module:** `ariadne.causal.discovery.graph_evidence.GraphEvidence`。PAG/CPDAG/DAG/temporal等の科学的Graph Evidenceを保持するimmutable Value。Product `GraphVersion`のVersion作成・編集・FIX権限を持たない。現行`e11-local-graph/1` Wireでは`version_id`と`parent_version_id`を両方`null`に固定する（Schema const-null）。Product実在IDをE11 Local Wireへ写像・importしない。既存Product GraphVersionの実在IDと親整合は旧Product互換Bridgeで別に扱い、Graph科学的親はprovenance/ContentRef/hashで検証する。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `kind` | `GraphKind` | DAG/CPDAG/PAG等の区別 |
| `nodes` | `tuple[Node,...]` | unique identity |
| `edges` | `tuple[EndpointEdge,...]` | endpoint/lag/identityをlossless |
| `temporal` | `TemporalConvention|None` | lagの符号・基準時刻 |
| `source_graph_version_id` | `str|None` | E11 Localでは常にNone。実在するProduct IDは旧Product互換Bridgeの別契約でのみ検査 |
| `source_graph_parent_version_id` | `str|None` | E11 Localでは常にNone。科学的親provenanceは別のContentRef/hashで保持 |
| `provenance, content_hash` | `GraphProvenance, str` | Graph意味射影に一致するdigest |

#### Constructor / Factory

`from_canonical_json(raw:bytes)->GraphEvidence`：strict Graph Schema＋意味Validator。不可逆PAG→DAG変換、未知node/endpoint/重複edge/lag規約欠落を拒否。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_canonical_json(raw:bytes)` | `GraphEvidence` | pure strict graph decode | schema、endpoint、lag、hash不整合 |
| `canonical_payload()` | `Mapping[str,JsonValue]` | lossless domain serialization | invalid/incomplete Graph |

#### 処理仕様

`EndpointEdge(source,target,source_mark,target_mark,lag)`のmarkはTAIL/ARROW/CIRCLE。Node順序を反転する場合はendpointも対応させる。PAGのbidirected/circleをDAGへ暗黙確定しない。FIXEDは編集状態であってScientific Truthではない。未確定GraphからのEffect識別は独立のEstimand別識別証拠を要求。

#### I/O・連携・失敗処理

Graph Valueの純粋操作はI/Oなし。既存Productの`endpoint_source`／`endpoint_target`と新Wireの`source_mark`／`target_mark`は明示した双方向変換Adapterで対応し、端点の順序反転とmarkの交換を同時に行う。既存`graph_semantics.validate_graph_document`に新Wire dictを無変換で渡さない。内部`content_hash=SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256=SHA256(完成Graph File実bytes)`を**別々に検証**。RevisionとFIXはProductの既存GraphVersionServiceが所有する。

#### 検証

`DD-E11-GRAPH01` FCI PAG circle/arrow/bidirected・standalone両Version null、`GRAPH02` PCMCI lag、`GRAPH03` silent PAG→DAG拒否、`GRAPH04` Local内容hash・科学的親provenance・non-null Product import拒否と旧Product別Bridgeでの互換保護。FR-186/196、AR-028/036/043。

### 3.5. `EffectOutcome` — complete Class method protocol

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。

#### フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics` | `tuple[DiagnosticRef,...]`。Method別typed診断参照 |
| `method_evidence, upstream_hashes` | typed Backend evidenceとlineage |

#### Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_result_payload()` | typed Result payload | pure typed result projection。JCS byte encodingは共通Codec | incompatible schema/estimand |

#### 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。

## 4. Required implementation — G10/P03 replay and science boundaries

1. **Entry:** G10 06/07/Pxx Frozen、all required G01〜G09 latest canonical 999 PASS、Owner Coding Authorization、full Source/lock/environment SHA、Pxx checkpointを検証。未成立Gateを仮PASSとして扱わない。
2. Fixed Source/lock/fixture/MethodDescriptor/Backend/seed/Study/Graph/Method configから、Request SHAとSource ContentRefの異なるHash domainを検証して同一Result再現経路を構築。
3. 既存G01 LocalRunManifest/LocalManifestReaderの正規Schemaとcommit markerを再利用。Readerはactual byte SHA/size/MIME/Schema/operation discriminator/lineageとPublisherのno-clobberを確認する。
4. 科学的非決定性はseed固定のもとで事前に宣言した許容差/統計特性で判断し、bitwise equalityを暗黙要求しない。再計算とArtifact再読戻し/Checksum再確認を別Evidenceとして記録。
5. 途中失敗/電源断/Concurrent publish/manifest corruption/marker missingの再現でcompletedを偽装しない。実Readonly Sourceを改変/Row policy迂回してReplayしない。
6. **Boundaries:** Value/Scientific typed Ports→G01 StagingSink/Atomic Publisher/Readerを使い、CLI専用Scientific Kernel、未承認Row export、old v2破壊、Unknown Backendへのfallbackを禁止。科学的・技術的Statusは独立。
7. **Output/Evidence:** Method/Operation/Version/Backend/Profile/Source/Fixture/Oracle/seed/CI/Privacy/Manifest/Result SHA、実行時のenvironment、negativeとaccepted/rejected Reasonを残す。Independent 07/999は本Packageが代行しない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

Applicationの`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`を用いるFacade。二重の公開アルゴリズムにしない。staging全File/Directory fsync→同一FSの`renameat2(RENAME_NOREPLACE)`→親dir fsync→独立Reader readbackまで成功して初めてCOMMITTED。EEXIST時の同request hash再利用は全bytes/Manifest/Privacy検証済みに限る。rename後の失敗は`PUBLICATION_INDETERMINATE`、削除・上書き禁止。

**公開Portの正規署名：** `LocalPublicationPort.begin(*,run_id,request_hash,root)->StagingArtifactSink`、`seal(*,sink,manifest,privacy)->ValidatedStagedBundle`、`publish(*,bundle,root)->CommittedLocalRun`。`LocalManifestReaderPort.verify(*,root,run_id)->VerifiedLocalRun`。Publisher Concreteはrun-scopedで、Sinkが同一run handleを保持する。Reader readbackは公開成功の必要条件である。

`LocalRunManifest.to_canonical_bytes`は`e11-json-jcs-rfc8785/1`のstrict JCSで符号化しProductの`hash_mapping(default=str)`は用いない。request hashはValidatedStudy意味射影、Graph内部hashは自己fieldを除く意味射影、ContentRefとMarkerが指すManifest hashは保存実bytes。Markerはinventory外に置き、非Effect操作の`schema_dispatch.result=null`を認める。これだけでIDENTIFY/REFUTE/SENSITIVITY/DIAGNOSEの成果物を省略してよいことにはならない。23_42 §2.1のOperation Bundle ValidatorがGraph/Identification/Effect/Diagnosticsの必須性、Status、Method、upstream hashを結合検証する。

Concrete `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は公開`LocalManifestReaderPort.verify(*,root:TrustedLocalRoot,run_id:RunId)`から委譲される。Marker→Manifest→Artifact bytes/type/hash/size→cross-refsとPrivacyを検証する。入力Schema不正はexit2、公開済みbundle readback破損はphase=PUBLICATIONのexit5。修復・自動削除は行わない。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row ParquetはStudyの`privacy.row_export_requested=true`による単独opt-in、Linux非root実効EUID所有private ext4/XFS root（0700/0600、owner/mode/local ext4-XFS/同一FSを検証）、Method別ApprovedRowSchema/ordered column/row/byte/memory capsに合致する場合だけ、認可後の`RowEffectsParquetWriter`がG01 StagingSinkに遅延生成する。初期denyはexit3/Source反復0/row bytes0。署名鍵・独立承認者・失効はOwner 2026-11-21限定改訂で不要。G01 Publisher/Readerが唯一の公開/readback authority。実FS/Parquet/Method RowSchemaの実測未完はBLOCKED。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer delivery legal acceptance（配布時のみ）を意味しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof boundary:** G10の全41 Methodの§5 DGP/NEG/REF/ACは検証対象であり、Listが存在するだけで実Fixture/Oracle生成済みやScience PASSを意味しない。独立Reference/Generatorを事前固定し、FWER=.05とMethod別K/R/compute/MC-SE/coverageをFreeze前に確定する。未測定はBLOCKEDであり、Backendの出力を真値にしない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g10/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Package-focused acceptance and evidence matrix

- §4の各段階をunit/contract/実Backend・FS integrationで測定し、実在するlegacy product testsをcurrent checkoutからdiscoverして実行。Completion Reportのpath/commandを物理Authorityにしない。
- **Target-specific mandatory cases:** Fixed Source/lock/fixture/MethodDescriptor/Backend/seed/Study/Graph/Method configから、Request SHAとSource ContentRefの異なるHash domainを検証して同一Result再現経路を構築。 既存G01 LocalRunManifest/LocalManifestReaderの正規Schemaとcommit markerを再利用。Readerはactual byte SHA/size/MIME/Schema/operation discriminator/lineageとPublisherのno-clobberを確認する。 科学的非決定性はseed固定のもとで事前に宣言した許容差/統計特性で判断し、bitwise equalityを暗黙要求しない。再計算とArtifact再読戻し/Checksum再確認を別Evidenceとして記録。 途中失敗/電源断/Concurrent publish/manifest corruption/marker missingの再現でcompletedを偽装しない。実Readonly Sourceを改変/Row policy迂回してReplayしない。
- P04は§5の全41 MethodについてDGP/NEG/REF/DDと独立数値/構造Oracleを判定する。P01〜P03/P05はScopeに関係するMethod/Result保護義務を保持し、科学Kernelを再実装しない。
- Actual fixture/Source/lock/Backend/API SHA、Test layer/lifecycle、collected command、Observed/Expected、Quantitative Science K/R/MC-SE、PASS/FAIL/BLOCKED Reasonを記録。未実施をPASSとすることは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04,P05。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit design/Science/Legal Freeze conditions

Class Fields/Constructors/Public Methodの実行意味は§3、Method固有処理は§4、Method/DD/Science義務は§5〜6に収める。外部DDから不足仕様の推論をCoding Agentに強制しない。**Freeze blockers:** Replayのbitwise/数値許容差・Backend seed/version/Manifests/FS-failure semantics。 OwnerまとめReviewがこれらを判定するまでNo Coding Authorization/No Science PASS/No canonical promotion。

### Owner SIM-01/03/04 initial-Gate simplification (2026-11-21)

Mandatory integration profiles are ENV-BASE, ENV-DOWHY, ENV-ECONML and ENV-TIGRAMITE, each with actual lock/distribution/API smoke and Method-specific science/reproducibility checks. ENV-COMBINED all-extras runtime/CI is an optional later interop check, **not** G10 initial PASS dependency; do NOT claim simultaneous all-extras environment is verified. Local scientific Manifest has NO required `runtime.sbom_ref` or `review.legal_delivery_status` (the active Draft 2020-12 Schema removed them); installed distribution/version/lock source provenance and independent science review evidence remain required. SBOM generation, per-customer authorization state and legal evidence are NOT G10 CLI runtime functionality. Prior to any actual customer external delivery, the Owner/legal reviewer must manually review actual shipped dependencies and block unapproved distribution. FS privacy boundary is ordinary nonroot Linux EUID/private owner-only ext4/XFS root with 0700/0600 and FD-safe paths/same FS; no separate ACL/xattr digest, mount namespace/ID proof or CI/container classification. Preserve G01 Publisher/Reader, NFR-030/031/032/033/035/036, all science, all Method ID targets, upstream Gate999 independence and Product v2. Historical DEC08/PREP02 remains historical, specifically superseded by combined_review/131. No runtime evidence / Gate999 PASS / Coding Authorization.


## S02-01〜08：G10 全Method証拠・差分再実行の正規契約

G10は41 Method全件（P1=20/P2=8/P3=13）の独立DGP/NEG/REF、Method別Schema/Estimand/Inference、Backendとsource+fixture SHA、T2/T3事前登録・FWER=.05、上流999を検証する。**全件を無条件に数値再実行する要求はない**。承認済み独立証拠について、Method code、shared scientific kernel、Method Registry/descriptor/schema、ports/validation、依存コード/ABI、Python/uv.lock/extra/Backend distribution+version、fixture/DGP、negative、Oracle/reference source、seed/quantitative AC/protocol、privacy・Result/Manifestが科学的結果に影響し得る**推移的依存閉包**を監査し、厳密に同一のものだけ再利用する。完全な閉包不変証明が欠損・不整合なら再実行し、再実行不能なら該当MethodをBLOCKしてG10_999 PASSを禁止する。新規/変更された評価指標を既存証拠から事後推測しない。最終Fixed Trial Candidate全体のOperation・Method/Estimand/Inference dispatch、JCS/ContentRef/Manifest/Marker/Reader、G05 Study単独opt-in/Privacy、Product v2互換と横断Negativeは毎回独立に実行する。Libraryのsymbol/API存在はScience PASSではない。

G10-07の最小受入集合：同一full-SHA閉包→上流Science証拠再利用の正例、共有Kernel/Schema/lock/Backend/Fixture/REF/Policyの各1点変更→影響Methodの再実行またはBLOCK、依存グラフに未知辺→BLOCK、既存証拠に欠損/科学的FAIL→全41のPASS禁止、未変更41件のScience真値と後続横断統合別軸検証。旧Productの無関係なSuiteは全件無条件再試験せず、protected境界への影響閉包を証明して必要分を実行する。未知影響なら実行またはBLOCK。G05はStudy trueとnonroot same-UID private ext4/XFS/Method別allowlist・row/byte/memory capsのAND、false/省略は個票なし。署名Verifier・PolicyRef・追加CLI許可Flagは実装しない。現行Local Graphは内容hash/由来、Product Version IDはnull、非対応import拒否。40 Profileは共通Schema＋Method overlayを再構成して厳格検証し、未登録/未試験はfail-closed。外販向けLicense Governance NFR-034はDEFERREDだが社内OSS義務は継続。Coding Authorization未発行、B04/B05の実効証拠は未取得。

## S09-R12 P3-M06 ITS output integration invariant (2026-11-22; DRAFT)

P3-M06 output is Method-config dependent: `effect_components=LEVEL` publishes scalar β_L and typed `its_components.json`; `LEVEL_AND_SLOPE` has a non-scalar Result point with `NON_SCALAR_TARGET` and the same typed sidecar carrying β_L, β_S and only explicitly predeclared horizon effects `β_L+hβ_S`. Both must match the current strict P3-M06 Output Profile/Descriptor catalog and the `e11_its_components_draft1.schema.json` draft. G10 must not drop the sidecar when rebuilding the 41-Method Operation/Result/Manifest matrix; preserve checksum/Study/Design/Method identity, request-mode/Status consistency, and independent DGP-014/NEG-023 science tests. Tested marginal HAC intervals do not automatically certify joint level+slope coverage. No arbitrary default horizon, no observed row leakage, no new public wire.

**This package:** P03 verifies actual Manifest/Marker/Reader and replay integrity without inventing completed science.

## DEC-S09-P3M04-01 Owner A — G10 cross-Gate capability reconciliation (2026-11-22)

Owner DEC-S09-P3M04-01=A: P3-M04 initial 2×2 DiD ATT is the sole executable positive variant (`design_variant=DID_2X2`) when separately scientifically/backend eligible. `STAGGERED` remains a syntactically recognized but `DEFERRED` future capability. The Method-specific scientific preflight must reject STAGGERED as `SCIENCE_CONTRACT_NOT_AVAILABLE` / `CAPABILITY_UNAVAILABLE` (CLI exit4), never estimating, publishing a successful Effect Result/Manifest or silently falling back to DID_2X2, TWFE or P3-M05. Unknown/malformed variant is validation exit2. The 41-Method count stays unchanged. The G10 41-Method evidence matrix requires independent valid science for P3-M04 DID_2X2 and the deferred-variant negative, **not** a staggered ATT(g,t) executable positive. DGP-013 remains mandatory where applicable to P3-M05, but not as positive P3-M04 STAGGERED. Existing G10 transitive-closure evidence reuse rules remain unchanged.

**Package-scoped action:** P03 rejects successful Manifest/Marker replay for an unsupported STAGGERED attempt and protects correctly published DID_2X2 bundles.
