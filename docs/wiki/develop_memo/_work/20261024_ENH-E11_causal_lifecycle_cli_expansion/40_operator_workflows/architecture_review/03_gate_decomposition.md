# ENH-E11 — Gate分割案（未承認）

**文書区分:** 計画・Operator資料  
**状態:** DRAFT／Architecture Review・Human承認待ち  
**前提資料:** 事前調査`../../00_enhance_background/00_01_foundation_gap_reconciliation.md`→`../../00_enhance_background/00_02_foundation_gap_closure_assessment.md`→`../../00_enhance_background/00_03_phase1_to_phase3_reconciliation.md`。残存Foundation Gapと8月Phase 1〜3候補を照合してから、承認後のGate境界を判断する。

## 1. 分割原則

Gateは下流の手法や利用者が依拠できる**意味上の受入境界**である。実装ファイル数、Issue数、Agentの作業量などはWork Packageの分割理由であり、Gateを増やす理由にはならない。正式なauthorityは将来固定するGateごとの06/07と、独立したcanonical 999判定にある。

## 2. 暫定Gate一覧

| Gate | 暫定の受入主張 | 着手前提 | PASS後に保護するもの | Issue |
|---|---|---|---|---|
| G01 | Local causal contextとGraph/FCIの不確定性を再現できる | Local Context/Graph schemaの承認 | Spec/hash、PAG端点の忠実性 | #15、#17 |
| G02 | Identification/Eligibilityおよびoptional DoWhyで推定可否を安全に判定する | 適用可能なG01 semantics | Native/DoWhyの統一statusと科学的負結果 | #15、#16 |
| G03 | Refutation/Sensitivityと既存IPTW/AIPWの推論・診断を検証する | G02の識別・適格性 | Effect/Refutation/Sensitivityの科学的契約 | #16、#19 |
| G04 | CATE/HTE estimandとEconML推定器を提供する | G02、適用可能なG03診断 | CATE Resultと承認済みEstimator | #18 |
| G05 | CATEのsupport/calibration/uncertaintyとprivacy配慮済みfileを検証する | G04の推定結果 | Policy-ready Artifact、HTE Diagnostics | #18、#24 |
| G06 | Temporal Discoveryでlag/不確実性を保持する | G01 Graph Schema判断 | TIME_SERIES_GRAPHとPCMCI系 | #20 |
| G07 | DiD/Event Study/ITSのDesign・推定と診断を検証する | 準実験Designの承認 | Timing/pretrend/cluster/ITSのResult契約 | #21 |
| G08 | RDD/IV/LATEの局所効果とDesign検証を行う | Design/Identification semantics承認 | RD/IV Resultとweak identification対策 | #22 |
| G09 | Synthetic Control/SDIDのdonor・counterfactual・placeboを検証する | Donor Design承認 | Synthetic系のResultとDiagnostics | #23 |
| G10 | CLI/Manifest/Benchmark回帰でlocal再現性を検証する | 各手法Gateの受入 | すべての承認済み結果をchecksum付きで再実行可能にする | #24 |

## 3. 暫定順序の理由

G01〜G03はContext/Identification/既存推論を固め、G04〜G05がCATE/HTEを拡張する。Temporal G06と準実験G07〜G09は、Design決定後に依存関係を再評価する。CLI file contractは**初期に必要**だが、全体的な最終受入は各手法の科学結果が受け入れられた後となる。このためGateの統合・分割・順序はArchitecture Reviewで変更し得る。

## 4. 全体の完了条件（案）

Phase 1〜3の必須手法が、再利用済みであることを証拠で示すか、手法ごとの独立999 PASSを得ている。G10で固定SHA・成果物hash・Manifest・再現性を確認する。方法一覧を確定するauthorityは承認済み要件/設計であり、Issue closeではない。

## 5. 不適切な並列作業を避ける

- 識別されていない、または曖昧なEstimand schemaのままCATEを実装しない。
- Graph semanticsの合意前にLPCMCIのendpointを固定しない。
- 方法別仮定と負結果契約の承認前にRDD/IV/SynthのResultを固定しない。
- Issueが複数あるだけでGateを分けず、単なる作業分割はWork Packageで扱う。

## 6. Architecture Reviewで再検討する事項

- G04とG05を独立Gateとする科学的理由は十分か。
- G07〜G09を共通Design authorityのGateへ統合し、Work Packageを分けるべきか。
- G10でのManifest検証は最終統合だけでなく各Gateの必須ACとすべきか。

**G01〜G10の番号・依存関係はいずれも案であり、固定されていない。**
