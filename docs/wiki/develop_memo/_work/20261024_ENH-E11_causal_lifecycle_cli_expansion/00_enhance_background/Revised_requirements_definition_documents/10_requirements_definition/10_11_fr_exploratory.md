# 10_11_fr_exploratory


---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-023 | Explore | Dataset overview、schema、型、欠損率、cardinalityを表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-024 | Explore | 数値列・カテゴリ列の記述統計と分布を生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-025a | Explore | 列別missingnessを確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-025b | Explore | 複数列のjoint missing-pattern analysisを行える | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-026a | Explore | 変数の型に応じた二変量間の関係を分析できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-026b | Explore | 散布図、箱ひげ、クロス集計等のfull exploratory bivariate visualization surfaceを提供する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-027 | Explore | group-by集計および時系列推移を生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-028 | Explore | correlation / association matrixを型に応じて生成できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-029 | Explore | 可視化の条件を保存し同じデータ版で再実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-030 | Explore | 探索実行のResultとArtifactを保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-031 | Explore | 保存した探索Resultに観察メモと限界をAnnotationできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-032 | Explore | 探索結果から因果・予測分析の草案を生成し由来を追跡できる。本人の確定・実行を必要とする | SHOULD | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-033 | Explore | 探索結果をEXPLORATORYと表示し、確認的結論として自動昇格しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-034 | Explore | 探索に用いたデータ選択・分析設定・実行環境および成果物の由来を再構成できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-146 | Exploratory | Exploratoryは`profile / data-quality / distribution / relationships / comparison / findings`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-147 | Exploratory | 可視化は探索の各目的に即して利用できる | MUST NOT | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-148 | Exploratory | 探索上のFindingで既存の結果・注釈・来歴を利用できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-175 | Exploratory Surface | 探索のデータ品質・時間推移・Findingを既存意味で利用できる | MUST | ACTIVE | IMPLEMENTED | ENH-E7 |
