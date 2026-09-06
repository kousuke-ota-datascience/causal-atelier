# Migration後Verification

**状態:** `NOT_STARTED`  
**目的:** Test Architecture Migrationのclosure checklist

## 1. Structural verification

- [ ] target directoryが設計どおり存在する
- [ ] active testのownershipが `regression` / `enhancement` 間で曖昧になっていない
- [ ] ENH-E9由来testがGate/layer単位で `tests/enhancement/enh_e9/...` に整理されている
- [ ] permanent regression filenameが、明示的理由なしにhistorical Enhancement identityへ依存していない
- [ ] `tests/legacy_archive/` が通常pytest collectionから除外されたままである
- [ ] scientific benchmarkが独立識別可能である

## 2. Pytest collection / fixture verification

- [ ] default pytest collectionが成功する
- [ ] active test countをpre-migration baselineと照合済み
- [ ] path変更によりtestがsilent dropしていない
- [ ] legacy testが誤って再collectionされていない
- [ ] shared fixtureが意図したscopeからresolveする
- [ ] PostgreSQL依存testのskip / marker behaviorが維持されている
- [ ] custom markerが登録済みかつ意味を保持している

## 3. Regression verification

- [ ] unit regression suite PASS
- [ ] contract regression suite PASS
- [ ] integration regression suite PASS
- [ ] frontend regression suite PASS
- [ ] scientific deterministic regression suite PASS
- [ ] benchmark suiteがdefault blocking regressionと分離して実行可能

## 4. Enhancement verification

- [ ] `tests/enhancement/<enhancement>/<gate>/...` をGate単位で独立実行できる
- [ ] ENH-E9の各Gate由来testについてoriginal acceptance semanticsを保持している
- [ ] PASS済みGateを含め、各Enhancement-specific testにpromotion / retain / retire / archiveのdispositionが追跡可能である
- [ ] Enhancement-specific testが、明示的dispositionなしにhistorical permanent regressionとして残っていない

## 5. Browser E2E verification

- [ ] canonical `run_project_lifecycle.py` がcurrent Project lifecycleを実行する
- [ ] canonical `run_analysis_navigation.py` がcurrent family/stage navigationとhistory behaviorを実行する
- [ ] canonical `run_causal_critical_journey.py` がDiscovery -> candidate -> comparison -> adopt/fix connectivityを実行する
- [ ] canonical `run_predictive_critical_journey.py` がcurrent predictive connectivityを実行する
- [ ] canonical runnerがhistorical Enhancement runner moduleをimportしていない
- [ ] Browser assertionがobsolete internal DOMではなくsemantic observable state / canonical routeを優先している
- [ ] failure時のtrace / screenshot / log / evidence生成が維持されている

## 6. Docker / CI / command-reference verification

- [ ] `Dockerfile.browser-e2e` がcurrent canonical runner pathを参照する
- [ ] `.dockerignore` が必要なtest file/directoryを含む
- [ ] Compose / Browser execution commandがcurrent pathを使用する
- [ ] CI / workflow scriptがcurrent pathを使用する
- [ ] documentation / operator promptがarchived runner pathを実行しない
- [ ] repository searchで意図しないstale referenceが残っていない

## 7. Semantic non-regression audit

各 `SPLIT`, `MERGE`, `RETIRE`, `ARCHIVE` actionについて:

- [ ] durable current invariantにreplacement testが存在する、または
- [ ] 当該behaviorがauthoritativeではなくなった明示的rationaleがある。

Migrationが面倒であるという理由だけでassertionを消してはならない。

## 8. Gate / Enhancement provenance保護

- [ ] test architecture migrationによってactive/completed Gateのcandidate identityを遡及変更していない
- [ ] 各Gateのfrozen `07` をmigration都合で変更していない
- [ ] test harness / filesystem migration commitとproduct remediation commitを区別できる
- [ ] migration中にproduct defectを発見した場合、該当Gateの正式routeへ分離している
- [ ] 特定Gate固有のblocker resolutionを本migration全体のscopeやclosure条件として誤定義していない

## 9. Closure record

Migration execution完了後に記入する。

```text
Final migration commit(s):
Pre-migration baseline SHA:
Post-migration verification SHA:
Regression result:
Enhancement result:
Browser result:
Known residual risks:
Final status: PASS | BLOCKED | FAIL
```
