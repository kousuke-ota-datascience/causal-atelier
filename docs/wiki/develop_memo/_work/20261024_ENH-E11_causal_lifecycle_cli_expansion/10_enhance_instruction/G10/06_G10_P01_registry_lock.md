# ENH-E11 G10 P01 — registry_lock

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G10 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G10_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G10_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 41 Method registryと5 Environment profile、uv.lock/effective API/optional extras/SBOMと配布制約を検査。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 41 Method/10 UCの再実行・Manifest/依存・科学証拠・旧v2互換を統合する。

**科学/Designの必須制約:** 各GateのScience999を省略しない。GPLの顧客個別License判断は別。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 41 Method registryと5 Environment profile、uv.lock/effective API/optional extras/SBOMと配布制約を検査。

### 2A. 41 Method横断Reuseと既存ABIの実在確認（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter`は`run_discovery(DiscoveryInput, Path)`、`run_identification(IdentificationInput, Path)`、`run_estimation(EstimationInput, Path)`、`run_refutation(RefutationInput, Path)`、`run_sensitivity(SensitivityInput, Path)`の公開ABI（返値はいずれも`list[ScientificResultDescriptor]`）。対応実体は`scientific/discovery|identification|inference|refutation|sensitivity/adapter.py`の各`run(input_, output_dir)`。これらは旧Product Path APIであり、E11の`Discovery/Identification/Estimator/DiagnosticPort`のtyped Request/Outcomeとは互換性を自動仮定しない。
- **横断責務:** G10は41 Method×Operation/Estimand/Backend/Result/Manifest/Licenseの再実行と統合検証を所有するが、科学計算Kernel、G01 Registry、GraphVersion writer、Publisher、Reader、G05独立Privacy Authorityを複製しない。旧ABI・Product v2を変更せず、既存upstream Gateの同一Class・Method profileを参照する。Sourceに存在しないE11新規Classを「導入済み」と呼ばない。
- **科学的Boundary:** G10の横断テストには全41 MethodのDGP/NEG/独立REF、実効Backend/lock/fixture/SBOM SHA、Source/Environment/seed、preregistered K/R/MC-SE/coverage/threshold、FWER=.05とMethod別Inference profileが必要。未決は該当MethodのBLOCKED、G10全体のGate PASS禁止。

### 2B. Standalone Operation/Result/Manifest契約
| Operation | 必須Artifact | 禁止・Negative |
|---|---|---|
| DISCOVER | `study.json`・`status.json`・Graph成功なら`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`と理由必須、`schema_dispatch.graph=null`。Backend失敗との混同禁止 |
| IDENTIFY | `study.json`・`status.json`・`identification.json` | Effect `result.json`禁止。非識別もtypedでGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`・`status.json`・`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、科学PASSと混同禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`・`status.json`・`diagnostics.json` | Effectの再発行禁止、元Effect/Graph/Design hash、seed/適用条件の照合 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）、ただし両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key、実bytes SHA256/size/MediaType/Privacyを網羅。 `request_hash=SHA256(JCS(validated typed Study JSON))`。Manifestに自己hashを格納せず、Markerの`manifest_sha256`にManifest実bytes hashを保存。ReaderはMarker→Manifest→実File→Operation/Profile→上流hashをTrustedRootで検証し、一致しない未コミット/破損データを拒否。Outputは既存G01のStaging→同一FS atomic no-clobber publish、個票bytesはG05のStudy＋CLI二重opt-in/OS適格性確認以前に生成禁止。各Methodのpoint/uncertainty/science_acceptance/statusを別軸で保持し、計算成功はScience PASSでない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `MethodCapabilityRegistry` | `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry` | Port/Value/Facade integration (no duplicate implementation) | describe(method_id) / resolve(method_id,backend_id,profile) / load_adapter(capability) |
| `BackendCapabilityRecord` | `ariadne.scientific.capabilities.BackendCapabilityRecord` | Port/Value/Facade integration (no duplicate implementation) | check(self,request:ValidatedCapabilityRequest) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降に埋め込んだClass Field/Constructor/Public Methodが実装の一次規範。外部DDは履歴/Provenanceのみであり、unknown Concrete型/Backend/Runtime値を補完しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent source)

以下のInstance Fields/Constructor/Method/Failureは本Packageの規範。外部DD参照はProvenanceのみ。Designed Classが実在する証拠ではないのでSource/ABIを実行時検証する。

### 3.1. `MethodCapabilityRegistry` — complete Class method protocol

#### 識別情報・責務

- **Class:** `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。Product ScientificCoreAdapterとは別契約である。
- **責務:** 41 Method IDごとのOperation/Estimand/Eligibility/Inference/Backend/Profileをstrictに選択し、Version/API capabilityを検証し、Adapter importを遅延させる。外部Libraryの既定推論を黙認しない。
- **責務外:** Estimator計算、Local FS publication、Customer Delivery LegalのPASS。
- **関連契約:** 30_63 Method41 allocation、23_41 §6〜7。

#### フィールド

配置：`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。Method IDごとにOperation、Estimand Family、Design/Eligibility、Backend ID、推論方式、Profile/Extra、Adapter Factoryを宣言。外部libraryはresolution後にlazy import。Methodが同じでも対象Estimand・inference configが異なれば別個の互換性判断を要する。

| Field | Type | 生成元 | 可変性／制約 |
| --- | --- | --- | --- |
| `descriptors` | `Mapping[str, MethodDescriptor]` | pinned Method41 Registry | Immutable; Method ID unique; target Estimand/Inference explicit |
| `backend_factories` | `Mapping[str, AdapterFactory]` | composition root | Immutable; import lazy; only eligible Method/Profile |
| `effective_env` | `RuntimeEnvironmentPort` | runtime injection | Observed installed version/API; no fake availability |
| `inference_registry` | `InferenceRegistry` | fixed Method-specific policy | Immutable, point-only vs confirmatory separated |

#### Constructor / Factory

- **Constructor:** `__init__(self, descriptors, backend_factories, effective_env, inference_registry)`. Validate unique IDs, declared Operation/Estimand and versioned descriptor schema; do not import optional modules.
- **Factory** is a collaborator of Registry; 独立実装を置く場合も 独立Factoryを設ける場合も同じMethod×Backend×Inference不変条件に従う。
- **Failure:** Invalid registry/duplicate ID/unsupported policy fails during preflight without selecting unrelated Method or importing missing Backend.

#### メソッド

~~~python
def describe(self, method_id: str) -> MethodDescriptor: ...
def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord: ...
def load_adapter(self, capability: BackendCapabilityRecord) -> ScientificAdapter: ...
~~~

`describe`はpure metadata。`resolve`でDistribution metadata、実効API signature/Version、指定Methodの利用可能性・Inference availabilityを検査。`load_adapter`だけがoptional importを実行する。Unavailable時は当該Methodのtyped reasonとし、core起動や旧v2を破壊しない。`pyproject.toml`・universal `uv.lock`・実効runtime・SBOM・Legalは別軸で記録。

| Method | Observable contract | Side effects / exceptions |
| --- | --- | --- |
| `describe(method_id)` | pinned descriptor | pure; unknown ID typed rejection |
| `resolve(method_id, backend_id, profile)` | effective Capability Record | inspect distribution/API/version; unavailable reason, never auto fallback |
| `load_adapter(capability)` | scientifically eligible Adapter | only this method may lazy import; import failure localized as capability error |

#### 処理仕様

1. Resolve declared Method ID and operation/estimand eligibility from frozen descriptor.
2. Check profile/extras and **effective installed distribution+API version**, not just `pyproject.toml` declaration.
3. Check Method-specific inference availability for requested analysis_mode. Backend default is not evidence of valid CI.
4. Return typed supported/unavailable/unsupported with reasons. Only eligible selected capability permits actual lazy import; never fallback to other Method.
5. Export effective config/version/seed/algorithm facts for Manifest, not a pre-run Science PASS.

#### I/O・連携・失敗処理

- **Input:** MethodRequest, Backend ID/Profile, versioned method descriptors, effective runtime probe.
- **Output:** `MethodDescriptor`, `BackendCapabilityRecord`, `ScientificAdapter` only after eligibility; external estimator objects never enter Domain persistence.
- **No DB/FS mutation** from `describe`/`resolve`; `load_adapter` may import optional modules.
- **Errors:** unknown method, incompatible estimand/inference, missing extra, incompatible API signature, import failure. Each is typed and does not disable core or legacy v2 startup. Combined env/BLAS conflicts are not silently ignored.

#### 検証

`DD-E11-CAP01`ENV-BASE隔離、`CAP02`単独3Profile、`CAP03`Combined API parity、`CAP04`Versionとunsupported mode、`CAP05`transitive package有無とMethod選択区別、`CAP06`Customer Delivery legal blocked。

**関連ID:** DD-E11-CAP01〜CAP06、FR-185/194/195/196/197/202、NFR-028〜030/032、AR-034/040、BD01-F08/F09/F12。

### 3.2. `BackendCapabilityRecord` — complete Class method protocol

#### 識別情報・責務

**Class / module:** `ariadne.scientific.capabilities.BackendCapabilityRecord`（Runtime能力値としてScientific層が所有）。実効Backend適格性の証拠を保持し、silent fallbackを禁止する。

#### フィールド

| Field | 制約 |
|---|---|
| `method_id, backend_id` | 明示指定した組 |
| `distribution_version, adapter_version, api_signature_hash` | 観測された実効版とAPI |
| `extra, profile` | effective environment/profile |
| `available, reason` | boolと欠落時のtyped reason |

#### Constructor / Factory

Constructorは観測証拠から作成。未実測値を使用可能とするdefault/fallback禁止。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `check(self, request: ValidatedCapabilityRequest)` | typed compatibility decision | version/Method/API/Inference照合 | unsupported/unavailable typed reason |

#### 処理仕様

静的Registryと実効Probeから指定Methodと推論方式の可用性を検証。Probeの取得はConcrete Registry/Runtime Port側で行い、Value自身がoptional Backendをimportしない。`load_adapter`時だけBackend import可能。

#### I/O・連携・失敗処理

RecordはI/Oなし。Runtime probe、distribution inspection、optional importは30_62のCapability Registryと30_63のAdapter実装の責務。

#### 検証

`DD-E11-EFF03` version/API mismatch、`DD-E11-CAP01〜06` profile isolation/inference availability、no silent fallback。

**能力の単一Authority：** `ariadne.scientific.capabilities.BackendCapabilityRecord`が実効Distribution/API/probeを表現し、`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`がMethod×Estimand×Inferenceの唯一のRegistryになる。Productの既存`ESTIMATOR_CAPABILITIES`を独立した二重Rules表にしない。

## 4. Required implementation — G10/P01 replay and science boundaries

1. **Entry:** G10 06/07/Pxx Frozen、all required G01〜G09 latest canonical 999 PASS、Owner Coding Authorization、full Source/lock/environment SHA、Pxx checkpointを検証。未成立Gateを仮PASSとして扱わない。
2. 41 MethodのMethod ID/operation/estimand/backend/profile/method-schema/inference availability/versionをMethodCapabilityRegistryのsingle ownerへ登録し、StageRunnerRegistryやCLI専用の第2 Registryを作らない。
3. 各optional Backendの実効installed distribution/API/signature、extra/lock/profile/licenseをProbeし、未導入は該当Method unavailableで全Ariadneのimport/startupを壊さない。
4. 変更がある場合はMethod DescriptorのSchema Hashと実行Audit Evidenceを更新し、Version/Operation/Estimand/Inferenceの一致しないMatchはtyped reject。G01〜G09 Methodに新たな数理Kernelを作らない。
5. **Boundaries:** Value/Scientific typed Ports→G01 StagingSink/Atomic Publisher/Readerを使い、CLI専用Scientific Kernel、未承認Row export、old v2破壊、Unknown Backendへのfallbackを禁止。科学的・技術的Statusは独立。
6. **Output/Evidence:** Method/Operation/Version/Backend/Profile/Source/Fixture/Oracle/seed/CI/Privacy/Manifest/Result SHA、実行時のenvironment、negativeとaccepted/rejected Reasonを残す。Independent 07/999は本Packageが代行しない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

41 Method IDは固定Catalog識別子であり、各IDにOperation、Estimand、Backend/Profile、Method Config Schema、Question/Design Evidence Profile、Inference Policy、Output Artifact Profileを登録する。Class割当があることだけでは実行可能性を意味しない。`ValidatedMethodRequest`は登録済みstrict Method Schemaとcross-asset semantic Validatorの双方に成功した場合のみFactoryから生成する。

P1-M06は`e11_p1_m06_fci_method_config_v1.schema.json`、専用Question/Design internal profilesを使用する。他のMethodについてconfig/profile未定義のまま`config={}`やBackend defaultで通すことを禁止し、`METHOD_PROFILE_UNAVAILABLE`等のtyped reasonでfail-closedにする。各Method提供前に対応Gateで正規Schema、条件付き必須項目、negative fixturesを確定し登録する。Gate IDはSchema dispatchのキーにしない。

公開`MethodCapabilityPort.resolve(request:ValidatedCapabilityRequest)`はOperation/Estimand/Inference/Designを含む要求を厳格検証し、整合が確認できたMethod/Backend/ProfileだけをConcrete `MethodCapabilityRegistry.resolve(method_id,backend_id,profile)`へ委譲するFacadeである。Method ID/Backend/Profileの3値だけから要求全体の適格性を推測してはならない。`describe`はpure、`resolve`は実効Distribution/APIを検査、`load_adapter`だけがoptional importを行う。互換検証とfallback禁止の規則を2系統に複製しない。

**Adapter dispatch：** `MethodCapabilityPort.resolve`はConcrete `MethodCapabilityRegistry`の単一metadata/Runtime probeを使い、`BackendCapabilityRecord`をValidated Requestに付与する。各Scientific Port Concreteは同じRegistryの`load_adapter(capability)`を利用する。UseCaseが任意のBackend objectを受け取らず、`LocalCausalUseCase.run → MethodCapabilityPort.resolve → DiscoveryPort.discover → FciDiscoveryAdapter.execute`を唯一のG01実行経路にする。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row ParquetはStudy個票要求とCLI flagのdouble opt-in、Linux非root実効EUID所有private ext4/XFS root（0700/0600、ACL/mount/namespace/同一FSを検証）、Method別ApprovedRowSchema/ordered column/row/byte/memory capsに合致する場合だけ、認可後の`RowEffectsParquetWriter`がG01 StagingSinkに遅延生成する。初期denyはexit3/Source反復0/row bytes0。署名鍵・独立承認者・失効はOwner 2026-11-21限定改訂で不要。G01 Publisher/Readerが唯一の公開/readback authority。実FS/Parquet/Method RowSchemaの実測未完はBLOCKED。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer LegalのPASSを意味しない。

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
- **Target-specific mandatory cases:** 41 MethodのMethod ID/operation/estimand/backend/profile/method-schema/inference availability/versionをMethodCapabilityRegistryのsingle ownerへ登録し、StageRunnerRegistryやCLI専用の第2 Registryを作らない。 各optional Backendの実効installed distribution/API/signature、extra/lock/profile/licenseをProbeし、未導入は該当Method unavailableで全Ariadneのimport/startupを壊さない。 変更がある場合はMethod DescriptorのSchema Hashと実行Audit Evidenceを更新し、Version/Operation/Estimand/Inferenceの一致しないMatchはtyped reject。G01〜G09 Methodに新たな数理Kernelを作らない。
- P04は§5の全41 MethodについてDGP/NEG/REF/DDと独立数値/構造Oracleを判定する。P01〜P03/P05はScopeに関係するMethod/Result保護義務を保持し、科学Kernelを再実装しない。
- Actual fixture/Source/lock/Backend/API/SBOM SHA、Test layer/lifecycle、collected command、Observed/Expected、Quantitative Science K/R/MC-SE、PASS/FAIL/BLOCKED Reasonを記録。未実施をPASSとすることは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P02,P03。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit design/Science/Legal Freeze conditions

Class Fields/Constructors/Public Methodの実行意味は§3、Method固有処理は§4、Method/DD/Science義務は§5〜6に収める。外部DDから不足仕様の推論をCoding Agentに強制しない。**Freeze blockers:** 41 Methodごとのstrict config schemas、選択ProfileでのBackend実効API、Version+License/Dependency policy。 OwnerまとめReviewがこれらを判定するまでNo Coding Authorization/No Science PASS/No canonical promotion。
