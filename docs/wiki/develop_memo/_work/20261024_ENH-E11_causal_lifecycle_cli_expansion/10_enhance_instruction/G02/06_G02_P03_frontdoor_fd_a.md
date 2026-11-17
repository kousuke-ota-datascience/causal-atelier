# ENH-E11 G02 P03 — frontdoor_fd_a

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G02 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G02_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G02_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 単一Mediator FD-Aの識別仮定と限定二段階線形数値を別契約で実装。一般Frontdoor Formulaへの拡張禁止。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native/DoWhy識別、推定適格性、FD-A限定線形効果を安全に区別する。

**科学/Designの必須制約:** P1-M05のIV識別対象は未確定。FD-A識別成立と数値推定成立は別。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 単一Mediator FD-Aの識別仮定と限定二段階線形数値を別契約で実装。一般Frontdoor Formulaへの拡張禁止。

### 2A. 既存SourceとのABI境界（HEAD `2cf28f59a324`で実体を確認）
- **実在する公開API:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_identification(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]`は`src/ariadne/scientific/identification/adapter.py`の`IdentificationAdapter.run(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]`へ委譲する。後者の既存Randomized/Backdoor処理を再利用する。DoWhy IV/Frontdoor数値推定/MethodCapabilityRegistryの存在は、このABIだけからは導けない。
- **旧と新は異なる契約:** 上記`run(..., output_dir:Path)`は既存Productのpath-based API。`IdentificationPort.identify(ValidatedIdentificationRequest)->IdentificationOutcome`、`EstimatorPort.estimate(..., *, sink:StagingArtifactSink)->EffectOutcome`はE11の**設計中**の型付きPortであり、既存実装済みと仮定しない。既存旧API/旧DTO/旧Path Writerを変更・無検証cast・新型付きPortから直接公開先へ出力することは禁止。共通の純粋Scientific Kernelを通す互換Bridgeで、旧呼出しを不変に保ち、E11側は検証済Request/typed responseとstaging sinkで完結させる。
- **Ownership:** G01で設ける共通Local Facade/Registry/Publisher/Reader/GraphVersion契約を各Packageが再定義しない。本Packageで新設するAdapterだけを§3/4に従い実装。実Sourceとの署名差・Facade owner未定・Backend config未承認は`BLOCKED_CONTRACT_AMBIGUITY`としてCoding開始前に報告し、外部設計から推測して署名を補完しない。

### 2B. Operation別Artifact/Schema/Publisher契約（実行規範）
| Operation | 成功時に必須 | 禁止・負例 |
|---|---|---|
| DISCOVER | `study.json`、`status.json`、Graph生成時`graph.json` | `result.json`禁止。Graph無しの正当な科学負例は`diagnostics.json`＋非空reason、`schema_dispatch.graph=null`。Backend技術失敗を科学的negativeに変換しない |
| IDENTIFY | `study.json`、`status.json`、`identification.json` | `result.json`禁止。識別/非識別ともGraph・Design・Estimand・Proofのhashを照合する |
| ESTIMATE | `study.json`、`status.json`、`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。無推定のpointはnull＋typed reason、仮の推定値禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`、`status.json`、`diagnostics.json` | Effect再発行禁止。元Effect/Graph/Design hash、seed、適用条件を必ず照合 |

全Operationで`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）を必須とし、両者はartifact inventory外。Inventoryには実Artifactの相対POSIX key・SHA256・bytes size・MediaType・Privacyを列挙。`schema_dispatch.result`はESTIMATE以外null。Readerはcommit marker→manifest実bytes hash→artifact bytes/hash/size→Operation別必須/禁止・upstream content hashを同一TrustedRoot内で検査する。`request_hash=SHA256(JCS(validated typed Study JSON))`、manifestは自己hashを持たず、markerがmanifestの実bytes hashを保持する。Stageのみからatomic no-clobber publishし、既存G01のPublisher/Readerを再利用。行レベルParquetの作成はG05の独立事前承認検証以前は禁止。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `FrontdoorLinearAdapter` | `ariadne.scientific.causal_methods.frontdoor.FrontdoorLinearAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | Port/Value/Facade integration (no duplicate implementation) | validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy) -> ValidatedEstimatorRequest |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約が各ClassのFields/Constructor/Public Method/Pre-Post/Failureの一次規範である。Method Adapterを本Packageが所有する場合のみそのMethodのpreflight/executeを実装し、既存run ABIは変更しない。統合専用Packageが新Adapterを創作してはならず、DomainからCLI Concreteへ逆依存しない。

**Responsibility:** Method Adapterを担当するClassは `FrontdoorLinearAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。



### 3. Embedded class contracts — no external normative dependency

以下のClass定義は実装対象を自ら規定する。DD30_61/62/63へのPathはprovenanceのみであり、Coding Agentに外部DDを読んで仕様を補完させない。設計Classは実装済みを意味しない。既存実装は開始時に現実のmodule/ABIを検証し、衝突があればBLOCKEDとしてGate Freeze前に解決する。

### 3.1. `FrontdoorLinearAdapter` — embedded executable class contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.frontdoor.FrontdoorLinearAdapter`。 EstimationのMethod実行Adapter。担当Method：`P1-M07`。**再利用:** 既存CausalDesign・回帰推定器を再利用。数値FD-A固有契約を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M07` | restricted FD-A ATE | 線形Mediator/Outcomeモデルとno direct path仮定、別Reference・CI |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有実装・検証節に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P107`（`P1-M07`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageに明記したMethod/Science義務を優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EstimatorRequest` — embedded executable class contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EstimatorRequest`。Identification proofが適格な場合だけEstimatorへ渡すRequest Value。

#### フィールド

| Field | Type・制約 |
|---|---|
| `method_id, estimand_family` | Method×target一致 |
| `identification_ref` | 上流証拠参照 |
| `question/design/graph/dataset_hashes` | 完全な上流digest集合 |
| `method_config, inference_request` | Method/Inference適格なtyped config |

#### Constructor / Factory

`validate_against(identification,design,policy)->ValidatedEstimatorRequest`は入力と上流証拠を照合する型付きvalidator。Validation前の生RequestをAdapterへ送らない。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy)` | `ValidatedEstimatorRequest` | pure eligibility check | scientific negative / schema validation区別 |

#### 処理仕様

Method-specific assumptions、Mediator/Instrument/support、Data Eligibility、Graph/Design/Question/Dataset hash全一致、CI要求を検証。不適格は`ScientificNegativeOutcome`としてBackend未呼出。Path/schema mismatchはtechnical validationとする。

#### I/O・連携・失敗処理

Value自身はI/Oなし。ScientificValidationServiceの既存適格性規則を共通pure policyとして再利用する。実Estimator I/O/Artifactは`EstimatorPort.estimate(...,sink)`を通す。

#### 検証

`DD-E11-ID01〜04`およびMethod固有Negative Tests。

### 3.3. `EstimatorPort` — embedded executable class contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.EstimatorPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...
```

#### 処理仕様

識別・Method適格なRequestのみ実行し、ArtifactをStagingSinkへ限定。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol本体はI/Oなし。Concrete Adapterは本Packageの§3/§4で明示された所有Classのみが実装し、選択は単一MethodCapabilityPortから行う。validated request→typed outcomeを守り、外部DDの参照を実装規範の代用にしない。配置やOwnerが本Packageで決まらない場合はBLOCKEDとして新Facadeを創作しない。

#### 検証

DD-E11-EFF01〜05。

### 3.4. `EffectOutcome` — embedded executable class contract

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

## 4. Required execution — class-to-method contract (G02/P03)

1. **Entry:** G02 06/07・本PxxがFrozen、Owner Coding Authorization発行、G01 latest canonical 999 PASS、依存Pxx checkpoint SHAと実際のbranch source/lock一致を確認。不一致は開始禁止。
2. `P1-M07`はFrontdoor一般識別(`P1-M04`)と異なる限定された線形二段階回帰。単一Mediator、明示no-direct-path、両回帰のcovariate/design、交互作用有無と有効DGPを検査する。
3. 適格なDGPでのみMediator slope×Outcome slopeをeffectとする。一般Graphから二段階回帰を自動許可せず、二段階係数/標本/推論有無/Assumptionを別Evidenceとして保存する。
4. 識別成功だけで数値推定可能とせず、CI未提供/未実証は`POINT_ONLY`またはtyped unavailable。Method別REF-E04/DGP-005で独立数値照合する。
5. **Common postcondition:** preflight→typed eligibility→selected backend/科学Kernel→validated typed outcome→G01正規StagingSink。Staging外のfinal run path、Resultと未承認の個票出力へ直接書かない。Technical exit0はScience PASSを意味しない。
6. **Prohibited:** 類似名称によるMethod置換、旧v2のSignature/Graph/Codec改変、mock-onlyによるScience PASS、unsupported CIの捏造。Backend failureと正当な科学的負結果を識別する。

**Science-specific method constraints incorporated here:** General Frontdoor識別とは異なるFD-A線形数値推定を対象。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P1-M07` Frontdoor two-stage regression／ATE | `DD-E11-METH-P107` | DGP-005; NEG-004, NEG-005 | REF-I02, REF-E04 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED |

**Proof boundary:** 本Pxx§5のDGP/NEG/REF/ACは全件独立科学検証義務である。IDの列挙は実Fixture/独立Reference生成済みやPASSを意味しない。Backend自己出力を真値としない。FWER=.05・K/R/Compute/MC-SE/CI coverageと閾値はFreeze前に決定し、未確定はBLOCKED。別文書を読んで値を推測・補完しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g02/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Package-specific executable evidence

- 対象MethodとDD IDは§5の各行を一つも省略しない。DGP/NEG/REFの名前は検証対象IDであり、**実測/fixtureが作成済みという主張ではない**。
- **必須Focused Contract:** `P1-M07`はFrontdoor一般識別(`P1-M04`)と異なる限定された線形二段階回帰。単一Mediator、明示no-direct-path、両回帰のcovariate/design、交互作用有無と有効DGPを検査する。 適格なDGPでのみMediator slope×Outcome slopeをeffectとする。一般Graphから二段階回帰を自動許可せず、二段階係数/標本/推論有無/Assumptionを別Evidenceとして保存する。 識別成功だけで数値推定可能とせず、CI未提供/未実証は`POINT_ONLY`またはtyped unavailable。Method別REF-E04/DGP-005で独立数値照合する。
- Test discovery/pathは40に委譲するが、何を検証するか（出力Status、Method target、reason、既存ABI不変、科学Oracleと適格Backend）は本文と§5に保持する。Unit/Contract/実Backend integrationを役割ごとに実施し、適用不能なものはReasonを明示する。
- EvidenceにClass.Module/Method/入力形、正例・負例のexpected vs actual、使用Backend version/API/seed、source+fixture SHA、effective Method/Estimand/Inference、pytest collect/command、PASS/FAIL/BLOCKEDを記録する。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Freeze-critical independence audit (review DRAFT)

- **Self-containment:** Class Fields/Constructor/public Method/処理は§3.1以降、Package固有順序は§4、Methodと独立検証IDは§5〜6で与える。他の06/P00/07やDDをNormative手順の補完材料にしない。
- **Remaining review:** FD-A数値推定の条件付き共変量構造、Variance/CI、Backend版/Reference妥当性。 Method-specific Schema/Backend/独立Fixture/Science quantitative thresholdを実際に固定する。未確定部分を実装推測で埋めず、対象MethodをBLOCKEDとして扱う。
