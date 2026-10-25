# ENH-E11 — 要件定義書改定案

**文書区分:** 計画・意思決定資料  
**状態:** DRAFT／要件の意味上の差分案／未承認  
**前提資料:** `00_foundation_gap_reconciliation.md` → `01_enhancement_concept_and_requirement_revision_plan.md`  
**採番規則:** `E11-REQ-*`は計画上の仮識別子であり、承認されたFR/NFR/AR番号ではない。

## 1. 参照元

- 正本：`docs/wiki/requirement_definition/00_product_concept_memo.md`、`10_requirements_definition.md`（Implementation Status訂正SHA `84c5a624389b233fcb97c656f1c94d177f459c5a`）、`21/22/23/30`の設計文書。
- **第一比較:** `00_foundation_gap_reconciliation.md`。9月末Foundation Gapの既解消・部分充足・新Capability候補を区別する。
- 追加の歴史資料：`20260804_causal_lifecycle_enhancement/03_01〜03_03`、9月末[ENH-E11申し送り](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5)（`HANDOFF_DRAFT`）。
- 後段の三資料比較：`06_three_source_reconciliation_matrix.md`。追跡Issue：#13。

## 2. 現行要件と変更後の意味（案）

| 仮ID | 変更前：現行の正本 | 変更後：ENH-E11案 | 理由・Issue |
|---|---|---|---|
| E11-REQ-P1Q | FR-040/041はQuestion/Designを固定。FR-054・NFR-002のlineageはPARTIAL | ローカルCLIでQuestion/Design/Graphをversion/hash付きで識別する。既存Product資源を再利用できるか検証 | 残差確認 #15 |
| E11-REQ-P1I | FR-042/043/046、AR-005/023はRandomized/BackdoorのIdentification | optional backendによるBackdoor/Frontdoor/IVと`NOT_IDENTIFIED`等の明示的結果を追加 | DoWhy候補 #16 |
| E11-REQ-P1G | FR-035/037は複数Discovery・Graph endpointを要求 | FCIを追加し、PAGのCIRCLE端点と潜在交絡warningを保持。DAGへ暗黙変換しない | 新Discovery #17 |
| E11-REQ-P1R | FR-049はPlaceboとData Subset | Random Common Cause・Bootstrap Refutationと再実行情報を追加 | 新方式 #16 |
| E11-REQ-P1S | FR-050はAdjustment Set・Clipping | 採用が認められた未観測交絡Sensitivity等を追加し、既存2方式を維持 | 拡張 #16 |
| E11-REQ-P1W | FR-047/048はATE/ATTと適用可能な診断。IPW実装済み | Hájek型正規化、IPTWの分散・区間推定の品質、Balance/ESS/Overlapの適用性を明文化 | 品質強化 #19 |
| E11-REQ-P2 | 現行FRにCATE/HTE・EconMLの第一級推定要件なし | CATE/HTEのestimand/spec/result、effect modifier、推論・supportと承認済みEstimatorを規定 | 新規Phase 2 #18 |
| E11-REQ-P2A | CATEファイル成果物の現行要件なし | privacy制限付きParquet/JSON、seed/split/versionと群別要約を規定 | #18、#24 |
| E11-REQ-P3T | 時系列Graph/Discovery専用FRなし | TemporalDesign、TIME_SERIES_GRAPH、PCMCI/PCMCI+/LPCMCI、CI test、lagの忠実な保存 | #20 |
| E11-REQ-P3D | DiD/Event Study/ITS専用FRなし | QuasiExperimentalDesign、event-time、pretrend、cluster等の検証 | #21 |
| E11-REQ-P3I | 既存のRandomized/Backdoorは準実験IVやRDDではない | Sharp/Fuzzy RDD、IV/LATE、first-stage/weak-IVと関連する仮定を規定 | #22 |
| E11-REQ-P3S | Synthetic Control/SDID専用FRなし | donor適格性、pre-fit、timing、placebo、重みと負結果を規定 | #23 |
| E11-REQ-CLI | NFR-001b/002はPARTIAL、NFR-025/028は既存範囲でIMPLEMENTED | ローカルversioned spec、hash/manifest、実効dependency version・seed/split、永続artifact、科学的status | #24 |

**正本との衝突:** 正本§11で未承認のDoWhy/EconMLが対象外とされている。ENH-E11で導入する場合、承認済みoptional Capabilityへ切り替える意味上の変更を明記する。Tigramiteその他Libraryにも同じ採用審査を適用する。

## 3. 必須不変条件（案）

1. **識別可能性を優先:** Estimation/CATE/準実験は対応するDesign・Estimand・Eligibilityを検証する。科学的負結果は実行失敗ではない。
2. **Graphの忠実性:** PAG/CPDAGの不確定性とTemporal lag/向きを保持し、互換性を理由にDAGを偽造しない。
3. **推定対象を区別:** ATE/ATT/CATE/LATE/RD local effectを同一視せず、Predictive subgroup scoreをCATEとして扱わない。
4. **重みの意味:** IPW解析重み、AIPWのPropensity成分、Hájek正規化、Stabilized numerator、Clipping、Trimmingを区別する。
5. **準実験の仮定:** staggered adoption、pretrend、exclusion、weak-IV、RD density、donor contaminationを診断する。ただしソフトウェアは仮定を「証明」できない。
6. **optional engine:** 外部ライブラリの生オブジェクトをDomain/Resultへ保存しない。欠落時は選択した機能のみ unavailable とする（NFR-028）。
7. **CLI-only:** 新機能のAPI/Worker/DB/UI統合なし。既存Product・`causal-analysis-spec/2`・CLI contractとの互換性を保護する。
8. **機密性と再現性:** 個票CATEの出力制限を定義し、任意pickle/importを禁止。Manifestに入力、hash、version、seed/split、成果物、科学的statusを保存する。

## 4. 削除・廃止する要件

**承認された削除・廃止はない。** 9月末`HANDOFF_DRAFT`の「Phase 2/3は後続」の扱いは、正式な構想承認後にENH-E11の計画範囲として改定予定だが、現行FRの削除を意味しない。

## 5. 科学的受入条件への影響（案）

| 手法群 | 主要な科学的根拠 | 負結果・境界事例 |
|---|---|---|
| Backdoor/Frontdoor/IV、FCI | 既知真値のDAG/PAG・識別・endpoint往復 | 非識別、外部依存なし、潜在変数の曖昧性 |
| IPTW/AIPW | ATE/ATT bias、信頼区間被覆率、E9 Diagnostics回帰 | Overlap不足、極端重み、Clipping、PS推定不確実性 |
| EconML CATE/HTE | 既知の効果異質性とestimand互換性 | subgroup support不足、処置型不適合、crossfit leakage |
| PCMCI系 | lag既知の時系列・CI試験 | 不規則時間、lag不一致、潜在交絡warning |
| DiD/Event/ITS | 既知介入効果、pretrend、cluster | 平行トレンド違反、staggered adoption、自己相関 |
| RDD/IV/LATE | cut-off付近の局所効果、強いIV、first stage | 操作、weak/invalid IV、Fuzzy Design不適合 |
| Synthetic Control/SDID | donor panel、RMSPE、placebo | pre-fit不良、donor contamination、support不足 |
| CLI・再現性 | 固定seed再実行、manifest/checksum、method contract | optional依存不足、不正仕様、科学的負結果 |

試験データ、許容誤差、bootstrap回数、clusterルール、coverage閾値等は承認済みGate 07に固定する。**本案はAcceptance Criteriaの確定を意味しない。**

## 6. 未決定事項

- 新規FR/NFR/ARの正式採番とProductコンセプト改定。
- IPTW推論・Trimmingの科学的に適切なdefault。
- Phase 2のIV+MLとしてDRIVまたは同等手法をどう認めるか。
- 個票CATEファイルの最小化・アクセス制限。
- Local spec/manifestのschema versionと既存readerの互換性。
