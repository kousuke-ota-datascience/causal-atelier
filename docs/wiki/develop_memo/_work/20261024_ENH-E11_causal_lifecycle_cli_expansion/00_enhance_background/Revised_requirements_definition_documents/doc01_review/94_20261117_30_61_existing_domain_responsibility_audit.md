# 30_61 — 既存Domain責務・Class差分監査（2026-11-17）

**種別:** FLOW / DOC-01補助監査（ストック正本には昇格しない）  
**対象:** `30_detailed_design/30_61_causal_domain_ports.md`、13 Class/Protocol  
**比較基準:** `prototype/ariadne_mvp` / `a8363840450087c3c7e72e8823b1d18a95d7c733`（audit作成前HEAD）  
**監査手段:** GitHub上の既存Pythonソースを直接照合。実行・単体テスト・科学ベンチマークは実施していない。  
**判定:** `STATIC_DIFFERENCE_AUDIT_COMPLETE / DESIGN_RECONCILIATION_REQUIRED / CODING_NOT_AUTHORIZED`

## 1. 問題設定と結論

「CLIのみの拡張」から、独立した`causal.local_contract` Domainや別系統のScientific Coreを導出するのは誤り。入口の相違はInterface Adapterの設計論点である。対象となる科学的概念（Estimand/Graph/Identification/Inference/Effect）はInterfaceに依存しない。ただし、既存コードに必要な型や意味契約が存在しない部分を追加設計することまで禁止するものではない。

現行の分担は、Productのresource/lifecycle状態（`product.domain`）、因果設計とアルゴリズム（`causal`）、実行・Backend Adapter（`scientific`）、境界Port（`product.ports`）、CLI configとI/O（`interfaces.cli`）である。ただし`product.domain.graph_semantics`や`analysis_spec`にも科学的検証が実装されており、完全に一方向の分離が完成しているとみなさない。

**総合判定:** 13件のうち、完全に既存同名Classへ置換できると立証したものはない。一方、既存の型・Validation・Portへ統合すべき機能が複数存在し、13件を独立のNew Domain/Portsとして実装承認する根拠もない。以下は責務境界の**監査判定・設計上の修正要求**であり、個別Classの最終配置承認ではない。

## 2. ソースと責務の一次証拠

| 層 | 既存実装 | 実際の責務・制限 |
|---|---|---|
| Product Resource | [lineage.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/lineage.py)、[artifact.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/artifact.py)、[analysis_specification.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/analysis_specification.py) | Project/Resource identity、Artifact/Specの状態とVersion。`ResourceRef`は論理Resource ID＋任意hash、VerifiedContentではない |
| Product Graph | [graph_version.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/graph_version.py)、[graph_version_service.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/application/graph_version_service.py)、[graph_semantics.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/graph_semantics.py) | GraphVersion lifecycleと編集・確定。PAG endpoint markも検証。ただしlagの科学的意味・AR推論まで自動検証しない |
| Causal Science | [schemas.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/causal/design/schemas.py)、[treatment_effect.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/causal/inference/estimators/treatment_effect.py) | `Estimand`はATE/ATT、`CausalDesign`はtreatment/outcome等。`TreatmentEffectResult`はpoint、標準誤差、有限のci_low/ci_high |
| Scientific Adapter | [adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/scientific/identification/adapter.py)、[core_adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/scientific/core_adapter.py) | `IdentificationAdapter`は識別とdata eligibilityを`ScientificResultDescriptor`に正規化。科学計算の実装はProduct Entityと同一ではない |
| Ports / Execution | [scientific_core.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/ports/scientific_core.py)、[workflow.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/capabilities/causal/workflow.py)、[runner_registry.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/workflow/runner_registry.py) | `ScientificCorePort.run_discovery/identification/estimation/refutation/sensitivity`。StageRunnerRegistryはStageType単位で、Method/Backend/Inference適格性の完全なRegistryではない |
| Eligibility | [scientific_validation_service.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/application/scientific_validation_service.py)、[analysis_spec.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/analysis_spec.py) | 既存Estimand/Method対応とScientificStatusを検証。ただし既存supported範囲はE11全Methodではない |
| CLI/Codec | [config_schema.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/interfaces/cli/config_schema.py)、[schemas.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/product/domain/schemas.py)、[hashing.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/a8363840450087c3c7e72e8823b1d18a95d7c733/src/ariadne/infrastructure/config/hashing.py) | CLI configはversion 2.0。Product `canonical_bytes`はPython JSONに基づく独自正規化でRFC8785実装と同一と証明できない。`hash_mapping(default=str)`は任意オブジェクトを文字列化 |

## 3. 13 Class/Protocol差分・分類

分類語：**共通Value新設**＝既存Valueと責務を統合せず、共有可能な意味Valueとして追加／**拡張統合**＝既存Class/Validator/Portの意味を再利用して不足部分を追加／**新規科学型**＝既存型では情報を損失するため新しい値型が妥当／**移管**＝Domainではなく別層の責務／**境界再設計**＝現Portと用途を突き合わせて重複排除が必要。

| No. | 30_61候補 | 既存の対応Class・関数 | 確認した重複／不足 | 判定と責務Owner |
|---|---|---|---|---|
| 1 | `ContentRef` | `ResourceRef`, `Artifact`, `StoredArtifact` | 既存はProduct resource identity・storage metadata。`relative_key`安全性、verified same-fd bytes、外部File参照の包括的意味検証は別 | **共通Value新設（候補）**。内容識別は共通のtyped value、trusted FS検証はI/O adapter。Product Resourceと同一Entityにしない |
| 2 | `LocalStudySpec` | `AnalysisSpecification`, `CausalDesign`, `AnalysisSpec`, CLI config | 既存の分析仕様・Estimand/Operation検証と重複。ただしv2はATE/ATT中心、local envelopeはrun_id/Privacy/refsを含む | **拡張統合＋分割**。科学的Study/Designの共通意味型とCLI transport envelopeを分ける。v2互換を保持 |
| 3 | `GraphEvidence` | `GraphVersion`, `GraphVersionService`, `canonical_graph` | Graph kind/PAG端点/canonicalizationが既存。新要求はtemporal lag・Evidence hash・lossless round-trip。`make_revision`は既存Version管理と競合 | **拡張統合＋責務分割**。Graph意味・Evidence Valueのみ新拡張。Version生成・FIXは既存Productのauthoritative serviceと調整 |
| 4 | `IdentificationOutcome` | `IdentificationAdapter`、`ScientificResultDescriptor`、Product `Result` | status/eligibility/reasonsは存在、Estimand固有のProof・UpstreamHash・typed negativeは不足 | **新規科学型（既存結果Adapterとの統合）**。識別証拠は科学層、Product Resultは保存・所属権威 |
| 5 | `EstimatorRequest` | `EstimationInput`, `ScientificValidationService.validate_estimator_compatibility` | Method/Estimand/Eligibilityの既存検証と重複。IV/CATE・typed proof・inference requestまでの契約は不足 | **拡張統合**。共通科学適格性のValidatorとtyped validated request。二重Rule表を作らない |
| 6 | `ARConfidenceSet` | `TreatmentEffectResult.ci_low/ci_high` | 既存の有限下限・上限ではEMPTY、ALL_REAL、DISCONNECTED、無限端点をlossless表現できない | **新規科学型**。Causal inference Value、Product保存へはVersion付きCodec |
| 7 | `InferenceEvidence` | `TreatmentEffectResult`, `ScientificResultDescriptor` | 有限CIの数値は既存。一方availability/status/reason、AR set、Method別推論APIの状態はない | **新規科学型（既存の有限CIをAdapter変換）**。科学的可用性と実行・Product状態を分離 |
| 8 | `EffectOutcome` | `TreatmentEffectResult`, `ScientificResultDescriptor`, Product `Result` | 効果値・基本diagnosticsは重複。点推定有無とScience Acceptance/Inference/Lineageは独立軸が必要 | **新規科学型または既存DTOの型付き拡張**。Product `Result` Entityを複製せず明示Mapping |
| 9 | `BackendCapabilityRecord` | `ESTIMATOR_CAPABILITIES`, `StageRunnerRegistry` | Method supportの一部は既存。distribution/API signature/optional deps/probeは不足。実効環境の事実でありEffect Domain Valueではない | **移管＋拡張統合**。Application/Scientific capability registryへ。唯一のMethod能力authorityを設ける |
| 10 | `IdentificationPort` | `ScientificCorePort.run_identification` | Operation重複。既存入力はPath+dict、出力は`ScientificResultDescriptor`。新案はtyped proof request/outcome | **境界再設計**。既存Portの後継version／内部Adapterで対応。二重公開Portを無条件に採用しない |
| 11 | `EstimatorPort` | `ScientificCorePort.run_estimation` | Operation重複。既存は`output_dir: Path`、新案は`StagingArtifactSink`、typed eligibility/AR | **境界再設計**。typed Portに進化させても既存公開Contractは互換維持。新旧Portの唯一の実行経路を定義 |
| 12 | `MethodCapabilityPort` | `ESTIMATOR_CAPABILITIES`, `StageRunnerRegistry` | Stage登録はMethod適格性ではない。Method能力問合せの具体Portが既存にない | **拡張統合／新Port候補**。Method registryを一元化し、Application/Scientific boundaryへ配置 |
| 13 | `DiagnosticPort` | `ScientificCorePort.run_refutation/run_sensitivity`、`DesignDiagnostics` | 検証・診断の部分機能は既存だが、すべてのdiagnosticがrefutation/sensitivityと同義ではない | **境界再設計**。診断Operation taxonomyを揃えて既存Adapterを再利用。新Port必要性はMethodごとに確認 |

## 4. 修正要求と反証条件

| Finding | 深刻度 | 未解消事項 | この判定を覆すために必要な証拠 |
|---|---|---|---|
| D61-R01 | **BLOCKER** | `causal.local_contract`の独立構築を、CLI入口のみを理由に正当化している可能性 | 既存Product/Causal型の拡張では責務・科学的意味が保持できない具体的反例／依存図 |
| D61-R02 | **BLOCKER** | `LocalStudySpec`が科学的StudyとCLI run envelopeを混在させる | 不変条件と入出力責務が分離不要であることを示す型・call graph、既存Specとの重複回避 |
| D61-R03 | **BLOCKER** | `GraphEvidence.make_revision`が`GraphVersionService`と並列のVersion authorityに見える | Pure evidence revision とProduct persistent GraphVersion lifecycleを区別する単一Writerの契約 |
| D61-R04 | MAJOR | `BackendCapabilityRecord`がeffect domainにありruntime probeを暗黙に含む | ValueとRegistry/Probeの不変性およびownerの確定 |
| D61-R05 | **BLOCKER** | `IdentificationPort`/`EstimatorPort`が既存`ScientificCorePort`と並立する | 呼出し方向、compat bridge、single execution path、no silent estimator fallbackの契約 |
| D61-R06 | MAJOR | `EffectOutcome`とProduct `Result`への意味保存mappingが未証明 | Point/Inference/Science/Technical statusを落とさないversioned result/wire round-trip |
| D61-R07 | MAJOR | `product.domain.schemas.canonical_bytes`をRFC8785の代用と誤認する危険 | 正しいCodecの独立実装・test vector・byte一致検証 |
| D61-R08 | MAJOR | `DiagnosticPort`と既存Refutation/SensitivityのOperation範囲が未対応 | Method×Operation×Diagnostics coverageと既存Runnerの利用可否の対応表 |

**Scope上の注意:** 新規科学型（特にAR集合）を消して既存の`Result.payload_json`だけに押し込む案は不適切。逆に既存の`GraphVersion`や`Execution`のBusiness lifecycleを科学Valueにコピーする案も不適切。両者は異なる変化理由・authoritative ownerを持つ。

## 5. 判定・後続への影響

1. **確定した事実：** 現行Sourceには上表のClass/Port/Validatorが存在する。新しい13件は現行Source上の同名実装ではない。
2. **監査上の推奨：** `ContentRef`、AR集合、typed inferenceなど不足を証明できる値型を先行対象とし、既存Graph/Spec/Portとは共通の意味を再利用する。独立Local Domain全体の新設は承認しない。
3. **未決定：** 具体module path・Port改訂のABI・GraphVersion pure immutable revisionとProduct writerの調停・全Method能力表・Result mapping。ここはClass仕様書の段階で勝手にFINALとしない。
4. **必要な次工程：** 上記8 findingをArchitecture/Interface Designの正本候補と整合させる → 30_61のClass.Signature/Package配置を確定 → 30_60/62/63、23_41/42及びG01 06/07を再配線 → 独立意味照合。**現在Coding Authorizationなし。**
5. **完了条件：** 13行の差分トレースは静的監査として作成完了。8 findingと科学的/実装上の独立Verificationは未閉鎖。DOC-01全体のPASS・G01 PASSを宣言しない。

## 6. 対象資料・監査時点の再現性

上記ソースへのGitHubリンクは比較基準Commitに固定。監査対象`30_61`は`a8363840450087c3c7e72e8823b1d18a95d7c733`時点の版。以降の設計書修正Commitは別途追跡する。Repo `kousuke-ota-datascience/causal-atelier`、branch `prototype/ariadne_mvp`。検索対象は最新コードの当該Class実体・対応Adapter・Validation・Portであり、Issue/PRとRuntime science benchmarkは照合対象外。
