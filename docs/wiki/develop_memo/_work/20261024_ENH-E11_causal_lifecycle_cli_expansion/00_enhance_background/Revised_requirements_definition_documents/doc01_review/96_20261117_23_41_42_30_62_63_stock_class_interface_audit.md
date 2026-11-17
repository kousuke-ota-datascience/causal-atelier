# 23_41/23_42/30_62/30_63 — ストック適合性・責務境界・既存Class差分監査（2026-11-17）

**区分:** FLOW / Design Audit（正本候補となるClass・Interface設計には昇格しない）  
**対象:** `23_41_cli_scientific_ports.md`, `23_42_local_result_manifest_artifact.md`, `30_62_local_execution_publication.md`, `30_63_causal_method_adapters.md`  
**対象Branch:** `prototype/ariadne_mvp`。Source基準は監査時の同Branch。  
**状態:** `STOCK_STRUCTURE_AND_CLASS_REUSE_REMEDIATED / STATIC_VERIFIED / SCIENCE_AND_RUNTIME_PENDING / CODING_NOT_AUTHORIZED`

## 1. 文書別の責務と修正

| Stock文書 | 永続的な責務 | 既存との重複排除／再利用 | 修正結果 |
|---|---|---|---|
| `30_62_local_execution_publication` | Application UseCase/Capability Registry、run単位Publication、Manifest/Reader/Privacy、Backend Capability | `product.workflow.GenericExecutor`、`StageRunnerRegistry`はProduct Stage lifecycleを保持。ArtifactStorePortはObject保存、Local Publisherはtransactional multi-file run公開を保持し同一視しない。Method能力は単一Registryへ寄せる | 7 Classを個別7区分に編成。冒頭にEnhancement境界や独立Domain前提を置かない |
| `30_63_causal_method_adapters` | 41 MethodのScientific Adapter、Method固有preflight、Backend、Inference、Scientific Negativeと検証義務 | 既存`scientific.discovery/identification/inference/refutation/sensitivity`および`causal.discovery/inference`を利用。旧`ScientificCorePort`のv2公開ABIは維持 | 22 Adapter Classの7区分を追加しMethod ID 41を保持。2 Class EXISTING、20候補PROPOSED |
| `23_41_cli_scientific_ports` | CLI wire/Version/exitと入口非依存のScientific Port契約 | `LocalStudySpec`はCLI、`ValidatedStudy`はCausal、ScientificCorePort v2互換Bridge、MethodRegistry単一authority | 入口とScienceの責務分離・型Owner表を明示し、Transient E11固有の目的説明を除く |
| `23_42_local_result_manifest_artifact` | Run file bundleのResult/Graph/Manifest/Marker/Privacy/Readback wire | Product `Result/Artifact`とFile bundleのauthorityを分離。JCS Codecは共通typed encoder、Local Publisher/Readerと責務を分担 | 現在有効なFile Interface契約として整理し、Version/Hash/Privacyの不変条件を維持 |

## 2. Class配置・署名・再利用の対照

### 30_62 の7 Class

| Class | 配置 | 主な公開契約 | Existingとの差分 |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution` | `preflight(spec: ValidatedStudy)`; `run(spec: ValidatedStudy)` | Product Stage Runner/Executionの代替ではない。学術実行部分を再複製しない |
| `MethodCapabilityRegistry` | `ariadne.capabilities.causal.method_registry` | `describe`, `resolve`, `load_adapter` | `ScientificValidationService.ESTIMATOR_CAPABILITIES`を二重Rule表にせず既存Facade互換 |
| `LocalArtifactPublisher` | `ariadne.interfaces.cli.local_causal.publication` | `begin`, `stage_bytes`, `validate`, `commit`, `abort` | Existing Product `ArtifactStorePort.store`は原子的multi-file Publicationと同義でない |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest` | `from_payload`, `to_canonical_bytes`, `validate_invariants` | 旧`CliManifest(2.0)`とVersionを混同しない |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader` | `read_run(trusted_root,run_id)` | Marker→Manifest→All Artifacts readbackとprivate policyを新契約で追加 |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy` | `assert_export_allowed(spec: ValidatedStudy,...)` | Product Membership/RBACではなく独立PolicyとTrustedRoot認可 |
| `BackendCapabilityRecord` | `ariadne.scientific.capabilities` | `check(request: ValidatedCapabilityRequest)` | 実効Distribution/API/Inference可用性を証拠化。optional importはValue責務外 |

### 30_63 の22 Adapter Class

`NativeIdentificationAdapter`, `DoWhyIdentificationAdapter`, `FciDiscoveryAdapter`, `FrontdoorLinearAdapter`, `NativeEffectAdapter`, `WeightingEffectAdapter`, `RefutationAdapter`, `SensitivityAdapter`, `ObservedNceAdapter`, `ObservedNcoAdapter`, `OlsRvAdapter`, `EconmlCateAdapter`, `MetaLearnerAdapter`, `EconmlDrivAdapter`, `TigramiteTemporalAdapter`, `PanelQuasiAdapter`, `InterruptedTsAdapter`, `RddAdapter`, `WaldRatioAdapter`, `TwoSlsAdapter`, `SyntheticControlAdapter`, `SyntheticDidAdapter`。

既存の`ariadne.scientific.refutation.adapter.RefutationAdapter`と`ariadne.scientific.sensitivity.adapter.SensitivityAdapter`の`run(input_,output_dir)`契約は変更しない。Refutationは**Placebo TreatmentとData Subsetが現行実装済み**、Random Common CauseとBootstrapは追加実装が必要。残り20 Classは候補であり、既存アルゴリズムの数理的同義部分を共有することが設計条件。

FciDiscoveryAdapterの`preflight(ValidatedDiscoveryRequest)`／`execute(ValidatedDiscoveryRequest, *, sink: StagingArtifactSink)`はMethod固有の型付き契約。全Adapterの共通Contractは`preflight(ValidatedMethodRequest)`／`execute(ValidatedMethodRequest, *, sink)`で、既存Adapterの公開ABIを直接書き換えるものではない。Method ID表／科学的条件／受入IDの正本は30_63 §2〜§8と要件10_32。

## 3. Wire Versionと変更範囲

`e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1`, `e11-commit/1`, `e11-json-jcs-rfc8785/1`は既存Version識別子として維持。これは文書Filenameに残すEnhancement番号ではなく、Schema互換性の識別子である。実際のCode/Schema Migrationを許可なく行っていない。

## 4. 追跡・検証範囲

- 改名：4文書、参照修正は関連Stock/Flow/G01計画とテスト指示に適用。旧FilenameはGit treeから削除。
- 構造：30_62は7 Class×7区分＝49、30_63は22 Class×7区分＝154。41 Method ID・41 Method検証IDの列挙を保持。
- 23_41/42の`IF-E11-`/`IO-E11-`受入義務および7種のVersion識別子は維持。
- 既存コードの再利用は設計判断であり、Runtime ABI/Algorithm同値性・Science reference・Monte Carlo coverage・OS/fsync/no-clobber/Privacy securityの実証は未実施。
- 読者が暫定Phase/Work PackageをDomainの意味と取り違えないよう、Class OwnerとInterface Ownerを分離。

## 5. 後続の未閉鎖事項

1. 既存`ScientificCorePort`のv2 Adapterと新typed Portを共通Kernelに接続するBridgeの具体Data mappingとException整合、Regression実証。
2. Method Registry単一authorityへ既存Estimand Validatorを移す際の依存循環と旧Product Exportの互換検証。
3. 新Method20/既存Refutation2追加分のImplementationとDGP/Reference/Inference/CI/AR/Graph scientific validation。
4. 23_42のstrict Schema/Hash/Privacy/Marker/readbackと各OperationのBundle全件対応、実効FS fault-injection。
5. G01の06/07 Gate単位のFreezeとCoding Authorizationは別工程で、**未発行**。原正本`docs/wiki/requirement_definition/`への昇格は全GateテストPASSまで禁止。

**監査判定：** Stock文書の責務分離・Class構造・設計方針は更新済み。独立した実行・科学・法務受入までPASSを主張しない。
