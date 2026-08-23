# ENH-E9 申し送り: Causal Diagnostics backend result contract

## 1. 目的

Causal / Diagnostics Navigation Stage の人間向け表示を整備する過程で確認した、Frontendだけでは解消できないbackend側の不足をENH-E9後続作業へ申し送る。

Diagnostics Stageの現行詳細設計上のprimary surfaceは、`DIAGNOSTICS_RESULT`、balance、overlap、effective sample size (ESS)、weight diagnostics、scientific warningである。また要件FR-048は、estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存することを要求する。

今回のFrontend改修では、既存Resultに構造化保存済みの項目のみを人間向けに可読化する。以下の項目はbackend Result contractの補完が必要である。

## 2. 申し送り対象

| 項目 | 現状 | 必要なbackend対応 | Frontend側の暫定表示 |
| --- | --- | --- | --- |
| Effective sample size (ESS) | IPW estimator内部では`ess_treated` / `ess_control`を計算しているが、`DIAGNOSTICS_RESULT`へ構造化保存されていない | `diagnostics.weighting.effective_sample_size`等の安定したschemaへ保存する | 「現行backend Resultに構造化保存されていない」と表示 |
| Weight diagnostics | structured Resultなし | estimatorが実際に使用したweightについて、少なくともcount、min/max、quantile、mean、極端weight件数等をResultへ保存する | 未表示理由を明示 |
| Weighted / post-adjustment balance | `compute_balance_table`はweightsを受け取れるが、現行EstimationAdapterはunweighted balanceのみ保存 | IPW/AIPW等weighting estimatorではbefore / afterを区別してbalanceを構造化保存する | 現在のbalanceを`Unweighted / before weighting`と明記 |

## 3. 現行コード上の事実

### 3.1 ESS

`TreatmentEffectEstimator.ipw()` は次を計算している。

```python
ess_treated = effective_sample_size(weights_treated)
ess_control = effective_sample_size(weights_control)
```

ただし現在はnotes文字列へ埋め込まれるだけで、Product側`EstimationAdapter`の`diagnostics` dictには格納されない。

### 3.2 Weight diagnostics

Product側`EstimationAdapter`が保存するdiagnosticsは現在、正常系で概ね次である。

```text
sample_size
design
balance
overlap  # propensity estimatorの場合
```

weight summaryそのものはstructured fieldとして存在しない。

### 3.3 Weighted balance

`compute_balance_table(..., weights=None)` はunweighted SMDを返し、weightsを渡せばweighted mean / std / SMDを計算できる。しかし現行`EstimationAdapter`は次の形で呼び出しておりweightsを渡していない。

```python
compute_balance_table(complete, treatment, adjustment_set)
```

したがって現行`DIAGNOSTICS_RESULT.balance`は、IPW/AIPWであってもweighting前のbalanceである。

## 4. 推奨Result schema

既存Resultとの互換性を維持しつつ、例えば以下のような追加を検討する。

```json
{
  "sample_size": {
    "n_input": 500,
    "n_complete": 480,
    "n_treated": 245,
    "n_control": 235,
    "sample_loss": 20
  },
  "balance": {
    "before": [],
    "after": []
  },
  "overlap": {},
  "weighting": {
    "effective_sample_size": {
      "treated": 221.0,
      "control": 198.0
    },
    "weights": {
      "min": 0.5,
      "p50": 1.1,
      "p95": 3.8,
      "p99": 7.2,
      "max": 12.0
    }
  }
}
```

物理field名は既存Result schema/versioning方針に従って確定すること。全Estimatorへ同一diagnostic setを強制せず、非該当項目は「適用対象外」と判断できるcontractにする。

## 5. Acceptance観点

- IPW/AIPWの`DIAGNOSTICS_RESULT`からESSを文字列parseなしで取得できる。
- 使用weightの分布・極端値をstructured payloadから評価できる。
- weighting前後のbalanceを明確に区別できる。
- OLS等、weightingを行わないEstimatorにweight diagnosticsを捏造しない。
- `Execution.status=SUCCEEDED`とscientific diagnostic statusを混同しない。
- 既存のEffects / Diagnostics Navigation Stageとruntime ExecutionOperationの分離を維持し、新しい`DIAGNOSTICS` runtime operationを追加しない。

## 6. 今回のFrontend対応範囲

今回のFrontend改修では、既存backend Resultから取得可能な次を表示する。

- Human-readable diagnostic summary
- Estimator / Treatment / Outcome / Estimand / Adjustment set
- Sample loss
- Treated / Control count
- Covariate balance（`Unweighted / before weighting`と明記）
- Propensity overlap（適用可能なEstimatorのみ）
- Scientific warning
- 同一ExecutionのTreatment Effect Resultへのreference
- Technical details / Lineage

ESS、weight diagnostics、weighted/post-adjustment balanceは、本申し送りのbackend対応完了後にFrontend表示へ接続する。
