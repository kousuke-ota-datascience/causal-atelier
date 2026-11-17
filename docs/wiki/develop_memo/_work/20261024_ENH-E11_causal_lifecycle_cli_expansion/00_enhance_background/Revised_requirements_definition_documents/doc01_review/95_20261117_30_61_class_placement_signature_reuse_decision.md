# 30_61 — Class配置・Method署名・既存実装再利用の決定（2026-11-17）

**文書種別:** FLOW / DESIGN DECISION（Stock正本へ昇格しない）  
**比較Source基準:** `prototype/ariadne_mvp`、`a8363840450087c3c7e72e8823b1d18a95d7c733`  
**先行監査:** [94_既存Domain責務差分監査](94_20261117_30_61_existing_domain_responsibility_audit.md)  
**決定状態:** `CLASS_MODULE_SIGNATURE_REUSE_SELECTED / IMPLEMENTATION_NOT_STARTED / GATE_06_07_DRAFT / CODING_NOT_AUTHORIZED`

## 1. 13対象の決定表

| Class / Protocol | 完全修飾Module（Class名を除く） | 再利用方式 | 重複させない既存Authority | Public Method Signature | Class仕様Owner |
|---|---|---|---|---|---|
| `ContentRef` | `ariadne.shared.content_ref` | NEW shared value | ResourceRef/Artifactと別のbytes identity | `from_payload(payload: Mapping[str, JsonValue]) -> ContentRef` | 30_60 §11 |
| `LocalStudySpec` | `ariadne.interfaces.cli.local_causal.study` | NEW CLI DTO | CausalDesignとAnalysisSpecificationを科学的意味Ownerとして再利用 | `validate_local_invariants(self) -> tuple[Reason,...]` | 30_60 §12 |
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence` | NEW scientific value | graph_semanticsを再利用、GraphVersionServiceは唯一のVersion writer | `from_canonical_json(raw: bytes) -> GraphEvidence; canonical_payload() -> Mapping[str, JsonValue]` | 30_61 §1 |
| `IdentificationOutcome` | `ariadne.causal.identification.contracts` | NEW typed evidence | IdentificationAdapterとProduct Resultへの変換を保つ | `from_evidence(evidence: ValidatedIdentificationEvidence) -> IdentificationOutcome` | 30_61 §2 |
| `EstimatorRequest` | `ariadne.causal.inference.contracts` | EXTEND pure eligibility | 既存ScientificValidationServiceの判定規則を共通policyに統合 | `validate_against(self, identification: IdentificationOutcome, design: CausalDesign, policy: EstimandEligibilityPolicy) -> ValidatedEstimatorRequest` | 30_61 §2 |
| `ARConfidenceSet` | `ariadne.causal.inference.confidence_sets` | NEW scientific value | 既存有限CIでは表現できない集合をlossless保持 | `from_components(level, components, evidence) -> ARConfidenceSet; contains(beta: float) -> bool` | 30_61 §3 |
| `InferenceEvidence` | `ariadne.causal.inference.contracts` | NEW typed evidence | 既存Finite CIとAR集合の可用性を分離 | `validate_for(mode, method) -> InferenceValidation` | 30_61 §3 |
| `EffectOutcome` | `ariadne.causal.inference.contracts` | NEW typed result value | TreatmentEffectResult/ScientificResultDescriptorを型付き変換 | `validate_consistency(); to_result_payload() -> TypedEffectResult` | 30_61 §4 |
| `BackendCapabilityRecord` | `ariadne.scientific.capabilities` | NEW runtime value | Product ESTIMATOR_CAPABILITIESはMethodRegistryへの互換Facadeに移行 | `check(self, request: ValidatedCapabilityRequest) -> CapabilityDecision` | 30_62 §8 |
| `IdentificationPort` | `ariadne.scientific.ports.causal` | NEW typed Port facet | ScientificCorePort.run_identificationを保持して共通科学KernelにBridge | `identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome` | 30_61 §5 |
| `EstimatorPort` | `ariadne.scientific.ports.causal` | NEW typed Port facet | ScientificCorePort.run_estimationを保持して共通科学KernelにBridge | `estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome` | 30_61 §5 |
| `MethodCapabilityPort` | `ariadne.scientific.ports.capability` | NEW typed Port | ariadne.capabilities.causal.method_registryを唯一のMethod能力Authorityとする | `resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord` | 30_61 §5 |
| `DiagnosticPort` | `ariadne.scientific.ports.causal` | NEW typed Port facet | 既存Refutation/Sensitivity/DesignDiagnosticsを共通実装へ接続 | `run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome` | 30_61 §5 |

この表のModuleは**実装時の確定配置先**であり、既存コードにファイル・Classが存在すると主張しない。Methodの引数・戻り値の型記述はPythonの型注釈を含むインターフェース契約であってOwner Sign-offではない。詳細なField/Constructor/失敗処理は各Class仕様Ownerが定義する。

## 2. 実装構造と依存方向の決定

- `ariadne.product.domain`はProject/AnalysisSpecification/Execution/GraphVersion/Result/Artifact/Lineageとその永続化ライフサイクルを所有し続ける。CLIだけを理由にProductのEntityやVersionを擬似生成しない。
- `ariadne.causal`はGraph Evidence、Identification Proof、Estimator Request、Confidence Set、Inference/Effectの科学的なValueと不変条件を持つ。既存`causal.design.schemas.CausalDesign`と既存`product.domain.graph_semantics`の意味検証を利用し、二重Ruleを作らない。Productとの直接依存で循環を生じさせないよう、共有Validatorを抽出する場合は既存Exportの互換Facadeを保つ。
- `ariadne.scientific`はBackendの実行、typed Protocol、Runtime Probe・実効Capability Recordを所有する。既存`product.ports.scientific_core.ScientificCorePort`の旧v2署名を維持。旧`scientific.core_adapter.ScientificCoreAdapter`は必要なCompatibility Bridgeを通して新旧の計算を共通Kernelへ接続する。別の科学Engineを無根拠に複製しない。
- `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`がMethod ID、Estimand、Inferenceの唯一のMethod Policyを所有する。旧Product `ScientificValidationService.ESTIMATOR_CAPABILITIES`は移行時の互換Facadeとなる。StageType登録`StageRunnerRegistry`はMethod適格性のauthorityではない。
- `ariadne.interfaces.cli.local_causal`はLocal Study/YAML/JSON Parser、TrustedRootでのFile I/O、Publication/Reader/Privacy、CLI exit codeを所有する。既存`interfaces.cli`のv2互換挙動を変更しない。
- `ariadne.shared.content_ref`はFile内容参照の値を所有。`ariadne.shared.serialization.jcs`は新wire向けRFC8785 strict canonical bytesの予定配置。旧Product`canonical_bytes`および`hash_mapping(default=str)`との同一性は宣言しない。

## 3. 既存Classと新Classの境界の固定

1. **Graph:** `GraphEvidence`はGraphデータと意味Hashの不変Valueであり、`make_revision`やFIXは持たない。ProductでGraphを永続化・版管理する場合のみ既存`GraphVersionService`がVersion IDを発行する。CLI-only Graph生成はProduct GraphVersion生成を必須としない。
2. **Study:** `LocalStudySpec`はCLI execution envelopeであって新しいCausalDesign authorityではない。既存のCausal Design/EstimandのValidatorを再利用し、Operation/Method/Graph/Privacy eligibilityを各Ownerで検査する。
3. **Estimator Request:** `validate_against`は純粋な識別/Estimand適格性のみを判定し、BackendのDistribution/API availabilityは別途MethodCapabilityPortが検査する。
4. **Effect:** `EffectOutcome.to_result_payload`は純粋な型付き射影であり、JCS byte encode・File write・Product Result ID発行を行わない。Typed Effect Result → Wire Schemaのmappingがlosslessであることは独立Testで検証する。
5. **Port:** 入力型`Validated*`は単なる型注釈ではなくFactoryで不変条件を検証する。旧ScientificCorePortの5 Operationを削除せず、入口Adapterの違いが科学的な実装差分にならないようCompat Bridgeを用いる。
6. **Backend:** Effect Domainに`BackendCapabilityRecord`やoptional Backend importを置かない。`MethodCapabilityRegistry.resolve`は定義済みMethod/Inference判定、`load_adapter`のみoptional engine importを行う。

## 4. 旧監査D61-R01〜08との対応

| Finding | 設計対応 | 状態 |
|---|---|---|
| R01 独立Local Domain | `causal.local_contract`新設を取りやめ、既存層へ機能別配置 | **設計決定済** |
| R02 Study/CLI Envelope混在 | `LocalStudySpec`をCLIへ移し、CausalDesign既存Ownerを維持 | **設計決定済** |
| R03 GraphVersion重複 | `GraphEvidence.make_revision`廃止、Product GraphVersionServiceを唯一のWriter | **設計決定済** |
| R04 BackendCapability誤配置 | `scientific.capabilities`へ移管、MethodRegistryはCapability layer | **設計決定済** |
| R05 既存ScientificCorePort二重化 | v2互換Portを維持し、型付きPortと実行KernelをBridgeで再利用 | **設計決定済／Bridge実証待ち** |
| R06 Effect/Result lossless mapping | 型付き射影とversioned codecを分離 | **実装・Roundtrip実証待ち** |
| R07 JCS | Strict JCS Moduleを新設し旧Python normalizerを無検証流用しない | **実装・Test vector実証待ち** |
| R08 Diagnostic taxonomy | MethodDescriptor.operationに従うDiagnostic Portと既存Refutation/Sensitivity実装の対応 | **Operation別受入試験待ち** |

## 5. 決定範囲と残条件

この記録により13件の配置・メソッド署名・再利用方式を選定した。設計の型境界とModule構造は作業上の正規ベースラインとするが、既存コードとの完全なABI互換、Method Schema網羅、OS/FS・Codec・科学的実行は未実証。特にG01の06/07は**DRAFT/NOT_FROZEN**であり、Gate分割レビュー・Coding Authorization・試験PASS・正本昇格とは独立した状態を維持する。
