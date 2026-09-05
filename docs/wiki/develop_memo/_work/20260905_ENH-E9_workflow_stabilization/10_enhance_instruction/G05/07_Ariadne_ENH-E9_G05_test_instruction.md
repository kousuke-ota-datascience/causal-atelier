# Ariadne ENH-E9 G05 Verification Contract

**Document class:** Primary Execution Contract  
**Verification contract status:** `FROZEN`

## Blocking journey

```text
Analysis Context
 -> Discovery
 -> Graph review / comparison
 -> FIXED Graph
 -> Identification
 -> Estimation
 -> Effects
 -> Diagnostics
```

## Acceptance Criteria

1. canonical Analysis route/contextからjourneyを開始できる。
2. Discovery executionとGraph review/comparison/adoption/fixがG02 semanticsで成立する。
3. FIXED Graph designated OutcomeがIdentificationへ自動/read-only継承される。
4. selected Identification Result execution lineageからEstimationを実行できる。
5. Effectsはpersisted `TREATMENT_EFFECT_RESULT`をprimary sourceとしてhuman-readableに表示する。
6. Diagnosticsはpersisted structured `DIAGNOSTICS_RESULT`をprimary sourceとし、G04 structured weighting/balance semanticsを表示できる。frontend再計算を行わない。
7. Result / Execution / Graph lineageがjourney全体で保持される。
8. Navigation Stageをruntime Execution stateとして扱わない。
9. G01–G04およびE8 protected contractsがregressionしない。

## Browser E2E policy

Canonical Compose/browser test environmentを使用し、fixtureはAnalysis ContextからDiagnosticsまで同一project lineageで到達可能なものとする。UI synchronizationはfixed sleepをprimary mechanismにせずobservable state/element conditionを使用する。Failure時はscreenshot/log/current route/visible Stage/last successful checkpointをevidenceとして保存する。

Browser E2Eはcross-layer connectivity proofであり、G04のESS/weight/balance数値correctnessはG04 unit/integration testsをprimary authorityとする。

全blocking AC PASSのみG05 PASS。
