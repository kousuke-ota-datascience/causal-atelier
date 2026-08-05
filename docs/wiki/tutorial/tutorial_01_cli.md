# ariadne CLIチュートリアル

## 1. このチュートリアルで行うこと

ariadneのCLIには、次の3つの入口があります。

| コマンド | 用途 |
|---|---|
| `ariadne-discovery` | 因果探索だけを実行する |
| `ariadne-inference` | Edge WeightまたはTreatment Effect推定だけを実行する |
| `ariadne-pipeline` | 因果探索から因果推論までを一つの再現可能なRunとして実行する |

通常は、manifest生成とstage間の整合性検査を含む`ariadne-pipeline`を推奨します。

このCLIフローは、Complete Journeyの複数raw fileをETLし、設定YAMLに基づいて特徴量を構築する`CONFIGURED_FEATURE_BUILD`経路です。既存の前処理classと設定資産を利用するための入口として、今後も維持します。

一方、Web MVPの通常フローは、Databricks等の外部ETLで作成した分析可能な単一CSV/Parquetを受け取る`ANALYSIS_READY`経路です。Web画面からComplete Journeyの複数raw fileを対応付けたり、このチュートリアルのETLを起動したりはしません。Webの操作は`tutorial_03_how_to_use_web_app.md`を参照してください。

以降のコマンドは、repository rootで実行してください。

```bash
cd /datadrive/user_work/[USER_NAME]/ariadne
```

## 2. 実行環境を準備する

必要なものはPython 3.13以上、`uv`、Gitです。

```bash
python --version
uv --version
git --version
uv sync --all-groups --python 3.12
```

CLIがインストールされたことを確認します。

```bash
uv run ariadne-discovery --help
uv run ariadne-inference --help
uv run ariadne-pipeline --help
```

## 3. CLI用のComplete Journeyデータを準備する

既定設定は、Complete Journeyのraw dataを次の場所から読み込みます。

```text
data/00_raw/completejourney/rdata/
  campaign_descriptions.rda
  campaigns.rda
  coupon_redemptions.rda
  coupons.rda
  demographics.rda
  products.rda
  promotions.rds
  transactions.rds
```

データは[completejourney upstream repository](https://github.com/bradleyboehmke/completejourney/tree/master/data)から取得できます。次は一時directoryへcloneして必要なファイルだけを配置する例です。

```bash
completejourney_checkout=$(mktemp -d)
git clone --depth 1 \
  https://github.com/bradleyboehmke/completejourney.git \
  "$completejourney_checkout"

mkdir -p data/00_raw/completejourney/rdata
cp \
  "$completejourney_checkout/data/campaign_descriptions.rda" \
  "$completejourney_checkout/data/campaigns.rda" \
  "$completejourney_checkout/data/coupon_redemptions.rda" \
  "$completejourney_checkout/data/coupons.rda" \
  "$completejourney_checkout/data/demographics.rda" \
  "$completejourney_checkout/data/products.rda" \
  "$completejourney_checkout/data/promotions.rds" \
  "$completejourney_checkout/data/transactions.rds" \
  data/00_raw/completejourney/rdata/
```

配置を確認します。

```bash
find data/00_raw/completejourney/rdata -maxdepth 1 -type f | sort
```

raw dataを正規化し、CLIが利用するParquetへ変換します。

```bash
uv run python - <<'PY'
from pathlib import Path

from ariadne.application.pipeline.etl import execute_completejourney_etl

outputs = execute_completejourney_etl(Path.cwd())
for logical_name, path in sorted(outputs.items()):
    print(f"{logical_name}: {path}")
PY
```

次のdirectoryに8個のParquetが作成されます。

```bash
find data/10_interim/completejourney -maxdepth 1 -name '*.parquet' | sort
```

## 4. 実行前に計画を確認する

`--dry-run`は分析処理やvalidationを実行せず、解決後の設定path、stage引数、出力先をJSONで表示します。

```bash
uv run ariadne-pipeline \
  --project-root "$PWD" \
  --pipeline-config configs/causal/inference/pipeline.yaml \
  --run-id tutorial-dry-run \
  --dry-run
```

次に、設定ファイル、feature semantics、causal design、adjustment setを検査します。分析stage自体は実行されません。

```bash
uv run ariadne-pipeline \
  --project-root "$PWD" \
  --pipeline-config configs/causal/inference/pipeline.yaml \
  --run-id tutorial-validation \
  --validate-only
```

成功時は`validation status: ok`と`errors: none`が表示されます。

## 5. 因果探索からEdge Weight推定まで実行する

既定のInference modeは`edge_weight`です。次のコマンドはPCによる因果探索を行い、探索edgeごとの回帰係数を推定します。

```bash
uv run ariadne-pipeline \
  --project-root "$PWD" \
  --pipeline-config configs/causal/inference/pipeline.yaml \
  --run-id tutorial-edge-weight \
  --random-seed 42 \
  --discovery-algorithms pc \
  --inference-mode edge_weight
```

主な出力は次のとおりです。

```text
artifacts/pipelines/causal_discovery/
  algorithm_summary.csv
  graph.md
  manifest.yaml
  pc/edges.csv

artifacts/pipelines/causal_inference/
  edge_weight/edge_effects.csv
  edge_weight/edge_effects.md
  manifest.yaml
```

確認例:

```bash
sed -n '1,40p' artifacts/pipelines/causal_discovery/graph.md
sed -n '1,20p' artifacts/pipelines/causal_inference/edge_weight/edge_effects.csv
```

Edge Weightは探索された関係に対する探索的係数であり、それだけで識別済みの因果効果を意味しません。

## 6. Treatment Effectを推定する

Complete Journeyの既定causal designでは、処置を`treated`、結果を`outcome_sales_value`、estimandを`ATE`としています。

```bash
uv run ariadne-pipeline \
  --project-root "$PWD" \
  --pipeline-config configs/causal/inference/pipeline.yaml \
  --run-id tutorial-treatment-effect \
  --random-seed 42 \
  --discovery-algorithms pc \
  --inference-mode treatment_effect \
  --inference-treatment treated \
  --inference-outcome outcome_sales_value \
  --inference-estimand ATE \
  --inference-adjustment-strategy pre_treatment_covariates \
  --inference-effect-methods diff_in_means ols_coefficient g_computation_ate ipw_ate
```

主な結果と診断は次に出力されます。

```text
artifacts/pipelines/causal_inference/treatment_effect/
  treatment_effects.csv
  treatment_effects.md
  selected_adjustment_set.csv
  balance_table.csv
```

```bash
sed -n '1,30p' \
  artifacts/pipelines/causal_inference/treatment_effect/treatment_effects.csv
sed -n '1,80p' \
  artifacts/pipelines/causal_inference/treatment_effect/treatment_effects.md
```

推定値だけでなく、調整変数、balance、overlap、positivity等の診断と、宣言した識別仮定を併せて評価してください。本サービスは識別仮定の成立を自動証明しません。

## 7. 個別CLIを使用する

### 7.1. Discoveryのみ

```bash
uv run ariadne-discovery \
  --project-root "$PWD" \
  --analysis-config configs/causal/discovery.yaml \
  --feature-config configs/preprocessing/discovery_features.yaml \
  --campaign-id 18 \
  --algorithms pc \
  --alpha 0.01 \
  --random-seed 42 \
  --output-dir "$PWD/artifacts/tutorial/discovery"
```

個別Discovery CLIはstage-localな成果物を作成します。次のInference stageへ確実に接続する場合は、Discovery manifestを生成する統合Pipelineを使用してください。

### 7.2. 既存Discovery manifestを使ってInferenceのみ

統合Pipelineなどで`manifest.yaml`がすでに存在する場合は、Inferenceだけを再実行できます。

```bash
uv run ariadne-inference \
  --project-root "$PWD" \
  --config configs/causal/inference/defaults.yaml \
  --feature-config configs/preprocessing/inference_features.yaml \
  --discovery-manifest "$PWD/artifacts/pipelines/causal_discovery/manifest.yaml" \
  --mode edge_weight \
  --algorithms pc \
  --output-dir "$PWD/artifacts/tutorial/inference"
```

## 8. 設定と上書きの考え方

主要設定は次のファイルにあります。

| ファイル | 内容 |
|---|---|
| `configs/causal/inference/pipeline.yaml` | stage構成と共通Run設定 |
| `configs/causal/discovery.yaml` | 因果探索algorithm、alpha、bootstrap等 |
| `configs/causal/inference/defaults.yaml` | Inference mode、estimand、推定method等 |
| `configs/preprocessing/discovery_features.yaml` | Discovery特徴量 |
| `configs/preprocessing/inference_features.yaml` | Inference特徴量とadjustment set |
| `configs/preprocessing/feature_semantics.yaml` | featureの役割と調整可否 |
| `configs/causal/inference/designs/completejourney_household.yaml` | treatment、outcome、estimand、仮定 |

CLIで指定した値はYAML設定を上書きします。再現性のため、実行時に使用したコマンド、`run-id`、random seed、生成されたmanifestを一緒に保存してください。

## 9. よくあるエラー

### rawまたはParquetが見つからない

- raw dataが`data/00_raw/completejourney/rdata`にあるか確認する。
- ETL後のParquetが`data/10_interim/completejourney`にあるか確認する。
- repository root以外から実行する場合は`--project-root`を明示する。

### `missing discovery manifest`

Inferenceだけを実行する前に統合PipelineのDiscovery stageを完了するか、正しい`--discovery-manifest`を指定してください。

### `lingam`または`notears`が利用できない

これらはoptional algorithmです。標準依存だけでチュートリアルを実行する場合は`--discovery-algorithms pc`を使用してください。

### validation error

まず`--dry-run`で解決pathを確認し、次に`--validate-only`でfeature semantics、causal design、adjustment setの不一致を確認してください。
