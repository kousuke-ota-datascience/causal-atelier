# 23_90_interface_verification


---

## 9. Interface verification観点

- `analysis_family`の値集合が`EXPLORATORY / CAUSAL / PREDICTIVE`で一意である。
- `AnalysisSpecification`にnavigation-only fieldが追加されていない。
- CLI/library/backend executionがNavigation metadata readなしで成立する。
- runtime `StageType`とNavigation Stage IDが別type/namespaceとして扱われる。
- Worker claimが`Execution.lease_owner / lease_expires_at`をauthorityとし、存在しないpublic claim resourceを前提にしない。
- Result / Annotation / Artifactのpublic pathとresponse fieldが本文contractと一致する。
- Findings / Model Managementのread surfaceが§11〜12で定義したResult / Annotation / Artifact / Lineage responsibilityを利用し、UI名だけの重複Resourceを作らない。
- Navigation route changeがExecution / StageExecution stateを変化させない。
- Project Management routeとAnalysis routeが別authorityとしてdirect-link / reload / Back / Forwardを復元できる。
- Analysis Contextは既存Project/Context/Dataset/Analysis View contractを再利用し、専用persistent/API resourceを要求しない。
- Dataset Version変更時のincompatible Analysis View deselectionをclient/application stateで扱い、Family/Stage routeを書き換えない。
- `GET /api/v1/navigation/analysis`が`analysis-navigation/1`のfrozen catalogを返す。
- AnalysisView type mismatchが`FILTER_TYPE_MISMATCH`を返す。
- required idempotency key missingが`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestが409 `IDEMPOTENCY_CONFLICT`となる。
- VIEWERがexplicit sensitive prediction/local-explanation detailへアクセスできない。
- `StageAttempt.effective_random_seed`と`runtime_version_json`がreproducibility contractを満たす。
- `DEFERRED` interface（general AuditLog/retention/object-store等）をcurrent mandatory acceptanceへ混ぜない。
