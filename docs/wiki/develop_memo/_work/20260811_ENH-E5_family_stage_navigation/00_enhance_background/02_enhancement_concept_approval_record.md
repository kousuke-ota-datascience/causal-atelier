# ENH-E5 Enhancement Concept Approval Record

- 状態: `PLANNING_DECISIONS_FROZEN / CODING_BLOCKED_UNTIL_NFR019_PASS`
- Planning pin: `46122c68333df03680b97c253a7b5d32bf9393e7`
- Alignment baseline: `a770cc4f38137063cd5f22d8035e91e3c63b7502`
- Phase H updated: `2026-08-12` (Asia/Tokyo)

## 0. Approval conclusion

ENH-E5 planningで必要なproduct/architecture/remediation decisionはfreeze済みである。

ただし、これはCoding開始承認を意味しない。`10/21/22/23/30`改訂とNFR-019再監査PASS前に`06/Pxx/07`をfinal freezeしてはならない。

## 1. Product concept approval

以下を承認済みbaselineとする。

1. Familyはglobal analytical contextである。
2. Application model上のFamilyは`EXPLORATORY / PREDICTIVE / CAUSAL`である。
3. 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用する。
4. Navigation StageはFamily-local work/view contextである。
5. `Navigation Stage != Execution Stage`をcritical invariantとする。
6. concrete Navigation Stage catalogはFamily Capabilityが所有する。
7. current Family/StageのauthorityはURL/Application stateでありDBへpersistしない。
8. Predictive existing settings / generated specification / execution semanticsを100%保持して再配置・拡張する。
9. LightGBM / DoWhy / EconMLはENH-E5へ含めない。

## 2. Navigation architecture approval

### 2.1 Navigation descriptor

Navigation metadataはruntime `StageType / StageDefinition`とは別のdescriptor/value modelとする。

禁止:

- Navigation Stageをruntime `StageType`へ1:1対応させる。
- Navigation Stageを`AnalysisSpecification`へpersistする。
- Navigation catalogからruntime Stageを生成する。
- CLI/library/backend execution inputへNavigation Stageを必須化する。

### 2.2 Catalog authority

採用:

```text
GET /api/v1/navigation/analysis
```

response schema:

```text
analysis-navigation/1
```

ownership:

```text
Family capability descriptor
    ↓
application/interface aggregator
    ↓
read-only metadata endpoint
```

Frontendはfull catalogのduplicate ownershipを持たない。

`analysis-navigation/1`はscientific generic `SchemaRegistry`へ登録しない。

### 2.3 Canonical route

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Default Stage:

| Family | slug | default_stage_id |
|---|---|---|
| EXPLORATORY | `exploratory` | `profile` |
| CAUSAL | `causal` | `setup` |
| PREDICTIVE | `predictive` | `setup` |

Legacy routeを残す場合はdefault Stageへ一方向normalizeする。

### 2.4 Resource deep route

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

E5 resource types:

- `analysis-specification`
- `execution`
- `result`
- `graph-version`

## 3. D1 / D2 / D3 remediation approval

remediation baseline:

| Decision | Count | Meaning |
|---|---:|---|
| D1 | 31 | current implementationをcurrent canonical contractとして採用 |
| D2 | 35 | ENH-E5 target |
| D3 | 28 | ENH-E5では実装せずFUTUREへ延期 |

D1/D2/D3はMUST/SHOULD/MUST NOTとは別軸である。

### 3.1 Final D3 explicit approval

2026-08-12、Human ownerは以下4 Decision ItemをENH-E5では実装せず`D3 / FUTURE`へ送ることを明示承認した。

- `FR-122` — General operational audit trail
- `FR-126` — Configurable retention/deletion policy
- `D10-006a` — General Audit contract
- `D10-006b` — Retention/deletion contract

したがって、formal remediation freeze blockerは解消済みとして扱う。

## 4. Phase G D2 planning freeze approval

D2 35 Decision Itemは次の11 packageへfreeze済みである。

| Package | Title |
|---|---|
| PF-D2-01 | AnalysisView Typed Filter Validation |
| PF-D2-02 | Exploratory Handoff & Provenance |
| PF-D2-03 | Predictive Subgroup Evaluation |
| PF-D2-04 | Scientific Comparability & Exploratory-Reuse Guard |
| PF-D2-05 | Command Idempotency & Retry-safe Artifact Commit |
| PF-D2-06 | Project Authorization & Sensitive Output Boundary |
| PF-D2-07 | Canonical Lineage Completion |
| PF-D2-08 | Reproducibility Metadata Completion |
| PF-D2-09 | Frontend Deep Navigation, Action State & Accessibility |
| PF-D2-10 | Derived E5 Test Architecture |
| PF-D2-11 | Documentation Self-containment & Navigation Architecture Freeze |

Freeze status:

- D2 Decision Item: 35
- assigned: 35
- unassigned: 0
- duplicate: 0
- unresolved planning decision: 0

下流`06/Pxx`でこれらの値・scope・error semantics・algorithm・route・persistence boundaryを変更してはならない。

## 5. Requirement lifecycle approval

Requirement tableでは次を独立管理する。

```text
ID
Area
Requirement
Level
Requirement Status
Implementation Status
Delivery
```

Approved vocabulary:

- Requirement Status: `ACTIVE / DEFERRED / RETIRED`
- Implementation Status: `IMPLEMENTED / PARTIAL / NOT_IMPLEMENTED / UNVERIFIED`
- Delivery: `BASELINE / ENH-E5 / FUTURE`

D3はRequirement削除を意味しない。Requirement正本へ`DEFERRED / FUTURE`として残す。

## 6. Scope exclusions approval

ENH-E5 acceptanceへ含めない。

- LightGBM / DoWhy / EconML
- Navigation state DB persistence
- runtime Execution Stage architecture redesign
- common Stage taxonomy across Families
- general AuditLog / retention policy
- system-level Operator authorization
- object-storage adapter
- configurable sensitive-column governance
- generic Product orchestration CLI
- general resource hard-limit framework
- general p95 performance gate
- comprehensive observability overhaul
- D3に属するverification target

## 7. Approval status

| Item | Status | Note |
|---|---|---|
| Product concept | `APPROVED / FROZEN` | Family × Navigation Stage |
| Requirement lifecycle model | `APPROVED / FROZEN` | Status / Implementation / Delivery |
| D1/D2/D3 remediation | `APPROVED / FROZEN` | 94 Decision Item |
| D3 blocker 4件 | `APPROVED` | 2026-08-12 explicit human approval |
| Navigation catalog authority | `APPROVED / FROZEN` | backend read-only endpoint |
| Navigation endpoint/schema | `APPROVED / FROZEN` | `GET /api/v1/navigation/analysis`, `analysis-navigation/1` |
| Canonical route/default Stage | `APPROVED / FROZEN` | Phase G PF-D2-11 |
| D2 planning details | `APPROVED / FROZEN` | 11 packages / unresolved 0 |
| Gate map | `RETAINED` | G00〜G05; detailed assignmentはPhase K |
| Canonical docs 10/21/22/23/30 | `REVISION_REQUIRED` | Phase I |
| NFR-019 | `FAIL / REMEDIATION_REQUIRED` | Phase Jで再監査 |
| Coding contract final freeze | `BLOCKED` | NFR-019 all PASS required |
| Coding start | `BLOCKED` | 06/Pxx/07 final freeze前は禁止 |

## 8. Change control

freeze済みdecisionの変更が必要になった場合:

1. `06/Pxx`で変更しない。
2. 対応するpreflight decision recordを先にamendする。
3. Human reviewを受ける。
4. `10/21/22/23/30`へ反映する。
5. NFR-019を再監査する。
6. その後`06/Pxx/07`へ収束する。
