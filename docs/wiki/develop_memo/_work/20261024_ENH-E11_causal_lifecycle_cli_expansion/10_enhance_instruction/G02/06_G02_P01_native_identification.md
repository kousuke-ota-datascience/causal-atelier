# ENH-E11 G02 P01 — native_identification

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G02 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G02_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G02_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 既存randomized/backdoor識別・adjustment/Graph Validatorを再利用。非識別とProof/Upstream整合を厳格化。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native/DoWhy識別、推定適格性、FD-A限定線形効果を安全に区別する。

**科学/Designの必須制約:** P1-M05のIV識別対象は未確定。FD-A識別成立と数値推定成立は別。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 既存randomized/backdoor識別・adjustment/Graph Validatorを再利用。非識別とProof/Upstream整合を厳格化。

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
| `NativeIdentificationAdapter` | `ariadne.scientific.causal_methods.identification.NativeIdentificationAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `IdentificationOutcome` | `ariadne.causal.identification.contracts.IdentificationOutcome` | Port/Value/Facade integration (no duplicate implementation) | from_evidence(evidence:ValidatedIdentificationEvidence) -> IdentificationOutcome |
| `IdentificationPort` | `ariadne.scientific.ports.causal.IdentificationPort` | Port/Value/Facade integration (no duplicate implementation) | identify(self, request:ValidatedIdentificationRequest) -> IdentificationOutcome |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約が各ClassのFields/Constructor/Public Method/Pre-Post/Failureの一次規範である。Method Adapterを本Packageが所有する場合のみそのMethodのpreflight/executeを実装し、既存run ABIは変更しない。統合専用Packageが新Adapterを創作してはならず、DomainからCLI Concreteへ逆依存しない。

**Responsibility:** Method Adapterを担当するClassは `NativeIdentificationAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。



### 3. Embedded class contracts — no external normative dependency

以下のClass定義は実装対象を自ら規定する。DD30_61/62/63へのPathはprovenanceのみであり、Coding Agentに外部DDを読んで仕様を補完させない。設計Classは実装済みを意味しない。既存実装は開始時に現実のmodule/ABIを検証し、衝突があればBLOCKEDとしてGate Freeze前に解決する。

### 3.1. `NativeIdentificationAdapter` — embedded executable class contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.identification.NativeIdentificationAdapter`。 IdentificationのMethod実行Adapter。担当Method：`P1-M01, P1-M02`。**再利用:** 既存ariadne.scientific.identification.adapter.IdentificationAdapterのrandomized/backdoor処理・証拠表現。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P1-M01` | randomized identification | 割当機構・target、proofの型付き正規化 |
| `P1-M02` | backdoor ATE | adjustment/backdoor、Graph・Design適格性 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有実装・検証節に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P101`（`P1-M01`）、`DD-E11-METH-P102`（`P1-M02`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageに明記したMethod/Science義務を優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `IdentificationOutcome` — embedded executable class contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.identification.contracts.IdentificationOutcome`。識別状態・対象Estimand・Proof・lineageを保持するValue。DoWhy内部ラベルをDomainの推定対象と混同しない。

#### フィールド

| Field | Type・制約 |
|---|---|
| `identification_id` | immutable identity |
| `estimand` | `EstimandRef`。B0/B1/DRIV等の区別 |
| `status` | `IdentificationStatus`。nonidentified/review/partialを型付け |
| `strategy, proof` | Strategy、`IdentificationProof|None` |
| `upstream, reasons` | `UpstreamHashSet, tuple[ScientificReason,...]` |

#### Constructor / Factory

`from_evidence(evidence:ValidatedIdentificationEvidence)->IdentificationOutcome`。BackendのStatus、assumption、GraphVersion、Estimand、Upstreamを意味検証して正規化。未提供Proofを生成しない。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_evidence(evidence:ValidatedIdentificationEvidence)` | `IdentificationOutcome` | pure status/proof normalization | proof/estimand/upstream不整合 |

#### 処理仕様

`NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED`を点推定許可へ自動昇格しない。緩和可能な列挙WARNだけに理由付きoverrideを許可。

#### I/O・連携・失敗処理

外部I/Oなし。実際のBackend識別計算は`IdentificationPort`、Proof/File readbackは別Port。Retry/RollbackはN/A。

#### 検証

`DD-E11-ID01` B0/B1/DRIV mislabel、`ID02` lineage差、`ID03` nonidentified override拒否、`ID04` GraphVersion再識別。FR-187/194/199、AR-029/039/043。

### 3.3. `IdentificationPort` — embedded executable class contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.IdentificationPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...
```

#### 処理仕様

IdentificationとEvidenceの意味を守り、非識別をIDENTIFIEDと偽装しない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol本体はI/Oなし。Concrete Adapterは本Packageの§3/§4で明示された所有Classのみが実装し、選択は単一MethodCapabilityPortから行う。validated request→typed outcomeを守り、外部DDの参照を実装規範の代用にしない。配置やOwnerが本Packageで決まらない場合はBLOCKEDとして新Facadeを創作しない。

#### 検証

DD-E11-ID01〜04。

## 4. Required execution — class-to-method contract (G02/P01)

1. **Entry:** G02 06/07・本PxxがFrozen、Owner Coding Authorization発行、G01 latest canonical 999 PASS、依存Pxx checkpoint SHAと実際のbranch source/lock一致を確認。不一致は開始禁止。
2. `P1-M01`のRandomized割当はDesignのrandomization evidenceとPopulation/Contrastを検査し、識別済みと推定値ありを混同しない。
3. `P1-M02`はGraph/DAGが許すBackdoor adjustmentと候補Covariate集合を照合し、post-treatment/collider/欠損Graphの無理な補完をしない。
4. 既存Scientific KernelのGraph Validator/Adjustment計算をPort経由で再利用する。既存実体のfile+callableを現場で特定し、存在しない関数の名前を作らない。新NativeIdentificationAdapterはtyped proofに正規化する層に限定。
5. **Common postcondition:** preflight→typed eligibility→selected backend/科学Kernel→validated typed outcome→G01正規StagingSink。Staging外のfinal run path、Resultと未承認の個票出力へ直接書かない。Technical exit0はScience PASSを意味しない。
6. **Prohibited:** 類似名称によるMethod置換、旧v2のSignature/Graph/Codec改変、mock-onlyによるScience PASS、unsupported CIの捏造。Backend failureと正当な科学的負結果を識別する。

**Science-specific method constraints incorporated here:** RandomizationとBackdoor識別は対応Design/Graph proofが必須。

### 設計書で定義済みの科学・型契約（このPxxに展開済みの規範）

以下は30_63の確定記述のうち本Packageに該当する部分を**本文へ複製した実装規則**であり、DDへの外部参照によって補完する規則ではない。担当外Methodの記述がある場合は担当Classを追加実装しない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M01` | randomized identification | 割当機構・target、proofの型付き正規化 |
| `P1-M02` | backdoor ATE | adjustment/backdoor、Graph・Design適格性 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

41 Method IDは固定Catalog識別子であり、各IDにOperation、Estimand、Backend/Profile、Method Config Schema、Question/Design Evidence Profile、Inference Policy、Output Artifact Profileを登録する。Class割当があることだけでは実行可能性を意味しない。`ValidatedMethodRequest`は登録済みstrict Method Schemaとcross-asset semantic Validatorの双方に成功した場合のみFactoryから生成する。

P1-M06は`e11_p1_m06_fci_method_config_v1.schema.json`、専用Question/Design internal profilesを使用する。他のMethodについてconfig/profile未定義のまま`config={}`やBackend defaultで通すことを禁止し、`METHOD_PROFILE_UNAVAILABLE`等のtyped reasonでfail-closedにする。各Method提供前に対応Gateで正規Schema、条件付き必須項目、negative fixturesを確定し登録する。Gate IDはSchema dispatchのキーにしない。

**未実測のBackend/Independent Reference/Method固有Schema/定量閾値は上記契約が未定義であることとは異なる。** 採用済みTarget/数理規則をAgent裁量で変更せず、未実測はScience/Freezeの該当判定でBLOCKEDとする。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P1-M01` Native Randomized identification／A | `DD-E11-METH-P101` | DGP-001; NEG-001, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M02` Native Backdoor identification／ATE | `DD-E11-METH-P102` | DGP-002, DGP-021; NEG-002, NEG-003 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |

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
- **必須Focused Contract:** `P1-M01`のRandomized割当はDesignのrandomization evidenceとPopulation/Contrastを検査し、識別済みと推定値ありを混同しない。 `P1-M02`はGraph/DAGが許すBackdoor adjustmentと候補Covariate集合を照合し、post-treatment/collider/欠損Graphの無理な補完をしない。 既存Scientific KernelのGraph Validator/Adjustment計算をPort経由で再利用する。既存実体のfile+callableを現場で特定し、存在しない関数の名前を作らない。新NativeIdentificationAdapterはtyped proofに正規化する層に限定。
- Test discovery/pathは40に委譲するが、何を検証するか（出力Status、Method target、reason、既存ABI不変、科学Oracleと適格Backend）は本文と§5に保持する。Unit/Contract/実Backend integrationを役割ごとに実施し、適用不能なものはReasonを明示する。
- EvidenceにClass.Module/Method/入力形、正例・負例のexpected vs actual、使用Backend version/API/seed、source+fixture SHA、effective Method/Estimand/Inference、pytest collect/command、PASS/FAIL/BLOCKEDを記録する。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P02,P03,P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical independence audit (review DRAFT)

- **Self-containment:** Class Fields/Constructor/public Method/処理は§3.1以降、Package固有順序は§4、Methodと独立検証IDは§5〜6で与える。他の06/P00/07やDDをNormative手順の補完材料にしない。
- **Remaining review:** 既存Scientific Kernelで利用可能なGraph/Adjustment APIとNativeAdapterへのBridgeの現物照合。 Method-specific Schema/Backend/独立Fixture/Science quantitative thresholdを実際に固定する。未確定部分を実装推測で埋めず、対象MethodをBLOCKEDとして扱う。
