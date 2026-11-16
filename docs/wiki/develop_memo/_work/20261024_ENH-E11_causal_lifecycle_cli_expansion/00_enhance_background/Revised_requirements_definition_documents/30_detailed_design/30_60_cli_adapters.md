# 30_60_cli_adapters

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 7. `CliManifest` (existing v2 local CLI)

**Responsibility:** Legacy manifest serialization; source marks snapshot_schema_version default `causal-analysis-spec/2`.

| Field group | Actual Python fields | Notes |
|---|---|---|
| Identity | `manifest_version: str`, `operation: str`, `algorithm_or_estimator: str` | Required |
| Inputs | `dataset: dict[str,Any]`, `graph: dict[str,Any]|None`, `parameters: dict[str,Any]`, `analysis_spec: dict[str,Any]` | Existing shape |
| Environment | `random_seed: int|None`, `code_version: str`, `runtime_versions: dict[str,str]`, `backend_version: str|None` | Existing provenance |
| Result | `scientific_status: str`, `result_summary: dict[str,Any]`, `artifacts: list[dict[str,Any]]=[]`, `warnings: list[Any]=[]`, `scientific_warnings: list[dict[str,Any]]=[]` | Mutable list within frozen dataclass: do not equate with deep immutability |
| Compat | `snapshot_schema_version: str="causal-analysis-spec/2"`, `analysis_mode: str|None`, `causal_question_hash: str|None`, `graph_origin: str|None`, `upstream_result_reference: str|None`, `identification_status: str|None`, `eligibility_status: str|None` | Legacy contract |

| Method | Return | Behavior |
|---|---|---|
| `to_dict(self)` | `dict[str,Any]` | `dataclasses.asdict(self)` |

**Negative:** E11 typed AR or revised GraphResult must not be shoehorned into v2 manifest without an explicitly versioned reader/writer and regression tests.


## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-120b（SPLIT）

- 移管する原条項の具体内容：canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する
- 上位Requirementと整合する要求核：API仕様と公開する入出力例との整合性を検証できる
- `FR-120b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. NFR-005（SPLIT）

- 移管する原条項の具体内容：新Analysis Familyを既存Executor変更なしにRegistry追加できる
- 上位Requirementと整合する要求核：新しい分析領域を既存分析の挙動を壊さず追加できる
- `NFR-005`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.3. NFR-010b（SPLIT）

- 移管する原条項の具体内容：Worker restart後の明示的resume/recovery semanticsを定義する
- 上位Requirementと整合する要求核：実行基盤の再起動後に処理状態を復元・回復できる
- `NFR-010b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)
