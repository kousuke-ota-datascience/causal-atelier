> **Historical classification snapshot（2026-11-16）:** 本台帳はRD-01時点の`DISPOSITION_PROPOSED`を保持する。後続の[RD-04全体監査](../98_rd04_consistency_verification.md)で再審査・条文改訂・下位設計移管を実施済み（FR-176/177・AR-021/024等にDisposition改訂あり）。以下のRD-01「NOT_STARTED／PENDING」は本書作成時点の履歴であり現在の進捗を表さない。

# RD-01 — Requirement Granularity Disposition Review

**Review ID:** RD-01  
**Date:** 2026-11-16  
**Source branch:** `prototype/ariadne_mvp` / source blob `40b83f29c67b4a39f6db5393be7534c5e892d656`; E11 draft blob `e6b151a0537054a11e8368520e940bd42cb68e2f`  
**Status:** `DISPOSITION_PROPOSED / NOT_YET_APPLIED / OWNER_REVIEW_REQUIRED`. 本書は逐条分類の提案記録であり、正式RD/BD/IF/DDの改訂、既存Requirementの失効、Method Scopeの変更、Gate PASSを意味しない。

**判定原則:** 『何を満たさなければならないか』をRDに残す。方法自体が承認された提供義務の場合は`10_32_scientific_method_scope.md`相当のScope契約で保持し、実装と同一視しない。科学的Estimand/前提の制限は`10_31`等で保持する。移管のみのIDもTrace台帳から削除せず、統合元要求を明記してControlled Publicationで処理する。

## 1. 判定母集団と完全性

| 群 | 件数 | KEEP_RD | REWRITE_RD | SPLIT | MOVE_* |
|---|---:|---:|---:|---:|---:|
| FR | 195 | 107 | 3 | 67 | 18 |
| NFR | 36 | 13 | 2 | 20 | 1 |
| AR | 27 | 16 | 2 | 5 | 4 |
| E11-F | 19 | 0 | 3 | 16 | 0 |
| E11-N | 8 | 1 | 0 | 7 | 0 |
| E11-A | 7 | 0 | 0 | 3 | 4 |
| **合計** | **292** | **137** | **10** | **118** | **27** |

- 既存FR 195、NFR 36、AR 27、ENH-E11 draft 34（E11-F19 / E11-N8 / E11-A7）、計292 IDについて原文→Disposition→RD要件核→移管先を1:1で記録。
- 既存正式RequirementのID/Level/Status/Implementation Status/Deliveryは**変更していない**。E11 IDは**暫定**であり正式番号ではない。
- `KEEP_RD` の要件核は原文。 `REWRITE_RD` / `SPLIT` の要件核は**未承認の編集候補**。
- `MOVE_BD` 等は『元の義務を黙って廃止』する意味ではない。再配置時には基になる要件とのTraceと承認履歴を必須とする。
- 要件が属するCategoryと移管先の判定は独立。すべての文書に原文を保存するのではなく原正本へのリンクとblob SHAで監査可能にする。

## 2. 一貫性と重点レビュー

1. **FR-178/181/182、E11-F-04〜16:** 各Methodの供給義務・適格制限・対象Estimandは抽象的な能力要件から消してはならず、承認済ScopeカタログへTraceする。
2. **AR系列の意味:** 既存`AR-001〜027`はScientific Integrity/Analytical Requirement。E11-AはArchitecture要求草案であり、正式ARへ単純連番してはならない。
3. **純粋な設計制約:** `MOVE_BD` 等の旧Requirement IDは移行判定後もlegacy traceとして保持し、Requirement Statusを自動`RETIRED`にしない。
4. **RD以外の移管先:** `21 LDD`は論理データ定義、`22 BD`は方式、`23 IF`は具体的インターフェース、`30 DD`はクラス・数値実装、`10_31/10_32`は科学的要求・承認Method範囲である。
5. **科学的受入基準:** `AR-016`のbootstrap 95%/1000回や`E11-N-07`のFWER 0.05など、承認済の定量的条件は技術的検証プロトコルへ移しても受入基準として保持する。
6. **既存要件状態:** Source snapshotで`DEFERRED/PARTIAL`のものを`ACTIVE/IMPLEMENTED`へ変更していない。

## 3. 出力台帳

- [92_rd01_fr_disposition_register.md](92_rd01_fr_disposition_register.md) — 既存FR 195件
- [93_rd01_nfr_ar_disposition_register.md](93_rd01_nfr_ar_disposition_register.md) — 既存NFR36/AR27件
- [94_rd01_e11_draft_disposition_register.md](94_rd01_e11_draft_disposition_register.md) — E11草案34件

## 4. RD-01終了判定と残課題

- **対象ID抽出・逐条分類:** DONE（292/292、ID重複0、未定義Disposition0）。
- **意味・採用先の独立承認:** PENDING。逐条Dispositionは編集提案であって正式改訂ではない。
- **Requirement本文の再配置・採番変更（RD-02）:** NOT_STARTED。
- **E11正式IDと68 Scope / 41 Method / 10 UC完全照合（RD-03）:** NOT_STARTED。
- **科学Method/Backend検証:** NOT_EXECUTED。

## 5. 確定した次期ファイル番号（RD-02）

Owner採用の`10_00`, `10_01`, `10_02`, FR `10_10〜18`, NFR `10_20〜22`, 科学 `10_30〜32`, `10_40`, `10_50`, `10_90`, `10_91`, `10_99`を移行先の**構成契約**とする。RD-01でファイルを移動した事実はない。
