# RD-03 — ENH-E11正式要件発行・68 Scope／41 Method／10 UC監査

**Date:** 2026-11-16. **Decision:** DEC09; blob `64127cf02c72325f93685a383b44f0e38a580b8f`. **Method trace input:** SR04-F `43baa1e6fbf7336b5b10344b30ca1b89a50ae8d9`.  
**Status:** `FORMAL_RD_CLAUSES_ISSUED_IN_REVISED_COPY / OWNER_SHA_REVIEW_PENDING / SCIENCE_NOT_RUN / GATE06_07_NOT_FROZEN / CODING_NOT_AUTHORIZED`.

## 1. 発行境界

- 正式発行条文：FR-185〜203（19件）、NFR-029〜036（8件）、科学的AR-028〜044（17件）。各件`MUST / ACTIVE / UNVERIFIED / ENH-E11`。
- 元の195 FR／36 NFR／27 ARのID・原文・Statusを改変しない。E11-Aの7件はArchitecture要求草案でありScientific ARと混同しない。
- DEC09は要件の意味とScopeを承認した。**実装充足・独立科学受入・Legal Gate・Owner SHA最終確認は未完**。GitHub改訂版への発行と旧canonicalへの昇格は別。
- R/Q/N/DのDispositionを尊重。D-only ScopeにはE11初期実装義務なし。Dを含む混合Scopeでは承認されたLocal部分のみ要件化する。

## 2. 旧E11草案からの正式ID crosswalk（27）

| Draft ID | Formal ID | Level | Requirement status | Implementation status | Delivery |
| --- | --- | --- | --- | --- | --- |
| E11-F-01 | FR-185 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-02 | FR-186 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-03 | FR-187 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-04 | FR-188 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-05 | FR-189 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-06 | FR-190 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-07 | FR-191 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-08 | FR-192 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-09 | FR-193 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-10 | FR-194 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-11 | FR-195 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-12 | FR-196 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-13 | FR-197 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-14 | FR-198 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-15 | FR-199 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-16 | FR-200 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-17 | FR-201 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-18 | FR-202 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-F-19 | FR-203 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-01 | NFR-029 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-02 | NFR-030 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-03 | NFR-031 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-04 | NFR-032 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-05 | NFR-033 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-06 | NFR-034 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-07 | NFR-035 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| E11-N-08 | NFR-036 | MUST | ACTIVE | UNVERIFIED | ENH-E11 |


## 3. DEC09付録Aの全68 Scope行

| Scope ID | DEC09 Approved Disposition | Formal/legacy requirements | Method IDs | Issue | Boundary |
| --- | --- | --- | --- | --- | --- |
| P1-01 | **R** | FR-185 / FR-040 | — | #15 | R/Q/N as approved |
| P1-02 | **R+N／D** | FR-185 | — | #15,#24 | R/Q/N as approved |
| P1-03 | **R+N** | FR-187 / FR-041 | — | #15 | R/Q/N as approved |
| P1-04 | **R** | FR-186 / FR-037 | — | #17 | R/Q/N as approved |
| P1-05 | **R／D** | FR-186 / FR-039 | — | #17 | R/Q/N as approved |
| P1-06 | **R** | FR-187 / FR-042 | P1-M01, P1-M02 | #15,#16 | R/Q/N as approved |
| P1-07 | **R** | FR-187 / FR-036 | P1-M02 | #15 | R/Q/N as approved |
| P1-08 | **N（Frontdoor数値推定をPhase1に含む方針採用）** | FR-187 / FR-188 / AR-030 | P1-M03, P1-M04, P1-M05, P1-M07 | #16 | R/Q/N as approved |
| P1-09 | **N** | FR-186 / AR-028 | P1-M06 | #17 | R/Q/N as approved |
| P1-10 | **R+N** | FR-187 / FR-044 | — | #15,#16 | R/Q/N as approved |
| P1-11 | **R** | FR-192 / FR-047 | P1-M08, P1-M09, P1-M10, P1-M11 | #19 | R/Q/N as approved |
| P1-12 | **R+Q** | FR-192 / FR-048 | P1-M10, P1-M11 | #19 | R/Q/N as approved |
| P1-13 | **R** | FR-189 / FR-049 | P1-M12, P1-M13 | #16 | R/Q/N as approved |
| P1-14 | **N** | FR-189 | P1-M14, P1-M15 | #16 | R/Q/N as approved |
| P1-15 | **N（NCE/NCO各1Method、DEC06-1/2 Owner個別採用）** | FR-190 / AR-031 | P1-M18, P1-M19 | #16 | R/Q/N as approved |
| P1-16 | **R** | FR-189 / FR-050 | P1-M16, P1-M17 | #16 | R/Q/N as approved |
| P1-17 | **N（OLS partial R²/point RV個別採用）／D（広範Sensitivity）** | FR-191 / AR-032 | P1-M09, P1-M20 | #16 | R/Q/N as approved |
| P1-18 | **R+N／D** | FR-201 / NFR-029 | — | #15,#24,#14 | R/Q/N as approved |
| P1-19 | **D** | SCOPE_D_ONLY | — | #14 | D-only, no E11 initial capability |
| P1-20 | **R+N** | FR-201 | — | #16,#24 | R/Q/N as approved |
| P1-21 | **R+N** | NFR-035 / AR-044 | — | #16,#17,#24 | R/Q/N as approved |
| P2-01 | **N** | FR-193 / AR-034 | — | #18 | R/Q/N as approved |
| P2-02 | **N** | FR-193 | P2-M01 | #18 | R/Q/N as approved |
| P2-03 | **N** | FR-193 | P2-M02 | #18 | R/Q/N as approved |
| P2-04 | **N** | FR-193 | P2-M03 | #18 | R/Q/N as approved |
| P2-05 | **N** | FR-193 | P2-M04 | #18 | R/Q/N as approved |
| P2-06 | **N** | FR-193 | P2-M05 | #18 | R/Q/N as approved |
| P2-07 | **N** | FR-193 | P2-M06 | #18 | R/Q/N as approved |
| P2-08 | **N** | FR-193 | P2-M07 | #18 | R/Q/N as approved |
| P2-09 | **N** | FR-194 / AR-034 | P2-M08 | #18,#22 | R/Q/N as approved |
| P2-10 | **N** | FR-193 / FR-202 | — | #18 | R/Q/N as approved |
| P2-11 | **R+N** | NFR-032 / NFR-033 | — | #18,#24 | R/Q/N as approved |
| P2-12 | **R+N** | FR-193 / NFR-029 | — | #18,#24 | R/Q/N as approved |
| P2-13 | **R+N** | FR-193 / AR-034 | — | #18 | R/Q/N as approved |
| P2-14 | **N** | FR-193 / AR-035 | — | #18 | R/Q/N as approved |
| P2-15 | **N** | FR-195 / NFR-031 | — | #18,#24 | R/Q/N as approved |
| P2-16 | **N** | NFR-035 / AR-044 | — | #18,#24 | R/Q/N as approved |
| P2-17 | **N** | FR-193 / FR-194 | — | #18 | R/Q/N as approved |
| P2-18 | **D／N** | FR-195 / SCOPE_D_PRODUCT | — | #18,#24 | D portion excluded |
| P3-01 | **N** | FR-196 | — | #20 | R/Q/N as approved |
| P3-02 | **N** | FR-196 | P3-M01 | #20 | R/Q/N as approved |
| P3-03 | **N** | FR-196 | P3-M02 | #20 | R/Q/N as approved |
| P3-04 | **N** | FR-196 | P3-M03 | #20 | R/Q/N as approved |
| P3-05 | **R+N** | FR-196 | — | #20 | R/Q/N as approved |
| P3-06 | **N** | FR-196 / AR-036 | — | #20 | R/Q/N as approved |
| P3-07 | **N** | FR-197 / AR-037 | P3-M04 | #21 | R/Q/N as approved |
| P3-08 | **N** | FR-197 / AR-037 | P3-M05 | #21 | R/Q/N as approved |
| P3-09 | **N** | FR-197 / AR-037 | P3-M06 | #21 | R/Q/N as approved |
| P3-10 | **N** | FR-198 / AR-038 | P3-M07 | #22 | R/Q/N as approved |
| P3-11 | **N** | FR-198 / AR-038 | P3-M08 | #22 | R/Q/N as approved |
| P3-12 | **N（初期推定器A＋Bをオーナー採用）** | FR-199 / AR-039 / AR-040 | P3-M09, P3-M10, P3-M11 | #22 | R/Q/N as approved |
| P3-13 | **N** | FR-200 / AR-041 | P3-M12 | #23 | R/Q/N as approved |
| P3-14 | **N** | FR-200 / AR-041 | P3-M13 | #23 | R/Q/N as approved |
| P3-15 | **N** | FR-197 / FR-198 / FR-199 / FR-200 | — | #21,#22,#23 | R/Q/N as approved |
| P3-16 | **N** | NFR-035 / AR-044 | — | #20,#21,#22,#23,#24 | R/Q/N as approved |
| P3-17 | **R+N** | FR-201 / NFR-029 | — | #20,#24 | R/Q/N as approved |
| P3-18 | **D** | SCOPE_D_ONLY | — | #20 | D-only, no E11 initial capability |
| P3-19 | **D／N** | FR-201 / SCOPE_D_PRODUCT | — | #21,#22,#23,#24 | D portion excluded |
| X-01 | **D／OWNER_APPROVED** — ATCを後続審議へ | SCOPE_D_ONLY | — | #14 | D-only, no E11 initial capability |
| X-02 | **D** | SCOPE_D_ONLY | — | #14 | D-only, no E11 initial capability |
| X-03 | **D／OWNER_APPROVED** — matching/g-computationを後続審議へ | SCOPE_D_ONLY | — | #14 | D-only, no E11 initial capability |
| X-04 | **N(partial)+D／OWNER_APPROVED** — Observed NCE/NCO、追加A0はD | FR-190 / SCOPE_D_REMAINDER | P1-M18, P1-M19 | #16,#14 | D portion excluded |
| X-05 | **N(partial)+D／OWNER_APPROVED** — classic OLS partial R²/RV、一般化D | FR-191 / SCOPE_D_REMAINDER | P1-M20 | #16,#14 | D portion excluded |
| X-06 | **Q一部／D** | NFR-035 / SCOPE_D_REMAINDER | — | #19,#20,#21,#24 | D portion excluded |
| X-07 | **D** | SCOPE_D_ONLY | — | #14 | D-only, no E11 initial capability |
| X-08 | **D** | SCOPE_D_ONLY | — | #14 | D-only, no E11 initial capability |
| X-09 | **R+N(local)/D(Product)** — Product GAP-C01〜04を後続管理 | FR-201 / SCOPE_D_PRODUCT | — | #14,#24 | D portion excluded |
| X-10 | **R+N(local)/D(Product)** — 新Product統合は後続 | FR-201 / FR-203 / SCOPE_D_PRODUCT | — | #14,#24 | D portion excluded |


## 4. SR04-F Method全41行（Method固有の意味は別契約）

| Method ID | Method / Estimand | Scope | Formal FR | Scientific AR | Environment | DGP/NEG | Independent REF | AC draft | PLAN / Evidence NOT_GENERATED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1-M01 | Native Randomized identification／A | SCOPE:P1-06 | FR-187 | AR-029 | ENV-BASE | DGP-001; NEG-001, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M02 | Native Backdoor identification／ATE | SCOPE:P1-06, SCOPE:P1-07 | FR-187 | AR-029 | ENV-BASE | DGP-002, DGP-021; NEG-002, NEG-003 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M03 | DoWhy Backdoor identification／ATE候 | SCOPE:P1-08 | FR-187 | AR-029 | ENV-DOWHY | DGP-002, DGP-021; NEG-002, NEG-027 | REF-G01, REF-I01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M04 | DoWhy Frontdoor identification／ATE | SCOPE:P1-08 | FR-187 | AR-029 | ENV-DOWHY | DGP-005; NEG-004 | REF-G01, REF-I02 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M05 | DoWhy IV identification／方法固有の対象は未確 | SCOPE:P1-08 | FR-187 | AR-029 | ENV-DOWHY | DGP-006; NEG-006, NEG-007 | REF-I03, REF-G01 | AC-D01, AC-D02, AC-D07 | PLAN:G02 / BLOCKED / NOT_GENERATED |
| P1-M06 | FCI／PAGと等価類 | SCOPE:P1-09 | FR-186 | AR-028 | ENV-BASE | DGP-011, DGP-021; NEG-003, NEG-021, NEG-028 | REF-G02 | AC-D02, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G01 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| P1-M07 | Frontdoor two-stage regression／ATE | SCOPE:P1-08 | FR-188 | AR-030 | ENV-DOWHY | DGP-005; NEG-004, NEG-005 | REF-I02, REF-E04 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02 | PLAN:G02 / OWNER_METHOD_ACCEPTED_TECH_AND_SCIENCE_BLOCKED / NOT_GENERATED |
| P1-M08 | Native diff-in-means／ATE | SCOPE:P1-11 | FR-192 | AR-033 | ENV-BASE | DGP-001, DGP-022; NEG-001, NEG-010 | REF-E01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M09 | Native OLS／採用済み契約範囲のATE/ATT表現 | SCOPE:P1-11, SCOPE:P1-17 | FR-192 | AR-033 | ENV-BASE | DGP-002, DGP-003; NEG-002, NEG-008, NEG-020 | REF-E01, REF-I01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M10 | Native IPW／ATE・ATT（別fixture） | SCOPE:P1-11, SCOPE:P1-12 | FR-192 | AR-033 | ENV-BASE | DGP-002, DGP-003; NEG-010, NEG-018 | REF-E02 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M11 | Native AIPW／ATE・ATT（別fixture） | SCOPE:P1-11, SCOPE:P1-12 | FR-192 | AR-033 | ENV-BASE | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012 | REF-E03 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / BLOCKED / NOT_GENERATED |
| P1-M12 | Placebo Treatment refutation／null診 | SCOPE:P1-13 | FR-189 | AR-044 | ENV-BASE | DGP-022; NEG-014 | REF-R01 | AC-D01, AC-R01, AC-T01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M13 | Data Subset refutation／安定性 | SCOPE:P1-13 | FR-189 | AR-044 | ENV-BASE | DGP-001, DGP-002; NEG-015 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M14 | Random Common Cause refutation／摂動安 | SCOPE:P1-14 | FR-189 | AR-044 | ENV-BASE | DGP-002; NEG-017 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M15 | Bootstrap refutation／再標本化安定性 | SCOPE:P1-14 | FR-189 | AR-044 | ENV-BASE | DGP-001, DGP-002; NEG-016 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M16 | Adjustment Set Sensitivity／設計変更 | SCOPE:P1-16 | FR-189 | AR-044 | ENV-BASE | DGP-021, DGP-002; NEG-002 | REF-G01, REF-R01 | AC-D01, AC-D02, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M17 | Propensity Clipping Sensitivity／tr | SCOPE:P1-16 | FR-189 | AR-044 | ENV-BASE | DGP-002, DGP-023; NEG-010, NEG-018 | REF-E02, REF-R01 | AC-D03, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P1-M18 | Observed NCE null diagnostic／条件付き関 | SCOPE:P1-15, SCOPE:X-04 | FR-190 | AR-031 | ENV-BASE | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P1-M19 | Observed NCO null diagnostic／条件付き関 | SCOPE:P1-15, SCOPE:X-04 | FR-190 | AR-031 | ENV-BASE | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P1-M20 | OLS partial R² / RV sensitivity／指定 | SCOPE:P1-17, SCOPE:X-05 | FR-191 | AR-032 | ENV-BASE | DGP-020; NEG-020 | REF-R03 | AC-D01, AC-D03, AC-R04 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P2-M01 | LinearDML／CATE(x) | SCOPE:P2-02 | FR-193 | AR-034 | ENV-ECONML | DGP-003; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M02 | CausalForestDML／CATE(x) | SCOPE:P2-03 | FR-193 | AR-034 | ENV-ECONML | DGP-004; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M03 | DRLearner／CATE(x) | SCOPE:P2-04 | FR-193 | AR-034 | ENV-ECONML | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M04 | ForestDRLearner／CATE(x) | SCOPE:P2-05 | FR-193 | AR-034 | ENV-ECONML | DGP-004; NEG-010, NEG-011, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M05 | S-Learner／CATE(x) | SCOPE:P2-06 | FR-193 | AR-034 | ENV-ECONML | DGP-002, DGP-003; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M06 | T-Learner／CATE(x) | SCOPE:P2-07 | FR-193 | AR-034 | ENV-ECONML | DGP-003, DGP-004; NEG-010, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M07 | X-Learner／CATE(x) | SCOPE:P2-08 | FR-193 | AR-034 | ENV-ECONML | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P2-M08 | DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE | SCOPE:P2-09 | FR-194 | AR-034 | ENV-ECONML | DGP-008; NEG-009, NEG-012, NEG-013 | REF-E06 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M01 | PCMCI／time-lagged graph | SCOPE:P3-02 | FR-196 | AR-036 | ENV-TIGRAMITE | DGP-009; NEG-021 | REF-G03 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G05 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P3-M02 | PCMCI+／time-series CPDAG | SCOPE:P3-03 | FR-196 | AR-036 | ENV-TIGRAMITE | DGP-009, DGP-010; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| P3-M03 | LPCMCI／time-series PAG | SCOPE:P3-04 | FR-196 | AR-036 | ENV-TIGRAMITE | DGP-011; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| P3-M04 | DiD／ATT（2×2とstaggeredは別契約） | SCOPE:P3-07 | FR-197 | AR-037 | ENV-BASE / backend pending | DGP-012, DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M05 | Event Study／event-time効果 | SCOPE:P3-08 | FR-197 | AR-037 | ENV-BASE / backend pending | DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M06 | Interrupted Time Series／介入時点のlevel | SCOPE:P3-09 | FR-197 | AR-037 | ENV-BASE / backend pending | DGP-014; NEG-023 | REF-Q02 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M07 | Sharp RDD／cutoff局所効果 | SCOPE:P3-10 | FR-198 | AR-038 | ENV-BASE / backend pending | DGP-015; NEG-023 | REF-Q03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M08 | Fuzzy RDD／cutoff局所complier効果 | SCOPE:P3-11 | FR-198 | AR-038 | ENV-BASE / backend pending | DGP-016; NEG-006, NEG-023 | REF-Q03, REF-I03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M09 | Wald ratio／binary Z/A complier LAT | SCOPE:P3-12 | FR-199 | AR-039 | ENV-BASE / backend pending | DGP-006; NEG-006, NEG-007 | REF-I03, REF-E07 | AC-D03, AC-P01, AC-P03, AC-P05, AC-D07 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P3-M10 | B0 just-identified 2SLS／binary Z/A | SCOPE:P3-12 | FR-199 | AR-039 | ENV-BASE / backend pending | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| P3-M11 | B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | SCOPE:P3-12 | FR-199 | AR-039 | ENV-BASE / backend pending | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| P3-M12 | Synthetic Control／処置単位の時点別反実仮想ギャップ | SCOPE:P3-13 | FR-200 | AR-041 | ENV-BASE / backend pending | DGP-017; NEG-024 | REF-Q04 | AC-D03, AC-P01, AC-P03, AC-Q04 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED |
| P3-M13 | Synthetic DiD／panel平均介入効果 | SCOPE:P3-14 | FR-200 | AR-041 | ENV-BASE / backend pending | DGP-018; NEG-024 | REF-Q05 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q05 | PLAN:G09 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |


## 5. Concept UC-01〜10

| UC ID | Goal | Requirement IDs | Evidence |
| --- | --- | --- | --- |
| UC-01 | 潜在交絡が疑われる設備トラブルの因果探索 | FR-186 / FR-187 / AR-028 | Science acceptance not yet run |
| UC-02 | 観察研究で介入効果の識別条件を検討する | FR-187 / FR-188 / AR-029 / AR-030 | Science acceptance not yet run |
| UC-03 | 店舗施策の平均効果を診断付きで評価する | FR-189 / FR-190 / FR-191 / FR-192 / AR-033 | Science acceptance not yet run |
| UC-04 | 顧客属性によって異なる支援施策の効果を調べる | FR-193 / FR-194 / FR-195 / AR-034 / AR-035 | Science acceptance not yet run |
| UC-05 | センサデータの時間lagを考慮した因果探索 | FR-196 / AR-036 | Science acceptance not yet run |
| UC-06 | 段階導入された施策の効果を評価する | FR-197 / AR-037 | Science acceptance not yet run |
| UC-07 | 支援対象の点数閾値を利用して局所効果を推定する | FR-198 / AR-038 | Science acceptance not yet run |
| UC-08 | 奨励の割当をInstrumentとして介入効果を調べる | FR-199 / AR-039 / AR-040 | Science acceptance not yet run |
| UC-09 | 介入地域の反事実を複数地域から構成する | FR-200 / AR-041 | Science acceptance not yet run |
| UC-10 | 第三者が分析結果を再現・監査する | FR-185 / FR-201 / FR-202 / FR-203 / NFR-029 / NFR-030 / NFR-031 / NFR-036 | Science acceptance not yet run |


## 6. Architecture候補 E11-A-01〜07 の移管

| Draft ID | Design destination | Related RD obligations |
| --- | --- | --- |
| E11-A-01 | 22 BD/ADR: Domain authority | FR-187, AR-029 |
| E11-A-02 | 22 BD/ADR: Adapter separation | NFR-032, NFR-033 |
| E11-A-03 | 22 BD/ADR: fail-closed workflow | FR-187, AR-029 |
| E11-A-04 | 21 LDD/22 BD: local vs Product authority | FR-201, FR-203, NFR-036 |
| E11-A-05 | 21 LDD/23 IF: typed results | FR-202, AR-040, AR-042 |
| E11-A-06 | 22 BD/30 DD: profile/lock/SBOM | NFR-029, NFR-033, NFR-034 |
| E11-A-07 | 22 BD/ADR: CLI-only scope | FR-203, NFR-036, 10_90 |


## 7. 新Scientific ARの根拠と法的位置付け

AR-028〜044はDEC09と03_requirements_revision §3の科学的不変条件から導出した要件条文。E11-A番号の再利用ではない。特にFD-Aの単一Mediator/線形、観測NCE/NCO opt-in、OLS partial R²／point RV(q=1)、非IV CATEとDRIV、B0 LATEとB1構造係数、弱IVのAR信頼集合、SCM point-onlyを保持する。科学的方法別の実効APIとCIの妥当性は試験未済。

## 8. 整合性検証

| Test | Result |
|---|---|
| DEC09 Scope行 | 68 unique = P1:21 + P2:18 + P3:19 + X:10 |
| SR04-F Method行 | 41 unique = P1:20 + P2:8 + P3:13 |
| UC | 10 unique |
| Crosswalk | 27 unique old draft IDs mapped to formal ID |
| Scope→Requirement | All 68 rows mapped; all IDs resolve to new or existing requirements |
| Implementation / science / legal | **NOT VERIFIED** |
| Gate06/07 accepted evidence | **NOT GENERATED / NOT FROZEN** |

## 9. Source links

- [DEC09 approval](../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- [SR04-F trace draft](../../working_notes/20261115_sr04_gate07_traceability_draft.md)
- [Concept UC list](../../00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md)
- [RD-01 review](rd01_review/91_rd01_requirement_granularity_review.md)
