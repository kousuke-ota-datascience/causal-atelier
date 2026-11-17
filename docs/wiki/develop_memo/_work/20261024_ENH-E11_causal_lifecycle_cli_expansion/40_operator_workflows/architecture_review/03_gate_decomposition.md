# ENH-E11 — G01〜G10 Gate Decomposition (Enhance Workflow Gate IDs)

**文書区分:** 計画・Operator資料  
**状態:** Gate計画Owner承認済み／個別06・07はFreeze前。G01境界は再審査対象  
**前提資料:** 事前調査`../../00_enhance_background/00_01_foundation_gap_reconciliation.md`→`../../00_enhance_background/00_02_foundation_gap_closure_assessment.md`→`../../00_enhance_background/00_03_phase1_to_phase3_reconciliation.md`→`../../00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md`。残存Foundation Gapと8月Phase 1〜3候補を照合してから、承認後のGate境界を判断する。

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

**2026-11-16 DEC-SR04-09によりG01〜G10のGate配置・受入境界をOwnerが計画承認**。個別のGate 06実装契約・07独立検証契約は順次完成させるため、細部の依存・方法別閾値は未Freeze。G01〜G10のGate IDと、各Gate内の`06`/`07`/`999`を混同しない。


## PREP-03：初期実施内容（2026-11-17）

[PREP-02共通設計baseline](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)に基づき、初回対象は**G01（UC-01 Local Question/Design/Graph／FCI/PAG）**。G01の[06実装指示書案](../../10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md)と[07テスト指示書案](../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md)を作成済み。G01では共通値・Graph/PAG・Safe Local Publishの最小基盤を構築し、G02以降は同じ共通契約を再使用する。個票出力Policy認可はG05、IV/ARのHC1推論科学試験はG08、最終全体回帰・配布適格性はG10に配分する。

**状態:** `PREP03_G01_06_07_DRAFT / PREP02_COMMON_DESIGN_FROZEN / G01_CODING_AUTHORIZATION_NOT_YET_ISSUED`。各Gateの正式06/07に対象MethodのDGP/NEG/独立Reference/環境を定め、科学的対象を変更しない。


## 7. 用語訂正と未解決のGate受入境界

G01〜G10は正式Enhance Workflow Gate IDであり、独自Workstream IDではない。06/07/999はGate内の契約・判定文書、P00は計画、P01〜Pxxは実装Execution Unit。従来G01の下に置いた5実装単位は、正式にはG01/P01〜P05と呼ぶ。10 Gateの計画は存在するが全件999未実施。現在のG01はGraph/FCI Science、Linux Atomic Publication/Privacy等の独立authorityを跨ぐため、1 Gateに収める論拠をCoding Authorization前に再審査し、必要なら再分割とOwner承認を行う。06/07はDRAFT。
