# 今やるべきこと
## 1. まずsource identityを確認
```
git status --short
git rev-parse HEAD

git diff --stat \
  575cdd139aea09d4f19b46ab6a6d38545f645c71..HEAD \
  -- src frontend Dockerfile compose.yaml
```
```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ git status --short
git rev-parse HEAD

git diff --stat \
  575cdd139aea09d4f19b46ab6a6d38545f645c71..HEAD \
  -- src frontend Dockerfile compose.yaml
?? docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix/_work/
135fc1213a49a0d89d2c38336527697888d6bca5
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier
```

## 2. main APIをrebuild/recreate

元コマンド

```
docker compose build api
docker compose up -d --force-recreate api

docker compose ps
curl -fsS http://127.0.0.1:8000/health/ready | jq .

curl -fsS \
  http://127.0.0.1:8000/api/v1/navigation/analysis \
  | jq .

```

実行結果

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker compose build api
[+] Building 2.9s (18/18) FINISHED                                                                                                                                                                 
 => [internal] load local bake definitions                                                                                                                                                    0.0s
 => => reading from stdin 994B                                                                                                                                                                0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                          0.0s
 => => transferring dockerfile: 957B                                                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                                                                                           1.6s
 => [internal] load .dockerignore                                                                                                                                                             0.0s
 => => transferring context: 934B                                                                                                                                                             0.0s
 => [ 1/11] FROM docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36                                                                   0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36                                                                     0.0s
 => [internal] load build context                                                                                                                                                             0.3s
 => => transferring context: 1.45MB                                                                                                                                                           0.3s
 => CACHED [ 2/11] RUN pip install --no-cache-dir uv==0.8.3                                                                                                                                   0.0s
 => CACHED [ 3/11] WORKDIR /app                                                                                                                                                               0.0s
 => CACHED [ 4/11] RUN groupadd --system causal && useradd --system --gid causal --home /app causal                                                                                           0.0s
 => CACHED [ 5/11] COPY --chmod=0644 pyproject.toml uv.lock README.md ./                                                                                                                      0.0s
 => CACHED [ 6/11] RUN uv sync --frozen --no-dev --no-install-project --no-cache                                                                                                              0.0s
 => CACHED [ 7/11] COPY --chmod=0755 src ./src                                                                                                                                                0.0s
 => CACHED [ 8/11] RUN uv sync --frozen --no-dev --no-cache                                                                                                                                   0.0s
 => CACHED [ 9/11] COPY --chmod=0644 alembic_product.ini ./                                                                                                                                   0.0s
 => CACHED [10/11] COPY --chmod=0755 product_migrations ./product_migrations                                                                                                                  0.0s
 => CACHED [11/11] RUN mkdir -p /state/objects /state/workspaces && chown -R causal:causal /state                                                                                             0.0s
 => exporting to image                                                                                                                                                                        0.4s
 => => exporting layers                                                                                                                                                                       0.0s
 => => exporting manifest sha256:55c19356059e12583d31389ac64e5ba115e52437ffe2f535dc3e2b149bfad1a9                                                                                             0.0s
 => => exporting config sha256:b30b71c764fa8084930eb84ddb81aed958d1fda8a6fddd54db7276c4c0a1844e                                                                                               0.0s
 => => exporting attestation manifest sha256:cbfbfe3c145bfc8ae25322e2654e08dcbcf0ae38247e750e041471806b9c8ff7                                                                                 0.1s
 => => exporting manifest list sha256:b956ef871fe75c91f754e5177e2f42a27dc31b8b8de992fec12db44b2548570c                                                                                        0.0s
 => => naming to docker.io/library/causal-atelier-api:latest                                                                                                                                  0.0s
 => => unpacking to docker.io/library/causal-atelier-api:latest                                                                                                                               0.0s
 => resolving provenance for metadata file                                                                                                                                                    0.0s
[+] build 1/1
 ✔ Image causal-atelier-api Built                                                                                                                                                              3.0s
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker compose up -d --force-recreate api
[+] up 3/3
 ✔ Container causal-atelier-database-1 Healthy                                                                                                                                                 1.6s
 ✔ Container causal-atelier-api-1      Started                                                                                                                                                 5.1s
 ✔ Container causal-atelier-migrate-1  Exited                                                                                                                                                  3.2s
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker compose ps
NAME                        IMAGE                   COMMAND                  SERVICE    CREATED          STATUS                            PORTS
causal-atelier-api-1        causal-atelier-api      "uvicorn ariadne.int…"   api        8 seconds ago    Up 3 seconds (health: starting)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
causal-atelier-database-1   postgres:17-alpine      "docker-entrypoint.s…"   database   51 minutes ago   Up 51 minutes (healthy)           127.0.0.1:5432->5432/tcp
causal-atelier-frontend-1   nginx:1.27-alpine       "/docker-entrypoint.…"   frontend   51 minutes ago   Up 51 minutes                     0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
causal-atelier-worker-1     causal-atelier-worker   "ariadne-worker"         worker     51 minutes ago   Up 51 minutes                     8000/tcp
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ curl -fsS http://127.0.0.1:8000/health/ready | jq .
{
  "status": "ok"
}
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ curl -fsS \
  http://127.0.0.1:8000/api/v1/navigation/analysis \
  | jq .
{
  "schema_version": "analysis-navigation/1",
  "families": [
    {
      "family": "EXPLORATORY",
      "slug": "exploratory",
      "label": "Exploratory",
      "default_stage_id": "profile",
      "stages": [
        {
          "stage_id": "profile",
          "slug": "profile",
          "label": "Profile",
          "order": 0
        },
        {
          "stage_id": "data-quality",
          "slug": "data-quality",
          "label": "Data Quality",
          "order": 1
        },
        {
          "stage_id": "distribution",
          "slug": "distribution",
          "label": "Distribution",
          "order": 2
        },
        {
          "stage_id": "relationships",
          "slug": "relationships",
          "label": "Relationships",
          "order": 3
        },
        {
          "stage_id": "comparison",
          "slug": "comparison",
          "label": "Comparison",
          "order": 4
        },
        {
          "stage_id": "findings",
          "slug": "findings",
          "label": "Findings",
          "order": 5
        }
      ]
    },
    {
      "family": "PREDICTIVE",
      "slug": "predictive",
      "label": "Predictive",
      "default_stage_id": "setup",
      "stages": [
        {
          "stage_id": "setup",
          "slug": "setup",
          "label": "Setup",
          "order": 0
        },
        {
          "stage_id": "train",
          "slug": "train",
          "label": "Train",
          "order": 1
        },
        {
          "stage_id": "predict",
          "slug": "predict",
          "label": "Predict",
          "order": 2
        },
        {
          "stage_id": "metrics",
          "slug": "metrics",
          "label": "Metrics",
          "order": 3
        },
        {
          "stage_id": "explainability",
          "slug": "explainability",
          "label": "Explainability",
          "order": 4
        },
        {
          "stage_id": "model-management",
          "slug": "model-management",
          "label": "Model Management",
          "order": 5
        }
      ]
    },
    {
      "family": "CAUSAL",
      "slug": "causal",
      "label": "Causal",
      "default_stage_id": "setup",
      "stages": [
        {
          "stage_id": "setup",
          "slug": "setup",
          "label": "Setup",
          "order": 0
        },
        {
          "stage_id": "discovery",
          "slug": "discovery",
          "label": "Discovery",
          "order": 1
        },
        {
          "stage_id": "identification",
          "slug": "identification",
          "label": "Identification",
          "order": 2
        },
        {
          "stage_id": "estimation",
          "slug": "estimation",
          "label": "Estimation",
          "order": 3
        },
        {
          "stage_id": "effects",
          "slug": "effects",
          "label": "Effects",
          "order": 4
        },
        {
          "stage_id": "diagnostics",
          "slug": "diagnostics",
          "label": "Diagnostics",
          "order": 5
        },
        {
          "stage_id": "sensitivity",
          "slug": "sensitivity",
          "label": "Sensitivity",
          "order": 6
        }
      ]
    }
  ]
}
```