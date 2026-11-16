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
