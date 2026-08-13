# 3. 次に実行してほしいのは、これ1つ

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ for url in \
  http://127.0.0.1:8080/api/v1/navigation/analysis \
  http://127.0.0.1:8000/api/v1/navigation/analysis \
  http://127.0.0.1:18080/api/v1/navigation/analysis \
  http://127.0.0.1:18000/api/v1/navigation/analysis
do
  echo
  echo "===== $url ====="
  curl -sS -w '\nHTTP_STATUS=%{http_code}\n' "$url" | head -c 10000
  echo
done

===== http://127.0.0.1:8080/api/v1/navigation/analysis =====
{"detail":"Not Found"}
HTTP_STATUS=404


===== http://127.0.0.1:8000/api/v1/navigation/analysis =====
{"detail":"Not Found"}
HTTP_STATUS=404


===== http://127.0.0.1:18080/api/v1/navigation/analysis =====
{"schema_version":"analysis-navigation/1","families":[{"family":"EXPLORATORY","slug":"exploratory","label":"Exploratory","default_stage_id":"profile","stages":[{"stage_id":"profile","slug":"profile","label":"Profile","order":0},{"stage_id":"data-quality","slug":"data-quality","label":"Data Quality","order":1},{"stage_id":"distribution","slug":"distribution","label":"Distribution","order":2},{"stage_id":"relationships","slug":"relationships","label":"Relationships","order":3},{"stage_id":"comparison","slug":"comparison","label":"Comparison","order":4},{"stage_id":"findings","slug":"findings","label":"Findings","order":5}]},{"family":"PREDICTIVE","slug":"predictive","label":"Predictive","default_stage_id":"setup","stages":[{"stage_id":"setup","slug":"setup","label":"Setup","order":0},{"stage_id":"train","slug":"train","label":"Train","order":1},{"stage_id":"predict","slug":"predict","label":"Predict","order":2},{"stage_id":"metrics","slug":"metrics","label":"Metrics","order":3},{"stage_id":"explainability","slug":"explainability","label":"Explainability","order":4},{"stage_id":"model-management","slug":"model-management","label":"Model Management","order":5}]},{"family":"CAUSAL","slug":"causal","label":"Causal","default_stage_id":"setup","stages":[{"stage_id":"setup","slug":"setup","label":"Setup","order":0},{"stage_id":"discovery","slug":"discovery","label":"Discovery","order":1},{"stage_id":"identification","slug":"identification","label":"Identification","order":2},{"stage_id":"estimation","slug":"estimation","label":"Estimation","order":3},{"stage_id":"effects","slug":"effects","label":"Effects","order":4},{"stage_id":"diagnostics","slug":"diagnostics","label":"Diagnostics","order":5},{"stage_id":"sensitivity","slug":"sensitivity","label":"Sensitivity","order":6}]}]}
HTTP_STATUS=200


===== http://127.0.0.1:18000/api/v1/navigation/analysis =====
{"schema_version":"analysis-navigation/1","families":[{"family":"EXPLORATORY","slug":"exploratory","label":"Exploratory","default_stage_id":"profile","stages":[{"stage_id":"profile","slug":"profile","label":"Profile","order":0},{"stage_id":"data-quality","slug":"data-quality","label":"Data Quality","order":1},{"stage_id":"distribution","slug":"distribution","label":"Distribution","order":2},{"stage_id":"relationships","slug":"relationships","label":"Relationships","order":3},{"stage_id":"comparison","slug":"comparison","label":"Comparison","order":4},{"stage_id":"findings","slug":"findings","label":"Findings","order":5}]},{"family":"PREDICTIVE","slug":"predictive","label":"Predictive","default_stage_id":"setup","stages":[{"stage_id":"setup","slug":"setup","label":"Setup","order":0},{"stage_id":"train","slug":"train","label":"Train","order":1},{"stage_id":"predict","slug":"predict","label":"Predict","order":2},{"stage_id":"metrics","slug":"metrics","label":"Metrics","order":3},{"stage_id":"explainability","slug":"explainability","label":"Explainability","order":4},{"stage_id":"model-management","slug":"model-management","label":"Model Management","order":5}]},{"family":"CAUSAL","slug":"causal","label":"Causal","default_stage_id":"setup","stages":[{"stage_id":"setup","slug":"setup","label":"Setup","order":0},{"stage_id":"discovery","slug":"discovery","label":"Discovery","order":1},{"stage_id":"identification","slug":"identification","label":"Identification","order":2},{"stage_id":"estimation","slug":"estimation","label":"Estimation","order":3},{"stage_id":"effects","slug":"effects","label":"Effects","order":4},{"stage_id":"diagnostics","slug":"diagnostics","label":"Diagnostics","order":5},{"stage_id":"sensitivity","slug":"sensitivity","label":"Sensitivity","order":6}]}]}
HTTP_STATUS=200

```

# 4. 可能ならhash比較もする

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ for port in 8000 18000; do
  echo "===== $port ====="
  curl -fsS "http://127.0.0.1:$port/api/v1/navigation/analysis" \
    | jq -S . \
    | sha256sum
done
===== 8000 =====
curl: (22) The requested URL returned error: 404
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
===== 18000 =====
c98a4611bd9fa2771eabd741baee8272da71549aced3769c528608c2a96c72bd  -
```

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ curl -fsS http://127.0.0.1:8000/api/v1/navigation/analysis | jq .
curl -fsS http://127.0.0.1:18000/api/v1/navigation/analysis | jq .
curl: (22) The requested URL returned error: 404
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