# Section 02 Story｜Decision起点のPoC設計

## Polaris

**分析PoCは、モデルやEffect Estimateを作ること自体ではなく、誰が何を決めるのかを起点に必要なEvidenceとAnalysis Questionを逆算し、分析結果を業務Actionへ変換する利用ルールまで設計したうえで、分析成立性・業務利用性・次フェーズ判断を検証する。**

## このセクションの役割

- PoCの目的を「分析ができるか」から「意思決定に使えるEvidenceを作れるか」へ拡張する。
- Business Questionを、そのまま分析仕様に変換せず、DecisionとRequired Evidenceを経由してAnalysis Questionへ落とす。
- 分析結果を業務で利用するための `WHO / WHEN / Decision Rule / Action` をPoC段階で仮説として設計する。
- Section 03のPoC共通プロセスへ渡す入力条件を定義する。

## Storyline

1. **PoCで検証するのは3つである。**
   - **分析成立性**：対象Questionに対し、妥当な結果を再現可能に得られるか。
   - **業務利用性**：分析結果をDecision / Actionの判断材料として利用できるか。
   - **次フェーズ判断**：本番化、追加検証、追加Data取得、Scope変更、中止等をEvidenceに基づいて判断できるか。
   - よってPoC成果は「良いモデル」や「有意な効果」そのものではなく、**何が分かり、何がまだ分からず、次に何を判断できるか**で捉える。

2. **分析設計はDecisionから逆算する。**
   - `Business Question → Decision → Required Evidence → Analysis Question` の順で具体化する。
   - Business Questionは改善したいOutcomeを示すが、Analysis Targetを一意に決めない。
   - 同じ課題でも、対象選択・優先順位付けにはPrediction、施策実施・継続判断にはCausal Effectが必要になる場合がある。
   - Decisionは設計アンカーだが、Data、Assumption、業務制約と整合しなければScope自体を見直す。

3. **Analysis Resultは、そのままActionではない。**
   - 結果を実務で使うには、`WHO / WHEN → Analysis Result → Decision Rule → Action` を定義する。
   - **WHO**：誰が結果を使うか。
   - **WHEN**：いつ使うか。Prediction Horizonや施策Decisionの時点と整合させる。
   - **Decision Rule**：Threshold、Ranking、Effect、不確実性、業務Cost、Capacity等をどう判断へ変換するか。
   - **Action**：対象、施策、配分、時期、追加Review等のうち何を変えるか。

4. **PoC段階で利用ルールを置くのは、本番仕様を固定するためではない。**
   - 分析結果が業務判断へ使える条件を検証可能にするための仮説として置く。
   - Offline Evaluation / Simulationで確認できる範囲と、実際にActionを変えないと確認できない範囲を分ける。
   - Dashboard / API / Batch等は配送手段であり、`WHO / WHEN / Decision Rule / Action` 自体が業務接続の本体である。

## Must Keep｜編集で崩してはいけない境界

- 「業務課題 → 手法」へ直接ジャンプしない。必ずDecision / Required Evidenceを介する。
- Decisionを先に置くことは、初期Decisionを無条件に固定することではない。Data・Assumption・Feasibilityに応じたScope見直しを許容する。
- PredictionのThresholdやCausalの有意差を、そのまま業務Decision Ruleとみなさない。
- 分析結果を表示するUIを作ることと、業務利用設計を同義にしない。
- Business Outcome改善をPoCのOffline分析だけで証明したことにしない。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 02-01 | PoC目的 | 分析成立性・業務利用性・次フェーズ判断まで検証する |
| 02-02 | Analysis Question設計 | 誰が何を決めるかからRequired Evidenceを逆算する |
| 02-03 | 利用設計 | WHO / WHEN / Decision Rule / ActionまでPoCで設計する |

## 編集時の判断基準

- 各スライドは `PoCで何を検証するか → 何のDecisionのための分析か → 結果をどうActionへ使うか` の順で詳細化する。
- Predictive / Causal固有の評価方法は共通概念の例示に留め、詳細は各分析章へ送る。
- 新しい項目を追加するときは、それが「Decisionから分析要件を逆算する」「分析結果を利用可能にする」のどちらに寄与するかを明確にする。

## Section Transition

**Decision、Required Evidence、Analysis Question、利用ルールを定義したら、それらをPoC全体の工程へ組み込む必要がある。Section 03では、業務設計から分析検証を経て業務判断へ戻る共通プロセスと、その開始・終了条件を定義する。**
