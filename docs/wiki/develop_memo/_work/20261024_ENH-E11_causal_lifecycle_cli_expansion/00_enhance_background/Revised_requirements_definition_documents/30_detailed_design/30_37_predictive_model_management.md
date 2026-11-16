# 30_37_predictive_model_management


---

### 15.7 Model Management

read-oriented model surfaceとしてResult / Artifact / Lineageを使用する。

対象:

- `TRAINING_RESULT`
- `EVALUATION_RESULT`
- `MODEL_CARD_RESULT`
- fitted preprocessor/model artifact
- Model Card artifact
- revised/rerun lineage

UI名だけを理由に別`ModelRegistry` persistent aggregateを追加しない。
