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

**当該構成要素の詳細設計制約（関連Requirement）**

- **`FR-120b`（将来拡張・現行提供対象外）**：canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する
- **`NFR-005`**：新Analysis Familyを既存Executor変更なしにRegistry追加できる
- **`NFR-010b`（将来拡張・現行提供対象外）**：Worker restart後の明示的resume/recovery semanticsを定義する
