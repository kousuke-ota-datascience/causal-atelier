# ENH-E11 G05 P01 — hte_diagnostics

### 現行G05個票出力契約 — Owner 2026-11-21

- **要件:** FR-195／NFR-031／P2-15。一般ユーザーによるローカル分析中間Artifact。第三者Approver、署名、鍵、失効、issuer registryの承認プロセスを要求しない。「独立承認」ではなく「実行者の明示的opt-in」と定義する。
- **対象環境:** Linux非root実効UID・ext4/XFS local filesystem。UID=root owner、root/staging 0700・Parquet 0600、ACL/mount/namespace/symlink/dirfd・same-FSを検証。管理者・同一UID processは本Threat Modelで隔離できない。
- **許可AND:** `Study.privacy.row_export_requested=true` ∧ CLI `--allow-row-level-export` ∧ `RESTRICTED_ROW_LEVEL` ∧ 対象Methodの`ApprovedRowSchema`/ordered allowlist/row ID・row/byte/memory上限 ∧ private EUID-owned TrustedRoot ∧ same-run G01 StagingSink。未認可ならexit3、RowSource反復0・row bytes0、暗黙aggregate fallback無し。
- **既決APIの限定変更:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase.__init__`から署名Verifier依存を除く。`e11-local-study/1`は維持し任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **維持するClass:** `RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`。Sourceは全許可成立後だけ反復。WriterはG01公開責務を複製しない。
- **出力:** `row_effects.parquet`／`application/vnd.apache.parquet`／`RESTRICTED_ROW_LEVEL`。G01のみstaging/atomic no-clobber/Manifest/Marker/Reader。Stage/Seal/Publish前にroot/UID/ACL/mount/runを再検査。後段異常でprivate stagingの過去bytes0を主張せず、公開成功にもしない。Result/Manifest/stdout/stderr/logに行値なし。
- **未完了:** Method別RowSchema/制約数値、実ext4/XFS/ACL/mount、Parquet ABI、科学Reference、独立07実測。Freeze・Coding Authorization・999は未実施。変更のAuthorityは`combined_review/129_20261121_dec_g05_local_row_export_simplification.md`、過去PREP-02/03/04.2は履歴として保持。


**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G05 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G05_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G05_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。

### 2A. 既存SourceとRow Release authorityの境界（`2cf28f59a324`）
- **既存:** `src/ariadne/product/application/graph_version_service.py`の`GraphVersionService.create(...)`/`fix_graph(...)`はProduct GraphVersion Authorityであり、Local CLIが同名Publisher/Version writerを作って代替しない。`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(input_: EstimationInput, output_dir: Path)`は旧Path API、HTEと認可済Parquet Writerの実装済み証拠ではない。
- **現行G05実装条件:** Study＋CLI両方の明示opt-in、実効EUID/private root、Method別RowSchema/上限。初期denyは行生成0、stage後異常はCOMMITTED無し。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | Port/Value/Facade integration (no duplicate implementation) | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent of external DD)

このPxxの実行に必要なClassのField/Constructor/Method/Process/Failureを以下に内包。外部DDはTraceabilityのみ。現行SourceとのABI差分は開始時に確認し、欠陥ならOwnerレビューに戻す。

### 3.1. `EffectOutcome` — normative implementation contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。

#### フィールド

| Field | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `result_id, estimand` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `point_availability, point_value` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `inference` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `science_acceptance` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `diagnostics` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `method_evidence, upstream_hashes` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

#### Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### メソッド

| Signature | Return | 処理と副作用 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `to_result_payload()` | typed Result payload | pure typed result projection。JCS byte encodingは共通Codec | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

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

| Field | Type | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `availability` | `InferenceAvailability` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `kind` | Method-specific enum | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `reason` | `ScientificReason|None` | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `method_config` | typed config | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

#### Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### メソッド

| Signature | Return | 処理と副作用 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---|---|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

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

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**現行G05個票出力条件:** StudyとCLIの二重opt-in、実効一般Linux UID所有のprivate ext4/XFS rootとMethod別承認済みRowSchema/列・行・byte上限のAND。初期deny時にsource反復せずexit3。既存WriterとG01 Publisher/Readerのみを使用。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
|---| Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| unit | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| contract | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| integration | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |
| scientific evidence | Study＋CLI double opt-in、一般Linux EUID/private ext4/XFS、Method別RowSchemaと列行byte cap、初期deny時source反復0・row bytes0、G01 readback正負例 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g05/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. G05 privacy and evidence test contract

- 必須の受入条件は§4の各分岐、§5のScience/Method依存、§6のunit/contract/実filesystem integrationで個別に判定する。
- CATE supportはTreatment×X/Wのデータ範囲と推定対象のSupportに基づき、Overlap/Effective Sample/CalibrationとUncertaintyを混同せず別Metric/Statusとして計算。 Calibration/Coverage評価は事前指定Holdoutまたは独立SimulationとEstimator/Backendのvalid inferenceに限定。適格な標本数、group size、CI availabilityを記録。 G04のCATE Resultを入力として検証し、Method固有nuisanceや数値Estimatorを再実装しない。aggregateだけ返し、G05/P02の独立認可なしに個票値を作らない。
- **現行G05実装条件:** Study＋CLI両方の明示opt-in、実効EUID/private root、Method別RowSchema/上限。初期denyは行生成0、stage後異常はCOMMITTED無し。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03,P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit unresolved design — freeze barrier

**Document independence:** Class Fields/Constructor/Methodは§3、専用処理は§4、検証/負例は§6で完結。Owner決定が無い要件は仮構実装で埋めない。

**BLOCKED before Freeze:** HTE calibration metricとholdout policy/必要Science Oracle、G04推論契約。 これらは本Pxxに係る未確定決定であり、他Pxx/07/設計書を読んで推定してはならない。G05のRow出力をG01〜G04に遡及して許可しない。

