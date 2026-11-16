# ENH-E11 — SR-04 Gate07 Traceability（策定Draft）

**区分:** working_notes／SR-04-Fの追跡設計案。正式Scope/FR/NFR/AR、Architecture Review、Gate06/07 freeze、Work Package、Science PASS、Coding許可ではない。  
**策定日:** 2026-11-15 JST。**branch:** prototype/ariadne_mvp。**状態:** TRACE_DRAFT / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN / PENDING_FULL_CONCEPT_APPROVAL。  
**先行資料:** [00_04 Scope案](../00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md)／[03 Requirements](../00_enhance_background/03_requirements_revision.md)／[05 Gate候補](../00_enhance_background/05_requirements_design_consistency_and_traceability_review.md)／[SR04-A](20261115_sr04_method_acceptance_matrix_draft.md)／[SR04-B](20261115_sr04_scientific_fixture_catalog_draft.md)／[SR04-C](20261115_sr04_reference_specification_draft.md)／[SR04-D](20261115_sr04_quantitative_acceptance_criteria_draft.md)／[SR04-E](20261115_sr04_execution_environment_contract_draft.md)。

> **2026-11-16個別判断更新:** [DEC-SR04-01（B1-A）／DEC-SR04-02（DRIV-A）](20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md)をHuman ownerのsemantic target判断として**採用済み**。P3-M11の加法線形IV係数とP2-M08の条件付きIV構造斜率について**Owner決裁待ちは解消**したが、`OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED`はBackend実効適格性・独立Inference/AR検証・定量AC・正式schema/FR/ADR/Gateが未完であることを表す。元のGate/Science証拠は一切生成されていない。

> **2026-11-16 Owner判断：** [DEC-SR04-03 FD-A](20261116_sr04_dec03_frontdoor_fd_a_owner_decision.md) および [DEC-SR04-04 GRAPH-A](20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md) を個別採用。FD-AはP1-M07の**線形・単一Mediator数値Method方針**、GRAPH-AはP1-M06／P3-M01〜03の**独立Graph Oracle原理**を固定した。Source schema/Oracleの実装、DoWhy実効stage/CI、FCI/LPCMCI/PCMCI+の独立同値類Oracle、Graph accuracy、正式Gate Evidenceは未生成。

> **2026-11-16 DEC-SR04-05-1〜7をOwner個別採用:** [準実験7手法のEstimator／Inference判断](20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md)。初期Method基準と条件付き推論方針のみ決定。P3-M12 SCMは初期defaultを探索的点推定に限定しPlacebo順位を95%CIと認定しない。他6手法のCIも実効Method/cluster/coverageの認証前は未承認。**正式FR/ADR/Schema/Gate、Science Benchmarkは未実施。**

> **DEC-SR04-06（2026-11-16）Owner個別採用済み:** [NCE/NCO/OLS partial R²・RV独立技術記録](20261116_sr04_dec06_negative_control_ols_rv_scope_decision_proposal.md)と02承認記録第23項で**DEC06-1〜5すべてAを採用**。P1-M18/P1-M19を実在Observed NCE/NCO、P1-M20を古典OLS partial R²＋point RV（q=1）の初期Nとする。X-04/X-05の未提供の広範方式は初期非採用D。**Owner Scope採用のみCLOSED**であり、Null size/power・RV独立数値Oracle・正式FR/NFR/AR/Gate07・Science Evidenceは未完了。Method行は`OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED`とする。

> **DEC-SR04-07（2026-11-16）Owner正式個別採用:** [Quantitative Acceptance／Monte Carlo／Computeの独立判断記録](20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)と02承認記録第24項により**DEC07-1〜7全A採用済み**。41 Method／68 Scope／45 Quant ACのレジストリ構成は維持。FWER=0.05、Hard統計比較Kの事前列挙、Wilson/連続MC bound、Method別R/Pass確率、T2 Pilot、実測予算・seed・中断/失敗分母とGate分離を**設計方針として採用**。**実効K/R/Cell/inner-bootstrap/CPU・Money予算、Method-specific閾値の本適用、正式Gate Evidenceは未freeze**。

> **DEC-SR04-08事前設計（Owner採否待ち、2026-11-16）:** [uv.lock／Backend／Optional Dependency／License独立技術判断案](20261116_sr04_dec08_backend_optional_dependency_lock_license_owner_decision_proposal.md)を作成。既存5 Environment Profile＋条件付きRD候補、Method別Backend、pyproject／universal uv.lock、SR02候補版・実効Lock検証、SBOMとGPL Customer Delivery Gateを別契約とした。**DEC08-1〜8は全A推奨・Owner未採用**。ENV-AC01〜09のScope/Method連結・NOT_GENERATEDは変えない。現行uv.lockはDoWhy/EconML/Tigramite/rdrobust未登録、SR02単独install/API smokeと同一環境ではない。

## 0. 名前空間・証拠の厳格な境界

**名前衝突:** 00_04の「X-01〜X-10」は68 Scope行の上位横断要求であり、SR04-Aの「X-01〜X-09」は横断受入Contract。以降前者を SCOPE:X-xx、後者を SR04:X-xx と表記する。**SCOPE:X-04 ≠ SR04:X-04。** 元ファイルのIDは変更しない。

**Gate衝突:** 05案にある G01〜G10は未freezeの暫定Gate群で、05の G07（DiD/Event/ITS領域）を正式Gate07科学受入と同一視しない。以下 PLAN:Gnn は候補配置であり、Methodごとの正式Gate07 Evidenceはすべて NOT_GENERATED。Issue open/API smoke/Draft作成はScience PASSではない。

**Evidence型:** Method→Scope→DGP/NEG→独立Reference→AC/ENV-AC→E11-REQ Draft→Issue→PLAN:Gnn→正式Gate07証拠。識別対象、Science妥当性、実装実行可能性を別判定し、対象未確定なら BLOCKED。NCE/NCO/RV候補や後続送りを承認済みMethodへ格上げしない。

## 1. 全41 Method のPrimary Traceability

| Method ID・対象 | Scope ID（SCOPE） | DGP/NEG | 独立REF | Quantitative AC | Environment | Requirement Draft / Issue | PLAN Gate / Evidence |
|---|---|---|---|---|---|---|---|
| P1-M01 Native Randomized identification／A | SCOPE:P1-06 | DGP-001; NEG-001, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | ENV-BASE | E11-REQ-P1I / #15,#16 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M02 Native Backdoor identification／ATE | SCOPE:P1-06, SCOPE:P1-07 | DGP-002, DGP-021; NEG-002, NEG-003 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | ENV-BASE | E11-REQ-P1I / #15,#16 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M03 DoWhy Backdoor identification／ATE候 | SCOPE:P1-08 | DGP-002, DGP-021; NEG-002, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | ENV-DOWHY | E11-REQ-P1I / #16 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M04 DoWhy Frontdoor identification／ATE | SCOPE:P1-08 | DGP-005; NEG-004 | REF-G01, REF-I02 | AC-D01, AC-D02, AC-D07 | ENV-DOWHY | E11-REQ-P1I / #16 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M05 DoWhy IV identification／方法固有の対象は未確 | SCOPE:P1-08 | DGP-006; NEG-006, NEG-007 | REF-I03, REF-G01 | AC-D01, AC-D02, AC-D07 | ENV-DOWHY | E11-REQ-P1I / #16 | PLAN:G02 / BLOCKED / NOT_GENERATED |
| P1-M06 FCI／PAGと等価類 | SCOPE:P1-09 | DGP-011, DGP-021; NEG-003, NEG-021, NEG-028 | REF-G02 | AC-D02, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | ENV-BASE | E11-REQ-P1G / E11-REQ-SR03D06 / #17 | PLAN:G01 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| P1-M07 Frontdoor two-stage regression／ATE | SCOPE:P1-08 | DGP-005; NEG-004, NEG-005 | REF-I02, REF-E04 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02 | ENV-DOWHY | E11-REQ-P1I / #16 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED |
| P1-M08 Native diff-in-means／ATE | SCOPE:P1-11 | DGP-001, DGP-022; NEG-001, NEG-010 | REF-E01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | ENV-BASE | E11-REQ-P1W / #19 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M09 Native OLS／採用済み契約範囲のATE/ATT表現 | SCOPE:P1-11, SCOPE:P1-17 | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020 | REF-E01, REF-I01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | ENV-BASE | E11-REQ-P1W / #19,#16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M10 Native IPW／ATE・ATT（別fixture） | SCOPE:P1-11, SCOPE:P1-12 | DGP-002, DGP-003; NEG-010, NEG-018 | REF-E02 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05 | ENV-BASE | E11-REQ-P1W / #19 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M11 Native AIPW／ATE・ATT（別fixture） | SCOPE:P1-11, SCOPE:P1-12 | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012 | REF-E03 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | ENV-BASE | E11-REQ-P1W / #19 | PLAN:G03 / BLOCKED / NOT_GENERATED |
| P1-M12 Placebo Treatment refutation／null診 | SCOPE:P1-13 | DGP-022; NEG-014 | REF-R01 | AC-D01, AC-R01, AC-T01 | ENV-BASE | E11-REQ-P1R / #16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M13 Data Subset refutation／安定性 | SCOPE:P1-13 | DGP-001, DGP-002; NEG-015 | REF-R01 | AC-D01, AC-D03, AC-R02 | ENV-BASE | E11-REQ-P1R / #16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M14 Random Common Cause refutation／摂動安 | SCOPE:P1-14 | DGP-002; NEG-017 | REF-R01 | AC-D01, AC-D03, AC-R02 | ENV-BASE | E11-REQ-P1R / #16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M15 Bootstrap refutation／再標本化安定性 | SCOPE:P1-14 | DGP-001, DGP-002; NEG-016 | REF-R01 | AC-D01, AC-D03, AC-R02 | ENV-BASE | E11-REQ-P1R / #16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M16 Adjustment Set Sensitivity／設計変更 | SCOPE:P1-16 | DGP-021, DGP-002; NEG-002 | REF-G01, REF-R01 | AC-D01, AC-D02, AC-R02 | ENV-BASE | E11-REQ-P1S / #16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M17 Propensity Clipping Sensitivity／tr | SCOPE:P1-16 | DGP-002, DGP-023; NEG-010, NEG-018 | REF-E02, REF-R01 | AC-D03, AC-R05 | ENV-BASE | E11-REQ-P1S / #16 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M18 Observed NCE null diagnostic／条件付き関 | SCOPE:P1-15, SCOPE:X-04 | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | ENV-BASE | E11-REQ-P1NC / #16,#14 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P1-M19 Observed NCO null diagnostic／条件付き関 | SCOPE:P1-15, SCOPE:X-04 | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | ENV-BASE | E11-REQ-P1NC / #16,#14 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P1-M20 OLS partial R² / RV sensitivity／指定 | SCOPE:P1-17, SCOPE:X-05 | DGP-020; NEG-020 | REF-R03 | AC-D01, AC-D03, AC-R04 | ENV-BASE | E11-REQ-P1S / #16,#14 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P2-M01 LinearDML／CATE(x) | SCOPE:P2-02 | DGP-003; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M02 CausalForestDML／CATE(x) | SCOPE:P2-03 | DGP-004; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M03 DRLearner／CATE(x) | SCOPE:P2-04 | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M04 ForestDRLearner／CATE(x) | SCOPE:P2-05 | DGP-004; NEG-010, NEG-011, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M05 S-Learner／CATE(x) | SCOPE:P2-06 | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M06 T-Learner／CATE(x) | SCOPE:P2-07 | DGP-003, DGP-004; NEG-010, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M07 X-Learner／CATE(x) | SCOPE:P2-08 | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M08 DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE | SCOPE:P2-09 | DGP-008; NEG-009, NEG-012, NEG-013 | REF-E06 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | ENV-ECONML | E11-REQ-P2 / E11-REQ-SR03D05 / #18,#22 | PLAN:G04 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M01 PCMCI／time-lagged graph | SCOPE:P3-02 | DGP-009; NEG-021 | REF-G03 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G05 | ENV-TIGRAMITE | E11-REQ-P3T / #20 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P3-M02 PCMCI+／time-series CPDAG | SCOPE:P3-03 | DGP-009, DGP-010; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | ENV-TIGRAMITE | E11-REQ-P3T / #20 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| P3-M03 LPCMCI／time-series PAG | SCOPE:P3-04 | DGP-011; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | ENV-TIGRAMITE | E11-REQ-P3T / #20 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| P3-M04 DiD／ATT（2×2とstaggeredは別契約） | SCOPE:P3-07 | DGP-012, DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | ENV-BASE / backend pending | E11-REQ-P3D / #21 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M05 Event Study／event-time効果 | SCOPE:P3-08 | DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | ENV-BASE / backend pending | E11-REQ-P3D / #21 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M06 Interrupted Time Series／介入時点のlevel | SCOPE:P3-09 | DGP-014; NEG-023 | REF-Q02 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02 | ENV-BASE / backend pending | E11-REQ-P3D / #21 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M07 Sharp RDD／cutoff局所効果 | SCOPE:P3-10 | DGP-015; NEG-023 | REF-Q03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | ENV-BASE / backend pending | E11-REQ-P3I / #22 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M08 Fuzzy RDD／cutoff局所complier効果 | SCOPE:P3-11 | DGP-016; NEG-006, NEG-023 | REF-Q03, REF-I03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | ENV-BASE / backend pending | E11-REQ-P3I / #22 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M09 Wald ratio／binary Z/A complier LAT | SCOPE:P3-12 | DGP-006; NEG-006, NEG-007 | REF-I03, REF-E07 | AC-D03, AC-P01, AC-P03, AC-P05, AC-D07 | ENV-BASE / backend pending | E11-REQ-P3I / #22 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P3-M10 B0 just-identified 2SLS／binary Z/A | SCOPE:P3-12 | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | ENV-BASE / backend pending | E11-REQ-P3I / #22 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P3-M11 B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | SCOPE:P3-12 | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | ENV-BASE / backend pending | E11-REQ-P3I / #22 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M12 Synthetic Control／処置単位の時点別反実仮想ギャップ | SCOPE:P3-13 | DGP-017; NEG-024 | REF-Q04 | AC-D03, AC-P01, AC-P03, AC-Q04 | ENV-BASE / backend pending | E11-REQ-P3S / #23 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED |
| P3-M13 Synthetic DiD／panel平均介入効果 | SCOPE:P3-14 | DGP-018; NEG-024 | REF-Q05 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q05 | ENV-BASE / backend pending | E11-REQ-P3S / #23 | PLAN:G09 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

## 2. 全68 Scope行のDispositionとSR-04への接続

00_04のR/Q/N/Dは未承認スコープ案。DおよびProductの後続部分をSR04文書で閉鎖したとはみなさない。X-scopeとX-contractは別物である。

| Scope ID | 00_04 Disposition案 | Method direct | SR04 Cross / Deferred境界 | E11-REQ案 | Issue | Trace status |
|---|---|---|---|---|---|---|
| SCOPE:P1-01 | R | — | SR04:X-01 | E11-REQ-P1Q | #15 | CROSS_BOUND |
| SCOPE:P1-02 | R+N／D | — | SR04:X-01, SR04:X-05 | E11-REQ-P1Q | #15,#24 | CROSS_BOUND |
| SCOPE:P1-03 | R+N | — | SR04:X-01 | E11-REQ-P1Q | #15 | CROSS_BOUND |
| SCOPE:P1-04 | R | — | SR04:X-03 | E11-REQ-P1G / SR03D06 | #17 | CROSS_BOUND |
| SCOPE:P1-05 | R／D | — | SR04:X-03 | E11-REQ-P1G / SR03D06 | #17 | CROSS_BOUND |
| SCOPE:P1-06 | R | P1-M01, P1-M02 | SR04:X-02 | E11-REQ-P1I / P1G | #15,#16 | METHOD_BOUND |
| SCOPE:P1-07 | R | P1-M02 | SR04:X-02, SR04:X-03 | E11-REQ-P1I / P1G | #15 | METHOD_BOUND |
| SCOPE:P1-08 | N（Frontdoor数値推定をPhase1に含む方針採用） | P1-M03, P1-M04, P1-M05, P1-M07 | — | E11-REQ-P1I / P1G | #16 | METHOD_BOUND |
| SCOPE:P1-09 | N | P1-M06 | SR04:X-03 | E11-REQ-P1I / P1G | #17 | METHOD_BOUND |
| SCOPE:P1-10 | R+N | — | SR04:X-02 | E11-REQ-P1I / P1G | #15,#16 | CROSS_BOUND |
| SCOPE:P1-11 | R | P1-M08, P1-M09, P1-M10, P1-M11 | — | E11-REQ-P1W | #19 | METHOD_BOUND |
| SCOPE:P1-12 | R+Q | P1-M10, P1-M11 | — | E11-REQ-P1W | #19 | METHOD_BOUND |
| SCOPE:P1-13 | R | P1-M12, P1-M13 | — | E11-REQ-P1R | #16 | METHOD_BOUND |
| SCOPE:P1-14 | N | P1-M14, P1-M15 | — | E11-REQ-P1R | #16 | METHOD_BOUND |
| SCOPE:P1-15 | N（DEC06-1/2 Observed NCE/NCO 初期NをOwner個別採用） | P1-M18, P1-M19 | — | E11-REQ-P1NC | #16 | METHOD_BOUND |
| SCOPE:P1-16 | R | P1-M16, P1-M17 | — | E11-REQ-P1S | #16 | METHOD_BOUND |
| SCOPE:P1-17 | N（DEC06-3 古典OLS partial R²＋point RV Owner個別採用）／D（汎用Sensitivity） | P1-M09, P1-M20 | 後続/例外案 | E11-REQ-P1S | #16 | METHOD_BOUND+PART_DEFERRED |
| SCOPE:P1-18 | R+N／D | — | SR04:X-05 | E11-REQ-CLI | #15,#24,#14 | CROSS_BOUND |
| SCOPE:P1-19 | D | — | SR04:X-08 | E11-REQ-CLI | #14 | CROSS_BOUND |
| SCOPE:P1-20 | R+N | — | SR04:X-05, SR04:X-07 | E11-REQ-CLI | #16,#24 | CROSS_BOUND |
| SCOPE:P1-21 | R+N | — | SR04:X-09 | E11-REQ-CLI | #16,#17,#24 | CROSS_BOUND |
| SCOPE:P2-01 | N | — | SR04:X-01, SR04:X-04 | E11-REQ-P2 | #18 | CROSS_BOUND |
| SCOPE:P2-02 | N | P2-M01 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-03 | N | P2-M02 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-04 | N | P2-M03 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-05 | N | P2-M04 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-06 | N | P2-M05 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-07 | N | P2-M06 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-08 | N | P2-M07 | — | E11-REQ-P2 | #18 | METHOD_BOUND |
| SCOPE:P2-09 | N | P2-M08 | — | E11-REQ-P2 | #18,#22 | METHOD_BOUND |
| SCOPE:P2-10 | N | — | SR04:X-01, SR04:X-04 | E11-REQ-P2 | #18 | CROSS_BOUND |
| SCOPE:P2-11 | R+N | — | SR04:X-07 | E11-REQ-P2 | #18,#24 | CROSS_BOUND |
| SCOPE:P2-12 | R+N | — | SR04:X-05 | E11-REQ-P2 | #18,#24 | CROSS_BOUND |
| SCOPE:P2-13 | R+N | — | SR04:X-02 | E11-REQ-P2 | #18 | CROSS_BOUND |
| SCOPE:P2-14 | N | — | SR04:X-04 | E11-REQ-P2 | #18 | CROSS_BOUND |
| SCOPE:P2-15 | N | — | SR04:X-06 | E11-REQ-P2A | #18,#24 | CROSS_BOUND |
| SCOPE:P2-16 | N | — | SR04:X-09 | E11-REQ-P2 | #18,#24 | CROSS_BOUND |
| SCOPE:P2-17 | N | — | SR04:X-09 | E11-REQ-P2 | #18 | CROSS_BOUND |
| SCOPE:P2-18 | D／N | — | SR04:X-06, SR04:X-08 | E11-REQ-P2A | #18,#24 | CROSS_BOUND |
| SCOPE:P3-01 | N | — | SR04:X-01, SR04:X-03 | E11-REQ-P3T | #20 | CROSS_BOUND |
| SCOPE:P3-02 | N | P3-M01 | — | E11-REQ-P3T | #20 | METHOD_BOUND |
| SCOPE:P3-03 | N | P3-M02 | — | E11-REQ-P3T | #20 | METHOD_BOUND |
| SCOPE:P3-04 | N | P3-M03 | — | E11-REQ-P3T | #20 | METHOD_BOUND |
| SCOPE:P3-05 | R+N | — | SR04:X-07 | E11-REQ-P3T | #20 | CROSS_BOUND |
| SCOPE:P3-06 | N | — | SR04:X-03 | E11-REQ-P3T | #20 | CROSS_BOUND |
| SCOPE:P3-07 | N | P3-M04 | — | E11-REQ-P3D | #21 | METHOD_BOUND |
| SCOPE:P3-08 | N | P3-M05 | — | E11-REQ-P3D | #21 | METHOD_BOUND |
| SCOPE:P3-09 | N | P3-M06 | — | E11-REQ-P3D | #21 | METHOD_BOUND |
| SCOPE:P3-10 | N | P3-M07 | — | E11-REQ-P3I | #22 | METHOD_BOUND |
| SCOPE:P3-11 | N | P3-M08 | — | E11-REQ-P3I | #22 | METHOD_BOUND |
| SCOPE:P3-12 | N（初期推定器A＋Bをオーナー採用） | P3-M09, P3-M10, P3-M11 | SR04:X-04 | E11-REQ-P3I | #22 | METHOD_BOUND |
| SCOPE:P3-13 | N | P3-M12 | — | E11-REQ-P3S | #23 | METHOD_BOUND |
| SCOPE:P3-14 | N | P3-M13 | — | E11-REQ-P3S | #23 | METHOD_BOUND |
| SCOPE:P3-15 | N | — | SR04:X-01, SR04:X-02 | E11-REQ-CLI | #21,#22,#23 | CROSS_BOUND |
| SCOPE:P3-16 | N | — | SR04:X-09 | E11-REQ-CLI | #20,#21,#22,#23,#24 | CROSS_BOUND |
| SCOPE:P3-17 | R+N | — | SR04:X-05, SR04:X-06 | E11-REQ-CLI | #20,#24 | CROSS_BOUND |
| SCOPE:P3-18 | D | — | 後続/例外案 | E11-REQ-P3T | #20 | DEFERRED_REQUIRES_OWNER |
| SCOPE:P3-19 | D／N | — | SR04:X-08 | E11-REQ-CLI | #21,#22,#23,#24 | CROSS_BOUND |
| SCOPE:X-01 | D（要承認） | — | 後続/例外案 | DEFERRED | #14 | DEFERRED_REQUIRES_OWNER |
| SCOPE:X-02 | D | — | 後続/例外案 | DEFERRED | #14 | DEFERRED_REQUIRES_OWNER |
| SCOPE:X-03 | D（要承認） | — | 後続/例外案 | DEFERRED | #14 | DEFERRED_REQUIRES_OWNER |
| SCOPE:X-04 | N一部（NCE/NCO Owner個別採用）／D（simulated/Graph） | P1-M18, P1-M19 | 後続/例外案 | E11-REQ-P1NC | #16,#14 | METHOD_BOUND+PART_DEFERRED |
| SCOPE:X-05 | N一部（OLS partial R²/RV Owner個別採用）／D（IPW/AIPW/CATE一般化） | P1-M20 | 後続/例外案 | E11-REQ-P1S | #16,#14 | METHOD_BOUND+PART_DEFERRED |
| SCOPE:X-06 | Q一部／D | — | SR04:X-04, SR04:X-07 | E11-REQ-SR03D05 | #19,#20,#21,#24 | CROSS_BOUND |
| SCOPE:X-07 | D | — | 後続/例外案 | DEFERRED | #14 | DEFERRED_REQUIRES_OWNER |
| SCOPE:X-08 | D | — | 後続/例外案 | DEFERRED | #14 | DEFERRED_REQUIRES_OWNER |
| SCOPE:X-09 | R+N／D | — | SR04:X-05, SR04:X-08, SR04:X-09 | E11-REQ-CLI | #14,#24 | CROSS_BOUND |
| SCOPE:X-10 | R+N／D | — | SR04:X-01, SR04:X-06, SR04:X-08 | E11-REQ-CLI | #14,#24 | CROSS_BOUND |

**後続の明示処遇:** SCOPE:X-01/02/03/07/08＝A0のATC/mediation/matching/policy/monitoring等の未承認Deferred候補。SCOPE:X-04/05＝NCE/NCO・OLS partial R²候補のOwner Method採否待ち。P1-19/P2-18/P3-19＝Product API/UI/Worker/DBの後続部分をCLI横断回帰で閉鎖しない。GAP-C01〜04の正式帰属もOPEN。

## 3. 検証用に参照したSource Blob（固定承認SHAではない）

| 参照資料 | Git blob SHA |
|---|---|
| gate | `4bd58ed903d31a6d2b59401914b1159c4de93ad6` |
| req | `b75d2e315794d41ec7cc33bd3446ab302115b88b` |
| scope | `5276ec87f5249e876e5185f19fe8d3e1566c600c` |
| matrix | `6d9f0bdacfed77401630ee099b900f9a1868a832` |
| fixture | `a93c744b0fe87124a81b8d4c7701c0d382a72313` |
| quant | `f046ef66a0c3e51206b092e967f895ead5965541` |
| ref | `231cd74e81c186dbc2b8fde77489c0fb711828b4` |
| env | `d4021bc2fd5856b5b00d840e5cb4f83a5f53b81d` |

**後続節（Cross9 / NEG28 / AC45 / ENV-AC9 / Requirement・Gate / Evidence）はこの文書の一部として追加記載する。** この段階の文書の状態はTRACE_DRAFTであり、Science PASSではない。


## 4. SR04横断9件の独立Traceability

SR04:X-* は受入Contract、SCOPE:X-* は68 Scopeの上位行。両者は別物。PLAN Gateは05の未承認案であり正式Gate07 Evidenceではない。

| SR04 Cross | 主なAcceptance | SCOPEとの対応 | Requirement候補 | ENV-AC | PLAN Gate | Evidence |
|---|---|---|---|---|---|---|
| SR04:X-01 | E11 versioned local schema／P1-01〜03,P2-01/10,P3-01/15 | SCOPE:P1-01, SCOPE:P1-02, SCOPE:P1-03, SCOPE:P2-01, SCOPE:P2-10, SCOPE:P3-01, SCOPE:P3-15, SCOPE:X-10 | E11-REQ-P1Q/CLI | ENV-AC01, ENV-AC07, ENV-AC08 | PLAN:G01/G02/G10 | NOT_GENERATED |
| SR04:X-02 | Normalized IdentificationResult→EstimatorSpec／D04 | SCOPE:P1-06, SCOPE:P1-07, SCOPE:P1-10, SCOPE:P2-13, SCOPE:P3-15 | E11-REQ-SR03/P1I | ENV-AC03, ENV-AC07 | PLAN:G02/G10 | NOT_GENERATED |
| SR04:X-03 | GraphVersion refix／P1-04/05/09,D06 | SCOPE:P1-04, SCOPE:P1-05, SCOPE:P1-07, SCOPE:P1-09, SCOPE:P3-01, SCOPE:P3-06 | E11-REQ-SR03D06/P1G | ENV-AC04, ENV-AC07 | PLAN:G01/G02 | NOT_GENERATED |
| SR04:X-04 | EffectResult inference／D03/D05/D06 | SCOPE:P2-01, SCOPE:P2-10, SCOPE:P2-14, SCOPE:P3-12, SCOPE:X-06 | E11-REQ-SR03/SR03D05 | ENV-AC06, ENV-AC07 | PLAN:G04/G08/G10 | NOT_GENERATED |
| SR04:X-05 | Lineage reproducibility／P1-02/18,P2-12/15,P3-17 | SCOPE:P1-02, SCOPE:P1-18, SCOPE:P1-20, SCOPE:P2-12, SCOPE:P3-17, SCOPE:X-09 | E11-REQ-CLI/P1Q | ENV-AC04, ENV-AC05, ENV-AC07 | PLAN:G10 | NOT_GENERATED |
| SR04:X-06 | Local Artifact/privacy／P2-15,P3-17 | SCOPE:P2-15, SCOPE:P2-18, SCOPE:P3-17, SCOPE:X-10 | E11-REQ-P2A/CLI | ENV-AC07, ENV-AC08 | PLAN:G05/G10 | NOT_GENERATED |
| SR04:X-07 | Backend optional dep／SR-02 | SCOPE:P1-20, SCOPE:P2-11, SCOPE:P3-05, SCOPE:X-06 | E11-REQ-CLI/P3T | ENV-AC01, ENV-AC02, ENV-AC03, ENV-AC09 | PLAN:G01/G04/G06/G10 | NOT_GENERATED |
| SR04:X-08 | Legacy Product/v2／D04 R2 | SCOPE:P1-19, SCOPE:P2-18, SCOPE:P3-19, SCOPE:X-09, SCOPE:X-10 | E11-REQ-SR03/CLI | ENV-AC07, ENV-AC08 | PLAN:G02/G10 | NOT_GENERATED |
| SR04:X-09 | Traceability／SR-01〜12 | SCOPE:P1-21, SCOPE:P2-16, SCOPE:P2-17, SCOPE:P3-16, SCOPE:X-09 | E11-REQ-CLI | ENV-AC06, ENV-AC07, ENV-AC08 | PLAN:G01〜G10 | NOT_GENERATED |

### 4.1. 横断Reference REF-X01（Methodではない独立Oracle）

SR04-C Reference Registryの`REF-X01`はNew E11 versioned schema、strict identification/estimator link、GraphVersion/lineage、CI/AR set typed serialization、privacy、optional dependencies、旧Product/v2回帰に対する**横断Contract Oracle**であり、特定Method IDには割り当てられない。適用先は**SR04:X-01〜X-09の全9件**（主たる証跡：X-01〜08のreadback/hash/override/privacy、X-09の68 Scope trace）。独立Golden reference/旧v2保護の検査コードと結果は`NOT_GENERATED`、正式Gate acceptanceは未実施。

## 5. NEG28件のMethod reverse index

負例のうち観測上検出不能な識別仮定違反は、自動拒否を要求しない。宣言上の無効入力拒否、計算失敗、統計的性能悪化を別に判定する。

| Negative ID | 関連Method | 反証対象 | Evidence |
|---|---|---|---|
| NEG-001 | P1-M01, P1-M08 | DGP-001で処置片群のみ、割付Design根拠空欄 | NOT_GENERATED |
| NEG-002 | P1-M02, P1-M03, P1-M09, P1-M16 | DGP-021でcollider Kを調整、媒介Mを総効果の調整に使用 | NOT_GENERATED |
| NEG-003 | P1-M02, P1-M06 | CPDAG/PAGを入力しDAGに黙って変換／未解決Graphを識別済と表記 | NOT_GENERATED |
| NEG-004 | P1-M04, P1-M07 | DGP-005で媒介M欠落／直接A→Y追加／U→Mを追加 | NOT_GENERATED |
| NEG-005 | P1-M07 | DGP-005のYモデルに非線形M又は効果修飾を追加、元の線形2-stageを適用 | NOT_GENERATED |
| NEG-006 | P1-M05, P3-M08, P3-M09, P3-M10 | DGP-006でcomplier比率0/微小、またはZ群片側欠落 | NOT_GENERATED |
| NEG-007 | P1-M05, P3-M09 | DGP-006にZ→Y直接矢印／Z-U相関／defierを追加 | NOT_GENERATED |
| NEG-008 | P1-M09, P3-M11 | DGP-007のCを欠落/後処置変数に変更、Y baselineに未指定非線形項 | NOT_GENERATED |
| NEG-009 | P2-M08 | DGP-008でconditional first-stageを0近傍、Z→Y直接、T/Z型不適合 | NOT_GENERATED |
| NEG-010 | P1-M08, P1-M10, P1-M11, P1-M17, P2-M02, P2-M04, P2-M05, P2-M06 | DGP-023のpositivity破綻／near-violation、少数arm | NOT_GENERATED |
| NEG-011 | P1-M11, P2-M01, P2-M03, P2-M04, P2-M07 | DGP-003/004で正しくないPS/outcome nuisanceの組合せ | NOT_GENERATED |
| NEG-012 | P1-M11, P2-M01, P2-M02, P2-M03, P2-M05, P2-M07, P2-M08 | Train/test fold混同、cross-fittingでvalidation label漏洩、same-sample nuisance再利用 | NOT_GENERATED |
| NEG-013 | P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08 | CATE評価xをsupport外に変更／推論設定None／不適合final estimator | NOT_GENERATED |
| NEG-014 | P1-M12 | DGP-022でPlacebo treatmentを元Aと同じ列に誤指定、又は再割付null不適格 | NOT_GENERATED |
| NEG-015 | P1-M13 | Data subsetでrare subgroupを消失、残存sample不足 | NOT_GENERATED |
| NEG-016 | P1-M15 | Bootstrapのiid resampleをcluster/timeに適用、seed未保存、nuisance再fit省略 | NOT_GENERATED |
| NEG-017 | P1-M14 | Random Common Causeを実際の未観測交絡補正と称する、又はrandom変数がconstant | NOT_GENERATED |
| NEG-018 | P1-M10, P1-M17 | Propensity clippingの閾値・weight定義変更、対象母集団の誤表示 | NOT_GENERATED |
| NEG-019 | P1-M18, P1-M19 | DGP-019のNCEでZ→Y直接経路を追加、NCOでA→Wを追加、null/conditioning根拠無し | NOT_GENERATED |
| NEG-020 | P1-M09, P1-M20 | DGP-020でHC3 SEをclassic SEと誤表示、partial R²∉[0,1)、指定外IPW/AIPWへ適用 | NOT_GENERATED |
| NEG-021 | P1-M06, P3-M01, P3-M02, P3-M03 | DGP-009〜011で重複timestamp、欠測、非定常、CI-test misspec、PAG endpointの強制DAG化 | NOT_GENERATED |
| NEG-022 | P3-M04, P3-M05 | DGP-012/013でparallel trends破綻、no anticipation違反、staggered TWFE contaminated | NOT_GENERATED |
| NEG-023 | P3-M06, P3-M07, P3-M08 | DGP-014〜016で同時介入、cutoff manipulation、mass points、弱いRD first-stage、悪いbandwidth | NOT_GENERATED |
| NEG-024 | P3-M12, P3-M13 | DGP-017/018でpost donor汚染、poor prefit、donor support不足、unit/time weight混同 | NOT_GENERATED |
| NEG-025 | P3-M10, P3-M11 | DGP-024で有限grid切断、AR-Q2を単一区間化、AR-Q4をEMPTY化、非PSD共分散 | NOT_GENERATED |
| NEG-026 | P1-M18, P1-M19 | DGP-019のγ=0だがU→A,Wは維持（NCOの偽警告stress）、又はNCE/NCO未指定 | NOT_GENERATED |
| NEG-027 | P1-M01, P1-M03 | 未承認Identification、Question/Graph/Design/Dataset hash mismatch、旧v2 override | NOT_GENERATED |
| NEG-028 | P1-M06, P3-M02, P3-M03 | GraphVersion再固定時に親を改変、編集根拠なし、又は旧PAG矢印を欠損 | NOT_GENERATED |

## 6. AC45件とENV-AC9件の逆引き登録

ACはMethod×DGP×n×推論の評価セルへ割り当ててから正式freezeする。下表でMethod直接参照のないルールも、横断/条件付きでの割当を閉じるまでOPENのまま保持する。

| Quant AC | Method direct references | Draft科学契約・残留条件 |
|---|---|---|
| AC-D01 | P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M12, P1-M13, P1-M14, P1-M15, P1-M16, P1-M18, P1-M19, P1-M20, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08, P3-M01, P3-M02, P3-M03 | 不一致0件／全固定case100%一致 |
| AC-D02 | P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M06, P1-M16 | 定義済みGraph-oracle上で100%の正誤一致 |
| AC-D03 | P1-M07, P1-M08, P1-M09, P1-M10, P1-M11, P1-M13, P1-M14, P1-M15, P1-M17, P1-M20, P3-M04, P3-M05, P3-M06, P3-M07, P3-M08, P3-M09, P3-M10, P3-M11, P3-M12, P3-M13 | abs(actual−ref) ≤ 1e−10 + 1e−8×max(1,abs(ref)) |
| AC-D04 | SR04:X-01/X-05/X-07（型・byte/hash完全一致） / RULE_BOUND_DRAFT | 数学上/論理上の離散量は完全一致（整数・列挙・byte hash） |
| AC-D05 | SR04:X-03/X-04/X-06（Graph/集合/成果物lossless） / RULE_BOUND_DRAFT | 集合・endpoint・schema/原因codeのlossless round-trip 100% |
| AC-D06 | SR04:X-05、ENV-AC04/05（RNG/再実行） / RULE_BOUND_DRAFT | deterministic componentは同一実効出力。並列数値推定のfloatはD03適用 |
| AC-D07 | P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P3-M09 | hard invalid fixtureの誤許可0件、legacy契約の期待差分0件 |
| AC-A01 | P3-M10, P3-M11 | set kind（bounded/2-ray/half-line/all-real）4/4一致、connected components、順序、開閉、無界端点の符号全て一致 |
| AC-A02 | P3-M10, P3-M11 | abs(endpoint−oracle) ≤ 1e−6×max(1,abs(oracle))。係数の特異・重根・near-tangentは対象外で別条件数に応じた精度契約 |
| AC-A03 | P3-M10, P3-M11 | 正確な独立二次不等式oracleで、各区間内部／外部／端点近傍の事前指定検査点について、端点上の浮動誤差帯を除く誤判定0件 |
| AC-A04 | P3-M10, P3-M11 | 正常just-ID ARでAVAILABLE/EMPTY 0件、unbounded/disconnected/all-realを切断してfinite CI化0件 |
| AC-A05 | P3-M10, P3-M11 | sample first-stage=0等でpoint unavailableでもARが定義可能なら信頼集合を評価。ARが未定義/分散非PSDなら正常EMPTYではなくtyped failure 100% |
| AC-I01 | P1-M07, P1-M08, P1-M09, P1-M10, P1-M11, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08, P3-M04, P3-M05, P3-M06, P3-M07, P3-M08, P3-M10, P3-M11, P3-M13 | 真のcoverage pに対する多重性補正済み片側Wilson下限 L(p) ≥ 0.93 |
| AC-I02 | P1-M07, P1-M08, P1-M09, P1-M10, P1-M11, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08, P3-M04, P3-M05, P3-M06, P3-M07, P3-M08, P3-M10, P3-M11, P3-M13 | failure割合fに対する多重性補正済み片側Wilson上限 U(f) ≤ 0.01 |
| AC-I03 | P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08 | pointwise(x) / average / simultaneousを正しく識別し、誤ったlabel 0件 |
| AC-I04 | SR04:X-04、P2-M01〜08、P3-M10/M11（報告専用） / RULE_BOUND_DRAFT | 平均幅・median幅・分位点・AR集合形状率を全て報告。一律上限は設けない |
| AC-I05 | SR04:X-04、推論提供Method（method-specific、conditional） / RULE_BOUND_DRAFT | inference method/backend/final model/nuisance/fold/bootstrap単位に別セルで評価 |
| AC-I06 | SR04:X-04、P2-M01〜08ほか推論Method（不適格/CI null） / RULE_BOUND_DRAFT | CI未対応・unsupported・対象不整合ではCI=null＋理由、confirmatory science-pass禁止 |
| AC-T01 | P1-M12, P1-M18, P1-M19 | 多重性補正済み片側Wilson上限 U(size) ≤ 0.07（2ポイントの工学許容） |
| AC-T02 | P1-M18, P1-M19 | 候補多重性補正済み片側Wilson下限 L(power) ≥ 0.80。ただし真の対立強度、n、null式、CI/testが既に固定され計算予算が成立するケースのみ |
| AC-T03 | P1-M18, P1-M19 | null非棄却から無交絡の証明を出力するケース 0件。NCO非特異性の負例を必須 |
| AC-T04 | SR04:X-09、NEG-005/007/008/009/011/022/023/024（stress報告） / RULE_BOUND_DRAFT | バイアス、誤被覆、警告を定量記録。exclusion等の隠れた違反を自動検出するpower閾値は設定しない |
| AC-T05 | SR04:X-09、P1-M13〜17/M20（検定対象外の定義） / RULE_BOUND_DRAFT | 単なるSubset安定性、Random CC、Graph fidelity、Sensitivity数値式には無理に検定sizeを追加しない |
| AC-P01 | P1-M07, P1-M08, P1-M09, P1-M10, P1-M11, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08, P3-M04, P3-M05, P3-M06, P3-M07, P3-M08, P3-M09, P3-M10, P3-M11, P3-M12, P3-M13 | \bias_hat=(1/R_est)Σ(θhat_r−θ_true)\、\MCSE_bias=sd(θhat_r−θ_true)/sqrt(R_est)\。regular well-specified DGPの提案: \ |
| AC-P02 | AC-P01を適用するすべてのMethod（scale補助条件） / RULE_BOUND_DRAFT | \s_0=SD[Y(0)]\ または同等のDGP指定固定母集団尺度を事前選択し、未定義/ゼロなら別の物理単位・臨床/事業許容誤差を事前登録。標本実測値に適応して閾値を変えない |
| AC-P03 | P1-M07, P1-M08, P1-M09, P1-M10, P1-M11, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08, P3-M04, P3-M05, P3-M06, P3-M07, P3-M08, P3-M09, P3-M10, P3-M11, P3-M12, P3-M13 | \sqrt(mean[(θhat_r−θ_true)^2])\ とそのMonte Carlo SE（squared-errorのvariance・delta method/paired independent bootstrap）を報告。regular wel |
| AC-P04 | AC-P01を適用するすべてのMethod（Estimand・support制約） / RULE_BOUND_DRAFT | CATE fixed x、ATT(g,t)、RD cutoff、IV structural coefficientなど正しいestimandごとに別評価。extrapolation/positivity構造違反下のBias/RMSEは科学stressでありP0 |
| AC-P05 | P1-M08, P1-M09, P1-M10, P1-M11, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08, P3-M09, P3-M10, P3-M11 | well-specified regular caseに限り点推定非有限/計算失敗率のWilson上限 ≤0.01を提案。方法別最小sample/supportを固定すること |
| AC-P06 | SR04:X-04、P2-M01〜08／point+confirmatory分離 / RULE_BOUND_DRAFT | Exploratoryでpoint-only可でもP01/P03の適格な精度検証は省略しない。ConfirmatoryはAC-Iも必須 |
| AC-G01 | P1-M06, P3-M01, P3-M02, P3-M03 | known ground-truth edge type、lag、circle/arrow/tail、GraphVersion hashのlossless保存 100%（AC-D02/05と同一） |
| AC-G02 | P1-M06, P3-M01, P3-M02, P3-M03 | DGP指定のvalid nullでAC-T01を適用。serial dependence/conditional independenceの前提を別保持 |
| AC-G03 | P1-M06, P3-M01, P3-M02, P3-M03 | DGP・n/T・alpha・CI test・Graph oracleが承認された正例に限る暫定候補：strong-signal DGPでreplicate平均precision/recallの多重性補正済み下限が各≥0.80、FPRの上限が≤0.10。区間はr |
| AC-G04 | P1-M06, P3-M02, P3-M03 | Oracle強制端点のみで方向正解率を評価。未決のorientationの真DAG方向と一致させるHard Gateは禁止。Endpoint候補≥0.80はGraph oracle導出後にのみ審査 |
| AC-G05 | P3-M01 | edgeごとの数を独立repetitionとみなさず、DGP replicate単位で精度のMC intervalを作る。Graph metricの分母zero規則を固定 |
| AC-G06 | P1-M06, P3-M02, P3-M03 | DGP-011等で独立PAG導出がない場合、scientific orientation判定はBLOCKED。契約上のendpoint忠実性のみ評価可能 |
| AC-Q01 | P3-M04, P3-M05 | 群別差・ATT(g,t)・event-time weightsのexact sample/oracle parity D03。Bias/RMSEは各正しいtargetでP01/P03 条件付き |
| AC-Q02 | P3-M06 | level=2、slope=.1などの母集団真値に対するP01/P03候補。serial errorでiid CI/SEをvalid扱い 0件。HAC/GLSの採否・coverageはPENDING |
| AC-Q03 | P3-M07, P3-M08 | cutoffの片側極限／局所jump／局所WaldのD03真値一致（数式Reference）。bandwidth/local SE/weak local first-stage coverageはPENDING |
| AC-Q04 | P3-M12 | DGP-017 noiselessでpost counterfactual誤差≤D03、donor weights=(.6,.4)は独立rank・一意解が確定した時のみD03。noise付きはP01/P03 条件付き |
| AC-Q05 | P3-M13 | DGP-018 ATT=2の既知真値／unit-time weightとobjective valueを独立Referenceに照合。Method-specific optimization tolerance・SE/coverageはPENDING |
| AC-R01 | P1-M12 | 事前指定したnull/testがある時のみT01、十分な対立の強度を設定した時のみT02 |
| AC-R02 | P1-M13, P1-M14, P1-M15, P1-M16 | seed/transform/resample parity D03、sample/cluster unit一致D01/D07、refutation変動率はreport-only（恣意的な「元効果との差5%以内」等は設けない） |
| AC-R03 | P1-M18, P1-M19 | opt-in、conditioningとnullの妥当性が承認された時のみT01/02＋typed rejection。Method Scope未決 |
| AC-R04 | P1-M20 | DGP-020既知OVB bias=0.2581988897…にD03のfloat tolerance、R² domain/status D01。RV値は独立数式Oracleと一緒にfreezeするまでBLOCKED |
| AC-R05 | P1-M10, P1-M17 | 既知PSのweight、ESS=(Σw)^2/Σw²、clip/trim sampleのreference parity D03。科学的なbias/target変化は報告、改善保証をHard Gateにしない |

| ENV-AC | Environment要件 | SR04横断の参照 | Evidence |
|---|---|---|---|
| ENV-AC01 | Runtime/Architecture | SR04:X-01, SR04:X-07 | NOT_GENERATED |
| ENV-AC02 | Lock/SBOM/Extras | SR04:X-07 | NOT_GENERATED |
| ENV-AC03 | Backend isolation | SR04:X-02, SR04:X-07 | NOT_GENERATED |
| ENV-AC04 | RNG and splits | SR04:X-03, SR04:X-05 | NOT_GENERATED |
| ENV-AC05 | Parallel numerical reproducibility | SR04:X-05 | NOT_GENERATED |
| ENV-AC06 | Budget/retry/fail denominator | SR04:X-04, SR04:X-09 | NOT_GENERATED |
| ENV-AC07 | Manifest/lineage/artifact | SR04:X-01, SR04:X-02, SR04:X-03, SR04:X-04, SR04:X-05, SR04:X-06, SR04:X-08, SR04:X-09 | NOT_GENERATED |
| ENV-AC08 | Privacy / legacy | SR04:X-01, SR04:X-06, SR04:X-08, SR04:X-09 | NOT_GENERATED |
| ENV-AC09 | GPL/customer delivery | SR04:X-07 | NOT_GENERATED |


### 6.1. 11件の横断ACの統合レビュー再バインド（2026-11-16）

上の45件のうちMethod表に直接割り当てられていなかった11件を、**SR04横断契約・Method群・Negative Case・既存ACの適用条件**へ明示的に再バインドした。**Method単位のDirect RuleとCross/Conditional/Report-only Ruleを同一視せず**、各適用セルで`applies_if`・`required_evidence`・`not_applicable_reason`・`rule_version`を保持する。

| AC | 種別・責務 | 正本への意味 |
|---|---|---|
| AC-D04/D05/D06 | CROSS_CONTRACT：schema/hash、Graph/AR set/readback、RNG/replay | SR04:X-01/03/04/05/06/07へ接続。0件の契約違反はImplementation Gateで確認 |
| GROUP-AC-I04 | REPORT_ONLY：CI幅やAR集合informativeness | 強IV等でuninformativeな区間を記録。幅に普遍的Hard Gateを設定しない |
| AC-I05/I06 | CONDITIONAL_INFERENCE：Method-specific推論構成／CI unavailable | 確認的MethodのCI科学妥当性とexploratory point-onlyを区別 |
| AC-T04/T05 | STRESS/NOT_APPLICABLE：識別違反・refutation時の誤用回避 | Hidden invalid IV検出の偽保証をしない |
| AC-P02/P04 | CONDITION_OF_P01：効果尺度・target・支持域 | P01の数値判定に対する前提制約。独立な追加閾値として二重計上しない |
| GROUP-AC-P06 | CONDITIONAL_MODE：exploratory/confirmatory | SR03-D05 Owner採用のモード別意味を保持 |

**ステータス:** 上記の参照漏れ（単純なID欠落）は`RULE_BOUND_DRAFT`として解消した。ただしformal Method config、閾値採用、Evaluation Cell、正式Gate Evidenceは依然OPEN。

## 7. E11-REQ仮IDと正本要件/Gateへの引渡し

03のE11-REQ-*は計画上の仮識別子であり、正式FR/NFR/AR番号ではない。05の旧AC-01〜12案はSR04-Dの45件（AC-D01等）と別体系。正式Gate07 Evidenceも未採番・未生成。

| E11-REQ仮ID | 現行要件・差分出典（03） | PLAN Gate | Method直接参照（代表） | Approval |
|---|---|---|---|---|
| E11-REQ-P1Q | FR-040/041はQuestion/Designを固定。FR-054・NFR-002のlineageはPARTIAL | PLAN:G01/G02 | 横断契約 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P1I | FR-042/043/046、AR-005/023はRandomized/BackdoorのIdentification | PLAN:G02 | P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M07 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P1G | FR-035/037は複数Discovery・Graph endpointを要求 | PLAN:G01 | P1-M06 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P1R | FR-049はPlaceboとData Subset | PLAN:G03 | P1-M12, P1-M13, P1-M14, P1-M15 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P1S | FR-050はAdjustment Set・Clipping | PLAN:G03 | P1-M16, P1-M17, P1-M20 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P1NC | 現行FR-049のRefutationはPlacebo・Data Subset。A0/A1にNegative Controlの追加要求あり | PLAN:G03:05追補待ち | P1-M18, P1-M19 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P1W | FR-047/048はATE/ATTと適用可能な診断。IPW実装済み | PLAN:G03 | P1-M08, P1-M09, P1-M10, P1-M11 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P2 | 現行FRにCATE/HTE・EconMLの第一級推定要件なし | PLAN:G04 | P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-SR03D05 | 現行v2 EffectResultは非IV CATE／DRIV向けのMethod別CI検証と科学的推論可用性を一級には規定しない。EconML 0.17のAPI smokeは有限CIを一部設定で取得したが被覆率は未実証 | PLAN:G04/G05/G10 | P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P2A | CATEファイル成果物の現行要件なし | PLAN:G05 | 横断契約 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P3T | 時系列Graph/Discovery専用FRなし | PLAN:G06 | P3-M01, P3-M02, P3-M03 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P3D | DiD/Event Study/ITS専用FRなし | PLAN:G07 | P3-M04, P3-M05, P3-M06 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P3I | 既存のRandomized/Backdoorは準実験IVやRDDではない | PLAN:G08 | P3-M07, P3-M08, P3-M09, P3-M10, P3-M11 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-P3S | Synthetic Control/SDID専用FRなし | PLAN:G09 | P3-M12, P3-M13 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-SR03D06 | 現行Native IdentificationはCPDAG/PAGでREQUIRES_REVIEWを返し、方向不確定を保持する。GraphVersionは親子・origin・edit_rationaleを持つが、一般化識別や部分識別エンジンは未実装 | PLAN:G01/G02/G10 | P1-M06 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-SR03 | 現行SpecはATE/ATT・RANDOMIZED/BACKDOORのみ。Estimation CLIは識別REQUIRES_REVIEWを受け入れる経路を持つ | PLAN:G02/G04/G08/G10 | P1-M06, P2-M01, P2-M02, P2-M03, P2-M04, P2-M05, P2-M06, P2-M07, P2-M08 | DRAFT / FR-NFR-AR未承認 |
| E11-REQ-CLI | NFR-001b/002はPARTIAL、NFR-025/028は既存範囲でIMPLEMENTED | PLAN:G10 | 横断契約 | DRAFT / FR-NFR-AR未承認 |

## 8. Gate07 Evidence Bundle（未生成の仕様案）

1評価セルはMethod ID、SCOPE ID、正式Estimand/contrast、DGP variant、n/T/R/K、inference mode、Environment、RNG streamを一意に固定する。以下はファイルの作成済み宣言ではない。

| Evidence分類 | 必要な証拠 |
|---|---|
| Authority | 承認済みScope処遇、FR/NFR/AR、ADR、正式GateとIssue、Ownerの署名と固定commit |
| Scientific | 独立Reference truth/導出、Graph/Design識別仮定、DGP・NEGと適用条件 |
| Config | Reference/generator/backend/source SHA、Python/OS/dependency lock、data/Graph/Question hash、seed/split/parallel |
| Quantitative | Rule/threshold version、sample n/T/R、familywise K、bias/RMSE/coverage/size/Graph metrics、MCSE、失敗分母 |
| Typed result | point/inference/science/technical status、AR集合と通常CIの分離、PAG endpoint、reasons/negative |
| Repro/Legal | manifest readback/atomic write/checksum、旧Product/v2回帰、個票privacy、顧客SI GPL確認 |
| Review | 独立Science Review/失敗・修正履歴、正式Gate07承認者・日時・SHA |

**証拠ファイルの候補配置:** evidence/sr04/<campaign>/<method>/<cell>/<replicate>/... は設計上の命名例であり実在pathではない。SR-02 ActionsによるAPI smokeは環境導入可能性だけを支持し、科学的Known-truth・95%CI coverage・PAG oracleの実証ではない。

### 8.1. B1-A／DRIV-A正式判断とGate evidenceの非同一性

- `P3-M11`: **Owner semantic decision closed**。正式科学Target=`LINEAR_IV_STRUCTURAL_COEFFICIENT`（加法線形β）。残余は`REF-E08/U01`、均質性stress、schema/HC AR/coverage、Issue #22・PLAN:G08の科学Evidence。
- `P2-M08`: **Owner semantic decision closed**。family=`IV_HETEROGENEOUS_EFFECT`、target=`CONDITIONAL_IV_STRUCTURAL_SLOPE`、X/W残差化IV moment。`W=∅`のDGP-008ではx=-1,+1。残余は`REF-E06`、0.17.0 runtime/projection/nuisance/CI、Issue #18・PLAN:G04の科学Evidence。
- 構造方程式・数値Referenceは独立技術記録へ、正式採用の事実は02へ一元化する。**元の`METHOD_SPEC_PENDING`等の古い文書内表示は、Owner意味論だけ2026-11-16判断で上書きされた**ことを示し、正式Gate ACCEPTEDにはしない。

### 8.2. FD-A／GRAPH-A採用後のMethod別残務

| Method／Owner判断 | 決定済み範囲 | 未実行の必須検証 |
|---|---|---|
| P1-M07／DEC-SR04-03 FD-A | P1-M04のFrontdoor識別を前提とする線形単一Mediatorの二段階係数積。Stage1 M~1+A、Stage2 Y~1+M+A | REF-I02/E04の独立sample Oracle、DoWhy 0.14実効stage調整、DGP-005/NEG-004/005、CI/coverage |
| P1-M06／DEC-SR04-04 GRAPH-A | 生成DAGと観測同値類PAGを区別する独立Oracleの原理 | 独立MAG/PAG/CI oracle・多変数motif、DGP-011はlatent stress |
| P3-M01〜03／DEC-SR04-04 GRAPH-A | temporal lag + contemporaneous CPDAG/PAGの強制方向を区別する原理 | REF-G02/G03、DGP-009〜011のGraph CI test/独立同値類/精度、Tigramite version |
 
**上記のOwner決定は、科学的Accuracy・有限標本CI・正式Source SHA受入・Architecture/Legal GateをPASSにしない。**

### 8.3. DEC-05 Method別のGate evidence引渡し

| DEC ID / Method | Owner採用Estimator | Inference初期扱い | 残余Evidence |
|---|---|---|---|
| DEC-05-1 / P3-M04 | 2×2 ATT・単位変化の群差 | 独立unit clusterに適格なSE | REF-Q01、DGP-012、NEG-022、SE/coverage |
| DEC-05-2 / P3-M05 | never-treated基準のATT(g,t)→cohort重みのevent-time集約 | cohort-stratified unit trajectory bootstrap候補 | REF-Q01、DGP-013、TWFE汚染・pointwise/joint CI |
| DEC-05-3 / P3-M06 | segmented regression：level/slope+seasonality | HAC（適格なT/lag/serial model条件付き） | REF-Q02、DGP-014、HAC/GLS coverage |
| DEC-05-4 / P3-M07 | Sharp RD local-linear p=1 triangular kernel | q=2 robust bias-corrected CI候補 | REF-Q03、DGP-015、bandwidth/rdrobust optional/license |
| DEC-05-5 / P3-M08 | Fuzzy RD cutoff jump ratio | joint local RBC、weak first-stageでfail-closed | REF-Q03/I03、DGP-016、弱局所IV stress |
| DEC-05-6 / P3-M12 | SCM simplex donor weights/post treated gap | **EXPLORATORY_POINT_ONLY**、Placebo/RMSPEは診断 | REF-Q04、DGP-017、donor rank/uniqueness |
| DEC-05-7 / P3-M13 | SDID unit/time weights別最適化のweighted DID | unit cluster bootstrap／毎replicate weights再推定 | REF-Q05、DGP-018、solver/few-treated/coverage |

全7件で`OWNER_BASELINE_ACCEPTED / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN`。METHODのOwner方針採用はAC-Q01〜05の数値基準の承認ではない。

### 8.4. DEC06 Owner採用後の科学的未完事項

| Method | Owner採用済み科学的Scope | Science/Gate未完 |
|---|---|---|
| DEC06:NCE (P1-M18) | Observed NCE、明示opt-in・null/conditioning、条件付き係数の診断 | DGP-019 null/alternativeの独立妥当性、REF-R02、AC-T01/T02/T03、CI有効性 |
| DEC06:NCO (P1-M19) | Observed NCO、A→W causal nullに加えて統計的conditional nullを個別に審査 | DGP-019でγ=0でもU→A,WによりW~Aが関連しうるNEG-026。Null size/power/REF-R02 |
| DEC06:OLS-RV (P1-M20) | 古典OLS partial R²（2軸grid）・q=1点RV。HC3とは科学的に別診断 | DGP-020のOVB algebra、REF-R03/RV数値・AC-R04、OLS design hash/df/SE |

**この3件のOwner判断は完了したが、Runtime・科学的Inference・Formal FR/ADR/Gateは未完了。**

### 8.5. DEC07 Quantitative/Resource Pre-freeze追加依存

- 判定ファミリー候補：全mandatory stochastic comparisonsについてGate-wide FWER=0.05、片側Wilson/Method適格なContinuous interval。**実Kは未計数**。固定Sample exact／Losslessは別Hard契約。
- R=6000はp=.95のMCSE≈.002814を満たすだけ。K=1024（説明例）、failure実測0.005、R6000の補正Wilson上限は.01000657で閾値.01に満たない。
- Pilotは100〜200repからMethod/n/T/inner-bootstrapごとに実測する案。pilot未実施・T3 R/CPU/Wall/RAM/Money上限未確定。
- `DEC07-1〜7`の7判断は[Owner採用済み独立技術記録](20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)にA/B/C比較と数値成立性を保持し、**02第24項でA×7のOwner採用を記録済み**。一方、**実K/R/inner-bootstrap/Cost・Cell SHAの数値凍結とScience/Gate PASSは未実施**。

### 8.6. DEC07採用を数値Freezeと混同しないためのGate区分

- **Owner decision（CLOSED）:** DEC07-1〜7全A／AC分類・FWER/K設計・Method別R・独立Pilot・実測Budget審査・seed・Gate分離。
- **Quant/Resource pre-freeze（OPEN）:** 45 ACのMethod別Hard適用とmandatoryセル列挙、実効K、R・Bootstrap・n/T・Seed/Source/REF SHA、実測CPU/Wall/RAM・承認Spend cap。
- **Independent science（NOT_RUN）:** DGP/Reference・Backend推論適格性、Monte Carlo、Graph/AR・旧v2回帰、独立Reviewerと正式Gate判断。
- **Fail-closed:** K/R/費用未確定やOracle未構築のまま、Owner方針採用を`SCIENCE_PASS`、`QUANT_FROZEN`または`GATE07_ACCEPTED`にしない。

### 8.7. DEC08 profile/lock/Legal未決・Evidence義務

- **ENV-AC01〜03:** platform/Python/CPU Profile、既存5＋RD追加候補、extrasとuniversal-resolutionの実効互換性、fresh venvでの`uv lock --check`/`uv sync --locked`/`uv pip check`、Method API・既存v2/E9回帰。**E11 Extraおよびlock未実装、Evidence NOT_GENERATED**。
- **ENV-AC04〜08:** RNG/BLAS/CPU/Manifest/SBOM/source hash/個票・旧v2契約。uv.lockのpinと実行・科学的再現性を同値にしない。
- **ENV-AC09:** Tigramite GPLv3-or-later、rdrobust GPL-3.0-onlyに関する個別SI顧客納入のLegal/配布/結合/Source義務とArtifact SHA。**未法務承認ならDelivery BLOCKED**。Internal Science適格性と別状態。
- **Owner判断:** [DEC08独立提案](20261116_sr04_dec08_backend_optional_dependency_lock_license_owner_decision_proposal.md)のDEC08-1〜8全Aは審議案であり**正式採用前**。**ENV LOCK/SCIENCE/GATEは未freeze、対象Method41/Scope68/NEG28/DGP24/REF24/AC45/ENV-AC9/X9のレジストリ数を変えない**。

## 9. 残余Blocker・閉鎖条件・状態

| Status candidate | 意味 |
|---|---|
| TRACE_DRAFT | ID接続の設計のみ。Science PASSやCoding許可ではない |
| SCIENCE_CONTRACT_BLOCKED | B1-A/DRIV-A/FD-A/GRAPH-AのOwner意味論・Method方針は採用済み。ただしBackend実効Inference・独立PAG/CPDAG oracleとQuasi個別推論は未完 |
| SCOPE_APPROVAL_BLOCKED | 68 Scope・NCE/NCO/RV・GAP-C01〜04・FR/NFR/AR/Architecture未承認 |
| REFERENCE_ENV_BLOCKED | Oracle、数値閾値、dependency lock、seed/replay、n/R/K、資源/License未freeze |
| EXECUTED_NOT_REVIEWED | 実測があっても独立ReviewとOwner Gateの承認待ち |
| GATE_ACCEPTED | 承認済み科学契約、実測、独立Review、Owner正式Gateがそろったときのみ |

### 9.1. Blockerから正式Gateへの順序

1. SR03-R01 B1のformal estimand、SR03-R02 DRIVのconditional IV moment/射影を確定する。
2. Frontdoor数値、FCI/LPCMCIの独立Graph oracle、DiD/Event/ITS/RDD/SCM/SDIDのMethod別推論を確定する。
3. SR-01〜12を再審査し、68 Scope行・A0例外・NCE/NCO/RVとProduct Gap帰属をOwnerが項目別承認する。
4. 03/04/05の仮RequirementとPLAN:G01〜G10を正式FR/NFR/AR・ADR・Gate07責務へ結合する。
5. Reference/AC/Environment/lock・RNG/seed/n/R/K/計算予算・候補SHAを事前freezeし、承認されたCoding工程で実装/Science試験を行う。
6. 正例・負例・旧v2回帰・推論・Graph/再現性を独立レビューし、正式Gate07を判定する。

**現時点:** TRACE_DRAFT / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN / PENDING_FULL_CONCEPT_APPROVAL。今回変更するのはこのworking_notesのみ。コード、要件正本、Gate、Notion、Work Package、依存lockは変更しない。
