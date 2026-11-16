# 23_12_api_analysis_specification


---

## 5. Web API Interface

### 5.3 Analysis Specification API

#### 5.3.1 Common envelope

Analysis Specificationのschema versionは`analysis-specification/1`であり、Family固有payloadを共通envelopeに保持する。

Canonical envelope field:

```json
{
  "schema_version": "analysis-specification/1",
  "analysis_family": "PREDICTIVE",
  "research_context_version_id": "uuid",
  "dataset_version_id": "uuid",
  "analysis_view_id": "uuid-or-null",
  "analysis_mode": "CONFIRMATORY",
  "family_spec_schema_version": "predictive-analysis-spec/1",
  "family_spec": {},
  "revision_context": null,
  "warnings": []
}
```

`analysis_family`は`AnalysisFamily` enumをserializationした値である。

| Enum value | API value | 意味 |
| --- | --- | --- |
| `AnalysisFamily.EXPLORATORY` | `EXPLORATORY` | 探索的分析Capability |
| `AnalysisFamily.CAUSAL` | `CAUSAL` | 因果分析Capability |
| `AnalysisFamily.PREDICTIVE` | `PREDICTIVE` | 予測分析Capability |

Family-specific schema mapping:

| analysis_family | family_spec_schema_version |
| --- | --- |
| `EXPLORATORY` | `exploratory-analysis-spec/1` |
| `CAUSAL` | `causal-analysis-spec/2` |
| `PREDICTIVE` | `predictive-analysis-spec/1` |

このdiscriminatorはAnalysis Specification自身の分析semanticを表す。browser上で現在選択されているtabを表す`current_family`とは意味が異なる。

#### 5.3.2 Analysis Specification resource operations

Current public resource operations:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/analysis-specifications` | Family Specification DRAFT作成 |
| GET | `/projects/{project_id}/analysis-specifications` | Project内Specification一覧。現行実装ではFamily / Context / Dataset query filterは受けない |
| GET | `/projects/{project_id}/analysis-specifications/{spec_id}` | Specification取得 |
| PATCH | `/projects/{project_id}/analysis-specifications/{spec_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/validate` | 共通 + Family validation |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/fix` | FIXED化 |
| POST | `/projects/{project_id}/analysis-specifications/{spec_id}/revise` | child DRAFT作成 |

#### 5.3.3 Navigation Stageを保存しない

次のfieldはAnalysis Specification envelopeへ追加しない。

```json
{
  "current_family": "PREDICTIVE",
  "navigation_stage": "train",
  "current_stage": "train"
}
```

理由:

- `analysis_family`は分析Capabilityのsemantic discriminatorである。
- Current Family / Navigation StageはUI/application navigation stateである。
- 同じ`AnalysisSpecification`を`Train`、`Metrics`、`Explainability`等の複数Navigation Stageから参照し得る。
- Navigation Stageをspecへ保存すると、UI taxonomy変更がscientific/reproducibility contractへ波及する。

#### 5.3.4 Predictive specification contract

`predictive-analysis-spec/1`は次のtop-level fieldを持つ。

- `schema_version`
- `task_type`
- `prediction_question`
- `feature_spec`
- `split_spec`
- `preprocessing_spec`
- `model_spec`
- `tuning_spec`
- `evaluation_spec`
- `explanation_spec`

Task type:

- `BINARY_CLASSIFICATION`
- `REGRESSION`

Split strategy:

- `RANDOM`
- `STRATIFIED`
- `GROUP`
- `TIME_BASED`

Navigation Stage再配置を理由として、上記field、validation、default semanticsを削除・簡略化しない。
