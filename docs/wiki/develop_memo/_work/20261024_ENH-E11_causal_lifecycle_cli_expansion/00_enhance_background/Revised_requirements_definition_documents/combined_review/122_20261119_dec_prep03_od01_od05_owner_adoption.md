# DEC-PREP03-OD01–05 — Owner採用決定（2026-11-19 JST）

**Decision authority:** Owner明示回答「採用する」（2026-11-18T22:10:50Z / 2026-11-19 07:10:50 JST）。直前の推奨セット **OD-01=A、OD-02=A、OD-03=A、OD-05=Gate別Method Profile作成方針** を採用する。  
**Previous baseline:** `be7cfbf6d76ae438c215be3f4fc9f285b543648a` (`prototype/ariadne_mvp`)。  
**Status:** `OWNER_ADOPTED_DESIGN_CHOICES / DESIGN_PROPAGATED_REVIEW_DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED / NO_SCIENCE_TEST`。  
**Source candidates:** [118](118_20261118_prep03_od01_iv_target_decision_candidate.md)、[119](119_20261118_prep03_od02_od03_row_export_design_candidate.md)、[120](120_20261118_prep03_od05_method_profile_gap_register.md)、[121](121_20261118_prep03_owner_decision_submission.md)。各候補の未採用Option B/Cは採用しない。

## 1. 正式採用と責務境界

| Decision | Adopted option | 本決定で確定する契約 | 本決定で**確定しない**実効値・証拠 |
|---|---|---|---|
| **OD-01 / P1-M05** | **A** | **IDENTIFY-only、B0二値Z/A無調整・単一IVの条件付きcomplier `LATE_COMPLIER`識別**。DoWhy backend出力名だけでは認定せず、Graph/Designに記述された有効なIV仮定をtyped Evidenceへ紐付ける。B1/DRIV/ATEには自動転換しない。数値推定はG08 | 実効DoWhy API、前提の実世界での真偽、Method個別Profile、独立DGP/REF・Science PASS |
| **OD-02 / Row Trust** | **A** | **Ed25519 detached signature + admin-owned非EUID-writable trust registry/revocation**。strict versioned JCS署名payload／domain separator、Studyのpolicy_refをnullにした承認対象digest、run_id/issuer/key/scope/classification/columns/row/byte cap/期限/失効epoch束縛、署名鍵と検証鍵registryの権限分離。既存`LocalPolicyVerifierPort.verify`を保つ | **現実に権限を持つ独立承認者／admin provisionerの指定と鍵配備**、target OSでのtrust-store保護/clock/失効feedの実効動作、freshness上限の運用値。未充足時は個票deny、一般集計だけ可能 |
| **OD-03 / Row Writer** | **A** | `ariadne.interfaces.cli.local_causal.row_effects_parquet.RowEffectsParquetWriter`、`RowEffectsWriterFactory`、`DeferredRowEffectsSource`、`ValidatedParquetSerializer`を分離。承認後だけbounded rowsを読み、allowlistに従うParquetをG01 `StagingArtifactSink`に渡し、G01 Publisher/Readerが唯一の公開authority | 実効Parquet backend/ABIと各Method列dtype schemaの具体値、実OSでの反復検証、独立セキュリティ試験 |
| **OD-05 / 40 Method Profiles** | **Gate別実装方針** | P1-M06の既存専用3 draft以外の40 Methodは、各担当Gateにstrict Config/Question/Design/Output/Inference profileとpositive/negative fixtureを割り当てる。既決Target/数理の再議決なし。`METHOD_PROFILE_UNAVAILABLE`はfail-closed | 40件のJSON Schemaファイルを今生成したものとはみなさない。Backend effective API/CI、T2/T3/独立Science、真の追加数理判断は当該Gateで固定 |

**OD-04 Gate DAG/36 Pxx** は既承認のままで変更しない。P1-M05を含め全41 Methodを維持する。

## 2. OD-01 科学契約（Owner採用）

- `P1-M05`は`operation=IDENTIFY`, `estimand.family=LATE_COMPLIER`, `population=compliers`, binary treatment contrast `A1−A0`, explicit `design_profile=B0_BINARY_IV`。
- 検証対象：単一binary excluded instrument Z、binary treatment A、outcome Y、追加Cなし、relevance/nonzero first stage、exclusion、independence、monotonicity direction、consistency/SUTVAをEvidence付き設計仮定として宣言。Graphの検証だけで観測不可能な仮定の真偽を証明したと主張しない。
- 正例はDoWhyから取得した、backend-version/API互換性が確認されたIV expressionを保存したconditional typed `IdentificationOutcome`。DoWhyのdefault `nonparametric-ate` labelをそのままLATEとしてcastすることは禁止。`B1`/DRIV/一般ATE/ATT/continuous Z/A/missing designはtyped `METHOD_INCOMPATIBLE`／`IDENTIFICATION_TARGET_UNRESOLVED`。弱IVやfirst-stage診断に問題がある場合、`IDENTIFIED`を点推定・精密なCIの実在へ短絡しない。
- `IDENTIFY`は`identification.json`のtyped ProofとStudy/Status/Manifest/Markerを公開するが、Effect `result.json`は禁止。G08 B0がWald/2SLS/robust ARを所有。DGP-006、NEG-006/007、REF-I03/REF-G01を維持し、追加のinvalid-target/graph/assumption/API負例を要する。

## 3. OD-02 セキュリティ契約（Owner採用）

- Envelope `e11-local-row-export-policy/1`はstrictな`payload`とdetached `signature_ed25519`。**署名対象bytes**は`ASCII('ARIADNE-E11-ROW-POLICY-v1') + [0x00] + RFC8785_JCS(payload)`（`0x00`は区切りのNULバイト1個）。admin-only Trust Anchorにある公開鍵でEd25519署名を検証する。署名bytes自身は署名対象に含めず、Envelope実bytesのSHA256とTrustedRoot内`ContentRef`は別に照合する。
- signed payloadのmandatory fieldsは`policy_version/policy_id/issuer_id/key_id/subject_study_approval_digest/run_id/approved_scope/classification/allowed_columns/max_rows/max_output_bytes/issued_at/expires_at/revocation_epoch`。canonical `subject_study_approval_digest=SHA256(JCS(ValidatedStudy with privacy.policy_ref=null))`と完全な`request_hash=SHA256(JCS(ValidatedStudy including policy_ref))`は異なるHashドメイン。自己参照署名を禁止。
- Admin-only registryは `issuer_id`・`key_id`・`ROW_EFFECT_PARQUET_APPROVER`権限を固定、EUIDが鍵・grant・失効情報を差し替えられない。Issuerのprivate signing keyはCLI/Git/output rootへ置かず、Study由来public keyを信じない。
- 対象run_idとStudy/dataset/Method/scope/lineageを束縛。期限と失効・TrustStore/root/OS Principalの再確認を**row materialization前とstaging seal/publication前**に行う。未認可時にrow bytesを一切生成しない。許可済みstaging後にrevokedなら公開せず隔離する（過去に作られたprivate staging bytesをゼロと主張しない）。
- 行・列・byte bound、root/UID/ACL/mount、Study requestとCLI flagを全件AND。失敗時はexit3、row file無し、stdout/stderr/logへの個票/secret leak無し、要求をaggregateへsilently downgradeしない。
- **Deployment prerequisite:** `independent_approver_role`と`trust_store_admin_owner`の現実の主体、鍵rotation/revocation freshness、信頼可能な時計と対象OS supportを**Owner/運用者が別途指定し実証するまで**row releaseは`BLOCKED_DEPLOYMENT_AUTHORITY`。承認をチャットだけで発行したと扱わない。

## 4. OD-03 Class契約（Owner採用）

| Class/Type | Module/署名 | 不変条件 |
|---|---|---|
| `Ed25519LocalPolicyVerifier` | `ariadne.interfaces.cli.local_causal.policy_verifier`; `__init__(self, *, codec: StrictJcsCodec, clock: TrustedUtcClock)`; `verify(self, *, policy_ref: ContentRef, study: ValidatedStudy, root: TrustedLocalRoot, anchor: TrustedPolicyAnchor) -> VerifiedStudyPolicyEvidence` | Application既存`LocalPolicyVerifierPort`を満たし、preauthorized policyだけを承認。公開署名を複製しない |
| `TrustedPolicyAnchor` | `ariadne.interfaces.cli.local_causal.policy_trust`; admin-backed immutable handle, registry and revocation snapshot from trusted runtime loader | User Path/boolから構築不可。`PolicyTrustAnchor`旧候補と命名を`TrustedPolicyAnchor`に統一 |
| `RowEffectsParquetWriter` | `ariadne.interfaces.cli.local_causal.row_effects_parquet`; `__init__(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int)`; `write(self, *, source: DeferredRowEffectsSource, study: ValidatedStudy, decision: PrivacyDecision, selection: ColumnSelection, sink: StagingArtifactSink) -> ArtifactDescriptor` | `PrivacyDecision`単独は承認署名ではない。trusted UseCaseで検証済みEvidence/Run bindingと同一sinkからのみ使用 |
| `RowEffectsWriterFactory` | same module; `create(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int) -> RowEffectsParquetWriter` | Factoryは署名/承認authorityではない |
| `DeferredRowEffectsSource` | Scientific result/port-side Protocol: `schema() -> ColumnSchema`; `read_rows() -> Iterable[Mapping[str, JsonValue]]` | Row materializationは認可後、scope外の科学Kernel改変不可 |
| `ValidatedParquetSerializer` | CLI adapter-injected Protocol: `encode(self, *, rows: BoundedRowBatch, schema: ApprovedRowSchema) -> bytes` | allowlistのみのordered schema、bounded memory/bytes、NaN/invalid row拒否 |

**Execution:** verified Policy→`LocalPrivacyPolicy.authorize`→`filter_export_columns`→bounded row source（row limit+1 sentinel）→strict schema/size検査→Parquet memory bytes→`StagingArtifactSink.stage_bytes`→G01 LocalPublicationPort.seal/publish→Reader readback。Unknown dtype/column/row identity、超過行/bytes、失効、untrusted root、source identity driftはtyped deny/errorしpartial success無し。

## 5. OD-05 配分とFreeze境界

G02(6)、G03(13)、G04(8)、G06(3)、G07(3)、G08(5)、G09(2) = **40 Method**。G01 P1-M06の3 draftは実装/科学受入済みを意味しない。Method Owner GateのPxxにStrict JSON Schemaの有効な必須項目/制約、Question/Design/Output/Inference、typed negativesと独立Fixture計画を**本文規範として**確定し、MethodRegistryへ明示登録する。用意できないMethodは`METHOD_PROFILE_UNAVAILABLE`でfail-closed。再現/科学計測は07/999が独立に行う。G05はCross-cutting、G10は41件の統合検証でMethodを増やさない。

**Freeze前の保留:** OD-01/02/03の**設計上の採用判断はCLOSED**。残るものは、未作成Method Profile、実効Backend/Parquet環境と科学独立Oracle、独立承認者/key管理者の**実際の任命・配備**、revocation/clock運用値、Method-specific数理の未確定箇所、G08 PREP02-111とDD30_63のAR公式採用履歴整合。いずれも未実施をPASSとしない。

**No implicit authorization:** 本採用はRevised設計/06/07/Pxxの契約更新にのみ有効。Contract Freeze、Coding Authorization、Source/Tests/uv.lock変更、Gate999、個票の現実の配布認可には効力を持たない。旧正本は変更せず、Enhancement worktreeに限る。
