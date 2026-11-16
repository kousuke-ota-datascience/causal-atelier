# BD-01 — Architecture整合性レビュー／未解決事項台帳

**Date:** 2026-11-16  
**Review class:** `INTERNAL_DOCUMENT_AND_CODE_BASELINE_CONSISTENCY_REVIEW`（**独立第三者Architecture審査ではない**）。  
**Status:** `BD01_BASIC_DESIGN_REVISED / ARCHITECTURE_CONSISTENCY_PARTIAL / 2_DOC_FINDINGS_RESOLVED / 11_OPEN / INDEPENDENT_GATE_PENDING`。

## 1. 総合判定

**暫定結論：Owner承認済みDEC09のArchitecture原則に沿う基本設計への再編は完了。ただし具体的Port・Version/Schema・Atomic/Privacy・Backend/CI・Science/Legalの独立確認が未了のため、独立Architecture ReviewのPASS・Gate06 Ready・Coding許可とは判断しない。**

- 既存ProductとE11 Localを2実行系として分け、E11新MethodをProduct Web/API/DB/Workerに統合しない。
- Estimand／Graph／Identification／Eligibility／Method／typed scientific ResultとLocal Manifestのauthorityを責務別に定義した。
- 既存`product.ports.scientific_core`などの再利用可能性は保持。実装の重複か破壊的改修かを先に決め打ちしない。
- 既存E9/E10、旧v2、Product GAP-C01〜04の回帰・Scopeを明示した。
- **文書論理と実コードの同一性は確認していない。** コード由来の観察は未実装Gap特定用であり、E11の仕様の実装済み判定には使わない。

## 2. ソースの検証境界

| Source | Evidence observed | Limits |
|---|---|---|
| [DEC09 Owner decisions](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md) | ARC09-01〜07 Owner adopted; Gate06/07 unexecuted | Detailed ADR/Port/Schema not frozen |
| [DEC08 environment record](../../../working_notes/20261116_sr04_dec08_backend_optional_dependency_lock_license_owner_decision_proposal.md) | 5 profiles, single lock, legal gate adopted | E11 lock/profile/legal not verified |
| [RD03 formal requirements](../96_rd03_formal_requirement_traceability.md) | FR/NFR/AR new 44, Method 41/Scope 68/UC10 trace | Method execution and scientific success not evidenced |
| [RD04 requirement review](../97_rd04_e11_requirement_review.md) | 44 clauses preserved, semantic gaps identified | Owner final SHA review pending |
| [Current CLI scientific_stage.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/535499b080ed129262bf2f6efd0a1033dc21ec47/src/ariadne/interfaces/cli/scientific_stage.py) | Existing CLI imports Product domain and port; calls core before manifest write | Not an exhaustive path/atomicity/security implementation audit |
| [Current Scientific Port](https://github.com/kousuke-ota-datascience/causal-atelier/blob/535499b080ed129262bf2f6efd0a1033dc21ec47/src/ariadne/product/ports/scientific_core.py) | ScientificResultDescriptor uses Product ScientificStatus; local result bridge needed | New E11 result schema not implemented |
| [Current CLI Manifest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/535499b080ed129262bf2f6efd0a1033dc21ec47/src/ariadne/interfaces/cli/manifest.py) | Legacy snapshot_schema_version/manifest_version design observable | E11 schema/version dispatch not frozen |
| [Existing ArtifactStorePort](https://github.com/kousuke-ota-datascience/causal-atelier/blob/535499b080ed129262bf2f6efd0a1033dc21ec47/src/ariadne/product/ports/artifact_store.py) | Product Port has store/retrieve/exists/delete | Multi-file local atomic publish cannot be assumed from Port surface |

## 3. Finding register

| Finding | Status | Severity | Question | Evidence / risk | BD-01 remediation | Acceptance / owner action |
|---|---|---|---|---|---|---|
| BD01-F01 | Resolved in BD | High | Existing Product/Local CLI System Context混在 | 22_00 §3の旧図はWeb Frontend/CLI→Web APIと読める。DEC09 CLI-onlyに不整合 | 22_00 §3を二系統に再描画、22_20でauthority固定 | Static diagram/source trace; no code test |
| BD01-F02 | Resolved in BD | High | Product DB正本とLocal Run Manifestの同一視 | Product ResourceとLocal Manifestのcanonical authorityが異なる | 22_20/22_22に別々のowner、無断cross-lane migration禁止を明記 | IF/DD schema / runtime proof still pending |
| BD01-F03 | OPEN | Blocking | Multi-file artifact atomicityとReadback | 現行scientific_stage.pyではScientificCoreAdapterへoutput_dirを渡して結果を生成後、manifest.json.write_text。staging/complete markerの整合手順は当該CLIコード上未確認 | 22_22 publication gateとcrash/partial failureの契約を新設 | IF-01/ DD-01: commit marker、rename/crash recovery、traversal/symlink、negative tests |
| BD01-F04 | OPEN | Blocking | Legacy Port/domain reuseとE11新typed outcome | 現行CLIはproduct.domain.analysis_spec/enums/ports.scientific_coreをimport。ScientificResultDescriptorはProduct ScientificStatusを使用。E11にはpoint/uncertainty/scienceの別軸・AR集合が必要 | 旧v2のPort/Resultは保護し、E11 variant/bridgeまたは明示新Portで分岐。重複設計の回避 | IF-01/ DD-01 actual Port/typed Domain/persisted schema and regression |
| BD01-F05 | OPEN | Blocking | Local individual exportの認可モデル不足 | Product OWNER/EDITOR/VIEWERのRBACはProductのProject境界。Local CLIにはProject DB/Membership必須依存を許せない | 22_23にlocal OS主体・explicit opt-in・artifact access policyを割当 | Owner+Security: identity/delegation, filesystem permissions, audit; negative export tests |
| BD01-F06 | OPEN | Blocking | Local spec versionと旧v2の意味的共存 | 現行CliManifestはmanifest_version 2.0/snapshot_schema_version causal-analysis-spec/2。新E11のwire schema/version/CLI dispatchは未Freeze | 22_20/22_23でseparate explicit dispatchと旧read互換を規定 | IF-01: schema/enum/CLI grammar/legacy reader/version migration tests |
| BD01-F07 | OPEN | Blocking | Confidence setおよび科学的状態の型付き契約 | AR信頼集合はbounded/unbounded/disconnected/ALL_REAL、point/uncertainty/scienceは別軸。現行Product valueで十分な表現保証は未検証 | 22_21/22_22に数学的状態とlossless serializationを分離 | IF-01: typed JSON/Parquet, null reasons, interval infinities; DD-01 math and test |
| BD01-F08 | OPEN | Blocking | Method別Estimator・InferenceのBackend適格性 | FD-A/B0/B1/DRIV/CATE7/RDD/SCM等は異なるestimand/CI、SR04-FにもBLOCKED/NOT_GENERATEDあり | 22_21でMethod family別のeligibilityとNegative結果を分離 | IF-01 method config/port; DD-01 adapters; Gate07 oracle/coverage |
| BD01-F09 | OPEN | Blocking | 5 Profile/uv.lock/ENV-RDの実効確認 | DEC08は5 Profiles採用、ENV-RDは条件付き。E11 extrasが現行lockへ導入済みとは未確認。SR02個別env PASSはE11 universal lock PASSでない | 22_23にfresh venv/lock/API version/SBOM受入契約 | Environment preflight all profiles + combined + old v2 regression |
| BD01-F10 | OPEN | Delivery blocker | GPL/配布単位の法務承認 | DEC08はTigramite/rdrobustの顧客SI配布を個別法務審査の対象としている | Internal Science/Customer Deliveryを別stateにし未承認顧客配布禁止 | Legal owner approval for actual distributed artifact/receiver |
| BD01-F11 | OPEN | Management | Product GAP-C01〜04の担当・期限 | DEC09でE11 CLI実装とProduct gapsの解消は分離採用。担当/期限は残課題 | 22_20 scope negative boundary、22_23 future Product lane | Separate owner/workstream, no E11 PASS/auto closure |
| BD01-F12 | OPEN | Gate blocker | Independent Architecture Review/Code/Frozen Schema | Owner ARC09原則の承認は独立Architecture ReviewやPort/Schema freezeを意味しない | 22_90 Self-review only; 22_91 allocation 44/44、ARC09 7/7 | Independent reviewer sign-off, Gate06 readiness, negative tests |
| BD01-F13 | OPEN | Gate blocker | Canonical昇格条件の保護 | RD-04文書整合性PASSはテスト全件PASSでなくcanonical promotion不可 | 93 Owner policyを参照。現行変更はworking copy限定 | Full applicable ENH-E11 tests PASS → promotion separately |

## 4. Approved architectural invariants vs specific pending contracts

| Owner authority | Owner policy state | BD target | Architecture gate status |
|---|---|---|---|
| ARC09-01 Domain authority | APPROVED | [22_20](22_20_e11_local_system_architecture.md), [22_21](22_21_e11_scientific_pipeline.md) | Typed Domain/legacy bridge detail pending |
| ARC09-02 Backend isolation | APPROVED | [22_20](22_20_e11_local_system_architecture.md), [22_23](22_23_e11_environment_security_compatibility.md) | Effective version/API/Port contract pending |
| ARC09-03 Identification first | APPROVED | [22_21](22_21_e11_scientific_pipeline.md) | Method eligibility + negative tests pending |
| ARC09-04 Local contract | APPROVED | [22_20](22_20_e11_local_system_architecture.md), [22_22](22_22_e11_local_result_artifact_lineage.md) | Exact version/atomic/path + privacy pending |
| ARC09-05 Typed inference | APPROVED | [22_21](22_21_e11_scientific_pipeline.md), [22_22](22_22_e11_local_result_artifact_lineage.md) | ConfidenceSet JSON and coverage pending |
| ARC09-06 Provenance/Profiles | APPROVED | [22_23](22_23_e11_environment_security_compatibility.md) | 5 profile lock/preflight/SBOM pending |
| ARC09-07 Future Product | APPROVED | [22_20](22_20_e11_local_system_architecture.md) | Product gaps independently unresolved |

[44 formal requirement ⇄ BD Trace](22_91_bd01_requirement_architecture_trace.md) はすべて責務へ割当済み。これを設計の科学・実装検証済みとの主張に使わない。

## 5. IF-01 / DD-01 / Gate06引渡し

1. **IF-01:** 旧v2／新E11 version dispatch、CLI option/schema、Result/Confidence Set、Scientific negative vs technical error、Backend Capability、Manifest/Artifact contract、Local export policy、reference/path semanticsを定義しFreezeレビューへ回す。
2. **DD-01:** 現行`ScientificCoreAdapter`・Product Port・CLI Manifestとの再利用可否、Method Adapter/typed bridge、Fail-closed use case、Safe staging/commit/readback、Permission/seed/Lock実効記録を採用済み7項目Classテンプレートへ展開する。
3. **Test/Gate06:** Architecture import static checks、negative cases、全Profile legacy regression、atomic crash/readback、authorization/export、typing/interoperability、41 Method別Implementation Testの事前freeze条件を管理する。
4. **Gate07:** Method/Semantic Oracle、CI Coverage、FWER、Monte Carlo, Compute、Backend、Licenseを独立判定。未測定EvidenceをPASSと扱わない。
5. **Owner:** 完成するADR/IF/Port/Schema/残Open findingのDispositionと実名責任者、実装WP／Coding authorityを別途記録する。

## 6. Canonical promotion boundary

- 本レビューとBD改訂は`Revised_requirements_definition_documents/`のみで行った。元`docs/wiki/requirement_definition/`正本は未更新。
- 元正本への昇格は[Owner決定](../93_enh_e11_canonical_promotion_policy.md)の**ENH-E11対象テスト全件PASS後のみ**。
- `Owner Architecture policy APPROVED` ≠ `Independent Architecture Review PASS` ≠ `Gate06 PASS` ≠ `Gate07 Science PASS` ≠ `Delivery Legal APPROVED`。
