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


### 18.4. F03/F05/F06とF04/F07レビューのFreeze準備（2026-11-17）

承認済みA/A/Aの選択を実装拘束として反映：F03はLinux同mount/FS `RENAME_NOREPLACE`（ロックのみの代替を禁止）、F05はOwner EUID/private TrustedLocalRoot/事前Policy＋CLI flagを独立検証、F06は`e11-local-*/1`の5識別子を正確なdiscriminatorでdispatchし旧v2を改変しない。F04は既存Product Port/Statusの無検証cast禁止、F07は有界/無界/非連結集合とInference/Scienceの独立を保持。

レビューにより、汎用ARの`EMPTY`、Legacy Study YAML例の`path`と`ContentRef.relative_key`差、Publisherの`Path`引数とTrusted Rootの不一致、Process lock fallback矛盾を発見。修復した設計と未決定事項は[レビュー](../combined_review/103_20261117_prep02_f04_f07_design_review_findings.md)、[F03](../combined_review/104_20261117_prep02_f03_atomic_publish_contract.md)、[F05](../combined_review/105_20261117_prep02_f05_trusted_root_privacy_contract.md)、[F06](../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md)を参照。実効FS・Privacy・Science試験は未実施。F04/F07レビューは**Author Self Review**であり、F12独立Architecture Reviewを満たさない。


### 18.5. DEC-PREP02-D Owner採用結果

4件A案（F07 generic EMPTY、F05 independently approved Policy、F06 strict versioned canonical JSON、F06 privacy denial exit3）を[DEC-PREP02-D](../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md)として採用。これにより『Owner未決定』という分類は終了。ただしF05の信頼Anchor/F06のRFC8785適合・有限精度/F07のB0/B1 Scienceは実装・独立review対象であり、Port/Schema Freezeは未完了。


### 18.6. E11 Cross Port・Scientific/Schema不変条件

Typed Local Port/DTOの境界は[共通契約](../combined_review/112_20261117_prep02_f03_f07_shared_port_signature_contract.md)に統合。Graphのsemantic hashと外部File hashは別計算として扱い、ManifestはOperation別のEffect存在性を厳格判定する。B0/B1のARは一律EMPTY拒否ではなくjust-ID**非退化条件**を伴うMethod固有validatorを設計する。個票の事前Policyの独立Trust AnchorとOSの実効Principalを別検証する。詳細：[F06 semantic join](../combined_review/114_20261117_prep02_f06_schema_semantic_invariants.md)、[F07統計量](../combined_review/111_20261117_prep02_b0_b1_ar_science_method_contract.md)、[F05信頼Anchor](../combined_review/113_20261117_prep02_f05_policy_trust_anchor_candidate.md)。これらはmechanical/scientific review inputsであり、Port/Schema Freezeを宣言しない。


### G01 P01 contract ownership and E11 codec isolation

P01 is the pure typed Study/ContentRef/JCS/Manifest value boundary. The strict e11-local-study/1 and e11-local-manifest/1 wire decoders reject unknown keys, wrong version, legacy v2 interpretation, incompatible Operation/Method/Estimand/privacy, bad cross-ref and invalid scientific-negative reason combinations. P02 owns FD-rooted input/Artifact bytes, atomic staging/publish and independent Reader; P03 Graph scientific-structure serialization; P04 actual FCI execution and science proof; P05 caller orchestration and effective runtime facts. `from_payload` cannot recompute a request hash from absent external Study or recheck Status code bytes; the full evidence factory/P05/Reader must perform cross-file joins. Existing public JSON versions and Product ABI are unchanged.


### G01 internal Graph-negative diagnostics schema boundary

The G01 P1-M06 DISCOVER `diagnostics.json` uses the strict **internal** profile `schema_drafts/internal_scientific/e11_g01_discover_negative_diagnostics_draft1.schema.json`. It is NOT the separate `e11_method_diagnostics_draft1.schema.json` for P1-M12–20 REFUTE/SENSITIVITY/DIAGNOSE, and its internal profile identifier is not a public Study/Status/Manifest `schema_version` or new `schema_dispatch` field. No changes to the five public E11 payload versions or Product v2. P02 and Reader perform semantic run/reason joins rather than relying on hash/size alone.
