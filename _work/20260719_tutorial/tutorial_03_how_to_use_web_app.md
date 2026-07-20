# causal-atelier Webアプリ利用チュートリアル

## 1. このチュートリアルで行うこと

起動済みのcausal-atelierへ分析可能な単一CSVを登録し、Frontendだけで次の一連の操作を行います。

1. Projectを作成する。
2. CSVを不変のDataset Versionとして登録する。
3. 各列のFeature Semanticsを定義してpublishする。
4. PCとGESで因果探索を実行し、グラフを比較する。
5. 採用する探索グラフをSaved Graph Versionとして保存・publishする。
6. Saved Graphを入力に、Edge WeightとTreatment Effectを推定する。
7. Run履歴と推定結果を確認する。

Web MVPはETL製品ではありません。複数raw fileのjoin、集計、時点整合、業務固有の変換等はDatabricksなどの外部ETLへ任せ、causal-atelierには「1行が1分析単位」になった単一CSVまたはParquetを登録します。

Complete Journeyの複数fileを処理する既存classとYAML設定は削除されておらず、CLIの`CONFIGURED_FEATURE_BUILD`経路で引き続き利用できます。CLI操作は`tutorial_01_cli.md`を参照してください。

## 2. 前提条件とアクセス先

repository rootへ移動し、serviceが起動していることを確認します。

```bash
cd /loc0/bigbrother/repositories/causal-atelier
docker compose ps
curl --fail http://localhost:8000/health/ready
```

起動していない場合は次を実行します。

```bash
docker compose up --build -d
```

主なアクセス先は次のとおりです。

| 用途 | URL |
|---|---|
| Frontend | `http://localhost:8080` |
| OpenAPI UI | `http://localhost:8000/docs` |
| API health check | `http://localhost:8000/health/ready` |

正常時のhealth checkは`{"status":"ready"}`を返します。

## 3. チュートリアル用の分析tableを準備する

手元に分析可能なCSVまたはParquetがあれば、それを使用できます。このチュートリアルと同じ列で試す場合は、次のPython標準libraryだけのscriptで300行のCSVを作成します。

```bash
causal_tutorial_dir=$(mktemp -d)
causal_tutorial_csv="$causal_tutorial_dir/household_campaign.csv"

python3 - "$causal_tutorial_csv" <<'PY'
import csv
import math
import random
import sys

random.seed(42)
with open(sys.argv[1], "w", newline="", encoding="utf-8") as stream:
    writer = csv.writer(stream)
    writer.writerow([
        "household_id",
        "age",
        "income",
        "baseline_sales",
        "treated",
        "outcome_sales_value",
    ])
    for household_id in range(1, 301):
        age = random.randint(20, 75)
        income = max(20_000, random.gauss(55_000 + 450 * (age - 40), 12_000))
        baseline = max(5, random.gauss(30 + 0.0006 * income + 0.35 * age, 8))
        logit = -0.4 + 0.012 * (age - 45) + 0.018 * (baseline - 65)
        probability = 1 / (1 + math.exp(-logit))
        treated = int(random.random() < probability)
        outcome = 20 + 0.42 * baseline + 0.00015 * income + 9 * treated
        outcome += random.gauss(0, 7)
        writer.writerow([
            household_id,
            age,
            round(income, 2),
            round(baseline, 2),
            treated,
            round(outcome, 2),
        ])
PY

sed -n '1,6p' "$causal_tutorial_csv"
```

このtableでは1行が1世帯を表します。`treated`はcampaign処置、`outcome_sales_value`は処置後売上、`age`、`income`、`baseline_sales`は処置前共変量です。サンプルは画面動作確認用の合成データであり、実際の業務判断には使わないでください。

## 4. Projectを作成する

Browserで`http://localhost:8080`を開きます。

1. 「新しいProject」を押す。
2. Slugへ`web-tutorial`を入力する。
3. Nameへ`Web tutorial`を入力する。
4. Descriptionへ分析目的を入力する。
5. 「作成する」を押す。
6. 作成されたProject cardを開く。

Slugは小文字英数字とhyphenを使用します。同じSlugがすでに存在する場合は、`web-tutorial-2`のように別の値を使用してください。

Projectを開くと、左側に次の4 sectionが表示されます。

| Section | 役割 |
|---|---|
| `Overview` | Dataset、Run、Saved Graphと次の操作を確認する |
| `Analysis dataset` | 単一tableを登録し、列の意味を定義する |
| `Causal discovery` | 因果探索を実行し、探索グラフを比較・保存する |
| `Causal inference` | Saved Graphを使って推定する |

## 5. 分析Datasetを登録する

左側の`Analysis dataset`を開き、「ファイルを登録」へ次を入力します。

| 項目 | 入力例 |
|---|---|
| File | 前節の`household_campaign.csv` |
| Dataset名 | `Household campaign analysis` |
| Slug | `household-campaign-analysis` |
| Logical table名 | `analysis_table` |
| Dataset kind | `PROCESSED` |
| 1行が表す分析単位 | `1行は1世帯を表す` |

「アップロードしてVersionを作成」を押します。この1操作で、Frontendは次をserverへ作成します。

- upload object
- 論理Dataset
- 内容hashで固定されたDataset Version
- 単一のDataset Table Version
- `READY`なAnalysis Dataset Binding

登録fileはDocker Composeの`artifact-data` named volumeへ保存されます。repositoryの`data/`directoryへ直接格納されるわけではありません。DatasetやVersionのmetadataはPostgreSQLの`metadata-data` named volumeへ保存されます。

画面下部の`Project datasets`にDatasetが追加され、Readinessが`READY`になっていることを確認します。Dataset Versionは不変です。内容を更新するときは、既存Versionを上書きせず、新しいfileから新しいVersionを作成します。

## 6. Feature Semanticsを定義する

upload後は、右側の「列の意味を定義」で作成したDataset Versionが選択され、列一覧が表示されます。表示されない場合はDataset Versionを選び直します。

各列を次のように設定します。

| Column | Role | Categorical | Discovery | Adjustment |
|---|---|---:|---:|---:|
| `household_id` | `identifier` | OFF | OFF | OFF |
| `age` | `covariate` | OFF | ON | ON |
| `income` | `covariate` | OFF | ON | ON |
| `baseline_sales` | `covariate` | OFF | ON | ON |
| `treated` | `treatment` | OFF | ON | OFF |
| `outcome_sales_value` | `outcome` | OFF | ON | OFF |

Roleを変更すると、一般的な安全規則に合わせてDiscoveryとAdjustmentのcheckboxも更新されます。最終状態を表と同じにしてください。

「検証してSemanticsをpublish」を押します。FrontendはFeature Semantics Configuration Versionを作成し、物理DatasetColumnとの対応、treatment／outcomeの個数、調整可否等を検証してpublishします。

通常の画面操作ではtreatmentとoutcomeをそれぞれ1列ずつ指定する必要があります。`post_treatment`、`mediator`、`collider`を安易にAdjustmentへ含めないでください。roleは列の意味、Adjustmentは調整集合へ採用してよいかを表す別の宣言です。

## 7. 因果探索を実行する

左側の`Causal discovery`を開き、次を設定します。

| 項目 | 設定例 |
|---|---|
| 分析Dataset Version | 前節で登録したVersion |
| Feature Semantics | 前節でpublishしたSemantics |
| Algorithms | `PC`と`GES`をON |
| 有意水準 α | `0.01` |
| Random seed | `42` |
| 実行モード | `RUN` |
| Bootstrap samples | `0` |

`Algorithm input conditioning`は、まず既定値を使用します。

| Conditioning | 既定値 | 意味 |
|---|---|---|
| 欠損値 | `Complete case` | 欠損のある行を除外する |
| Categorical encoding | `Ordinal codes` | categorical列を整数codeへ変換する |
| Collinearity threshold | `0.995` | 強い共線性を持つ後続列を除外する |

入力table自体は変更されません。Runごとに実際に選択・除外した列、conditioning条件、分析用feature frameが来歴として記録されます。

「因果探索を実行」を押します。Run monitorが`SUCCEEDED`になると、結果は自動でGraph Explorerへ読み込まれます。自動表示されない場合は、`Discovery Run`から対象Runを選び「Runから読込」を押します。

`DRY RUN`は解決済みExecution Planの確認、`VALIDATE ONLY`は入力整合性の検証に使います。どちらも探索algorithmを実行しないため、探索グラフは生成されません。

## 8. 探索グラフを比較して保存する

Graph Explorerでは、algorithm名のtabを切り替えると各グラフを単体表示できます。PCとGESの両方が成功していれば、「並べて比較」で次を確認できます。

- 共通するedge
- PCだけに現れたedge
- GESだけに現れたedge
- endpointの向きや未確定性

探索結果はalgorithmと仮定に依存する構造仮説であり、真のDAGが証明されたものではありません。業務知識、時間順序、測定過程と矛盾していないかを確認してください。

採用するalgorithmのtabへ戻り、「このグラフを保存してpublish」を押します。これにより、選択したDiscovery ResultをsourceとするCausal Graph Versionがserver側へ保存され、`PUBLISHED`になります。

保存されたグラフはBrowserのlocal storageではなく、PostgreSQLとArtifact Storeが正本です。Dataset Version、Feature Semantics、元のDiscovery Resultへの来歴も保持されます。

## 9. Edge Weightを推定する

左側の`Causal inference`を開きます。

1. 分析modeで`Edge weight`を選ぶ。
2. 「保存した探索グラフVersion」で前節の`PUBLISHED` Graphを選ぶ。
3. Dataset VersionとFeature Semanticsが自動選択されたことを確認する。
4. 実行モードを`RUN`、Random seedを`42`にする。
5. 「因果推論を実行」を押す。

Saved Graph、Dataset Version、Feature Semanticsは同じDiscovery来歴の組合せでなければなりません。Graphを選ぶと対応するDatasetとSemanticsが自動入力されるため、通常は変更しません。

Runが`SUCCEEDED`になると「推論結果」にedgeごとの係数、95%信頼区間、p-value、sample数、statusが表示されます。過去結果は`Inference Run`を選び「Runから読込」で再表示できます。

Edge Weightは探索edgeに対する探索的な回帰係数です。それだけで識別済みの因果効果を意味しません。

## 10. Treatment Effectを推定する

同じ`Causal inference`画面で分析modeを`Treatment effect`へ切り替え、次を入力します。

| 項目 | 入力例 |
|---|---|
| 保存した探索グラフVersion | 前節でpublishしたGraph |
| Treatment | `treated` |
| Outcome | `outcome_sales_value` |
| Estimand | `ATE` |
| 調整戦略 | `Pre-treatment covariates` |
| Adjustment set | `age,income,baseline_sales` |
| 推定手法 | `diff_in_means,ols_coefficient,g_computation_ate,ipw_ate` |
| Target population | `登録した300世帯と同じ対象集団` |
| 因果仮定 | 1行ずつ`consistency`、`exchangeability given age, income, baseline_sales`、`positivity` |
| 実行モード | `RUN` |
| Random seed | `42` |

「因果推論を実行」を押すと、Frontendは入力内容からCausal Designを作成・検証・publishし、そのVersionとSaved Graphを固定入力にしたInference Runを投入します。

検証では少なくとも次の整合性が確認されます。

- Dataset Version、Feature Semantics、Saved Graphが同じ来歴を持つ。
- TreatmentとOutcomeがSemanticsのrole宣言と一致する。
- TreatmentとOutcomeがSaved Graphのnodeとして存在する。
- Adjustment setがSemantics上で調整可能である。
- post-treatment、mediator、collider等の危険なroleが調整集合へ混入していない。

Runが`SUCCEEDED`になると、method別の推定値、95%信頼区間、p-value、sample数、選択された調整変数、診断が表示されます。

推定値は宣言したconsistency、exchangeability、positivity等の仮定の下で解釈します。causal-atelierは仮定と来歴を固定し診断を提示しますが、因果識別の成立を自動証明しません。

## 11. RunとResultの来歴を確認する

DiscoveryとInferenceの各画面下部にRun履歴があります。Run ID、status、mode、作成日時を確認でき、完了済みRunのResultを再読込できます。

より詳細な情報はOpenAPI UI（`http://localhost:8000/docs`）またはAPIから確認できます。

```text
GET /api/v1/runs/{run_id}
GET /api/v1/runs/{run_id}/events
GET /api/v1/runs/{run_id}/artifacts
GET /api/v1/runs/{run_id}/results
GET /api/v1/artifacts/{artifact_id}/content
GET /api/v1/artifacts/{artifact_id}/lineage
GET /api/v1/causal-graph-versions/{version_id}
```

`GET /api/v1/runs/{run_id}/results`は、RunからDiscovery、Edge Weight、Treatment Effectの各Resultへ移動するための入口です。UUIDを手入力してResultを探す必要はありません。

## 12. 保存場所とservice再起動

Webから登録したresourceは次の場所へ永続化されます。

| 内容 | 保存先 |
|---|---|
| Project、Dataset、Version、Semantics、Run、Result、Saved Graph等のmetadata | PostgreSQL (`metadata-data` volume) |
| uploadしたCSV/Parquet、Run成果物、Saved Graph JSON | Artifact Store (`artifact-data` volume) |
| CLIが直接扱うComplete Journeyのraw／interim data | repositoryの`data/`配下 |

serviceだけを停止する場合、volumeは残ります。

```bash
docker compose down
```

再開後も登録内容を利用できます。

```bash
docker compose up -d
```

`docker compose down --volumes`はPostgreSQL metadataとArtifact Storeを含む全volumeを削除します。登録済みProject、Dataset、Saved Graph、Run結果が不要だと確認できた場合だけ使用してください。

## 13. Projectを論理削除する

Projectを開き、`Overview`の「編集」から「Projectを削除」を押します。確認画面へ表示されたProject slugを正確に入力すると、「論理削除する」が有効になります。

この操作を実行できるのは`PROJECT_ADMIN`だけです。削除後はProject一覧へ戻り、対象Projectは表示されなくなります。

この操作は論理削除です。Dataset、Run、Saved Graph、Artifactはretention policyに従って保持されますが、現在のFrontendにはProjectを復元する機能がありません。Projectを間違えて削除した場合は、metadataを直接変更せず、運用管理者へ連絡してください。

## 14. よくある問題

### Dataset Versionを選んでも列が表示されない

- uploadが成功し、`Project datasets`にVersionが追加されているか確認する。
- DatasetのReadinessが`READY`か確認する。
- `Analysis dataset`画面の「更新」を押してからVersionを選び直す。
- APIまたはworkerのlogを確認する。

```bash
docker compose logs --tail=200 api worker
```

### Semanticsをpublishできない

- treatmentとoutcomeをそれぞれ正確に1列指定する。
- identifier、excluded、post-treatment列がDiscovery／AdjustmentでONになっていないか確認する。
- AdjustmentをONにする列は原則として処置前の`covariate`に限定する。

### Runが進まない

```bash
docker compose ps worker
docker compose logs --tail=200 worker
```

workerが停止していれば再開します。

```bash
docker compose up -d worker
```

### Discovery Runは成功したがグラフがない

- 実行モードが`RUN`だったか確認する。`DRY RUN`と`VALIDATE ONLY`は結果を生成しない。
- Run履歴で対象Runが`SUCCEEDED`か確認する。
- `Discovery Run`を選び「Runから読込」を押す。
- algorithmが入力データに対してedgeを検出しない場合、空のグラフも正常な探索結果になり得る。

### Inferenceで来歴不一致になる

Saved Graphを選び直し、自動設定されたDataset VersionとFeature Semanticsをそのまま使用してください。別Datasetや別Semanticsと手作業で組み替えることはできません。

### Treatment EffectのCausal Design検証に失敗する

- Treatment／Outcomeの名前がSemanticsの列名と完全一致しているか確認する。
- Saved GraphにTreatment／Outcome nodeが存在するか確認する。
- Adjustment setをカンマ区切りで入力し、各列が`covariate`かつAdjustment ONか確認する。
- mediator、collider、post-treatment列を調整集合から外す。

### `401`、`403`、`404`になる

Frontendはdevelopment認証で`X-User-Subject: local-developer`を使用します。curlやSwaggerから同じProjectを操作する場合も同じsubjectを使用してください。異なるsubjectは別利用者として扱われます。

Project一覧は表示されるのに詳細画面で一部Resourceが`Not Found`になる場合は、FrontendとAPI containerのversionが一致していない可能性があります。FrontendはHostのsourceをbind mountしていますが、APIとworkerはbuild済みimageを使用するため、Backend変更後は次を実行してください。

```bash
docker compose up --build -d migrate api worker frontend
```

再build後、Browser側もcacheを無視して再読み込みします。
