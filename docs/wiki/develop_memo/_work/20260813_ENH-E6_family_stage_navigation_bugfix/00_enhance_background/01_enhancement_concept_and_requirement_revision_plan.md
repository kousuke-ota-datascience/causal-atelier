# ENH-E6 Enhancement 構想・要件改定計画

- 状態: `APPROVED / G01 CONTRACT FROZEN`
- 対象branch: `bugfix/ariadne_mvp_e6`
- Planning baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Source anomaly: `ANOM-E5-001`

## 0. 結論

ENH-E6 は ENH-E5 G01 をやり直す enhancement ではなく、E5 closeout で分離された observable UI anomaly を回収する bugfix enhancement とする。

修正対象は単なる Family tab の表示処理ではない。canonical Family/Stage Navigation Context を変更・復元・表示する transition lifecycle を一元化し、通常導線、Family/Stage click、deep link、reload、browser history、legacy analytical navigation の全てを同じ authority へ収束させる。

## 1. Problem statement

### 1.1 Intended behavior

Analysis画面では次の3 Familyを tab で切り替える。

- `EXPLORATORY`
- `PREDICTIVE`
- `CAUSAL`

Familyを切り替えると、そのFamilyのdefault Navigation Stageへ遷移し、Stage sidebarはcurrent Family固有のStageだけを表示する。

### 1.2 Baseline implementation fact

source inspection では以下を確認した。

- `frontend/index.html` に `analysis-family-tabs` と `analysis-stage-sidebar` がある。
- `frontend/app.js` に `renderAnalysisNavigation()` があり、backend catalog から Family tabs と current Family stages をrenderする。
- Family click / Stage click handler は canonical route を push し `restoreProjectRoute()` を呼ぶ。
- `restoreProjectRoute()` の canonical analysis route branch は `renderAnalysisNavigation()` を呼ぶ。
- 一方 `activateWorkspace()` は legacy workspace / left-nav activationを担い、Navigation Context とURLを変更し得るが `renderAnalysisNavigation()` を呼ばない。
- `ANALYSIS_WORKSPACES` は `causal: 'discovery'` と Family 単位でpresentation workspaceを固定する。

### 1.3 Root-cause classification

| Layer | Root cause | Classification |
|---|---|---|
| Direct | normal workspace transition が Navigation Shell render lifecycle を通らない | frontend integration defect |
| Structural | Navigation Context / URL / selected UI / presentation activation を複数関数が個別に操作する | state transition authority fragmentation |
| Structural | `(family, stage)` ではなく Family 単位で legacy workspace を選ぶ経路が残る | presentation binding defect |
| Verification | source existence test が observable user journey の代替になった | acceptance coverage defect |

## 2. Enhancement objective

1. Family/Stage navigation state transition authorityを一元化する。
2. canonical URL、`state.navigationContext`、Family tab selected state、Stage sidebar selected state、presentation surfaceをatomicに同期させる。
3. legacy analytical left navigationをprimary state authorityから外し、canonical Family/Stage routeへのcompatibility entryに限定する。
4. Causal Family内の Discovery系surface と Inference系surface のbindingをStage単位で定義する。
5. real browser critical journeyで observable regression をblocking verificationする。

## 3. Scope

### In scope

- `frontend/app.js` navigation lifecycle / presentation binding
- 必要に応じた `frontend/navigation_state.js` のpure transition helper
- legacy analysis navigation compatibility mapping
- Family/Stage shell visibility/selected semantics
- current analysis presentation activation
- product tests / browser E2E regression
- ENH-E5 G01 protected behavior regression

### Out of scope

- Navigation catalog schema変更
- `AnalysisFamily` canonical values変更
- backend scientific operation semantics変更
- runtime `Execution Stage`へのNavigation Stage混入
- new analysis algorithms
- broad UI redesign
- Results / Lineage 等 non-analysis workspace のIA再設計

## 4. Constraints / invariants

- `Navigation Stage != Execution Stage`
- backend navigation catalog remains Family/Stage catalog authority
- Navigation ContextをDomain Resource / Executionへpersistしない
- E5 frozen evidenceを改変しない
- Family/Stage navigation errorをsilent fallbackしない
- test green化のためのassertion weakening / skipは禁止

## 5. Legacy navigation decision

legacy left navigation の analytical entries は **compatibility shortcut** とする。選択後の authority は canonical Family/Stage navigationへ委譲する。

| Legacy entry | Canonical compatibility target | Rationale |
|---|---|---|
| Explore / exploratory entry | `exploratory/profile` | E5 legacy normalization と一致 |
| Predictive | `predictive/setup` | E5 legacy normalization と一致 |
| Causal Discovery | `causal/discovery` | entry label の semantic intent を保持 |
| Causal Inference | `causal/identification` | current inference surface は Identification を先に行い、その後 Estimationへ進む。canonical Causal stage orderでも inference-phase の先頭が identification |

`Causal Inference -> causal/identification` は compatibility entry point であり、「Inference = Identification」というdomain equivalenceを定義しない。Estimation / Effects / Diagnostics / Sensitivity はStage sidebarから明示選択する。

## 6. Presentation binding decision

Familyだけでworkspaceを決定する `ANALYSIS_WORKSPACES` 型のbindingをcanonical authorityにしない。

E6では `(familySlug, stageSlug)` から current presentation surface を決める binding layer を持つ。

最小互換surface mapping:

| Family | Stage | Existing presentation surface |
|---|---|---|
| exploratory | all current exploratory stages | `explore` workspace（stage-specific detailは既存renderer semanticsを保持） |
| predictive | all current predictive stages | `predictive` workspace |
| causal | `setup`, `discovery` | `discovery` workspace |
| causal | `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` | `inference` workspace |

これはE6で既存surfaceを再利用するためのpresentation bindingであり、Navigation Stageをruntime operationへ1:1 aliasするものではない。

## 7. Gate decomposition

1 Gate とする。

### G01 — Observable Family / Stage Navigation Integration

PASSすると、どのsupported entry pathからでも canonical Navigation Context と observable analysis navigation / presentation が一貫し、後続作業は Family/Stage navigation のreal user behaviorへ依存できる。

## 8. Execution mode

`WORK_PACKAGE` を提案する。

- P01: navigation transition authority / lifecycle integration
- P02: stage-aware presentation binding + legacy compatibility
- P03: observable browser regression + static/unit regression strengthening

## 9. Planning completion condition

- source anomaly provenance がE5 ledgerまでtrace可能
- requirement / design / current source alignmentが明示
- legacy nav responsibilityが決定
- Causal Discovery / Inference compatibility entryが決定
- G01 06/07 が self-contained draft
- Browser E2Eをblocking critical journeyとして07へ具体化
