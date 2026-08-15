# ENH-E7 G04 Source Confirmation

**目的:** G04 Gate contract freeze 前提の source confirmation（current checkout: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`）  
**実施範囲:** Planning / Requirements / Design artifact が source confirmation へ defer した項目のみ。Product/test code は変更していない。

## 結論

- deferred source-confirmation item は **AR-E7-09** と **AR-E7-10** の 2 件である。
- 2 件とも current source / tests / config と矛盾しない。G04 に API・schema・persistence・新 operation の追加変更は不要。
- **source semantic blocker はない。**
- ただし、`G04/README.md` と `06/07` は既に `FROZEN` と表示される。したがって「freeze 前」という手続状態を要求するなら、これは source fact ではなく operator/document-state の矛盾であり、本記録で freeze を再実行・変更する権限はない。

## Deferred item inventory

| ID | deferred source confirmation | origin |
| --- | --- | --- |
| AR-E7-09 | `Data Quality`、`TIME_TREND`、`CHART` の final placement または explicit deferred behavior | `01_enhancement_concept_and_requirement_revision_plan.md` §9; `02_target_architecture_decision_record.md` |
| AR-E7-10 | Persistence/API change が不要であることの source-based confirmation | 同上 |

`02_target_architecture_decision_record.md` は AR-E7-09 を G02 freeze 用に CONFIRMED と記録している。本書では、G04 freeze 判断に必要な current checkout の再確認だけを行う。

## AR-E7-09 — Exploratory stage / operation mapping

### Facts

- `src/ariadne/product/application/navigation_catalog.py` の Exploratory catalog は `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` を stage として持つ。
- `src/ariadne/capabilities/exploratory/planner.py` の許可 operation は `PROFILE`, `DISTRIBUTION`, `ASSOCIATION`, `GROUP_SUMMARY`, `TIME_TREND`, `CHART` だけであり、`DATA_QUALITY` operation は存在しない。
- `src/ariadne/capabilities/exploratory/runners.py` は `TIME_TREND` を `GROUP_SUMMARY_RESULT`（schema `exploratory-time-trend-result/1`）として生成する。入力には valid grouping と互換な aggregation を要求するが、時刻型、時間順序、トレンドモデルを検証・推定しない。
- 同 runner は `CHART` を `CHART_RESULT` として生成し、`CHART_SPECIFICATION` artifact を `application/vnd.vegalite.v5+json` で生成する。
- `frontend/app.js` は `data-quality` を既存 `DATA_PROFILE_RESULT` の read-only availability 表示とし、未存在時は `NO_PROFILE_RESULT` と Profile への遷移だけを提供する。Comparison は `GROUP_SUMMARY` と `TIME_TREND`、Findings は `CHART` を許可する。
- `tests/product/test_enh_e7_g02_p04_exploratory_stage_surface_migration.py`、`test_exploratory_contract_e3.py`、`test_exploratory_api_worker_e2e_e3.py` を含む focused suite は **13 passed** だった。

### Actual behavior

| 対象 | current behavior |
| --- | --- |
| Data Quality | execution/preview API を呼ばない。保存済み Profile result の可用性情報を read-only 表示する。 |
| TIME_TREND | grouping/aggregation による既存 Exploratory execution。結果種別は `GROUP_SUMMARY_RESULT`。 |
| CHART | 既存 Exploratory execution。`CHART_RESULT` と永続 artifact `CHART_SPECIFICATION` を生成する。 |

### Design recommendation

- G04 は上記 mapping を presentation/routing re-integration の protected behavior として維持すること。
- `DATA_QUALITY` operation、時間順序/時刻型/トレンドモデルの新 semantics、client-only chart state は導入しないこと。
- G04 implementation に **追加変更は不要**。既存 G04 AC-G04-12 の operation regression と P03/P05 の existing-binding regression で十分である。

### Freeze blocker

- なし。source と test の証拠は mapping を一意に確定する。

## AR-E7-10 — API / persistence change necessity

### Facts

- API application は既存 router を `/api/v1` 配下に登録し、Projects、workspace lifecycle、dataset versions、exploration、results、navigation 等の既存 endpoints を提供する。
- frontend は既存 API を使用して Project resource、`/workspace-state` の GET/PUT、Dataset Version、Analysis View、Exploration execution/result を操作する。G04 が必要とする route/state re-integration のための新 API 呼出しは source 上要求されない。
- current migration inventory の最新 revision は `20260813_product_0011_enh_e5_reproducibility.py` である。
- `git diff --name-only 1beea1c9eb3ffa5d01f7c266b826e52136d01e8f..HEAD -- product_migrations alembic_product.ini src/ariadne/interfaces/web_api src/ariadne/product/persistence src/ariadne/product/domain` は空である。
- したがって、この Enhancement の baseline から current HEAD まで、API/router・domain/persistence・migration には変更がない。

### Actual behavior

- Project ID は Project route または Analysis route から frontend state に復元され、Project-scoped resources と workspace state は既存 API で取得/更新される。
- Explorer result/artifact は既存 persistence/domain model を通じて保存され、Result/Lineage 側で参照可能な既存 result identity を持つ。

### Design recommendation

- G04 は frontend route restore、history、selected state、既存 API binding の再結合に限定すること。
- migration、schema、API contract、backend domain/operation の追加・変更は禁止範囲のまま維持すること。
- G04 implementation に **追加変更は不要**。

### Freeze blocker

- なし。現行 API/persistence は G04 が再結合する existing behavior を支える。これは「全 API が将来の任意の機能にも十分」という一般化ではなく、G04 scope に限った結論である。

## Discovery prompt の周辺 source facts（deferred item に関係する範囲）

- Project route authority は `frontend/project_navigation.js` であり、`/projects`、`/projects/new`、`/projects/<id>`→overview、4 local sectionsを parse/serialize する。
- Analysis route restore は `frontend/app.js` の `AnalysisNavigation.parse` / `applyAnalysisNavigation` が先行し、URLの project ID を用いて current Project を取得する。`popstate` は `restoreProjectRoute` に接続される。
- G03 の top-level root ownership は `frontend/top_level_surface_activation.js` にあり、Projects、Project Management、Analysis の 3 root を排他的に activate する。
- Project metadata、Dataset Version、Analysis View の DOM handler は `frontend/app.js` にあり、いずれも Project-scoped existing API を使用する。
- Results / Lineage は Analysis routing action から `results` workspace へ遷移する既存 Project Management section であり、Analysis stage-local result と同一 UI owner ではない。
- Browser harness は `tests/browser_e2e/run_enh_e7_project_integration.py`、Family/Stage harness は `tests/browser_e2e/run_enh_e6_family_stage_navigation.py` に存在する。G01/G02/G03 の protected product tests も `tests/product/test_enh_e7_*` に存在する。
- Git fact: remote=`causal-atelier`、branch=`feature/ariadne_mvp_e7`、HEAD=`cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`。

## Non-deferred current defect boundary

`ProjectNavigation.parse('/')` は root route を parse しない。G04 06 が AC-G04-01 として `/`→`/projects` normalization を要求する理由は current source で裏付けられる。この修復は G04 P01 の既存 scope であり、AR-E7-09/10 から追加された requirement ではない。

## Final freeze assessment

### Facts

- deferred items AR-E7-09/10 に未解決の source fact はない。
- G04 primary contract files は current checkout ですでに FROZEN と記録される。

### Design recommendation

- G04 contract は AR-E7-09 の既存 operation mapping と AR-E7-10 の no-API/no-persistence policy を変更せずに使用する。

### BLOCK decision

- **Source-confirmation blocker: NO**。
- **Procedural caveat:** 「freeze 前」を厳密な前提とする場合、既存 `FROZEN` 表記との不整合を operator が解決すべきである。これは未解決の product/source semantics ではない。
