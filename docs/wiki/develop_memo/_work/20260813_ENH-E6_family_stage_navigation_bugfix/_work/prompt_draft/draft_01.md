INSTRUCTION: 上に行くほどあたらシイメッセージ

---
# まず取得してほしいもの

## ① Docker Composeの所属関係

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker compose ls
NAME                STATUS              CONFIG FILES
ariadne-e1a         running(4)          /loc0/bigbrother/repositories/causal-atelier/compose.yaml,/loc0/bigbrother/repositories/causal-atelier/compose.e1a.yaml
causal-atelier      running(4)          /loc0/bigbrother/repositories/causal-atelier/compose.yaml
```

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker ps -a --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.Label "com.docker.compose.project"}}\t{{.Label "com.docker.compose.service"}}'
NAMES                          IMAGE                    STATUS                      PORTS                                         project          service
causal-atelier-frontend-1      nginx:1.27-alpine        Up 30 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp       causal-atelier   frontend
causal-atelier-worker-1        causal-atelier-worker    Up 30 minutes               8000/tcp                                      causal-atelier   worker
causal-atelier-api-1           causal-atelier-api       Up 30 minutes (healthy)     0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   causal-atelier   api
causal-atelier-migrate-1       causal-atelier-migrate   Exited (0) 30 minutes ago                                                 causal-atelier   migrate
causal-atelier-database-1      postgres:17-alpine       Up 31 minutes (healthy)     127.0.0.1:5432->5432/tcp                      causal-atelier   database
ariadne-e1a-api-1              ariadne-e1a-api          Up 33 minutes (healthy)     127.0.0.1:18000->8000/tcp                     ariadne-e1a      api
ariadne-e1a-worker-1           ariadne-e1a-worker       Up 33 minutes               8000/tcp                                      ariadne-e1a      worker
ariadne-e1a-migrate-1          ariadne-e1a-migrate      Exited (0) 33 minutes ago                                                 ariadne-e1a      migrate
ariadne-test-database_test-1   postgres:17-alpine       Exited (0) 3 days ago                                                     ariadne-test     database_test
ariadne-e1a-frontend-1         nginx:1.27-alpine        Up 10 hours                 127.0.0.1:18080->80/tcp                       ariadne-e1a      frontend
ariadne-e1a-database-1         postgres:17-alpine       Up 10 hours (healthy)       127.0.0.1:15432->5432/tcp                     ariadne-e1a      database
```

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ for c in \
  causal-atelier-frontend-1 \
  causal-atelier-api-1 \
  causal-atelier-database-1 \
  ariadne-e1a-frontend-1 \
  ariadne-e1a-api-1 \
  ariadne-e1a-database-1
do
  echo "===== $c ====="
  docker inspect -f '
project={{index .Config.Labels "com.docker.compose.project"}}
service={{index .Config.Labels "com.docker.compose.service"}}
working_dir={{index .Config.Labels "com.docker.compose.project.working_dir"}}
config_files={{index .Config.Labels "com.docker.compose.project.config_files"}}
image={{.Image}}
networks={{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}
' "$c"
done
===== causal-atelier-frontend-1 =====

project=causal-atelier
service=frontend
working_dir=/loc0/bigbrother/repositories/causal-atelier
config_files=/loc0/bigbrother/repositories/causal-atelier/compose.yaml
image=sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10
networks=causal-atelier_default 

===== causal-atelier-api-1 =====

project=causal-atelier
service=api
working_dir=/loc0/bigbrother/repositories/causal-atelier
config_files=/loc0/bigbrother/repositories/causal-atelier/compose.yaml
image=sha256:ed7ac20ce5f6a4e23ca46e87ff17bcf734089365423951f0ad292eee92979f7a
networks=causal-atelier_default 

===== causal-atelier-database-1 =====

project=causal-atelier
service=database
working_dir=/loc0/bigbrother/repositories/causal-atelier
config_files=/loc0/bigbrother/repositories/causal-atelier/compose.yaml
image=sha256:742f40ea20b9ff2ff31db5458d127452988a2164df9e17441e191f3b72252193
networks=causal-atelier_default 

===== ariadne-e1a-frontend-1 =====

project=ariadne-e1a
service=frontend
working_dir=/loc0/bigbrother/repositories/causal-atelier
config_files=/loc0/bigbrother/repositories/causal-atelier/compose.yaml,/loc0/bigbrother/repositories/causal-atelier/compose.e1a.yaml
image=sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10
networks=ariadne-e1a_default 

===== ariadne-e1a-api-1 =====

project=ariadne-e1a
service=api
working_dir=/loc0/bigbrother/repositories/causal-atelier
config_files=/loc0/bigbrother/repositories/causal-atelier/compose.yaml,/loc0/bigbrother/repositories/causal-atelier/compose.e1a.yaml
image=sha256:d07ee9409b08556c4d4880fdb3040e7695ba956318f625c5a7e732dd5eecd109
networks=ariadne-e1a_default 

===== ariadne-e1a-database-1 =====

project=ariadne-e1a
service=database
working_dir=/loc0/bigbrother/repositories/causal-atelier
config_files=/loc0/bigbrother/repositories/causal-atelier/compose.yaml,/loc0/bigbrother/repositories/causal-atelier/compose.e1a.yaml
image=sha256:742f40ea20b9ff2ff31db5458d127452988a2164df9e17441e191f3b72252193
networks=ariadne-e1a_default 

```
## ② 実際に配信されているfrontendが同じか

まずrepository側:

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ sha256sum \
  frontend/index.html \
  frontend/app.js \
  frontend/navigation_state.js \
  frontend/analysis_presentation.js \
  frontend/causal_stage_presentation.js \
  frontend/styles.css
8a0349529622a1efeb16da8c2cee714eab2af903d04c335a941813ada4e87afd  frontend/index.html
cdbee3610b80d102dbc9a38e2360b8659ed08192959aa8f8f1b57655128b3135  frontend/app.js
f66784b95a02926622c3a0ca06bae2179d2d9efd6174f57bb265611ef4df14cb  frontend/navigation_state.js
c467b7f019e4a1e99cf94296ac9bf89f92ec617ca5cb98d8cfe0857b3295aa16  frontend/analysis_presentation.js
dadad922d4c3ae618a77d9aed76c4dfbf54e29025e00798cec4c3df07fcacb58  frontend/causal_stage_presentation.js
24c49a169df459645730523712858e6bd2c846ac3343500c57c910d3f5050d6a  frontend/styles.css
```

次に現在の 8080 stack:

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ for f in index.html app.js navigation_state.js analysis_presentation.js causal_stage_presentation.js styles.css
do
  printf '%-35s ' "$f"
  curl -fsS "http://127.0.0.1:8080/$f" | sha256sum
done
index.html                          8a0349529622a1efeb16da8c2cee714eab2af903d04c335a941813ada4e87afd  -
app.js                              cdbee3610b80d102dbc9a38e2360b8659ed08192959aa8f8f1b57655128b3135  -
navigation_state.js                 f66784b95a02926622c3a0ca06bae2179d2d9efd6174f57bb265611ef4df14cb  -
analysis_presentation.js            c467b7f019e4a1e99cf94296ac9bf89f92ec617ca5cb98d8cfe0857b3295aa16  -
causal_stage_presentation.js        dadad922d4c3ae618a77d9aed76c4dfbf54e29025e00798cec4c3df07fcacb58  -
styles.css                          24c49a169df459645730523712858e6bd2c846ac3343500c57c910d3f5050d6a  -
```

旧/別stackと思われる 18080 も同様に:

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ for f in index.html app.js navigation_state.js analysis_presentation.js causal_stage_presentation.js styles.css
do
  printf '%-35s ' "$f"
  curl -fsS "http://127.0.0.1:18080/$f" | sha256sum
done
index.html                          8a0349529622a1efeb16da8c2cee714eab2af903d04c335a941813ada4e87afd  -
app.js                              cdbee3610b80d102dbc9a38e2360b8659ed08192959aa8f8f1b57655128b3135  -
navigation_state.js                 f66784b95a02926622c3a0ca06bae2179d2d9efd6174f57bb265611ef4df14cb  -
analysis_presentation.js            c467b7f019e4a1e99cf94296ac9bf89f92ec617ca5cb98d8cfe0857b3295aa16  -
causal_stage_presentation.js        dadad922d4c3ae618a77d9aed76c4dfbf54e29025e00798cec4c3df07fcacb58  -
styles.css                          24c49a169df459645730523712858e6bd2c846ac3343500c57c910d3f5050d6a  -
```

## ③ 両stackのProject APIレスポンス

`````
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ echo '===== 8080 via frontend nginx ====='
curl -fsS http://127.0.0.1:8080/api/v1/projects | jq .

echo '===== 8000 direct API ====='
curl -fsS http://127.0.0.1:8000/api/v1/projects | jq .

echo '===== 18080 via old/e1a nginx ====='
curl -fsS http://127.0.0.1:18080/api/v1/projects | jq .

echo '===== 18000 direct e1a API ====='
curl -fsS http://127.0.0.1:18000/api/v1/projects | jq .
===== 8080 via frontend nginx =====
{
  "items": [
    {
      "project_id": "dca4b57c-9206-43f4-a40e-eba39cf2bf47",
      "name": "SALES dataset",
      "topic": "coupon and sales",
      "objective": "影響確認",
      "memo": "なんか適当なメモ",
      "status": "ACTIVE",
      "created_at": "2026-08-13T06:59:42.634463Z",
      "updated_at": "2026-08-13T06:59:42.634463Z"
    },
    {
      "project_id": "55d7f73d-c52b-4745-b1ba-af40ea47aea1",
      "name": "SALES dataset",
      "topic": "aaa",
      "objective": "aaa",
      "memo": "aaa",
      "status": "ACTIVE",
      "created_at": "2026-08-13T07:05:12.796691Z",
      "updated_at": "2026-08-13T07:05:12.796691Z"
    },
    {
      "project_id": "8045f08b-c83b-491e-a96a-f6026e189b06",
      "name": "SALES dataset",
      "topic": "aaa",
      "objective": "aaa",
      "memo": "",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:33:16.303271Z",
      "updated_at": "2026-08-13T09:33:16.303271Z"
    },
    {
      "project_id": "d68ad143-707b-4aaa-9549-8506b11ce93b",
      "name": "SALES dataset",
      "topic": "クーポンの効果推定を行う",
      "objective": "aaa",
      "memo": "aaa",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:33:42.531799Z",
      "updated_at": "2026-08-13T09:33:42.531799Z"
    },
    {
      "project_id": "68d8a98f-3862-4a27-a707-820639786ea6",
      "name": "coupon test",
      "topic": "クーポンの効果推定を行う",
      "objective": "あああ",
      "memo": "あああ",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:34:37.562463Z",
      "updated_at": "2026-08-13T09:34:37.562463Z"
    }
  ],
  "next_cursor": null
}
===== 8000 direct API =====
{
  "items": [
    {
      "project_id": "dca4b57c-9206-43f4-a40e-eba39cf2bf47",
      "name": "SALES dataset",
      "topic": "coupon and sales",
      "objective": "影響確認",
      "memo": "なんか適当なメモ",
      "status": "ACTIVE",
      "created_at": "2026-08-13T06:59:42.634463Z",
      "updated_at": "2026-08-13T06:59:42.634463Z"
    },
    {
      "project_id": "55d7f73d-c52b-4745-b1ba-af40ea47aea1",
      "name": "SALES dataset",
      "topic": "aaa",
      "objective": "aaa",
      "memo": "aaa",
      "status": "ACTIVE",
      "created_at": "2026-08-13T07:05:12.796691Z",
      "updated_at": "2026-08-13T07:05:12.796691Z"
    },
    {
      "project_id": "8045f08b-c83b-491e-a96a-f6026e189b06",
      "name": "SALES dataset",
      "topic": "aaa",
      "objective": "aaa",
      "memo": "",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:33:16.303271Z",
      "updated_at": "2026-08-13T09:33:16.303271Z"
    },
    {
      "project_id": "d68ad143-707b-4aaa-9549-8506b11ce93b",
      "name": "SALES dataset",
      "topic": "クーポンの効果推定を行う",
      "objective": "aaa",
      "memo": "aaa",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:33:42.531799Z",
      "updated_at": "2026-08-13T09:33:42.531799Z"
    },
    {
      "project_id": "68d8a98f-3862-4a27-a707-820639786ea6",
      "name": "coupon test",
      "topic": "クーポンの効果推定を行う",
      "objective": "あああ",
      "memo": "あああ",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:34:37.562463Z",
      "updated_at": "2026-08-13T09:34:37.562463Z"
    }
  ],
  "next_cursor": null
}
===== 18080 via old/e1a nginx =====
{
  "items": [
    {
      "project_id": "48e547ec-686f-4f59-a4bd-fb1f7d76bdf2",
      "name": "ENH-E1a Browser 1786580171",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T00:16:12.428203Z",
      "updated_at": "2026-08-13T00:16:13.454677Z"
    },
    {
      "project_id": "67d26fe8-3801-4108-8d57-3939d62fe74a",
      "name": "ENH-E1a Browser 1786583282",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:08:03.054670Z",
      "updated_at": "2026-08-13T01:08:03.832084Z"
    },
    {
      "project_id": "999116fc-3c11-4866-b124-110b6c897254",
      "name": "ENH-E1a Browser 1786583605",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:13:25.974182Z",
      "updated_at": "2026-08-13T01:13:26.786922Z"
    },
    {
      "project_id": "d5c330ba-e2a3-497a-b1ec-dd9c9b31087f",
      "name": "ENH-E1a Browser 1786586081",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:54:42.165019Z",
      "updated_at": "2026-08-13T01:54:42.966400Z"
    },
    {
      "project_id": "880f82e2-01a0-4840-b49f-3e58e38a6f32",
      "name": "ENH-E1a Browser 1786586236",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:57:17.388192Z",
      "updated_at": "2026-08-13T01:57:18.384408Z"
    },
    {
      "project_id": "00a69699-0dd3-408d-9b31-59ba3d1eb113",
      "name": "ENH-E1a Browser 1786586457",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:00:58.422055Z",
      "updated_at": "2026-08-13T02:00:59.197708Z"
    },
    {
      "project_id": "0bf5831d-17de-4d04-894b-61380bd22cdb",
      "name": "ENH-E3 Final Browser 1786586555",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:02:35.909582Z",
      "updated_at": "2026-08-13T02:02:35.909582Z"
    },
    {
      "project_id": "8e1fb78e-db62-4413-bbb3-1da5515dff44",
      "name": "ENH-E3 Final Browser 1786586979",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:09:40.102026Z",
      "updated_at": "2026-08-13T02:09:40.102026Z"
    },
    {
      "project_id": "e103a765-fc34-4da7-95d1-8554fc680859",
      "name": "ENH-E3 Final Browser 1786588641",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:37:21.795011Z",
      "updated_at": "2026-08-13T02:37:21.795011Z"
    },
    {
      "project_id": "8ede0fed-5b02-455b-a80d-64e44e3c85e2",
      "name": "ENH-E3 Final Browser 1786588757",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:39:17.748027Z",
      "updated_at": "2026-08-13T02:39:17.748027Z"
    },
    {
      "project_id": "18f96bce-39bb-4668-a1e5-65ad7904d2cc",
      "name": "ENH-E3 Final Browser 1786589144",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:45:44.950995Z",
      "updated_at": "2026-08-13T02:45:44.950995Z"
    },
    {
      "project_id": "162a55fa-3369-4827-99d6-b34d2a5521d8",
      "name": "ENH-E3 Final Browser 1786589343",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:49:04.244545Z",
      "updated_at": "2026-08-13T02:49:04.244545Z"
    },
    {
      "project_id": "1c3252da-7f0c-4d4d-b480-b608c8bb2a0a",
      "name": "ENH-E3 Final Browser 1786589758",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:55:58.567876Z",
      "updated_at": "2026-08-13T02:55:58.567876Z"
    },
    {
      "project_id": "f2a70464-6b33-446d-b4f9-0cbf276c2328",
      "name": "ENH-E3 Final Browser 1786591135",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:18:56.343321Z",
      "updated_at": "2026-08-13T03:18:56.343321Z"
    },
    {
      "project_id": "778c3d3f-5806-4efe-b467-323422fb6034",
      "name": "ENH-E3 Final Browser 1786591970",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:32:50.771266Z",
      "updated_at": "2026-08-13T03:32:50.771266Z"
    },
    {
      "project_id": "37f5bb88-6d2b-4683-b855-bc8d236ca1d4",
      "name": "ENH-E3 Final Browser 1786592084",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:34:44.609896Z",
      "updated_at": "2026-08-13T03:34:44.609896Z"
    },
    {
      "project_id": "9aeeeb47-51ad-407e-ab28-400bdf5c2bb7",
      "name": "ENH-E3 Final Browser 1786592175",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:36:15.733488Z",
      "updated_at": "2026-08-13T03:36:15.733488Z"
    },
    {
      "project_id": "c0539044-8034-4e85-afa3-5e6d0ed438e0",
      "name": "ENH-E3 Final Browser 1786592896",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:48:16.949596Z",
      "updated_at": "2026-08-13T03:48:16.949596Z"
    },
    {
      "project_id": "c889f4fb-ddd1-4da0-89fa-5bcd5cac23d6",
      "name": "ENH-E3 Final Browser 1786592980",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:49:40.441874Z",
      "updated_at": "2026-08-13T03:49:40.441874Z"
    },
    {
      "project_id": "f541f3de-68a7-4a0c-9a30-8c761e7543dc",
      "name": "ENH-E3 Final Browser 1786593082",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:51:22.961966Z",
      "updated_at": "2026-08-13T03:51:22.961966Z"
    },
    {
      "project_id": "a2f14e98-50ec-4f4d-a876-3e1a9d50e339",
      "name": "ENH-E3 Final Browser 1786593281",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:54:42.161585Z",
      "updated_at": "2026-08-13T03:54:42.161585Z"
    },
    {
      "project_id": "4ae38b56-0d9e-4935-a55e-ffe463c1d7dc",
      "name": "ENH-E3 Final Browser 1786593397",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:56:38.243628Z",
      "updated_at": "2026-08-13T03:56:38.243628Z"
    },
    {
      "project_id": "b1117d7a-0cf2-4818-9c3c-1ff34462693f",
      "name": "ENH-E3 Final Browser 1786593572",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:59:33.300465Z",
      "updated_at": "2026-08-13T03:59:33.300465Z"
    },
    {
      "project_id": "42641321-5b83-4307-ae17-7efb6f2b1dfa",
      "name": "ENH-E3 Final Browser 1786593693",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:01:33.449859Z",
      "updated_at": "2026-08-13T04:01:33.449859Z"
    },
    {
      "project_id": "e8c565d0-25fe-471d-b308-149a913f2ccf",
      "name": "ENH-E3 Final Browser 1786594195",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:09:55.590912Z",
      "updated_at": "2026-08-13T04:09:55.590912Z"
    },
    {
      "project_id": "2c10ee21-c0ea-43ce-b6de-35760344d66f",
      "name": "ENH-E3 Final Browser 1786594373",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:12:54.047423Z",
      "updated_at": "2026-08-13T04:12:54.047423Z"
    },
    {
      "project_id": "eb07fe93-dee7-48fd-be64-cd56599bba8d",
      "name": "ENH-E1a Browser 1786594412",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:13:33.824227Z",
      "updated_at": "2026-08-13T04:13:34.777781Z"
    },
    {
      "project_id": "ba29c1ce-51ff-43db-8f64-3dea2e572153",
      "name": "ENH-E3 Final Browser 1786595072",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:24:33.333440Z",
      "updated_at": "2026-08-13T04:24:33.333440Z"
    },
    {
      "project_id": "c94406df-9e0a-4e2b-ab7d-279ca1f48878",
      "name": "ENH-E1a Browser 1786595113",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:25:14.008617Z",
      "updated_at": "2026-08-13T04:25:14.817234Z"
    },
    {
      "project_id": "052c0ba1-b3e6-47e5-b81a-479353c864c5",
      "name": "ENH-E6 Baseline 1786605459",
      "topic": "ENH-E6 baseline",
      "objective": "Family stage navigation baseline reproduction",
      "memo": "ENH-E6 preflight",
      "status": "ACTIVE",
      "created_at": "2026-08-13T07:17:39.501797Z",
      "updated_at": "2026-08-13T07:17:39.501797Z"
    },
    {
      "project_id": "f2c6fd7a-142e-49cc-88a8-7493d5517875",
      "name": "ENH-E6 Navigation Browser 1786612789",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:19:49.735683Z",
      "updated_at": "2026-08-13T09:19:49.735683Z"
    },
    {
      "project_id": "0cd77b5e-3b2c-4fed-9f93-030d18779e42",
      "name": "ENH-E6 Navigation Browser 1786612832",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:20:32.650379Z",
      "updated_at": "2026-08-13T09:20:32.650379Z"
    },
    {
      "project_id": "928580cb-ee72-4794-9218-c279e0048dc3",
      "name": "ENH-E6 Navigation Browser 1786613179",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:26:19.788890Z",
      "updated_at": "2026-08-13T09:26:19.788890Z"
    },
    {
      "project_id": "93ad4a74-ab0d-4c06-ac7a-056d2bd240d4",
      "name": "ENH-E6 Navigation Browser 1786613368",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:29:28.594748Z",
      "updated_at": "2026-08-13T09:29:28.594748Z"
    }
  ],
  "next_cursor": null
}
===== 18000 direct e1a API =====
{
  "items": [
    {
      "project_id": "48e547ec-686f-4f59-a4bd-fb1f7d76bdf2",
      "name": "ENH-E1a Browser 1786580171",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T00:16:12.428203Z",
      "updated_at": "2026-08-13T00:16:13.454677Z"
    },
    {
      "project_id": "67d26fe8-3801-4108-8d57-3939d62fe74a",
      "name": "ENH-E1a Browser 1786583282",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:08:03.054670Z",
      "updated_at": "2026-08-13T01:08:03.832084Z"
    },
    {
      "project_id": "999116fc-3c11-4866-b124-110b6c897254",
      "name": "ENH-E1a Browser 1786583605",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:13:25.974182Z",
      "updated_at": "2026-08-13T01:13:26.786922Z"
    },
    {
      "project_id": "d5c330ba-e2a3-497a-b1ec-dd9c9b31087f",
      "name": "ENH-E1a Browser 1786586081",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:54:42.165019Z",
      "updated_at": "2026-08-13T01:54:42.966400Z"
    },
    {
      "project_id": "880f82e2-01a0-4840-b49f-3e58e38a6f32",
      "name": "ENH-E1a Browser 1786586236",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T01:57:17.388192Z",
      "updated_at": "2026-08-13T01:57:18.384408Z"
    },
    {
      "project_id": "00a69699-0dd3-408d-9b31-59ba3d1eb113",
      "name": "ENH-E1a Browser 1786586457",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:00:58.422055Z",
      "updated_at": "2026-08-13T02:00:59.197708Z"
    },
    {
      "project_id": "0bf5831d-17de-4d04-894b-61380bd22cdb",
      "name": "ENH-E3 Final Browser 1786586555",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:02:35.909582Z",
      "updated_at": "2026-08-13T02:02:35.909582Z"
    },
    {
      "project_id": "8e1fb78e-db62-4413-bbb3-1da5515dff44",
      "name": "ENH-E3 Final Browser 1786586979",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:09:40.102026Z",
      "updated_at": "2026-08-13T02:09:40.102026Z"
    },
    {
      "project_id": "e103a765-fc34-4da7-95d1-8554fc680859",
      "name": "ENH-E3 Final Browser 1786588641",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:37:21.795011Z",
      "updated_at": "2026-08-13T02:37:21.795011Z"
    },
    {
      "project_id": "8ede0fed-5b02-455b-a80d-64e44e3c85e2",
      "name": "ENH-E3 Final Browser 1786588757",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:39:17.748027Z",
      "updated_at": "2026-08-13T02:39:17.748027Z"
    },
    {
      "project_id": "18f96bce-39bb-4668-a1e5-65ad7904d2cc",
      "name": "ENH-E3 Final Browser 1786589144",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:45:44.950995Z",
      "updated_at": "2026-08-13T02:45:44.950995Z"
    },
    {
      "project_id": "162a55fa-3369-4827-99d6-b34d2a5521d8",
      "name": "ENH-E3 Final Browser 1786589343",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:49:04.244545Z",
      "updated_at": "2026-08-13T02:49:04.244545Z"
    },
    {
      "project_id": "1c3252da-7f0c-4d4d-b480-b608c8bb2a0a",
      "name": "ENH-E3 Final Browser 1786589758",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T02:55:58.567876Z",
      "updated_at": "2026-08-13T02:55:58.567876Z"
    },
    {
      "project_id": "f2a70464-6b33-446d-b4f9-0cbf276c2328",
      "name": "ENH-E3 Final Browser 1786591135",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:18:56.343321Z",
      "updated_at": "2026-08-13T03:18:56.343321Z"
    },
    {
      "project_id": "778c3d3f-5806-4efe-b467-323422fb6034",
      "name": "ENH-E3 Final Browser 1786591970",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:32:50.771266Z",
      "updated_at": "2026-08-13T03:32:50.771266Z"
    },
    {
      "project_id": "37f5bb88-6d2b-4683-b855-bc8d236ca1d4",
      "name": "ENH-E3 Final Browser 1786592084",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:34:44.609896Z",
      "updated_at": "2026-08-13T03:34:44.609896Z"
    },
    {
      "project_id": "9aeeeb47-51ad-407e-ab28-400bdf5c2bb7",
      "name": "ENH-E3 Final Browser 1786592175",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:36:15.733488Z",
      "updated_at": "2026-08-13T03:36:15.733488Z"
    },
    {
      "project_id": "c0539044-8034-4e85-afa3-5e6d0ed438e0",
      "name": "ENH-E3 Final Browser 1786592896",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:48:16.949596Z",
      "updated_at": "2026-08-13T03:48:16.949596Z"
    },
    {
      "project_id": "c889f4fb-ddd1-4da0-89fa-5bcd5cac23d6",
      "name": "ENH-E3 Final Browser 1786592980",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:49:40.441874Z",
      "updated_at": "2026-08-13T03:49:40.441874Z"
    },
    {
      "project_id": "f541f3de-68a7-4a0c-9a30-8c761e7543dc",
      "name": "ENH-E3 Final Browser 1786593082",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:51:22.961966Z",
      "updated_at": "2026-08-13T03:51:22.961966Z"
    },
    {
      "project_id": "a2f14e98-50ec-4f4d-a876-3e1a9d50e339",
      "name": "ENH-E3 Final Browser 1786593281",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:54:42.161585Z",
      "updated_at": "2026-08-13T03:54:42.161585Z"
    },
    {
      "project_id": "4ae38b56-0d9e-4935-a55e-ffe463c1d7dc",
      "name": "ENH-E3 Final Browser 1786593397",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:56:38.243628Z",
      "updated_at": "2026-08-13T03:56:38.243628Z"
    },
    {
      "project_id": "b1117d7a-0cf2-4818-9c3c-1ff34462693f",
      "name": "ENH-E3 Final Browser 1786593572",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T03:59:33.300465Z",
      "updated_at": "2026-08-13T03:59:33.300465Z"
    },
    {
      "project_id": "42641321-5b83-4307-ae17-7efb6f2b1dfa",
      "name": "ENH-E3 Final Browser 1786593693",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:01:33.449859Z",
      "updated_at": "2026-08-13T04:01:33.449859Z"
    },
    {
      "project_id": "e8c565d0-25fe-471d-b308-149a913f2ccf",
      "name": "ENH-E3 Final Browser 1786594195",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:09:55.590912Z",
      "updated_at": "2026-08-13T04:09:55.590912Z"
    },
    {
      "project_id": "2c10ee21-c0ea-43ce-b6de-35760344d66f",
      "name": "ENH-E3 Final Browser 1786594373",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:12:54.047423Z",
      "updated_at": "2026-08-13T04:12:54.047423Z"
    },
    {
      "project_id": "eb07fe93-dee7-48fd-be64-cd56599bba8d",
      "name": "ENH-E1a Browser 1786594412",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:13:33.824227Z",
      "updated_at": "2026-08-13T04:13:34.777781Z"
    },
    {
      "project_id": "ba29c1ce-51ff-43db-8f64-3dea2e572153",
      "name": "ENH-E3 Final Browser 1786595072",
      "topic": "conversion prediction and causal follow-up",
      "objective": "Explore, predict, and preserve cross-analysis lineage",
      "memo": "G6 real Chromium acceptance",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:24:33.333440Z",
      "updated_at": "2026-08-13T04:24:33.333440Z"
    },
    {
      "project_id": "c94406df-9e0a-4e2b-ab7d-279ca1f48878",
      "name": "ENH-E1a Browser 1786595113",
      "topic": "E2E-04 to E2E-10",
      "objective": "Browser acceptance",
      "memo": "Metadata updated from Project / Data",
      "status": "ACTIVE",
      "created_at": "2026-08-13T04:25:14.008617Z",
      "updated_at": "2026-08-13T04:25:14.817234Z"
    },
    {
      "project_id": "052c0ba1-b3e6-47e5-b81a-479353c864c5",
      "name": "ENH-E6 Baseline 1786605459",
      "topic": "ENH-E6 baseline",
      "objective": "Family stage navigation baseline reproduction",
      "memo": "ENH-E6 preflight",
      "status": "ACTIVE",
      "created_at": "2026-08-13T07:17:39.501797Z",
      "updated_at": "2026-08-13T07:17:39.501797Z"
    },
    {
      "project_id": "f2c6fd7a-142e-49cc-88a8-7493d5517875",
      "name": "ENH-E6 Navigation Browser 1786612789",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:19:49.735683Z",
      "updated_at": "2026-08-13T09:19:49.735683Z"
    },
    {
      "project_id": "0cd77b5e-3b2c-4fed-9f93-030d18779e42",
      "name": "ENH-E6 Navigation Browser 1786612832",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:20:32.650379Z",
      "updated_at": "2026-08-13T09:20:32.650379Z"
    },
    {
      "project_id": "928580cb-ee72-4794-9218-c279e0048dc3",
      "name": "ENH-E6 Navigation Browser 1786613179",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:26:19.788890Z",
      "updated_at": "2026-08-13T09:26:19.788890Z"
    },
    {
      "project_id": "93ad4a74-ab0d-4c06-ac7a-056d2bd240d4",
      "name": "ENH-E6 Navigation Browser 1786613368",
      "topic": "family and stage navigation",
      "objective": "exercise canonical analysis navigation in Chromium",
      "memo": "ENH-E6 G01 P03 browser fixture",
      "status": "ACTIVE",
      "created_at": "2026-08-13T09:29:28.594748Z",
      "updated_at": "2026-08-13T09:29:28.594748Z"
    }
  ],
  "next_cursor": null
}
`````

## ④ E2EがどのURLを使ったか

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ rg -n \
'baseURL|base_url|8080|18080|8000|18000|analysis-family-tabs|chromium|playwright|B01|B02|B03' \
tests frontend . \
-g '!docs/**' \
-g '!*.lock'
frontend/index.html
28:        <div id="analysis-family-tabs" role="tablist" aria-label="Analysis family"></div>
121:          <label>Rationale<input name="rationale" value="Algorithm and PC sensitivity comparison" maxlength="8000"></label>

./deploy/nginx.conf
7:    set $api_upstream http://api:8000;

frontend/app.js
129:  $('#analysis-family-tabs').replaceChildren();$('#analysis-stage-sidebar').replaceChildren();
135:  $('#analysis-family-tabs').innerHTML=catalog.families.map(f=>'<button type="button" role="tab" aria-selected="'+(f.slug===current.slug)+'" aria-label="Analysis family: '+escapeHtml(f.label)+'" data-family="'+escapeHtml(f.slug)+'">'+escapeHtml(f.label)+'</button>').join('');
137:  $$('#analysis-family-tabs button').forEach(button=>button.onclick=()=>{const family=catalog.families.find(f=>f.slug===button.dataset.family);applyAnalysisNavigation(AnalysisNavigation.defaultContext(catalog,state.project.project_id,family.slug),{historyMode:ANALYSIS_HISTORY_MODES.PUSH,source:'family-tab-click'}).catch(error=>notice(error.message))});

frontend/styles.css
11:#analysis-navigation-shell{display:grid;gap:12px}#analysis-family-tabs,#analysis-stage-sidebar{display:flex;gap:8px;flex-wrap:wrap}#analysis-family-tabs button[aria-selected="true"],#analysis-stage-sidebar button[aria-current="page"]{background:#173f31;color:#fff;border-color:#173f31}#operation-availability .status{margin-right:6px;border:1px solid #52665c}

./README.md
20:- Frontend: <http://localhost:8080>
21:- OpenAPI UI: <http://localhost:8000/docs>
22:- Readiness: <http://localhost:8000/health/ready>

./pyproject.toml
85:    "playwright>=1.49.0,<2",

./product_migrations/env.py
16:database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
17:if not database_url:
19:config.set_main_option("sqlalchemy.url", database_url)

./src/ariadne/interfaces/web_api/schemas/__init__.py
19:    memo: str | None = Field(default=None, max_length=8000)
26:    memo: str | None = Field(default=None, max_length=8000)
67:    rationale: str | None = Field(default=None, max_length=8000)
73:    change_reason: str | None = Field(default=None, max_length=8000)
180:    edit_rationale: str = Field(min_length=1, max_length=8000)
214:    statement: str = Field(min_length=1, max_length=8000); rationale: str | None = None
219:    statement: str | None = Field(default=None, min_length=1, max_length=8000)

./src/ariadne/interfaces/web_api/dependencies.py
36:    database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
37:    if not database_url:
39:    engine = create_engine(database_url)

./src/ariadne/interfaces/web_api/routers/product_closure.py
53:    statement: str = Field(min_length=1, max_length=8000)
54:    rationale: str | None = Field(default=None, max_length=8000)
62:    statement: str | None = Field(default=None, min_length=1, max_length=8000)
63:    rationale: str | None = Field(default=None, max_length=8000)

./Dockerfile.browser-e2e
1:FROM mcr.microsoft.com/playwright/python:v1.62.0-noble
3:RUN pip install --no-cache-dir playwright==1.62.0

./frontend/index.html
28:        <div id="analysis-family-tabs" role="tablist" aria-label="Analysis family"></div>
121:          <label>Rationale<input name="rationale" value="Algorithm and PC sensitivity comparison" maxlength="8000"></label>

./frontend/app.js
129:  $('#analysis-family-tabs').replaceChildren();$('#analysis-stage-sidebar').replaceChildren();
135:  $('#analysis-family-tabs').innerHTML=catalog.families.map(f=>'<button type="button" role="tab" aria-selected="'+(f.slug===current.slug)+'" aria-label="Analysis family: '+escapeHtml(f.label)+'" data-family="'+escapeHtml(f.slug)+'">'+escapeHtml(f.label)+'</button>').join('');
137:  $$('#analysis-family-tabs button').forEach(button=>button.onclick=()=>{const family=catalog.families.find(f=>f.slug===button.dataset.family);applyAnalysisNavigation(AnalysisNavigation.defaultContext(catalog,state.project.project_id,family.slug),{historyMode:ANALYSIS_HISTORY_MODES.PUSH,source:'family-tab-click'}).catch(error=>notice(error.message))});

./frontend/styles.css
11:#analysis-navigation-shell{display:grid;gap:12px}#analysis-family-tabs,#analysis-stage-sidebar{display:flex;gap:8px;flex-wrap:wrap}#analysis-family-tabs button[aria-selected="true"],#analysis-stage-sidebar button[aria-current="page"]{background:#173f31;color:#fff;border-color:#173f31}#operation-availability .status{margin-right:6px;border:1px solid #52665c}

./src/ariadne/interfaces/web_api/app.py
64:    uvicorn.run("ariadne.interfaces.web_api.app:app", host="0.0.0.0", port=8000, reload=False)

./src/ariadne/interfaces/worker/runner.py
31:    database_url: str,
40:    engine = create_engine(database_url)
95:    database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
96:    if not database_url:
101:    run_worker(database_url, artifact_root, poll_seconds)

./src/ariadne/legacy/interfaces/api/app.py
37:    resolved_database = database or Database(resolved_settings.database_url)
66:        allow_origins=["http://localhost:8080", "http://localhost:3000"],
217:        "ariadne.interfaces.api.app:app", host="0.0.0.0", port=8000, reload=False

./src/ariadne/legacy/workers/main.py
30:    database = Database(settings.database_url)

tests/browser_e2e/run_enh_e6_family_stage_navigation.py
14:from playwright.sync_api import Page, sync_playwright
17:WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
18:API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
65:        "family_tabs": controls("#analysis-family-tabs button"),
76:    selected = page.locator(f'#analysis-family-tabs button[data-family="{family}"][aria-selected="true"]')
84:    page.locator(f'#analysis-family-tabs button[data-family="{slug}"]').click()
103:    with sync_playwright() as playwright:
104:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
115:            # B01: normal entry and real Family/Stage tab interactions, without reload.
118:            tabs = page.locator('#analysis-family-tabs button[role="tab"]')
129:            evidence["scenarios"]["B01-normal-entry-family-switching"] = {"status": "PASS", "snapshot": _snapshot(page)}
131:            # B02: the two legacy causal entries are compatibility shortcuts, not parallel routes.
138:            evidence["scenarios"]["B02-causal-discovery-inference-boundary"] = {"status": "PASS", "snapshot": _snapshot(page)}
140:            # B03: direct canonical state, history traversal, and reload preserve the same UI identity.
161:            evidence["scenarios"]["B03-direct-reload-history-restore"] = {

tests/browser_e2e/run_enh_e3.py
12:from playwright.sync_api import sync_playwright
106:    with sync_playwright() as playwright:
107:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])

tests/browser_e2e/run_enh_e3_predictive.py
15:from playwright.sync_api import Page, sync_playwright
18:WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
19:API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
159:    with sync_playwright() as playwright:
160:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])

tests/browser_e2e/run_enh_e1a.py
15:from playwright.sync_api import Page, sync_playwright
18:WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
19:API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
174:    with sync_playwright() as playwright:
175:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])

tests/legacy_archive/retired_control_plane/unit/web/test_rbac.py
30:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

tests/legacy_archive/retired_control_plane/unit/web/test_artifact_lineage.py
34:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

tests/legacy_archive/retired_control_plane/unit/web/test_execution_state_machine.py
29:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

tests/legacy_archive/retired_control_plane/unit/web/test_constraints.py
35:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

tests/legacy_archive/retired_control_plane/unit/web/test_web_mvp.py
16:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

tests/legacy_archive/retired_control_plane/unit/web/test_negative_e2e.py
33:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

tests/legacy_archive/retired_control_plane/unit/test_worker_mlflow.py
31:        database_url=f"sqlite:///{tmp_path / 'test.db'}",
39:    db = Database(settings.database_url)

tests/product/test_enh_e6_g01_p03_browser_runner.py
16:    assert "#analysis-family-tabs" in runner
18:    assert "B01-normal-entry-family-switching" in runner
19:    assert "B02-causal-discovery-inference-boundary" in runner
20:    assert "B03-direct-reload-history-restore" in runner

tests/product/test_enh_e6_g01_p01_navigation_transition.py
37:    assert "$('#analysis-family-tabs').replaceChildren();$('#analysis-stage-sidebar').replaceChildren();" in source

./src/ariadne/infrastructure/settings.py
21:    database_url: str
51:        database_url = os.getenv(
56:            database_url=database_url,
111:        if self.database_url.startswith("sqlite:///"):
112:            Path(self.database_url.removeprefix("sqlite:///")).parent.mkdir(

tests/product/test_frontend_contract.py
59:    assert 'name="rationale" value="Algorithm and PC sensitivity comparison" maxlength="8000"' in html

tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py
94:    database_url = os.getenv("ARIADNE_PRODUCT_TEST_DATABASE_URL")
95:    if not database_url:
97:    engine = create_engine(database_url, pool_pre_ping=True)

tests/product/test_enh_e5_g01_navigation_shell.py
8:    assert 'id="analysis-family-tabs"' in html

tests/product/compose_golden_path_smoke.py
20:BASE_URL = os.getenv("ARIADNE_GOLDEN_PATH_BASE_URL", "http://127.0.0.1:8000/api/v1")
81:    with httpx.Client(base_url=BASE_URL, timeout=30) as client:

tests/product/test_enh_e4_g08_clean_bootstrap_postgres.py
21:    database_url = os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"]
22:    monkeypatch.setenv("ARIADNE_PRODUCT_DATABASE_URL", database_url)
26:            transport=httpx.ASGITransport(app=create_app()), base_url="http://test",

tests/product/conftest.py
28:    database_url = f"sqlite:///{tmp_path / 'product.db'}"
29:    monkeypatch.setenv("ARIADNE_PRODUCT_DATABASE_URL", database_url)
38:    yield database_url, tmp_path
86:        transport=httpx.ASGITransport(app=create_app()), base_url="http://test"

./tests/browser_e2e/run_enh_e6_family_stage_navigation.py
14:from playwright.sync_api import Page, sync_playwright
17:WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
18:API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
65:        "family_tabs": controls("#analysis-family-tabs button"),
76:    selected = page.locator(f'#analysis-family-tabs button[data-family="{family}"][aria-selected="true"]')
84:    page.locator(f'#analysis-family-tabs button[data-family="{slug}"]').click()
103:    with sync_playwright() as playwright:
104:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
115:            # B01: normal entry and real Family/Stage tab interactions, without reload.
118:            tabs = page.locator('#analysis-family-tabs button[role="tab"]')
129:            evidence["scenarios"]["B01-normal-entry-family-switching"] = {"status": "PASS", "snapshot": _snapshot(page)}
131:            # B02: the two legacy causal entries are compatibility shortcuts, not parallel routes.
138:            evidence["scenarios"]["B02-causal-discovery-inference-boundary"] = {"status": "PASS", "snapshot": _snapshot(page)}
140:            # B03: direct canonical state, history traversal, and reload preserve the same UI identity.
161:            evidence["scenarios"]["B03-direct-reload-history-restore"] = {

./tests/browser_e2e/run_enh_e3.py
12:from playwright.sync_api import sync_playwright
106:    with sync_playwright() as playwright:
107:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])

./tests/browser_e2e/run_enh_e3_predictive.py
15:from playwright.sync_api import Page, sync_playwright
18:WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
19:API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
159:    with sync_playwright() as playwright:
160:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])

./tests/browser_e2e/run_enh_e1a.py
15:from playwright.sync_api import Page, sync_playwright
18:WEB = os.getenv("ARIADNE_E2E_WEB_URL", "http://127.0.0.1:8080")
19:API = os.getenv("ARIADNE_E2E_API_URL", "http://127.0.0.1:8000/api/v1")
174:    with sync_playwright() as playwright:
175:        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])

./tests/legacy_archive/retired_control_plane/unit/web/test_rbac.py
30:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

./tests/legacy_archive/retired_control_plane/unit/web/test_artifact_lineage.py
34:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

./tests/legacy_archive/retired_control_plane/unit/web/test_execution_state_machine.py
29:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

./tests/legacy_archive/retired_control_plane/unit/web/test_constraints.py
35:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

./tests/legacy_archive/retired_control_plane/unit/web/test_web_mvp.py
16:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

./tests/legacy_archive/retired_control_plane/unit/web/test_negative_e2e.py
33:        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",

./tests/legacy_archive/retired_control_plane/unit/test_worker_mlflow.py
31:        database_url=f"sqlite:///{tmp_path / 'test.db'}",
39:    db = Database(settings.database_url)

./tests/product/test_enh_e6_g01_p03_browser_runner.py
16:    assert "#analysis-family-tabs" in runner
18:    assert "B01-normal-entry-family-switching" in runner
19:    assert "B02-causal-discovery-inference-boundary" in runner
20:    assert "B03-direct-reload-history-restore" in runner

./tests/product/test_enh_e6_g01_p01_navigation_transition.py
37:    assert "$('#analysis-family-tabs').replaceChildren();$('#analysis-stage-sidebar').replaceChildren();" in source

./tests/product/test_frontend_contract.py
59:    assert 'name="rationale" value="Algorithm and PC sensitivity comparison" maxlength="8000"' in html

./tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py
94:    database_url = os.getenv("ARIADNE_PRODUCT_TEST_DATABASE_URL")
95:    if not database_url:
97:    engine = create_engine(database_url, pool_pre_ping=True)

./tests/product/test_enh_e5_g01_navigation_shell.py
8:    assert 'id="analysis-family-tabs"' in html

./tests/product/compose_golden_path_smoke.py
20:BASE_URL = os.getenv("ARIADNE_GOLDEN_PATH_BASE_URL", "http://127.0.0.1:8000/api/v1")
81:    with httpx.Client(base_url=BASE_URL, timeout=30) as client:

./tests/product/test_enh_e4_g08_clean_bootstrap_postgres.py
21:    database_url = os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"]
22:    monkeypatch.setenv("ARIADNE_PRODUCT_DATABASE_URL", database_url)
26:            transport=httpx.ASGITransport(app=create_app()), base_url="http://test",

./tests/product/conftest.py
28:    database_url = f"sqlite:///{tmp_path / 'product.db'}"
29:    monkeypatch.setenv("ARIADNE_PRODUCT_DATABASE_URL", database_url)
38:    yield database_url, tmp_path
86:        transport=httpx.ASGITransport(app=create_app()), base_url="http://test"

./compose.yaml
35:      - "8000:8000"
39:      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/ready')"]
60:      - "8080:80"

./compose.e1a.yaml
7:      - "127.0.0.1:18000:8000"
10:      - "127.0.0.1:18080:80"
15:    image: ariadne-e1a-browser-e2e:playwright-1.62.0
22:      ARIADNE_E2E_API_URL: http://api:8000/api/v1
24:      PLAYWRIGHT_BROWSERS_PATH: /ms-playwright

./src/ariadne/product/persistence/database.py
15:def build_engine(database_url: str, **kwargs: object):  # type: ignore[no-untyped-def]
16:    return create_engine(database_url, **kwargs)  # type: ignore[arg-type]
19:def create_all_tables(database_url: str) -> None:
20:    engine = build_engine(database_url)
25:    def __init__(self, database_url: str, **engine_kwargs: object) -> None:
26:        self._engine = build_engine(database_url, **engine_kwargs)

./src/ariadne/product/application/product_closure_service.py
573:        if not statement or len(statement) > 8000:
574:            raise InvalidSchema("statement must be 1 to 8000 characters")

./Dockerfile
23:EXPOSE 8000
24:CMD ["uvicorn", "ariadne.interfaces.web_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## aaa

---
何を取得したら良い？
あと、関係ないかもしれないが、docker container
不要と思われるコンテナも結構ある。これらは消すべきか？あるいは、テストに悪影響を及ぼさないならばそっとしておくのが良いか？

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker container ls -a
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                      PORTS                                         NAMES
61dd04197e24   nginx:1.27-alpine        "/docker-entrypoint.…"   26 minutes ago   Up 26 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp       causal-atelier-frontend-1
e133190c97fb   causal-atelier-worker    "ariadne-worker"         26 minutes ago   Up 26 minutes               8000/tcp                                      causal-atelier-worker-1
bd69d83af6ba   causal-atelier-api       "uvicorn ariadne.int…"   26 minutes ago   Up 26 minutes (healthy)     0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   causal-atelier-api-1
ab7fd81e58a3   causal-atelier-migrate   "alembic -c alembic_…"   26 minutes ago   Exited (0) 25 minutes ago                                                 causal-atelier-migrate-1
e8a3417f7399   postgres:17-alpine       "docker-entrypoint.s…"   26 minutes ago   Up 26 minutes (healthy)     127.0.0.1:5432->5432/tcp                      causal-atelier-database-1
3ce6f66d0c61   ariadne-e1a-api          "uvicorn ariadne.int…"   28 minutes ago   Up 28 minutes (healthy)     127.0.0.1:18000->8000/tcp                     ariadne-e1a-api-1
3efa16c113e2   ariadne-e1a-worker       "ariadne-worker"         28 minutes ago   Up 28 minutes               8000/tcp                                      ariadne-e1a-worker-1
bad8ecbeb36a   ariadne-e1a-migrate      "alembic -c alembic_…"   28 minutes ago   Exited (0) 28 minutes ago                                                 ariadne-e1a-migrate-1
1c2b80446b87   postgres:17-alpine       "docker-entrypoint.s…"   4 days ago       Exited (0) 3 days ago                                                     ariadne-test-database_test-1
c13e8ed52c38   nginx:1.27-alpine        "/docker-entrypoint.…"   5 days ago       Up 10 hours                 127.0.0.1:18080->80/tcp                       ariadne-e1a-frontend-1
33bde72e228c   postgres:17-alpine       "docker-entrypoint.s…"   5 days ago       Up 10 hours (healthy)       127.0.0.1:15432->5432/tcp                     ariadne-e1a-database-1

```