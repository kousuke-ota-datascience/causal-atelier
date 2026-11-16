# 30_37_predictive_model_management

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

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
