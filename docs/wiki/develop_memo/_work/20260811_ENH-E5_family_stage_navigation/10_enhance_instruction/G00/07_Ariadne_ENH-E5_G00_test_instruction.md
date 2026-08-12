# Ariadne ENH-E5 G00 — Family / Navigation Stage Domain Contract — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G00`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `a4d96b33c81b5a263a2e82e6d64475de5085b616`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


## 1. Verification claim

Navigation catalog/APIがexact、self-contained、runtime-independent、non-persistentであることを独立検証する。

### Canonical Navigation Catalog

| family | slug | default_stage_id | stages in deterministic order |
|---|---|---|---|
| `EXPLORATORY` | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| `PREDICTIVE` | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| `CAUSAL` | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

Canonical metadata response fields:

```text
schema_version = "analysis-navigation/1"
families[].family
families[].slug
families[].label
families[].default_stage_id
families[].stages[].stage_id
families[].stages[].slug
families[].stages[].label
families[].stages[].order
```

Required invariants:

- Family descriptorは`EXPLORATORY / PREDICTIVE / CAUSAL`各1件。
- Family slugはglobalに一意。
- `stage_id / slug`はFamily内で一意。
- `default_stage_id`は当該FamilyのStage内に存在。
- Stage orderはdeterministic。
- `stage_id == slug`をENH-E5 canonical valueとする。
- runtime input/output/status/retry/attempt/leaseをNavigation metadataへ含めない。
- Navigation descriptorをpersistent Domain Resource、Repository、UoWへ登録しない。
- `analysis-navigation/1`をscientific generic `SchemaRegistry`へ登録しない。Navigation metadataはdedicated interface/application validationで検証する。
- catalogからruntime `StageType / StageDefinition / StageExecution`を生成しない。


## Acceptance Criteria

- `AC-G00-001`: canonical Familyはexisting `AnalysisFamily.EXPLORATORY / PREDICTIVE / CAUSAL`のみ。
- `AC-G00-002`: `GET /api/v1/navigation/analysis`がHTTP read-only metadata endpointとして存在する。
- `AC-G00-003`: response top-level fieldは`schema_version`であり、値は`analysis-navigation/1`。`schema`へのrenameは禁止。
- `AC-G00-004`: Stage identity fieldは`stage_id`。generic `id`へのrenameは禁止。
- `AC-G00-005`: canonical metadata response field set、3 Family slug/default/catalogが本文のexact値に一致する。
- `AC-G00-006`: Family exactly-once、global Family slug uniqueness、Family-local Stage ID/slug uniqueness、default membership、deterministic orderをvalidateする。
- `AC-G00-007`: duplicate Family / blank ID or slug / duplicate Stage ID or slug / empty stages / invalid defaultをrejectする。
- `AC-G00-008`: Navigation metadataへruntime input/output/status/retry/attempt/leaseを混入しない。
- `AC-G00-009`: Navigation descriptorをpersistent Domain Resource/Repository/UoWへ登録せず、Navigation導入のDB migrationを行わない。
- `AC-G00-010`: runtime planner/runner/CLI/libraryはNavigation catalog/default/sidebar orderなしでcurrent executionを成立させる。
- `AC-G00-011`: `analysis-navigation/1`をscientific generic `SchemaRegistry`へ登録しない。


## 3. Verification architecture

- API: exact endpoint、`schema_version`、nested field names、Family catalog/default/order。
- unit: Family/Stage invariantとreject case。
- architecture/static: Navigation descriptorのRepository/UoW登録禁止、runtime Stage生成依存禁止。
- persistence: Navigation導入由来のDB migrationがない。
- regression: planner/executor/worker/CLI/libraryがNavigation metadataなしでcurrent execution可能。

## 4. PASS / FAIL

全ACに独立evidenceがあり、`schema`/`id`等のfield drift、runtime coupling、persistent navigation追加が0件の場合のみPASS。
