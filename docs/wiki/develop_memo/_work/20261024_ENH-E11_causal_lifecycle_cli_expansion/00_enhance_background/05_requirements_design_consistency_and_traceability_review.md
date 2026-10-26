# ENH-E11 — 要件・設計整合性とトレーサビリティ確認（計画案）

**文書区分:** 計画・判断記録  
**状態:** DRAFT／照合・承認待ち／Gate未承認  
**前提:** 事前調査`00_01_foundation_gap_reconciliation.md`→`00_02_foundation_gap_closure_assessment.md`→`00_03_phase1_to_phase3_reconciliation.md`と、68行の実装スコープ案`00_04_phase1_to_phase3_cli_scope_proposal.md`を構想・要件・設計策定前に参照する。

## 1. 要件→設計→Gate→受入条件→Issueの対応

`E11-REQ-*`と`AC-*`は**計画上の仮識別子**。承認済みFR/NFR/ARや固定済みGate 07を表さない。IssueのcloseはGate PASSではない。

| 要件案・不変条件 | 設計への反映（案） | 暫定Gate | 受入条件（案） | Issue |
|---|---|---|---|---|
| E11-REQ-P1Q；FR-040/041/054、NFR-002 | Versioned local Question/Design/Graph、適格性・lineage | G01/G02 | AC-01 Identity、不正Design拒否 | #15 |
| E11-REQ-P1G；FR-035/037 | FCI registry、PAG CIRCLE、潜在交絡warning | G01 | AC-02 endpoint往復、潜在交絡の既知例 | #17 |
| E11-REQ-P1I；FR-042/046、AR-023 | optional DoWhy、Identificationの分離 | G02 | AC-03 Backdoor/Frontdoor/IVの識別・非識別 | #16 |
| E11-REQ-P1R/P1S；FR-049/050 | Refutation/Sensitivityの方法別Result | G03 | AC-04 既知真値、seed再実行 | #16 |
| E11-REQ-P1W；FR-047/048 | IPW/AIPWの推論、E9 Diagnosticsの再利用 | G03 | AC-05 Effect精度、coverage、overlap/balance/ESS | #19 |
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
| 要件案と設計案 | **PENDING** | 新FR/NFR/AR、local CLI schema、versioningが未承認 |
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
