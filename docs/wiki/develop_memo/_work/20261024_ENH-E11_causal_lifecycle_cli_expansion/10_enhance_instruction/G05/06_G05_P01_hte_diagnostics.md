# ENH-E11 G05 P01 — hte_diagnostics

### G05現行個票出力契約 — Owner 2026-11-21改訂

- **機能/範囲:** FR-195、NFR-031、P2-15。一般ユーザーがlocal Linux ext4/XFSで個票中間データを出力する場合、実行者がversioned Studyの`privacy.row_export_requested=true`で単独明示opt-inする。独立した人的承認者・暗号署名・鍵管理・承認失効はこの範囲に要求しない。
- **Privacy/OS:** EUIDが所有するprivate TrustedRoot、root/staging 0700、row file 0600、owner/mode/local ext4-XFS/symlink/dirfdとsame-FSを検査。rootと同一UIDのプロセスは隔離できない。個票は`RESTRICTED_ROW_LEVEL`に分類。
- **Eligibility:** `Study.privacy.row_export_requested=true` ∧ private verified root/UID ∧ Method別`ApprovedRowSchema`/許可列・行ID・row/byte/memory上限 ∧ 同一runのG01 staging。初期denyはPrivacy exit3、Source反復0・row bytes0、暗黙aggregate fallback無し。通常集計は個票権限と独立。
- **内部Port:** `LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase`に署名Verifier依存無し。`e11-local-study/1`には`privacy.policy_ref`を設けない（未知キーはstrict reject）。
- **Writer:** 既決`RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`を維持。実行条件成立後だけread_rows、G01 Sink以外へ書かない。
- **Publication/test:** `row_effects.parquet`／`application/vnd.apache.parquet`のみG01 Publisher/Readerが原子的にpublish・readback。Stage/Seal/Publish前にroot/UID/mode/FS/runを再検査、障害後にCOMMITTEDを偽装しない。個票値はaggregate Result/Manifest/CLI/logsへ出さない。未検証事項：Method RowSchema、実FS/Parquet、07独立Science/Privacy Test、Freeze、Coding Authorization。


**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G05 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G05_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G05_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。

**Scope:** Local intermediate row artifact only. Science CATE/DRIVの対象は変更せず、行出力はStudyの`privacy.row_export_requested=true`という単独opt-inとnonroot private rootを満たす場合だけ。


Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** G04推定器を再実装せずMethod別support/calibration/uncertaintyを型付き診断。算法/Result owner不足ならDESIGN_GAP。

### 2A. 既存SourceとRow Release authorityの境界（`2cf28f59a324`）
- **既存:** `src/ariadne/product/application/graph_version_service.py`の`GraphVersionService.create(...)`/`fix_graph(...)`はProduct GraphVersion Authorityであり、Local CLIが同名Publisher/Version writerを作って代替しない。`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(input_: EstimationInput, output_dir: Path)`は旧Path API、HTEと認可済Parquet Writerの実装済み証拠ではない。
**Input/output:** Studyは`e11-local-study/1`で`privacy.policy_ref`を持たない。run/Study/Data/Method ref hash、private ext4/XFS root、G01 stagingとReader一致を確認し、旧v2と混同しない。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | 禁止・negative条件 |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`＋nonempty reason、`schema_dispatch.graph=null`。Backend失敗との混同は禁止 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Effect `result.json`禁止。識別negativeもtyped、Graph/Design/Estimand/Proof hashを照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。point欠落はnull＋理由で表し、非識別への推定値偽装禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effect再発行禁止。上流Effect/Graph/Design hash、seed・適用条件の検証が必須 |


## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | Port/Value/Facade integration (no duplicate implementation) | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome |

**Class boundary:** LocalPrivacyPolicyがStudy・EUID/TrustedRoot・Method ApprovedRowSchemaを検証する。RowWriter/Factoryは許可後Serializerだけを所有し、G01 Publisherは変更しない。

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

**Method steps:** P02は拒否時Source反復0を保証。P03は許可されたRowSchema/column orderでmax_rows+1とbyte capを検査し、G01 sinkへstage。P04はOS/FS正常・異常双方をE2E。



## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Scientific boundary:** G04のCATE(x)／DRIV heterogeneous IV coefficientは異なるEstimand。HTE support/uncertainty、Method別oracleと推論の可用性を混同せず、個票Releaseの可否を科学Statusへ偽装しない。

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
**Independent test:** Study true正例、false/未指定の拒否、wrong UID/owner/mode/FS/symlink、許可Method RowSchema、Source iteration count、row/byte cap、atomic commit/Readerと旧v2回帰を独立実測。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03,P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit unresolved design — freeze barrier

**Document independence:** Class Fields/Constructor/Methodは§3、専用処理は§4、検証/負例は§6で完結。Owner決定が無い要件は仮構実装で埋めない。

**BLOCKED before Freeze:** HTE calibration metricとholdout policy/必要Science Oracle、G04推論契約。 これらは本Pxxに係る未確定決定であり、他Pxx/07/設計書を読んで推定してはならない。G05のRow出力をG01〜G04に遡及して許可しない。


### SIM-01 — local FS evidence requirements trimmed by Owner (2026-11-21)

This Gate's privacy threat boundary is a normal unprivileged Linux EUID and a local ext4/XFS filesystem. Enforce same-EUID ownership, private root/staging 0700, row file 0600, verified safe dirfd/O_NOFOLLOW/path and same-filesystem Publisher, Method-specific allowed schema/row/byte limits and the single explicit Study opt-in (`privacy.row_export_requested=true`); no additional CLI row-authorization flag. **Remove as mandatory implementation/test features** independent POSIX ACL/xattr extraction/digest, statx mount-ID/namespace visibility attestation, CI/container heuristic/environment classification. This is not a guarantee against another process running with the same UID or a privileged OS administrator. Real ownership/modes/FS/path failures are still negative tests; no row source iteration before eligibility. G01 no-clobber Publisher/Reader and G05 independent science tests remain unchanged. Do not implement a key/Trust Store or signed prior approval. Reconciliation authority: combined_review/129 + /131. Independent Test NOT_RUN; Gate NOT_FROZEN.


## S02-01/02/05 現行契約の確認（2026-11-22、Owner採用）

本書が規範とする現行E11 Local個票出力の唯一の実行者opt-inは`ValidatedStudy.privacy.row_export_requested=true`である。CLI上の追加のrow-export許可flag、`LocalRunContext.cli_row_flag`、`privacy.policy_ref`、署名Verifier/鍵/独立Approverは実装しない。正規署名は`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`。Study trueのみで個票を無条件許可するわけではない。必ずnonroot実効UID同一所有者・private ext4/XFS TrustedRoot・owner-only mode・安全なdirfd/relative path・Method別ApprovedRowSchemaとallowed ordered columns、row/byte/memory制限、同一run G01 stagingをAND検証する。有効Studyで`row_export_requested=false`またはroot/Method等のPrivacy不適格はexit3。必須`row_export_requested`の省略・型違反はStudy構造検証エラー(exit2)、廃止CLI row許可flagは未知Option(exit2)。いずれも個票Source反復0・row bytes0、aggregateへ自動格下げせず、log/Manifestに個票値を流出させない。検証後もSeal/Publish/readbackまでRoot/lineage driftを拒否し、既存Product v2は変更しない。独立試験ではtrue/false/省略、未知`policy_ref`、廃止CLI flag、Wrong UID/Root、unapproved column/row/byte、WriterとReaderの正負例を検証する。本契約はS02-01/02/05の**実装指示本文**であり、科学的Test PASSやCoding Authorizationではない。
