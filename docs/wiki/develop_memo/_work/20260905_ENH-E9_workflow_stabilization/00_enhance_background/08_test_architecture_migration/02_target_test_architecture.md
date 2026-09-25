# 目標テストアーキテクチャ

**状態:** `PROPOSED_BASELINE`  
**Scope:** filesystem organization / test lifecycle policy

## 1. 目標filesystem

```text
tests/
├── regression/
│   ├── unit/
│   │   ├── causal/
│   │   ├── predictive/
│   │   └── scientific/
│   ├── contract/
│   │   ├── architecture/
│   │   ├── causal/
│   │   ├── predictive/
│   │   └── scientific/
│   ├── integration/
│   │   ├── api/
│   │   ├── worker/
│   │   ├── persistence/
│   │   └── execution/
│   ├── frontend/
│   │   ├── project/
│   │   ├── navigation/
│   │   ├── causal/
│   │   └── predictive/
│   └── browser_e2e/
│       ├── run_project_lifecycle.py
│       ├── run_analysis_navigation.py
│       ├── run_causal_critical_journey.py
│       └── run_predictive_critical_journey.py
│
├── enhancement/
│   └── <enhancement>/
│       └── <gate>/
│           ├── unit/
│           ├── contract/
│           ├── integration/
│           ├── frontend/
│           └── browser_e2e/
│
├── characterization/
│   └── scientific/
│
├── benchmarks/
│   └── scientific/
│
├── support/
│   ├── fixtures/
│   ├── factories/
│   └── helpers/
│
└── legacy_archive/
```

## 2. 直交する分類軸

### Lifecycle / authority axis

- `regression` — 現在のauthoritative product behaviorとして恒久的に守るもの
- `enhancement` — 開発・verification中のEnhancement delta
- `characterization` — hard regression contractではない観測的・scientific characterization
- `benchmarks` — repeated scientific/statistical acceptance benchmark
- `support` — fixtures / factories / helpers。独立assertionではない
- `legacy_archive` — retired historical tests。通常collection対象外

### Verification-layer axis

- `unit`
- `contract`
- `integration`
- `frontend`
- `browser_e2e`

各testはまずlifecycle / authority上の責務を持ち、その内側でverification layerに分類する。

## 3. Regressionの定義

`tests/regression/` は「過去にpassしたtestをすべて保存する場所」ではない。

Regression testは **現在のauthoritative behavior** を表現する。Intentional Enhancementによってnavigation、API shape、内部architecture等が変わった場合、旧実装形状を維持するのではなく、新しいcurrent contractを表すようregressionを再記述する。

Failureを通すためだけのexpectation弱体化は禁止する。Driftは以下に分類する。

| Drift type | Required action |
|---|---|
| Intended specification change | 承認済みcurrent contractへregressionを更新 |
| Product violates existing contract | productを修正し、regressionは弱めない |
| Implementation/DOM/navigationのみ変更しsemanticsは同じ | harness / locator / route表現を更新 |
| Old specification retired | decisionを記録した上で旧regressionを置換・削除 |

## 4. Enhancement test lifecycle

新規・変更behaviorは以下から開始する。

```text
tests/enhancement/<enhancement>/<gate>/<layer>/
```

GateまたはEnhancementの安定化後、各testに以下のdispositionを与える。

```text
PROMOTE      -> current invariantをregressionへ昇格
REWRITE      -> semanticsを維持しつつhistorical/temporary structureを置換
MERGE        -> 重複assertionをcanonical regressionへ統合
SPLIT        -> current invariantとmigration/history assertionを分離
RETIRE       -> 不要になったtemporary assertionを終了
ARCHIVE      -> historical evidenceとしてactive regression外に保存
```

Promotionはsemanticな判断であり、単純file moveとは限らない。複数のEnhancement-specific testsを少数のcanonical regressionへdistillしてよい。

## 5. Browser E2E policy

Browser E2Eはcritical cross-layer user journeyに限定する。詳細なcorrectnessはdeterministicなlower layerをprimary proofとする。

初期canonical Browser regression候補:

1. `run_project_lifecycle.py`
   - Project List -> New Project -> overview/context/data/results -> return/history
2. `run_analysis_navigation.py`
   - Project -> analysis family/stage navigation -> direct entry/reload/back-forward
3. `run_causal_critical_journey.py`
   - dataset/fixture -> Discovery -> candidate -> comparison -> adopt/fix -> persisted observable result
4. `run_predictive_critical_journey.py`
   - dataset/fixture -> predictive setup/run -> result -> persisted observable result

Historical Enhancement acceptance runnerはscenario抽出元であり、恒久authorityではない。

## 6. ENH-E9への適用

ENH-E9では、各Gate由来testを以下の原則で整理する。

```text
tests/enhancement/enh_e9/<gate>/<layer>/...
```

特定Gateのtestだけを対象とするのではなく、G01-G05を含むENH-E9全体のtest lifecycleを同じ規則で扱う。既にPASS済みのGateであっても、恒久regressionへ昇格すべきか、Enhancement provenanceとして保持すべきか、retire/archiveすべきかを明示的に判定する。

## 7. Migration invariants

Migrationは以下を維持しなければならない。

- filesystem cleanupのみを理由とするproduct semantic changeを行わない;
- recorded dispositionなしにcurrent authoritative assertionを弱体化・削除しない;
- test architecture workを特定Gateのproduct remediationと混同しない;
- activeなGate candidateやfrozen contractをmigration都合で遡及変更しない;
- `legacy_archive` はdefault pytest collection外を維持する;
- scientific benchmark executionを独立識別可能に保つ;
- fixture resolution / pytest markersを維持する;
- file move時はDocker / CI / Browser runner path referenceをatomicに更新する。
