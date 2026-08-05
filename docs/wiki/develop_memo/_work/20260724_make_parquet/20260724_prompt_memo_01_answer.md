# 20260724_prompt_memo_01 回答

## 1. parquetファイルを作るにはどのプログラムを起動すればよいか？

**Complete Journey ETL（`execute_completejourney_etl`）** を起動します。これが `data/10_interim/completejourney/*.parquet`（8テーブル）を生成します。

実体は `src/ariadne/application/pipeline/etl.py` の `execute_completejourney_etl()` で、内部で extract → transform → load を実行します。

- extract: `src/ariadne/etl/completejourney/extract.py`（`data/00_raw/completejourney/rdata` の rda/rds を読込）
- transform: `src/ariadne/etl/completejourney/transform.py`
- load: `src/ariadne/etl/completejourney/load.py`（`data/10_interim/completejourney` へ parquet 書出し）

起動方法は、チュートリアル `_work/20260719_tutorial/tutorial_01_cli.md` に記載の通り、専用CLIコマンドは無く、関数を直接呼び出す形です:

```bash
uv run python - <<'PY'
from pathlib import Path
from ariadne.application.pipeline.etl import execute_completejourney_etl

outputs = execute_completejourney_etl(Path.cwd())
for logical_name, path in sorted(outputs.items()):
    print(f"{logical_name}: {path}")
PY
```

別経路として、Worker の `src/ariadne/workers/executor.py` の `_run_etl` でも同関数が呼ばれますが、こちらは Web サービス/DB 経由の実行系です。CLI 相当で手早く作るなら上記が該当します。

> 注意: 入力元の `data/00_raw/completejourney/rdata/` は現状 `data/00_raw/` に `README_data.md` しか無く、rda/rds の生データが未配置の可能性があります。ETL 実行前に raw データの配置が必要です。

## 2. run.py の input を指定する config ファイルは何か？

`experiments/004_discovery_inference_integration/run.py` は `ariadne.interfaces.cli.pipeline:main`（= `ariadne-pipeline`）を呼ぶだけの薄いラッパーです。input を決める config は次の通りです:

- **直接の起点**: `configs/causal/inference/pipeline.yaml`
  - `run.py` の同ディレクトリにある `experiments/004_discovery_inference_integration/config.yaml` で `pipeline_config: configs/causal/inference/pipeline.yaml` と指定されています。
  - pipeline.yaml が discovery / inference 各ステージの feature_config・analysis_config・causal_design 等を参照します。

- **今回問題の parquet（データ入力）を指定している config**: `configs/etl/completejourney/load.yaml`
  - `path: {path_sys_base}/data/10_interim/completejourney` として、パイプラインが読み込む parquet の場所・ファイル名を定義しています。
  - その parquet の生成元データは `configs/etl/completejourney/extract.yaml`（`data/00_raw/completejourney/rdata`）です。

まとめると、`run.py` の設定チェーンは **config.yaml → pipeline.yaml → 各ステージ config**、データ入力(parquet)の定義は **configs/etl/completejourney/load.yaml** です。
