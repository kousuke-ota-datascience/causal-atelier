# 22_15_schema_dependency


---

## 18. Schema / Dependency Boundary

- `analysis-specification/1`の既存`analysis_family`を再利用する。
- Navigation Stage fieldをAnalysisSpecificationへ追加しない。
- ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。
- Product Domainはbrowser route/navigation implementationへ依存しない。
- Scientific / ML / visualization libraryはPort / Adapter背後へ隔離する。
- Capability固有Adapterはcanonical runtime lifecycleを制御しない。
- Navigation metadata/stateについてはDB migrationを行わない。
- Reproducibility contractとして`StageAttempt.effective_random_seed: int | null`を追加するDB migrationを行う。
- `Execution.runtime_version_json`へ`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保存する。



### 18.1. Version Dispatch・Legacy互換・Schema依存

- `causal-analysis-spec/2`と旧CLI parser/Result/overrideの意味を保護する。新Local E11のversioned schemaは別dispatchし、old v2を暗黙移行させない。
- Product Web API、Frontend、Worker、DB migrationには新E11のroute/field/role/Stageを追加しない。既存Productの認証上の不完全性をE11の設計で解消済みと宣言しない。
- Local Scientific Core共有部分の改変が既存E9/E10機能・Predictive Model Loader/SHAP/LIMEに影響しないことを回帰試験で確認する。
- Product GAP-C01〜04は明示的に別Workstreamへ残す。担当・期限未確定のものをE11 CLIのテストPASSでClosedにしない。

新たなLocal Specと`causal-analysis-spec/2`の間では明示的なSchema Version識別を要求する。Unknown Versionを旧Readerに渡して暗黙で解釈しない。

**当該機能に適用する設計制約（関連Requirement）**

- **`FR-161`**：LightGBM / SHAP / LIME等のexternal analytical engineはoptional capabilityとして導入し、未導入でもcore startupと既存supported flowを壊さず、unavailable capabilityから別model/methodへsilent fallbackしない
- **`FR-114a`**：Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する
- **`FR-120a`**：runtime API schemaから生成されるFastAPI OpenAPIをcurrent API contractとして提供する
- **`NFR-014`**：`causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ
- **`NFR-028`**：optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する
