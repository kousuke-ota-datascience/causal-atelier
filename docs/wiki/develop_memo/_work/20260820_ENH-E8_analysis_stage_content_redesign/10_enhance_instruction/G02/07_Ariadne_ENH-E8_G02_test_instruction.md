# Ariadne ENH-E8 G02 Verification Contract

- Document class: Primary Execution Contract / Acceptance Authority
- Verification contract status: `FROZEN`
- Status: `FROZEN`
- Gate: `G02`

## Entry identity audit

Trial Implementation Completion Reportに記録されたexact Fixed Trial Candidate SHAだけを検証する。

mutable/uncommitted candidateは`BLOCKED`とする。

## Acceptance Criteria

| AC | Criterion | Primary layer |
|---|---|---|
| G02-AC01 | canonical Family/Stage catalogとrouteが変更されていない | contract/integration |
| G02-AC02 | current Stageがprimary Stage Contents identityであり、legacy `Inference` が競合current-stage headingとして表示されない | frontend contract |
| G02-AC03 | Causal presentation groupingがnon-routable/non-persistent/non-runtimeである | frontend + diff audit |
| G02-AC04 | Identificationのpositive/negative visibilityが責務に一致する | frontend DOM/integration |
| G02-AC05 | Estimationのpositive/negative visibilityが責務に一致する | frontend DOM/integration |
| G02-AC06 | EffectsとDiagnosticsがdistinct primary surfaceである | frontend DOM/integration |
| G02-AC07 | Refutation/Sensitivity control/resultがSensitivityのみのownerであり他Stageではnon-interactive | frontend DOM/integration |
| G02-AC08 | affected Causal Stageに責務と整合する日本語中心のpurpose guidanceがある | frontend contract/review |
| G02-AC09 | Predictive 6 Stageのpurpose/result ownershipが指定どおり分離される | frontend DOM/integration |
| G02-AC10 | Predictive Setup feature selectorがselected Dataset Version schemaからcandidateを取得しcheckbox multi-selectionを提供する | frontend DOM/state |
| G02-AC11 | selector Cancelはnon-mutating、Confirmはchecked columnをdeterministic orderでcommitする | frontend state |
| G02-AC12 | confirmed selector valueがnew spec field/versionなしにexisting `predictive-analysis-spec/1.feature_spec.feature_columns` semanticsへserializeされる | regression/integration |
| G02-AC13 | Dataset Version変更でnew schemaに存在しないfeature nameをsilent保持しない | frontend state |
| G02-AC14 | Trainはselected draft/spec feature setをread-only表示しeditable selectorを持たない | frontend DOM/state |
| G02-AC15 | Predictはselected executionのrecorded feature setをread-only表示しeditable selector/ad-hoc scoring operationを持たない | frontend DOM/integration |
| G02-AC16 | feature interaction以外のexisting Predictive spec/default/validation/submission semanticsが維持される | regression/integration |
| G02-AC17 | valid Predictive draft（confirmed feature selection含む）がStage切替で保持される | state/frontend |
| G02-AC18 | selector logicをshare/generalizeした場合、existing Causal Discovery selector/request behaviorが維持される | protected regression |
| G02-AC19 | major semantic sectionがvertical flowで、supported desktop/narrow viewportでsection composition起因のpage-level horizontal overflowがない | DOM/CSS + browser |
| G02-AC20 | G01 PASS済みparent navigationが維持される | protected regression |
| G02-AC21 | API/persistence/backend/runtime semantic changeおよびLightGBM/LIME/SHAP追加がない | diff/architecture/protected regression |
| G02-AC22 | direct link/reload/Back/ForwardでStage restorationがdeterministic | navigation integration + Browser E2E |
| G02-AC23 | selector trigger/dialog/checkbox/Confirm/Cancelがkeyboard操作とaccessible-name要件を満たす | accessibility/frontend |

## Required lower-level selector verification

Independent Verificationで直接確認する。

1. Dataset A schemaからDataset Aのcolumn candidateだけが生成される。
2. Dataset/schemaなしでは明示的unavailable stateとなり、架空columnを生成しない。
3. existing confirmed feature listがopen時にchecked stateへ復元される。
4. pending change + Cancelでconfirmed draft/specが変わらない。
5. pending change + Confirmでdeterministic checked-column listになる。
6. Dataset A -> Dataset B変更でBにないcolumnをsilent保持しない。
7. Setup -> Train -> Setupでvalid confirmed feature selectionを保持する。
8. same logical feature listがbaseline form serializerと同一 `feature_spec.feature_columns` semanticsになる。
9. Train/Predictにeditable selectorがない。
10. shared selector導入時、Causal Discovery open/Confirm/Dataset-change/request-validation testがgreen。

## Browser E2E critical journey

1. Causal:
   - Identification -> Estimation -> Effects -> Diagnostics -> Sensitivity
   - current headingとwrong-stage primary control absenceをkey transitionで確認
2. Predictive:
   - selected Dataset Version付きSetupへ入る
   - feature selectorをopen
   - 複数featureを選びConfirm
   - Setup -> Trainへ遷移しread-only feature contextを確認
   - repositoryのcanonical harnessが許す形でexisting Predictive executionを使用/実行
   - Predictでexecution-recorded feature setがread-onlyであることを確認
   - Metrics -> Explainability -> Model Managementへ進む
   - Stage identityとdraft/state continuityを確認

詳細visibility / selector state correctnessはdeterministic lower-level testをprimary proofとし、Browser E2Eはcross-layer journey proofに限定する。

Canonical Browser E2E commands:

Causal journey:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py
```

Predictive journey:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py
```

Environment/bootstrap authority:

- Compose: `compose.yaml` + `compose.e1a.yaml`
- profile: `e2e`
- service: `browser-e2e`
- browser: Playwright Chromium
- default web URL: `ARIADNE_E2E_WEB_URL=http://127.0.0.1:8080`
- evidence root: `ARIADNE_E2E_OUTPUT_DIR` または `test-results/browser_e2e`
- current-source imageを`--build`で生成し、`--rm`でephemeral runnerを使用する
-各scriptはAPI/frontend/execution等のsemantic ready stateを待機し、fixed sleepだけをsynchronization authorityにしない

## Final decision

blocking ACとapplicable protected regressionがすべてPASSした場合のみPASS。

harness/environment inabilityは`BLOCKED`、valid candidateのproduct mismatchは`FAIL`。
