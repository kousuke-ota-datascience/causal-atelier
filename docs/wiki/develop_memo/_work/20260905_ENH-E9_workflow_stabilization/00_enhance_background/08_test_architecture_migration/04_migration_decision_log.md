# テストMigration Decision Log

**状態:** `OPEN`  
**Rule:** execution開始後はdecisionを追記し、過去のrationaleを黙って書き換えない

## D001 — Lifecycle authorityとverification layerを分離する

**Decision:** `tests/` は、まずlifecycle / authority (`regression`, `enhancement` 等)で整理し、その内側でverification layer (`unit`, `contract`, `integration`, `frontend`, `browser_e2e`)に分類する。

**Rationale:** 現行構造はdomain/purposeとtest layerを同一階層で混在させており、ownershipとpromotion判断が不明確である。

## D002 — RegressionはEnhancement履歴ではなくcurrent behaviorを表現する

**Decision:** 恒久regressionのfilename/directoryに、behaviorを最初に導入したという理由だけで `enh_e*` identityを残さない。

**Rationale:** regression suiteはchronological archiveではなく、現在のexecutable product contractである。

## D003 — Historical Browser acceptance runnerを恒久authorityにしない

**Decision:** `run_enh_e1a.py` を全体修理してcanonical causal Browser regression runnerへ昇格しない。

**Rationale:** historical mega-journeyとstale navigation/DOM assumptionを含む。価値のあるscenarioはcurrent canonical journeyへdistillする。

## D004 — Canonical Browser E2Eは少数のjourney-oriented suiteとする

**Decision:** Browser regressionは、project lifecycle、analysis navigation、causal critical journey、predictive critical journey等の少数critical journeyへ収束させる。

**Rationale:** Browser E2Eの責務はcross-layer connectivity proofであり、詳細なsemantic/scientific correctnessは主としてdeterministic lower layerで保証する。

## D005 — Enhancement固有testは明示的なpromotion判定までEnhancement provenanceを保持する

**Decision:** ENH-E9を含むEnhancement由来testは、まず `tests/enhancement/<enhancement>/<gate>/...` へ整理し、Gate/Enhancement stabilization後に個別dispositionを与える。

**Rationale:** promotionはtest lifecycle上の明示的判断であり、Enhancementで作成されたというだけで自動的にpermanent regressionにもtemporary testにも分類しない。

## D006 — Migration/cutover testはsemantic extractionする

**Decision:** `migration`, `cutover`, `cleanup`, `legacy shutdown` 等を主identityとするtestを、そのままregressionへ移さない。

**Rationale:** durable current invariantを含むものと、historical transitionのみを証明するものが混在するため、分離が必要である。

## D007 — Scientific benchmarkは別authority classとして維持する

**Decision:** repeated scientific/statistical acceptance benchmarkは通常regression hierarchyとは分離し、`tests/benchmarks/scientific/` で管理する。

**Rationale:** 実行cost、解釈、statistical acceptance semanticsがdeterministic regressionと異なる。

## D008 — Legacy archiveはdefault collection外を維持する

**Decision:** `tests/legacy_archive/` はhistorical evidence areaとして維持し、通常pytest collectionから除外する。

**Rationale:** 現状の隔離方式がtarget lifecycle modelと整合している。

## D009 — Fixture migrationは後段で行う

**Decision:** shared `conftest.py` とproduct fixture placementを初回migration batchで機械的に移動しない。

**Rationale:** pytest fixture scopeはpath-sensitiveであり、consumer/dependency分析前の移動はproduct/test semanticsと無関係なfalse failureを発生させ得る。

## D010 — Test Architecture Migrationと各Gateのverification provenanceを分離する

**Decision:** 本migrationは、特定GateのCandidate remediation、Acceptance Criteria変更、frozen verification contract変更を目的としない。Activeまたはcompleted Gateのcandidate/evidence identityはtest architecture整理の都合で遡及変更しない。

**Rationale:** test lifecycle / filesystem / harness architectureの整理はENH-E9横断の構造改善であり、個別Gateのproduct implementation remediationとはauthorityとprovenanceを分離すべきである。Migration中に個別Gateのproduct defectを確認した場合は、当該Gateの正式routeへ切り出す。
