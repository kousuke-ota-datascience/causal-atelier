# Section 01 Story｜サービス全体像と Why Us

## Polaris

**当チームは、予測分析で「将来の見通し」を、因果推論で「施策の効果」を判断材料として提供し、業務の意思決定へ接続する。分析は業務課題と「何を知り、何を決めたいか」から選び、問いに合う分析設計・非定型課題への柔軟な実装・Enterprise利用条件の考慮を一つのPoCとして提供する。**

## このセクションの役割

- 読み手に、当チームが提供するPredictive / Causal PoCの全体像を最初に理解してもらう。
- Predictive / Causalの違いを手法名ではなく、**問い・推論対象・成立条件・評価・Decisionへの利用方法**の違いとして整理する。
- 分析結果の価値はモデルやEffect Estimateそのものではなく、Decision / Actionを変えることでBusiness Outcomeへ接続する点にあることを示す。
- 最後に、当チームへ依頼する理由を `Specialist Analytics × Enterprise Base` として提示し、後続のPoC設計章へつなぐ。

## Storyline

1. **当チームは、意思決定に異なる2種類の判断材料を提供する。**
   - Predictive：**何が起こりそうか？** → 将来・未知のOutcomeの見通し → 計画・配分・優先順位等の判断。
   - Causal：**何をするとどう変わるか？** → Treatment / InterventionによるOutcomeの変化 → 施策の実施・継続・変更等の判断。
   - 両者はともに業務意思決定へ接続するが、提供するEvidenceの意味が異なる。

2. **サービス選択は、業務課題だけでなく「何を知りたいか」から決める。**
   - 同じ「解約を減らしたい」「不良を減らしたい」「配送遅延を減らしたい」という課題でも、Riskを知りたいのか、介入効果を知りたいのかで必要な分析は異なる。
   - Algorithmや手元Dataから分析を決めるのではなく、Business Questionを具体的なAnalysis Questionへ落とす。

3. **Predictive / Causalは、問いだけでなく成立条件と評価基準が異なる。**
   - Predictive：未知データでも関係が再現することが重要で、Out-of-sample performance、Calibration、Error Pattern等で評価する。
   - Causal：観測された比較を介入効果として解釈できるIdentification Assumptionが必要で、推定値だけでなくAssumption、Uncertainty、Diagnostics / Sensitivityを評価する。
   - **高い予測精度 ≠ 正しい介入効果。** Feature importanceやSHAPも原則として因果効果を意味しない。

4. **分析価値は、結果を使ってActionを変えることで発現する。**
   - Predictive：将来Risk / 状態を予測 → 対象・時期・対応を変える → 対応効率、品質、Cost等の改善へ接続。
   - Causal：施策効果を推定 → 施策・対象・配分を変える → ROI、品質、Process等の改善へ接続。
   - Business Outcomeは分析結果から直接発生せず、Decision Rule、業務制約、運用実装等を介する。案件固有の効果量はPoC前に保証しない。

5. **当チームの価値は、分析専門性とEnterprise利用条件を一つのPoCに統合することにある。**
   - **問いに合う分析を選ぶ**：Predictive / Causalを顧客の問いから使い分ける。
   - **非定型課題にも合わせる**：Scratch +成熟OSSを用い、特定Productや単一Algorithmへ課題を合わせない。
   - **利用段階まで見据える**：Data / System / Security / Operation / Governance等のEnterprise Contextを必要に応じてPoC段階から考慮する。
   - 3つを束ねるPositioningは **Specialist Analytics × Enterprise Base**。

## Must Keep｜編集で崩してはいけない境界

- PredictiveとCausalを優劣関係として見せない。異なる問いに答える補完的な分析である。
- 「予測上重要な変数 = 操作すべき原因」「高Risk対象 = 施策効果が大きい対象」と解釈しない。
- Business Outcomeを分析サービスの直接成果として保証しない。`Analysis Result → Decision / Action → Business Outcome` の経路を保持する。
- 解約・設備・物流等の例はConcept Anchorであり、サービスScopeを特定Domainへ限定しない。
- `Specialist Analytics × Enterprise Base` は有力なPositioning仮説であり、競合優位を無条件に断定しない。
- Ariadneや特定技術をサービス選択の起点にしない。技術はQuestion / Decisionへ答える手段である。

## Slide Mapping

| Slide | Story上の役割 | Core Claim |
|---|---|---|
| 01-01 | サービス全体像 | 将来の見通しと施策効果を業務意思決定へつなげる |
| 01-02 | サービス選択基準 | 業務課題と「何を知りたいか」からPredictive / Causalを選ぶ |
| 01-03 | 両分析の境界 | 推論対象・成立条件・評価基準が異なる |
| 01-04 | 顧客価値 | 分析結果をActionへ利用してBusiness Outcomeへ接続する |
| 01-05 | Why Us | 問い起点の分析、柔軟な実装、Enterprise Contextを統合する |

## 編集時の判断基準

- 各スライドは、`サービス理解 → 選択基準 → 科学的な違い → Business Value → Why Us` の論理を一段ずつ前進させる。
- 手法詳細、PoC工程、個別評価指標は後続章へ送り、Section 01ではサービスの意味と発注価値の理解を優先する。
- 新しい例を追加する場合も、Predictive / Causalの意味論差を明確にでき、特定DomainへのScope誤認を生まないものを優先する。

## Section Transition

**サービスの全体像と選択基準を示した後は、「その分析PoCで何を検証し、分析結果をどのDecision / Actionへ利用可能にするのか」を具体化する。Section 02では、Decision起点のPoC設計へ進む。**
