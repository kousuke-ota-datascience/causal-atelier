# 30_60_cli_adapters


---

## 7. `CliManifest` — Existing v2 CLI DTO（Owner 7区分）

### 7.1. 識別情報・責務
- **Class/Module:** `ariadne.interfaces.cli.manifest.CliManifest`、`src/ariadne/interfaces/cli/manifest.py` blob `97216eca9d777e97f7a5ebd4e248afd31c6b4de0`。**EXISTING**。
- **Responsibility:** Existing v2 CLI manifest fieldsの構造保持と`to_dict` serialization。E11 typed Graph/PAG、AR集合、Local commit marker、独立Science acceptanceのAuthorityではない。
- **Reuse:** E11新結果をこのv2 DTOへ暗黙拡張しない。FR-120b/NFR-005/NFR-010bをE11の既成機能と扱わない。

### 7.2. フィールド
| Field group | Existing Python fields / defaults | Invariant / risk |
| --- | --- | --- |
| Identity | `manifest_version: str`, `operation: str`, `algorithm_or_estimator: str` | mandatory、constructorでversion whitelist判定なし |
| Input | `dataset: dict[str,Any]`, `graph: dict[str,Any]|None`, `parameters: dict[str,Any]`, `analysis_spec: dict[str,Any]` | shallow frozenの内側のdictはmutable |
| Runtime | `random_seed: int|None`, `code_version: str`, `runtime_versions: dict[str,str]`, `backend_version: str|None=None` | Provenance値の実効性をClass自身は検証しない |
| Status | `scientific_status: str`, `result_summary: dict[str,Any]` | Science PASSと実測を結びつけるVerifierは本Classには存在しない |
| Artifacts/Warnings | `artifacts: list[dict[str,Any]]=field(default_factory=list)`, `warnings: list[Any]=field(default_factory=list)`, `scientific_warnings: list[dict[str,Any]]=field(default_factory=list)` | Instance毎独立list、nested mutable |
| Legacy compat | `snapshot_schema_version: str="causal-analysis-spec/2"` | Old v2 schema defaultを変更しない |
| Optional | `analysis_mode: str|None`, `causal_question_hash: str|None`, `graph_origin: str|None`, `upstream_result_reference: str|None`, `identification_status: str|None`, `eligibility_status: str|None` | New E11 confirmation/identification validationは自動実施されない |

### 7.3. Constructor / Factory
- `@dataclass(frozen=True)`生成`__init__`。上記mandatory fieldsを位置引数で受け、3 listは各Instanceにdefault_factoryで生成する。Optional fieldsは宣言済みdefault。
- **N/A:** custom `__post_init__`やstrict Schema Parser/validator、Builder/Factoryは存在しない。Constructor引数と`to_dict()`だけではE11 schema supportを証明しない。
- **Postcondition:** top-level fieldへの再代入は拒否。ただしdict/listのnested mutationは可能。

### 7.4. メソッド
| Method | Return | Behavior / side effect / failure |
| --- | --- | --- |
| `to_dict(self) -> dict[str,Any]` | nested mapping | `dataclasses.asdict(self)`のdeep-copy recursionによるJSON準備。File I/Oなし、Schema/Scientific correctnessは未検査 |

### 7.5. 処理仕様
`CliManifest`は既存`scientific_stage.py`などのWriter側から生成し、`to_dict()`で辞書化する。外部`manifest.json`のFile書込はCallerの責務。Old v2のScientific/Technical statusと新E11の識別・推定・区間・Science Acceptance axesを混同しない。

### 7.6. I/O・連携・失敗処理
- **I/O:** Class自身にfile read/writeなし。Outputは通常のPython辞書。Payloadに非JSON型がある場合の`json.dump`失敗は実Writer側の扱い。
- **Transaction/Retry/Rollback:** N/A（DTO）。`asdict`の生成失敗以外に明示Exceptionはない。
- **Compatibility:** `manifest_version=2.0`など既存Version semanticsを変更せず、E11 `e11-local-manifest/1`は独立Reader/DTOで扱う。

### 7.7. 検証
既存manifestのlist default instance分離、`to_dict` nested mapping、legacy v2 reader/roundtrip、unknown new E11 schema拒否、JSON file write失敗/partial publish時の取り扱いはWriterの負例。Product/E9/E10と旧CLI全回帰が対象。テスト実行**NOT_RUN**。

**Requirement trace:** `FR-120b`（DEFERRED）、`NFR-005`、`NFR-010b`（DEFERRED）、`NFR-014`（legacy reader compatibility）。

## 8. 既存CLI DTOと拡張CLIの互換境界

旧`CliManifest`実装と旧Product Portは上記§7の正規source contractを維持し、新E11の型付きResult／AR集合へ暗黙移行しない。因果Domain型と科学Portは[30_61](30_61_causal_domain_ports.md)、Local Application／Atomic Publisher/Reader/Privacyは[30_62](30_62_e11_local_execution_publication.md)、全41 MethodのAdapter割当と受入制約は[30_63](30_63_e11_method_adapters.md)を参照する。

新候補Classを現行コードに実在するClassとして扱わず、Method/Backend/Scienceの実測受入を別途要求する。

## 9. Local CLI Decoder（Interface adapter / PROPOSED）

### 9.1. `LocalConfigDecoder`

#### 9.1.1. 識別情報・責務

**Protocol / planned concrete module:** `ariadne.interfaces.cli.local_causal.decoder.LocalConfigDecoder`と`ariadne.interfaces.cli.local_causal.config_decoder`。raw YAML/JSONからstrict Validation済みのStudyを生成。Application内で再parseしない。**PROPOSED（未実装）。**

#### 9.1.2. フィールド

Protocol instance fieldはN/A。入力`raw: bytes`、`declared_format: Literal["yaml","json"]`。Schema Registry/Method profileはConcrete Decoder注入の読み取り専用依存。

#### 9.1.3. Constructor / Factory

`decode`はstrict version dispatch後だけValidatedStudy factoryへ渡す。Decoder内の`decode_yaml(raw:bytes)->LocalStudySpec`は内部helperであり公開Portの別Contractにはしない。

#### 9.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `decode(self, raw:bytes, *, declared_format:Literal["yaml","json"])` | `ValidatedStudy` | pure strict parse/schema/method profile | unknown version、duplicate key、invalid profile |
| `decode_yaml(raw:bytes)` | `LocalStudySpec` | Concrete内部helper | 同上 |

#### 9.1.5. 処理仕様

重複Key、YAML Python Tag、過大alias/nesting、不明key、legacy/無版を拒否。P1-M06の[Question](../23_api_interface_design/schema_drafts/e11_p1_m06_fci_question_profile_v1.schema.json)・[Design](../23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json)は**当該Method内部のprofile**で、全Discoveryへ一般化しない。Dataset列名/順序、BK、CI family/measurement scaleは意味Validatorも使う。

#### 9.1.6. I/O・連携・失敗処理

Raw bytesからのparse以外のI/Oはない。外部Ref実bytes確認は`ContentReferencePort`で行う。Malformed configはCLI exit2へ、input/hash/path不一致はexit3へ正規化。

#### 9.1.7. 検証

`DD-E11-SPEC01〜04`、invalid YAML/JSON duplicate、P1-M06 ProfileとStudyのcross-asset join、untrusted refを検証する。FR-185、**FR-201**、NFR-029/036。


## 10. Trusted File Reference I/O（Interface adapter / PROPOSED）

### 10.1. `ContentReferencePort`

#### 10.1.1. 識別情報・責務

**Protocol / planned module:** `ariadne.interfaces.cli.local_causal.content_io.ContentReferencePort`。trusted root内のRefを実際に検証・読み出すI/O interface。`ContentRef`そのものを信頼済みbytes扱いしない。**PROPOSED（未実装）。**

#### 10.1.2. フィールド

Protocol自身にmutable fieldなし（N/A）。引数`ref: ContentRef`、`root: TrustedLocalRoot`をcall単位で受け取り、返却`VerifiedContent`は検証されたbytes/digestを保持する。

#### 10.1.3. Constructor / Factory

Protocolに具体constructorはない（N/A）。TrustedLocalRootの生成とrootfd所有は具体I/O Adapterの責務。

#### 10.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `verify(self, ref: ContentRef, *, root: TrustedLocalRoot)` | `VerifiedContent` | 安全なopenとsame-fd hash/size照合 | path/race、digest、permission、read failure |

#### 10.1.5. 処理仕様

Rootのdirfdなどを用いてsymlink traversalとraceを防ぎ、実際に開いた同一FDからdigestを計算。mime/schema等の意味検証はDomain validatorに委ね、Ref上のself-asserted hashだけで成功としない。

#### 10.1.6. I/O・連携・失敗処理

File読み取りあり、書き込みはしない。Root外read・未知mount・FD置換はfail-closed。Retry時も再読込／再hash検証必須、cached未検証bytes禁止。

#### 10.1.7. 検証

`DD-E11-REF01〜04`、特にTOCTOU/hardlink/symlink攻撃と実bytes改変を独立Contract/Negative testで検査。FR-185、NFR-029、**NFR-031**。


これらは科学的Domain Modelではなく、入力とtrusted file I/OのInterface境界。CLIを理由にGraph・Estimand・Inferenceの別Domainを作らない。


## 11. `ContentRef` — Portable content reference value（PROPOSED）


### 11.1. 識別情報・責務

**Class / module:** `ariadne.shared.content_ref.ContentRef`。immutable value object。Dataset・Question・Design・Graph・Identification等の内容参照を識別し、物理bytesの検証結果を**保持しない**。外部絶対pathやaccess tokenを保存しない。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

### 11.2. フィールド

| Field | Python型 | 必須/default | 制約 |
|---|---|---|---|
| `identity` | `str` | 必須 | 非空の論理identity |
| `relative_key` | `str` | 必須 | safe relative POSIX key。絶対・dotdot・NUL・drive等を拒否 |
| `sha256` | `str` | 必須 | 完成ファイル実bytesのSHA256小文字hex64 |
| `media_type` | `str` | 必須 | Schema/Readerとの整合必須 |
| `schema_version` | `str|None` | 必須／nullable | unknown versionを無条件に推測しない |

### 11.3. Constructor / Factory

`from_payload(payload: Mapping[str, JsonValue]) -> ContentRef`（設計上のFactory）。strict key／型／hash文字種／relative pathを検査。invalid payloadは型付きvalidation error。mutableな入力Mappingを保持しない。

### 11.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_payload(payload: Mapping[str, JsonValue])` | `ContentRef` | strict parse; I/Oなし | Schema／relative-key／digest validation error |

### 11.5. 処理仕様

Pathの文法検査は実filesystem参照の安全性証明ではない。dotdot、absolute path、drive letter、NUL、backslash区切り混在、不正Unicode正規化を拒否し、HashはコンテンツIDと別に保持。

### 11.6. I/O・連携・失敗処理

I/Oなし。Root閉じ込めとTOCTOUの防止、same-fd bytes hashは`ContentReferencePort.verify`の実装責務。Transaction/Retry/Rollbackは該当しない（immutable value）。

### 11.7. 検証

`DD-E11-REF01`有効Ref、`REF02` traversal/symlink/race、`REF03` input差替え/TOCTOU、`REF04` metadata-only同ID別bytes拒否。FR-185、NFR-029/031。


## 12. `LocalStudySpec` — CLI execution request envelope（PROPOSED）


### 12.1. 識別情報・責務

**Class / module:** `ariadne.interfaces.cli.local_causal.study.LocalStudySpec`。Operation、Method、Estimand、Input refs、Inference、Privacy要求を保持するimmutable CLI execution envelope DTO。Parse/FS I/O/Backend呼出しは責務外。科学的DesignとEstimandは既存CausalDesign/共通validatorを再利用する。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

### 12.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `schema_version` | `Literal["e11-local-study/1"]` | 既存v2へのfallback禁止 |
| `run_id, operation, analysis_mode` | `str, LocalOperation, AnalysisMode` | safe run ID・enum |
| `question, design, dataset` | `ContentRef` | Operationごとの必須性をvalidate |
| `graph, identification` | `ContentRef|None` | DISCOVERで未生成参照を要求しない |
| `estimand, method, inference` | `EstimandRef, MethodRequest, InferenceRequest` | Operation×Method×Target整合 |
| `randomness, privacy` | `RandomnessSpec, LocalPrivacySpec` | seedおよび行出力要求を明示 |

### 12.3. Constructor / Factory

ValidatedStudy生成はStrict Decoder/Validatorを経由する。直接constructorまたはfactoryで型・必須フィールド・Operationの整合を検査する必要があり、単なるdataclass生成を`ValidatedStudy`の証明としない。

### 12.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_local_invariants(self)` | `tuple[Reason,...]` | pure Operation/Method/Target/Privacy検査 | 実行不適格理由を列挙 |

### 12.5. 処理仕様

`DISCOVER`は探索Target `{family:GRAPH_STRUCTURE,population:OBSERVED_VARIABLES,contrast:NOT_APPLICABLE}`をタグ付き非Effect値として扱い、ATE/ATTを偽造しない。`ESTIMATE`等のEffect Operationには効果Estimandと適格なIdentification参照が必要。

### 12.6. I/O・連携・失敗処理

I/Oなし。Studyの意味射影をcanonical encodingしたbytesからrequest hashを作り、Codec versionをManifestで追跡する。Hashは物理File参照とは区別。

### 12.7. 検証

`DD-E11-SPEC01` strict valid/schema、`SPEC02` legacy dispatch、`SPEC03` confirmatory/inference、`SPEC04` Method/Estimand mismatch。FR-185/201、AR-034、NFR-029/036。
