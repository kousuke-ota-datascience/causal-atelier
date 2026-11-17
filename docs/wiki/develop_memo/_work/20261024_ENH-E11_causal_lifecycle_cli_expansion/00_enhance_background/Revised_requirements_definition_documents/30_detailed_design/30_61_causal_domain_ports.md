# 30_61_causal_domain_ports

---

## 1. Content Reference Value

### 1.1. `ContentRef`

#### 1.1.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.references.ContentRef`。immutable value object。Dataset・Question・Design・Graph・Identification等の内容参照を識別し、物理bytesの検証結果を**保持しない**。外部絶対pathやaccess tokenを保存しない。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 1.1.2. フィールド

| Field | Python型 | 必須/default | 制約 |
|---|---|---|---|
| `identity` | `str` | 必須 | 非空の論理identity |
| `relative_key` | `str` | 必須 | safe relative POSIX key。絶対・dotdot・NUL・drive等を拒否 |
| `sha256` | `str` | 必須 | 完成ファイル実bytesのSHA256小文字hex64 |
| `media_type` | `str` | 必須 | Schema/Readerとの整合必須 |
| `schema_version` | `str|None` | 必須／nullable | unknown versionを無条件に推測しない |

#### 1.1.3. Constructor / Factory

`from_payload(payload: Mapping[str, JsonValue]) -> ContentRef`（設計上のFactory）。strict key／型／hash文字種／relative pathを検査。invalid payloadは型付きvalidation error。mutableな入力Mappingを保持しない。

#### 1.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_payload(payload: Mapping[str, JsonValue])` | `ContentRef` | strict parse; I/Oなし | Schema／relative-key／digest validation error |

#### 1.1.5. 処理仕様

Pathの文法検査は実filesystem参照の安全性証明ではない。dotdot、absolute path、drive letter、NUL、backslash区切り混在、不正Unicode正規化を拒否し、HashはコンテンツIDと別に保持。

#### 1.1.6. I/O・連携・失敗処理

I/Oなし。Root閉じ込めとTOCTOUの防止、same-fd bytes hashは`ContentReferencePort.verify`の実装責務。Transaction/Retry/Rollbackは該当しない（immutable value）。

#### 1.1.7. 検証

`DD-E11-REF01`有効Ref、`REF02` traversal/symlink/race、`REF03` input差替え/TOCTOU、`REF04` metadata-only同ID別bytes拒否。FR-185、NFR-029/031。

## 2. Causal Study Value

### 2.1. `LocalStudySpec`

#### 2.1.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.study.LocalStudySpec`。Operation、Method、Estimand、Input refs、Inference、Privacy要求を保持するimmutable Domain Value。Parse/FS I/O/Backend呼出しは責務外。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 2.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `schema_version` | `Literal["e11-local-study/1"]` | 既存v2へのfallback禁止 |
| `run_id, operation, analysis_mode` | `str, LocalOperation, AnalysisMode` | safe run ID・enum |
| `question, design, dataset` | `ContentRef` | Operationごとの必須性をvalidate |
| `graph, identification` | `ContentRef|None` | DISCOVERで未生成参照を要求しない |
| `estimand, method, inference` | `EstimandRef, MethodRequest, InferenceRequest` | Operation×Method×Target整合 |
| `randomness, privacy` | `RandomnessSpec, LocalPrivacySpec` | seedおよび行出力要求を明示 |

#### 2.1.3. Constructor / Factory

ValidatedStudy生成はStrict Decoder/Validatorを経由する。直接constructorまたはfactoryで型・必須フィールド・Operationの整合を検査する必要があり、単なるdataclass生成を`ValidatedStudy`の証明としない。

#### 2.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_local_invariants(self)` | `tuple[Reason,...]` | pure Operation/Method/Target/Privacy検査 | 実行不適格理由を列挙 |

#### 2.1.5. 処理仕様

`DISCOVER`は探索Target `{family:GRAPH_STRUCTURE,population:OBSERVED_VARIABLES,contrast:NOT_APPLICABLE}`をタグ付き非Effect値として扱い、ATE/ATTを偽造しない。`ESTIMATE`等のEffect Operationには効果Estimandと適格なIdentification参照が必要。

#### 2.1.6. I/O・連携・失敗処理

I/Oなし。Studyの意味射影をcanonical encodingしたbytesからrequest hashを作り、Codec versionをManifestで追跡する。Hashは物理File参照とは区別。

#### 2.1.7. 検証

`DD-E11-SPEC01` strict valid/schema、`SPEC02` legacy dispatch、`SPEC03` confirmatory/inference、`SPEC04` Method/Estimand mismatch。FR-185/201、AR-034、NFR-029/036。

## 3. Causal Graph Value

### 3.1. `GraphEvidence`

#### 3.1.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.graph.GraphEvidence`。PAG/CPDAG/DAG等のGraphとprovenance/Versionを保持するimmutable Value。`GraphVersion`はこの設計では**Version関連フィールドとrevision操作の概念**であり、単独のClassを別途定義したとは解釈しない。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 3.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `kind` | `GraphKind` | DAG/CPDAG/PAG等の区別 |
| `nodes` | `tuple[Node,...]` | unique identity |
| `edges` | `tuple[EndpointEdge,...]` | endpoint/lag/identityをlossless |
| `temporal` | `TemporalConvention|None` | lagの符号・基準時刻 |
| `version_id, parent_version_id` | `str, str|None` | immutable provenance chain |
| `provenance, content_hash` | `GraphProvenance, str` | Graph意味射影に一致するdigest |

#### 3.1.3. Constructor / Factory

`from_canonical_json(raw:bytes)->GraphEvidence`：strict Graph Schema＋意味Validator。不可逆PAG→DAG変換、未知node/endpoint/重複edge/lag規約欠落を拒否。

#### 3.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_canonical_json(raw:bytes)` | `GraphEvidence` | pure strict graph decode | schema、endpoint、lag、hash不整合 |
| `make_revision(edit:GraphEdit,rationale:str,assumptions:tuple[str,...])` | `GraphEvidence` | 元Graph不変で新Version生成 | missing rationale / incompatible edit |
| `canonical_payload()` | `Mapping[str,JsonValue]` | lossless domain serialization | invalid/incomplete Graph |

#### 3.1.5. 処理仕様

`EndpointEdge(source,target,source_mark,target_mark,lag)`のmarkはTAIL/ARROW/CIRCLE。Node順序を反転する場合はendpointも対応させる。PAGのbidirected/circleをDAGへ暗黙確定しない。FIXEDは編集状態であってScientific Truthではない。未確定GraphからのEffect識別は独立のEstimand別識別証拠を要求。

#### 3.1.6. I/O・連携・失敗処理

Graph Valueの純粋操作はI/Oなし。内部`content_hash=SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256=SHA256(完成Graph File実bytes)`を**別々に検証**。Version revisionは元Versionを上書きしない。

#### 3.1.7. 検証

`DD-E11-GRAPH01` FCI PAG circle/arrow/bidirected、`GRAPH02` PCMCI lag、`GRAPH03` silent PAG→DAG拒否、`GRAPH04` Version/再識別。FR-186/196、AR-028/036/043。

## 4. Identification / Estimation Request Values

### 4.1. `IdentificationOutcome`

#### 4.1.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.identification.IdentificationOutcome`。識別状態・対象Estimand・Proof・lineageを保持するValue。DoWhy内部ラベルをDomainの推定対象と混同しない。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 4.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `identification_id` | immutable identity |
| `estimand` | `EstimandRef`。B0/B1/DRIV等の区別 |
| `status` | `IdentificationStatus`。nonidentified/review/partialを型付け |
| `strategy, proof` | Strategy、`IdentificationProof|None` |
| `upstream, reasons` | `UpstreamHashSet, tuple[ScientificReason,...]` |

#### 4.1.3. Constructor / Factory

`from_adapter(raw:AdapterIdentification)->IdentificationOutcome`。BackendのStatus、assumption、GraphVersion、Estimand、Upstreamを意味検証して正規化。未提供Proofを生成しない。

#### 4.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_adapter(raw:AdapterIdentification)` | `IdentificationOutcome` | pure status/proof normalization | proof/estimand/upstream不整合 |

#### 4.1.5. 処理仕様

`NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED`を点推定許可へ自動昇格しない。緩和可能な列挙WARNだけに理由付きoverrideを許可。

#### 4.1.6. I/O・連携・失敗処理

外部I/Oなし。実際のBackend識別計算は`IdentificationPort`、Proof/File readbackは別Port。Retry/RollbackはN/A。

#### 4.1.7. 検証

`DD-E11-ID01` B0/B1/DRIV mislabel、`ID02` lineage差、`ID03` nonidentified override拒否、`ID04` GraphVersion再識別。FR-187/194/199、AR-029/039/043。

### 4.2. `EstimatorRequest`

#### 4.2.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.identification.EstimatorRequest`。Identification proofが適格な場合だけEstimatorへ渡すRequest Value。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 4.2.2. フィールド

| Field | Type・制約 |
|---|---|
| `method_id, estimand_family` | Method×target一致 |
| `identification_ref` | 上流証拠参照 |
| `question/design/graph/dataset_hashes` | 完全な上流digest集合 |
| `method_config, inference_request` | Method/Inference適格なtyped config |

#### 4.2.3. Constructor / Factory

`assert_eligible(...)->ValidatedEstimatorRequest`は入力と上流証拠を照合する型付きvalidator。Validation前の生RequestをAdapterへ送らない。

#### 4.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `assert_eligible(identification:IdentificationOutcome,design:CausalDesignEvidence,capability:BackendCapability)` | `ValidatedEstimatorRequest` | pure eligibility check | scientific negative / schema validation区別 |

#### 4.2.5. 処理仕様

Method-specific assumptions、Mediator/Instrument/support、Data Eligibility、Graph/Design/Question/Dataset hash全一致、CI要求を検証。不適格は`ScientificNegativeOutcome`としてBackend未呼出。Path/schema mismatchはtechnical validationとする。

#### 4.2.6. I/O・連携・失敗処理

Value自身はI/Oなし。実Estimator I/O/Artifactは`EstimatorPort.estimate(...,sink)`を通す。

#### 4.2.7. 検証

`DD-E11-ID01〜04`およびMethod固有Negative Tests。

## 5. Inference Values

### 5.1. `ARConfidenceSet`

#### 5.1.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.effect.ARConfidenceSet`。Anderson–Rubin反転の損失ない数学集合を表すValue。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 5.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `confidence_level` | `float` | 0 < level < 1 |
| `components` | `tuple[ExtendedRealInterval,...]` | EMPTYは0件。finite/±∞をtagged endpointsで表現 |
| `topology` | `SetTopology` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED |
| `inversion_evidence` | `ContentRef` | 成功した数学的反転の証拠 |

#### 5.1.3. Constructor / Factory

`from_components(level,components,evidence)->ARConfidenceSet`：finite endpoint、順序、open/closed、重複/接触区間の数学的正規化。

#### 5.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_components(level,components,evidence)` | `ARConfidenceSet` | pure set normalization | invalid endpoint/topology |
| `contains(beta:float)` | `bool` | endpoint条件で判定 | NaN/invalid β |
| `to_payload() / from_payload(payload)` | JSON / Value | Lossless roundtrip | malformed topology / JSON非有限数値 |

#### 5.1.5. 処理仕様

Topology分類はEMPTY→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDED。ALL_REALは(-∞,+∞)一成分。∞端点はopen、双方openで接触する2区間は1点gapを残すため結合しない。数学的EMPTYは`AVAILABLE + inversion_evidence`と両立、計算失敗`FAILED+reason`とは別。B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件が成立する場合`T_AR(βhat)=0`により非空が必要となり、**Method別validator**でEMPTYを拒否。

#### 5.1.6. I/O・連携・失敗処理

Valueはpure。JSONのNaN/Infinity数値は禁止、tagged endpointで表現。実AR反転・HC1・coverageはMethod Adapterと独立科学検証に委譲。

#### 5.1.7. 検証

`DD-E11-AR01` 5分類、`AR02` generic EMPTYとjust-identified条件分離、`AR03` lossless roundtrip、`AR04` null reason、`AR05` confirmatory fail-closed。FR-202、AR-040、NFR-036。

### 5.2. `InferenceEvidence`

#### 5.2.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.effect.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 5.2.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### 5.2.3. Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### 5.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 5.2.5. 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### 5.2.6. I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 5.2.7. 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

## 6. Effect / Backend Evidence Values

### 6.1. `EffectOutcome`

#### 6.1.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.effect.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 6.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics` | `tuple[DiagnosticRef,...]`。Method別typed診断参照 |
| `method_evidence, upstream_hashes` | typed Backend evidenceとlineage |

#### 6.1.3. Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### 6.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_canonical_result()` | typed Result payload | pure versioned encoding | incompatible schema/estimand |

#### 6.1.5. 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### 6.1.6. I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 6.1.7. 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。

### 6.2. `BackendCapabilityRecord`

#### 6.2.1. 識別情報・責務

**Class / candidate module:** `causal.local_contract.effect.BackendCapabilityRecord`（論理所属は実装前にPort/Registryとの依存方向を照合する）。実効Backend適格性の証拠を保持し、silent fallbackを禁止する。**PROPOSED（未実装）。配置先は既存Domainとの統合判断まで暫定。**

#### 6.2.2. フィールド

| Field | 制約 |
|---|---|
| `method_id, backend_id` | 明示指定した組 |
| `distribution_version, adapter_version, api_signature_hash` | 観測された実効版とAPI |
| `extra, profile` | effective environment/profile |
| `available, reason` | boolと欠落時のtyped reason |

#### 6.2.3. Constructor / Factory

Constructorは観測証拠から作成。未実測値を使用可能とするdefault/fallback禁止。

#### 6.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `check(request)` | typed compatibility decision | version/Method/API/Inference照合 | unsupported/unavailable typed reason |

#### 6.2.5. 処理仕様

静的Registryと実効Probeから指定Methodと推論方式の可用性を検証。Probeの取得はConcrete Registry/Runtime Port側で行い、Value自身がoptional Backendをimportしない。`load_adapter`時だけBackend import可能。

#### 6.2.6. I/O・連携・失敗処理

RecordはI/Oなし。Runtime probe、distribution inspection、optional importは30_62のCapability Registryと30_63のAdapter実装の責務。

#### 6.2.7. 検証

`DD-E11-EFF03` version/API mismatch、`DD-E11-CAP01〜06` profile isolation/inference availability、no silent fallback。

## 7. Scientific Ports

### 7.1. `IdentificationPort`

#### 7.1.1. 識別情報・責務

`causal` Domainの科学的Protocol。**PROPOSED**。現行`ScientificCorePort`とのreuse/extension要否を既存コード基準で判定し、CLIだけを理由に重複Portを作らない。

#### 7.1.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 7.1.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 7.1.4. メソッド

```python
class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...
```

#### 7.1.5. 処理仕様

IdentificationとEvidenceの意味を守り、非識別をIDENTIFIEDと偽装しない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 7.1.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 7.1.7. 検証

DD-E11-ID01〜04。実装未完・runtime/science verification未実施。

### 7.2. `EstimatorPort`

#### 7.2.1. 識別情報・責務

`causal` Domainの科学的Protocol。**PROPOSED**。現行`ScientificCorePort`とのreuse/extension要否を既存コード基準で判定し、CLIだけを理由に重複Portを作らない。

#### 7.2.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 7.2.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 7.2.4. メソッド

```python
class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...
```

#### 7.2.5. 処理仕様

識別・Method適格なRequestのみ実行し、ArtifactをStagingSinkへ限定。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 7.2.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 7.2.7. 検証

DD-E11-EFF01〜05。実装未完・runtime/science verification未実施。

### 7.3. `MethodCapabilityPort`

#### 7.3.1. 識別情報・責務

`causal` Domainの科学的Protocol。**PROPOSED**。現行`ScientificCorePort`とのreuse/extension要否を既存コード基準で判定し、CLIだけを理由に重複Portを作らない。

#### 7.3.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 7.3.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 7.3.4. メソッド

```python
class MethodCapabilityPort(Protocol):
    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord: ...
```

#### 7.3.5. 処理仕様

Method/Estimand/Backend/Inferenceを検証し、silent fallbackをしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 7.3.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 7.3.7. 検証

DD-E11-CAP01〜06。実装未完・runtime/science verification未実施。

### 7.4. `DiagnosticPort`

#### 7.4.1. 識別情報・責務

`causal` Domainの科学的Protocol。**PROPOSED**。現行`ScientificCorePort`とのreuse/extension要否を既存コード基準で判定し、CLIだけを理由に重複Portを作らない。

#### 7.4.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 7.4.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 7.4.4. メソッド

```python
class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...
```

#### 7.4.5. 処理仕様

診断結果を型付きで正規化し、未検証Science PASSにしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 7.4.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 7.4.7. 検証

DD-E11-METH-P101〜P313。実装未完・runtime/science verification未実施。

## 8. 既存Classとの責務境界・拡張原則

本章は、科学的概念の責務とProduct/Scientific/Interfaceの関係を定義する。実行入口がCLIのみであることは、独立したDomain Model、Scientific Core、Method Registryをもう1組作る理由にならない。Web/HTTP、CLI/YAML等の表示・伝送事項はInterface Adapterの責務であり、Estimand・識別成立・Graph・Confidence Setの不変条件は入口に依存しない。

### 8.1. 既存の責務と変更対象

| 責務の所有先 | 既存の実装（source） | 本書との境界 |
|---|---|---|
| Product resource/lifecycle | `product.domain.AnalysisSpecification`、`Execution`、`GraphVersion`、`Result` | Project所属・Version固定・Execution state・Product上の保存とlineageを所有。Scientific DTOはProduct Entityを複製しない |
| Causal science meaning | `causal.design.schemas.CausalDesign`、`Estimand`、`product.domain.graph_semantics` | Estimand、Graph endpoint、科学的妥当性を共通化する。既存ATE/ATTやPAGを超える契約は既存validatorの意味を維持して拡張 |
| Scientific execution | `product.ports.scientific_core.ScientificCorePort`、`scientific.core_adapter.ScientificCoreAdapter` | Backend実行の入口は共通。新Request/Output型は既存Portとの明示的な互換Adapter・versioned evolutionを前提とする |
| Product eligibility | `product.application.scientific_validation_service.ScientificValidationService` | Method×Estimand×Identification適格性の規則が分裂しないよう共通sourceに統合 |
| CLI/file interface | `interfaces.cli.config_schema`、`interfaces.cli.manifest`、Local Reader/Publisher | config YAML/JSON parse、filesystem認可、exit code等を保有。科学的なDomain Typeの権威にはならない |

### 8.2. Class単位の責務境界

| 本書のClass/Port | 既存の対応 | 新たに必要な契約と重複禁止事項 |
|---|---|---|
| `ContentRef` | `product.domain.lineage.ResourceRef`、`product.domain.artifact.Artifact` | immutable file bytes identity。Product resource identity／Filesystem verifierを同一Classへ混ぜない |
| `LocalStudySpec` | `AnalysisSpecification`、`causal.design.schemas.CausalDesign` | 科学的Study意味情報とCLI run envelopeを分離し、同じEligibility/Estimand validatorを共有 |
| `GraphEvidence` | `GraphVersion`、`GraphVersionService`、`graph_semantics.canonical_graph` | PAG/temporalの科学的Evidence。Product GraphVersionの生成・FIX・Project所属を二重所有しない |
| `IdentificationOutcome` | `ScientificResultDescriptor`、`IdentificationAdapter` | Proof、上流Hash、typed理由の科学的表現。Product Result/状態へのMappingを明示 |
| `EstimatorRequest` | `EstimationInput`、`ScientificValidationService` | validated RequestとIV/CATE等のEligibility。既存Estimator/Validation規則を重複させない |
| `ARConfidenceSet` | `TreatmentEffectResult.ci_low/ci_high` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDEDをlosslessに扱う独立科学Value。有限CIへの縮約禁止 |
| `InferenceEvidence` | `TreatmentEffectResult`、`ScientificResultDescriptor` | availability・reason・AR集合・推論の可否を独立に表す |
| `EffectOutcome` | `TreatmentEffectResult`、`ScientificResultDescriptor`、Product `Result` | Point/Inference/Science/Technicalの状態軸を維持。Product Result Entityを複製しない |
| `BackendCapabilityRecord` | `ScientificValidationService.ESTIMATOR_CAPABILITIES`、`StageRunnerRegistry` | 実効Backend/Method/Inferenceのcapability evidence。Environment probeとRegistryはApplication/Scientific layerに置く |
| `IdentificationPort` | `ScientificCorePort.run_identification` | 既存Portをversionedに発展させ、typed evidenceをBridge。無根拠なParallel execution owner禁止 |
| `EstimatorPort` | `ScientificCorePort.run_estimation` | 同様にtyped request・staging sinkに対応し、旧Path-based契約の互換性を保持 |
| `MethodCapabilityPort` | `ESTIMATOR_CAPABILITIES`、`StageRunnerRegistry` | Stage-level登録とMethod-level適格性を分けつつ、唯一のMethod capability authorityへ統合 |
| `DiagnosticPort` | `ScientificCorePort.run_refutation/run_sensitivity`、`DesignDiagnostics` | Operation/Method別diagnosticと既存Refutation・Sensitivityを対応させ、重複実装を避ける |

### 8.3. 配置・利用上の不変条件

- `causal.local_contract.*`という旧設計候補Pathは、本書のClass識別欄に残る場合も**確定した独立Domain packageの意味を持たない**。共通の科学的意味と既存Classの責務差分に基づき配置する。
- `GraphEvidence.make_revision`はGraph内容から新しいEvidence値を導出する操作候補としてのみ解釈し、Product `GraphVersionService`のProject/Version writer権威を置き換えない。これが保証できない場合、このsignature自体を再設計する。
- `BackendCapabilityRecord`のRuntime probeとoptional scientific library importはDomain Valueの生成処理ではなく、Capability Registry/Scientific Adapter側の責務とする。
- `ContentRef`のpath表現検証はfilesystem安全性検証ではない。TrustedRoot内same-fd read/hashはI/O Adapterが所有する。
- Scientific Resultの`AVAILABLE`、Identificationの`IDENTIFIED`、Productの`Execution.SUCCEEDED`、Science Acceptanceは別状態であり、単一`ScientificStatus`への無検証圧縮は禁止する。
- Product `schemas.canonical_bytes`／`infrastructure.config.hash_mapping(default=str)`と、外部Wireが要求するJCS/RFC8785を機械的に同一視しない。Hash Versionを含むCodecを独立検証する。
- 新規Portは既存`ScientificCorePort`のinterface version・Bridgeと実行経路が定義されるまで、別Runtimeの並行Authorityとして実装しない。
- 科学的な値型を追加すること自体は可能だが、具体的なModule配置・Port version・統合方法はClass Method signatureと既存Product contractの整合を保証した上で定める。
