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

**Decision:** historical mega-runnerを全体修理してそのままcanonical regressionへ昇格しない。必要scenarioはcurrent journeyへdistillする。

**Rationale:** historical runnerにはstale navigation/DOM assumptionや過去Enhancement間dependencyが混在するため。

## D004 — Canonical Browser E2Eは少数のjourney-oriented suiteとする

**Decision:** 将来的なBrowser regressionはproject lifecycle、analysis navigation、causal critical journey、predictive critical journey等の少数critical journeyへ収束させる。

**Rationale:** Browser E2Eの責務はcross-layer connectivity proofであり、詳細なsemantic/scientific correctnessは主としてdeterministic lower layerで保証する。

## D005 — Enhancement固有testはEnhancement provenanceを保持する

**Decision:** 新規・変更testは原則 `tests/enhancement/<enhancement>/<gate>/<layer>/...` へ配置する。

**Rationale:** 新しいtest lifecycle architectureを今後のEnhancementから段階的に適用するため。

## D006 — Migration/cutover testはsemantic extractionする

**Decision:** `migration`, `cutover`, `cleanup`, `legacy shutdown` 等を主identityとするtestを、そのままregressionへ移さない。

**Rationale:** durable current invariantとhistorical transition proofが混在し得るため。

## D007 — Scientific benchmarkは別authority classとして維持する

**Decision:** repeated scientific/statistical acceptance benchmarkは通常regression hierarchyとは分離する。

## D008 — Legacy archiveはdefault collection外を維持する

**Decision:** `tests/legacy_archive/` はhistorical evidence areaとして維持し、通常pytest collectionから除外する。

## D009 — Fixture migrationは後段で行う

**Decision:** shared `conftest.py` / fixture体系の全面再編はENH-E9で行わない。

**Rationale:** pytest fixture scopeはpath-sensitiveであり、repository-wide migrationとして別途扱うべきである。

## D010 — Test Architecture Migrationと各Gate provenanceを分離する

**Decision:** 本migrationは特定GateのCandidate remediation、Acceptance Criteria変更、frozen verification contract変更を目的としない。

## D011 — ENH-E9はminimum must migrationに縮小する

**Decision:** ENH-E9ではrepository全体のtest estateを再認証しない。E9で実際に使用・変更するtestからbatch単位で新体系へ移行する。

**Rationale:** comprehensive migrationを完了しなくてもEnhancement実装・verification自体は継続可能であり、test estate整理を理由にE10/E11等のfeature roadmapを長期間blockしないため。

## D012 — Comprehensive Test Code MigrationはENH-E12以降へdeferする

**Decision:** E1-E8を含む既存test全件の再認証、canonical regression再構築、historical Browser runner統廃合、旧directory撤去等はENH-E12以降の独立Enhancementで実施する。

**Rationale:** これはfilesystem cleanupではなくrepository-wide Test Architecture Reconciliationであり、独立Enhancement相当の作業量・verification責務を持つ。

## D013 — 未判定testはarchiveせず現状位置を許容する

**Decision:** 「現Enhancementで使わない」だけを理由に `legacy_archive` へ移さない。Historical / supersededと確認できたものだけarchiveする。Current invariantか未判定の既存testは旧位置に残してよい。

**Rationale:** `legacy_archive` はdefault collection外であり、未判定testをarchiveするとcurrent regression coverageを黙って失う危険がある。

## D014 — E10/E11へ過渡期test estateをhandoffする

**Decision:** ENH-E10 / E11開始時に、test architectureが段階移行中であること、new testsの推奨配置、historical Browser runnerの扱い、test-side drift発生時の対処をhandoffする。

**Rationale:** comprehensive migration完了前でも各Enhancementを安全に進めるため。

## D015 — Generic enhancement workflow templateには過渡期事情を埋め込まない

**Decision:** `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/README.md` にAriadne repository固有の「過渡期test code体系」を記載しない。

**Rationale:** generic workflow templateのnormative contractと、現在のrepository固有migration debtを分離するため。
