# 10_11_fr_exploratory

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-023 | Explore | Dataset overview、schema、型、欠損率、cardinalityを表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-024 | Explore | 数値列・カテゴリ列の記述統計と分布を生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-025a | Explore | 列別missingnessを確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-025b | Explore | 複数列のjoint missing-pattern analysisを行える | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-026a | Explore | current capabilityとして型に応じた二変量association / bivariate analysisを生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-026b | Explore | 散布図、箱ひげ、クロス集計等のfull exploratory bivariate visualization surfaceを提供する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-027 | Explore | group-by集計および時系列推移を生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-028 | Explore | correlation / association matrixを型に応じて生成できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-029 | Explore | Chart Specificationを保存し、同じDataset Versionで再実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-030 | Explore | 探索実行のResultとArtifactを保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-031 | Explore | 保存した探索Resultに観察メモと限界をAnnotationできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-032 | Explore | Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない | SHOULD | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-033 | Explore | 探索結果をEXPLORATORYと表示し、確認的結論として自動昇格しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-034 | Explore | Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-146 | Exploratory | Exploratoryは`profile / data-quality / distribution / relationships / comparison / findings`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-147 | Exploratory | Visualizationは各分析Stageの表現手段とし、独立Navigation Stageを設けない | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-148 | Exploratory | Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-175 | Exploratory Surface | Data Qualityはdedicated backend operationを新設せずread-only availabilityとして扱い、Comparisonの`TIME_TREND`は既存grouping/aggregation semanticsを維持し、Findingsの`CHART`は既存persistent operation/result/artifact semanticsを維持する | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
