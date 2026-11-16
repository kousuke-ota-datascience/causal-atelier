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
| 要件案と設計案 | **PARTIAL/PENDING** | SR03-D04-1〜5、D05-1〜5、D06-1〜6の個別設計方針は2026-11-15オーナー採用済みで03/04 Draftにも反映。新FR/NFR/AR、具体的local CLI schema/version/enum、全体要件・Architecture ReviewとGateは未承認 |
| 設計案とGate分割 | **PENDING** | Architecture ReviewがauthorityとGate境界を未確定 |
| Gate間の依存 | **PENDING** | G01〜G10は草案であり06/07契約ではない |
| Transition Debtの終了条件 | **PARTIAL/PENDING** | API/DBの将来境界は記載したが正式な承認なし |
| 現行要件と実装の照合 | **PARTIAL COVERAGE** | `00_01_foundation_gap_reconciliation.md`で9月末13項目のSource照合を完了。現行SHAでのテスト再実行と厳密なFR単位の全件確認は未実施 |

## 3. 残る判断・承認の阻害要因

1. `00_04_phase1_to_phase3_cli_scope_proposal.md`におけるPhase 1〜3の全必須候補と、A0上位要求の後続送り・最小Negative Control/Sensitivity方式、および利用するLibrary版で該当classが存在しない場合の科学的同等代替をHuman ownerが決める。
2. 正本§11の外部engine除外を承認付きの要件差分で改定する。
3. DB-free local runのQuestion/Design/Graph identity・versionを確定する。
4. 手法固有の分散推定・coverage・科学ベンチマークの許容閾値を固定する。
5. 個票CATEの保存・privacy・atomic writeを決める。
6. 暫定G01〜G10とIssue→Gateの対応をArchitecture Review後に見直す。
7. 正式オーナー承認、固定SHAでの独立科学的検証はいずれも未了。

## 4. 結論

**現時点では06/07のfreezeやCodingに進めない。** トレーサビリティの構造は草案として存在するが、重要な判断は保留中。先行照合資料を踏まえ、Issue #14のArchitecture Reviewとオーナー承認を経て03/04/05を改訂し、承認済み正本Snapshotを作成する。
