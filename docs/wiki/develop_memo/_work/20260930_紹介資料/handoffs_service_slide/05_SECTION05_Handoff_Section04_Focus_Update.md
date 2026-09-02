Document title: Section 05 Handoff｜Section 04重点テーマ追加に伴う因果推論セクション修正

# 1. Handoff目的

Section 04に、当チームの重点テーマとして以下3枚を追加した。

1. 故障予測・異常検知とは何か
2. 故障予測・異常検知が適する業務課題
3. 故障予測・異常検知の期待効果

これにより、Predictiveセクションは7枚から10枚へ増え、Section 05以降のDeck Slide番号がすべて+3される。また、Section 04 → Section 05の論理接続に「設備のFailure Risk / Anomaly」と「保全施策のTreatment Effect」の境界が新たに加わる。

本Handoffは、05-*を修正する際に必要な番号・意味論・Cross-slide変更を一括して引き継ぐためのものである。

# 2. Section 04変更後の確定構造

| File | Deck Slide | 役割 |
|---|---:|---|
| 04-01 | 11 | 予測分析とは |
| 04-02 | 12 | 予測分析が適する業務課題 |
| 04-03 | 13 | 予測分析適用による期待効果 |
| 04-04 | 14 | 重点テーマ：故障予測・異常検知とは |
| 04-05 | 15 | 重点テーマ：故障予測・異常検知が適する業務課題 |
| 04-06 | 16 | 重点テーマ：故障予測・異常検知の期待効果 |
| 04-07 | 17 | 予測分析PoCの分析プロセス |
| 04-08 | 18 | 代表的な予測アプローチと選定方法 |
| 04-09 | 19 | 予測モデルの評価と解釈 |
| 04-10 | 20 | 予測分析PoCの成果物とGo / No-Go |

Section 04の最終Transitionは以下の意味論でSection 05へ渡す。

```text
Predictive / Detection
「どの設備が故障しそうか」
「どの状態が通常と異なるか」
        ↓
保全Decisionの判断材料にはできる
        ↓
しかし
「保全施策を変えると故障・停止がどれだけ減るか」
には直接答えられない
        ↓
Causal / Treatment Effect
```

# 3. Section 05の新しいDeck Slide番号

05-*のファイル番号はそのまま保持し、Deck Slide番号のみ+3する。

| File | 旧Deck Slide | 新Deck Slide | 役割 |
|---|---:|---:|---|
| 05-01 | 18 | **21** | 因果推論とは |
| 05-02 | 19 | **22** | なぜ予測だけでは施策判断に答えられないのか |
| 05-03 | 20 | **23** | 因果推論が適する業務課題 |
| 05-04 | 21 | **24** | 因果推論適用による期待効果 |
| 05-05 | 22 | **25** | 因果推論PoCの分析プロセス |
| 05-06 | 23 | **26** | Causal QuestionとEstimandの定義 |
| 05-07 | 24 | **27** | 因果構造と前提条件の整理 |
| 05-08 | 25 | **28** | IdentificationとEstimationを分けて考える |
| 05-09 | 26 | **29** | 代表的な因果推論アプローチと選定方法 |
| 05-10 | 27 | **30** | 診断・感度分析とPoC成果物 |

各05-*ファイルでは以下を一括更新すること。

- `# XX. Slide XX` のDeck番号。
- `## XX.1`〜`XX.5`および配下の見出し番号。
- Supporting Logic内の `Slide XX` 参照。
- Transitionの `Slide XXからSlide XX+1`。
- 前後Slide番号への言及。

# 4. 05-00_Section05_Story.mdで必要な変更

## 4.1. Slide Mapping

Deck Slideを21〜30へ変更する。

## 4.2. Section Entry

Section 04の重点テーマ追加を受け、Section EntryではCustomer Retentionだけでなく設備保全の境界も明示する。

保持すべき対比：

| Predictive / Detection Question | Causal Question |
|---|---|
| 誰が解約しそうか | Retention施策で解約はどれだけ減るか |
| どの設備が故障しそうか | 保全施策を変えると故障・停止はどれだけ減るか |
| どの設備状態が通常と異なるか | 特定の保全介入がOutcomeをどれだけ変えるか |

ただし、以下を混同しない。

- `Anomaly Score ≠ Failure Probability`
- `Failure Risk ≠ Treatment Effect`
- `High Risk設備 ≠ 特定保全施策で最も改善する設備`
- Predictive Explanation / Sensor importance ≠ Cause / Intervention Effect

## 4.3. 05-02の主例

現行Polarisでは05-02の主例をCustomer Retentionとしている。この方針は**維持を推奨**する。

理由：

- Section 04で設備保全を3枚連続で深掘りするため、Section 05冒頭まで設備だけにするとサービスScopeが設備領域に限定されて見えるRiskがある。
- Customer Retentionは `High Churn Risk ≠ High Retention Treatment Effect` を短く説明しやすい。
- 一方、重点テーマとの接続を切らないため、05-02のSupporting LogicまたはChartの補助例として、以下を1行追加することを推奨する。

```text
高Failure Risk設備 ≠ 保全施策によるFailure削減効果が最大の設備
```

すなわち、**主例はCustomer Retention、並行例としてMaintenance**という役割分担を推奨する。

# 5. Section 05で崩してはいけないScientific boundary

Section 04に設備テーマが追加されても、因果推論の定義・分析責務は変更しない。

- Causal QuestionはTreatment、Outcome、Population、Time、Contrastを明示する。
- EstimandをEstimatorより先に定義する。
- IdentificationとEstimationを分ける。
- RCT / A-B Testと観測研究の仮定を同一視しない。
- Confounder / Mediator / Colliderを無差別に調整しない。
- DAGを真の因果構造の自動発見装置として扱わない。
- Diagnosticsで未観測交絡等のIdentification Assumptionを証明できると表現しない。
- Causal MLはIdentification Assumptionを不要にしない。
- Effect Estimateや統計的有意差だけをPoC成功基準にしない。

設備保全の例を追加する場合も、`故障予測のFeature重要度 → 原因 → 保全施策` という短絡を置かない。

# 6. Section 05以降への番号波及

3枚追加により、旧Slide 28以降も+3する。

| 旧Slide | 新Slide | 現行役割 |
|---:|---:|---|
| 28 | **31** | 分析実装の基本方針とAriadneの位置づけ |
| 29 | **32** | 予測分析PoCの適用イメージ |
| 30 | **33** | 因果推論PoCの適用イメージ |
| 31 | **34** | PoC開始までの進め方 |

したがって、資料総枚数は **31枚 → 34枚** となる。

# 7. 00_README_handoff.mdへの波及

資料全体SSOTである `handoffs_service_slide/00_README_handoff.md` には、次の変更が必要である。

1. 「31枚」の記述を「34枚」へ更新する。
2. 全スライド表へSlide 14〜16の重点テーマ3枚を追加する。
3. 旧Slide 14〜31を+3して新Slide 17〜34へ更新する。
4. セクション別役割を以下へ更新する。
   - 11–20：Predictive
   - 21–30：Causal
   - 31：実装方針
   - 32–33：適用イメージ
   - 34：PoC開始
5. Predictiveの説明に「当チームの重点テーマとして故障予測・異常検知を深掘る。ただし異常検知と将来Outcome予測の意味論は区別する」を追加する。
6. Predictive Scientific constraintへ `Anomaly Score ≠ Failure Probability` を追加する。

**注意:** Section 05修正完了時点で、このREADME更新を残したままにすると、SSOTのSlide Mappingと実ファイルが不一致になる。05-*の番号移行と同一作業単位で更新・検証すること。

# 8. 後続スライドへの内容面の波及

## 8.1. 予測分析PoCの適用イメージ

旧Slide 29（新Slide 32）が現在Customer Churn中心の場合、Section 04で故障予測・異常検知を重点テーマ化したため、例の整合性を再評価すること。

選択肢は2つある。

- **A. Customer Churnを維持**：Domain breadthを優先する。
- **B. 故障予測へ変更**：重点テーマとの一貫性・営業訴求を優先する。

現時点では自動的にBへ変更しない。Slide 32の役割が「具体的なPoCイメージ」なのか「重点テーマのCase Study」なのかを確認して決めること。

## 8.2. 因果推論PoCの適用イメージ

旧Slide 30（新Slide 33）も、Section 04のMaintenance focusを受けて設備保全のTreatment Effect例を採用する余地がある。ただしPredictive / Causalの両適用イメージを同一業務課題で対にすると比較は明確になる一方、資料全体のDomain breadthは狭くなる。

したがって、Slide 32–33の例選定は別途意思決定すること。

# 9. 修正時チェックリスト

- [ ] 05-00 Slide Mappingが21〜30になっている。
- [ ] 05-01〜05-10のHeading番号が21〜30になっている。
- [ ] 05-*内部の前後Slide参照も+3されている。
- [ ] 05-01 EntryがSlide 20のMaintenance bridgeを受けている。
- [ ] 05-02で `Failure Risk ≠ Treatment Effect` を必要に応じて補助例として扱っている。
- [ ] Customer Retention主例を維持する場合、Maintenance focusとの役割分担が説明できる。
- [ ] `Anomaly Score ≠ Failure Probability ≠ Treatment Effect` の意味論を崩していない。
- [ ] 旧Slide 28〜31を新Slide 31〜34へ更新している。
- [ ] 00_README_handoff.mdの総枚数・全体表・Section範囲を34枚構成へ更新している。
- [ ] 各Transitionを再取得して、Deck全体で番号飛び・重複がないことを確認している。

# 10. 完了条件

Section 05修正は、単に番号を+3した時点では完了としない。

以下をすべて満たして完了とする。

1. Section 04の `Failure Risk / Anomaly → Maintenance Decision` から、Section 05の `Treatment → Counterfactual Outcome Difference` への問いの切替が明確である。
2. Predictive / DetectionとCausal Effectの意味論が混同されていない。
3. 05-00、05-01〜05-10、00_README_handoff.md、後続Slide番号が一致している。
4. Deck総枚数が34枚として一貫している。
5. Section 05の既存Polaris（Estimand → Assumptions / Identification → Estimation → Diagnostics / Sensitivity → Evidence Stack）は変更されていない。
