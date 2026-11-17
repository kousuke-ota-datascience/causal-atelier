# 30_61_local_domain_ports — Local Domain / Scientific Port 物理詳細設計

## 1. 目的・設計Authority・依存方向

Local causal laneのDomain DTO／Portを物理的なClass、署名、状態不変条件、検証義務として定義する。既存Product DomainとLocal Domainのauthorityを混在させない。個別の外部Backend数値計算は[30_63](30_63_e11_method_adapters.md)、UseCase・具体Publication/Reader/Privacy実装は[30_62](30_62_e11_local_execution_publication.md)、CLI/Resultのwire contractは[23_41](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)と[23_42](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)を正本とする。

**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。 Source blob SHAは存在しないため、既存コードのblob SHAをこれらのClassに転記しない。検証IDは実装・試験の**義務**でありPASSの証拠ではない。本書は[Class設計の共通7区分](30_01_class_design_template.md)を採用する。

| 論理Package | Planned modules / responsibility | 依存上の境界 |
|---|---|---|
| `causal.local_contract` | `references.py`, `study.py`, `graph.py`, `identification.py`, `effect.py`, `ports.py` | 外部scientific library、Product DB/Worker/ORMへ依存しない |
| `causal.local_application` | `use_case.py`, `capability_registry.py` | Domain Portを呼び、per-run orchestrationを担う。詳細は30_62 |
| `scientific.local_adapters` | `native.py`, `dowhy.py`, `econml.py`, `temporal.py`, `quasi.py` | Domain DTOへ結果を正規化。optional importsはAdapter load時のみ |
| `interfaces.cli.e11` | `command.py`, `config_decoder.py`, `publication.py`, `manifest_reader.py` | version dispatchとtrusted file I/Oを所有。詳細は30_62/23_41/23_42 |

依存方向は `CLI → Application → Domain Port ← Scientific Adapter`。Productへの統合は型・authority・lifecycleを確認した明示Adapterを通す。PortにBackend Model/Estimator Objectを渡さず、Typed DTO／bytes／content referenceを渡す。

## 2. Content Reference契約


### 2.1. `ContentRef`

#### 2.1.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.references.ContentRef`。immutable value object。Dataset・Question・Design・Graph・Identification等の内容参照を識別し、物理bytesの検証結果を**保持しない**。外部絶対pathやaccess tokenを保存しない。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 2.1.2. フィールド

| Field | Python型 | 必須/default | 制約 |
|---|---|---|---|
| `identity` | `str` | 必須 | 非空の論理identity |
| `relative_key` | `str` | 必須 | safe relative POSIX key。絶対・dotdot・NUL・drive等を拒否 |
| `sha256` | `str` | 必須 | 完成ファイル実bytesのSHA256小文字hex64 |
| `media_type` | `str` | 必須 | Schema/Readerとの整合必須 |
| `schema_version` | `str|None` | 必須／nullable | unknown versionを無条件に推測しない |

#### 2.1.3. Constructor / Factory

`from_payload(payload: Mapping[str, JsonValue]) -> ContentRef`（設計上のFactory）。strict key／型／hash文字種／relative pathを検査。invalid payloadは型付きvalidation error。mutableな入力Mappingを保持しない。

#### 2.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_payload(payload: Mapping[str, JsonValue])` | `ContentRef` | strict parse; I/Oなし | Schema／relative-key／digest validation error |

#### 2.1.5. 処理仕様

Pathの文法検査は実filesystem参照の安全性証明ではない。dotdot、absolute path、drive letter、NUL、backslash区切り混在、不正Unicode正規化を拒否し、HashはコンテンツIDと別に保持。

#### 2.1.6. I/O・連携・失敗処理

I/Oなし。Root閉じ込めとTOCTOUの防止、same-fd bytes hashは`ContentReferencePort.verify`の実装責務。Transaction/Retry/Rollbackは該当しない（immutable value）。

#### 2.1.7. 検証

`DD-E11-REF01`有効Ref、`REF02` traversal/symlink/race、`REF03` input差替え/TOCTOU、`REF04` metadata-only同ID別bytes拒否。FR-185、NFR-029/031。


### 2.2. `ContentReferencePort`

#### 2.2.1. 識別情報・責務

**Protocol / planned module:** `causal.local_contract.ports.ContentReferencePort`。trusted root内のRefを実際に検証・読み出すI/O interface。`ContentRef`そのものを信頼済みbytes扱いしない。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 2.2.2. フィールド

Protocol自身にmutable fieldなし（N/A）。引数`ref: ContentRef`、`root: TrustedLocalRoot`をcall単位で受け取り、返却`VerifiedContent`は検証されたbytes/digestを保持する。

#### 2.2.3. Constructor / Factory

Protocolに具体constructorはない（N/A）。TrustedLocalRootの生成とrootfd所有は具体I/O Adapterの責務。

#### 2.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `verify(self, ref: ContentRef, *, root: TrustedLocalRoot)` | `VerifiedContent` | 安全なopenとsame-fd hash/size照合 | path/race、digest、permission、read failure |

#### 2.2.5. 処理仕様

Rootのdirfdなどを用いてsymlink traversalとraceを防ぎ、実際に開いた同一FDからdigestを計算。mime/schema等の意味検証はDomain validatorに委ね、Ref上のself-asserted hashだけで成功としない。

#### 2.2.6. I/O・連携・失敗処理

File読み取りあり、書き込みはしない。Root外read・未知mount・FD置換はfail-closed。Retry時も再読込／再hash検証必須、cached未検証bytes禁止。

#### 2.2.7. 検証

`DD-E11-REF01〜04`、特にTOCTOU/hardlink/symlink攻撃と実bytes改変を独立Contract/Negative testで検査。


## 3. Study Specification / Decoder契約


### 3.1. `LocalStudySpec`

#### 3.1.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.study.LocalStudySpec`。Operation、Method、Estimand、Input refs、Inference、Privacy要求を保持するimmutable Domain Value。Parse/FS I/O/Backend呼出しは責務外。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 3.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `schema_version` | `Literal["e11-local-study/1"]` | 既存v2へのfallback禁止 |
| `run_id, operation, analysis_mode` | `str, LocalOperation, AnalysisMode` | safe run ID・enum |
| `question, design, dataset` | `ContentRef` | Operationごとの必須性をvalidate |
| `graph, identification` | `ContentRef|None` | DISCOVERで未生成参照を要求しない |
| `estimand, method, inference` | `EstimandRef, MethodRequest, InferenceRequest` | Operation×Method×Target整合 |
| `randomness, privacy` | `RandomnessSpec, LocalPrivacySpec` | seedおよび行出力要求を明示 |

#### 3.1.3. Constructor / Factory

ValidatedStudy生成はStrict Decoder/Validatorを経由する。直接constructorまたはfactoryで型・必須フィールド・Operationの整合を検査する必要があり、単なるdataclass生成を`ValidatedStudy`の証明としない。

#### 3.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_local_invariants(self)` | `tuple[Reason,...]` | pure Operation/Method/Target/Privacy検査 | 実行不適格理由を列挙 |

#### 3.1.5. 処理仕様

`DISCOVER`は探索Target `{family:GRAPH_STRUCTURE,population:OBSERVED_VARIABLES,contrast:NOT_APPLICABLE}`をタグ付き非Effect値として扱い、ATE/ATTを偽造しない。`ESTIMATE`等のEffect Operationには効果Estimandと適格なIdentification参照が必要。

#### 3.1.6. I/O・連携・失敗処理

I/Oなし。Studyの意味射影をcanonical encodingしたbytesからrequest hashを作り、Codec versionをManifestで追跡する。Hashは物理File参照とは区別。

#### 3.1.7. 検証

`DD-E11-SPEC01` strict valid/schema、`SPEC02` legacy dispatch、`SPEC03` confirmatory/inference、`SPEC04` Method/Estimand mismatch。FR-185/201、AR-034、NFR-029/036。


### 3.2. `LocalConfigDecoder`

#### 3.2.1. 識別情報・責務

**Protocol / planned concrete module:** `causal.local_contract.ports.LocalConfigDecoder`と`interfaces.cli.e11.config_decoder`。raw YAML/JSONからstrict Validation済みのStudyを生成。Application内で再parseしない。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 3.2.2. フィールド

Protocol instance fieldはN/A。入力`raw: bytes`、`declared_format: Literal["yaml","json"]`。Schema Registry/Method profileはConcrete Decoder注入の読み取り専用依存。

#### 3.2.3. Constructor / Factory

`decode`はstrict version dispatch後だけValidatedStudy factoryへ渡す。Decoder内の`decode_yaml(raw:bytes)->LocalStudySpec`は内部helperであり公開Portの別Contractにはしない。

#### 3.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `decode(self, raw:bytes, *, declared_format:Literal["yaml","json"])` | `ValidatedStudy` | pure strict parse/schema/method profile | unknown version、duplicate key、invalid profile |
| `decode_yaml(raw:bytes)` | `LocalStudySpec` | Concrete内部helper | 同上 |

#### 3.2.5. 処理仕様

重複Key、YAML Python Tag、過大alias/nesting、不明key、legacy/無版を拒否。P1-M06の[Question](../23_api_interface_design/schema_drafts/e11_p1_m06_fci_question_profile_v1.schema.json)・[Design](../23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json)は**当該Method内部のprofile**で、全Discoveryへ一般化しない。Dataset列名/順序、BK、CI family/measurement scaleは意味Validatorも使う。

#### 3.2.6. I/O・連携・失敗処理

Raw bytesからのparse以外のI/Oはない。外部Ref実bytes確認は`ContentReferencePort`で行う。Malformed configはCLI exit2へ、input/hash/path不一致はexit3へ正規化。

#### 3.2.7. 検証

`DD-E11-SPEC01〜04`、invalid YAML/JSON duplicate、P1-M06 ProfileとStudyのcross-asset join、untrusted refを検証する。


## 4. Graph Evidence / Version契約


### 4.1. `GraphEvidence`

#### 4.1.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.graph.GraphEvidence`。PAG/CPDAG/DAG等のGraphとprovenance/Versionを保持するimmutable Value。`GraphVersion`はこの設計では**Version関連フィールドとrevision操作の概念**であり、単独のClassを別途定義したとは解釈しない。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 4.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `kind` | `GraphKind` | DAG/CPDAG/PAG等の区別 |
| `nodes` | `tuple[Node,...]` | unique identity |
| `edges` | `tuple[EndpointEdge,...]` | endpoint/lag/identityをlossless |
| `temporal` | `TemporalConvention|None` | lagの符号・基準時刻 |
| `version_id, parent_version_id` | `str, str|None` | immutable provenance chain |
| `provenance, content_hash` | `GraphProvenance, str` | Graph意味射影に一致するdigest |

#### 4.1.3. Constructor / Factory

`from_canonical_json(raw:bytes)->GraphEvidence`：strict Graph Schema＋意味Validator。不可逆PAG→DAG変換、未知node/endpoint/重複edge/lag規約欠落を拒否。

#### 4.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_canonical_json(raw:bytes)` | `GraphEvidence` | pure strict graph decode | schema、endpoint、lag、hash不整合 |
| `make_revision(edit:GraphEdit,rationale:str,assumptions:tuple[str,...])` | `GraphEvidence` | 元Graph不変で新Version生成 | missing rationale / incompatible edit |
| `canonical_payload()` | `Mapping[str,JsonValue]` | lossless domain serialization | invalid/incomplete Graph |

#### 4.1.5. 処理仕様

`EndpointEdge(source,target,source_mark,target_mark,lag)`のmarkはTAIL/ARROW/CIRCLE。Node順序を反転する場合はendpointも対応させる。PAGのbidirected/circleをDAGへ暗黙確定しない。FIXEDは編集状態であってScientific Truthではない。未確定GraphからのEffect識別は独立のEstimand別識別証拠を要求。

#### 4.1.6. I/O・連携・失敗処理

Graph Valueの純粋操作はI/Oなし。内部`content_hash=SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256=SHA256(完成Graph File実bytes)`を**別々に検証**。Version revisionは元Versionを上書きしない。

#### 4.1.7. 検証

`DD-E11-GRAPH01` FCI PAG circle/arrow/bidirected、`GRAPH02` PCMCI lag、`GRAPH03` silent PAG→DAG拒否、`GRAPH04` Version/再識別。FR-186/196、AR-028/036/043。


## 5. Identification / Estimator Request契約


### 5.1. `IdentificationOutcome`

#### 5.1.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.identification.IdentificationOutcome`。識別状態・対象Estimand・Proof・lineageを保持するValue。DoWhy内部ラベルをDomainの推定対象と混同しない。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 5.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `identification_id` | immutable identity |
| `estimand` | `EstimandRef`。B0/B1/DRIV等の区別 |
| `status` | `IdentificationStatus`。nonidentified/review/partialを型付け |
| `strategy, proof` | Strategy、`IdentificationProof|None` |
| `upstream, reasons` | `UpstreamHashSet, tuple[ScientificReason,...]` |

#### 5.1.3. Constructor / Factory

`from_adapter(raw:AdapterIdentification)->IdentificationOutcome`。BackendのStatus、assumption、GraphVersion、Estimand、Upstreamを意味検証して正規化。未提供Proofを生成しない。

#### 5.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_adapter(raw:AdapterIdentification)` | `IdentificationOutcome` | pure status/proof normalization | proof/estimand/upstream不整合 |

#### 5.1.5. 処理仕様

`NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED`を点推定許可へ自動昇格しない。緩和可能な列挙WARNだけに理由付きoverrideを許可。

#### 5.1.6. I/O・連携・失敗処理

外部I/Oなし。実際のBackend識別計算は`IdentificationPort`、Proof/File readbackは別Port。Retry/RollbackはN/A。

#### 5.1.7. 検証

`DD-E11-ID01` B0/B1/DRIV mislabel、`ID02` lineage差、`ID03` nonidentified override拒否、`ID04` GraphVersion再識別。FR-187/194/199、AR-029/039/043。


### 5.2. `EstimatorRequest`

#### 5.2.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.identification.EstimatorRequest`。Identification proofが適格な場合だけEstimatorへ渡すRequest Value。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 5.2.2. フィールド

| Field | Type・制約 |
|---|---|
| `method_id, estimand_family` | Method×target一致 |
| `identification_ref` | 上流証拠参照 |
| `question/design/graph/dataset_hashes` | 完全な上流digest集合 |
| `method_config, inference_request` | Method/Inference適格なtyped config |

#### 5.2.3. Constructor / Factory

`assert_eligible(...)->ValidatedEstimatorRequest`は入力と上流証拠を照合する型付きvalidator。Validation前の生RequestをAdapterへ送らない。

#### 5.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `assert_eligible(identification:IdentificationOutcome,design:CausalDesignEvidence,capability:BackendCapability)` | `ValidatedEstimatorRequest` | pure eligibility check | scientific negative / schema validation区別 |

#### 5.2.5. 処理仕様

Method-specific assumptions、Mediator/Instrument/support、Data Eligibility、Graph/Design/Question/Dataset hash全一致、CI要求を検証。不適格は`ScientificNegativeOutcome`としてBackend未呼出。Path/schema mismatchはtechnical validationとする。

#### 5.2.6. I/O・連携・失敗処理

Value自身はI/Oなし。実Estimator I/O/Artifactは`EstimatorPort.estimate(...,sink)`を通す。

#### 5.2.7. 検証

`DD-E11-ID01〜04`およびMethod固有Negative Tests。


## 6. Confidence Set / Inference Evidence契約


### 6.1. `ARConfidenceSet`

#### 6.1.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.effect.ARConfidenceSet`。Anderson–Rubin反転の損失ない数学集合を表すValue。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 6.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `confidence_level` | `float` | 0 < level < 1 |
| `components` | `tuple[ExtendedRealInterval,...]` | EMPTYは0件。finite/±∞をtagged endpointsで表現 |
| `topology` | `SetTopology` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED |
| `inversion_evidence` | `ContentRef` | 成功した数学的反転の証拠 |

#### 6.1.3. Constructor / Factory

`from_components(level,components,evidence)->ARConfidenceSet`：finite endpoint、順序、open/closed、重複/接触区間の数学的正規化。

#### 6.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_components(level,components,evidence)` | `ARConfidenceSet` | pure set normalization | invalid endpoint/topology |
| `contains(beta:float)` | `bool` | endpoint条件で判定 | NaN/invalid β |
| `to_payload() / from_payload(payload)` | JSON / Value | Lossless roundtrip | malformed topology / JSON非有限数値 |

#### 6.1.5. 処理仕様

Topology分類はEMPTY→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDED。ALL_REALは(-∞,+∞)一成分。∞端点はopen、双方openで接触する2区間は1点gapを残すため結合しない。数学的EMPTYは`AVAILABLE + inversion_evidence`と両立、計算失敗`FAILED+reason`とは別。B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件が成立する場合`T_AR(βhat)=0`により非空が必要となり、**Method別validator**でEMPTYを拒否。

#### 6.1.6. I/O・連携・失敗処理

Valueはpure。JSONのNaN/Infinity数値は禁止、tagged endpointで表現。実AR反転・HC1・coverageはMethod Adapterと独立科学検証に委譲。

#### 6.1.7. 検証

`DD-E11-AR01` 5分類、`AR02` generic EMPTYとjust-identified条件分離、`AR03` lossless roundtrip、`AR04` null reason、`AR05` confirmatory fail-closed。FR-202、AR-040、NFR-036。


### 6.2. `InferenceEvidence`

#### 6.2.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.effect.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 6.2.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### 6.2.3. Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### 6.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 6.2.5. 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### 6.2.6. I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 6.2.7. 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。


## 7. Effect / Backend Evidence契約


### 7.1. `EffectOutcome`

#### 7.1.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.effect.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 7.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics, method_evidence, upstream_hashes` | typed evidenceとlineage |

#### 7.1.3. Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### 7.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_canonical_result()` | typed Result payload | pure versioned encoding | incompatible schema/estimand |

#### 7.1.5. 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### 7.1.6. I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 7.1.7. 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。


### 7.2. `BackendCapabilityRecord`

#### 7.2.1. 識別情報・責務

**Class / planned module:** `causal.local_contract.effect.BackendCapabilityRecord`（論理所属は実装前にPort/Registryとの依存方向を照合する）。実効Backend適格性の証拠を保持し、silent fallbackを禁止する。**状態：PROPOSED（設計契約、Source実装なし）。** 現在の`prototype/ariadne_mvp`の`src/ariadne/causal/local_contract/`は未作成。既存Product Classとの同一性・実装済み・Runtime PASSを主張しない。実装時の変更は上位契約と同期する。

#### 7.2.2. フィールド

| Field | 制約 |
|---|---|
| `method_id, backend_id` | 明示指定した組 |
| `distribution_version, adapter_version, api_signature_hash` | 観測された実効版とAPI |
| `extra, profile` | effective environment/profile |
| `available, reason` | boolと欠落時のtyped reason |

#### 7.2.3. Constructor / Factory

Constructorは観測証拠から作成。未実測値を使用可能とするdefault/fallback禁止。

#### 7.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `check(request)` | typed compatibility decision | version/Method/API/Inference照合 | unsupported/unavailable typed reason |

#### 7.2.5. 処理仕様

静的Registryと実効Probeから指定Methodと推論方式の可用性を検証。Probeの取得はConcrete Registry/Runtime Port側で行い、Value自身がoptional Backendをimportしない。`load_adapter`時だけBackend import可能。

#### 7.2.6. I/O・連携・失敗処理

RecordはI/Oなし。Runtime probe、distribution inspection、optional importは30_62のCapability Registryと30_63のAdapter実装の責務。

#### 7.2.7. 検証

`DD-E11-EFF03` version/API mismatch、`DD-E11-CAP01〜06` profile isolation/inference availability、no silent fallback。


## 8. Local Scientific / Infrastructure Port契約

### 8.1. Portの正規署名

```python
class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...

class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...

class MethodCapabilityPort(Protocol):
    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord: ...

class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...

class LocalConfigDecoder(Protocol):
    def decode(self, raw: bytes, *, declared_format: Literal["yaml", "json"]) -> ValidatedStudy: ...

class ContentReferencePort(Protocol):
    def verify(self, ref: ContentRef, *, root: TrustedLocalRoot) -> VerifiedContent: ...

class LocalPolicyVerifierPort(Protocol):
    def verify(self, *, policy_ref: ContentRef, study: ValidatedStudy,
               root: TrustedLocalRoot, anchor: PolicyTrustAnchor) -> VerifiedStudyPolicyEvidence: ...

class LocalPrivacyPolicyPort(Protocol):
    def authorize(self, *, study: ValidatedStudy, cli_row_flag: bool,
                  root: TrustedLocalRoot, policy: VerifiedStudyPolicyEvidence | None,
                  output_shape: PlannedOutputShape) -> PrivacyDecision: ...

class LocalPublicationPort(Protocol):
    def begin(self, *, run_id: RunId, request_hash: Sha256Digest,
              root: TrustedLocalRoot) -> StagingArtifactSink: ...
    def seal(self, *, sink: StagingArtifactSink, manifest: LocalRunManifest,
             privacy: PrivacyDecision) -> ValidatedStagedBundle: ...
    def publish(self, *, bundle: ValidatedStagedBundle,
                root: TrustedLocalRoot) -> CommittedLocalRun: ...

class LocalManifestReaderPort(Protocol):
    def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ...
```

署名で用いたDomain DTOとProtocolはこのLocal lane独自の契約である。Product `ScientificCorePort`／`ArtifactStorePort`を単純aliasせず、外部Estimator Objectを値に通さない。Type annotationが`Validated*`であってもFactoryとAdapter直前で再検証する。`TrustedLocalRoot`はOS principal/owner/ACL/mount/dirfdの検証済みCapabilityであり、生Pathではない。

### 8.2. Portごとの7区分が必要な場合の所有文書

上位のInterface境界とClass設計は重複Authorityにしない。以下でSource Classの7区分・実装詳細を定義するのは担当文書であり、本節はProtocolの論理署名・依存方向を保持する。

| Port / Protocol | 物理Class詳細のOwner | 主要失敗／検証 |
|---|---|---|
| `IdentificationPort`, `EstimatorPort`, `DiagnosticPort` | [30_63 Method Adapters](30_63_e11_method_adapters.md) と[23_41 Scientific Port IF](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md) | 識別、Estimand、Backend結果、staging限定 |
| `MethodCapabilityPort` | [30_62 MethodCapabilityRegistry](30_62_e11_local_execution_publication.md) | Method/Backend/ProfileとInference/API不整合 |
| `LocalConfigDecoder` | 本書§3.2 | strict wire/version/method profile |
| `ContentReferencePort` | 本書§2.2 | root閉じ込め、bytes hash、TOCTOU |
| `LocalPolicyVerifierPort`, `LocalPrivacyPolicyPort` | [30_62 Privacy](30_62_e11_local_execution_publication.md) | independent policy authority、no self-approval、row export deny |
| `LocalPublicationPort`, `LocalManifestReaderPort` | [30_62 Publisher / Reader](30_62_e11_local_execution_publication.md)、[23_42 wire IF](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md) | atomic no-clobber、Marker→Manifest→Artifact readback |

**共通のProtocol責務（7区分への対応）：** 識別＝上表Ownerと署名、フィールド＝ProtocolはN/A、Constructor＝ProtocolはN/A、メソッド＝§8.1、処理仕様＝各Owner契約、I/O/失敗＝各Owner契約、検証＝DD/IF/IOと独立契約テスト。Protocol宣言は具体Classがすでに実装済みであることの証明ではない。

Portで生成するArtifactはStagingSinkに限定する。Publisher Facadeとrun-scoped Concrete、Reader Facadeの`verify`とConcreteの`read_run`は**同一処理の異なるInterface境界**であり、二重のPublication/Readbackアルゴリズムを設けない。

## 9. ストック型設計書としての検証責務

上位RD/Interface/科学的契約の意味をこの物理設計だけで書き換えない。全Class/Protocolは未実装の新規提案であるため、Runtime PASS・科学的妥当性・実効Linux FS/Codec保証を本書から推認しない。実装時は本書に列挙したConstructor／署名／exception／DDテストIDをCodeと照合し、各Owner文書と独立Science Referenceを検証する。
