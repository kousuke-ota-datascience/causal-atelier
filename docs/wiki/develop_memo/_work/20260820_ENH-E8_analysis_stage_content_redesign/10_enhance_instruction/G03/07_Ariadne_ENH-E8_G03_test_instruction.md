# Ariadne ENH-E8 G03 Verification Contract

- Document class: Primary Execution Contract / Acceptance Authority
- Verification contract status: `RETROSPECTIVE_FROZEN / A01_APPLIED`
- Status: `RETROSPECTIVE_FROZEN / A01_APPLIED`
- Gate: `G03`
- Reconstruction date: `2026-08-23`
- Amendment: `09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`

## 1. Gate PASS rule

retrospective verification開始時に固定したexact repository commit SHAに対して、blocking Acceptance CriterionがすべてPASSし、protected ENH-E8 regressionがgreenの場合のみPASSとする。

environment / harness要因で判定不能な場合はproduct FAILではなく`BLOCKED`とする。

本Gateは後追い文書化であるため、過去のbugfix commitを「当時formal verification済みだった」と遡及認定しない。

## 2. Acceptance Criteria

| AC | Criterion | Primary layer |
|---|---|---|
| G03-AC01 | Estimation actionがIdentification formのnative submit ownershipから独立している | frontend contract / product test |
| G03-AC02 | hidden Identification required controlsがinvalidでもEstimation action handlerへ到達できる | Browser E2E |
| G03-AC03 | Identification Result未選択時は明示的にsubmissionを拒否する | frontend behavior / Browser E2E |
| G03-AC04 | selected Identification Resultのexecution lineageを`prefill`から復元する | product test / frontend contract |
| G03-AC05 | `dataset_version_id` / `input_graph_version_id` / `analysis_spec`をcurrent hidden form値から取得しない | product test / code audit |
| G03-AC06 | `input_result_id`がselected Identification Resultを参照する | product test / integration |
| G03-AC07 | invalid / incomplete Identification prefill lineageではsubmissionしない | frontend integration |
| G03-AC08 | submission operation / endpointが既存`ESTIMATION` execution-batch contractを維持する | product/integration |
| G03-AC09 | ENH-E8 G02のStage visibility/separation behaviorを壊さない | protected regression + Browser E2E |
| G03-AC10 | API/schema/DB/backend causal semanticsに不要な変更がない | diff / architecture audit |
| G03-AC11 | handler attachment前のEstimation buttonが`type="button"`かつdisabledで、native/shared-form submitへfallbackしない | Browser E2E / DOM lifecycle |
| G03-AC12 | app runtime declaration後、`DOMContentLoaded`を起点としてsubmission module loadを開始し、`window.load`待ちのinteraction raceを作らない | frontend contract / Browser E2E |
| G03-AC13 | canonical Compose frontend runtimeがcurrent sourceの`/causal_estimation_submission.js`をHTTP successで配信し、runtime readerからread可能である | container/runtime integration |
| G03-AC14 | regression evidenceがcurrent semantic contractを検証し、obsolete exact source-string assertionをPASS authorityにしない | test audit |

## 3. Automated regression evidence policy

Historical regression guard:

```bash
pytest -q tests/product/test_enh_e9_estimation_submission_regression.py
```

このtest filenameの`ENH-E9`はhistorical artifact identityであり、G03のenhancement identityを変更しない。

ただしA01時点では、このhistorical testは旧`const button=$('#estimation-inputs button');`および`global.addEventListener('load'`をexact source-stringとしてassertしており、current implementationに対してstaleである。

したがって、上記commandのFAILを直ちにproduct FAILとは判定しない。まずfailureがobsolete implementation-detail assertionによるものか、G03 semantic regressionによるものかを分類する。obsolete assertionの場合はtest harness defectとしてevidence化し、current semanticsを検証する更新済みtestまたは代替focused evidenceを用意するまでG03をPASSにしない。

obsolete testをgreenにする目的でcurrent implementationを旧`window.load`方式や旧button lookupへ戻してはならない。

Causal Stage Browser E2E:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py
```

## 4. Required Browser E2E observations

Browser E2Eでは少なくとも次を観測する。

1. Estimation Stageで`#run-estimation`がvisibleである。
2. hidden Identification controlsの`dataset_version_id` / `graph_version_id`がinvalidである状態を確認できる。
3. handler ready後の`#run-estimation`が`type="button"`である。
4. button activationがnative validationに遮断されず、Estimation action固有のvalidationへ到達する。
5. Identification Result未選択時に`Identification Resultを選択してください`というaction-level rejectionを観測する。
6. G02の各Causal Stageでwrong-stage primary surfacesが露出しない。

A01追加critical journeyとして、**handler loadを意図的に遅延させた状態**を観測する。

7. `causal_estimation_submission.js` responseをbrowser/network interception等で遅延させる。
8. submission module未ready期間にEstimation buttonが`type="button"`かつdisabledであることを確認する。
9. 未ready期間のclick / keyboard activationがshared form submitやIdentification native validationへfallbackしないことを確認する。
10. delayed module load完了後にbuttonがenableされ、Estimation action-level validationへ到達することを確認する。

単に最終DOMだけを観測してAC11/AC12をPASSにしてはならない。temporal pre-ready stateを観測する。

## 5. Frontend asset delivery verification

G03-AC13について、canonical Compose runtimeをbuildして次を確認する。

- frontend serviceが`Dockerfile.frontend`からcurrent sourceを含むimageとしてbuildされる。
- `/causal_estimation_submission.js`へのHTTP requestがsuccessする。
- response contentがFixed Verification Candidate内のcurrent sourceと対応する。
- nginx processがstatic fileをreadできるpermissionを持つ。
- host bind mountの偶然のpermission / local filesystem stateへ依存しない。

`Dockerfile.frontend` / `compose.yaml`の変更自体をPASS理由にせず、runtime observationをevidenceとする。

## 6. Additional lineage verification

G03-AC04〜AC08について、static contract assertionsだけで十分とみなさない。

Independent Verificationでは、可能な範囲でintegration/API evidenceまたはfocused browser scenarioを追加し、selected Identification Resultのexecution prefillからdataset / graph / analysis specが復元され、`ESTIMATION` execution batch requestへ渡ることを確認する。

この追加観測が現行test harnessでは構成不能な場合、理由と未検証範囲をevidenceへ明記する。blocking ACを観測できない場合は`BLOCKED`とし、推測でPASSにしない。

## 7. Fixed Verification Candidate identity

verification開始直前にrepositoryのexact commit SHAを取得し、A01適用済みG03 Trial01のFixed Verification Candidateとしてevidenceへ記録する。

verification中にcandidateが変化した場合、その結果を同一candidateのPASS evidenceとして使用しない。

## 8. Protected regression

少なくとも次を保護する。

- ENH-E8 G01 Project return navigation
- ENH-E8 G02 Causal Stage content separation
- existing Identification submission behavior
- existing execution-batch API contract
- canonical Compose API/backend startup behavior

## 9. Test Agent prohibited work

Test Agentはverification中に次を行わない。

- product code修正
- Acceptance Criteriaの緩和
- hidden Identification controlsの再表示等によるworkaround
- historical evidenceの改変
- ENH-E9名のtest artifactを根拠なくrenameしてprovenanceを消すこと
- stale testをgreenにするためcurrent implementationを旧bootstrap方式へ戻すこと
- handler load raceをfixed sleepだけで「検証済み」とみなすこと

## 10. Decision

Test Item evidence作成後、G03のcanonical decisionを`PASS` / `FAIL` / `BLOCKED`のいずれかで記録する。

本ドキュメントre-baseline時点では、retrospective Independent Verificationを実行済みとは扱わない。
