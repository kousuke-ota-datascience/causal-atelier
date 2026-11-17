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


### 18.2. PREP-02 Schema／Port Freezeへ引き渡す決定事項

この節は**Freeze済みSchemaの宣言ではない**。既存SourceとIF/DD候補の差から、実装前に必要なAuthority・Version決定を列挙する。

| Contract | Current Source観測 | Proposed E11 Authority | Freezeに必要な証拠 |
| --- | --- | --- | --- |
| Study Config/Version | 旧CLIのconfig parserと`causal-analysis-spec/2` | `e11-local-study/1`専用decoder、unknown/versionless fail-closed | version discriminator / strict JSON Schema / duplicate YAML key / legacy fixtures |
| Graph/Lineage | Product `GraphVersion`はProject DB authority | `e11-local-graph/1`、PAG circle/temporal lag付き独立Local graph | Endpoint/GraphKind/lagのunion、参照SHA、編集時のversion発行 |
| Scientific Port | Product ScientificCorePortはProduct ScientificStatusへ結合 | E11 Local Domain Portとversioned typed DTO | Class/Port signatures、Adapter boundary、Method-specific negative/AR result |
| Effect/AR/Inferences | 旧ResultはEffectと科学Statusの2軸契約を持つがE11 ARのset形状はない | `e11-local-effect-result/1`と`e11-local-status/1` | bounded/unbounded/disconnected/ALL_REAL、null reason、JSON finite、roundtrip |
| Publication/Readback | ArtifactStorePortはsingle-Artifact surface | `e11-local-manifest/1`、commit marker、LocalPublicationPort/ManifestReader | no-clobber/collision、同一FS、Manifest→Artifact hash、Privacy/Crash tests |
| Backend/Env | 現行`pyproject.toml`のE11 extrasは未宣言 | DEC08 5 profile＋conditional ENV-RD | locked distribution/API/ABI、fresh isolated import、SBOM、配布Legal separate |

**依存順序:** (1) Scope/Estimand/Graph意味契約 → (2) Schema version・enum/codec → (3) Port signature・failure → (4) File publish/readback → (5) Backend Profileの実効検証 → (6) 独立Architecture Review。必要なContractをfreezeする前に、設計済みの文章を実装成功の証拠として扱わない。BD01-F03〜09/F12は対応する独立証拠が揃うまでOPEN。



### 18.3. F04/F07 の具体化とFreeze境界（2026-11-17）

現行Product `ScientificCorePort` / `ScientificResultDescriptor` / `ArtifactStorePort`とE11 Local Port/DTOを同一interfaceへ合流させない。E11は独立したTyped Identification、Effect、Inference、AR Confidence Set、Technical/Scientific statesと、staging→atomic no-replace publicationを要求する。旧Product v2の実効挙動を変更せず、必要な純計算だけを互換性と科学的意味が証明されたexplicit Adapterで再利用する。

F07の区間表現はextended-real tagged endpoints・nonempty canonical component union・lossless topology、CI不在のtyped reason、ScienceAcceptanceの独立を守る。詳細は`30_61` `11/12、`23_41` `9、`23_42` `12。Draft Schema/ABIは独立Architecture Reviewまで未Freeze。F03/F05/F06/環境/Method Scienceの未証明も残る。
