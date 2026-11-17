# ENH-E11 G05 P03 — parquet_bundle

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G05 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G05_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G05_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 個票Parquet WriterのClass責務・正確署名未確定はDESIGN_GAPとして明記。Writer/Reader両側でcolumn/row bound検査。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** CATE support/calibration/uncertaintyと独立事前承認に基づく個票成果物発行を検証する。

**科学/Designの必須制約:** 独立承認Authority、鍵・失効、Row WriterのClass/Method所有権に設計未確定がある。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 個票Parquet WriterのClass責務・正確署名未確定はDESIGN_GAPとして明記。Writer/Reader両側でcolumn/row bound検査。

### 2A. 既存SourceとRow Release authorityの境界（`2cf28f59a324`）
- **既存:** `src/ariadne/product/application/graph_version_service.py`の`GraphVersionService.create(...)`/`fix_graph(...)`はProduct GraphVersion Authorityであり、Local CLIが同名Publisher/Version writerを作って代替しない。`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(input_: EstimationInput, output_dir: Path)`は旧Path API、HTEと認可済Parquet Writerの実装済み証拠ではない。
- **Design-only:** `LocalPrivacyPolicy`の純粋`authorize/filter_export_columns`と、独立承認機関が発行する証拠を検証するVerifier、認可後に初めてrow bytesを生成するParquet Writerは別責務。現在の§3契約のうちAuthorityの署名・Key Owner・Scope・期限・失効・Anti-replay、Row Writer Class/Factory/Methodが**未決**であり、Agentが作成したPolicyRef/bool/CLI flagは認可として無効。承認前のrow materialize/serialize/publishは禁止。`LocalCausalUseCase`・G01 Publisher/Reader/RegistryをG05で複製しない。
- **Freeze blocker:** Row許可のOwner決定後、本Pxxの設計中Class/API・G05 Gate06/07の同一Authorityを改訂/Freezeするまでは、個票処理パスは`BLOCKED_PRIVACY_AUTHORITY_UNRESOLVED`。mockは実認可証拠を代替せず、無断でパスを実装しない。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | 禁止・negative条件 |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`＋nonempty reason、`schema_dispatch.graph=null`。Backend失敗との混同は禁止 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Effect `result.json`禁止。識別negativeもtyped、Graph/Design/Estimand/Proof hashを照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。point欠落はnull＋理由で表し、非識別への推定値偽装禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effect再発行禁止。上流Effect/Graph/Design hash、seed・適用条件の検証が必須 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）を置くが、両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key・size bytes・SHA256・MediaType・Privacyを列挙。`request_hash=SHA256(JCS(validated typed Study JSON))`、Manifestに自己hashを入れずMarkerがManifestの実bytes SHA256を保持。Readerはmarker→manifest→artifact→Operation Profile→upstream hashをTrustedRoot内で検証。staging→atomic no-clobber publishを既存G01 Publisherで行い、Row Parquetは独立承認証拠の検証前にbytes生成すら禁止。Publication不正・欠損をScience negativeに変換しない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | Port/Value/Facade integration (no duplicate implementation) | begin(self)->StagingArtifactSink; stage_bytes(self,key:RelativeArtifactKey,data:bytes,media_type:str,classification:PrivacyClass)->ArtifactDescriptor; validate(self,manifest:LocalRunManifest)->ValidatedBundle; commit(self,validated:ValidatedBundle)->CommittedRunRef; abort(self,reason:str)->None |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | Port/Value/Facade integration (no duplicate implementation) | to_canonical_bytes() |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) |

**Class/Method authority:** 本Pxx §3.1以降に埋め込んだField/Constructor/Public Methodが一次規範。本Gateの主責務はHTE診断/Policy/認可付きWriter/Readerであり、新Scientific Adapterを追加しない。Approval AuthorityやRow WriterのClass/Methodは未決ならBLOCKEDとしてOwner決定を求め、Agentが独自署名・鍵・出力方式を創作してはならない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent of external DD)

このPxxの実行に必要なClassのField/Constructor/Method/Process/Failureを以下に内包。外部DDはTraceabilityのみ。現行SourceとのABI差分は開始時に確認し、欠陥ならOwnerレビューに戻す。

### 3.1. `LocalArtifactPublisher` — normative implementation contract

#### 識別情報・責務

- **Module / Class:** `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher`
- **責務:** 同一local filesystem上の複数Artifactをrun単位で検証・原子的に公開し、readback成功を確認する。Local File Bundleのpublication authorityでありProductの`ArtifactStorePort`ではない。
- **責務外:** Scientific Estimator、HTTP/DB、顧客配布Legal、外部FSのcross-device atomicity。
- **関連設計:** 23_42 §2/6/7。Product ArtifactStorePortは別のauthorityである。

#### フィールド

| Field | Type | 生成元 | 可変性・制約 |
| --- | --- | --- | --- |
| `root` | `TrustedLocalRoot` | OS検証済みdirfd Capability | Immutable root handle。所有者・ACL・mount/同一FSを検証し、commit時にも整合を確認 |
| `run_id` | `str` | 正規化済LocalStudySpec | Immutable。23_42のsafe grammar |
| `request_hash` | `str` | canonical LocalStudySpec bytes | Immutable。小文字SHA256 hex64 |
| `state` | `PublishState` | FactoryでPREPARING | PREPARING→STAGING→VALIDATING→PUBLISHING→COMMITTED/INDETERMINATE、公開前のみABORTED |
| `staging_handle` | `StagingHandle|None` | begin | State依存。Trusted FS descriptorを閉鎖管理 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | stage_bytes | Commitまで追加、公開後immutable |
| `permission_policy` | `LocalPrivacyPolicy` | 注入Policy | Resultのrelease policyと一致を要求 |

#### Constructor / Factory

- **Constructor:** `__init__(self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`。rootはOS/ACL/mount/dirfdを検証済みのCapability（任意Pathではない）。random staging tokenは`begin`時に生成する。実装時にRootの変更をcommit境界まで検出する。
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

### 3.2. `LocalRunManifest` — normative implementation contract

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
| `review` | evidence refs + legal release state | SCI + policy | absent proof remains null / NOT_EVALUATED |

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

### 3.3. `LocalManifestReader` — normative implementation contract

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

## 4. Required implementation — G05/P03 dedicated processing

1. **Entry:** G04 canonical 999 PASS、G05 Frozen06/07/Pxx、Owner Coding Authorization、Source/lock、依存Pxxを確認。G04のEffect/CATE/Graph/Studyが同一Hash/Version/Estimand対象であることを検証。
2. Typed CATE/Diagnosticから認可されたColumnSelection・RowLimit・verified Approval Evidenceを検証し、実データ行は許可前にmaterialize/serializeしない。
3. **Row WriterのConcrete Class・Factory・Signatureは現設計で未確定**。`LocalArtifactPublisher`の`StagingArtifactSink`/atomic no-clobber責務と、Parquet row serialization責務を混同しない。Parser/Writer/Publisherの所有権はFreeze前Owner設計決定が必要。
4. 承認済み場合に限りParquet schema/column order/dtype/row count/privacy class、artifact SHA/size、manifest lineage、readback consistencyを実測。明示的な非列集合/有効行数/零行を検証。
5. commit marker/fsync/no-clobber/torn-writeはG01と同一Publisherに委譲し、並行実行と失効/期限切れでのzero-row/no publishを負例検証。
6. **Privacy boundary:** 未承認・技術的失敗・Authority未定はzero-rowでstopし、許可ErrorをError suppressionやdummy Policyで回避しない。G01 Publisher/Readerは再実装しない。Optional Backend/Science Availabilityも分離する。
7. **Output:** Typed Decision/Evidence/Aggregate/Policy-bound Artifactを必要な場合のみStaging→Atomic Publisherへ渡す。既存Product ABIとException/Exit policyを保護する。

### 設計書で定義済みの実装意味論（本Packageの規範）

以下は既存30_62/30_63の設計規則のうち本Packageへ適用する本文内契約である。外部DDを読ませて仕様を補完することは禁止する。自Packageが所有しないClassは再実装しない。

Applicationの`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`を用いるFacade。二重の公開アルゴリズムにしない。staging全File/Directory fsync→同一FSの`renameat2(RENAME_NOREPLACE)`→親dir fsync→独立Reader readbackまで成功して初めてCOMMITTED。EEXIST時の同request hash再利用は全bytes/Manifest/Privacy検証済みに限る。rename後の失敗は`PUBLICATION_INDETERMINATE`、削除・上書き禁止。

**公開Portの正規署名：** `LocalPublicationPort.begin(*,run_id,request_hash,root)->StagingArtifactSink`、`seal(*,sink,manifest,privacy)->ValidatedStagedBundle`、`publish(*,bundle,root)->CommittedLocalRun`。`LocalManifestReaderPort.verify(*,root,run_id)->VerifiedLocalRun`。Publisher Concreteはrun-scopedで、Sinkが同一run handleを保持する。Reader readbackは公開成功の必要条件である。

`LocalRunManifest.to_canonical_bytes`は`e11-json-jcs-rfc8785/1`のstrict JCSで符号化しProductの`hash_mapping(default=str)`は用いない。request hashはValidatedStudy意味射影、Graph内部hashは自己fieldを除く意味射影、ContentRefとMarkerが指すManifest hashは保存実bytes。Markerはinventory外に置き、非Effect操作の`schema_dispatch.result=null`を認める。これだけでIDENTIFY/REFUTE/SENSITIVITY/DIAGNOSEの成果物を省略してよいことにはならない。23_42 §2.1のOperation Bundle ValidatorがGraph/Identification/Effect/Diagnosticsの必須性、Status、Method、upstream hashを結合検証する。

Concrete `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は公開`LocalManifestReaderPort.verify(*,root:TrustedLocalRoot,run_id:RunId)`から委譲される。Marker→Manifest→Artifact bytes/type/hash/size→cross-refsとPrivacyを検証する。入力Schema不正はexit2、公開済みbundle readback破損はphase=PUBLICATIONのexit5。修復・自動削除は行わない。

`LocalPolicyVerifierPort.verify`は`context.policy_anchor`（Study/CLI入力とは独立のsecure runtime configuration由来）によりStudy・scope・columns・row boundを事前承認した`VerifiedStudyPolicyEvidence`を生成する。Study自身のbool/policy_refは認可証拠ではない。`LocalPrivacyPolicyPort.authorize`の`PrivacyDecision`前に個票bytesをstagingに出力しない。same-UID/private owner-controlled TrustedRootが基準で、shared/CI/container-root可視mountや不明ACL/namespaceはfail-closed。署名アルゴリズムや鍵配布・失効方式は別の具体Policyとして設定可能であり、Ed25519等を無条件の仕様に固定しない。

**PrivacyのAuthority署名方式・鍵配布/失効・Writer Class等の具体未決は上記方針とは別の真のDesign Gapであり、未決ScopeをBLOCKEDにする。**

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof boundary:** §5のMethod参照は科学Kernelの再実装指示ではない。G05の主受入は§4と§6のPolicy/Privacy/HTE診断のpositive/negative。必要な科学真値は独立Referenceを使用し、未生成FixtureやFWER=.05/K/R/Coverage未決をPASSとしない。Trust AnchorとRow Writerの設計空白はBLOCKEDであり外部文書から推測しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g05/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. G05 privacy and evidence test contract

- 必須の受入条件は§4の各分岐、§5のScience/Method依存、§6のunit/contract/実filesystem integrationで個別に判定する。
- Typed CATE/Diagnosticから認可されたColumnSelection・RowLimit・verified Approval Evidenceを検証し、実データ行は許可前にmaterialize/serializeしない。 **Row WriterのConcrete Class・Factory・Signatureは現設計で未確定**。`LocalArtifactPublisher`の`StagingArtifactSink`/atomic no-clobber責務と、Parquet row serialization責務を混同しない。Parser/Writer/Publisherの所有権はFreeze前Owner設計決定が必要。 承認済み場合に限りParquet schema/column order/dtype/row count/privacy class、artifact SHA/size、manifest lineage、readback consistencyを実測。明示的な非列集合/有効行数/零行を検証。 commit marker/fsync/no-clobber/torn-writeはG01と同一Publisherに委譲し、並行実行と失効/期限切れでのzero-row/no publishを負例検証。
- Evidenceはpositive/negative、Approval Signature/Expiry/Scope、Effective UID/ACL/mount、row bytes createdか、Parquet/Manifest/Marker/Readback、source/fixture SHAとactual commandを含める。秘密鍵そのものや個票のログ出力は禁止。
- Test側のCollection/Runner実Pathは40の発見規則に従う。未実装Approval Authority/Writerをmockして正規Privacy PASSとしない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit unresolved design — freeze barrier

**Document independence:** Class Fields/Constructor/Methodは§3、専用処理は§4、検証/負例は§6で完結。Owner決定が無い要件は仮構実装で埋めない。

**BLOCKED before Freeze:** Parquet Row WriterのClass/Method/Factory/API、認可されたbytes作成前の安全な連携。 これらは本Pxxに係る未確定決定であり、他Pxx/07/設計書を読んで推定してはならない。G05のRow出力をG01〜G04に遡及して許可しない。
