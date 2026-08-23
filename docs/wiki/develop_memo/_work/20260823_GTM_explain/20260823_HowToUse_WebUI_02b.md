# Identification

最終的な入力値案

| 項目                      | 入力値                                                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Analysis mode           | **CONFIRMATORY**                                                                                                       |
| Population              | **2024-02-26時点の分析対象household**                                                                                         |
| Comparator              | **クーポン非配布（treated = 0）**                                                                                               |
| Treatment               | **treated**                                                                                                            |
| Outcome                 | **outcome_sales_value**                                                                                                |
| Analysis unit           | **household**                                                                                                          |
| Treatment time          | **2024-02-26**                                                                                                         |
| Outcome window          | **2024-02-26 ～ 2024-03-24（Week 9–12）**                                                                                 |
| Estimand                | **ATT**                                                                                                                |
| Identification strategy | **BACKDOOR**                                                                                                           |
| Adjustment set          | **pre_sales_value**                                                                                                    |
| Assumptions             | **Conditional exchangeability given pre_sales_value / Positivity / Consistency / No interference / temporal ordering** |



-----

# Estimation

| 項目                                     | 推奨入力値                                  | 意味                                               |
| -------------------------------------- | -------------------------------------- | ------------------------------------------------ |
| **Identification Result**              | 今回作成した `REQUIRES_REVIEW / <result id>` | 推定の根拠となるIdentification Result                    |
| **WARN override reason**               | 下記参照                                   | `REQUIRES_REVIEW` / Eligibility WARNを承知して推定へ進む理由 |
| **Base Execution (re-run / revision)** | **新規分析**                               | 初回Estimationなので既存Executionを基準にしない                |
| **Change reason**                      | **空欄**                                 | Base Executionを指定しない場合は不要                        |
| **Estimators**                         | **OLS, IPW, AIPW**                     | BACKDOOR + ATTで比較可能な推定器                          |
| Difference in means                    | **選択しない**                              | 現行実装では `RANDOMIZED + ATE` 用                      |

## WARN override reason

以下を入力

> CPDAGの未確定方向をドメイン知識と時間順序に基づいて確認した上で、方向不確実性を認識したまま探索的な推定を実施するため。

より詳細に記載するならば

> pre_sales_valueはTreatment前、outcome_sales_valueはTreatment後であることをデータ生成過程から確認済み。CPDAGの未確定方向を認識した上で、推定結果を確定的な因果結論とは扱わずEstimationを実施する。




