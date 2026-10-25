# ENH-E11 — 現行アーキテクチャの調査

**文書区分:** 計画・Operator調査資料  
**状態:** 読取り調査の初版／網羅性の審査待ち  
**事前の必須入力:** `../../00_enhance_background/00_01_foundation_gap_reconciliation.md`（9月末の照合）→`../../00_enhance_background/00_02_foundation_gap_closure_assessment.md`（残存Gap）→`../../00_enhance_background/00_03_phase1_to_phase3_reconciliation.md`（Phase 1〜3差分）。  
**正本の参照点:** 要件訂正SHA `84c5a624389b233fcb97c656f1c94d177f459c5a`。現行実装の一次照合は先行00資料に記録済み。

## 1. コードから確認した事実

| 調査対象 | コード上の確認事項 |
|---|---|
| Scientific Estimation | `src/ariadne/scientific/inference/adapter.py`はDiff/OLS/IPW/AIPWを選び、Result/Diagnosticsを返す |
| 推定器 | `src/ariadne/causal/inference/estimators/treatment_effect.py`にATE/ATT、IPW/AIPWの実装がある |
| Propensity Score | `src/ariadne/causal/inference/nuisance/propensity.py`にlogistic fittingがある |
| Graph Discovery | `src/ariadne/scientific/discovery/adapter.py`はPC/GES/LiNGAM/NOTEARSを提供。FCIは現行registryにない |
| Identification | `src/ariadne/scientific/identification/adapter.py`はnative識別とCPDAG/PAGの慎重な扱いを実装 |
| Refutation/Sensitivity | 各`scientific/refutation/adapter.py`・`scientific/sensitivity/adapter.py`は正本にある2方式ずつに対応 |
| CLI入力 | `src/ariadne/interfaces/cli/config_schema.py`はDiscovery/Identification/Estimation/Refutation/Sensitivityの厳格なlocal schemaを持つ |
| CLI Manifest | `src/ariadne/interfaces/cli/manifest.py`は再現性metadataを定義。ただし実効backend版の記録は要確認 |
| Product Specification | `src/ariadne/product/domain/analysis_spec.py`は既存ATE/ATT・識別手法に限定 |
| 正本 | `docs/wiki/requirement_definition/10_requirements_definition.md`のFR-035〜054等。§11に未承認engineの除外規定 |
| E9の検証 | `tests/enhancement/enh_e9/g04/scientific/`にweight適用性、ESS、保存、balanceなどのテスト |

上記は**ソース調査による存在確認**であり、現行SHAでの新規pytest合格を意味しない。今回の作業でコード・DB・schema・server経路は変更しない。

## 2. 検証を要する推論

1. Domainを外部ライブラリ型から独立させ、optional Adapterを使えば、新規API/Worker/DBなしでCLI実行できる可能性がある。ただしQuestion/Design/Graphのlocal identityを定義する必要がある。
2. E9の既存Weighting DiagnosticsはIPTWと**適用可能な**Phase 2推定器で再利用できる。一方、すべてのEconML EstimatorにIPW最終重みが存在するわけではない。
3. 時系列・準実験は横断データ向けATE推定器の入力に項目を足すだけでなく、独立した型付きDesignが必要と考えられる。
4. Versioned Manifestとchecksumは将来のProduct統合に利用できる可能性があるが、現時点のcanonical DB lineageを完成させる根拠にはならない。

## 3. 未確認事項と追加の調査

- 既存Product API/Worker/DBの書込・読取経路とMigration owner。ENH-E11では変更しないが将来の境界を記録する。
- 既存Question/Design version resourceをDBに依存せずlocal serializeできるか。
- 外部Library version/platformごとのPhase 1〜3のAPIと統計推論の提供状況。
- Local Manifest schema、partial writeのatomicity、個票CATEのprivacy policy。
- 現行動作に対応する過去の999と、固定SHAで再実行すべきテスト。
- CATE/Temporal/Quasi-experimentalで共通のResult envelopeが方法別仮定を隠さず表現できるか。

## 4. 判断待ち事項

Architecture Decision Recordでは、authority・version・optional engine、方法別科学的status、ファイル書込とread-back、privacy、推論の品質、semantic Gate境界を決定する。**未承認であり、コード調査から承認を推定しない。**
