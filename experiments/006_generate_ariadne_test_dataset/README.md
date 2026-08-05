# 006 Ariadne登録用テストデータ生成

## 目的

Ariadne Web Appへ登録し、DiscoveryからInferenceまでを試すための決定的なsynthetic datasetを生成する。

登録用fileは独自に列を組み立てたCSVではない。syntheticなComplete Journey形式の4 source tableを作り、既存の次の前処理を実行した戻り値をそのまま保存する。

```text
configs/preprocessing/inference_features.yaml
    -> ariadne.preprocessing.inference.config.load_feature_config
    -> ariadne.preprocessing.inference.builder.FeatureBuilder.build
    -> FeatureBuildResult.inference_frame
    -> CSV / Parquet
```

## 生成

repository rootで実行する。

```bash
uv sync --frozen --python 3.12
uv run python experiments/006_generate_ariadne_test_dataset/run.py
```

本repositoryの検証済みruntimeはPython 3.12.xである。`python --version`または既存`.venv`が3.13の場合でも、上の`uv sync --python 3.12`により`.venv`を3.12で再作成してから実行する。

既定値:

- seed: `20260805`
- 世帯数: `500`
- campaign ID: `18`
- pre-treatment window: 8週
- outcome window: 4週

出力先:

```text
artifacts/experiments/006_generate_ariadne_test_dataset/
├── ariadne_completejourney_household_test.csv      # Web登録用
├── ariadne_completejourney_household_test.parquet  # Web登録用（推奨）
├── generation_manifest.json
├── source_tables/
│   ├── campaign_descriptions.csv
│   ├── campaigns.csv
│   ├── demographics.csv
│   └── transactions.csv
└── diagnostics/
    ├── dropped_columns.csv
    └── standardized_frame.parquet
```

CSVとParquetの行・列内容は同一である。型を維持しfile sizeを小さくできるため、通常はParquetを登録する。

## Web Appへの登録値

Project / Data Workspaceで次を指定する。

| 項目 | 値 |
|---|---|
| File | `artifacts/experiments/006_generate_ariadne_test_dataset/ariadne_completejourney_household_test.parquet` |
| Dataset key | `completejourney_household_test` |
| Name | `Complete Journey synthetic household test` |
| Version label | `seed-20260805-v1` |
| Source note | `FeatureBuilder inference_frame; synthetic seed=20260805` |

同一Project、同一Dataset keyへ内容が同じfileを別Version labelで再登録するとcontent hash重複制約により拒否される。再試行時は画面が送る同じIdempotency-Keyを使用するか、既存Dataset Versionを選択する。

## Discovery推奨設定

全列を無条件に投入せず、最初は次の8列を選択する。

```text
age_midpoint
income_midpoint_k
household_size
kids_count
pre_sales_value
pre_quantity
treated
outcome_sales_value
```

Algorithm:

- PC: `alpha=0.05`
- GES: parameterなし
- random seed: `42`

known structureを試験する場合、`treated -> outcome_sales_value`をrequired edgeに指定できる。ただし、これはsynthetic DGPの既知情報を与える操作であり、dataだけから因果方向を発見したことにはならない。

## Inference推奨設定

```text
treatment: treated
outcome: outcome_sales_value
estimand: ATE
adjustment_set:
  - age_midpoint
  - age_unknown
  - income_midpoint_k
  - income_unknown
  - household_size
  - kids_count
  - pre_baskets
  - pre_quantity
  - pre_sales_value
  - pre_coupon_disc
  - pre_coupon_match_disc
  - pre_retail_disc
  - homeowner_yes
  - homeowner_unknown
  - married_yes
  - married_unknown
assumptions:
  - consistency
  - conditional_exchangeability
  - positivity
  - no_interference
```

EstimatorはOLS、IPW、AIPWの比較を推奨する。

## データ生成上の既知情報

- treatmentはbaseline demographicsと非観測のshopping affinityに依存するBernoulli割付である。
- outcome期間の週次salesへ、treated householdに対して`+3.0`を加えている。
- outcomeは4週集計なので、simulation code上の直接加算は1世帯あたり合計`+12.0`である。
- `+12.0`は生成過程のparameterであり、有限標本に対する推定値の期待一致を保証するものではない。
- shopping affinityは直接列として出力しないが、pre-period集約値がproxyとなる。したがって、これは完全に識別が保証されたbenchmarkではなく、診断・比較用synthetic dataである。

再現性は`generation_manifest.json`のseed、feature config hash、source/output SHA-256で追跡する。

## 検証

生成後、Productの実Scientific AdapterでPC、GES、OLS、IPW、AIPWを実行する。

```bash
uv run python experiments/006_generate_ariadne_test_dataset/verify.py
```

この検証ではCSV/Parquetの値一致、欠損なし、両treatment arm、adjustment列の非定数性も確認する。結果は次へ保存する。

```text
artifacts/experiments/006_generate_ariadne_test_dataset/verification/verification_summary.json
```
