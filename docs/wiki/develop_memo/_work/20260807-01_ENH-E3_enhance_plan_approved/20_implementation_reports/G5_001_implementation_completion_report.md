# ENH-E3 G5 Trial 001 Implementation Completion Report

Gate: G5 Explain + Predictive UI

Trial: 001

Status: READY_FOR_TEST

Implementation base commit: `5b41affe599614f47a51ddf1ec32b528aa132b6a`

Implementation completed commit: `cb0f45164fe5190af37df466af70057b89b8c8cb`

Handoff report commit: omitted because this report is contained by that commit

Migration head: `20260807_product_0005` (unchanged; migration execution not performed)

Working tree summary: implementation commit後は、実装対象外であるuntracked control document `06b` / `07b`と、untracked `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template_complete/`だけが残存

## G5 start evidence

- G4 Trial 003 Gate Decision: PASS
- Tested G4 implementation commit: `a8b656b463b2f8251eff8006538d04ad5af83918`
- G4 handoff report commit: `28c57400a2966568975698297eb7554ce51af80c`
- G4 Trial 003 reports `001`〜`013`: 全項目PASS
- Full active pytest evidence: `174 passed, 4 skipped`
- PostgreSQL / migration evidence: clean upgrade、single head `20260807_product_0005`、Predictive API/Worker persistence `3 passed`
- Final G4 PASS evidence HEAD at G5 start: `5b41affe599614f47a51ddf1ec32b528aa132b6a`

## Implemented scope

1. `predictive.explain.v1`をregistered Stage Runnerとして追加した。
2. frozen model / TRAIN-fitted frozen preprocessor / explicit TEST explanation dataset / fixed explanation specification / sampling definitionを検証する。
3. `LINEAR_COEFFICIENT_CONTRIBUTION`について、変換後feature orderに対応するglobal coefficient explanationとdeterministic local contributionを生成する。
4. classification contributionの`model_output_scale=LOG_ODDS`と予測の`prediction_output_scale=PROBABILITY`を分離して保存する。
5. method、TEST provenance、sampling、TRAIN background metadata、global/local explanation、warnings、limitationsを`PREDICTIVE_EXPLANATION_RESULT`とArtifactへ保存する。
6. 未対応methodは近似値を生成せず`NOT_APPLICABLE`とし、sample shortfallは`GENERATED_WITH_WARNINGS`で明示する。
7. intended use、deployment population、Dataset / optional Analysis View snapshot、feature set、split、model、hyperparameters、validation/test metrics、limitations、warnings、runtime metadataを含む`MODEL_CARD_RESULT`とArtifactを生成する。
8. Model CardからSpecification、Dataset / Analysis View、Split、Preprocessor、Model、Evaluationへのlineageを保存する。
9. multi-result StageのArtifactを対応Resultへ関連付けるため、`ArtifactDraft.result_type`をoptional shared contractとして追加し、不明Result typeを永続化時にrejectする。
10. `/projects/{project_id}/predictive`にBackend capability主導のPredictive Workspaceを追加し、Context / Dataset / View / Task / Features / Split / Training / Evaluation / Error Analysis / Explanation / Model Card / status / Artifact referenceを表示する。
11. `/context`、`/data`、`/explore`、`/causal`、`/predictive`、`/results`の6 routeを認識するProjectShellと、Predictive deep link / reload / browser backを実装した。
12. UI、Result、JSON Artifactで`Predictive Explanation is not a Causal Explanation or Treatment Effect.`を明示し、Predictiveの一般結果名に`effect`を使用していない。
13. G4互換性のため、空の`explanation_spec`は既存4-stage Planを維持し、明示された非空specだけが5番目のEXPLAIN Stageを追加する。

## Changed production files

- `frontend/app.js`
- `frontend/index.html`
- `frontend/styles.css`
- `src/ariadne/capabilities/predictive/__init__.py`
- `src/ariadne/capabilities/predictive/explanation_runner.py`
- `src/ariadne/capabilities/predictive/planner.py`
- `src/ariadne/capabilities/predictive/training_runners.py`
- `src/ariadne/capabilities/predictive/validation.py`
- `src/ariadne/product/application/predictive_workflow_service.py`
- `src/ariadne/product/workflow/contracts.py`

## Changed test files

- `Dockerfile.browser-e2e`
- `tests/browser_e2e/run_enh_e3_predictive.py`
- `tests/product/test_predictive_api_worker_e2e_e3.py`
- `tests/product/test_predictive_explanation_e3.py`
- `tests/product/test_predictive_frontend_contract_e3.py`
- `tests/product/test_predictive_split_api_e3.py`

## Added migration

- なし。既存generic persistenceで保存できるため、migration headは`20260807_product_0005`のまま。

## Architecture guard check

- Generic Executorは変更しておらず、静的監査で`predictive` tokenは0である。
- Product DomainからWeb Framework、ORM、ML library、legacy packageへの依存は追加していない。
- Product / Web APIの`ariadne.legacy` importは静的監査で0である。
- Family-specific explanation validation / computationはPredictive Capabilityに置いた。
- `ArtifactDraft.result_type`はmulti-result StageのArtifact associationをFamily分岐なしで表現するために不可避なshared interface変更である。default `None`の末尾optional fieldであり、既存constructorと従来の「Stage先頭Resultへ関連付ける」挙動を維持する。
- TEST explanation datasetは`selection_allowed=false`かつ`explanation_only=true`であり、TRAIN / PREPARE / tuningへTESTを戻すbindingは追加していない。
- 未対応methodではglobal/local explanationを`None` / emptyに固定し、曖昧なfallback値を作らない。
- G6のcross-family score、full lineage/export、Context / Results最終機能は実装していない。

## Known deviations

- なし。

## Known limitations

- G5の説明methodは、既存のlogistic / linear regression registryに対する`LINEAR_COEFFICIENT_CONTRIBUTION`だけである。
- Context routeとResults routeの最終機能、および全6 route共通selectorの完成は指示書どおりG6へ残している。
- G5 Browser E2Eは専用scriptを追加したが、Coding Agentは実行していない。
- Coding Agentはpytest、scientific benchmark、PostgreSQL、migration upgrade/downgradeを実行していない。

## Files intentionally excluded

- migration files
- G6 cross-analysis lineage / comparison / export codeとtest
- `00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`
- `00_enhance_plan_documents/07b_Ariadne_ENH-E3_テスト指示書.md`
- `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template_complete/`

## Required Test Agent focus

1. strict explanation specification、TEST-only dataset、sampling contract
2. 5-stage Plan登録、frozen model / preprocessor validation、4-stage G4互換性
3. deterministic global/local explanation、LOG_ODDS / PROBABILITY尺度、sampling provenance / warning
4. unsupported methodの`NOT_APPLICABLE`と非近似保証
5. Model Cardの必須fieldとSpecification / Dataset / optional View / Split / Preprocessor / Model / Evaluation lineage
6. Explain Stageの2 Artifactが各Resultへ正しく関連付くこと
7. Backend capabilitiesがPredictive button enablementの正本であること
8. Predictive Workspaceの全表示項目とTerminology Guard
9. Predictive routeのdeep link / reload / browser back
10. G1〜G4回帰、full active suite、PostgreSQL persistence、single migration head

Test execution by Coding Agent: NOT PERFORMED

Static implementation checks:

- changed Python 12 files: AST parse success
- `frontend/app.js`: `node --check` success
- `frontend/index.html`: parse success、103 ID unique
- G4 empty explanation Plan: `split -> prepare -> train -> evaluate` PlanValidator success
- G5 explicit explanation Plan: `split -> prepare -> train -> evaluate -> explain` PlanValidator success
- Generic Executor family token / Product-Web legacy import audit: 0 violations
- `git diff --check`: clean
