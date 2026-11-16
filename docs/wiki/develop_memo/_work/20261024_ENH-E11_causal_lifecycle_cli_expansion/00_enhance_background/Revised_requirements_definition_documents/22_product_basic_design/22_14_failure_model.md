# 22_14_failure_model


---

## 17. Failure Model

| Failure | 扱い |
| --- | --- |
| Navigation descriptor invalid | startup/query validation error。runtime execution failureへ変換しない |
| Unknown Family / Stage route | explicit 4xx / unsupported state。silent fallbackしない |
| Renderer binding missing | presentation/configuration defectとして検出 |
| Validation rejection | Executionを作成せず4xxまたはREJECTED Command Result |
| Technical runtime stage failure | Stage FAILED、Execution FAILED、既存retry policy |
| Analytical prerequisite unmet | Result/operation availabilityとして表現。Navigation Stage存在自体とは分離 |
| Artifact read integrity failure | `ArtifactHashMismatch`として扱い、破損contentを正常として返さない |
| Client disconnect | server-side Execution継続。cancelは明示Command |



### 17.1. Local Scientific Operationにおける失敗の分類

| Condition | Architecture response |
|---|---|
| Invalid schema/version/path/hash | 入力・セキュリティのpreflight拒否。科学的非識別と混同しない |
| Graph/Estimand nonidentification / ineligible | 原因・根拠を持つtyped scientific negative。Estimator不呼出し |
| Optional Backend unavailable | 選択MethodをUnavailableにし、他Estimatorへのsilent fallback禁止 |
| Inference unavailable / unsupported | point-onlyの許容をanalysis modeで判定し、無根拠CIは生成しない |
| Adapter execution or artifact readback failure | technical failure、完全公開禁止、staging・manifest commitを安全に回復 |
| Source/Artifact hash collision or mismatch | provenance/consistency error、正本の上書きや黙示再利用を拒否 |

**注意:** 旧Productのretry/idempotency/cross-store compensation方針とLocal Filesystem publicationの実装は分けて定義する。[科学的Gate](22_06_family_causal.md)／[Artifact publish](22_09_results_artifacts_lineage.md)。

技術失敗と科学的非識別は別のResult軸に保持し、継続可能なscientific negativeを汎用exceptionとして破棄しない。

**当該機能に適用する設計制約（関連Requirement）**

- **`FR-128b`（将来拡張・現行提供対象外）**：size limit、timeout等のoperational resource configurationを一元管理する
- **`NFR-007`（将来拡張・現行提供対象外）**：Metadata transactionとArtifact writeのcross-store failure compensationを定義する
