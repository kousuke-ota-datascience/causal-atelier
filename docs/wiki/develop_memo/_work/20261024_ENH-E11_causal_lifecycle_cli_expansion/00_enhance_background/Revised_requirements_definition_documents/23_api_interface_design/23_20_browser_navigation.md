# 23_20_browser_navigation

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

## 4. Browser Navigation Interface

Browser Navigation Interfaceは、Web App内で**どのProject / surface / Analysis Family / Navigation Stageを表示しているか**を表すinterfaceである。Navigation Contextは正本Domain Resourceではなく、URL path、必要なclient/workspace state、既存Resource identityのcompositionとして扱う。

### 4.1 Navigation Contextの責務

Navigation Contextの責務は次に限定する。

- Project Management surfaceのroute identity
- Analysis WorkspaceのProject / Family / Navigation Stage identity
- resource deep link identity
- direct link / reload / Back / Forwardで復元可能なbrowser state
- legacy analytical entryからcanonical routeへの一方向normalization

Navigation ContextへAnalysis SpecificationやExecution条件を複製しない。分析条件・scientific stateは正本Resource/APIから取得する。

Analysis Contextは専用backend resourceではない。Current Project / Active Research Context / Dataset Version / Analysis Viewを、既存Project / Context / Dataset / Analysis View interfaceとclient/workspace stateからcompositionする。

### 4.2 Project Navigation contract

Project routes:

```text
/projects
/projects/new
/projects/{project_id}/overview
/projects/{project_id}/context
/projects/{project_id}/data
/projects/{project_id}/results
```

Short route:

```text
/projects/{project_id}
```

は`/projects/{project_id}/overview`へhistory-replace semanticsでnormalizeする。

Project routeはProject Managementのnavigation authorityであり、Analysis Family / Stage stateを所有しない。

### 4.3 Analysis Navigation contract

Canonical Analysis route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

`resource_type`:

- `analysis-specification`
- `execution`
- `result`
- `graph-version`

Analysis WorkspaceのCurrent Projectはrouteの`project_id`をauthorityとしread-onlyとする。Family切替時のdefault Stageは`GET /api/v1/navigation/analysis`の`default_stage_id`をauthorityとする。

Navigation Stageはpresentation/application stateであり、runtime `StageType` / `StageExecution`とは別contractである。

### 4.4 Browser restoration / compatibility semantics

- Project routeとAnalysis routeの双方でdirect link / reload / Back / Forwardを成立させる。
- Explicit Family/Stageとresource semantic mismatchはsilent correctionせずroute errorとする。
- Supported legacy analytical entryはcanonical Analysis routeへ一方向normalizeし、parallel route/state authorityとして維持しない。
- 旧route tokenそのものの永続的存続をcurrent contractとはしない。
- Dataset Version変更によりAnalysis Viewがincompatibleになった場合、Analysis View selectionを解除する。Family/Stage routeは書き換えない。
- context不足を補うために架空のResearch Context / Dataset Version / Analysis Viewを生成しない。

### 4.5 Presentation state vocabulary

Async presentation state vocabulary:

```text
IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED
```

このvocabularyはbrowser/presentation stateであり、Execution / StageExecution lifecycle enumの代替ではない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-175`**：Data Qualityはdedicated backend operationを新設せずread-only availabilityとして扱い、Comparisonの`TIME_TREND`は既存grouping/aggregation semanticsを維持し、Findingsの`CHART`は既存persistent operation/result/artifact semanticsを維持する
- **`FR-150`**：既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する
- **`FR-107`**：操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す
- **`FR-108`**：AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる
- **`FR-130`**：Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる
- **`FR-133`**：FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する
- **`FR-136`**：canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる
- **`FR-144`**：concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する
- **`FR-159`**：supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない
- **`FR-163`**：`/projects`をProject Listのcanonical surfaceとする
- **`FR-164`**：`/projects/new`をProject Registerのcanonical surfaceとし、作成成功後は`/projects/{new_project_id}/overview`へ遷移する
- **`FR-165`**：`/projects/{project_id}/overview`をselected Projectのdefault canonical surfaceとし、`/projects/{project_id}`はhistory-replaceでoverviewへnormalizeする
- **`FR-171`**：Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う
- **`AR-024`**：Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない
