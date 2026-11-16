# ENH-E11 — 要件・設計整合性とトレーサビリティ確認（計画案）

**文書区分:** 計画・判断記録  
**状態:** **DEC09_SCOPE_REQUIREMENTS_ARCH_GATE_PLAN_OWNER_APPROVED / DETAILED_TRACE_SNAPSHOT_PENDING / GATE06_07_NOT_FROZEN**  
**前提:** 事前調査`00_01_foundation_gap_reconciliation.md`→`00_02_foundation_gap_closure_assessment.md`→`00_03_phase1_to_phase3_reconciliation.md`と、68行の実装スコープ案`00_04_phase1_to_phase3_cli_scope_proposal.md`を構想・要件・設計策定前に参照する。

> **2026-11-16 DEC-SR04-09正式統合Owner承認追補:** [DEC09独立統合承認記録](../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)と[02承認記録第26項](02_enhancement_concept_approval_record.md)で**Scope68、要件意味差分、Architecture Owner原則、G01〜G10暫定Workstream／受入Gate06/07の計画をOwner採用**。この表の`E11-REQ-*`と`AC-*`は引き続き**正本FR/NFR/AR／Gate07完成版の番号ではない**。正式条文・Schema/ADR・Method別適格性・実効Backend/Lock/法務・Quant K/R/Compute・独立DGP/Ref/Science Reviewのpre-freezeは未完で、実施GateをPASSと誤表示しない。

## 1. 要件→設計→Gate→受入条件→Issueの対応

`E11-REQ-*`と`AC-*`は**計画上の仮識別子**。承認済みFR/NFR/ARや固定済みGate 07を表さない。IssueのcloseはGate PASSではない。

| 要件案・不変条件 | 設計への反映（案） | 暫定Gate | 受入条件（案） | Issue |
|---|---|---|---|---|
| E11-REQ-P1Q；FR-040/041/054、NFR-002 | Versioned local Question/Design/Graph、適格性・lineage | G01/G02 | AC-01 Identity、不正Design拒否 | #15 |
| E11-REQ-P1G；FR-035/037 | FCI registry、PAG CIRCLE、潜在交絡warning | G01 | AC-02 endpoint往復、潜在交絡の既知例 | #17 |
| E11-REQ-P1I；FR-042/046、AR-023 | optional DoWhy、Identificationの分離 | G02 | AC-03 Backdoor/Frontdoor/IVの識別・非識別 | #16 |
| E11-REQ-P1R/P1S；FR-049/050 | Refutation/Sensitivityの方法別Result | G03 | AC-04 既知真値、seed再実行 | #16 |
| E11-REQ-P1W；FR-047/048 | IPW/AIPWの推論、E9 Diagnosticsの再利用 | G03 | AC-05 Effect精度、coverage、overlap/balance/ESS | #19 |
| E11-REQ-SR03（D04-1〜5） | 旧v2保護＋新local version dispatch、normalized IdentificationResult→Method別eligibility gate、hash整合、typed confidence_set、旧REQUIRES_REVIEW/override回帰保護。[D04独立記録](../working_notes/20261115_sr03_d04_identification_estimator_contract_options.md) | G02/G04/G08/G10の候補（未freeze） | D04-T01〜T12：識別→推定の正/負例、legacy read-back、hash mismatch拒否、集合round-trip（検証候補・未実行） | #16,#18,#22,#24 |
| E11-REQ-SR03D05／E11-REQ-P2 | **D05-1〜5のB/B/B/B/B方針採用（2026-11-15）**：非IV CATE7手法とDRIVの別Estimand・EstimatorSpec、Exploratory点推定とConfirmatory推論の区別、Method別Inference registry、point/uncertainty/science status、独立coverage検証。[D05判断詳細](../working_notes/20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md) | G04/G05/G10・Method固有Gate候補（未freeze） | D05-T01〜T13（未実行）：既知真値・pointwise coverage・CI未取得・support/weak IV・pointwiseと同時帯の非同一性、v2回帰 | #18,#22,#24 |
| E11-REQ-SR03D06／E11-REQ-P1G | **D06-1〜6のB/B/B/B/B/A方針採用（2026-11-15）**：CPDAG/PAGのGraph fidelity、未識別の新E11実行禁止、将来の検証済み別識別証明、研究者による新GraphVersion/再識別、partial-ID集合の将来専用Result、緩和可能WARNのみoverride、初期は自動一般化識別器を含めない。[D06詳細](../working_notes/20261115_sr03_d06_graph_uncertainty_identification_override_decision.md) | G01/G02/G10候補（未freeze） | D06-T01〜T14（未実行）：endpoint往復、未識別拒否、Graph親子・追加仮定、override、識別集合≠CI、旧v2回帰、別証明の将来条件 | #16,#17,#24 |
| E11-REQ-P2 | CATE/HTE、Capability指定EconML | G04 | AC-06 異質効果の既知真値と互換性 | #18 |
| E11-REQ-P2A | 個票Parquet、群別診断、privacy | G05 | AC-07 Artifact/support/calibration | #18、#24 |
| E11-REQ-P3T | TemporalDesign、PCMCI系 | G06 | AC-08 既知Lag、GraphとCI仮定 | #20 |
| E11-REQ-P3D | QuasiExperimentalDesign、DiD/Event/ITS | G07 | AC-09 pretrend、timing、cluster、既知効果 | #21 |
| E11-REQ-P3I | Sharp/Fuzzy RD、IV/LATE | G08 | AC-10 cutoff操作とfirst-stage/weak-IV | #22 |
| E11-REQ-P3S | Synthetic Control/SDID | G09 | AC-11 既知効果、RMSPE、donor選択 | #23 |
| E11-REQ-CLI；NFR-001b/002/025/028 | CLI schema、manifest、checksum、依存分離 | G10／各Gate | AC-12 再実行・version・欠落依存・科学的負結果 | #24 |
| 9月末案／8月案／現行基準 | 既存再利用とA/B/C/D/Eの分類 | Gate前 | AC-00 項目ごとの証拠と未確定事項 | #14 |

## 2. 現時点での整合性評価

| 確認事項 | 判定 | 理由 |
|---|---|---|
| 要件意味差分とArchitectureのOwner判断 | **DEC09_OWNER_POLICY_APPROVED / FORMAL_DETAILS_PENDING** | SR03-D01〜06＋DEC01〜08のOwner方針をDEC09で統合、68 Scope・E11-REQ意味差分・Architecture責務・Gate計画をOwnerが承認。FR/NFR/AR正文・具体local CLI schema/enum・独立Architecture Review／正式Gateは未発行 |
| Architecture分割 | **OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING** | ARC09-01〜07（Domain/Adapter/CLI/Product権威・Graph/Result/Manifest/Extras）をDEC09で採用。正式ADR/Port/Schemaと独立レビューのSHAが未完 |
| Gate計画と受入 | **GATE_PLAN_APPROVED / GATE06_07_NOT_FROZEN** | G01〜G10は暫定Workstreamとして採用。開発全体Gate06/07の事前条件と独立科学EvidenceをDEC09で承認したが、K/R/Method別AC・環境・独立ReviewとGate判定は未完 |
| Transition Debtの責務 | **OWNER_SCOPE_APPROVED / PRODUCT_HANDOFF_OPEN** | E11はCLI-only／Local Result、Product API/DB Gap-C01〜04は実装対象外で追跡#14の引渡し候補。専任Product owner・別Enhancement/期限と閉鎖Evidenceは未確認 |
| 現行要件と実装の照合 | **PARTIAL COVERAGE** | `00_01_foundation_gap_reconciliation.md`で9月末13項目のSource照合を完了。現行SHAでのテスト再実行と厳密なFR単位の全件確認は未実施 |

## 3. DEC09統合Owner承認後の具体的残余Blocking Gate

**[DEC-SR04-09独立統合承認記録](../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)の全68行／A0例外・01構想・03要件意味差分・04 Architecture方針・G01〜G10 WorkstreamはOwner採用済み**。この判断で残存するのは「何を初期提供するか」のOwner採否ではなく、以下のControlled Publication／独立Validationである。

1. **Formal Requirements Delta:** 現行要件正本§11のE11 Optional Engine例外と新FR/NFR/ARの実際の条文・新規ID／Status・統合SHAを発行する。既存FR statusを無断でIMPLEMENTEDに変更しない。
2. **Independent Architecture Review:** Domain／Adapter／CLI／Product authorityとLocal Version/Schema、Privacy／Atomic File、Graph/IV/Inference resultを具体ADR/Port/JSON Schemaへ落とし、独立レビューを通す。
3. **Method Science and Gate07 Freeze:** Method41／Scope68／DGP24／NEG28／REF24／AC45／ENV9／X9の全mandatory評価Cell、実K、Method-specific R・CI/B・予算、独立Oracle/Backendの科学的適格性をfreezeする。DEC07/08のOwner方針採用だけでScience PASSにならない。
4. **Environment/Legal:** `pyproject.toml`／`uv.lock`の承認済みWPでの改修、5 Profile＋条件付きRDのfresh isolated install/API・既存v2回帰、SBOM／GPL系顧客SI納入の法務承認を実施する。
5. **Product gap handoff:** GAP-C01〜04はE11で閉鎖しない。Issue #14／Product側の別の実施責任者・期限・別Enhancement・Evidence確認が必要。
6. **Coding authority:** GitHub Issue #15〜24のWork Packageごとのowner／rollback／受入基準と、承認済みFR/ADR/Gate entry snapshotを別途記録する。DEC09そのものをCoding許可に転用しない。

## 4. 結論

**DEC09統合Owner承認は完了。** 68 Scopeの処遇、E11-REQ意味差分、基本Architecture・Gate計画はOwnerが採用した。一方、正式FR/NFR/AR発行・具体ADR・独立Architecture Review・Gate06/07のfreeze・科学的受入・Coding着手条件は未完了のため、**実装／Science GateのAPPROVED/PASSは付与しない**。[DEC09](../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)を承認した入力スナップショットとし、Controlled Publicationと実効Validationへ渡す。
