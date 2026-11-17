# ENH-E11 G08 P03 — two_sls_ar

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G08 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G08_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G08_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** B0 Q=[1], B1 Q=[1,C]。Y−βA~Q+ZのHC1 χ²(1)全実数AR反転、EMPTY数学集合とFAILEDは別。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Sharp/Fuzzy RDDとB0/B1 IV/2SLSを局所Estimand・弱IV AR集合付きで提供する。

**科学/Designの必須制約:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** B0 Q=[1], B1 Q=[1,C]。Y−βA~Q+ZのHC1 χ²(1)全実数AR反転、EMPTY数学集合とFAILEDは別。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `TwoSlsAdapter` | `ariadne.scientific.causal_methods.iv.TwoSlsAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `ARConfidenceSet` | `ariadne.causal.inference.confidence_sets.ARConfidenceSet` | Port/Value/Facade integration (no duplicate implementation) | from_components(level,components,evidence) / contains(beta:float) / to_payload()/from_payload(payload) |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。Constructor/Field/公開MethodとARConfidenceSetの境界は本Pxx§3.1以降の埋込Class契約が規範。外部DDはProvenanceのみ、未知のConcrete型を推測しない。

**Responsibility:** Method Adapterを担当するClassは `TwoSlsAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class-level contracts (normative)

Class Fields/Constructor/Method/Pre/Post/Failureは以下で本Package内に定義する。外部DDはprovenanceに限り、Agentが参照しなければ実装できない仕様を残さない。Designed Module≠Source実装済み。ABIはSource照合する。

### 3.1. `TwoSlsAdapter` — full fields/constructor/methods

#### 1.20.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.iv.TwoSlsAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M10, P3-M11`。**再利用:** 共通IV適格性を再利用、B0/B1識別対象・AR反転を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.20.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.20.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.20.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.20.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M10` | B0 just-identified LATE | zero controls、single Z/A、robust covariance、AR |
| `P3-M11` | B1 additive linear IV slope | single binary Z/A、predeclared C、robust AR |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Package内の数理定義とMethod別科学契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.20.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.20.7. 検証

`DD-E11-METH-P310`（`P3-M10`）、`DD-E11-METH-P311`（`P3-M11`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageの各Method DGP/NEG/REF一覧を優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `ARConfidenceSet` — full fields/constructor/methods

#### 3.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.confidence_sets.ARConfidenceSet`。Anderson–Rubin反転の損失ない数学集合を表すValue。

#### 3.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `confidence_level` | `float` | 0 < level < 1 |
| `components` | `tuple[ExtendedRealInterval,...]` | EMPTYは0件。finite/±∞をtagged endpointsで表現 |
| `topology` | `SetTopology` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED |
| `inversion_evidence` | `ContentRef` | 成功した数学的反転の証拠 |

#### 3.1.3. Constructor / Factory

`from_components(level,components,evidence)->ARConfidenceSet`：finite endpoint、順序、open/closed、重複/接触区間の数学的正規化。

#### 3.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_components(level,components,evidence)` | `ARConfidenceSet` | pure set normalization | invalid endpoint/topology |
| `contains(beta:float)` | `bool` | endpoint条件で判定 | NaN/invalid β |
| `to_payload() / from_payload(payload)` | JSON / Value | Lossless roundtrip | malformed topology / JSON非有限数値 |

#### 3.1.5. 処理仕様

Topology分類はEMPTY→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDED。ALL_REALは(-∞,+∞)一成分。∞端点はopen、双方openで接触する2区間は1点gapを残すため結合しない。数学的EMPTYは`AVAILABLE + inversion_evidence`と両立、計算失敗`FAILED+reason`とは別。B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件が成立する場合`T_AR(βhat)=0`により非空が必要となり、**Method別validator**でEMPTYを拒否。

#### 3.1.6. I/O・連携・失敗処理

Valueはpure。JSONのNaN/Infinity数値は禁止、tagged endpointで表現。実AR反転・HC1・coverageはMethod Adapterと独立科学検証に委譲。

#### 3.1.7. 検証

`DD-E11-AR01` 5分類、`AR02` generic EMPTYとjust-identified条件分離、`AR03` lossless roundtrip、`AR04` null reason、`AR05` confirmatory fail-closed。FR-202、AR-040、NFR-036。

### 3.3. `InferenceEvidence` — full fields/constructor/methods

#### 3.2.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。

#### 3.2.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### 3.2.3. Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### 3.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 3.2.5. 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### 3.2.6. I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 3.2.7. 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

### 3.4. `EffectOutcome` — full fields/constructor/methods

#### 4.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。

#### 4.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics` | `tuple[DiagnosticRef,...]`。Method別typed診断参照 |
| `method_evidence, upstream_hashes` | typed Backend evidenceとlineage |

#### 4.1.3. Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### 4.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_result_payload()` | typed Result payload | pure typed result projection。JCS byte encodingは共通Codec | incompatible schema/estimand |

#### 4.1.5. 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### 4.1.6. I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 4.1.7. 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。

## 4. G08/P03 required scientific and code execution

1. **Preconditions:** G08 Frozen06/07/Pxx、G01/G02 upstream canonical 999、Owner Coding Authorization、fixed candidate Source/lock、Pxx checkpointsを照合。Method/Design/IV assumptions/Estimand/Inference/Backend selectionをpreflightで検証。
2. `P3-M10` B0はQ=[1]、single binary Z/A、just-identified no-adjustment complier LATE。`P3-M11` B1はQ=[1,C]（事前指定covariates C）、single excluded binary Z、single endogenous Aのadditive linear IV structural slope。
3. 2SLSはfirst-stage/reduced form/2nd-stageとinstrument support/partial rankを検証し、推定値のVarianceは採用されたheteroskedasticity-robust methodを使用。通常Wald CIをweak-IV-robustと偽称しない。
4. ARのH0(β)は各βでY−βA ~ Q+ZのZ係数=0をHC1/χ²(1)で検定。残差化と全実数のquadratic inversion/bracketing/無限tail判定を実装し、有限GridだけでALL_REAL/UNBOUNDED/DISCONNECTED/EMPTYを宣言しない。
5. Q Full Rank、HC1 varianceと退化を分離。非退化B0/B1 just-identified（gA≠0, Var_HC1(βhat)>0）ではβhatでAR test=0となり集合は非空。見かけのEMPTYはSCIENCE_INCONSISTENTを疑い、数値失敗やrank不足と数学的EMPTYを混同しない。
6. AR setの`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`と端点Infinity/開閉/Confidence levelをARConfidenceSetがlosslessに保持。Invalid IV仮定はARを実行しただけで検証済みとしない。
7. **Dataflow:** Typed ValidatedMethodRequest→Method Adapter eligibility→selected numeric kernel/effective Backend→EffectOutcome/ARConfidenceSet→G01 StagingSink/Atomic Publisher/Reader。外部Backend model objectやRaw row/SecretsをResultへ含めない。
8. **Typed failure:** Zero denominator, rank/HC1 variance degeneracy, unsupported CI, invalid design, optional backend unavailable, numerical FAILED, legitimate scientific weak IVを明確に区別。Technical exit0はScience PASSでない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M10` B0 just-identified 2SLS／binary Z/A | `DD-E11-METH-P310` | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M11` B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | `DD-E11-METH-P311` | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Proof boundary:** Method別§5のDGP/NEG/REF/ACは独立検証義務。実数全体のHC1 AR inversion・弱IV退化・LATE/structural slopeの区別は§4で規定。独立Oracleの不在、FWER=.05/K/R/Compute/MC-SE/coverageの未決はBLOCKEDであり、Backend自身の出力や有限GridからScience PASSを作らない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g08/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Deterministic/independent scientific proof matrix

- §5の各Method DGP/NEG/REF/DD/ACを保持。Positive DGPとindependent ReferenceをBackend予測から作らない。
- **Mandatory focused cases:** `P3-M10` B0はQ=[1]、single binary Z/A、just-identified no-adjustment complier LATE。`P3-M11` B1はQ=[1,C]（事前指定covariates C）、single excluded binary Z、single endogenous Aのadditive linear IV structural slope。 2SLSはfirst-stage/reduced form/2nd-stageとinstrument support/partial rankを検証し、推定値のVarianceは採用されたheteroskedasticity-robust methodを使用。通常Wald CIをweak-IV-robustと偽称しない。 ARのH0(β)は各βでY−βA ~ Q+ZのZ係数=0をHC1/χ²(1)で検定。残差化と全実数のquadratic inversion/bracketing/無限tail判定を実装し、有限GridだけでALL_REAL/UNBOUNDED/DISCONNECTED/EMPTYを宣言しない。 Q Full Rank、HC1 varianceと退化を分離。非退化B0/B1 just-identified（gA≠0, Var_HC1(βhat)>0）ではβhatでAR test=0となり集合は非空。見かけのEMPTYはSCIENCE_INCONSISTENTを疑い、数値失敗やrank不足と数学的EMPTYを混同しない。 AR setの`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`と端点Infinity/開閉/Confidence levelをARConfidenceSetがlosslessに保持。Invalid IV仮定はARを実行しただけで検証済みとしない。
- Unit: domain/Estimand/AR set serialization/edge cases; Contract: Class.Method、typed outputs、result discriminator/lineage; Integration: 実Backend、IV instrument/data support、real Publisher/readback、旧Product v2回帰。Weak IV / negative assumptions/HC1 confidence inversionは独立算出Referenceと照合。
- Environment/Backend/API、Source+fixture+lock SHA、DGP/negative、実行Command/Collection、Expected/Observed、Scientific vs Technical outcomeをEvidence化。未確定Oracle/quant K/R/coverageならBLOCKED、Science PASSは出さない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Freeze-critical standalone gaps

本PackageはClass Field/Constructor/Methodを§3、数理処理順序/分岐を§4、科学的DGP/NEG/REFとAcceptanceを§5〜6で内部定義する。**残未決:** HC1 AR推論の独立数理Referenceと全実数集合算法/退化、Pilot coverage判定。 P3-M10/M11で有限gridだけのAR反転を実装することは禁止。OwnerがFreeze時に独立数理/Backend/ConfigとScience受入条件を明示的に判定する。
