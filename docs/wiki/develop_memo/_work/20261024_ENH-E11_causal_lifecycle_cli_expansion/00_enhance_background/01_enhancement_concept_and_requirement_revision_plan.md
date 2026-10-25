# ENH-E11 — 構想・要件改定計画（案）

**文書区分:** 計画・意思決定資料  
**状態:** DRAFT／オーナーの対象範囲方針のみ確認済み／正式承認待ち  
**起案日:** 2026-10-24（日本時間）  
**追跡Issue:** https://github.com/kousuke-ota-datascience/causal-atelier/issues/13

> **前提となる事前調査:** [00_foundation_gap_reconciliation.md](00_foundation_gap_reconciliation.md) が先行する。以下の構想はその調査結果を入力として扱う。事前照合における「実装の存在」「テストの存在」「過去のGate PASS」「現行SHAでの再実行」を混同しない。Phase 1〜3への拡張は、9月末構想の不足判定とは別に審議する。

## 1. 解決すべき問題と経緯

2026年8月4日の因果推論ライフサイクル構想は、Identification、Refutation、Sensitivityに加えて、CATE/HTE、時系列因果探索、準実験デザインを対象としていた。9月末のENH-E11申し送り（`HANDOFF_DRAFT`）では、後続の実装を考慮し、対象を**現行実装に対する基盤の残存Gap**へ縮小した。その後のオーナー方針では、8月案Phase 1〜3の必須機能をENH-E11に再度含める一方、新機能の提供面をScientific Core・ローカルCLI・永続ファイル成果物に限定することとなった。

**事前照合による確定範囲:** 既存Graph、Randomized/Backdoor Identification、Data Eligibility、ATE/ATT・IPW/AIPW、構造化Diagnostics、既存Refutation/Sensitivityは実装・テストの存在が確認されている。FR-051/AR-004の探索データ再利用警告、FR-054/FR-008/FR-095/NFR-002のlineage、NFR-001bの再現性metadataには未充足が残る。DoWhy/FCIは現行必須要件の未実装ではなく**新規Capability候補**である。詳細・証拠・検証限界は先行資料00に記載した。

この区別を行わず8月案を実装すると、既存実装の重複、未承認外部ライブラリの導入、正本要件§11との不整合を生む。

## 2. 実施する理由

- **ENH-E7:** Project管理とAnalysis Workspaceが分離された。Scientific CLIをWeb Navigationの状態に依存させない。
- **ENH-E8:** Identification、Estimation、Effects、Diagnostics、Sensitivityの責務が分離された。Navigation Stageと実行Stageは同一概念ではない。
- **ENH-E9:** Weight、Balance、Overlap、ESSの構造化Diagnosticsは既存実装を再利用し、新規手法の名目で作り直さない。
- **ENH-E10:** optional analytical engineの依存分離を参考にする。Predictiveのadvanced modelを因果CATEと同一視しない。
- **検証方針:** CLI-only機能の科学的妥当性はUnit／Contract／Scientific Benchmarkを中心に確認し、Browser E2Eを第一証明としない。

## 3. 現状と基準

計画時の参照ブランチは`prototype/ariadne_mvp`。正本のImplementation Status訂正点は`84c5a624389b233fcb97c656f1c94d177f459c5a`、9月末案との現行コード照合は`00_foundation_gap_reconciliation.md`（調査時SHA `4c0129146a59e7a294f13f41a2e27a4b0d820a6f`）とする。**正式なENH-E11 Gateの受入基準SHAは未確定**。

新規候補はDoWhy、FCI、Refutation/Sensitivity追加方式、CATE/HTE、Tigramite、準実験群等である。これらを現行FRに含まれていたと読み替えない。正本§11の外部engine除外を変更する場合、承認された要件差分を先に作成する。

## 4. 目標状態

1. 8月案Phase 1〜3の必須Capabilityについて、既存機能の再利用・品質強化・新規実装・承認済み代替を識別できる。
2. 対象とする新機能をScientific CoreとローカルCLIで実行でき、科学的status、診断、入出力checksum、依存version・seedを永続ファイルから追跡できる。
3. 要件→設計→Issue→Gate→受入条件→独立検証→canonical 999判定を辿れる。

## 5. 対象範囲

### 5.1. 対象

- **Phase 1:** Question/Design/Graph/version/Eligibility残差、optional DoWhy、FCI/PAG fidelity、Refutation・Sensitivity追加、既存ATE/ATT・IPTW/AIPWの科学的品質と診断。
- **Phase 2:** LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S/T/X-Learner、DRIVまたは科学的に同等なIV+ML、第一級CATE/HTE、cross-fitting、推論・support・calibration、policy-ready**ファイル**成果物。
- **Phase 3:** Tigramite PCMCI/PCMCI+/LPCMCI、CI-test registry、DiD、Event Study、Sharp/Fuzzy RDD、IV/LATE、Synthetic Control、Synthetic DiD、Interrupted Time Series。それぞれのデザイン固有の仮定・診断・既知真値検証を含む。
- **横断:** ローカルCLI仕様、Manifest/Hash/Version/Seed/Split、依存分離、科学的結果と技術失敗の区別、科学ベンチマーク。

### 5.2. 対象外

- **新機能**のWeb UI、Web API、Worker、DB統合、およびCLI機能の科学的妥当性を証明するためのBrowser E2E。
- Phase 4：Policy Evaluation/自動意思決定、capacity/cost最適化、drift監視、運用承認。
- 8月の非必須拡張候補であるRPCMCI/J-PCMCI+、あらゆる外部Libraryの網羅。
- GitHub Issue #11のリポジトリ全体のテスト基盤移行。

## 6. 要件改定の見込み

- FR-035〜050およびFR-153〜156の**現在の意味**とImplementation Statusは維持する。それだけを根拠にDoWhy/FCI/CATE/Phase 3を実装済みとしない。
- optional backendの識別・Refutation、Graphの不確実性保持、CATE/HTE、時系列Graph、準実験Design、ローカル成果物の新FRを検討する。
- NFR-001b/002/025/028、試験可能性・科学的透明性に係るNFRおよびAR-005/010/023等について、新手法固有の受入条件を検討する。
- 非識別のまま数値を返さない、PAGから架空のDAGを作らない、Predictive subgroup指標をCATEとみなさない、weak-IV等を無警告で成功扱いしない。
- 正式なFR/NFR/AR採番・正本反映は**承認後**とし、具体案は`03_requirements_revision.md`に記す。

## 7. 設計改定の見込み

- Domainは外部Libraryの型に依存せず、Scientific Coreにはoptional backendと手法別validation/registryを設ける。
- Causal/Temporal/Quasi-experimental DesignとResultを、estimandと科学的negative statusを区別できる契約にする。
- Versioned local specとParquet/JSON/Markdown成果物、hash付きmanifestを使用し、E11に新規DBモデルは導入しない。
- 既存Product実行経路・API/Worker/UIおよび`causal-analysis-spec/2`を暗黙に変更しない。

## 8. 主なリスクと互換性

- **対象拡大:** 9月末案のPhase 2/3除外を変更する正式な承認が必要。
- **科学的妥当性:** estimandの異質性、識別可能性、時系列leakage、staggered DiD、weak-IV、overlap、信頼区間被覆率。
- **依存関係:** external engineのversion/platform互換性。optional install、局所import、明示的unavailable状態が必要。
- **後方互換性:** `ipw`等のCLI引数、Manifest reader、既存FRの意味、E9 Diagnosticsの適用範囲を保護。
- **セキュリティ:** 任意import/pickleを避け、個票CATEの無制限な出力を標準にしない。
- **受入証拠:** 過去の999 PASSと現行SHAでの再実行を別扱いにする。

## 9. Architecture Reviewの要否

**必須（未完了）。** 新たなScientific Core入口、Spec/Resultの所有権、時系列Graph、local fileの永続性・lineage、互換性、optional dependency、Gate境界を実装契約より前に決める。

## 10. 暫定Gate構成（承認前）

| Gate | 暫定的な受入境界 | 対応Issue |
|---|---|---|
| G01 | Local causal context、Graph/FCIの不確実性を保持する版管理 | #15、#17 |
| G02 | 識別・適格性とoptional backendの科学的status | #15、#16 |
| G03 | Refutation/SensitivityおよびIPTW/AIPWの推論・診断 | #16、#19 |
| G04 | CATE/HTE estimandとEconML推定器 | #18 |
| G05 | CATEのsupport・不確実性とプライバシー配慮済みファイル | #18、#24 |
| G06 | Temporal GraphとPCMCI系のlag/endpoint | #20 |
| G07 | DiD/Event Study/ITSとpretrend/timing/cluster | #21 |
| G08 | RDDとIV/LATEの局所効果・診断 | #22 |
| G09 | Synthetic Control/SDIDとdonor/placebo | #23 |
| G10 | CLI Manifest/Provenance、再現性と回帰・科学検証 | #24 |

**Gate数・順序は固定ではない。** Architecture Reviewによる統合・分割判断を要する。Work PackageはGate内の作業単位として別途定義する。

## 11. 実装前に必要な承認

- Foundation-onlyからPhase 1〜3のCLI-onlyへ対象を拡大する正式な構想承認。
- 必須手法、同等実装の許容条件、推論手法、許容誤差、privacy方針。
- 正本§11の変更、新FR/NFR/AR、設計上の所有権、optional dependency policy、file contract。
- Gate構成、固定SHA、06/07のfreeze。各種承認をIssueのcloseで代替しない。

## 12. 出典

- **先行調査:** [00_foundation_gap_reconciliation.md](00_foundation_gap_reconciliation.md)
- **歴史的構想:** `20260804_causal_lifecycle_enhancement/03_01〜03_03`（要件正本ではない）。
- **9月末申し送り:** https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5 （`HANDOFF_DRAFT`）。
- **正本の参照SHA:** `84c5a624389b233fcb97c656f1c94d177f459c5a`。
- **後段の比較案:** `06_three_source_reconciliation_matrix.md`。Issue台帳：`07_github_issue_register.md`。
