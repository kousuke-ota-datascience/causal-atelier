# 10_91_acceptance_conditions

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

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

## 12.1. ENH-E11の追加総合受入条件（正式要件発行時点）

1. DEC09の68 Scope行についてR/Q/N/Dを区別し、既存・新規Requirementへ追跡する。後続送りDを初期実装の完了義務と見なさない。
2. 全41 Methodを、Method別Estimand・適格性・推論Availability・実効Backend/Library・既知真値・科学的負例・参照比較で独立検証する。
3. 10 UCについて、Formal FR/NFR/Scientific AR、Method Scope、実装Workstream、受入Evidenceを追跡可能にする。
4. DEC07採用のGate-wide `FWER=0.05`方針とMethod別K/R/MC・Compute Budgetは、独立受入用の事前登録・Owner Freeze・科学的評価を別途必要とする。未測定値を科学的PASSとして扱わない。
5. 旧`causal-analysis-spec/2`と既存Product Web/API/Worker/DB、CLI、既存FR/NFR/ARの互換性を保護する。
6. 個票CATEやLocal Artifactの機微情報保護、Partial Artifactの不正公開防止、Optional Backend不在の隔離、配布前ライセンス審査を必須とする。

**Evidence status:** `NOT_GENERATED / GATE06_GATE07_NOT_FROZEN / SCIENCE_NOT_RUN`。計画の承認と科学的受入は区別する。[全件Trace](../96_rd03_formal_requirement_traceability.md)を参照。
