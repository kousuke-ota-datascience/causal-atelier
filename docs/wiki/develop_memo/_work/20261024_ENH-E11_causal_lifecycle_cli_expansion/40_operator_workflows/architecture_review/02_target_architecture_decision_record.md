# ENH-E11 — 目標アーキテクチャ判断記録（案）

**文書区分:** 計画・Operator判断記録  
**判断状態:** **PROPOSED／未承認**  
**判断権限:** Human architecture owner（保留中）  
**判断日時:** 未発行  
**前提調査:** `../../00_enhance_background/00_foundation_gap_reconciliation.md`、`01_architecture_discovery.md`

## 1. 背景

2026年8月のPhase 1〜3構想は、9月末`HANDOFF_DRAFT`でFoundation-onlyへ限定され、その後のオーナー方針によりCLI-onlyの対象へ再採用された。現行ProductはATE/ATT、Graph、既存Causal stageを実装済み。CATE、時系列、準実験は推定対象と科学的仮定が異なるため、独立したportable contractが必要である。

## 2. 現行コードの確認事項

`01_architecture_discovery.md`に根拠を記載した。ScientificCoreAdapterは型付きResult descriptorを返し、CLIには厳密な設定schemaとManifestがある。E9 Diagnosticsには適用対象を区別する契約がある。これらの事実だけでは、新しいLocal Designのsource of truthを確定できない。

## 3. 提案する決定（未承認）

- **Domain:** 外部Libraryに依存しないQuestion/Design/Graph/Estimand/Result semanticsを所有する。
- **Scientific Core Adapter:** Library実行、方法別validation、数値結果を所有する。
- **Local CLI:** 入出力path、Manifest、local fileを所有する。import方向はArchitecture Reviewで検証する。
- 共通envelopeを用いても、CATE/RD/LATEを根拠なくATEへ統一しない。方法別のDesign/Result statusを維持する。
- optional backendはメソッド単位でimport・versionを分離する。
- 新規出力はversioned local fileのみ。既存DBのauthorityを変更しない。
- 候補SHA、テスト証拠、受入はWorkflowによって決まり、Issueのチェック状態では決まらない。

## 4. 提案する権威情報の所在

| 関心事項 | CLI-only E11で提案するauthority |
|---|---|
| Local Question/Design/Graph | 検証済みVersioned local specとcontent hash。現行Productの意味へ対応付ける |
| 外部engineのobject | 一時的なScientific Core Adapter内部。標準payloadにはしない |
| 推定値と科学的負結果 | 手法固有estimand/status/warningsを持つAriadne Result |
| 個票CATE・時系列・donor data | schema version・checksum付きParquet/JSON |
| backend version・seed/split・入力 | local run Manifest（固定SHAで再現可能にする） |
| 既存Product DB Resource | 既存のauthorityを維持。統合は後続 |
| Gate受入状態 | 独立したcanonical 999 Gate Decision |

## 5. 不変条件と検証方式（案）

| ID | 不変条件 | 主な確認方法 |
|---|---|---|
| ADR-I01 | DomainがDoWhy/EconML/Tigramiteの型をimportしない | Import/Architecture contract |
| ADR-I02 | PAGのCIRCLE端点やTemporal lagを勝手にDAGへ変換しない | Graph往復・負例 |
| ADR-I03 | Identification/EligibilityをEstimationと分ける | 既知真値・非識別試験 |
| ADR-I04 | IPTW重み、DRのPropensity成分、Synthetic donor重みを混同しない | Estimator/Diagnostics contract |
| ADR-I05 | CATE/LATE/RD local effectを根拠なくATEと記録しない | Estimand/Design schema contract |
| ADR-I06 | optional backend欠落時も無関係なCLI機能が動く | Dependency-unavailable試験 |
| ADR-I07 | version/input/split/seed/artifact hashでfile出力を再実行できる | 固定SHAの再現性Benchmark |
| ADR-I08 | E11の新機能がWeb API/Worker/DB/UI runtimeに依存しない | Architecture contract |

## 6. 制約

- `causal-analysis-spec/2`と現行standalone CLIを維持するか、承認済みの明示的schema migrationを行う。
- 任意import/pickleの受入禁止。個票CATEをdefaultで無制限に公開しない。
- 科学的仮定・負結果statusを人間が読める形で保存する。

## 7. 削除・廃止対象

承認された削除はない。既存Product runtime経路を撤去しない。便宜的にE9/E10の安定実装を作り直さない。

## 8. Transition Debtと終了条件

新手法のlocal出力をProductの永続DB Resourceと同一視しない。将来のWeb API/Worker/DBへの対応とMigrationは後続案件で決定する。互換性を無制限に保証すると暗黙に約束しない。

## 9. 検討した代替案

- **Web UI/API/Worker/DBを同時実装:** 開発とBrowser E2Eの負担を考慮したオーナー方針により今回対象外。
- **DoWhy/EconML objectを標準Resultにする:** 外部Library versionへの依存が強く、提案として不採用。
- **すべての方法をATE/ATTのEstimationInputへ押し込む:** estimand/仮定が異なるため提案として不採用。
- **9月末案どおりPhase 1だけ:** 後のCLI-only方針で計画上は更新。ただし9月末案の歴史的事実は保持する。

## 10. 想定される影響・リスク

Versioned file schema、科学的Benchmark、optional dependency support matrixが必要となる。ENH-E11の結果をProduct全レイヤー統合済みとは表示しない。

## 11. 承認

- **状態:** PENDING
- **承認者:** Human owner / Architecture owner
- **承認根拠:** 未発行
- **禁止:** 本案だけを根拠にGate 06/07をfreezeしたり、実装を開始したりしない。
