# 10_91_acceptance_conditions


---

## 12. 総合完了条件

1. E2EシナリオがWeb API、Worker、Persistence、FrontendおよびCLI/library境界を通して成立する。
2. ACTIVE Requirementについて、Requirement Levelおよび設計上のverification contractに応じたtest、benchmarkまたはreview evidenceを用意できる。
3. DEFERRED Requirementはcurrent mandatory acceptanceへ混在させない。
4. ACTIVEなScientific Integrity Requirementについて、必要な自動test、scientific benchmarkまたはreview checklistによるverification evidenceを用意できる。
5. `causal-analysis-spec/2`および`predictive-analysis-spec/1`等のcurrent scientific contractを保持する。
6. `AnalysisSpecification.analysis_family`を再利用し、duplicate Family discriminatorを追加しない。
7. AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。
8. CLI / Python library / backend use case / runtime executorがCurrent Navigation Stageなしでanalysisを実行できる。
9. Product Domain / runtime execution layerからbrowser route / Navigation Stageへの逆依存がない。
10. Project Management / Analysis Workspace / Family / Stageのresponsibilityが同一navigation hierarchyへ再混在していない。
11. Project routeとAnalysis routeのdirect link / reload / Back / Forwardがdeterministicに成立する。
12. Analysis ContextのProject scope / Dataset-Version compatibility / read-only Current Project semanticsが守られる。
13. UI再編だけを理由とする新しいDB schema / API / backend execution semanticsが導入されていない。
14. 正本文書、OpenAPI、DB schema、Frontend文言およびtestが同じFamily / Navigation Stage / Execution Stage用語とcontractを使用する。
15. advanced Predictive engine未導入環境でもcore process startupとexisting logistic/linear + coefficient flowが成立する。
16. new fitted model writeはprovider-neutral `fitted-model/2` contractを満たし、existing `fitted-model/1`はread-compatibleである。
17. Predictive capability metadata、backend validation、Frontend selectionが同一model/method compatibility authorityと整合する。
18. SHAP/LIME/coefficient explanationをcausal effectまたはcausal mechanismへ読み替えない。

## 12.1. Local Scientific CLIの追加受入条件

1. 承認範囲の68 Scope行をR/Q/N/Dの処遇で追跡し、D（将来提供）を現行必須機能に算入しない。
2. 対象41 MethodのEstimand、適格条件、推論可用性、実効Backend／Library版、既知真値、負例、参照比較についてMethod別の独立検証証拠を求める。
3. 10 UCから正式FR/NFR/科学的ARとMethod契約・受入Evidenceを追跡可能にする。
4. 科学的受入はfamilywise error rate `FWER=0.05`の承認方針と、Method別の事前指定K/R/MC・計算資源上限・coverage・Monte Carlo誤差を満たす必要がある。計画のみをPASSとして扱わない。
5. 旧`causal-analysis-spec/2`、既存Product Web/API/Worker/DB、CLI、既存FR/NFR/ARへの互換性を保護する。
6. 個票CATEやLocal Artifactのプライバシー、部分保存の正常公開防止、Optional Backend不在の隔離を受入条件とする。顧客納入／受領者別License承認・SBOM/Legal Release WorkflowはENH-E11初期受入対象外。

## 12.2. 既存の定量的受入条件

- **`AR-016`**：適用可能なSubgroup metricで`sample_count`を保持し、信頼水準0.95のpercentile bootstrap（1000 resamples、deterministic seed）で計算可能なときのみuncertaintyを併記する。対象外・計算不能の区間を生成しない。
- **`FR-072`**：直接metric差分は同一DatasetVersion、同一TEST-row identity/hash、同一定義metricの一致を要する。
- **`AR-027`**：SHAP/LIME/coefficient contributionを因果効果または因果機構の証拠として表示しない。
- **`NFR-035`**：Method別の独立科学受入と多重性管理を求める。前項の条件を抽象的な能力表現によって弱めない。

`AR-016`のbootstrap条件をE11全ての因果Estimatorへの普遍的な推論要件へ一般化してはならない。

## 12.3. Local Scientific CLIの受入契約

1. 既存Product全体の§12は保持するが、新E11の実装対象は§12.1に列挙されたLocal Scientific CLIに限定する。変更影響が及ぶProductの回帰、および最終候補での旧v2互換性検証を実施する。
2. `FR-195/NFR-031`：Study単一明示opt-in、default拒否、実効UID/private ext4/XFS Root、Method別Schema/caps、個票生成前のdeny、aggregate/manifest/logへの値漏洩禁止、再利用Study時の毎回の適格性再検証をPositive/Negativeで確認する。
3. `NFR-030`：G01実OS上でatomic no-clobber、stage/rename/marker/Reader、失敗時のfalse-success防止と不定状態を確認する。全故障組合せや未検証の電源断耐久性を主張しない。
4. `NFR-035/AR-044`：独立DGP/NEG/REFと定量推論・FWERについて全41 Methodに有効証拠を必要とする。G10再利用にはMethod・共有Kernel・依存Lock・Fixture・Reference・Backend・評価契約を含む推移的影響閉包の不変性を検証し、変化/不明ならMethod再試験またはBLOCK。最終候補の横断統合/旧Product互換性は実測する。
5. 共有Method Schema/RowSchema/Graph/Portsは各Methodの科学的区別、厳格Positive/Negative parityとPrivacyを保持して初めて利用可能とする。設計承認はMethod/Profile/Backend実測やGate PASSを意味しない。


### G01 publication authorization consistency (NFR-030/031; G01-07-05/06/11)

Acceptance requires both valid same-run aggregate publication and denied cases for decision absence, denial, forgery, wrong run/request hash, wrong verified root FD, changed EUID, policy re-evaluation disagreement, and staged inventory/classification mutation. **All rejected cases must prevent a successfully sealed/published run**; actual Linux FD, secure stage, atomic no-replace, Reader and filesystem checks remain necessary. Pure decision tests alone cannot pass G01_999. This is a clarification of existing NFR-030/031 and related Gate tests, not an additional deferred product feature.


### G01 P01 pure-contract and cross-file acceptance distinction (FR-201/NFR-029)

G01 must separately prove (a) strict versioned Study/ContentRef/Method/Estimand/privacy decoding, (b) deterministic JCS golden bytes and four distinct hashes, (c) pure positive and synthetic justified-negative Manifest envelopes, five-field input lineage joins, safe output Graph Ref relative to TrustedRoot and exact inventory / Status consistency, and (d) physical P02/P05 Reader verification of actual Study/Status/Graph and secure files. A scientific-negative pure fixture may use the reserved G01 reason SCI_NO_ADMISSIBLE_PAG but **must not** establish that a real FCI run proves no admissible PAG. Technical reasons even when repeated in Status and factory evidence are rejected. P01 developer tests cannot be promoted to G01_999 independent science/OS PASS.


### G01 decision-equivalence positive/negative test boundary (NFR-030/031)

Test **both** the genuine-policy-produced decision and an independently reconstructed, immutable, schema-valid **value-identical** decision: each must be accepted **only when** the Publisher independently authorizes the current staged Study/root/UID and inventory. Test mismatched allowed/run/hash/root FD/UID/classification/row flag/output shape, denied policy, altered Study/inventory and untrusted policy substitution as rejects before Marker/rename. **Do not require rejection solely because a decision object was reconstructed.** No issuer attestation is in scope. Positive outcome still requires physical FS/Reader proof, not mere DTO equality.
