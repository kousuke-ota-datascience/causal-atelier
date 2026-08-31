Document title: 予測分析PoCの成果物とGo / No-Go

# 16. Slide 16｜予測分析PoCの成果物とGo / No-Go

## 16.1. Message

**予測PoCではモデルだけでなく、利用条件・誤り方・業務適用範囲まで成果物化し、本番化の可否を判断する。**

## 16.2. Chart

**チャートタイトル:** Predictive PoC Output → Decision Gate

Messageを説明・論証するための主たる視覚表現として、以下の構造を採用する。

### 16.2.1. Chart Structure

- 既存の論理フロー／概念図を主チャートとして用い、要素間の関係・順序が一目で追える構造にする。

```text
成果物
・Prediction Question / Data Assessment
・Baseline / Candidate Models
・Holdout Performance / Calibration
・Error Analysis / Explainability
・適用範囲・制約
        ↓
GO / ADDITIONAL VALIDATION / NO-GO
        ↓
本番化・データ追加・設計見直し・終了
```

**PowerPoint上の配置・強調**

- 上段に成果物5点、中央にDecision Gate、下段に次アクションを置く。
- Goだけを緑にせず、追加検証も正当な選択肢として並列に示す。
- No-Goを失敗ではなく合理的判断として扱う。

### 16.2.2. Chart内の最小表示テキスト

実際のPowerPoint上では、以下のラベル・短文を中心に表示する。Supporting Logicの全文をスライド上へ掲載しない。

- 成果物
- ・Prediction Question / Data Assessment
- ・Baseline / Candidate Models
- ・Holdout Performance / Calibration
- ・Error Analysis / Explainability
- ・適用範囲・制約
- GO / ADDITIONAL VALIDATION / NO-GO
- 本番化・データ追加・設計見直し・終了

## 16.3. Supporting Logic

- Go：現行Baselineに対する有意義な改善があり、重要Segmentでも性能が許容範囲にある。
- Go：予測結果を受ける業務Actionが明確で、推論時に必要データを利用できる。
- Additional Validation：データ期間・対象数・外部環境が不足し、追加検証で判断可能性が高い。
- No-Go：必要性能に届かない、leakageを除くと性能が成立しない、Actionへ接続できない等。
- 本番化時にはmonitoring、retraining、drift対応等を別途設計する。

- 補足論点：**予測PoCの成果は「モデルファイル」ではなく、本番利用可否を判断できるEvidence Packageである。**

## 16.4. Speaker Note

PoCで本番運用すべてを証明する必要はない。何が成立し、何が未検証かを明示して次フェーズへ接続する。

## 16.5. Slide 16からSlide 17への接続

> **次章では、介入効果を扱う因果推論PoCへ移る。**
