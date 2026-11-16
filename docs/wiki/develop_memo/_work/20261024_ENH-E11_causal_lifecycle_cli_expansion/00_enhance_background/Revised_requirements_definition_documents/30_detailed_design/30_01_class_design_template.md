# 30_01_class_design_template

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

**Status:** `SOURCE_VERIFIED_BASELINE / ENH_E11_NO_CODE_CHANGE`  
**Source commit:** `3ba5fe2465ec591f0da7f998c21a5241984b73dc`. This document records existing behavior for six representative classes/ports. It does not approve E11 use of these exact classes or cover all current product classes.

## 1. Scope and source mapping

| Symbol | Source | Source blob | Relation |
|---|---|---|---|
| `PlanValidator` | [src/ariadne/product/workflow/plan_validator.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/workflow/plan_validator.py) | `53aab649a0ed3f0dbec78e5fa98271ff78f5dc12` | workflow plan checks |
| `StageRunnerRegistry` | [src/ariadne/product/workflow/runner_registry.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/workflow/runner_registry.py) | `7ffa673d92818e597c4349737860df0ff75b4f97` | runner resolution |
| `GenericExecutor` / `ExecutionOutcome` | [src/ariadne/product/workflow/executor.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/workflow/executor.py) | `81d91e7de0fc0eb5a582711968b698fa4ac44761` | generic runtime |
| `GraphVersion` | [src/ariadne/product/domain/graph_version.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/domain/graph_version.py) | `37ff76e001c8e269a00127e18d375f1dbc34c0e3` | Product graph authority |
| `ArtifactStorePort` / `StoredArtifact` | [src/ariadne/product/ports/artifact_store.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/ports/artifact_store.py) | `e5bb990f9b69ef68df46a1559560ffb67b64caaf` | Product artifact Port |
| `CliManifest` | [src/ariadne/interfaces/cli/manifest.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/interfaces/cli/manifest.py) | `97216eca9d777e97f7a5ebd4e248afd31c6b4de0` | existing local manifest |

## 8. Verification boundary

These entries are source-inspected structural contracts, **not** proof of existing tests, successful E11 migration, scientific benchmark or independent Architecture Review. Each class needs source-linked test references and behavior-level evidence before reusing it as a normalized E11 component.
## Common class and function physical design template (owner-approved)

**採番:** `{N}` は文書内の見出し番号であり固定値5ではない。

```markdown
### {N}. `ClassName`

#### {N}.1. 識別情報・責務
- Class / Protocol名、配置先module
- 実装状態（Existing / Proposed）、Source SHA / ADR
- 目的・責務・責務外、依存Class / Port

#### {N}.2. フィールド
| Field | Type | Default・生成元 | 可変性 | 制約 |
|---|---|---|---|---|

#### {N}.3. Constructor / Factory
- Signature、入力条件、初期化処理
- 生成後の不変条件、例外

#### {N}.4. メソッド
| Method Signature | Return | 処理 | 副作用 | 例外 |
|---|---|---|---|---|

#### {N}.5. 処理仕様
- Preconditions、処理手順・分岐、Postconditions
- 状態遷移、数値的制約（該当時）

#### {N}.6. I/O・連携・失敗処理
- 呼出し元 / 呼出し先、Data / Schema / Version
- 永続化・Transaction、Error / Retry / Rollback

#### {N}.7. 検証
- Unit Test、Contract Test、Negative Test
- 関連FR/NFR/AR、Acceptance/Gate
```

**運用:** 不適用項目は理由付きN/Aを記載。Dataclassの業務メソッドが無ければ「業務メソッドなし」と記録。Module-level関数もsignature・入出力・副作用・失敗・検証を記載。既存実装と新規E11候補を区別する。数値Estimatorは上位Scientific Contractを参照して処理手順・精度・推論適格性を定める。
