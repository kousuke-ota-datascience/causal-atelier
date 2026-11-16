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


## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-175（SPLIT）

- 旧要件に含まれるIF固有情報：Data Qualityはdedicated backend operationを新設せずread-only availabilityとして扱い、Comparisonの`TIME_TREND`は既存grouping/aggregation semanticsを維持し、Findingsの`CHART`は既存persistent operation/result/artifact semanticsを維持する
- RDの要求核／Legacy Trace：探索のデータ品質・時間推移・Findingを既存意味で利用できる
- `FR-175`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-150（SPLIT）

- 旧要件に含まれるIF固有情報：既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する
- RDの要求核／Legacy Trace：既存の予測機能・入力検証・保存済み仕様の意味を維持する
- `FR-150`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-107（SPLIT）

- 旧要件に含まれるIF固有情報：操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す
- RDの要求核／Legacy Trace：操作の可否と不可理由を一貫した権限・状態に基づいて表示できる
- `FR-107`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-108（SPLIT）

- 旧要件に含まれるIF固有情報：AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる
- RDの要求核／Legacy Trace：分析仕様・実行・結果・Graphへ文脈を保持して直接移動できる
- `FR-108`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.5. FR-130（SPLIT）

- 旧要件に含まれるIF固有情報：Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる
- RDの要求核／Legacy Trace：現在の分析Familyと画面位置を識別・復元できる
- `FR-130`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.6. FR-133（MOVE_BD）

- 旧要件に含まれるIF固有情報：FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する
- RDの要求核／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-133`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.7. FR-136（SPLIT）

- 旧要件に含まれるIF固有情報：canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる
- RDの要求核／Legacy Trace：分析ページのURLから対象Project・Family・画面位置を復元できる
- `FR-136`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.8. FR-144（MOVE_BD）

- 旧要件に含まれるIF固有情報：concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する
- RDの要求核／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-144`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.9. FR-159（SPLIT）

- 旧要件に含まれるIF固有情報：supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない
- RDの要求核／Legacy Trace：旧分析画面から正規の分析画面へ一意に遷移できる
- `FR-159`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.10. FR-163（SPLIT）

- 旧要件に含まれるIF固有情報：`/projects`をProject Listのcanonical surfaceとする
- RDの要求核／Legacy Trace：Project一覧へ一意の正規画面からアクセスできる
- `FR-163`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.11. FR-164（SPLIT）

- 旧要件に含まれるIF固有情報：`/projects/new`をProject Registerのcanonical surfaceとし、作成成功後は`/projects/{new_project_id}/overview`へ遷移する
- RDの要求核／Legacy Trace：Project作成後に対象Projectの概要画面へ遷移できる
- `FR-164`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.12. FR-165（SPLIT）

- 旧要件に含まれるIF固有情報：`/projects/{project_id}/overview`をselected Projectのdefault canonical surfaceとし、`/projects/{project_id}`はhistory-replaceでoverviewへnormalizeする
- RDの要求核／Legacy Trace：対象Projectの標準表示画面を一意に復元できる
- `FR-165`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.13. FR-171（SPLIT）

- 旧要件に含まれるIF固有情報：Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う
- RDの要求核／Legacy Trace：分析画面で選択Projectを確認でき、Project変更は管理機能で実施できる
- `FR-171`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.14. AR-024（SPLIT）

- 旧要件に含まれるIF固有情報：Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない
- RDの要求核／Legacy Trace：因果効果の結果閲覧・利用と推定器の設定操作を混同せず、区別して利用できる
- `AR-024`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)
