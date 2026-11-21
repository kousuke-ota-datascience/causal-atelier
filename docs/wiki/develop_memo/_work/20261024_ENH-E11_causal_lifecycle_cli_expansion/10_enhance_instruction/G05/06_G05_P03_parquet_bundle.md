# ENH-E11 G05 P03 — parquet_bundle

### 現行G05個票出力契約 — Owner 2026-11-21

- **要件:** FR-195／NFR-031／P2-15。一般ユーザーによるローカル分析中間Artifact。第三者Approver、署名、鍵、失効、issuer registryの承認プロセスを要求しない。「独立承認」ではなく「実行者の明示的opt-in」と定義する。
- **対象環境:** Linux非root実効UID・ext4/XFS local filesystem。UID=root owner、root/staging 0700・Parquet 0600、ACL/mount/namespace/symlink/dirfd・same-FSを検証。管理者・同一UID processは本Threat Modelで隔離できない。
- **許可AND:** `Study.privacy.row_export_requested=true` ∧ CLI `--allow-row-level-export` ∧ `RESTRICTED_ROW_LEVEL` ∧ 対象Methodの`ApprovedRowSchema`/ordered allowlist/row ID・row/byte/memory上限 ∧ private EUID-owned TrustedRoot ∧ same-run G01 StagingSink。未認可ならexit3、RowSource反復0・row bytes0、暗黙aggregate fallback無し。
- **既決APIの限定変更:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase.__init__`から署名Verifier依存を除く。`e11-local-study/1`は維持し任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **維持するClass:** `RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`。Sourceは全許可成立後だけ反復。WriterはG01公開責務を複製しない。
- **出力:** `row_effects.parquet`／`application/vnd.apache.parquet`／`RESTRICTED_ROW_LEVEL`。G01のみstaging/atomic no-clobber/Manifest/Marker/Reader。Stage/Seal/Publish前にroot/UID/ACL/mount/runを再検査。後段異常でprivate stagingの過去bytes0を主張せず、公開成功にもしない。Result/Manifest/stdout/stderr/logに行値なし。
- **未完了:** Method別RowSchema/制約数値、実ext4/XFS/ACL/mount、Parquet ABI、科学Reference、独立07実測。Freeze・Coding Authorization・999は未実施。変更のAuthorityは`combined_review/129_20261121_dec_g05_local_row_export_simplification.md`、過去PREP-02/03/04.2は履歴として保持。


**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G05 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G05_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G05_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** RowEffectsParquetWriter/FactoryのClass責務・公開MethodはOwner採用済み。未配備Backend/ApprovedRowSchema/OSをFreeze前検証。Writer/Reader両側でcolumn/row bound検査。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** RowEffectsParquetWriter/FactoryのClass責務・公開MethodはOwner採用済み。未配備Backend/ApprovedRowSchema/OSをFreeze前検証。Writer/Reader両側でcolumn/row bound検査。

### 2A. 既存SourceとRow Release authorityの境界（`2cf28f59a324`）
- **既存:** `src/ariadne/product/application/graph_version_service.py`の`GraphVersionService.create(...)`/`fix_graph(...)`はProduct GraphVersion Authorityであり、Local CLIが同名Publisher/Version writerを作って代替しない。`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(input_: EstimationInput, output_dir: Path)`は旧Path API、HTEと認可済Parquet Writerの実装済み証拠ではない。
- **現行G05実装条件:** Study＋CLI両方の明示opt-in、実効EUID/private root、Method別RowSchema/上限。初期denyは行生成0、stage後異常はCOMMITTED無し。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher` | Port/Value/Facade integration (no duplicate implementation) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `RowEffectsParquetWriter` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsParquetWriter` | P03 primary new Class | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `RowEffectsWriterFactory` | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsWriterFactory` | P03 factory | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | Port/Value/Facade integration (no duplicate implementation) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

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

| Field | Type | 生成元 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `root` | `TrustedLocalRoot` | OS検証済みdirfd Capability | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `run_id` | `str` | 正規化済LocalStudySpec | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `request_hash` | `str` | canonical LocalStudySpec bytes | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `state` | `PublishState` | FactoryでPREPARING | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `staging_handle` | `StagingHandle|None` | begin | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | stage_bytes | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `permission_policy` | `LocalPrivacyPolicy` | 注入Policy | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

#### Constructor / Factory

- **Constructor:** `__init__(self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`。rootはOS/ACL/mount/dirfdを検証済みのCapability（任意Pathではない）。random staging tokenは`begin`時に生成する。実装時にRootの変更をcommit境界まで検出する。
- **前提:** `run_id`にseparator/「.」「..」を含まない、request hashはcanonical versionと一致。Trusted Root所有者／同一FS／OS principalの確認に失敗したらstaging生成しない。

#### メソッド

| Signature | Return | 責務・副作用 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `begin(self) -> StagingArtifactSink` | staging sink | 0700 staging dir作成、state遷移 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `stage_bytes(self, key: RelativeArtifactKey, data: bytes, media_type: str, classification: PrivacyClass) -> ArtifactDescriptor` | descriptor | dirfd相当のroot閉じ込めで0600 file作成/追加 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `validate(self, manifest: LocalRunManifest) -> ValidatedBundle` | readback済み候補 | 各Artifact→Manifest→markerのhash/Schema/Privacy検証 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `commit(self, validated: ValidatedBundle) -> CommittedRunRef` | published run ref | PUBLISHING状態でno-clobber rename、親dir fsync、独立Reader readbackを終えた場合にだけCOMMITTED | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `abort(self, reason: str) -> None` | None | 未公開stagingを隔離しHandle解放 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

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

| Test ID | Unit / Contract / Negative | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DD-E11-PUB01〜04 | disk full、commit marker前後、rename前後、fsync例外 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DD-E11-PUB05 | Concurrent same run_id／異request hash | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DD-E11-PUB06 | path traversal、intermediate symlink、TOCTOU | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DD-E11-PUB07〜09 | corruption、private 0700/0600、Reader roundtrip | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DD-E11-PUB10 | Legacy Product Portと旧v2 CLIの回帰 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

**関連ID:** FR-185/201/203、NFR-029/031/032/036、BD01-F03/F05/F06/F12、IF IO-E11-01〜09。実FS Fault Injectionと科学的受入は、恒久的な検証義務として別に確認する。

### 3.2. `LocalRunManifest` — normative implementation contract

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`、immutable typed DTO。
- **責務:** 1 Local runのidentity、lineage、Method/Science/Runtime、artifact inventoryをversioned schemaで保持し、canonical bytesのauthorityを定義する。
- **責務外:** file open、hash verificationのI/O、実効科学計算、Local OS permission enforcement。
- **参照:** IF `23_42` §6、`23_41` §5。Existing Product CliManifestとは別schema。

#### フィールド

| Field | Type | Origin | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `manifest_version` | `Literal["e11-local-manifest/1"]` | Schema | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `run_id, operation, request_hash` | `str, LocalOperation, str` | validated Study | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `lineage` | typed refs + hashes | Question/Design/Graph/Dataset/Identification | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `execution_status` | typed technical + scientific axes | LocalRunOutcome | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `runtime` | `RuntimeEvidence` | effective probe | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | Publisher stage validation | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `review` | evidence refs + legal release state | SCI + policy | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

この表は論理的なField groupingであり、wireの厳格なversion/Schema検証は23_42に従う。

#### Constructor / Factory

- **Factory:** `from_payload(payload: Mapping[str, JsonValue]) -> LocalRunManifest`、`from_run_evidence(evidence: ValidatedRunEvidence) -> LocalRunManifest`。
- **Precondition:** strict schema/version + no unknown critical keys; content hash references are normalized; `Manifest` must **not** include its own bytes hash; marker is outside Artifact list. Factories do not read the filesystem.
- **N/A:** runtime backend import is not part of this DTO. Factoryはstrict Schema違反を型付きErrorとして返す。

#### メソッド

| Signature | Result | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `validate_invariants(self) -> tuple[Reason,...]` | typed reasons | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `to_canonical_bytes(self) -> bytes` | canonical versioned JSON bytes | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `from_payload(payload) -> LocalRunManifest` | immutable DTO | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

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

| Field | Type | Origin | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| Instance fields | N/A（stateless Reader） | N/A | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

#### Constructor / Factory

- `__init__()`は特別な依存なし（read_runへ検証済み`TrustedLocalRoot`を明示注入するstateless API）。共通`LocalManifestReaderPort.verify(root,run_id)`はConcrete `read_run`へ委譲するAdapter。`Path`単独をTrustedRootに昇格しない。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

#### メソッド

| Signature | Result | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| --- | --- | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

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


### 3.4. `RowEffectsParquetWriter` — G05/P03 primary Class contract

#### 3.4.1. 識別情報・責務
**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

#### 3.4.2. Field / Constructor
`serializer: ValidatedParquetSerializer`（eff runtime/Version/APIを確認）、`max_memory_bytes: int`（正の上限）のimmutable依存だけ。`__init__(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int)`。run、Secret、Policy/Sourceはper-callで扱いClass内に永続保持しない。

#### 3.4.3. Method / exact types
`write(self, *, source: DeferredRowEffectsSource, study: ValidatedStudy, decision: PrivacyDecision, selection: ColumnSelection, sink: StagingArtifactSink) -> ArtifactDescriptor`。関連Protocolは`DeferredRowEffectsSource.schema()->ColumnSchema`、`read_rows()->Iterable[Mapping[str,JsonValue]]`、`ValidatedParquetSerializer.encode(self, *, rows: BoundedRowBatch, schema: ApprovedRowSchema)->bytes`。

#### 3.4.4. Preconditions / Steps
1. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
2. 認可前に`source.read_rows`を**一度も呼ばず**個票bytesを生成しない。`source.schema()`とApprovedRowSchemaを検証後、`max_rows+1` sentinelまで遅延取得し上限超過はfail closed。No automatic sampling/lineage change。row ID・Effect dtype・unique identity、unknown column、NaN/Inf、不正zero rowを拒否。
3. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
4. `sink.stage_bytes(key=RelativeArtifactKey("row_effects.parquet"), data=parquet_bytes, media_type="application/vnd.apache.parquet", classification=PrivacyClass.RESTRICTED_ROW_LEVEL)`して`ArtifactDescriptor`を返す。Publisherは唯一G01 `LocalArtifactPublisher`：seal/atomic no-clobber/fsync/Independent Reader readbackでCOMMITTEDを判定する。Writerは`runs/`や別commit markerを作らない。

#### 3.4.5. Failure / acceptance
**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

### 3.5. `RowEffectsWriterFactory` and Serializer contracts

- **Factory:** `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsWriterFactory.create(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int) -> RowEffectsParquetWriter`。Factoryは承認Authorityではない。
- **現行G05実装条件:** Study＋CLI両方の明示opt-in、実効EUID/private root、Method別RowSchema/上限。初期denyは行生成0、stage後異常はCOMMITTED無し。
- **`ValidatedParquetSerializer`:** CLI-adapter Protocol `encode(self, *, rows: BoundedRowBatch, schema: ApprovedRowSchema) -> bytes`。Backend effective version/API/valid dtype/ordered columns/row maxを確認、値/個人情報をログ出力しない。

## 4. Required implementation — G05/P03 dedicated processing

1. **Entry:** G04 canonical 999 PASS、G05 Frozen06/07/Pxx、Owner Coding Authorization、Source/lock、依存Pxxを確認。G04のEffect/CATE/Graph/Studyが同一Hash/Version/Estimand対象であることを検証。
2. Typed CATE/Diagnosticから認可されたColumnSelection・RowLimit・verified Approval Evidenceを検証し、実データ行は許可前にmaterialize/serializeしない。
3. **RowEffectsParquetWriter/FactoryのClass/Method契約はOD-03=AでOwner採用済み**。`LocalArtifactPublisher`の`StagingArtifactSink`/atomic no-clobber責務と、Parquet row serialization責務を混同しない。WriterはG05/P03、Signer検証はG05/P02、Publisher/ReaderはG01がOwner採用済み。実Deployment/Schema/Backend TestはFreeze前に必要。
4. 承認済み場合に限りParquet schema/column order/dtype/row count/privacy class、artifact SHA/size、manifest lineage、readback consistencyを実測。明示的な非列集合/有効行数/零行を検証。
5. Study＋CLI二重opt-in、実効Linux EUID所有のprivate ext4/XFS root、Method別行列byte上限とrun identityを検証。初期denyはexit3・RowSource反復0、成功時だけG01へstage。
6. **Privacy boundary:** 未承認・技術的失敗・Authority未定はzero-rowでstopし、許可ErrorをError suppressionやdummy Policyで回避しない。G01 Publisher/Readerは再実装しない。Optional Backend/Science Availabilityも分離する。
7. **Output:** Typed Decision/Evidence/Aggregate/Policy-bound Artifactを必要な場合のみStaging→Atomic Publisherへ渡す。既存Product ABIとException/Exit policyを保護する。

### 設計書で定義済みの実装意味論（本Packageの規範）

以下は既存30_62/30_63の設計規則のうち本Packageへ適用する本文内契約である。外部DDを読ませて仕様を補完することは禁止する。自Packageが所有しないClassは再実装しない。

Applicationの`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`を用いるFacade。二重の公開アルゴリズムにしない。staging全File/Directory fsync→同一FSの`renameat2(RENAME_NOREPLACE)`→親dir fsync→独立Reader readbackまで成功して初めてCOMMITTED。EEXIST時の同request hash再利用は全bytes/Manifest/Privacy検証済みに限る。rename後の失敗は`PUBLICATION_INDETERMINATE`、削除・上書き禁止。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

`LocalRunManifest.to_canonical_bytes`は`e11-json-jcs-rfc8785/1`のstrict JCSで符号化しProductの`hash_mapping(default=str)`は用いない。request hashはValidatedStudy意味射影、Graph内部hashは自己fieldを除く意味射影、ContentRefとMarkerが指すManifest hashは保存実bytes。Markerはinventory外に置き、非Effect操作の`schema_dispatch.result=null`を認める。これだけでIDENTIFY/REFUTE/SENSITIVITY/DIAGNOSEの成果物を省略してよいことにはならない。本書§2BのOperation Bundle ValidatorがGraph/Identification/Effect/Diagnosticsの必須性、Status、Method、upstream hashを結合検証する。

Concrete `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は公開`LocalManifestReaderPort.verify(*,root:TrustedLocalRoot,run_id:RunId)`から委譲される。Marker→Manifest→Artifact bytes/type/hash/size→cross-refsとPrivacyを検証する。入力Schema不正はexit2、公開済みbundle readback破損はphase=PUBLICATIONのexit5。修復・自動削除は行わない。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| unit | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| contract | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| integration | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| scientific evidence | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g05/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. G05 privacy and evidence test contract

- 必須の受入条件は§4の各分岐、§5のScience/Method依存、§6のunit/contract/実filesystem integrationで個別に判定する。
- **現行G05実装条件:** Study＋CLI両方の明示opt-in、実効EUID/private root、Method別RowSchema/上限。初期denyは行生成0、stage後異常はCOMMITTED無し。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit unresolved design — freeze barrier

**Document independence:** Class Fields/Constructor/Methodは§3、専用処理は§4、検証/負例は§6で完結。Owner決定が無い要件は仮構実装で埋めない。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

