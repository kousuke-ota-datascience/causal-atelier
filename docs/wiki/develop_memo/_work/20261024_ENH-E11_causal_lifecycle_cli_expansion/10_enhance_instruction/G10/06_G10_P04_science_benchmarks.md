# ENH-E11 G10 P04 — science_benchmarks

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G10 / **Package:** P04 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P02,P03  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G10_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G10_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 全41のDGP/NEG/REF、FWER=.05、独立K/R/Compute/coverage/MC-SE。未測定をPASSにしない。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 41 Method/10 UCの有効独立科学証拠を全件照合し、影響分のみ再実行してManifest/依存/旧v2互換を統合する。

**科学/Designの必須制約:** 各GateのScience999を省略しない。GPLの顧客配布時の手動License審査は内部分析Gate外。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 全41のDGP/NEG/REF、FWER=.05、独立K/R/Compute/coverage/MC-SE。未測定をPASSにしない。

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
| `MethodCapabilityRegistry` | `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry` | Port/Value/Facade integration (no duplicate implementation) | describe(method_id) / resolve(method_id,backend_id,profile) / load_adapter(capability) |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence.GraphEvidence` | Port/Value/Facade integration (no duplicate implementation) | from_canonical_json(raw:bytes) / canonical_payload() |

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

`describe`はpure metadata。`resolve`でDistribution metadata、実効API signature/Version、指定Methodの利用可能性・Inference availabilityを検査。`load_adapter`だけがoptional importを実行する。Unavailable時は当該Methodのtyped reasonとし、core起動や旧v2を破壊しない。`pyproject.toml`・universal `uv.lock`・実効runtime/Library versionを記録。SBOMと顧客別Legalは内部Scienceの必須runtime contractでない。

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

`DD-E11-CAP01` ENV-BASE隔離、`CAP02`単独3Backend Profile、`CAP04`Version/unsupported、`CAP05`transitive package有無とMethod選択区別を初期Gate必須とする。`CAP03` Combined API parityは初期Gate対象外（未検証の同時導入をsupportedと呼ばない）。`CAP06` Customer Delivery legal blockedは実際の顧客納入時の手動法務Checkであって内部Science Gateには含めない。

**関連ID:** DD-E11-CAP01〜CAP06、FR-185/194/195/196/197/202、NFR-028〜030/032、AR-034/040、BD01-F08/F09/F12。

### 3.2. `EffectOutcome` — complete Class method protocol

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

### 3.3. `InferenceEvidence` — complete Class method protocol

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

## 4. Required implementation — G10/P04 replay and science boundaries

1. **Entry:** G10 06/07/Pxx Frozen、all required G01〜G09 latest canonical 999 PASS、Owner Coding Authorization、full Source/lock/environment SHA、Pxx checkpointを検証。未成立Gateを仮PASSとして扱わない。
2. 全41 MethodのDGP/NEG/REF/DD/ACをMethod別に追跡する。§5表の記載は計画であり、全Methodの独立oracleが存在/実行されている証拠ではない。
3. T1 deterministic Contract と T2 Pilot、T3 confirmatory Monte Carloを分離。Pilotで効果量/Variance/条件付き排除Ruleを探索してよいがT3のThreshold/seed/Method/Family/K/R/computeを事後調整しない。
4. 多重性は承認済みFWER=0.05を適用し、Method×Outcome familyごとのKと試験棄却率/CI coverage/MC-SEを事前登録。Rが足りない、generator/verifier未固定、compute上限不足ならBLOCKEDでありPASSとしない。
5. DGP true estimand/Graph/Referenceは生成式・独立実装/レビューされた値を真値にし、Backend自己出力や他Agentの同一誤りをOracleにしない。IV/AR・Temporal/PAG・Negative Control・CATE/HTE/Quasi・Privacyは固有の仮定/負例を実測。
6. Gate G01〜G09のcanonical 999を科学証拠の代わりにしない。上流999とFull CandidateのSource/Fixture/Backend/Policy SHA、ScienceStatus/TechnicalStatusを照合し、実施していないMethodを全41 PASSへカウントしない。
7. **Boundaries:** Value/Scientific typed Ports→G01 StagingSink/Atomic Publisher/Readerを使い、CLI専用Scientific Kernel、未承認Row export、old v2破壊、Unknown Backendへのfallbackを禁止。科学的・技術的Statusは独立。
8. **Output/Evidence:** Method/Operation/Version/Backend/Profile/Source/Fixture/Oracle/seed/CI/Privacy/Manifest/Result SHA、実行時のenvironment、negativeとaccepted/rejected Reasonを残す。Independent 07/999は本Packageが代行しない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

- `DD-E11-METH-P101〜P120 / P201〜P208 / P301〜P313`は41 Methodに対応する恒久的な受入義務ID。各Methodについてpositive DGP/独立Reference、negative Scenario、Method×Estimand/Backend/CI、canonical Result/Manifest readback、Product regression影響を検証する。
- 独立検証ではDGP version・seed・Method-specific推論・Monte Carlo SE/Coverage/多重性と適格Run分母を定義する。型・Schema一致は科学的Coverageや識別の証明ではない。
- 顧客に実際に配布する場合は対象PackageのLicenseと配布方式をOwner/法務が手動確認し、未承認の納入を禁止する。内部CLI実行にSBOM生成や受領者別承認管理を要求しない。

参照：[E11 Domain/Ports](30_61_causal_domain_ports.md)、[Execution/Publisher](30_62_local_execution_publication.md)、[CLI Port IF](../23_api_interface_design/23_41_cli_scientific_ports.md)、[Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

**G10/P04は全41 MethodのScienceを再検証し、数値Kernelを再実装しない。**

| Method | DD | DGP/NEG | Ref | AC | Status |
|---|---|---|---|---|---|
| `P1-M01` Native Randomized identification／A | `DD-E11-METH-P101` | DGP-001; NEG-001, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M02` Native Backdoor identification／ATE | `DD-E11-METH-P102` | DGP-002, DGP-021; NEG-002, NEG-003 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M03` DoWhy Backdoor identification／ATE候 | `DD-E11-METH-P103` | DGP-002, DGP-021; NEG-002, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M04` DoWhy Frontdoor identification／ATE | `DD-E11-METH-P104` | DGP-005; NEG-004 | REF-G01, REF-I02 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M05` DoWhy IV identification／B0二値Z/A無調整complier LATE（条件付き識別） | `DD-E11-METH-P105` | DGP-006; NEG-006, NEG-007 | REF-I03, REF-G01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / OWNER_TARGET_ADOPTED_PROFILE_BACKEND_SCIENCE_PENDING / NOT_GENERATED |
| `P1-M06` FCI／PAGと等価類 | `DD-E11-METH-P106` | DGP-011, DGP-021; NEG-003, NEG-021, NEG-028 | REF-G02 | AC-D02, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G01 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P1-M07` Frontdoor two-stage regression／ATE | `DD-E11-METH-P107` | DGP-005; NEG-004, NEG-005 | REF-I02, REF-E04 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M08` Native diff-in-means／ATE | `DD-E11-METH-P108` | DGP-001, DGP-022; NEG-001, NEG-010 | REF-E01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M09` Native OLS／採用済み契約範囲のATE/ATT表現 | `DD-E11-METH-P109` | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020 | REF-E01, REF-I01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M10` Native IPW／ATE・ATT（別fixture） | `DD-E11-METH-P110` | DGP-002, DGP-003; NEG-010, NEG-018 | REF-E02 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M11` Native AIPW／ATE・ATT（別fixture） | `DD-E11-METH-P111` | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012 | REF-E03 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / BLOCKED / NOT_GENERATED |
| `P1-M12` Placebo Treatment refutation／null診 | `DD-E11-METH-P112` | DGP-022; NEG-014 | REF-R01 | AC-D01, AC-R01, AC-T01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M13` Data Subset refutation／安定性 | `DD-E11-METH-P113` | DGP-001, DGP-002; NEG-015 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M14` Random Common Cause refutation／摂動安 | `DD-E11-METH-P114` | DGP-002; NEG-017 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M15` Bootstrap refutation／再標本化安定性 | `DD-E11-METH-P115` | DGP-001, DGP-002; NEG-016 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M16` Adjustment Set Sensitivity／設計変更 | `DD-E11-METH-P116` | DGP-021, DGP-002; NEG-002 | REF-G01, REF-R01 | AC-D01, AC-D02, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M17` Propensity Clipping Sensitivity／tr | `DD-E11-METH-P117` | DGP-002, DGP-023; NEG-010, NEG-018 | REF-E02, REF-R01 | AC-D03, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M18` Observed NCE null diagnostic／条件付き関 | `DD-E11-METH-P118` | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M19` Observed NCO null diagnostic／条件付き関 | `DD-E11-METH-P119` | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M20` OLS partial R² / RV sensitivity／指定 | `DD-E11-METH-P120` | DGP-020; NEG-020 | REF-R03 | AC-D01, AC-D03, AC-R04 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P2-M01` LinearDML／CATE(x) | `DD-E11-METH-P201` | DGP-003; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M02` CausalForestDML／CATE(x) | `DD-E11-METH-P202` | DGP-004; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M03` DRLearner／CATE(x) | `DD-E11-METH-P203` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M04` ForestDRLearner／CATE(x) | `DD-E11-METH-P204` | DGP-004; NEG-010, NEG-011, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M05` S-Learner／CATE(x) | `DD-E11-METH-P205` | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M06` T-Learner／CATE(x) | `DD-E11-METH-P206` | DGP-003, DGP-004; NEG-010, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M07` X-Learner／CATE(x) | `DD-E11-METH-P207` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M08` DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE | `DD-E11-METH-P208` | DGP-008; NEG-009, NEG-012, NEG-013 | REF-E06 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M01` PCMCI／time-lagged graph | `DD-E11-METH-P301` | DGP-009; NEG-021 | REF-G03 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G05 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M02` PCMCI+／time-series CPDAG | `DD-E11-METH-P302` | DGP-009, DGP-010; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P3-M03` LPCMCI／time-series PAG | `DD-E11-METH-P303` | DGP-011; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P3-M04` DiD／初期2×2 ATTのみ（STAGGERED=DEFERRED） | `DD-E11-METH-P304` | DGP-012（初期2×2）, DGP-013（staggered将来／P3-M05別）; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M05` Event Study／event-time効果 | `DD-E11-METH-P305` | DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M06` Interrupted Time Series／介入時点level・事前宣言post-slope・指定horizon効果 | `DD-E11-METH-P306` | DGP-014; NEG-023 | REF-Q02 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M07` Sharp RDD／cutoff局所効果 | `DD-E11-METH-P307` | DGP-015; NEG-023 | REF-Q03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M08` Fuzzy RDD／cutoff局所complier効果 | `DD-E11-METH-P308` | DGP-016; NEG-006, NEG-023 | REF-Q03, REF-I03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M09` Wald ratio／binary Z/A complier LAT | `DD-E11-METH-P309` | DGP-006; NEG-006, NEG-007 | REF-I03, REF-E07 | AC-D03, AC-P01, AC-P03, AC-P05, AC-D07 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M10` B0 just-identified 2SLS／binary Z/A | `DD-E11-METH-P310` | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M11` B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | `DD-E11-METH-P311` | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M12` Synthetic Control／処置単位の時点別反実仮想ギャップ | `DD-E11-METH-P312` | DGP-017; NEG-024 | REF-Q04 | AC-D03, AC-P01, AC-P03, AC-Q04 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED |
| `P3-M13` Synthetic DiD／panel平均介入効果 | `DD-E11-METH-P313` | DGP-018; NEG-024 | REF-Q05 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q05 | PLAN:G09 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Proof boundary:** G10の全41 Methodの§5 DGP/NEG/REF/ACは検証対象であり、Listが存在するだけで実Fixture/Oracle生成済みやScience PASSを意味しない。独立Reference/Generatorを事前固定し、FWER=.05とMethod別K/R/compute/MC-SE/coverageをFreeze前に確定する。未測定はBLOCKEDであり、Backendの出力を真値にしない。


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row ParquetはStudyの`privacy.row_export_requested=true`による単独opt-in、Linux非root実効EUID所有private ext4/XFS root（0700/0600、owner/mode/local ext4-XFS/同一FSを検証）、Method別ApprovedRowSchema/ordered column/row/byte/memory capsに合致する場合だけ、認可後の`RowEffectsParquetWriter`がG01 StagingSinkに遅延生成する。初期denyはexit3/Source反復0/row bytes0。署名鍵・独立承認者・失効はOwner 2026-11-21限定改訂で不要。G01 Publisher/Readerが唯一の公開/readback authority。実FS/Parquet/Method RowSchemaの実測未完はBLOCKED。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer delivery legal acceptance（配布時のみ）を意味しない。

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
- **Target-specific mandatory cases:** 全41 MethodのDGP/NEG/REF/DD/ACをMethod別に追跡する。§5表の記載は計画であり、全Methodの独立oracleが存在/実行されている証拠ではない。 T1 deterministic Contract と T2 Pilot、T3 confirmatory Monte Carloを分離。Pilotで効果量/Variance/条件付き排除Ruleを探索してよいがT3のThreshold/seed/Method/Family/K/R/computeを事後調整しない。 多重性は承認済みFWER=0.05を適用し、Method×Outcome familyごとのKと試験棄却率/CI coverage/MC-SEを事前登録。Rが足りない、generator/verifier未固定、compute上限不足ならBLOCKEDでありPASSとしない。 DGP true estimand/Graph/Referenceは生成式・独立実装/レビューされた値を真値にし、Backend自己出力や他Agentの同一誤りをOracleにしない。IV/AR・Temporal/PAG・Negative Control・CATE/HTE/Quasi・Privacyは固有の仮定/負例を実測。 Gate G01〜G09のcanonical 999を科学証拠の代わりにしない。上流999とFull CandidateのSource/Fixture/Backend/Policy SHA、ScienceStatus/TechnicalStatusを照合し、実施していないMethodを全41 PASSへカウントしない。
- P04は§5の全41 MethodについてDGP/NEG/REF/DDと独立数値/構造Oracleを判定する。P01〜P03/P05はScopeに関係するMethod/Result保護義務を保持し、科学Kernelを再実装しない。
- Actual fixture/Source/lock/Backend/API SHA、Test layer/lifecycle、collected command、Observed/Expected、Quantitative Science K/R/MC-SE、PASS/FAIL/BLOCKED Reasonを記録。未実施をPASSとすることは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P05。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit design/Science/Legal Freeze conditions

Class Fields/Constructors/Public Methodの実行意味は§3、Method固有処理は§4、Method/DD/Science義務は§5〜6に収める。外部DDから不足仕様の推論をCoding Agentに強制しない。**Freeze blockers:** 41 Methodの独立DGP/NEG/REF、FWER family K/R、coverage/MC-SE/Compute、数理退化・point-onlyの定量判定。 OwnerまとめReviewがこれらを判定するまでNo Coding Authorization/No Science PASS/No canonical promotion。

### Owner SIM-01/03/04 initial-Gate simplification (2026-11-21)

Mandatory integration profiles are ENV-BASE, ENV-DOWHY, ENV-ECONML and ENV-TIGRAMITE, each with actual lock/distribution/API smoke and Method-specific science/reproducibility checks. ENV-COMBINED all-extras runtime/CI is an optional later interop check, **not** G10 initial PASS dependency; do NOT claim simultaneous all-extras environment is verified. Local scientific Manifest has NO required `runtime.sbom_ref` or `review.legal_delivery_status` (the active Draft 2020-12 Schema removed them); installed distribution/version/lock source provenance and independent science review evidence remain required. SBOM generation, per-customer authorization state and legal evidence are NOT G10 CLI runtime functionality. Prior to any actual customer external delivery, the Owner/legal reviewer must manually review actual shipped dependencies and block unapproved distribution. FS privacy boundary is ordinary nonroot Linux EUID/private owner-only ext4/XFS root with 0700/0600 and FD-safe paths/same FS; no separate ACL/xattr digest, mount namespace/ID proof or CI/container classification. Preserve G01 Publisher/Reader, NFR-030/031/032/033/035/036, all science, all Method ID targets, upstream Gate999 independence and Product v2. Historical DEC08/PREP02 remains historical, specifically superseded by combined_review/131. No runtime evidence / Gate999 PASS / Coding Authorization.


## S02-01〜08：G10 全Method証拠・差分再実行の正規契約

G10は41 Method全件（P1=20/P2=8/P3=13）の独立DGP/NEG/REF、Method別Schema/Estimand/Inference、Backendとsource+fixture SHA、T2/T3事前登録・FWER=.05、上流999を検証する。**全件を無条件に数値再実行する要求はない**。承認済み独立証拠について、Method code、shared scientific kernel、Method Registry/descriptor/schema、ports/validation、依存コード/ABI、Python/uv.lock/extra/Backend distribution+version、fixture/DGP、negative、Oracle/reference source、seed/quantitative AC/protocol、privacy・Result/Manifestが科学的結果に影響し得る**推移的依存閉包**を監査し、厳密に同一のものだけ再利用する。完全な閉包不変証明が欠損・不整合なら再実行し、再実行不能なら該当MethodをBLOCKしてG10_999 PASSを禁止する。新規/変更された評価指標を既存証拠から事後推測しない。最終Fixed Trial Candidate全体のOperation・Method/Estimand/Inference dispatch、JCS/ContentRef/Manifest/Marker/Reader、G05 Study単独opt-in/Privacy、Product v2互換と横断Negativeは毎回独立に実行する。Libraryのsymbol/API存在はScience PASSではない。

G10-07の最小受入集合：同一full-SHA閉包→上流Science証拠再利用の正例、共有Kernel/Schema/lock/Backend/Fixture/REF/Policyの各1点変更→影響Methodの再実行またはBLOCK、依存グラフに未知辺→BLOCK、既存証拠に欠損/科学的FAIL→全41のPASS禁止、未変更41件のScience真値と後続横断統合別軸検証。旧Productの無関係なSuiteは全件無条件再試験せず、protected境界への影響閉包を証明して必要分を実行する。未知影響なら実行またはBLOCK。G05はStudy trueとnonroot same-UID private ext4/XFS/Method別allowlist・row/byte/memory capsのAND、false/省略は個票なし。署名Verifier・PolicyRef・追加CLI許可Flagは実装しない。現行Local Graphは内容hash/由来、Product Version IDはnull、非対応import拒否。40 Profileは共通Schema＋Method overlayを再構成して厳格検証し、未登録/未試験はfail-closed。外販向けLicense Governance NFR-034はDEFERREDだが社内OSS義務は継続。Coding Authorization未発行、B04/B05の実効証拠は未取得。

## S09-R12 P3-M06 ITS output integration invariant (2026-11-22; DRAFT)

P3-M06 output is Method-config dependent: `effect_components=LEVEL` publishes scalar β_L and typed `its_components.json`; `LEVEL_AND_SLOPE` has a non-scalar Result point with `NON_SCALAR_TARGET` and the same typed sidecar carrying β_L, β_S and only explicitly predeclared horizon effects `β_L+hβ_S`. Both must match the current strict P3-M06 Output Profile/Descriptor catalog and the `e11_its_components_draft1.schema.json` draft. G10 must not drop the sidecar when rebuilding the 41-Method Operation/Result/Manifest matrix; preserve checksum/Study/Design/Method identity, request-mode/Status consistency, and independent DGP-014/NEG-023 science tests. Tested marginal HAC intervals do not automatically certify joint level+slope coverage. No arbitrary default horizon, no observed row leakage, no new public wire.

**This package:** P04 verifies independent numerical component truth, explicit horizon arithmetic and covariance eligibility.

## DEC-S09-P3M04-01 Owner A — G10 cross-Gate capability reconciliation (2026-11-22)

Owner DEC-S09-P3M04-01=A: P3-M04 initial 2×2 DiD ATT is the sole executable positive variant (`design_variant=DID_2X2`) when separately scientifically/backend eligible. `STAGGERED` remains a syntactically recognized but `DEFERRED` future capability. The Method-specific scientific preflight must reject STAGGERED as `SCIENCE_CONTRACT_NOT_AVAILABLE` / `CAPABILITY_UNAVAILABLE` (CLI exit4), never estimating, publishing a successful Effect Result/Manifest or silently falling back to DID_2X2, TWFE or P3-M05. Unknown/malformed variant is validation exit2. The 41-Method count stays unchanged. The G10 41-Method evidence matrix requires independent valid science for P3-M04 DID_2X2 and the deferred-variant negative, **not** a staggered ATT(g,t) executable positive. DGP-013 remains mandatory where applicable to P3-M05, but not as positive P3-M04 STAGGERED. Existing G10 transitive-closure evidence reuse rules remain unchanged.

**Package-scoped action:** P04 verifies independent DGP-012/REF-Q01 science and the STAGGERED refusal negative; do not count DGP-013 STAGGERED as accepted.
