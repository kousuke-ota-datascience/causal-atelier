# Ariadne ENH-E9 G04 Implementation Instruction

**Contract status:** `DRAFT_NOT_FROZEN`  
**Execution mode:** `WORK_PACKAGE`

## Gate claim

Applicable causal diagnosticsをstable structured `DIAGNOSTICS_RESULT`としてpersistし、Frontendがparse/推測せず表示できるbackend contractを成立させる。

## Mandatory pre-authoring evidence

- baseline estimator implementation
- adapter/result persistence path
- current balance implementation
- current diagnostics Result schema/payload
- IPW/AIPW weight semantics
- applicable scientific tests
- FR-048 requirement text/status

Evidence確認前にexact field schemaをfreezeしない。

## Required semantics to address

### Effective Sample Size

IPW等applicable estimatorでstructured valueとして取得可能にする。

### Weight diagnostics

estimatorが実際に使用したanalysis weightについて、少なくともcount/min/mean/median-or-p50/p95/p99/max/extreme-weight count+ruleを検討し、scale/normalization semanticsを明示する。

### Balance

weighting前後を意味的に区別する。current unweighted balanceをafter-weightingと誤認させない。

### Estimator applicability

- difference-in-means
- OLS
- IPW
- AIPW

をmethodologically区別する。

AIPWでpropensity-derived weighting diagnosticsを保存する場合、それがweighting componentのdiagnosticでありestimator全体の単一final weightではないことをcontract化する。

## Frontend boundary

Frontendはbackendに存在しないESS/weight/weighted balanceを推測・生成しない。Effects/Diagnostics presentation frameworkはE8 protected contractとして維持する。
