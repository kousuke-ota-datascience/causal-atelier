Document title: 標準分析 × Enterprise接続 の競争ポジション

# A01-04c. Appendix｜標準分析 × Enterprise接続

## A01-04c.1. Message

**分析が標準化し実装比重が高い案件では、SIer型Deliveryの重要性が高まる。**

## A01-04c.2. Chart

**チャートタイトル:** Deal Profile別Positioning｜標準分析 × Enterprise接続

### A01-04c.2.1. Chart Structure

```text
Deal Profile
────────────
Analytical Complexity   Low〜Medium
Implementation Coupling High
Problem Novelty         Low〜Medium
Standardizability       Medium〜High
Criticality             Medium〜High
        ↓
重視されるSelection Criteria
────────────
Delivery Feasibility
Risk
Organizational Acceptability
Economic Value
Capability / Quality
        ↓
Provider Position
────────────
SIer Analytics          強みが出やすい
当チーム               Competitive
Consulting Analytics    条件次第
AI / Platform Vendor    Product Fit次第
DS Specialist           相対的にFit低下
```

### A01-04c.2.2. Chart内の最小表示テキスト

- 低〜中Analytical Complexity
- 高Implementation Coupling
- **SIer Analyticsが有力になりやすい**
- **当チーム：Competitive**

## A01-04c.3. Supporting Logic

### A01-04c.3.1. このProfileの特徴

モデルや分析手法自体は比較的標準的で、主な難所がSystem Integration、Data Pipeline、Security、Operation、Production Reliability等へ移る案件。

### A01-04c.3.2. ProviderごとのFit仮説

- **SIer Analytics**：Integration / Production / Security / Operationの比重が高いほど構造的にFitしやすい。
- **当チーム**：SIer内分析組織として適合するが、Predictive / Causalや非定型分析の専門性が選定理由として効きにくい。
- **Consulting Analytics**：TransformationやGovernanceが大きい場合は競争可能だが、Pure Delivery中心では追加価値が限定される場合がある。
- **AI / Platform Vendor**：標準Productへ高くFitするなら強い。Product外のIntegration範囲が広いとSIer型Capabilityが必要になる。
- **DS Specialist**：分析部分では対応可能でも、Enterprise Delivery比重が高まるほど他Capabilityへの依存が増える。

### A01-04c.3.3. 当チームのPosition

> **Competitive。ただし当チーム固有の分析専門性による差別化は弱まりやすい。**

このProfileでは、当チームはSIer Analyticsの一員として十分競争可能だが、01-05で訴求する`Specialist Analytics × Enterprise Base`のうちSpecialist Analytics側の付加価値が小さくなる。

## A01-04c.4. Speaker Note

分析手法が比較的標準化され、難所が本番SystemやOperationへ移るほど、競争の中心はSIer型Deliveryになります。当チームも対応できますが、この場合は高度分析の専門性が決定的な差になりにくいため、Why Usの中心領域とは言いにくくなります。

## A01-04c.5. 次頁への接続

> さらに標準化可能性が高まり、既製Productへ問題を載せやすくなると、競争軸は別の方向へ移る。