# ENH-E11 G05 P01 — hte_diagnostics

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G05 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G05_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G05_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** CATE support/calibration/uncertaintyと独立事前承認に基づく個票成果物発行を検証する。

**科学/Designの必須制約:** Ed25519独立署名AuthorityとRowEffectsParquetWriter/FactoryのClass契約はOwner採用済み。現実の独立承認者・鍵Store管理者／配備・失効/時計・実OS/Parquet実証は未完了。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。

### 2A. 既存SourceとRow Release authorityの境界（`2cf28f59a324`）
- **既存:** `src/ariadne/product/application/graph_version_service.py`の`GraphVersionService.create(...)`/`fix_graph(...)`はProduct GraphVersion Authorityであり、Local CLIが同名Publisher/Version writerを作って代替しない。`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(input_: EstimationInput, output_dir: Path)`は旧Path API、HTEと認可済Parquet Writerの実装済み証拠ではない。
- **Design-only:** `LocalPrivacyPolicy`の純粋`authorize/filter_export_columns`と、独立承認機関が発行する証拠を検証するVerifier、認可後に初めてrow bytesを生成するParquet Writerは別責務。現在の§3契約のうちAuthorityの署名・Key Owner・Scope・期限・失効・Anti-replay、Row Writer Class/Factory/Methodが**未決**であり、Agentが作成したPolicyRef/bool/CLI flagは認可として無効。承認前のrow materialize/serialize/publishは禁止。`LocalCausalUseCase`・G01 Publisher/Reader/RegistryをG05で複製しない。
- **Freeze blocker:** Row方式/ClassはOwner採用済み。現実の独立Authority/鍵/Trust StoreとG05 06/07/Pxxの再監査・Freeze前に個票Releaseは`BLOCKED_DEPLOYMENT_AUTHORITY`。mockは実認可証拠を代替せず、無断でパスを実装しない。

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
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | Port/Value/Facade integration (no duplicate implementation) | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome |

**Class/Method authority:** 本Pxx §3.1以降に埋め込んだField/Constructor/Public Methodが一次規範。本Gateの主責務はHTE診断/Policy/認可付きWriter/Readerであり、新Scientific Adapterを追加しない。Ed25519独立Verifier／RowEffectsParquetWriter/FactoryはOwner採用済みClassとして責務を守り、実deployment未成立をBLOCKEDとして、Agentが独自署名・鍵・出力方式を創作してはならない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent of external DD)

このPxxの実行に必要なClassのField/Constructor/Method/Process/Failureを以下に内包。外部DDはTraceabilityのみ。現行SourceとのABI差分は開始時に確認し、欠陥ならOwnerレビューに戻す。

### 3.1. `EffectOutcome` — normative implementation contract

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

### 3.2. `InferenceEvidence` — normative implementation contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

### 3.3. `DiagnosticPort` — normative implementation contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.DiagnosticPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...
```

#### 処理仕様

診断結果を型付きで正規化し、未検証Science PASSにしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol自体はI/Oを持たない。Concrete Adapterは本書§3/§4で所有が割り当てられたClassのみが実装し、単一MethodCapabilityPort経由で選択する。validated Request→typed outcome/staging sinkを守り、外部DDを未記載の実装規範の代用としない。Owner/ABIが未確定なら新Facadeを創作せずBLOCKED。

#### 検証

DD-E11-METH-P101〜P313。

## 4. Required implementation — G05/P01 dedicated processing

1. **Entry:** G04 canonical 999 PASS、G05 Frozen06/07/Pxx、Owner Coding Authorization、Source/lock、依存Pxxを確認。G04のEffect/CATE/Graph/Studyが同一Hash/Version/Estimand対象であることを検証。
2. CATE supportはTreatment×X/Wのデータ範囲と推定対象のSupportに基づき、Overlap/Effective Sample/CalibrationとUncertaintyを混同せず別Metric/Statusとして計算。
3. Calibration/Coverage評価は事前指定Holdoutまたは独立SimulationとEstimator/Backendのvalid inferenceに限定。適格な標本数、group size、CI availabilityを記録。
4. G04のCATE Resultを入力として検証し、Method固有nuisanceや数値Estimatorを再実装しない。aggregateだけ返し、G05/P02の独立認可なしに個票値を作らない。
5. **Privacy boundary:** 未承認・技術的失敗・Authority未定はzero-rowでstopし、許可ErrorをError suppressionやdummy Policyで回避しない。G01 Publisher/Readerは再実装しない。Optional Backend/Science Availabilityも分離する。
6. **Output:** Typed Decision/Evidence/Aggregate/Policy-bound Artifactを必要な場合のみStaging→Atomic Publisherへ渡す。既存Product ABIとException/Exit policyを保護する。

### 設計書で定義済みの実装意味論（本Packageの規範）

以下は既存30_62/30_63の設計規則のうち本Packageへ適用する本文内契約である。外部DDを読ませて仕様を補完することは禁止する。自Packageが所有しないClassは再実装しない。

LinearDML/CausalForestDML/DRLearner/ForestDRLearner/S/T/X-Learnerを単にCATEという名称で同等に扱わない。X=effect modifiers、W=confounders、nuisance models、treatment type、target population、crossfitting/final model、backend/versionをper Method Configとする。

- Result Point CATE(x)、Population summary、support/overlap診断を分離し、個票値は明示的に認可されたParquetのみ。Stdoutや小さなJSONへの個票全件混入を禁止。
- Inference RegistryはMethod/Backend/version/final estimator config別に `POINT_ONLY / SUPPORTED_CI / UNSUPPORTED / UNAVAILABLE / FAILED` を判定。Native bootstrapを統計的妥当性確認なしに汎用適用しない。
- Exploratory point-onlyは許すが、Confirmatoryは事前に宣言したtargetに適合するCIと独立Science Evidenceが必要。Pointwise CIとsimultaneous bandを区別する。

`LocalPolicyVerifierPort.verify`は`context.policy_anchor`（Study/CLI入力とは独立のsecure runtime configuration由来）によりStudy・scope・columns・row boundを事前承認した`VerifiedStudyPolicyEvidence`を生成する。Study自身のbool/policy_refは認可証拠ではない。`LocalPrivacyPolicyPort.authorize`の`PrivacyDecision`前に個票bytesをstagingに出力しない。same-UID/private owner-controlled TrustedRootが基準で、shared/CI/container-root可視mountや不明ACL/namespaceはfail-closed。OD-02=Aにより、本EnhancementのRow Exportの署名方式はEd25519／domain-separated RFC8785-JCS、EUIDが改竄不能なadmin-owned Trust Storeと失効検証を用いるとOwner採用済み。ただし現実の独立承認者・鍵Store管理者／実配備・失効freshness/clock/OSが未確認ならrow releaseは`BLOCKED_DEPLOYMENT_AUTHORITY`。

**OD-02/03のEd25519+admin trust-store/RowEffectsParquetWriter方式・署名/ClassはOwner採用済み。実際の独立approver・admin鍵配備/失効freshness/clock/OS・Method別row schema/実Backend/Independent Testが未完なら当該個票Releaseは`BLOCKED_DEPLOYMENT_AUTHORITY`。**

**OD-02/03已採用の必要条件：** G05/P02の`Ed25519LocalPolicyVerifier.verify`でadmin-only authority（not user-owned）によるrun/Study/Method/Policy scopeに束縛された署名を検証し、`LocalPrivacyPolicy.authorize`の前にtrusted Proofを確定。G05/P03`RowEffectsParquetWriter.write`だけが認可後row bytesを作りG01 sinkへ渡す。未配備ならrelease deny、他PackageのHTE集計診断を無根拠に止めない。

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
- CATE supportはTreatment×X/Wのデータ範囲と推定対象のSupportに基づき、Overlap/Effective Sample/CalibrationとUncertaintyを混同せず別Metric/Statusとして計算。 Calibration/Coverage評価は事前指定Holdoutまたは独立SimulationとEstimator/Backendのvalid inferenceに限定。適格な標本数、group size、CI availabilityを記録。 G04のCATE Resultを入力として検証し、Method固有nuisanceや数値Estimatorを再実装しない。aggregateだけ返し、G05/P02の独立認可なしに個票値を作らない。
- Evidenceはpositive/negative、Approval Signature/Expiry/Scope、Effective UID/ACL/mount、row bytes createdか、Parquet/Manifest/Marker/Readback、source/fixture SHAとactual commandを含める。秘密鍵そのものや個票のログ出力は禁止。
- Test側のCollection/Runner実Pathは40の発見規則に従う。未実装Approval Authority/Writerをmockして正規Privacy PASSとしない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03,P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit unresolved design — freeze barrier

**Document independence:** Class Fields/Constructor/Methodは§3、専用処理は§4、検証/負例は§6で完結。Owner決定が無い要件は仮構実装で埋めない。

**BLOCKED before Freeze:** HTE calibration metricとholdout policy/必要Science Oracle、G04推論契約。 これらは本Pxxに係る未確定決定であり、他Pxx/07/設計書を読んで推定してはならない。G05のRow出力をG01〜G04に遡及して許可しない。


## PREP-04.2 / G05 operational closure checkpoint (DRAFT / NOT_FROZEN)

**Already Owner-adopted — no redesign:** OD-02 Ed25519 detached domain-separated RFC8785-JCS + admin-owned non-EUID-writable Trust Anchor; OD-03 exact `Ed25519LocalPolicyVerifier`, `RowEffectsParquetWriter`/`Factory` and `DeferredRowEffectsSource`/`ValidatedParquetSerializer` signatures; G01 alone owns staging/publication/readback. P02 is independent verification (not signing), P03 serializes only after independent authorization; P04 independently verifies the full release boundary. No new G05 Method ID or Product API/DB.

**BLOCKED deployment inputs:** real independent Approver and Trust Store admin principal unassigned; key custody/provisioning/rotation and authentic policy/key revocation source not deployed; approved revocation-snapshot freshness and trusted UTC clock operating bounds unspecified; actual EUID/ACL/mount/FS not verified; Method-specific `ApprovedRowSchema` exact ordered column/dtype/row identity not finalized; effective Parquet and Ed25519 versions/APIs not probed. Freeze can't be declared by a test key or these documentation drafts. See independent operational mapping `combined_review/128_20261121_prep04_2_g05_operational_authority_contract.md`.

**Acceptance invariant:** initial missing/invalid approval ⇒ exit3, zero `DeferredRowEffectsSource.read_rows` and zero new row bytes. Valid approval⇒ bounded ordered allowed rows only→G01 staging; recheck revocation/clock/root pre-stage/seal/publish. After authorized private staging revocation ⇒ no publish, but do not assert historical staged bytes were zero. `row_effects.parquet` restricted, no values in Result/Manifest/stdout/stderr/log; own G01 Reader required. 

**Work boundary:** no numerical timeouts/thresholds, guessed Method columns/dtypes, substituted backend libraries, new signer/Publisher or new scientific target; unresolved values remain explicit Owner/operations blockers. G05 999, Freeze and Coding Authorization NOT_PERFORMED.

**Package-specific PREP-04.2 note:** P01: HTE diagnostic support/calibration/uncertainty is separate from authorized row release. Do not generate RowSource values in diagnostics or grant private row policy. G04 CATE/DRIV Method scientific target/uncertainty must remain authoritative.
