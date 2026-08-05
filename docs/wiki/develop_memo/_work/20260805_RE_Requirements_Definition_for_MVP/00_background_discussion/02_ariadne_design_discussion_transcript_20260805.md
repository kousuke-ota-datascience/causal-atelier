# Ariadne設計討議 チャット記録

> 注: 可視のユーザー・アシスタント発言を時系列で収録している。システム指示、内部ツール呼出し、内部推論は含めない。添付・生成ファイルは内容を埋め込まず、ファイル名のみ記載する。

---

## User — 2026-08-05T00:18:53Z

まずはこれを読み込んでほしい

@Web search

添付ファイル:

- `ariadne_20260804_160757.zip`

## Assistant

アップロードされたZIPの構成と主要ファイルを確認し、内容の全体像を整理します。必要に応じて、外部依存や仕様だけWebで確認します。

## Assistant

全体は338ファイルで、因果探索・因果推論の数値実装に加え、FastAPI／PostgreSQL／worker／artifact store／静的フロントエンドを含む構成です。次に、現行アーキテクチャと直近の設計変更を優先して読みます。

## Assistant

読み込みました。対象はアップロードされたZIP `ariadne_20260804_160757.zip` です。

## 把握した全体像

### 1. プロダクトの目的

Ariadneは、以下を一体化した因果分析基盤です。

- ETL
- 分析用前処理
- 因果探索
- 因果効果推定
- 実行・成果物・設定・データセットの管理
- FastAPIによるControl Plane
- PostgreSQL Metadata DB
- 非同期Worker
- Local／S3／Azure Blob Artifact Store
- 静的Webフロントエンド
- MLflow実験追跡

単なる分析ライブラリではなく、**因果分析を実行・監査・再現するためのWebプラットフォーム**として設計されています。

### 2. 規模

確認できた範囲では、概ね以下です。

| 指標 | 値 |
|---|---:|
| ファイル数 | 338 |
| PythonソースLOC | 約23,870 |
| テストLOC | 約5,291 |
| SQLAlchemyテーブルモデル | 65 |
| Alembic revision | 4 |
| CLI | discovery / inference / pipeline |
| Web実行基盤 | API / Worker / Outbox / Stage Attempt |

特に大きいモジュールは次です。

- `domain/metadata.py`
- `application/run_execution/services.py`
- `workers/executor.py`
- `causal/discovery/config.py`
- `causal/inference/estimators/treatment_effect.py`

### 3. 現在の主要な設計境界

#### Web/API経路

- Ariadneの`Execution`を作成する
- `execution_id`が主識別子
- Metadata DBを使用する
- WorkerがStageを実行する
- MLflow RunはWorker側で冪等に確保する

#### CLI経路

- Ariadneの`Execution`を作成しない
- DB接続を必須にしない
- `run_label`は人間向けラベル
- MLflow有効時は`mlflow_run_id`を追跡識別子とする
- 擬似的なExecution IDやUUIDは生成しない

この区別は、直近のP0修正で明示的に整理されています。

### 4. 直近の修正履歴

重点的に読んだのは以下です。

#### P0

- 要件正本の矛盾解消
- CLIとWebのExecution Identity分離
- Alembic migrationからORM依存を除去
- 要件トレーサビリティと機能要件テストの整備

#### P1

- MLflow Port／Adapter／NullTrackerの導入
- WorkerでのMLflow Run冪等生成・障害回復
- Discovery CLIに集中していた責務のApplication Serviceへの分離
- CLI・Pipeline・Workerが同一のDiscovery Application Serviceを利用する構造への変更

MLflowの実装メモにある、`MlflowClient.create_run()`へ辞書形式のタグを渡し、`log_batch()`へ`Metric`、`Param`、`RunTag`の列を渡すという理解は、現在の公式API記述とも整合しています。

## 因果推論機能についての認識

### 実装済みまたは部分実装

- PC、GES、LiNGAM、NOTEARS
- ATE／ATT
- 差の平均
- OLS
- g-computation
- IPW
- AIPW
- robust SE
- propensity clipping
- cross-fitting設定
- balance／overlap／outcome diagnostics
- Feature Semantics
- adjustment set validation
- discovery結果とtreatment-effect結果の区別
- artifact lineage、config hash、manifest

### 未完成と自己評価されている領域

- 因果的問いのversioned resource
- Identificationを独立Stageとして扱う仕組み
- `NOT_IDENTIFIED`を正規の分析結果として保存する仕組み
- CPDAG／PAGの型とendpoint表現
- refutation／falsification
- 未観測交絡感度分析
- CATE／HTE
- DiD、RDD、Synthetic Control
- policy evaluation
- 時系列因果探索
- graph uncertaintyの下流推論への伝播
- effect／overlap／graph drift monitoring

## 現時点の暫定評価

**事実:** 実装されている因果科学機能よりも、Metadata DB、Execution管理、version管理、artifact lineage、Web APIのモデルがかなり大きい構成です。

**暫定仮説:** 「分析コードをWebから再現可能に動かすMVP」に対しては、Control Planeとデータモデルが先行して肥大化している可能性があります。65テーブル、複数のExecution／Stage／Attempt／Input Preparation／Projection／Eventモデルは、その兆候です。

ただし、これはまだ**過剰設計であるとの確定評価ではありません**。必要な利用者数、同時実行、監査要件、データ保持要件、将来のマルチテナント要件によっては妥当化されます。

なお、今回は構成、主要コード、正本要件、直近の修正文書を読み込んだ段階です。フルテストスイートの再実行や、全338ファイルの逐行レビューまでは実施していません。

---

## User — 2026-08-05T00:23:36Z

過剰設計はどこに記載されていた？

@Web search

## Assistant

前回の「過剰設計」という表現が、ZIP内の記載に由来するのか、私の評価だったのかを切り分けます。まずリポジトリ内を全文検索し、その後、外部公開情報に同趣旨の記載があるかを確認します。

## Assistant

**ZIP内に「過剰設計」と明記された箇所はありません。**  
前回の表現は、記載内容の引用ではなく、私の暫定評価でした。区別が不十分でした。

## 確認結果

リポジトリ全体に対して、以下を全文検索しました。

```text
過剰設計
過剰な設計
オーバーエンジニアリング
over-engineering
overdesign
over-design
肥大化
unnecessary complexity
premature abstraction
```

**該当は0件**です。

Web検索も補助的に実施しましたが、このZIPに対応する公開リポジトリや、「過剰設計」と評価した外部資料は確認できませんでした。

## 私が判断材料にした記載

### README

`README.md:10-12`

```text
FastAPI control plane、PostgreSQL metadata DB、非同期worker、
Local/S3/Azure Blob Artifact Store、静的Frontendを含むMVP実装を提供します。
```

ここには多数の基盤コンポーネントが列挙されていますが、**過剰であるとは書かれていません**。

### Frontend関連メモ

`docs/wiki/develop_memo/_work/20260720_expand_flontend/openapi_feature_catalog.md:302`

```text
現状は「API中心の分析Control Planeに、
Project作成用の最小Frontendを載せた状態」です。
```

これも現状説明であり、過剰設計という評価ではありません。

### コード構造

私が前回挙げた以下の点も、リポジトリから観察した構造です。

- 多数のMetadata DBテーブル
- Execution／Stage／Attempt／Outboxの管理
- 複数Artifact Store対応
- 設定やリソースのversion管理
- API、Worker、CLI、MLflowの実行経路

ただし、これらは**複雑性の存在を示す事実**であって、過剰性を直接証明するものではありません。

## 「過剰設計」という語の出所

この会話に付与されているプロジェクト文脈に、**「因果推論）アプリの過剰設計修正」**という題名があります。私はそれを分析目的として受け取り、コードの構造をその観点から評価しました。

したがって、正確には次のとおりです。

- **事実:** ZIP内に「過剰設計」との記載はない。
- **事実:** ZIP内では、この構成を「MVP」と表現している。
- **推論:** MVPとしては管理基盤の比重が大きい可能性がある。
- **未証明:** その複雑性が実際に不要、すなわち過剰設計であるかどうか。
- **誤りだった点:** 前回、「自己評価されている」「過剰設計の兆候」と書いたため、リポジトリ内にその評価が記載されているように読めたこと。

「過剰設計」は資料から読み取った結論ではなく、**プロジェクト文脈を踏まえて私が置いた検証仮説**です。

---

## User — 2026-08-05T00:27:08Z

これ読込んで。

添付ファイル:

- `Ariadne設計討議_引継サマリー.md`

## Assistant

読み込みました。

前回のZIP単体とは異なり、この引継ぎサマリーには**「過剰設計」について明示的な評価と検討方針**が記載されています。

## 把握した要点

### 現状評価

- 本番・実業務での稼働実績はない。
- 主にCLI上で計算経路を確認した段階。
- Webを通じた分析者の利用検証は未実施。
- 現状はMVPというより、**Engineering Prototype / Technical Vertical Slice**と位置付ける。
- 実利用前にエンタープライズ級の実行・メタデータ管理を先行実装しており、**過剰設計リスクが高い**。

### 過剰設計に関する中心命題

この文書の重要な区別は次です。

```text
概念として必要
≠ 独立エンティティとして必要
≠ 独立テーブルとして必要
≠ 利用者への必須入力項目として必要
```

つまり、Ariadneの意味論を削るのではなく、**意味論上の概念をすべて物理ERへ展開することを抑制する**方針です。

### Ariadneの意味論的な背骨

維持すべき概念は以下です。

```text
Project
Research Context
Analysis Specification
Execution Plan
Execution
Result
Artifact
Claim / Interpretation
```

ただし、これらを直ちに独立Resource・独立テーブルにする必要はありません。

### 独立エンティティ化を避ける候補

当面、以下はVersioned JSON、canonical document、親Resourceのsnapshotなどで扱う候補です。

- Research Topic
- Research Question
- Significance
- Hypothesis
- Claim
- Execution Plan

独立化する条件として、独立ライフサイクル、N:M関係、独立検索、承認、差分監査、再利用などが挙げられています。

### 最小集約候補

```text
Project
Analysis Definition Version
Execution
Result / Artifact
```

これは、豊かな意味論を保持しつつ、初期物理モデルを縮約する案です。

### 現行ERの評価

比較的維持理由が強いもの:

- `project`
- `dataset`
- `dataset_version`
- `configuration`
- `configuration_version`
- `execution`
- `stage_execution`
- `stage_attempt`
- `artifact`
- `execution_event`
- `outbox_event`
- `audit_event`
- `causal_graph`
- `causal_graph_version`

統合・再評価候補:

- `execution_plan`
- stage input系テーブル
- stage parameter
- planning時／attempt時のinput preparation
- 低利用・未使用projection
- `execution_result_summary`
- Supporting領域の一部

### 今後の進め方

文書は、既存ERからユースケースを作るのではなく、次の順序を要求しています。

```text
利用者の判断
→ 必要な証拠
→ 証拠を生成する分析
→ 保持すべき来歴
→ 最小論理構造
→ 現行ERとの差分
```

優先ユースケースは次の2つです。

1. 探索的分析から候補仮説を得る
2. 明示した仮説または分析目的を評価する

## 前回回答との関係

前回、私はZIP内に「過剰設計」との記載はないと回答しました。それ自体は正しいです。

今回のファイルには、明確に以下の趣旨が記載されています。

- 過剰設計リスクが高い
- 現行ERは完成仕様ではなく最大構成の設計仮説
- 概念モデルをそのまま物理ERへ展開してはいけない
- 利用者検証から最小構成を逆算する

したがって、以降はこの引継ぎサマリーを**設計討議の前提資料**として扱います。

---

## User — 2026-08-05T00:27:58Z

つーわけで、検証シナリオを考えるところから。

## Assistant

検証シナリオは「既存ERを正当化するため」ではなく、「利用者の判断に必要な最小構造を発見するため」に設計します。まず優先2ケースを、観察可能な仮説・成功条件・必要情報まで落とします。

## Assistant

まず押さえるべき点があります。

## 結論

引継ぎサマリーのUC-01、UC-02は、現状では**ユースケースの骨格**であり、まだ「検証シナリオ」にはなっていません。

検証シナリオにするには、少なくとも次を固定する必要があります。

```text
誰が
どのような状況で
何を判断するために
どの作業を行い
何を成果として残し
何が起きれば仮説を支持／棄却するか
```

また、UC-01とUC-02だけではAriadne固有の価値を十分に検証できません。分析を実行するだけならNotebookやCLIでも可能だからです。

Ariadneの差別化要素は主に次です。

- 複数実行の比較
- 問いから結果までの来歴
- 第三者による追跡
- 限定付き解釈の保持

したがって、**UC-03の比較再実行をUC-02へ組み込み、UC-04を独立したレビューシナリオとして残す**のが妥当です。

これは、既存ERからシナリオを作らず、「利用者の判断→必要な証拠→分析→来歴→最小構造」の順で逆算するという引継ぎ方針に沿います。

---

# 1. 初回検証のスコープ

## 対象利用者

初回は次の利用者に限定します。

> 基本的な統計・因果推論の知識を持ち、現在はPython NotebookやCLIで分析している分析者

非分析者や経営層まで含めると、分析機能、UI、説明資料、承認フローの問題が混ざり、何を検証しているか分からなくなります。

## 対象分析

初回は**因果分析だけ**に限定します。

機械学習評価やXAIまで混ぜると、Analysis Specificationの一般性は確認できますが、プロダクト価値の検証が散漫になります。

## 検証対象外

初回は次を主目的にしません。

- 大規模同時実行
- RBACの網羅性
- Worker障害回復
- Outboxの信頼性
- 詳細な監査イベント
- S3／Azure Blob対応
- マルチテナント性

これらはシステム品質の検証対象であり、利用者価値の検証とは分けるべきです。

---

# 2. 検証すべき仮説

## H1: 開始容易性

曖昧な問題意識しかない状態でも、利用者は分析を開始できる。

### 反対仮説

Research QuestionやHypothesisの入力を要求され、分析開始前に停止する。

---

## H2: 分析判断支援

複数の分析結果を比較することで、利用者は単一結果を見る場合よりも妥当な候補仮説または解釈を選べる。

### 反対仮説

比較画面はあるが、差分が意思決定に結び付かない。

---

## H3: 来歴価値

利用者は、結果から使用データ、設定、パラメータ、診断結果へ遡ることに実務上の価値を感じる。

### 反対仮説

Notebook、ファイル名、MLflowだけで十分であり、Ariadneの来歴は追加負担になる。

---

## H4: 厳格な結論形成

Ariadneは、点推定値や探索Graphから過剰な因果主張を行うことを抑制できる。

### 反対仮説

利用者はdiagnosticsや仮定を無視し、表示された結果だけから強い結論を書く。

---

## H5: 情報モデルの必要性

現行モデルで保持している情報のうち、実際に利用者が参照・再利用するものを特定できる。

### 反対仮説

多くの情報はユーザー行動に現れず、独立Resourceや永続テーブルとして保持する根拠が得られない。

---

# 3. 最小検証シナリオ案

## VS-01: 探索的分析から候補仮説を形成する

### 目的

`Start loose`が成立するか、および因果探索結果が候補仮説形成に役立つかを検証する。

### 利用者状況

小売企業の分析者が、店舗間の売上差の原因候補を調べている。

明確な仮説はまだない。

### 与える課題

> 店舗ごとの売上差に関係していそうな要因や構造を調べ、次に検証すべき候補仮説を2つ提示してください。

### 提供データ

店舗×週単位のデータを使用します。

例:

- 売上
- クーポン配布
- 商品価格
- 店頭陳列
- 来店客数
- 天候
- 祝日
- 店舗規模
- 地域属性

検証用には、構造を把握できる**半人工データ**が望ましいです。完全な実データでは、利用者の判断が正しかったかを評価できません。

### 利用者の作業

1. Projectを作成する
2. Problem Statementを記録する
3. Dataset Versionを選択する
4. 列の意味や分析対象を指定する
5. 因果探索を実行する
6. 異なる手法または設定でもう一度実行する
7. 結果の差分を比較する
8. 候補Graphを保存する
9. 候補仮説を2つ記録する
10. 探索結果だけでは断定できない事項を記録する

### 期待成果

- 保存された候補Graph
- 比較した2つ以上のExecution
- 候補仮説
- 仮説を支持する観察結果
- 不確実なエッジまたは構造
- 次に必要な検証

### 検証ポイント

#### 開始時

- Research Questionがなくても開始できるか
- Project、objective、Questionの違いで停止しないか
- 入力させるべき情報と自動生成すべき情報は何か

#### 実行時

- Algorithmやparameterを理解できるか
- デフォルト設定だけで進めるか
- 設定差分を認識できるか

#### 結果確認時

- エッジを確定因果関係として誤読しないか
- 複数結果の一致・不一致を判断に利用できるか
- Discovery ResultとSaved Graphを区別できるか

### 失敗条件

以下のいずれかが起きた場合、設計仮説は棄却または要修正です。

- 仮説を入力しないと分析を開始できない
- 利用者が探索Graphを因果関係の確定結果として扱う
- 複数結果を比較しても判断が変わらない
- 保存したGraphとExecution Resultの違いを説明できない
- どの設定で結果が生成されたか追跡できない

---

## VS-02: 明示した因果仮説を評価し、条件を変えて再評価する

### 目的

明示的な問いから、妥当な分析仕様、診断、限定付きClaimまで接続できるかを検証する。

UC-03の比較再実行もこのシナリオに含めます。

### 利用者状況

クーポン施策の継続可否を検討している分析者がいる。

### 与える課題

> クーポン配布が売上へ正の効果を持つか評価してください。結果だけでなく、その結論を採用できる条件と限界も記録してください。

### 提供データ

半人工の観察データを用意します。

変数例:

- treatment: クーポン配布
- outcome: 購買金額
- confounders: 過去購買額、会員ランク、地域、年齢層
- effect modifier候補: 顧客セグメント
- overlapが弱い領域を一部含める

重要なのは、単純に「正の効果」が出るデータではなく、diagnosticsを確認しないと強い結論を出せないデータにすることです。

### 利用者の作業

1. ProjectとDataset Versionを選択する
2. Research Questionまたはobjectiveを記録する
3. treatment、outcome、対象集団を定義する
4. 仮定または調整変数を指定する
5. 推定を実行する
6. 効果量、信頼区間、overlap、balance等を確認する
7. 結果の解釈を記録する
8. estimatorまたはparameterを変更して再実行する
9. 2つのExecutionを比較する
10. 最終的な限定付きClaimを記録する
11. Claimから根拠へ遡る

### 期待成果

- Research Question
- Analysis Specification
- 2つ以上のExecution
- 効果推定結果
- diagnostics
- 実行間差分
- Claim
- assumptions
- limitations
- 使用Dataset Version、code、parameter、Artifactへのリンク

### 検証ポイント

#### 分析設計

- treatment、outcome、populationを適切に指定できるか
- confounderと単なる予測変数を区別できるか
- Analysis Specificationの粒度が過剰でないか

#### 結果判断

- 点推定値だけで判断しないか
- overlapやbalanceを参照するか
- 「効果あり」「効果不明」「特定範囲のみ判断可能」を使い分けられるか

#### 再実行

- 技術的retryと利用者による再分析を区別できるか
- 変更した項目を理解できるか
- 旧Executionを上書きせず、新しいExecutionとして認識できるか

#### 来歴

- Claimから使用データへ戻れるか
- どのparameterが結果差に寄与したか確認できるか
- Execution Planの独立表示が必要か、それともsnapshot表示で十分か

### 失敗条件

- Questionの入力が形式的な作文になる
- diagnosticsを見ずに結論を書く
- 再実行時に何を変更したか分からない
- ResultとArtifactを混同する
- Claimの根拠となるExecutionを特定できない
- 同じ条件の再実行を同一Executionとして扱う
- 強い因果Claimを仮定・限界なしで確定できる

---

## VS-03: 第三者が結果の根拠をレビューする

### 目的

Ariadneの「再現・比較・監査可能な来歴」が、分析実施者以外にも価値を持つか検証する。

### 利用者状況

別の分析者またはレビュー担当者が、VS-02で作成されたClaimを確認する。

レビュー担当者は分析実施時には立ち会っていない。

### 与える課題

> 「クーポン施策は売上を増加させる」という結論を採用してよいか確認し、承認、条件付き承認、差戻しのいずれかを選んでください。

### 利用者の作業

1. ClaimまたはResultを開く
2. Research Questionを確認する
3. 対象Dataset Versionを確認する
4. treatment、outcome、adjustment setを確認する
5. estimatorとparameterを確認する
6. diagnosticsを確認する
7. 比較対象Executionを確認する
8. limitationsを確認する
9. 承認判断と理由を記録する

### 期待成果

- 承認判断
- 判断理由
- 参照した情報
- 不足していた情報
- 不要だった情報

### 検証ポイント

- 分析者へ直接質問せず判断できるか
- UI上の概念名を理解できるか
- Result、Artifact、Manifest、Executionの違いが必要か
- 全Event履歴が必要か
- 実際に参照された来歴情報は何か

### 失敗条件

- 分析者本人の説明がなければ判断できない
- Dataset Versionや設定を特定できない
- ClaimとResultの対応が分からない
- 内部的なExecution管理情報が前面に出てレビューを妨げる
- 必要な情報が複数画面に分散し、根拠を再構成できない

---

# 4. シナリオごとの最小情報構造

| 区分 | VS-01 探索 | VS-02 仮説評価 | VS-03 第三者レビュー |
|---|---|---|---|
| 入力 | Problem Statement、Dataset Version、対象変数 | Question、Dataset Version、treatment、outcome、population、分析仕様 | 既存ResultまたはClaim |
| 操作 | 探索、比較、候補保存 | 推定、診断、再実行、比較、解釈 | 根拠追跡、妥当性判断 |
| 出力 | 候補Graph、候補仮説 | 効果推定、diagnostics、限定付きClaim | 承認判断、理由 |
| 判断 | 次に何を検証するか | 施策効果をどう解釈するか | Claimを採用できるか |
| 必須来歴 | Dataset、設定、Execution、Graph | Dataset、仕様、parameter、Execution、Result、diagnostics | QuestionからResultまでの関係 |
| 任意候補 | Significance、完成済みHypothesis | 独立したExecution Plan Resource | 全Event、resource usage |
| 初期段階で不要な可能性 | 承認フロー、詳細監査 | 全入力型別binding、全projection | Worker内部Attempt詳細 |

---

# 5. 評価指標

## 行動指標

- タスクを完了できたか
- 介助が必要だった箇所
- 誤った概念理解の数
- Notebookへ戻った箇所
- 比較時に実際に参照した差分
- Claim作成時に参照したdiagnostics
- レビュー時に参照した来歴情報

## 成果物指標

- 候補仮説が探索結果と対応しているか
- ClaimがQuestionへ回答しているか
- assumptionsとlimitationsが記録されているか
- 過剰な因果主張がないか
- 第三者が根拠を再構成できるか

## 情報モデル評価

各情報項目を次に分類します。

```text
必須:
なければタスクまたは判断が成立しない

有用:
必須ではないが、判断品質または効率を改善する

内部:
利用者には不要だが、実行基盤には必要

未使用:
検証中に参照も生成もされない

将来:
今回のシナリオでは必要性を確認できない
```

「未使用」は直ちに削除を意味しません。ただし、独立Resourceや独立テーブルを維持する根拠にはなりません。

---

# 6. 検証順序

初回は次の順が妥当です。

```text
VS-01 探索
  ↓
VS-02 仮説評価・比較再実行
  ↓
VS-03 第三者レビュー
```

理由は、Ariadneの意味論的な流れを一続きで検証できるためです。

```text
曖昧な問題
→ 候補仮説
→ 明示的な問い
→ 分析仕様
→ Execution
→ Result
→ Claim
→ 第三者レビュー
```

この3シナリオで検証できないテーブルやResourceは、少なくとも**初期プロダクト価値の成立に必要であるとは証明されていない**と扱えます。

次は、VS-01について「画面遷移ではなく、被験者へ渡す具体的な課題文・データ仕様・観察シート」まで落とすのが適切です。

---

## User — 2026-08-05T00:40:08Z

シナリオとしては。
1. 分析者が、前処理済みデータをULして、因果探索→複数アルゴリズムでDAGを生成→複数ダグを比較しDAG候補選定、このDAG構造を使うと決める→DAGを使用して因果推論（ATE/ATT）因果推論の結果。
2. 一つの因果探索内でも、PCアルゴリズムのパラメータ感度推定のように複数結果を比較できる
3. 因果探索まで終わった状態で、別のアルゴリズムを使って因果推論を行う
4. 出てきた結果について、複数の結果の比較ができる。その際のデータ来歴、使用したアルゴリズム、パラメータなどを同定して比較ができる

## Assistant

挙げられた4点を、検証可能な業務シナリオへ再編します。特に「探索結果の比較」と「推論結果の比較」を分離し、来歴要件を横断的に定義します。

## Assistant

整理すると、提示された4点は妥当です。ただし、**4は独立シナリオというより、1〜3すべてに横断する比較・来歴要件**です。

また、科学的に1点修正が必要です。

> PCアルゴリズムの出力は一般にDAGではなく、Markov同値類を表すCPDAGです。

したがって、シナリオ上は「複数DAG」ではなく、まず**複数の因果グラフ候補**と表現する方が正確です。最終的にDAGとして採用する場合は、追加の方向付け、ドメイン知識による編集、またはDAG化規則の来歴も必要になります。

# 検証シナリオの再構成

## VS-01：因果探索から因果効果推定までの一連分析

### 利用者

因果分析を行う分析者。

### 開始状態

- Projectは作成済み、または新規作成する
- 前処理済みデータがローカルに存在する
- treatment、outcomeは分析途中または推論開始時に指定する
- 因果構造は未確定

### 利用者の目的

前処理済みデータから複数の因果構造候補を生成・比較し、採用した構造を用いてATEまたはATTを推定する。

### 操作フロー

```text
前処理済みデータをアップロード
  ↓
Dataset Versionを固定
  ↓
変数の意味・役割を設定
  ↓
複数の因果探索アルゴリズムを実行
  例: PC / GES / LiNGAM / NOTEARS
  ↓
複数の因果グラフ候補を比較
  ↓
採用候補を選択
  ↓
必要に応じて方向付け・編集
  ↓
使用するGraph Versionを確定
  ↓
treatment / outcome / estimandを設定
  ↓
調整集合と推定条件を確認
  ↓
ATEまたはATTを推定
  ↓
効果推定結果とdiagnosticsを確認
```

### 最終成果物

- Dataset Version
- 複数のDiscovery Execution
- 各Discovery Result
- 各因果グラフ候補
- 採用したGraph Version
- Graph選定理由
- treatment
- outcome
- estimand: ATEまたはATT
- adjustment set
- Estimation Execution
- 効果推定値
- 信頼区間または標準誤差
- overlap、balance等のdiagnostics
- 限定付き解釈

### 利用者が行う判断

1. どのグラフ候補を採用するか
2. そのグラフを因果推論に利用してよいか
3. treatmentとoutcome間の効果が識別可能か
4. ATEまたはATTの結果をどの範囲で解釈できるか

### 検証すべき価値

- 探索結果から推論へ自然に接続できるか
- 複数アルゴリズムの比較がGraph選定に役立つか
- 採用Graphが推論結果まで追跡可能か
- Graphと推定結果を一つの来歴として扱う価値があるか

### 重要な注意点

「DAGを選択したので、そのままATEを計算できる」とは限りません。

因果推論には少なくとも以下が必要です。

```text
Graph
+ treatment
+ outcome
+ estimand
+ target population
+ identification assumptions
+ adjustment set
+ estimator
```

Graphは推論設計の入力ですが、推論設計そのものではありません。

---

## VS-02：同一因果探索アルゴリズム内のパラメータ感度比較

### 利用者の目的

PCアルゴリズムなどについて、パラメータ変更によるグラフ構造の安定性を評価する。

### 例

PCアルゴリズムの有意水準を変更する。

```text
alpha = 0.01
alpha = 0.05
alpha = 0.10
```

または、独立性検定、最大条件集合サイズなどを変更する。

### 操作フロー

```text
Dataset Versionを固定
  ↓
Discovery AlgorithmをPCに固定
  ↓
基準パラメータで実行
  ↓
パラメータを変更して複数実行
  ↓
各結果を並べて比較
  ↓
安定したエッジ、不安定なエッジを確認
  ↓
採用する設定またはGraph候補を選択
```

### 比較対象

- ノード集合
- エッジ集合
- エッジ数
- skeletonの一致
- edge orientationの一致
- 追加・削除されたエッジ
- 向きが変化したエッジ
- SHD等のグラフ距離
- algorithm
- parameter差分
- 実行時間
- warning
- diagnostics

### 利用者が行う判断

- 結果はパラメータに対して安定しているか
- 特定のエッジだけが不安定か
- どのパラメータ設定を採用するか
- 単一Graphを採用すべきか、複数候補を残すべきか

### 来歴上必要なもの

```text
同一Dataset Version
同一Algorithm
異なるParameter Set
異なるExecution
異なるDiscovery Result
結果間の比較関係
```

### Executionの扱い

各パラメータ設定は、原則として**別Execution**です。

```text
PC(alpha=0.01) → execution_id=A
PC(alpha=0.05) → execution_id=B
PC(alpha=0.10) → execution_id=C
```

これらを「一つのExecutionの複数Attempt」として扱うのは不適切です。

Attemptは技術的retryを表し、パラメータ変更は分析条件を変更した新しい処理要求だからです。

### 設計上の論点

UI上では「一回の感度分析」としてまとめて見せてもよいですが、内部的には次のいずれかです。

```text
案A:
親となるSensitivity Analysis
  └ 複数Execution

案B:
比較グループ
  └ 複数Execution

案C:
明示的な親Resourceは作らず、
relationまたはcomparison requestで束ねる
```

初期段階では、独立したSensitivity Analysisテーブルを作る必要はありません。比較対象ExecutionのID集合と比較条件をJSONとして保持すれば足りる可能性があります。

---

## VS-03：同一Graphを用いた複数因果推論手法の比較

ユーザー記述の「別のアルゴリズムを使って因果推論」は、正確には次のように整理できます。

> 因果探索まで完了し、採用Graphを固定した状態で、異なる因果効果推定手法を用いて推定結果を比較する。

### 開始状態

- Dataset Versionが確定している
- 採用Graph Versionが確定している
- treatment、outcomeが確定している
- estimandが確定している
- adjustment setが確定または導出されている

### 比較する推定手法の例

- outcome regression
- IPW
- AIPW
- g-computation
- 単純差
- その他の対応推定器

### 操作フロー

```text
採用Graph Versionを選択
  ↓
treatment / outcome / estimandを指定
  ↓
調整集合を決定
  ↓
Estimator Aで実行
  ↓
Estimator Bで実行
  ↓
Estimator Cで実行
  ↓
効果推定値とdiagnosticsを比較
  ↓
最終的な解釈を記録
```

### 比較時に固定すべき条件

推定器の比較を成立させるには、原則として次を固定します。

- Dataset Version
- 対象集団
- treatment
- outcome
- estimand
- Graph Version
- adjustment set

これらまで変わると、推定器だけの比較ではなくなります。

### 比較対象

| 分類 | 比較項目 |
|---|---|
| 効果量 | estimate |
| 不確実性 | standard error、confidence interval |
| 推定対象 | ATE / ATT |
| overlap | propensity分布、極端値 |
| balance | weighted SMD等 |
| 安定性 | clippingやmodel specificationへの感度 |
| 実行条件 | estimator、parameter |
| 警告 | convergence、positivity、sample loss |

### 利用者が行う判断

- 推定器によらず結果は概ね一致しているか
- 特定手法だけ結果が大きく異なるか
- diagnostics上、どの推定結果を信頼できるか
- 効果が頑健か、推定手法依存か

### Executionの扱い

各推定器は別Executionです。

```text
AIPW → execution_id=D
IPW  → execution_id=E
OLS  → execution_id=F
```

ただし、すべて同じAnalysis Definitionから派生した再評価として関連付けます。

---

# 4. 比較・来歴機能は横断要件として扱う

提示された4番目は、独立した業務フローというより、VS-01〜VS-03すべてを成立させるAriadneの中核機能です。

引継ぎサマリーでも、複数結果比較、条件変更による再実行、Dataset・method・parameter・Artifactへの遡及がAriadne固有の価値候補として挙げられています。

## CR-01：複数結果の比較

利用者は任意の複数Resultを選択し、次を比較できる。

### 共通比較項目

- Dataset Version
- 入力データhash
- 使用列
- 欠損処理等の前処理情報
- analysis domain
- operation
- algorithm / estimator
- package version
- parameter
- random seed
- code version
- Graph Version
- treatment
- outcome
- estimand
- adjustment set
- 実行日時
- execution status
- warning / error
- Artifact
- Result
- diagnostics

### 差分表示

単にすべての情報を並べるのではなく、次の3分類が必要です。

```text
同一条件
変更条件
結果差分
```

例:

| 項目 | Execution A | Execution B | 差分 |
|---|---|---|---|
| Dataset | v3 | v3 | 同一 |
| Algorithm | PC | PC | 同一 |
| alpha | 0.01 | 0.05 | 変更 |
| Edge count | 18 | 25 | +7 |
| SHD | — | 9 | 結果差 |
| Runtime | 12.1s | 18.4s | +6.3s |

## CR-02：結果から来歴へ遡れる

結果から最低限、次へ移動できる必要があります。

```text
Result
  ↓
Execution
  ↓
Execution時の固定条件
  ├ Dataset Version
  ├ Analysis Specification
  ├ Algorithm / Estimator
  ├ Parameter
  ├ Graph Version
  ├ Runtime / code version
  └ Artifact
```

## CR-03：上流結果を下流分析の入力として同定できる

特に重要なのは、因果探索結果から因果推論への接続です。

Estimation Executionは、単にGraphファイルを受け取るのではなく、次を参照できる必要があります。

```text
input_graph_version_id
source_discovery_result_id
source_discovery_execution_id
```

すべてを独立カラムや独立テーブルにする必要はありませんが、意味論上はこの関係を失ってはいけません。

---

# 5. 4点をまとめた全体シナリオ

最終的には、次の一連のシナリオとして扱えます。

```text
1. Dataset Upload
   前処理済みデータを登録しDataset Versionを固定

2. Discovery Comparison
   複数の因果探索アルゴリズムを実行・比較

3. Discovery Sensitivity
   同一アルゴリズムの複数パラメータ結果を比較

4. Graph Selection
   候補Graphを選択し、必要に応じて編集・方向付け

5. Graph Version Fixing
   因果推論で使用するGraph Versionを確定

6. Causal Design
   treatment、outcome、estimand、population、
   adjustment set、assumptionsを設定

7. Estimator Comparison
   複数の推定器でATEまたはATTを推定

8. Result Comparison
   推定値、信頼区間、diagnosticsを比較

9. Lineage Review
   Dataset、Graph、algorithm、parameter、
   code、Artifactまで遡る

10. Interpretation
    採用結果、選定理由、仮定、限界を記録
```

# 6. このシナリオから導かれる最小概念

現時点では、少なくとも次が必要です。

| 概念 | 必要性 |
|---|---|
| Project | 分析テーマと境界 |
| Dataset | データの論理単位 |
| Dataset Version | 実際に使用したデータの固定 |
| Analysis Definition Version | 探索または推論の分析条件 |
| Execution | 各アルゴリズム・各パラメータ・各推定器の実行 |
| Result | 比較対象となる論理結果 |
| Artifact | Graphファイル、表、diagnostics等 |
| Causal Graph Version | 選択・編集・再利用されるGraph |
| Relation / Lineage | 探索結果からGraph、Graphから推論への関係 |
| Comparison | 複数Resultの比較条件と表示 |

## まだ独立エンティティ化を証明できないもの

- Comparison Group
- Sensitivity Analysis
- Graph Selection Decision
- Execution Plan
- Claim
- Adjustment Set Resource
- Parameter Set Resource

これらは概念としては必要ですが、初期段階ではAnalysis DefinitionやResult metadata内のVersioned JSONで表現できる可能性があります。

# 7. シナリオ上の主要な未決事項

## 1. Graph選定は新しいResourceか

複数Discovery Resultの一つをそのまま採用する場合と、人間が編集して採用する場合では意味が異なります。

```text
Discovery Result Graph
≠ Selected Graph
≠ Manually Edited Graph
```

編集可能なら、`causal_graph_version`を独立して保持する理由は強くなります。

## 2. Comparisonを永続化するか

一時的なUI比較だけなら、比較対象IDをクライアントまたはAPI requestで渡せばよいです。

比較結果にコメント、承認、共有、再利用が必要なら、独立Resource化の根拠が生まれます。

## 3. 一括実行をどう見せるか

例えばPCのalphaを3通り実行する場合、利用者には一つの操作に見えます。

しかし科学的・来歴的には3つのExecutionです。

したがって、

```text
ユーザー操作としての一括実行
≠ Execution Identity
```

と整理する必要があります。

## 4. Graphの不確実性を推論へどう渡すか

1つのGraphだけを採用して推論すると、Graph選定の不確実性が下流結果から消えます。

初期検証では単一Graph選択でよいですが、比較シナリオでは将来的に、

```text
Graph AでATE
Graph BでATE
Graph CでATE
```

という構造感度分析も自然に発生します。

---

この整理では、**VS-01をGolden Path、VS-02とVS-03を比較・感度分析シナリオ、4番目を横断的なComparison/Lineage要件**として扱うのが最も明確です。

---

## User — 2026-08-05T00:53:14Z

使いどころとして
- 売上改善
- 退職者抑制
- 従業員エンゲージメントの向上に聞くファクタ抽出
- クッキーの焼上り品質の改善
- 被介護者の健康状態向上に聞く介入施策の特定

を想定。これを考えたときに、他に必要なシナリオあるかい？

## Assistant

想定用途を因果分析の「実務判断」に落とすと、現行の探索→DAG選定→ATE/ATTだけでは不足します。追加候補を、初期検証で必須なものと将来拡張に分けます。

## Assistant

## 結論

追加シナリオは必要です。

現在の4シナリオは、概ね次の条件を暗黙に仮定しています。

```text
前処理済みの単一データセット
単一時点または独立同分布の観測
二値Treatment
単一Outcome
単一の採用Graph
ATE / ATTが識別・推定可能
推定結果を比較すれば意思決定できる
```

しかし、挙げられた5用途では、この仮定が成立しないケースが多いです。

特に重要なのは、**「効くファクタの発見」と「実行可能な介入施策の特定」は同じではない**ことです。

```text
予測に有用な変数
≠ 関連する変数
≠ 原因変数
≠ 人為的に変更可能な変数
≠ 現実に採用すべき介入
```

引継ぎサマリーでも、予測寄与、関連、モデルattribution、因果変数を混同しないことが明示されています。

---

# 1. 用途ごとに不足するシナリオ

| 用途 | 現行シナリオだけでは不足する点 |
|---|---|
| 売上改善 | 値引率などの連続Treatment、店舗別効果、利益とのトレードオフ、季節性 |
| 退職者抑制 | 退職までの時間、打切り、従業員別効果、介入可能性、公平性 |
| エンゲージメント向上 | 非介入可能変数の除外、尺度の妥当性、部署・上司単位の階層性 |
| クッキー品質改善 | 温度・時間・配合量などの連続Treatment、非線形性、交互作用、バッチ差 |
| 被介護者の健康向上 | 時系列、反復介入、時間変化する交絡、安全性、個人別効果 |

したがって、少なくとも以下の追加シナリオを検討すべきです。

---

# 2. 追加必須シナリオ

## VS-05：介入可能な候補因子を選別する

### 目的

因果探索で得られたノードやエッジから、実際に操作可能な介入候補を選別する。

### 例

退職者抑制で次の因子が見つかったとします。

- 年齢
- 勤続年数
- 上司との関係
- 残業時間
- 給与
- 職種
- エンゲージメント

このうち、年齢や過去の勤続年数は因果的に関連していたとしても、直接介入できません。

### 操作フロー

```text
因果Graph候補を表示
  ↓
各変数を分類
  ├ 介入可能
  ├ 介入困難
  ├ 不変属性
  ├ 機微属性
  ├ outcome測定後に得られる変数
  └ 不明
  ↓
介入候補を選択
  ↓
介入候補ごとに推論設計を作成
```

### 必要な分類

| 分類 | 例 |
|---|---|
| Actionable | 残業時間、研修、割引率、焼成温度 |
| Non-actionable | 年齢、過去履歴、地域 |
| Sensitive | 性別、障害、健康情報 |
| Post-treatment | 介入後に発生する満足度 |
| Mediator | 介入効果の途中経路 |
| Confounder | 調整対象 |
| Outcome | 最終評価対象 |

### このシナリオがない場合の問題

「年齢が退職に効くので年齢に介入する」といった、実務的に無意味または不適切な結論を防げません。

---

## VS-06：因果効果を推定できない場合を正しく返す

### 目的

Ariadneが必ず数値を返すのではなく、推定不能または解釈不能を正式な結果として扱えるか確認する。

### 発生例

- 有効な調整集合が存在しない
- 未観測交絡が強く疑われる
- treatment群とcontrol群のoverlapがない
- サンプル数が不足する
- Graph方向が確定しない
- positivityが成立しない
- 推定器が収束しない
- Graph候補によって結論が逆転する

### 操作フロー

```text
GraphとCausal Designを指定
  ↓
Identificationを実行
  ↓
推定可能性を判定
  ├ IDENTIFIED
  ├ PARTIALLY_IDENTIFIED
  ├ NOT_IDENTIFIED
  └ ESTIMATION_UNRELIABLE
  ↓
理由と必要な追加情報を表示
```

### 成果物

数値結果だけでなく、次のような結果を正式に保存します。

```text
このデータと仮定ではATEを識別できない。

理由:
- treatmentとoutcome間に未閉鎖のbackdoor pathがある
- 観測済み変数だけでは調整不能
```

### 重要性

このシナリオは科学的妥当性の中核です。

現在のGolden Pathが「必ずATE/ATT結果まで到達する」設計だと、分析者に誤った確信を与えます。

---

## VS-07：介入効果の異質性を比較する

### 目的

平均効果だけでなく、対象集団によって効果が異なるか確認する。

### 例

#### 売上改善

- 新規顧客にはクーポンが効く
- 既存顧客にはほとんど効かない

#### 退職抑制

- 若手社員には上司面談が有効
- 管理職には効果がない

#### 介護

- 軽症者には運動介入が有効
- 重症者では負担が上回る

### 初期段階の最小実装

高度なCATE推定を直ちに実装する必要はありません。

まずは、分析者が事前指定したsubgroupについて、層別ATEまたはATTを比較できればよいです。

```text
全体ATE
部署別ATE
年齢層別ATE
店舗別ATE
健康状態別ATE
```

### 比較時に必要な情報

- subgroup定義
- subgroup定義を事前に決めたか、結果を見て決めたか
- subgroupごとのサンプル数
- 効果推定値
- 信頼区間
- overlap
- 多重比較上の注意

### 設計上の注意

結果を見た後に都合のよいsubgroupを選ぶと、探索的な結果を確証的な結果として誤解する危険があります。

そのため、subgroup定義の来歴も必要です。

---

## VS-08：連続値・多値Treatmentを扱う

### 目的

二値の「介入あり／なし」では表現できない施策を評価する。

### 該当例

| 用途 | Treatment |
|---|---|
| 売上 | 割引率、広告費、陳列量 |
| エンゲージメント | 面談頻度、研修時間 |
| クッキー | 焼成温度、焼成時間、配合比 |
| 介護 | 運動時間、訪問頻度、投薬量 |

### 必要な比較

```text
180℃ vs 190℃
190℃ vs 200℃
割引率0% vs 5%
割引率5% vs 10%
週1回介入 vs 週3回介入
```

またはdose-responseとして、

```text
Treatmentの値
  ↓
期待Outcome
```

の関係を推定します。

### 現行ATE/ATTとの関係

ATE/ATTはestimandであり、二値Treatmentだけに限定される概念ではありませんが、現在の実装やUIが二値処置を前提としている可能性があります。

少なくとも、次を明示的に区別する必要があります。

```text
BINARY
MULTI_VALUED
CONTINUOUS
```

### 判断

このシナリオを持たないなら、**クッキー品質改善を初期対象用途として掲げるのは不正確**です。

クッキー製造で本質的な介入変数は、多くの場合連続値だからです。

---

## VS-09：時系列・反復測定データを扱う

### 目的

時間順序、遅延効果、反復介入を伴う分析を検証する。

### 該当例

- 月次売上と販促施策
- 従業員のエンゲージメント推移と退職
- 被介護者の健康状態と反復介入
- 製造バッチごとの条件と品質
- 店舗、部署、施設単位の反復観測

### データ構造例

```text
entity_id
timestamp
treatment
outcome
time-varying covariates
```

### 検証すべき事項

- 原因は結果より前に発生しているか
- 過去Outcomeを調整すべきか
- 過去Treatmentが現在の交絡因子へ影響していないか
- 同一対象の反復観測を独立データとして扱っていないか
- 退職や死亡による打切りをどう扱うか
- 介入の効果が何期間後に現れるか

### 重要な制限

通常のクロスセクションデータ向けDAGとATE推定だけでは、時間変化する交絡を適切に扱えない場合があります。

特に介護用途では、

```text
前回の介入
→ 現在の健康状態
→ 次回の介入
→ 将来の健康状態
```

という構造が発生します。

この用途を本気で対象に含めるなら、時系列またはlongitudinal causal inferenceは将来要件ではなく、中核要件候補です。

---

# 3. 強く推奨する追加シナリオ

## VS-10：複数Outcomeとトレードオフを比較する

介入を採用するかどうかは、単一Outcomeの効果だけでは決まりません。

### 売上改善

```text
売上
利益率
顧客離反
在庫消化
```

値引きで売上が上がっても、利益が下がれば採用できません。

### 退職抑制

```text
退職率
従業員満足度
施策コスト
管理職負荷
公平性
```

### クッキー品質

```text
焼上り品質
歩留まり
生産時間
エネルギーコスト
設備負荷
```

### 介護

```text
健康状態
QOL
副作用
介護者負担
医療費
```

### 操作フロー

```text
同一介入について複数Outcomeを推定
  ↓
Outcomeごとの効果と不確実性を比較
  ↓
制約条件を確認
  ↓
採用／不採用／追加検証を判断
```

これは単なる因果効果推定ではなく、**介入意思決定**のシナリオです。

---

## VS-11：ドメイン知識によるGraph制約・編集

### 目的

探索アルゴリズムの結果をそのまま採用せず、業務知識や時間順序を反映させる。

### 例

- 年齢は勤続年数の結果にはならない
- 退職後の情報が退職原因になることはない
- 焼成後の品質が焼成温度を決めることはない
- 介入後の健康状態を交絡因子として使わない
- 性別や生年月日は介入対象にしない

### 必要な操作

- 必須edge
- 禁止edge
- temporal ordering
- latent variable候補
- edge方向の手動修正
- ノードの追加・除外
- 修正理由の記録

### 来歴

```text
Algorithm Output Graph
  ↓
Domain Review
  ↓
Edited Graph Version
  ↓
Estimation Input Graph
```

ここでは以下を区別する必要があります。

```text
探索アルゴリズムの出力
≠ 分析者が採用したGraph
≠ 手動編集後のGraph
```

これは既存シナリオ1の中に組み込めますが、独立した検証観点として明示すべきです。

---

## VS-12：新しいデータで同じ分析を再実行する

### 目的

データ更新後も結論が維持されるかを確認する。

### 例

```text
Dataset Version 2026-04
Dataset Version 2026-05
Dataset Version 2026-06
```

同一Analysis Definitionを使って再実行し、次を比較します。

- Graph構造
- エッジ安定性
- 効果推定値
- 信頼区間
- overlap
- subgroup effect
- 結論
- warning

### 既存シナリオ4との違い

既存シナリオ4は主に、algorithmやparameterの違いを比較しています。

VS-12では、**分析条件を固定し、データだけを変更する**ことがポイントです。

### Ariadne固有の価値

このシナリオはVersion、Execution、Result、Lineageを保持する価値を直接検証できます。

---

# 4. 用途別の最低シナリオ構成

## 売上改善

最低限必要:

- 複数探索結果比較
- 推定器比較
- 介入可能性選別
- subgroup効果
- 連続／多値Treatment
- 複数Outcome
- データ更新再実行

追加候補:

- 店舗間spillover
- 季節性
- 施策コスト

---

## 退職者抑制

最低限必要:

- 介入可能性選別
- 機微属性の扱い
- subgroup効果
- 時系列
- 推定不能ケース
- 複数Outcome

追加候補:

- time-to-event
- censoring
- 施策対象者の選定
- 公平性評価

退職者抑制では、単純な退職有無のATEより、一定期間内の退職確率や退職までの時間が実務的に重要です。

---

## 従業員エンゲージメント向上

最低限必要:

- 介入可能性選別
- Graphへのドメイン制約
- subgroup効果
- 反復測定
- 複数Outcome

追加候補:

- エンゲージメント尺度の測定誤差
- 部署・上司単位のcluster
- 匿名化とアクセス制御

---

## クッキー品質改善

最低限必要:

- 連続Treatment
- 非線形効果
- 複数Treatment
- 交互作用
- 複数Outcome
- バッチ単位の来歴

追加候補:

- DOEとの統合
- ベイズ最適化
- process control

この用途は、観察データだけでなく実験計画法との接続が重要になる可能性があります。

---

## 被介護者の健康状態向上

最低限必要:

- 時系列・反復介入
- subgroupまたは個人別効果
- 推定不能ケース
- 安全性Outcome
- 複数Outcome
- Graphへの専門家制約

追加候補:

- time-varying confounding
- censoring
- treatment adherence
- adverse event
- 意思決定者と被介護者本人の権限分離

この用途は最も要求水準が高く、初期検証対象に含めるなら、単純なATE/ATT基盤だけでは不足します。

---

# 5. 最小限に絞った追加セット

過剰設計を避けつつ、用途との整合性を取るなら、まず追加するのは次の6つです。

1. **介入可能因子の選別**
2. **推定不能・信頼不能結果**
3. **Graphへのドメイン制約と手動修正**
4. **事前指定subgroupでの効果比較**
5. **連続／多値Treatment**
6. **データ更新後の再実行比較**

次段階:

- 時系列・反復測定
- 複数Outcomeと制約条件
- 高度なCATE
- time-varying treatment
- policy optimization

ただし、**介護と退職を初期の主要用途とするなら、時系列・反復測定を次段階へ送ることはできません**。その場合は初期必須です。

# 6. スコープ上の判断

対象用途を初期段階で全部成立させようとすると、再び過剰設計になります。

したがって、初期検証用途は次のどちらかへ絞るのが妥当です。

### 案A：事業データ中心

- 売上改善
- 退職者抑制
- エンゲージメント向上

必要な中心機能:

```text
表形式観察データ
二値／多値Treatment
Graph比較
ATE / ATT
subgroup効果
来歴・比較
```

### 案B：製造プロセス中心

- クッキー品質改善

必要な中心機能:

```text
連続Treatment
複数Treatment
非線形性
交互作用
複数Outcome
バッチ来歴
```

介護は、安全性、longitudinal data、time-varying confounding、個別効果まで要求されるため、**初期Golden Pathではなく、高要求ユースケースとして別トラックに置く**のが現実的です。

---

## User — 2026-08-05T01:29:24Z

案Aの事業データ中心、かな。

## Assistant

案Aで進めるのが妥当です。ただし、**売上改善・退職者抑制・エンゲージメント向上を同じ深さで初期対応するべきではありません**。

## 推奨する用途の優先順位

### 1. Golden Path：売上改善

初期の代表シナリオに最も適しています。

理由：

- 施策変数を比較的明確に定義できる  
  例：クーポン配布、広告接触、接客施策、商品陳列
- outcomeを定量化しやすい  
  例：売上額、購買額、購入有無
- ATE／ATTを業務判断へ接続しやすい
- 人事・健康領域より倫理的・法的な論点が少ない
- 因果探索、Graph選定、推定器比較、結果比較というAriadneの基本導線を一通り検証できる

### 2. Transfer Case：退職者抑制

売上改善で構築した構造が、人事データでも成立するかを検証します。

追加で露出する論点は以下です。

- outcomeが二値
- 機微属性を含む
- 介入可能変数と不変属性の区別
- 退職予測と退職原因の混同
- 対象者選定の公平性
- 将来的にはtime-to-eventや打切りが必要

### 3. Transfer Case：エンゲージメント向上

この用途は、退職者抑制より意味論が難しいです。

- エンゲージメントをoutcomeとするのか
- 退職抑制施策のmediatorとするのか
- アンケート尺度をどこまで信頼するか
- 上司、部署、組織など階層構造をどう扱うか

したがって、初期Golden Pathにはせず、**因果変数の役割付けとGraph編集の検証用途**として使うのが適切です。

---

# 初期プロダクト境界

## 対象に含める

```text
前処理済み表形式データ
単一時点または分析時点で固定したスナップショット
因果探索
複数アルゴリズム比較
同一アルゴリズム内のパラメータ感度比較
Graphへのドメイン制約
Graph候補の選定
二値Treatment
連続または二値Outcome
ATE / ATT
複数推定器の比較
Dataset・Graph・Algorithm・Parameter・Resultの来歴
推定不能または信頼不能という結果
```

## 初期対象外

```text
連続Treatment
時系列因果推論
time-varying treatment
生存時間分析
高度なCATE
複数施策の最適化
政策最適化
部署・店舗間spillover
多段階介入
自動的な意思決定
```

ここを明確にしないと、退職やエンゲージメントの現実的な問題をすべて扱おうとして、再び最大構成へ戻ります。

---

# 初期検証シナリオ

## BS-01：複数因果探索アルゴリズムによるGraph候補比較

### 業務例

> クーポン施策が売上へ与える効果を評価したいが、適切な変数関係や調整変数が明確でない。

### 操作

1. 前処理済みデータをアップロード
2. Dataset Versionを固定
3. 変数の意味を設定
4. PC、GES、LiNGAM等を実行
5. Graph候補を比較
6. 一致・不一致エッジを確認
7. 採用候補を選択

### 検証するもの

- 複数アルゴリズムの結果比較が判断に使えるか
- Graph差分を理解できるか
- Algorithm、Parameter、Datasetの違いを特定できるか
- 探索結果を確定的因果関係と誤認しないか

---

## BS-02：同一アルゴリズムのパラメータ感度比較

### 業務例

> PCアルゴリズムの有意水準を変更したとき、売上に関係する構造が安定しているか確認する。

### 操作

```text
PC alpha=0.01
PC alpha=0.05
PC alpha=0.10
```

を別Executionとして実行し、Graphを比較します。

### 検証するもの

- 安定エッジと不安定エッジを区別できるか
- パラメータ差分と結果差分を対応付けられるか
- 一括実行とExecution Identityを分離できるか
- 比較のために独立Sensitivity Analysis Resourceが本当に必要か

---

## BS-03：ドメイン知識によるGraph選定・修正

### 業務例

探索結果に、時間順序または業務上成立しない方向が含まれている。

### 操作

1. 探索結果Graphを選択
2. 禁止edge、必須edge、時間順序制約を指定
3. 必要に応じて方向を修正
4. 修正理由を記録
5. 推論に使用するGraph Versionを確定

### 区別すべきもの

```text
Algorithm Output Graph
Selected Graph
Edited Graph Version
Estimation Input Graph
```

### 検証するもの

- `causal_graph_version`を独立管理する実需要
- Graph選定理由の保存価値
- 人間による編集とAlgorithm出力の来歴を保持できるか

---

## BS-04：採用Graphを使用したATE／ATT推定

### 業務例

> クーポン配布が顧客の購買金額を増加させるか評価する。

### 固定する条件

- Dataset Version
- Graph Version
- treatment
- outcome
- estimand
- target population
- adjustment set

### 操作

1. Causal Designを設定
2. 識別可能性を確認
3. 推定器を選択
4. ATEまたはATTを推定
5. 信頼区間、overlap、balanceを確認
6. 限定付き解釈を記録

### 検証するもの

- Graphから推論へ接続できるか
- treatment、outcome、estimandを区別できるか
- adjustment setがどのGraphから導かれたか追跡できるか
- diagnosticsを見ずに結論を出してしまわないか

---

## BS-05：同一Causal Designで複数推定器を比較

### 業務例

同じ問いに対して、IPW、AIPW、outcome regressionを比較する。

### 固定条件

```text
Dataset Version
Graph Version
treatment
outcome
estimand
population
adjustment set
```

### 変更条件

```text
Estimator
Estimator固有Parameter
```

### 比較項目

- 推定値
- 信頼区間
- 標準誤差
- overlap
- balance
- clipping
- warning
- sample loss
- convergence
- runtime

### 検証するもの

- 推定器による違いを理解できるか
- 推定値だけでなく診断結果を比較できるか
- 「推定器によらず頑健」と「推定器依存」を区別できるか

---

## BS-06：推定不能・信頼不能を結果として扱う

これは例外処理ではなく、初期必須シナリオです。

### ケース例

- 有効な調整集合がない
- overlapがほぼ存在しない
- 特定群のサンプルが不足
- Graph候補によって結論が反転
- 推定器が収束しない
- treatmentがほぼ決定論的に割り当てられている

### 期待される結果

```text
NOT_IDENTIFIED
ESTIMATION_UNRELIABLE
INSUFFICIENT_OVERLAP
INSUFFICIENT_SAMPLE
```

などの状態と理由を、数値推定結果と同等に保存します。

### 検証するもの

- Ariadneが無理にATE／ATTを返さないか
- 利用者が「分析失敗」ではなく科学的結果として理解できるか
- 次に必要なデータや仮定を提示できるか

---

## BS-07：異なるDataset Versionでの再評価

### 業務例

4月と5月のデータで同じ分析を行い、結果が維持されるか確認する。

### 固定条件

- Analysis Definition
- GraphまたはGraph選定方針
- treatment
- outcome
- estimator
- parameter

### 変更条件

- Dataset Version

### 比較対象

- Graph構造
- 効果推定値
- 信頼区間
- overlap
- balance
- warnings
- 最終解釈

### 検証するもの

- Dataset Version管理の実際の価値
- 同一条件の再利用性
- データ更新による結論変化を追跡できるか
- ExecutionとResultの比較が実務上役立つか

---

# 横断要件：比較と来歴

すべての比較では、画面上の情報を次の3群に分ける必要があります。

## 1. 同一条件

```text
同じDataset
同じGraph
同じTreatment
同じOutcome
同じEstimand
```

## 2. 変更条件

```text
Algorithm
Parameter
Graph Version
Estimator
Dataset Version
Adjustment Set
```

## 3. 結果差分

```text
Edge差分
推定値差分
信頼区間差分
Diagnostics差分
Warning差分
```

単にExecutionの情報を横並びにするだけでは不十分です。

Ariadneが提供すべき価値は、

> **何が同じで、何を変え、その結果何が変わったのかを同定できること**

です。

---

# 用途とシナリオの対応

| シナリオ | 売上改善 | 退職抑制 | エンゲージメント |
|---|---:|---:|---:|
| 複数探索アルゴリズム比較 | 必須 | 必須 | 必須 |
| パラメータ感度比較 | 必須 | 必須 | 必須 |
| Graph制約・編集 | 必須 | 必須 | 必須 |
| ATE／ATT推定 | 必須 | 必須 | 条件付き |
| 推定器比較 | 必須 | 必須 | 条件付き |
| 推定不能結果 | 必須 | 必須 | 必須 |
| Dataset Version比較 | 必須 | 必須 | 必須 |
| 機微属性管理 | 任意 | 必須 | 必須 |
| 介入可能性分類 | 必須 | 必須 | 必須 |
| 時系列・生存時間 | 将来 | 将来必須 | 将来必須 |

---

# 現時点のスコープ定義案

> **Ariadneの初期検証対象は、前処理済みの表形式事業データを用いて、複数の因果探索結果から因果Graph候補を比較・選定し、そのGraphに基づく二値TreatmentのATE／ATTを複数推定器で評価し、分析条件・結果・来歴を比較可能にすることである。**

対象用途：

1. 売上改善をGolden Pathとする
2. 退職者抑制で人事領域への移植性を確認する
3. エンゲージメント向上で変数役割と介入可能性の扱いを確認する

対象外：

- 時系列因果推論
- 生存時間分析
- 連続Treatment
- 自動施策最適化
- 高度な個別効果推定

これは、意味論的な背骨を維持しながら、代表ユースケースから最小構成を逆算するという引継ぎ方針と整合します。


---

## User — 2026-08-05T01:40:17Z

今更だが、もともと考えていたこととして。

```
一つの大きなリサーチトピックに対して、イテレーティブに分析を回し、
論点でリサーチクエスチョンを分割（*1）して、答えが出せる粒度までリサーチクエスチョンを小さくし、
各論点=分割されたリサーチクエスチョンに対して実験を回すことで、それにこたえていく
最終的にはイシューツリーのように大きな問いとそれを分割した問い、それへの答え=示唆が得られるようにしたい。
```
というのがある


そのために必要な機能として、リサーチトピックとプロジェクトを1:1対応させ、
同一プロジェクトでは複数データセットを扱うことができる
同一データセットに対して複数の実験ができ、その際の実験の来歴を管理したいという

という方針が挙げられる

- 実験の来歴に最低限必要なものは以下を想定
    - 使用データセット
    - リサーチコンテクスト
    - 実験処理（計算するプログラム）
    - 実験処理に使ったパラメータセット
    - 得られた結果
    - どのような考えのもとに、その実験方針を決めたのか？という思想

現在まで討議された方針がないか確認せよ
----


*1) これは日本語として適切か？

## Assistant

引継ぎサマリーとZIP内の要求定義・討議メモを照合し、既に合意済み／未決／今回新規の方針に分けます。併せて「リサーチクエスチョンを分割」の日本語も評価します。

## Assistant

## 確認結果

**元々の構想の中核は、現在までの討議でかなり再発見されています。**  
ただし、次の2点はまだ明確に設計されていません。

1. **Research Questionを親子関係で分解するQuestion Tree**
2. **「なぜこの実験を行ったのか」という分析方針の選定理由**

現在の討議は「問いと実験を来歴で結ぶ」ところまでは進んでいますが、**複数の問いを階層化し、下位の回答から上位の問いへの示唆を組み立てる構造**までは定義されていません。

---

# 1. 既に討議されている方針

## 1.1 ProjectとResearch Topicの1:1対応

これは明示的に討議済みです。

`11-001_Execution_Identity_Draft.md:64-80, 141-149`では、次の方針になっています。

```text
Project
= 1つのResearch Topicを管理する
  業務・権限・分析来歴の境界

Project 1 : 1 Research Topic
```

さらに、1つのProjectが複数の以下を含むことも定義されています。

```text
Research Question
Hypothesis
Analysis Specification
Execution
Result
Claim
```

引継ぎサマリーでも、Projectは「1つのResearch Topicを扱う業務、権限、来歴の境界」と整理されています。

**判定:** 元の方針と一致しています。

---

## 1.2 Research Questionは分析を通じて段階的に精緻化する

これも討議済みです。

`11-001_Execution_Identity_Draft.md:94-117`では、Research QuestionやHypothesisは最初から完成していなくてよく、データ確認や探索的分析を通じて形成・精緻化されるとされています。

```text
Start loose.
Formalize progressively.
Conclude strictly.
```

また、探索的Executionについては、

```text
Research QuestionまたはProblem Statementを入力とし、
Hypothesis候補を出力してよい
```

と定義されています。同文書の`229-239`では、ExecutionとHypothesisの関係として以下も検討されています。

```text
GENERATE
TEST
COMPARE
REFINE
REPLICATE
```

したがって、

> イテレーティブに分析を行い、問いや仮説を精緻化する

という構想は、現在の方針と明確に整合します。

---

## 1.3 1つのResearch Questionに対して複数の実行を行う

これも明示されています。

`11-001_Execution_Identity_Draft.md:177-183`

```text
同一のResearch Questionに対して、
複数のExecutionを実行できる。

Research Question 1 : N Execution
```

ただし、現行の意味論では、より正確には次の区別が必要です。

```text
Research Question
= 答えたい問い

Experiment
= 問いに答えるための一連の分析計画・比較単位

Execution
= 特定の入力・アルゴリズム・パラメータで行う1回の計算
```

PCのパラメータを3通り試す場合は、例えば次の構造です。

```text
Research Question
└── Experiment: PCパラメータ感度分析
    ├── Execution: alpha=0.01
    ├── Execution: alpha=0.05
    └── Execution: alpha=0.10
```

---

## 1.4 Experimentが複数Executionを束ねる

これも既存要件と実装に存在します。

旧要件`10_web_service_requirements_v1.3.md:1361-1382`には、次が明記されています。

```text
利用者はExperimentを作成し、
複数Executionを所属させられること。
```

Experimentが保持する情報：

- title
- objective
- hypothesis
- notes
- source repository
- source commit
- notebook reference
- tags

また、Experiment内のExecutionを以下で比較する要件もあります。

- Dataset
- algorithm
- Graph Version
- estimand
- method
- result

現在のデータモデルにも`experiment`はSupporting領域として残っており、`execution.experiment_id`は任意の整理用Experimentへの参照です。実装上の`Experiment`にも`objective`、`hypothesis`、`notes`、`source_repository`、`source_commit`等が存在します。

**判定:** 「同じ論点に対して複数の実験・計算を回して比較する」という構想は、既存のExperiment管理と整合します。

ただし、現在のExperimentは**Research Questionへの明示的な参照を持っていません**。ここは未接続です。

---

## 1.5 1つのProjectで複数Datasetを扱う

データモデル上、既に可能です。

`21_data_model_definition_v1.4.md:152-174`の概念ERでは、

```text
PROJECT ||--o{ DATASET : owns
PROJECT ||--o{ EXECUTION : owns
```

となっています。

したがって、

```text
Project 1 : N Dataset
Project 1 : N Execution
```

です。

ただし、注意点があります。

現行Web MVPは、**1つのExecutionの標準入力を単一のAnalysis-ready Tableとする**方針です。

これは、

```text
Project内で複数Datasetを管理できない
```

という意味ではありません。

正確には、

```text
Project:
複数Datasetを保持できる

個々のMVP Execution:
原則として1つのAnalysis-ready Tableを入力する
```

という区別です。

---

# 2. 実験来歴の項目との対応

元々想定していた来歴項目は、現在の概念へ次のように対応します。

| 元の項目 | 現在の対応概念 | 状況 |
|---|---|---|
| 使用データセット | Dataset Version / Input Version binding | 定義済み |
| リサーチコンテクスト | Research Context Versionまたはsnapshot | 概念定義済み、物理管理方法は未決 |
| 実験処理・プログラム | Analysis Specification、Algorithm / Method、Runtime、code version | おおむね定義済み |
| パラメータセット | Execution PlanのParameter | 定義済み |
| 得られた結果 | Result / Artifact | 定義済み |
| 実験方針を決めた理由 | Research Context、objective、hypothesis、notes | 部分的。明示的なdecision rationaleは未定義 |

Execution Planには、次を固定する方針があります。

`11-001_Execution_Identity_Draft.md:294-317`

```text
Research Context snapshot
Input Version
Analysis Specification
Algorithm / Method
Parameter
Random seed
Runtime specification
Stage構成
Input / Output contract
Reproducibility metadata
```

したがって、計算再現性に必要な情報は概ね含まれています。

---

# 3. まだ討議されていない、または未決の部分

## 3.1 Research Questionの階層構造

リポジトリ全体を検索しましたが、以下に相当する仕様は確認できませんでした。

- `parent_question_id`
- Sub-question
- Question Tree
- Issue Tree
- 親の問い／子の問い
- 問いの分解関係
- 子の回答から親の問いへの集約

現在の構造は、

```text
Project
└── 複数Research Question
```

までです。

元の構想に必要なのは、

```text
Project / Research Topic
└── 上位Research Question
    ├── Sub-question A
    │   ├── Sub-question A-1
    │   └── Sub-question A-2
    └── Sub-question B
```

です。

**これは今回、明示的に追加すべき意味論です。**

---

## 3.2 Research QuestionとExperimentの関係

現在は次が個別に存在します。

```text
Research Question 1 : N Execution
Experiment 1 : N Execution
```

しかし、

```text
Research Question 1 : N Experiment
```

という関係は定義されていません。

元の構想では、次の構造の方が自然です。

```text
Research Question
└── Experiment
    └── Execution
```

つまり、

- Research Question：何に答えるか
- Experiment：どう答えるかという分析方針・比較単位
- Execution：具体的な1回の計算

です。

---

## 3.3 下位の答えから上位の問いへの統合

Claimは既に定義されています。

`11-001_Execution_Identity_Draft.md:556-583`

```text
Claim
= Resultを根拠として人間が構成する、
  Research Questionへの限定付き回答
```

Claimには以下を含める想定です。

- claim statement
- claim type
- 根拠Result
- 対象範囲
- 前提・仮定
- 不確実性
- qualification
- limitation

ただし、現在は、

```text
下位QuestionのClaim
→ 上位Questionへの部分回答
→ 複数Claimを統合した上位Claim
```

という構造は未定義です。

ここが、イシューツリー型ワークスペースを成立させる上で重要な欠落です。

---

## 3.4 「実験方針を決めた理由」

これは部分的には以下で表現できます。

- Problem Statement
- Research Question
- Significance
- Hypothesis
- Experiment.objective
- Experiment.notes
- Graphの選択理由
- adjustment setの選択理由

ただし、これらを合わせても、

> 過去のどの結果を見て、どの代替案を比較し、なぜ次の実験を選んだのか

を明示的に表す仕様にはなっていません。

「思想」という言葉は要件としては曖昧です。次の表現が適切です。

```text
分析方針の選定理由
実験設計の根拠
Decision Rationale
```

最小限必要なのは、自由記述の`rationale`と、参照元のResult・Claim・Experimentです。

```text
Experiment
├── target Research Question
├── objective
├── hypothesis
├── rationale
├── derived_from Result / Claim
└── Executions
```

独立したDecisionテーブルまでは現時点では不要です。

---

# 4. 元構想を反映した意味論的な構造

現時点の討議を元の構想へ接続すると、次が最も自然です。

```text
Project
= 1つのResearch Topic

Project
└── Research Question Tree
    ├── Research Question
    │   ├── Child Research Questions
    │   ├── Experiments
    │   │   ├── rationale
    │   │   └── Executions
    │   │       ├── Dataset Version
    │   │       ├── Analysis Specification
    │   │       ├── Program / Code Version
    │   │       ├── Parameter
    │   │       ├── Result
    │   │       └── Artifact
    │   └── Claims
    │       └── supported / challenged by Results
    └── Aggregate Claim / Insight
```

## 重要な区別

```text
Research Topic
= Project全体が扱う対象領域

Research Question
= 答えるべき問い

Sub-question
= 上位の問いを検証可能な粒度へ分解した問い

Experiment
= Questionに答えるための分析方針・比較単位

Execution
= 特定条件による一回の計算

Result
= 計算によって得られた事実

Claim / Insight
= Resultを根拠とした問いへの限定付き回答
```

この構造は、現在の意味論的な背骨を壊しません。追加される中心概念は、実質的には以下です。

```text
Research Questionの親子関係
ExperimentからResearch Questionへの参照
Experimentのrationale
Claim間またはQuestion間の集約関係
```

---

# 5. 過剰設計を避ける物理表現

この構想があるからといって、直ちに以下をすべて独立テーブル化する必要はありません。

- Research Topic
- Research Question
- Question Relation
- Significance
- Hypothesis
- Rationale
- Claim Relation

初期段階では、例えば次で十分です。

```text
Project
Analysis Definition Version
  └── research_context_json
      ├── topic
      └── question_tree
          ├── question_key
          ├── parent_question_key
          ├── statement
          ├── significance
          ├── hypothesis
          └── status

Experiment
  ├── target_question_key
  ├── objective
  ├── rationale
  └── executions

Execution
Result / Artifact
```

Question TreeをVersioned JSONとして開始し、独立検索、承認、共同編集などの必要性が確認された段階でResource化する方針が妥当です。これは「概念として必要」と「独立テーブルとして必要」を分離する引継ぎ方針とも整合します。

---

# 6. 日本語としての評価

> 論点でリサーチクエスチョンを分割する

は、意味は伝わりますが、やや不自然です。

問題は2点です。

- 「論点で」より「論点ごとに」または「論点単位で」が自然
- イシューツリーのような構造化には「分割」より「分解」が適切

推奨表現は次です。

```text
上位のリサーチクエスチョンを、
論点ごとのサブクエスチョンへ分解する。
```

さらに正確にするなら、

```text
上位のリサーチクエスチョンを、
検証可能・回答可能な粒度のサブクエスチョンへ
段階的に分解する。
```

となります。

## 構想文の修正版

Ariadneでは、1つのResearch Topicを1つのProjectとして管理する。

Project内では、上位のResearch Questionを論点ごとのSub-questionへ段階的に分解し、各Sub-questionを検証可能・回答可能な粒度まで具体化する。

各Sub-questionに対して1つ以上のExperimentを計画し、Dataset、分析手法、アルゴリズム、パラメータなどの条件を変えた複数のExecutionを実行・比較する。各Experimentには、その分析方針を選定した理由、前提となった仮説、および参照した過去のResultやClaimを記録する。

Executionによって得られたResultを根拠として、各Research Questionへの限定付きの回答であるClaimまたはInsightを記録する。

最終的には、Research Topicから上位のResearch Question、分解されたSub-question、各Questionに対するExperiment、Execution、ResultおよびClaimまでを、イシューツリーのような階層構造として追跡できるようにする。

この構想は現在までの討議と矛盾しません。**現在の設計へ不足しているのは、Question Treeと、Research Question―Experiment―Claim間の明示的な関係です。**

---

## User — 2026-08-05T01:52:51Z

> Research Question―Experiment―Claim間の明示的な関係
私の考え: これは必要かと思う。でなければ、問いから成果物までの来歴管理にならない。
反対意見あれば求む

> Research Topicから上位のResearch Question、分解されたSub-question、
> Question Tree
私の考え: これは私の思想が多分に入っている。実際の実験において、分析をしながらツリー構造を常に対応関係をとりながら整理する分析者は稀。大概後から整理することを考えると、階層構造はサポートせず、プロジェクト配下に複数のリサーチコンテクスト→executionをフラットに持つ構造でよいのではないか

この点について酸性反対の観点から意見を求む

## Assistant

## 結論

両方の考えに概ね賛成です。ただし、次のように修正するのが妥当です。

1. **問いから成果物までの明示的な関連は必要**
2. **Research Questionのツリー構造は初期機能として不要**
3. ただし、完全にフラットにして関係を何も持たないと、分析の反復過程が失われる
4. 初期段階では、**Research Contextをフラットに保持し、任意の軽量な関連だけを許す**のがよい

```text
必須:
Research Context → Experiment/Analysis → Execution → Result

任意:
Research Context間の派生・修正・関連

不要:
常時整備されたQuestion Tree
```

これは、Ariadneの目的である「問いから分析結果までの、なぜ・何を・どう実行し・何が得られたかの来歴管理」と整合します。

---

# 1. Research Question―Experiment―Claim間の関係

## 賛成意見

この関連は意味論上必要です。

これがない場合、Ariadneが管理できるのは次だけです。

```text
Dataset
→ Program
→ Parameter
→ Execution
→ Artifact
```

これは**計算来歴**ではありますが、**分析来歴**ではありません。

分析来歴には、少なくとも次の対応が必要です。

```text
なぜ分析したか
→ 何を明らかにしたかったか
→ どう分析したか
→ 何が得られたか
→ 何を言えると判断したか
```

Ariadneの定義上も、Research Contextは「分析を行う理由と問いの文脈」、ClaimはResultを根拠としたResearch Questionへの限定付き回答とされています。

したがって、問いとExecution・Result・Claimの間に関連がない場合、第三者は以下を復元できません。

- この実験は何を確かめるために行われたか
- 複数の実行のうち、どれが同じ問いに対応するか
- どの結果を根拠にどの結論を出したか
- なぜ別のアルゴリズムやパラメータを試したか
- 結論が変わったのは、問いが変わったためか、データや手法が変わったためか

よって、**意味論的な関連は必須**です。

---

## 反対意見1：線形な鎖として固定すると不正確

ただし、

```text
Research Question
→ Experiment
→ Claim
```

という単純な1対Nの鎖に固定することには反対です。

実際の分析では、関係はより複雑です。

### 1つのExperimentが複数の問いに関係する

例えば因果探索の実験は、次の複数の問いに寄与します。

- 売上の直接原因候補は何か
- クーポンと売上の間の交絡因子は何か
- 広告と来客数の関係は安定しているか

### 1つのClaimが複数のExperimentを統合する

例えば、

> クーポン施策には売上増加効果がある可能性が高いが、推定値は推定器と対象顧客層に依存する

というClaimは、複数の推定器、複数のDataset Version、複数の感度分析から作られます。

### 1つのResultが複数のClaimに使われる

同じATE推定結果から、

- 全顧客に対する平均効果
- 新規顧客への施策候補
- overlap不足による適用範囲の制限

という異なるClaimが作られることがあります。

したがって、論理的には次の方が正確です。

```text
Research Context / Question
    ↕
Experiment / Analysis Definition
    ↓
Execution
    ↓
Result
    ↕
Claim / Interpretation
```

関係は一方向の所有関係というより、**根拠・対象・派生の関係**です。

---

## 反対意見2：問いをExecution開始時の必須項目にすると探索を阻害する

引継ぎサマリーでは、次の原則が置かれています。

```text
Start loose.
Formalize progressively.
Conclude strictly.
```

つまり、分析開始時にはResearch Questionが明確でなくてもよく、分析の進行に伴ってResearch Contextを精緻化する方針です。

そのため、次の制約は強すぎます。

```text
すべてのExecutionは、
確定済みResearch Questionへ必ず所属しなければならない
```

探索的なExecutionでは、開始時点にあるのは次程度かもしれません。

```text
Problem Statement:
最近、店舗間の売上差が拡大している

Objective:
売上差に関係する構造を探索する
```

因果探索後に初めて、

```text
Research Question:
クーポン配布は来客数を介して売上へ影響するか
```

が形成されることがあります。

したがって、明示的な関係は必要ですが、**開始時の確定済みQuestionへの必須リンク**にしてはいけません。

---

# 2. Question Treeをサポートしない判断

## 賛成意見

初期段階でQuestion Treeをサポートしない判断には賛成です。

主な理由は4つあります。

### 理由1：分析中に常時メンテナンスされる可能性が低い

実務では、分析者は以下を並行して行います。

- データ確認
- 欠損や外れ値の調査
- 仮説生成
- 手法変更
- 結果比較
- ステークホルダーとの議論

その都度、問いの階層を厳密に更新するのは負担です。

Question Treeを必須にすると、分析者はAriadneを使うために、分析とは別の「問いの構造化作業」を求められます。

その結果、次のいずれかになりやすいです。

- 空欄のままになる
- 形式的なツリーが作られる
- 分析後にまとめて入力される
- Notebookやメモに戻る
- Ariadne自体が使われなくなる

---

### 理由2：問いの構造は必ずしもツリーではない

実際のResearch Questionの関係は、木構造に収まらないことがあります。

例えば、

```text
Q1: クーポンは売上を増やすか
Q2: クーポンは来客数を増やすか
Q3: 来客数は売上を増やすか
```

Q2とQ3はQ1の下位論点としても扱えますが、別の上位Questionにも再利用できます。

```text
Q4: 店舗施策は来客数を増やすか
```

この場合、Q2はQ1とQ4の両方に関係します。これはツリーではなくDAGまたは一般グラフです。

さらに、問いは分析中に次のように変化します。

```text
売上を改善する要因は何か
↓
クーポンは売上を増加させるか
↓
新規顧客に限定するとクーポンは売上を増加させるか
```

これは単純な親子関係だけでなく、

- 分解
- 精緻化
- 条件追加
- 言い換え
- 棄却
- 統合

を含みます。

最初からQuestion Treeを実装すると、実態に合わない構造を強制する可能性があります。

---

### 理由3：後から整理するなら、UI上のツリーはProjectionでよい

分析後に問いを整理する用途であれば、正本データをツリー構造にする必要はありません。

正本はフラットなResearch Contextと任意のrelationで保持し、必要なときにツリーまたはグラフとして表示できます。

```text
正本:
Research Context A
Research Context B
Research Context C
relation: B refines A
relation: C derived_from A

表示:
A
├── B
└── C
```

つまり、

```text
Question Tree
= 永続化必須のドメインモデル
```

ではなく、

```text
Question Tree
= Research Context間の関係から生成するProjection
```

として扱えます。

---

### 理由4：初期シナリオの価値検証に不要

現在の初期シナリオは次です。

- 複数因果探索結果の比較
- パラメータ感度比較
- Graph選択
- ATE／ATT推定
- 複数推定器比較
- Dataset Versionを変えた再評価
- 来歴比較

これらを成立させるためにQuestion Treeは不要です。

必要なのは、

> この分析または比較が、どの問題意識・目的・問いに基づいて行われたか

を復元できることです。

階層構造までは要求されません。

---

# 3. 完全フラット構造への反対意見

一方で、次の構造だけでは不十分です。

```text
Project
├── Research Context A → Execution
├── Research Context B → Execution
├── Research Context C → Execution
└── Research Context D → Execution
```

Research Context間に何の関連もない場合、次が分かりません。

- BはAを分解したものか
- BはAを修正したものか
- BはAと無関係な別論点か
- CはAの結果を受けて生まれたのか
- Dは過去の問いを再検証しているのか

これでは、個々の分析の来歴は保持できますが、**分析プロセス全体の思考来歴**は失われます。

特に元々の構想にある、

> どのような考えのもとに、その実験方針を決めたのか

を残すには、少なくとも「前の何を受けて次の分析を行ったか」が必要です。

---

# 4. 推奨案：フラット＋任意関係

## 論理構造

初期段階では次が妥当です。

```text
Project
├── Research Context Version
├── Analysis / Experiment
│   ├── Research Contextへの参照
│   ├── rationale
│   └── Execution
│       └── Result
└── Claim / Interpretation
    ├── Research Contextへの参照
    └── Resultへの参照
```

Research Contextはフラットに保持します。

ただし、任意で次の関係を記録できるようにします。

```text
DERIVED_FROM
REFINES
SUPERSEDES
RELATED_TO
REPRODUCES
CHALLENGES
```

初期実装では、このrelationを独立テーブルにする必要はありません。

例えばResearch Context document内に、次を持たせれば十分です。

```json
{
  "context_key": "RC-004",
  "problem_statement": "クーポン施策の効果が不明",
  "research_question": "新規顧客に対してクーポンは購買額を増加させるか",
  "derived_from": ["RC-001", "RESULT-017"],
  "relation_type": "REFINES",
  "status": "DRAFT"
}
```

この程度なら、分析者にツリー維持を要求せず、後から関係を追加できます。

---

# 5. Research Context、Experiment、Execution、Claimの最小関係

## 推奨する関係

### Research Context → Experiment

```text
Experimentは、0または1つの主要Research Contextを対象とする
```

`0`を許す理由は、探索開始時に問いがまだ明文化されていない可能性があるためです。

ただし、結果を正式に採用するときまでにはResearch Contextへ関連付けることを推奨します。

### Experiment → Execution

```text
Experimentは、1つ以上のExecutionを束ねる
```

例：

```text
Experiment:
PCアルゴリズムのalpha感度を評価する

Executions:
alpha=0.01
alpha=0.05
alpha=0.10
```

### Execution → Result

```text
Executionは、0以上のResultを生成する
```

失敗や`NOT_IDENTIFIED`もResult相当として保持するか、Execution outcomeとして保持します。

### Claim → Research Context

```text
Claimは、1つの主要Research Contextに回答する
```

Claimは「何についての主張か」がなければ意味を持ちません。ここは必須でよいです。

### Claim → Result

```text
Claimは、1つ以上のResultを根拠とする
```

複数Resultを許す必要があります。

### Claim → Experiment

直接リンクは必須ではありません。

ResultからExecution、Experimentへ遡れるためです。

```text
Claim
→ Result
→ Execution
→ Experiment
```

ClaimからExperimentへ直接FKを追加すると、同じ情報を二重管理し、不整合を生む可能性があります。

---

# 6. 「明示的な関係」の必要十分条件

問いから成果物までの来歴を実現するために、最低限必要なのは次です。

```text
Research Context
← Experiment / Analysis Definition

Experiment
← Execution

Execution
→ Result / Artifact

Claim
→ Research Context

Claim
→ Result
```

これにより、双方向に追跡できます。

## 問いから成果物へ

```text
Research Context
→ Experiment
→ Execution
→ Result
→ Artifact
```

## 結論から根拠へ

```text
Claim
→ Result
→ Execution
→ Experiment
→ Research Context
```

ここまであれば、Question Treeがなくても「問いから成果物までの来歴」は成立します。

---

# 7. 物理設計についての注意

この関係が必要だからといって、すべてを独立テーブルにする必要はありません。

引継ぎサマリーでも、Research QuestionやClaimは概念として必要だが、当初はVersioned JSON、canonical document、親Resourceのsnapshotとして扱えるとしています。また、独立Resource化は独立ライフサイクル、検索、承認、差分監査などの実需要が現れてから判断する方針です。

初期構成の例：

```text
project

analysis_definition_version
  - research_context_json
  - analysis_specification_json
  - rationale
  - parent_definition_id nullable

execution
  - analysis_definition_version_id
  - execution_snapshot_json

result
  - execution_id
  - result_type
  - result_json

artifact
  - result_id / execution_id

interpretation
  - research_context_key
  - statement
  - evidence_result_ids[]
  - assumptions
  - limitations
```

この構成なら、意味論上の関係を保持しながら、Research Question Tree専用のテーブル群を作らずに済みます。

---

# 8. 最終評価

## Research Question―Experiment―Claim間の関係

**賛成。ただし、単純な線形・1対N構造として固定することには反対。**

必要なのは、次の追跡性です。

```text
問い
↔ 分析方針
↔ 実行
↔ 結果
↔ 解釈
```

## Question Tree

**初期機能としては反対。**

理由：

- 利用中に維持されにくい
- 入力負担が大きい
- 現実の問いは必ずしもツリーにならない
- 現在の検証シナリオに不要
- 後からProjectionとして生成できる

## 完全フラット

**関係を一切持たない完全フラット構造には反対。**

最低限、任意の`derived_from`、`refines`、`supersedes`程度は保持した方がよいです。ただし、これらは初期UIで必須入力にする必要はありません。

## 推奨する正本候補

> Projectは複数のResearch Contextをフラットに保持する。Research Contextの階層構造は必須としない。ExperimentまたはAnalysis Definitionは、その分析が対象とするResearch Contextと分析方針の選定理由を保持し、複数のExecutionを束ねる。ResultはExecutionへ、Claimは回答対象のResearch Contextおよび根拠となるResultへ関連付ける。Research Context間の派生、精緻化、置換等の関係は任意とし、必要に応じて後から追加・表示できるものとする。

この構造が、現時点では**来歴管理を失わず、Question Treeの過剰設計も避ける折衷案**です。

---

## User — 2026-08-05T02:35:07Z

以下、二つの検証シナリオ案リストの関係はどのようなものか？包含関係か？補完し合う関係にあるのか？
また、接頭辞が VS と BS で異なるのはなぜか？各々どのような意味を持っているのか？

> 3. 最小検証シナリオ案
> VS-01: 探索的分析から候補仮説を形成する
> ...

> 初期検証シナリオ
> BS-01：複数因果探索アルゴリズムによるGraph候補比較
> ...

## Assistant

## 結論

両リストの関係は、**単純な包含関係でも、完全な補完関係でもありません**。

より正確には、

> **VSは上位の業務・価値検証シナリオ、BSは事業データ用途に限定してVSを機能単位へ分解・具体化したシナリオ群。ただし、BSにはVSから独立して追加された異常系・再評価シナリオも含まれる。**

という関係です。

また、`VS`と`BS`は既存仕様上の正式な接頭辞ではありません。私が会話中に導入した便宜的な名称であり、定義を明示せずに切り替えたのは不適切でした。

---

# 1. VSとBSの粒度の違い

## VS：上位の価値検証シナリオ

VSは、利用者の目的と業務上の成果を中心にした**エンドツーエンドのシナリオ**です。

例えばVS-01は、

```text
曖昧な問題意識
→ データ登録
→ 因果探索
→ 複数結果比較
→ Graph選定
→ 候補仮説の形成
```

までを一つの利用者タスクとして扱っています。

VSが検証しようとしているのは、個別機能よりも次です。

- 利用者が分析目的を達成できるか
- Ariadneを使用する価値があるか
- 問い、分析、結果、解釈が接続されるか
- NotebookやCLIと比べた来歴・比較機能に価値があるか

## BS：事業データ向けの機能・分析工程シナリオ

BSは、売上改善などの事業データ用途を前提として、因果分析プロセスをより細かく分解したものです。

例えば、

```text
BS-01 複数探索アルゴリズム比較
BS-02 同一アルゴリズムのパラメータ感度比較
BS-03 Graph選定・修正
BS-04 ATE/ATT推定
BS-05 複数推定器比較
```

という形です。

BSが主に検証するのは次です。

- 個々の分析工程が成立するか
- どの情報・Resource・来歴が必要か
- Executionをどの単位で分離するか
- 比較UIに何を表示すべきか
- 推定不能などの異常系をどう扱うか

---

# 2. 対応関係

## VS-01とBSの関係

### VS-01

> 探索的分析から候補仮説を形成する

主な流れは次でした。

```text
データ登録
→ 因果探索
→ 複数結果比較
→ Graph候補選定
→ 候補仮説の記録
```

対応するBSは主に以下です。

| VS-01の工程 | 対応するBS |
|---|---|
| 複数アルゴリズムで探索 | BS-01 |
| 同一アルゴリズムの感度確認 | BS-02 |
| Graph候補の選定・修正 | BS-03 |
| データ更新後の再探索 | BS-07の一部 |

したがって、

```text
BS-01 + BS-02 + BS-03
⊂ VS-01
```

に近い関係です。

ただし、完全な包含ではありません。BS側には、VS-01にあった次の要素が明示されていません。

- 曖昧なProblem Statementから開始する
- 候補仮説を記録する
- 次に検証すべき問いへ接続する
- Research Contextを段階的に精緻化する

つまり、BS-01〜03はVS-01の**分析計算部分を詳細化したもの**であり、Research Contextと仮説形成の部分は欠けています。

---

## VS-02とBSの関係

### VS-02

> 明示した因果仮説を評価し、条件を変えて再評価する

主な流れは次でした。

```text
Research Question
→ Causal Design
→ 推定
→ Diagnostics
→ 条件変更による再実行
→ 結果比較
→ 限定付きClaim
```

対応するBSは以下です。

| VS-02の工程 | 対応するBS |
|---|---|
| Graphの確定 | BS-03 |
| ATE/ATT推定 | BS-04 |
| 複数推定器比較 | BS-05 |
| 推定不能・信頼不能 | BS-06 |
| Dataset Versionを変えた再評価 | BS-07 |

したがって、

```text
BS-03〜BS-07
≈ VS-02の分析工程を分解・拡張したもの
```

です。

ただし、こちらも完全な包含ではありません。

### BSが詳細化した部分

- Graph選定と手動修正
- 推定器比較時に固定すべき条件
- `NOT_IDENTIFIED`や`INSUFFICIENT_OVERLAP`
- Dataset Version変更による再評価

### VSにあり、BSで弱くなった部分

- Research Questionとの明示的な関係
- Experimentの目的と選定理由
- ClaimがどのResultを根拠とするか
- 仮定・限界を含む正式な解釈
- 問いから成果物までの来歴

よってBSは、VS-02を単純に包含するのではなく、**科学計算・比較部分を深掘りする一方、研究文脈部分を省略した派生形**です。

---

## VS-03とBSの関係

### VS-03

> 第三者が結果の根拠をレビューする

これに直接対応するBSはありません。

BS群では来歴比較を横断要件として扱っていますが、次の第三者タスクは独立して検証されていません。

- 分析を実施していない人が結果を理解する
- Claimから根拠Resultへ遡る
- Dataset、Graph、Parameter、Diagnosticsを確認する
- 承認、条件付き承認、差戻しを判断する

したがって、

```text
VS-03はBSに包含されていない
```

となります。

BSの来歴機能が技術的に実装されても、第三者が実際に判断できるとは限りません。VS-03は独立して残す必要があります。

---

# 3. BS側に新しく追加されたもの

BSには、VSを単に分解しただけではない追加シナリオがあります。

## BS-06：推定不能・信頼不能

VS-02の失敗条件として類似内容はありましたが、独立した検証シナリオにはなっていませんでした。

BS-06では、

- `NOT_IDENTIFIED`
- `ESTIMATION_UNRELIABLE`
- `INSUFFICIENT_OVERLAP`
- `INSUFFICIENT_SAMPLE`

などを、正式な分析結果として扱うところまで具体化しています。

これはVSの**異常系・負の結果を補完するシナリオ**です。

## BS-07：異なるDataset Versionでの再評価

VS-02では主にEstimatorやParameter変更を扱っていました。

BS-07は、

```text
分析条件を固定
＋
Dataset Versionだけを変更
```

という別の比較軸を追加しています。

これはAriadneのVersion・Execution・Lineage管理を検証する上で重要ですが、元のVSでは独立していませんでした。

---

# 4. 関係を図式化すると

```text
上位の価値検証シナリオ

VS-01 探索から仮説形成
├── BS-01 複数探索アルゴリズム比較
├── BS-02 パラメータ感度比較
└── BS-03 Graph選定・修正
    ※候補仮説形成とResearch Context更新はBSに未収録

VS-02 明示的な問いの因果効果評価
├── BS-03 Graph選定・修正
├── BS-04 ATE/ATT推定
├── BS-05 複数推定器比較
├── BS-06 推定不能・信頼不能
└── BS-07 Dataset Version再評価
    ※Claim・分析方針の理由・問いとの関係はBSで弱い

VS-03 第三者レビュー
└── 対応するBSなし
```

BS-03はVS-01とVS-02の双方に登場します。

これは不整合ではありません。Graph選定は、

- 探索から候補仮説を形成する段階
- 明示的な問いについて因果効果を推定する段階

の接続点だからです。

---

# 5. 包含か、補完か

## 包含関係としての側面

BS-01〜05は主に、VS-01・VS-02の内部工程を詳細化しています。

したがって、一部は明確に包含関係です。

```text
BSの複数項目
⊂
1つのVS
```

## 補完関係としての側面

一方、次は補完関係です。

- BS-06が負の結果・推定不能を補完
- BS-07がDataset更新による再評価を補完
- VS-03がBSにはない第三者レビューを補完
- VS側がBSには弱いResearch Context・Claimを補完

したがって全体としては、

> **BSはVSを工程別に分解した下位シナリオ群であり、一部の追加シナリオによってVSを補完している**

という説明が最も正確です。

---

# 6. 接頭辞の意味

## `VS`

私が意図していた意味は、**Validation Scenario**です。

目的は、Ariadneが利用者価値を提供できるか検証することです。

対象：

- 業務目的
- 利用者の判断
- エンドツーエンドの作業
- Research Contextから結果・解釈まで
- Ariadne固有の価値

## `BS`

案Aの「事業データ中心」を選択した後に、私は事業用途へ絞ったシナリオとして`BS`を使いました。

文脈上の意図は、**Business-data Scenario**または**Business Scenario**です。

ただし、これは明示的に定義しておらず、正式名称でもありません。後から意味を推定できるものの、命名として一貫していません。

また、`Business Scenario`という名称にも問題があります。VS-01〜03も業務シナリオであり、両者の違いが名前から分からないためです。

---

# 7. 推奨する命名の統一

今後は、接頭辞を用途ではなく**抽象度**で分ける方が明確です。

## 案1：E2EとASに分ける

### `E2E`

End-to-End Validation Scenario。

```text
E2E-01 探索的分析から候補仮説を形成する
E2E-02 明示した因果仮説を評価する
E2E-03 第三者が結果をレビューする
```

### `AS`

Analysis Scenario。

```text
AS-01 複数因果探索アルゴリズム比較
AS-02 パラメータ感度比較
AS-03 Graph選定・修正
AS-04 ATE/ATT推定
AS-05 複数推定器比較
AS-06 推定不能・信頼不能
AS-07 Dataset Version再評価
```

この分類が最も分かりやすいです。

---

## 案2：VSを上位として残す

```text
VS-01 探索から候補仮説形成
  ├─ VS-01.1 複数アルゴリズム比較
  ├─ VS-01.2 パラメータ感度比較
  └─ VS-01.3 Graph選定

VS-02 因果仮説評価
  ├─ VS-02.1 ATE/ATT推定
  ├─ VS-02.2 推定器比較
  ├─ VS-02.3 推定不能
  └─ VS-02.4 Dataset Version再評価

VS-03 第三者レビュー
```

こちらは包含関係を直接番号で表せます。

ただし、Graph選定のように複数VSへまたがるシナリオを重複配置する問題があります。

---

# 8. 推奨整理

私は**案1**を推奨します。

| 階層 | 接頭辞 | 意味 |
|---|---|---|
| 上位 | E2E | 利用者目的を完結させる一連の価値検証 |
| 下位 | AS | 因果分析工程・比較機能の検証 |
| 横断 | CR | Comparison / Lineageなどの共通要件 |

整理すると次です。

```text
E2E-01 探索的分析から候補仮説を形成する
E2E-02 明示した因果仮説を評価する
E2E-03 第三者が結果をレビューする

AS-01 複数探索アルゴリズム比較
AS-02 パラメータ感度比較
AS-03 Graph選定・修正
AS-04 ATE/ATT推定
AS-05 複数推定器比較
AS-06 推定不能・信頼不能
AS-07 Dataset Version再評価

CR-01 複数Result比較
CR-02 Resultから来歴への遡及
CR-03 上流Resultを下流分析入力として同定
CR-04 Research ContextからClaimまでの追跡
```

## 最終回答

- **VSとBSは、部分的には包含、部分的には補完関係**
- VSは上位のエンドツーエンド価値検証
- BSは事業データ用途に限定した分析工程の詳細化
- BS-06、BS-07はVSを補完する追加シナリオ
- VS-03には対応するBSがなく、独立して残る
- `VS`と`BS`は会話中に私が導入した便宜的名称で、正式な定義はなかった
- 今後は`E2E`、`AS`、`CR`へ統一するのが妥当です


---

## User — 2026-08-05T02:48:45Z

具体的に成果物に落とそうと思う。以下を出力してほしい。観点に不足があれば提示してほしい


- 00_プロダクトコンセプトメモ: プロダクトのコンセプトを説明した資料。ariadne の設計思想を表現した記述をまとめる。このプロ
- 10_要件定義
    - 業務一覧: ariadne で実行可能な操作=業務をリストアップ
        - 以下はこれまでに出てきた例。議論を踏まえ、追加項目があるならば追加のこと。また、重複があるならば統合すること
            1. Dataset Upload: 前処理済みデータを登録しDataset Versionを固定
            2. Discovery Comparison: 複数の因果探索アルゴリズムを実行・比較
            3. Discovery Sensitivity: 同一アルゴリズムの複数パラメータ結果を比較
            4. Graph Selection: 候補Graphを選択し、必要に応じて編集・方向付け
            5. Graph Version Fixing: 因果推論で使用するGraph Versionを確定
            6. Causal Design: treatment、outcome、estimand、population、: adjustment set、assumptionsを設定
            7. Estimator Comparison: 複数の推定器でATEまたはATTを推定
            8. Result Comparison: 推定値、信頼区間、diagnosticsを比較
            9. Lineage Review: Dataset、Graph、algorithm、parameter、code、Artifactまで遡る
            10. Interpretation:  採用結果、選定理由、仮定、限界を記録
            11. 上流結果を下流分析の入力として同定
    - 業務シナリオ: ariadneで実行可能な検証シナリオをリストアップ（用語の理解に齟齬あれば訂正のこと）
        - E2Eシナリオ: 利用者への利用価値提供可能性の検証
            - E2E-01 探索的分析から候補仮説を形成する
            - E2E-02 明示した因果仮説を評価する
            - E2E-03 第三者が結果をレビューする
        - 分析シナリオ: E2Eシナリオにおける、分析作業のシナリオ
            - AS-01 複数探索アルゴリズム比較
            - AS-02 パラメータ感度比較
            - AS-03 Graph選定・修正
            - AS-04 ATE/ATT推定
            - AS-05 複数推定器比較
            - AS-06 推定不能・信頼不能
            - AS-07 Dataset Version再評価
        - 横断シナリオ: 各シナリオ間で共通して登場するシナリオのサブセット
            CR-01 複数Result比較
            CR-02 Resultから来歴への遡及
            CR-03 上流Resultを下流分析入力として同定
            CR-04 Research ContextからClaimまでの追跡

    - 機能要件
        - カバーしているアルゴリズム

    - アーキテクチャ要件
        - 上記機能は、以下の参照方法で機能を利用できるようにすること
            - Web アプリ
            - Web API
            - CLI

- 21_論理データ設計: 
    - この業務要件を成立させるエンティティの最小構成を出力。以下は例
        - Project: 分析テーマと境界
        - Dataset: データの論理単位
        - Dataset Version: 実際に使用したデータの固定
        - Analysis Definition Version: 探索または推論の分析条件
        - Execution: 各アルゴリズム・各パラメータ・各推定器の実行
        - Result: 比較対象となる論理結果
        - Artifact: Graphファイル、表、diagnostics等
        - Causal Graph Version: 選択・編集・再利用されるGraph
        - Relation / Lineage: 探索結果からGraph、Graphから推論への関係
        - Comparison: 複数Resultの比較条件と表示- 22_プロダクト基本設計: 

## Assistant

4つのMarkdown成果物として整え、相互参照できる構成にします。現行コードと引継ぎ資料を照合し、実装済み・要求・将来候補を混同しないよう明示します。

## Assistant

不足観点として、識別可能性判定、負の結果、Research Context―Experiment―Claimの追跡、役割・権限、非機能要件、インターフェース間の責務差を追加します。特に「全機能をWeb/API/CLIで同一提供」は現行方針と衝突するため、分析能力の共通化と管理機能の露出を分けます。

## Assistant

成果物をMarkdownで作成しました。引継ぎサマリーの設計方針と、現行コードのアルゴリズム・Web/API/CLI構成を照合しています。

## 成果物

- `ariadne_design_draft_20260805.zip`
- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`
- `README.md`

## 主な整理・追加点

### 業務一覧

提示された11項目を、以下の領域に再編しました。

- Research Context・Project管理
- Dataset管理
- 因果探索
- Graph管理
- Causal Design・推論
- 比較・来歴・解釈
- Execution運用

`Graph Selection`と`Graph Version Fixing`は同一ライフサイクルとして統合しています。

### シナリオ

以下の3層に統一しました。

- `E2E`: 利用者価値を検証するEnd-to-Endシナリオ
- `AS`: E2E内の分析工程
- `CR`: 複数シナリオに横断する共通能力

さらに、別条件で同じ問いを再評価する`E2E-04`と、分析方針の選定理由を追跡する`CR-05`を追加しました。

### 不足していた重要要件

以下を追加しています。

- 識別可能性の確認
- `NOT_IDENTIFIED`等を正式な分析結果として扱う要件
- Research Context―Experiment―Execution―Result―Interpretationの追跡
- Graph種別とendpoint意味の保持
- 介入可能性・機微性などの変数semantics
- Actor、権限、非機能要件
- Scientific outcomeとTechnical failureの分離
- 比較時の「同一条件・変更条件・結果差分」
- Exportおよびportable analysis package

### 論理データ設計

提示例に加えて、以下を最小構成に追加しました。

- Research Context
- Experiment
- Interpretation / Claim

一方、`Comparison`は初期の正本Entityから外し、**Result群から生成するProjection**としました。保存、共有、承認などの独立ライフサイクルが確認された場合のみResource化する方針です。

### Web App・Web API・CLI

「全機能を3経路で同一提供する」という要件は採用していません。

- 科学計算ロジックは共通化
- Web Appは共同作業・比較・レビュー
- Web APIはResource、Version、Execution、Lineageの正本
- CLIはローカル計算、Manifest、Artifact生成
- CLIではAriadne `execution_id`を生成しない

という責務分担にしています。

## 次に必要な成果物

今回の4文書から直接導かれる未作成物は、**E2E検証プロトコル**です。半人工Dataset、被験者への課題文、観察項目、完了条件、失敗条件を具体化しない限り、要件の必要性はまだ検証できません。

---

## User — 2026-08-05T03:18:45Z

レビュー結果は後で返却するが、これ、現状のコードベースからの修正とゼロベースでの構築と、どちらの方が効率良く作製できるか？もっと言うならばコーディングエージェントに任せた際に、トークンの消費量を抑えられるのは既存改修とゼロベース構築のどちらか？

## Assistant

現行コードの再利用可能部分と、設計変更で破棄・統合が必要な部分を分けて評価します。判断軸は開発工数だけでなく、コーディングエージェントの探索トークン、変更波及、テスト再利用性です。

## Assistant

現時点では、二択なら「全面的な既存改修」より「最小構成を新設して既存の科学計算資産を再利用」が有力です。フル・ゼロベースも、因果アルゴリズムと回帰試験を捨てるため非効率です。

## Assistant

## 結論

**二択なら、現行コードベースの全面改修より、プロダクト層をゼロベースで構築する方が効率的です。**

ただし、推奨するのは完全なゼロベースではありません。

> **科学計算部分は既存資産を再利用し、Webプロダクト・データモデル・業務導線を新規構築する。**

分類すると、次の方式です。

```text
科学計算コア     : Brownfield／既存再利用
プロダクト層     : Greenfield／新規構築
既存Control Plane: 段階的に置換・廃止
```

いわゆる**Strangler方式の段階的再構築**です。

コーディングエージェントのトークン消費も、この方式が最も少なくなる可能性が高いです。

---

# 1. 三つの選択肢の比較

| 方式 | 開発効率 | エージェントのトークン効率 | 主な問題 |
|---|---:|---:|---|
| 現行コードを全面改修 | 低〜中 | 低 | 既存設計の理解、影響分析、migration、回帰修正が重い |
| 完全ゼロベース | 低〜中 | 中 | 科学計算・検証・CLI・Artifact処理まで再実装が必要 |
| **プロダクト層新設＋計算コア再利用** | **高** | **高** | 境界設計と一時的な二重構造が必要 |

## 強制的に二択する場合

「ゼロベース」を以下の意味で捉えるなら、ゼロベースが優位です。

```text
新しい最小データモデル
新しいAPI
新しいWeb UI
新しいE2E導線
ただし既存の因果探索・因果推論コードはライブラリとして再利用
```

一方、次の意味での完全ゼロベースには反対です。

```text
因果探索アルゴリズムも再実装
ATE/ATT推定器も再実装
Diagnosticsも再実装
CLIも再実装
Artifact Storeも再実装
科学的回帰試験も作り直す
```

これは既存資産を捨てるため、トークンも工数も増えます。

---

# 2. 現行コードの構成から見た判断

アップロードされたコードを静的集計すると、Pythonコードは約23,870行です。

大まかな内訳は次のとおりです。

| 分類 | LOC概算 | 判断 |
|---|---:|---|
| 因果探索・因果推論・前処理・Discovery Service | 約9,563 | 再利用候補 |
| Web Control Plane・Worker・Metadataモデル | 約8,426 | 大部分を再設計 |
| Artifact Store・MLflow・Port | 約1,275 | 選択的に再利用 |
| CLI・Pipeline | 約1,993 | CLIは再利用、Pipelineは再評価 |
| ETL固有処理 | 約803 | 初期対象外または分離 |
| その他 | 約1,810 | 個別判断 |

つまり、**およそ4割の科学計算資産は再利用価値があり、3分の1超のControl Planeは新要件に対して負債になりやすい**構成です。

現行実装には、すでに以下があります。

- PC、GES、LiNGAM、NOTEARS
- ATE／ATTと複数Estimator
- Discovery／Inference Application Service
- Dataset Version
- Execution
- Artifact
- Causal Graph Version
- CLI
- FastAPI
- Worker
- Artifact Store
- MLflow Adapter

新設計で主に不足しているのは、Research Context、Experimentとの明示的関係、Interpretation、比較Projection、問いから成果物までの来歴とE2E画面導線です。

この状況で計算部分まで捨てる合理性はありません。

---

# 3. 現行コードの全面改修が高コストになる理由

## 3.1 既存ERが新しい最小モデルより大きい

現行コードにはSQLAlchemyモデルが65あります。

特にExecution周辺には、以下が分離されています。

- `execution`
- `execution_plan`
- `stage_execution`
- `stage_attempt`
- stage input各種
- planning時input preparation
- attempt時input preparation
- stage parameter
- manifest
- event
- outbox
- audit
- 各種projection

一方、現在の設計方針では、複数の概念をVersioned JSON、snapshot、再生成可能Projectionへ統合することを検討しています。

既存改修を行う場合、単純に不要テーブルを消すだけでは済みません。

```text
ORM
→ repository
→ application service
→ worker
→ API schema
→ router
→ migration
→ tests
→ frontend
```

まで変更が波及します。

コードを減らすための作業であっても、エージェントは削除対象が本当に未使用かを確認するために、広範囲を読む必要があります。

---

## 3.2 巨大な集中モジュールがある

特に大きいファイルは以下です。

| ファイル | 行数概算 |
|---|---:|
| `application/run_execution/services.py` | 1,543 |
| `domain/metadata.py` | 1,481 |
| `workers/executor.py` | 967 |
| `causal/discovery/config.py` | 706 |
| `interfaces/api/routers/datasets.py` | 605 |
| `causal/inference/estimators/treatment_effect.py` | 568 |

既存改修では、エージェントが一つの機能変更を行うたびに、これらの大規模ファイルと周辺依存を繰り返し読む可能性があります。

これはトークン消費に直結します。

---

## 3.3 「追加」より「意味の変更」が多い

新要件との差分は、単なる機能追加ではありません。

例：

- Execution中心UIからResearch Context／Experiment中心UIへ変更
- ResultとInterpretationを分離
- Comparisonを永続EntityではなくProjectionとして扱う
- Scientific outcomeとTechnical failureを分離
- Graphの型・endpoint semanticsを維持
- 問いから成果物までのLineageを追加
- 一部の独立テーブルをJSON／snapshotへ統合

これは既存構造へフィールドを追加する作業ではなく、**集約境界の変更**です。

集約境界の変更は、一般にインプレース改修と相性が悪いです。

---

## 3.4 不要な既存機能がエージェントを迷わせる

初期Golden Pathでは、以下は必ずしも必要ありません。

- 複数Artifact Storeの完全対応
- 全監査・可視化Projection
- 汎用Pipeline Definition
- 複雑なStage input preparation
- CompleteJourney固有ETL
- 全Supporting Resource
- 詳細なRBAC
- 高度なretry／lease／heartbeat

しかし既存コード内に存在するため、エージェントは次を判断し続ける必要があります。

- 残すのか
- 消すのか
- 新機能と接続するのか
- 互換性を維持するのか
- テストを修正するのか

これはコード生成量以上に、**判断・探索トークン**を消費します。

---

# 4. 完全ゼロベースにも反対する理由

## 4.1 科学計算コードは再実装コストが高い

通常のCRUDと異なり、因果探索・推論コードは「動いた」だけでは不十分です。

必要なのは以下です。

- 数値妥当性
- 入力条件の検証
- Algorithm固有parameter
- random seed
- Graph表現
- diagnostics
- synthetic dataによる検証
- regression tolerance
- estimator間の整合性

エージェントに新規実装させる場合、コード生成だけでなく、科学的検証のための反復が必要です。

9,000行超の既存科学計算領域を捨てると、トークン節約にはなりません。

## 4.2 既存テストが比較基準として使える

既存テストは約5,291行あります。

すべてをそのまま流用できるわけではありませんが、少なくとも次には使えます。

- Characterization Test
- 数値Regression Test
- CLI互換性確認
- Graph serialization確認
- Treatment Effect推定確認
- negative case確認

ゼロベースでこれらも作り直すと、実装トークンより検証トークンが増えます。

---

# 5. トークン消費の構造

コーディングエージェントのトークン消費は、単純な生成コード量では決まりません。

概ね次の和です。

```text
既存コードの探索
+ 仕様理解
+ 依存関係の推定
+ 実装
+ テスト失敗の解析
+ 修正
+ 回帰影響の確認
```

## 現行全面改修

```text
探索コスト       大
依存分析         大
生成コード       中
migration        大
回帰解析         大
```

## 完全ゼロベース

```text
探索コスト       小
仕様理解         中
生成コード       大
科学的検証       大
回帰試験作成     大
```

## 推奨方式

```text
探索コスト       中〜小
依存分析         小〜中
生成コード       中
科学的検証       小〜中
migration        小
```

したがって、トークン消費の順位はおそらく次です。

```text
最小:
新プロダクト層 + 既存科学計算コア再利用

次点:
完全ゼロベース

最大:
既存Control Planeを維持したまま全面改修
```

ただし、これは静的構造に基づく推論です。実測トークン数ではありません。正確な比較には、同一の小規模機能を各方式でエージェントへ実装させるベンチマークが必要です。

---

# 6. 推奨する再構築方式

## Phase 0：既存科学計算コアを隔離する

最初に、新旧どちらからも利用できる安定した境界を作ります。

```text
Scientific Core
├── Discovery
├── Inference
├── Graph representation
├── Diagnostics
└── Manifest / Result DTO
```

再利用候補：

- `ariadne.causal.discovery`
- `ariadne.causal.inference`
- `ariadne.causal.design`
- `ariadne.preprocessing.common`
- `ariadne.application.discovery`の純粋部分
- Artifact／MLflow Port

ただし、既存のDiscovery Application ServiceはETL Provider等への依存があるため、そのままではなく**依存を切り離してAdapter化**する必要があります。

実際、現環境でテストを収集した際、DiscoveryのimportからCompleteJourney ETLとDaskまで読み込む構造、APIのimportからAzure SDKまで読み込む構造が確認されました。これはテスト失敗そのものの証明ではありませんが、コアと任意Adapterの結合が強いことを示します。

## Phase 1：新しい最小プロダクト層を作る

既存Metadataモデルを直接削りながら作るのではなく、別境界に作ります。

例：

```text
src/ariadne/product_v2/
├── domain/
├── application/
├── persistence/
├── api/
└── projections/
```

またはパッケージ名を分けず、明確なbounded contextとして配置します。

初期対象：

- Project
- Research Context
- Dataset／Dataset Version
- Experiment
- Analysis Definition Version
- Execution
- Result
- Artifact
- Causal Graph Version
- Interpretation
- Lineage
- Comparison Projection

論理Entityをすべて独立テーブルにしないという方針は、現在の論理設計でも明示されています。

## Phase 2：Golden Pathだけ接続する

次だけを最初に成立させます。

```text
Dataset Upload
→ Discovery batch
→ Graph comparison
→ Graph selection
→ Causal Design
→ ATE/ATT
→ Estimator comparison
→ Interpretation
→ Lineage review
```

既存APIとの互換性を初期要件にしない方がよいです。

## Phase 3：旧資産を選択的に移植する

必要性が確認できたものだけを移植します。

- cancel
- retry
- outbox
- stage attempt
- RBAC
- S3／Azure
- audit
- MLflow
- export

この順序なら、「既存にあるから移植する」ではなく、「E2Eに必要だから移植する」になります。

## Phase 4：旧Control Planeを廃止する

Golden Pathが新構造で成立した後に、

- 旧Router
- 旧Repository
- 旧Projection
- 旧テーブル
- 旧Frontend

を削除します。

最初から削除と新規実装を同時に行わないことが重要です。

---

# 7. エージェントへの与え方

トークン削減には、方式よりタスク分割の方が効く場合があります。

## 悪い依頼

```text
現行Ariadneを新要件に合うよう全面的に修正せよ
```

この依頼では、エージェントが338ファイルを広範に探索します。

## 良い依頼

```text
対象:
E2E-01のうちResearch Context、Experiment、Discovery batch、
Result Comparisonまで

再利用してよい:
ariadne.causal.discovery
ariadne.application.ports.artifact_store

変更禁止:
legacy API
legacy metadata models
legacy worker

出力:
新規product_v2 package
SQLite migration
API
component tests
```

この方式なら、各タスクで読むべきコードを限定できます。

## エージェント用Context Pack

毎回リポジトリ全体を読ませず、次だけを与えます。

- `00_プロダクトコンセプトメモ`
- 対象E2E／AS／CR
- 対象Entity
- 対象API契約
- 再利用可能module一覧
- 変更禁止module一覧
- 受入れテスト
- Architecture Decision Record

これにより、セッションごとの再探索を抑えられます。

---

# 8. 再利用・再設計・廃止の暫定分類

## 原則再利用

- 因果探索アルゴリズム
- 因果推論Estimator
- Graphの基本処理
- Diagnosticsの数値処理
- CLIの科学計算経路
- Artifact StoreのPort
- MLflow Adapter
- synthetic／scientific test

## Adapterを挟んで再利用

- Discovery Application Service
- Inference Application Service
- Dataset read／profile
- Local Artifact Store
- Worker execution wrapper
- Configuration loader

## 新規構築

- Research Context
- ExperimentとResearch Contextの関係
- Experiment rationale
- Interpretation／Evidence
- Comparison Projection
- 新しいLineage
- E2E Web UI
- Identification outcome
- Scientific outcome model

## 原則として旧構造を直接改修しない

- 65モデルのMetadata全体
- 1,543行の`run_execution/services.py`
- 既存Projection群
- 型別stage inputテーブル群
- planning／attempt input preparation分割
- 既存1,073行の単一`frontend/app.js`

---

# 9. 最終判断

## 工数を最小化するなら

> **既存科学計算資産を利用した新規Vertical Slice**

## エージェントのトークンを最小化するなら

> **既存コードを変更禁止領域と再利用領域に分け、新しいbounded contextへGolden Pathだけを実装する**

## 避けるべき方式

> 65テーブルと既存Control Planeを維持したまま、Research Context、Interpretation、Comparison、Lineageを追加し、後から不要部分を削る方式

これは短期的には既存改修に見えますが、最終的に、

```text
旧設計の理解
+ 新設計の実装
+ 両者の整合
+ migration
+ 不要部分の削除
```

をすべて行うため、最もトークンを消費しやすいです。

**推奨は「フルリライト」ではなく、「科学計算コアを残したプロダクト層の再構築」です。**

---

## User — 2026-08-05T03:25:47Z

あと、最小構成といいつつ、エンティティの数も画面数もかなり多いのでは？

## Assistant

指摘は妥当です。作成した論理データ設計と基本設計を見直し、「意味論上の概念」「永続エンティティ」「画面」を分離して、実際の最小構成まで削れるか評価します。

## Assistant

はい。**現状の成果物は「最小構成」と呼ぶには大きすぎます。**  
私が、意味論上区別すべき概念と、初期リリースで独立実装すべきEntity・画面を十分に分離できていませんでした。

## 1. 現在案の規模

`21_論理データ設計.md`では、実質的に以下の13概念を論理Entityとして挙げています。

1. Project
2. Research Context
3. Dataset
4. Dataset Version
5. Experiment
6. Analysis Definition Version
7. Execution
8. Result
9. Artifact
10. Causal Graph
11. Causal Graph Version
12. Interpretation
13. Lineage Relation

加えてComparison Projection、Stage Execution、Stage Attemptがあります。

`22_プロダクト基本設計.md`では、主要ナビゲーションが8項目あり、個別画面候補も概ね以下まで分かれています。

- Project Overview
- Research Context
- Dataset
- Experiment
- Discovery Setup
- Discovery Comparison
- Graph Workbench
- Causal Design
- Identification / Preflight
- Inference Result
- Result Comparison
- Interpretation / Review

これは**ターゲットとなるプロダクト全体像**としては理解できますが、初期価値検証用のVertical Sliceとしては重いです。

---

# 2. なぜ膨らんだか

主な原因は3つあります。

## 2.1 意味論上の区別を、そのまま独立Entityへ寄せた

例えば以下は概念として区別する必要があります。

```text
Research Context
Experiment
Analysis Definition
Execution
Interpretation
```

しかし、

```text
概念として区別する
≠ 独立テーブルにする
≠ 独立画面にする
≠ グローバルナビゲーションに置く
```

です。

文書では「独立テーブル数を意味しない」と断っていますが、基本設計では各概念がほぼ個別モジュール・個別画面へ展開されています。結果として、実装上は分離したのと近い負担になります。

## 2.2 E2E-01〜04をすべて初期実装対象へ寄せた

特に以下が初期構成を大きくしています。

- 第三者レビュー
- Interpretationの正式管理
- Dataset Versionを変えた再評価
- Identificationの独立画面
- Research ContextのVersion履歴
- Execution運用
- Graph編集履歴
- Export
- Role別操作

これらは重要ですが、最初の価値仮説、

> 複数の因果探索・推論結果を比較し、採用結果と来歴を確認できることに価値があるか

を検証するだけなら、全ては不要です。

## 2.3 Entityと画面を対応させすぎた

EntityごとにCRUD画面を作る設計は避けるべきです。

利用者が行うのはEntity管理ではなく、次の分析作業です。

```text
データを登録する
→ 探索する
→ 比較する
→ Graphを選ぶ
→ 推論する
→ 結果を比較する
→ 根拠を確認する
```

したがって、画面はEntityではなく**作業単位のWorkspace**としてまとめる方がよいです。

---

# 3. 初期検証に必要な最小Entity

初期Golden Pathを次に限定します。

```text
前処理済みDatasetを登録
→ 複数条件で因果探索
→ Graphを比較・選定
→ ATE/ATT推定
→ 複数推定器を比較
→ 使用条件と来歴を確認
```

この場合、物理的な正本Entityは次の7つ程度まで削れます。

## 3.1 Project

分析テーマとデータ・実行の境界。

保持するもの：

- name
- topic / objective
- optional memo

Research Topicの独立Entityは不要です。

## 3.2 Dataset Version

初期段階では、`Dataset`と`Dataset Version`を物理的に分離しなくてもよいです。

```text
dataset_version_id
project_id
dataset_key
name
content_hash
schema
artifact_location
```

`dataset_key`が同じものを同一Dataset系列とみなせます。

Dataset一覧・Version一覧が本当に必要になった段階で、Dataset Resourceを分離します。

## 3.3 Execution

探索・推論の各実行を表します。

Research Context、Experiment、Analysis Definition、Execution Planを独立Entityにせず、Executionへsnapshotとして保持します。

```text
execution_id
project_id
batch_key
operation
objective
rationale
dataset_version_id
input_graph_version_id
algorithm / estimator
parameter_json
analysis_spec_json
code_version
status
timestamps
```

ここで、

- `objective`：何を確認する実行か
- `rationale`：なぜこの条件で実行するか
- `batch_key`：複数Executionを一括操作・比較単位として束ねる

とします。

初期段階では、これでExperimentの主要役割を代替できます。

## 3.4 Result

利用者が比較する論理結果。

```text
result_id
execution_id
result_type
scientific_status
summary_json
diagnostics_json
```

`NOT_IDENTIFIED`、`INSUFFICIENT_OVERLAP`等もResultとして保持します。

## 3.5 Artifact

Graph JSON、表、ログ、レポート等の物理ファイル。

Resultとは分けた方がよいです。

## 3.6 Graph Version

これは独立Entityとして残す理由があります。

- 探索結果を人間が選定する
- 必要に応じて編集する
- 因果推論の入力として再利用する
- 元のDiscovery Resultへ遡る

ただし、`Causal Graph`と`Causal Graph Version`の2階層は初期には不要です。

```text
graph_version_id
project_id
source_result_id
graph_type
graph_json
edit_rationale
status
hash
```

だけで開始できます。

## 3.7 Interpretation Annotation

これも独立Resourceにしなくてよい可能性があります。

初期段階ではResultまたは比較結果に対する注記として保持します。

```text
annotation_id
project_id
target_result_ids
statement
rationale
assumptions
limitations
```

レビュー、承認、独立Version管理が必要になってからInterpretation / Claim Resourceへ昇格させます。

---

# 4. 初期構成から外すもの

| 現行概念 | 初期表現 |
|---|---|
| Research Context | ProjectまたはExecutionのJSON snapshot |
| Experiment | `batch_key`＋objective＋rationale |
| Analysis Definition Version | Executionの`analysis_spec_json`＋hash |
| Execution Plan | Executionのimmutable snapshot |
| Causal Graph | Graph Versionだけで開始 |
| Interpretation / Claim | Result Annotation |
| Lineage Relation | 明示FKと入力参照から導出 |
| Comparison | 保存しないQuery Projection |
| Stage Execution | operationが単段なら不要 |
| Stage Attempt |非同期retryを実装する段階で追加 |
| Research Context Relation | 初期対象外 |
| Review | 初期対象外 |

この構成なら、正本は概ね以下です。

```text
Project
Dataset Version
Execution
Result
Artifact
Graph Version
Annotation
```

さらにAnnotationを後回しにするなら6つです。

---

# 5. 画面も4つ程度まで削れる

## 画面1：Project Workspace

Project Overview、Research Context、Dataset管理を統合します。

表示・操作：

- Project名、目的、メモ
- Dataset upload
- Dataset Version一覧
- 最近の分析
- 新規探索／推論の開始

Research Context専用画面は作りません。

---

## 画面2：Discovery Workspace

以下を一つの画面に統合します。

- Discovery Setup
- Algorithm batch
- Parameter grid
- Execution状態
- Discovery Comparison
- Graph選択
- 簡易Graph編集
- Graph Version確定

```text
左: 入力Datasetと設定
中央: Graph比較
右: 差分・警告・採用操作
```

Discovery Setup、Comparison、Graph Workbenchを3画面に分ける必要はありません。

---

## 画面3：Inference Workspace

以下を統合します。

- Causal Design
- Identification / Preflight
- Estimator実行
- Inference Result
- Estimator Comparison

```text
上部: treatment / outcome / estimand / adjustment set
中部: preflight結果
下部: 推定器ごとの結果・diagnostics比較
```

Identificationを独立画面にせず、実行前チェックまたは結果パネルとして扱います。

---

## 画面4：Result / Lineage

以下を統合します。

- Result詳細
- Result Comparison
- Lineage Review
- Interpretationメモ
- Export

表示：

```text
何を比較したか
何が同一だったか
何を変更したか
結果がどう変化したか
使用Dataset / Graph / Algorithm / Parameter
選定理由、仮定、限界
```

第三者レビュー専用画面は初期には不要です。同じResult画面をread-onlyで表示すれば足ります。

---

# 6. ナビゲーションの最小案

現在案：

```text
Overview
Research Contexts
Datasets
Experiments
Executions
Graphs
Results / Comparisons
Interpretations / Review
```

これは管理システム的です。

初期案は以下で十分です。

```text
Project
├── Data
├── Discovery
├── Inference
└── Results
```

`Execution`、`Graph Version`、`Artifact`などは内部概念として必要でも、主要ナビゲーションには出しません。

Execution履歴はDiscovery、Inference、Resultsの各画面内で表示します。

---

# 7. それでも残すべき区別

削りすぎてはいけない境界もあります。

## ResultとArtifact

これは分けるべきです。

```text
Result = 効果推定値やGraph構造などの分析上の結果
Artifact = JSON、CSV、PNGなどの物理ファイル
```

## ExecutionとResult

これも分けるべきです。

1つのExecutionから複数ResultやArtifactが生じます。また、技術的失敗と科学的な負の結果を分ける必要があります。

## Dataset Version

使用データの固定はAriadneの価値の中心なので削れません。

## Graph Version

探索結果を選択・編集し、推論へ渡すシナリオが中核であるため、初期から独立識別子が必要です。

---

# 8. 修正後の初期物理構造

```text
Project
  ├── Dataset Version
  ├── Execution
  │    ├── input Dataset Version
  │    ├── input Graph Version optional
  │    ├── context / rationale snapshot
  │    ├── analysis specification snapshot
  │    ├── Result
  │    └── Artifact
  ├── Graph Version
  │    └── source Result
  └── Annotation optional
       └── evidence Result IDs
```

Lineageは当初、汎用`lineage_relation`テーブルを置かず、以下の明示参照から復元します。

```text
Execution.dataset_version_id
Execution.input_graph_version_id
GraphVersion.source_result_id
Result.execution_id
Artifact.execution_id / result_id
Annotation.evidence_result_ids
```

この範囲であれば、問いから成果物への主要な追跡は成立します。

---

# 9. いつ独立Entityへ昇格させるか

次のいずれかが実利用で確認された場合だけ分離します。

- 独立したライフサイクルがある
- 単独で検索したい
- 複数箇所から再利用する
- N:M関係を管理する
- Version差分が重要
- review / approvalがある
- 独立した権限制御がある
- 独立URLで共有する

例えばResearch Contextについて、

- 多数のExecutionから共有される
- 単独でレビューされる
- Question単位で検索する
- Version差分を追いたい

という利用実績が出た場合、独立Resourceへ昇格させます。

---

# 10. 評価

作成した成果物は、名前を正確に付けるなら次です。

```text
現状:
初期プロダクトの最小構成

ではなく

修正後の位置付け:
Ariadneのターゲット意味モデルと将来基本設計
```

初期価値検証用としては、次まで縮約すべきです。

| 項目 | 現在案 | 縮約案 |
|---|---:|---:|
| 論理概念 | 約13 | 維持してもよい |
| 初期正本Entity | 10以上になり得る | 6〜7 |
| 主要ナビゲーション | 8 | 4 |
| 個別画面候補 | 約12 | 4 |
| 独立レビュー機能 | あり | 後回し |
| Research Context管理 | 独立画面・Version | snapshot |
| Experiment管理 | 独立Workspace | batch＋rationale |
| Analysis Definition管理 | 独立Resource | Execution snapshot |
| Lineage | 汎用Relation | 明示FKから導出 |

したがって、指摘どおりです。**現在案は意味論を守ろうとして、再び物理・UI構造を膨らませています。初期実装は6〜7の正本Entityと4画面程度に落とせます。**


---

## User — 2026-08-05T03:29:23Z

現在案はむしろ、「将来構想」に回すとして、縮約案をもとに再度4つの業務要件ドキュメントを出力して。

## Assistant

現行4文書は将来構想として保持し、別ディレクトリに縮約版を新規作成します。正本Entityは6〜7、主要画面は4、Golden Pathは1本に限定します。

## Assistant

縮約版では、Research Context・Experiment・Analysis Definitionを独立Resourceにせず、Executionの不変snapshotへ統合します。ComparisonとLineageも正本Entityではなく、既存参照から生成する表示モデルにします。

## Assistant

4文書を作成済みです。現在、相互整合性を確認し、要件・Entity・画面の数が縮約方針から再膨張していないかを最終チェックしています。

## Assistant

縮約案を基に、4文書を新規作成しました。既存案は変更せず、**将来構想版として保持**しています。設計方針は、引継ぎサマリーの「概念として必要であることと、独立Entity・テーブル・必須入力であることを分離する」という原則に基づいています。

## 成果物

- `ariadne_minimum_business_requirements_20260805.zip`
- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`

## 縮約内容

### 正本Entity：7つ

1. Project
2. Dataset Version
3. Execution
4. Result
5. Artifact
6. Graph Version
7. Annotation

以下は独立Entityにしていません。

- Research Context
- Experiment
- Analysis Definition
- Execution Plan
- Comparison
- Lineage Relation
- Dataset親Resource
- Causal Graph親Resource
- Claim
- Stage Execution / Stage Attempt

Research Context、実験目的、選定理由、分析仕様、Causal Designは、Executionの不変snapshotとして保持します。

### 主要画面：4つ

1. Project / Data Workspace
2. Discovery Workspace
3. Inference Workspace
4. Results / Lineage Workspace

EntityごとのCRUD画面ではなく、分析者の作業単位で統合しています。

### 初期Golden Path

```text
Dataset Version登録
→ 複数条件で因果探索
→ Graph比較・選定
→ Graph Version固定
→ 複数EstimatorでATE/ATT推定
→ Result・Diagnostics比較
→ 判断理由・仮定・限界の記録
→ Lineage確認
```

### 将来構想へ移したもの

- Research Contextの独立Version管理
- Experiment Workspace
- Analysis Definition Resource
- Claim / Interpretationの正式管理
- Comparisonの保存・共有
- 汎用Lineage Relation
- Question Tree
- 承認ワークフロー
- 詳細RBAC・Audit
- Stage / Attempt / Lease / Heartbeat
- 複数Artifact Store
- 高度な因果推論方式

ComparisonとLineageは、初期版では既存参照から生成するQuery Modelとして定義しています。

---

## User — 2026-08-05T04:18:22Z

レビュー結果である。レビュー指摘事項を受け、ドキュメントを修正せよ。

添付ファイル:

- `review_22.md`
- `review_21.md`
- `review_10.md`
- `review_00.md`

## Assistant

レビュー指摘を4文書へ横断反映します。特に、自己完結性、見出し階層、ER・FK定義、導出ロジック、各コンポーネント責務、画面遷移DTOを修正対象としています。

## Assistant

レビュー指摘を反映し、4文書を改訂しました。元ファイルは変更せず、`rev1`として別ディレクトリに出力しています。

## 改訂成果物

- `ariadne_minimum_business_requirements_20260805_rev1.zip`
- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`

## 主な修正

### 00 プロダクトコンセプトメモ

- 「既存設計」など、初見の読者が理解できない表現を削除
- 文書タイトルを「初期価値検証版」へ変更
- `Question Treeを実装しない`という否定的な見出しを廃止
- Research Contextについて、以下の方針へ変更
  - 初期版ではProjectメモまたはExecution snapshotとしてフラットに保持
  - 将来独立管理する場合も、フラットなContextと任意relationを正本とする
  - Treeはrelationから生成するProjectionとする

レビュー指摘に対応しています。

### 10 要件定義

- 前身コードや現在の実装を知らなくても理解できる、自己完結したAlgorithm要件へ変更
- PC、GES、LiNGAM、NOTEARS、Difference in means、OLS、IPW、AIPW、g-computationについて、初期対応優先度と位置付けを定義
- 資産流用や実装移行方針は、要件定義ではなく別のコーディング計画で扱うと明記
- CLI要件を次の粒度に修正
  - CLIとWeb/APIは独立した実行粒度を持つ
  - 識別用IDを共有しない
  - 物理実装上、CLIはWeb/APIの`execution_id`を生成しない

レビュー指摘に対応しています。

### 21 論理データ設計

- Mermaid形式のER図を追加
- 全関係についてCardinality一覧を追加
- 全7 Entityについて、属性を以下の表形式へ変更
  - PK
  - FK
  - データ型
  - NOT NULL
  - その他制約
  - 説明
- FKの参照・削除方針を追加
- `非Entityのデータモデル`章を新設
- 以下の生成・導出ロジックを記載
  - Execution Snapshot
  - Batch View
  - Comparison Projection
  - Lineage View
- 状態モデルの対象を明確化
  - Executionの技術的status
  - Graph Versionのstatus
  - ResultのScientific Status
- Annotationのpolymorphicな`target_id`を廃止し、明示FKへ変更
  - `target_result_id`
  - `target_graph_version_id`
  - どちらか一方のみ設定するCHECK制約

レビュー指摘に対応しています。

### 22 プロダクト基本設計

- 全文書の見出し階層を統一
- 各設計対象について、以下を表形式で追加
  - 存在目的
  - 主な責務
  - 主な対象外
- 非同期Execution Workerについて、存在理由と責務を明記
  - 長時間処理のWeb requestからの分離
  - Executionのclaim
  - 入力解決
  - Scientific Core呼出し
  - Result / Artifact保存
  - status更新
  - 技術例外処理
- 画面遷移とDTO設計を追加
- DTOを次の4分類に整理
  - Navigation Context DTO
  - Command DTO
  - Query / Response DTO
  - Scientific Core DTO
- 画面間遷移ごとに、引渡しDTOと受信画面の処理を定義
- 主要DTOの属性を具体化
  - `DiscoveryStartContextDTO`
  - `InferenceStartContextDTO`
  - `ResultSelectionContextDTO`
  - `RerunStartContextDTO`
  - `CreateExecutionBatchRequestDTO`
  - `ComparisonViewDTO`
  - `LineageViewDTO`等
- Entity object全体を画面間で渡さず、識別子を渡してAPIから正本を再取得する方針を明記

レビュー指摘に対応しています。

---

## User — 2026-08-05T04:27:52Z

ちなみにDTOの設計まで基本設計でやるっけ？

## Assistant

一般論では、**DTOのフィールド単位設計までを「基本設計」に含めるのはやや詳細すぎます**。

## 基本設計で決める範囲

基本設計では、画面・機能間で**何を引き渡す必要があるか**を論理的に定義すれば十分です。

例：

- Discovery画面からInference画面へ、採用したGraph Versionを引き渡す
- Result比較画面へ、比較対象Resultの集合を引き渡す
- 再実行時は、元Executionの分析条件を初期値として利用する
- 画面遷移ではEntity全体ではなく識別子を渡し、正本をAPIから再取得する

この程度は基本設計に必要です。画面間の責務や依存関係を確定するためです。

## 詳細設計へ回す範囲

以下は通常、詳細設計またはAPI／インターフェース設計です。

```text
DiscoveryStartContextDTO
- project_id: UUID
- dataset_version_id: UUID
- source_execution_id: UUID | null
- initial_algorithms: string[]
```

具体的には次です。

- DTOクラス名
- 全フィールド
- データ型
-必須／任意
- enum値
- validation
- serialization形式
- API request／response schema
- エラー形式
- バージョニング方法

これらは実装方式に近く、基本設計で固定すると変更コストが高くなります。

## 例外

次の場合は、基本設計段階でDTO相当の契約を詳細化することがあります。

- 外部システムとの連携仕様
- 複数チーム間のAPI契約
- APIファースト／契約ファースト開発
- フロントエンドとバックエンドを並行開発する
- 後方互換性が重要な公開API

ただし、その場合も通常は「基本設計書」に埋め込むより、**API仕様書やインターフェース設計書として分離**します。

## Ariadne文書への適用

今回の`22_プロダクト基本設計`では、レビュー指摘に対して私が過剰に具体化しました。

基本設計に残すべきなのは、例えば以下です。

| 遷移 | 引き渡す論理情報 |
|---|---|
| Project → Discovery | Project、Dataset Version |
| Discovery → Inference | Project、Dataset Version、採用Graph Version |
| Discovery／Inference → Results | Result ID群 |
| Results → 再実行 | 元Execution、変更対象条件 |
| Result → Lineage | Resultを起点とする来歴参照 |

そして、次は別文書へ移すべきです。

- DTO名
- DTOフィールド一覧
- JSON schema
- Request／Response定義
- 型・制約
- エラーコード

## 推奨する文書構成

```text
22_プロダクト基本設計
- コンポーネント責務
- 画面構成
- 画面遷移
- 論理的な引渡し情報
- APIの役割と境界

23_API・インターフェース設計
- Endpoint
- Request / Response
- DTO
- validation
- error model

30_詳細設計
- クラス構成
- repository / service
- 処理シーケンス
- transaction
- 例外処理
```

したがって、レビュー指摘の「画面間の引き渡し項目を定義する」は妥当ですが、**DTOクラスとフィールドまで基本設計へ入れたのは一段深すぎました**。論理引渡し情報だけ残し、DTO詳細は別文書へ移すのが適切です。

---

## User — 2026-08-05T04:32:11Z

推奨する文書構成
でもう一回出力してもらえる？

## Assistant

`22_プロダクト基本設計`からDTO・API契約・クラス詳細を分離し、`23_API・インターフェース設計`と`30_詳細設計`を追加した6文書構成へ再編します。既存4文書の内容も、参照先と粒度が整合するよう更新します。

## Assistant

基本設計には「論理的な引渡し情報」までを残し、DTO名・型・Endpoint・validationは`23`へ移します。package、class、repository、transaction、例外処理、実行sequenceは`30`へ分離します。

## Assistant

推奨した文書粒度に再編し、**Revision 2**として出力しました。

- `22`: システム境界、画面、論理的な引渡し情報
- `23`: Endpoint、DTO、validation、error model
- `30`: package、class、repository、transaction、例外処理、実行sequence

レビューで求められたER・FK定義、コンポーネント責務、画面間の情報引渡しは維持しつつ、基本設計から実装寄りの内容を分離しています。

## 成果物

- `ariadne_minimum_business_requirements_20260805_rev2.zip`
- `README.md`
- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`
- `23_API・インターフェース設計.md`
- `30_詳細設計.md`

## 分離した内容

### `22_プロダクト基本設計`

残したもの：

- コンポーネントの存在目的と責務
- システム構成
- 4 Workspace
- 画面構成
- 画面遷移
- 画面間で引き渡す論理情報
- Worker、Scientific Core、CLIの基本責務
- E2E処理フロー

削除・移動したもの：

- DTOクラス名
- JSON field定義
- API Endpoint
- package構成
- repository
- transaction
- 例外class

### `23_API・インターフェース設計`

- Navigation Context
- Web API Endpoint
- Request / Response DTO
- operation別Analysis Spec
- Scientific Core入出力契約
- CLI Manifest
- validation
- Idempotency
- HTTP statusとerror code
- Contract versioning

### `30_詳細設計`

- package構成
- Domain Entity / Value Object
- Repository Port
- Unit of Work
- Application Service
- Worker claim
- transaction境界
- Artifact保存失敗時の補償
- Domain / Infrastructure exception
- Scientific Core Adapter
- CLI exit code
- テスト構成
- logging / observability

なお、`30`は実装可能性を確認するための初期詳細設計です。前身コードからの資産流用、旧DBからのmigration、互換APIは別の**実装移行計画**として分離しています。

---

## User — 2026-08-05T04:48:15Z

概ね問題ないかな？
後は、「前身コードからの資産流用、旧DBからのmigration、互換APIは別の実装移行計画として分離しています。」これの出力お願い

## Assistant

`40_実装移行計画`を追加し、前身コードの再利用判定、旧DBからの移行方針、互換API方針、段階的切替、ロールバック、完了判定まで整理します。併せてREADMEの文書体系を更新します。

## Assistant

移行計画は「全面互換を前提にしない」方針で作成します。実稼働実績がない前提では、新スキーマを別系統で構築し、必要なデータだけを明示的にImportする方が、インプレースDB変換より安全で低コストです。

## Assistant

## 評価

概ね問題ありません。現状の文書セットは、以下の役割分担が明確になっています。

- `00`：プロダクトの目的と思想
- `10`：業務・機能・非機能要件
- `21`：論理Entityと関係
- `22`：システム・画面・コンポーネントの基本構造
- `23`：API、DTO、外部・内部インターフェース契約
- `30`：クラス、Repository、Transaction、Worker等の実装設計
- `40`：前身コードからの移行戦略

ただし、現時点で未確定なのは設計漏れではなく、実装開始後に判定する次のDecision Gateです。

1. 各Scientific Algorithmを本当に流用できるか
2. 旧DBから移すべきデータが実在するか
3. 維持すべき前身API clientが実在するか
4. Legacy Control Planeを停止できる条件が整ったか

これらを先に固定すると、未確認要件を再び設計へ取り込むことになります。

## 実装移行計画

Revision 3として、`40_実装移行計画.md`を追加しました。

- `ariadne_minimum_business_requirements_20260805_rev3.zip`
- `40_実装移行計画.md`
- `README.md`

## `40`の主要方針

### コード移行

```text
Scientific Core
  → 選択的に流用

Product Domain / DB / API / Worker / Web App
  → 新規構築

Legacy Control Plane
  → 凍結後、段階的に廃止
```

前身コードについて、資産ごとに以下を判定しています。

- `REUSE`
- `ADAPT`
- `CHARACTERIZE`
- `DEFER`
- `RETIRE`

### DB移行

3段階に分類しました。

| Level | 方針 |
|---|---|
| M0 | 新DBを空で開始。旧DBはread-only archive |
| M1 | Dataset、Graph等の必要資産だけ選択Import |
| M2 | 全履歴移行。初期対象外 |

現状の推奨は**M0 Clean Start**です。

### API互換性

| Level | 方針 |
|---|---|
| C0 | 互換なし。clientを新APIへ変更 |
| C1 | 主要GETのみ互換 |
| C2 | Commandを新APIへ変換 |
| C3 | 完全互換 |

現状の既定は**C0 No Compatibility**です。実在するclientが確認されたEndpointだけ、C1またはC2へ引き上げます。

### 実装Phase

```text
Phase 0  Baseline固定
Phase 1  Scientific Core Adapter
Phase 2  新Product Domain・DB
Phase 3  新API・Worker
Phase 4  4 Workspace Web App
Phase 5  必要なImport・互換API
Phase 6  Cutover・Legacy廃止
```

### コーディングエージェント対応

作業を`WP-00`〜`WP-10`へ分割し、各作業で以下を指定する方針を記載しました。

- 参照可能ファイル
- 変更可能範囲
- 変更禁止範囲
- 対象要件
- 受入れテスト
- 再利用可能module

これにより、「リポジトリ全体を読み、全面改修する」というトークン消費の大きい作業を避けます。

---

## User — 2026-08-05T04:56:38Z

DBに入っているデータは基本全部破棄して問題ない。
後方互換性を意識して、新システムの整合性が崩さないように移行計画を立ててほしい。

## Assistant

DBデータは全破棄可能、API互換性は「必要な範囲だけ維持し、新設計の整合性を優先」という前提へ変更します。`40_実装移行計画`を中心に、互換レイヤを新ドメインへ侵入させない構造へ改訂します。

## Assistant

後方互換性は「旧仕様を新ドメインへ持ち込む」ことではなく、外縁の互換Adapterで吸収します。旧DBデータ移行は廃止し、新DBのClean Startと契約互換だけに移行計画を集中させます。

## Assistant

旧DBデータを全破棄する前提に変更し、後方互換性を**新システム外縁のCompatibility Adapterだけで提供する**移行計画へ改訂しました。

## 成果物

- `ariadne_minimum_business_requirements_20260805_rev4.zip`
- `40_実装移行計画.md`
- `README.md`

## 主な変更

### DB移行

以下をすべて廃止しました。

- 旧DB recordのImport
- Legacy IDと新IDのmapping
- Execution・Result・Graph履歴の移行
- Curated Import
- reverse migration
- 新旧DBへのdual-write

新DBは独立したAlembic baselineから空で構築します。切替後、新システムから旧DBへの接続は禁止し、確認期間後に旧DBを破棄します。

### 後方互換性

後方互換性の対象を、実在する以下のclient契約に限定しました。

- Web API
- CLI command
- config形式
- Manifest形式

互換処理は次の境界だけに置きます。

```text
Legacy Client
→ Compatibility Adapter
→ New Application Service
→ New Product Domain / DB
```

Compatibility Adapterの都合で、新Domainや新DBへ以下を追加することは禁止しています。

- `legacy_id`
- Legacy status
- Legacy Resource
- Legacy固有FK
- Legacy Configuration / Experiment Entity

### 互換レベル

| Level | 内容 |
|---|---|
| C0 | 互換なし |
| C1 | path・command aliasと移行案内 |
| C2 | Request / Response変換 |
| C3 | side effect等を含む完全互換 |

既定は`C0`または`C1`です。実在clientの変更が困難な契約だけ、期限付きで`C2`とします。`C3`は原則採用しません。

### 整合性保護

以下を明示的に禁止しました。

- 意味不明なLegacy parameterの黙示的無視
- Graph typeの推測変換
- `NOT_IDENTIFIED`等の科学的状態の隠蔽
- Compatibility Adapter内のbusiness logic・Repository
- Compatibility障害を理由としたProduct Core全体のrollback

新APIが正常で互換APIだけに問題がある場合は、互換経路だけを停止します。

### 最終状態

```text
新Product Domain / DB
  = 唯一の正本

Scientific Adapter
  = 前身科学計算資産の限定的な再利用

Compatibility Adapter
  = 期限付きの外縁変換層

Legacy API / Worker / Frontend / DB
  = 停止・廃止
```

互換Adapterを削除しても新システムが完全に動作することを、移行完了条件に含めています。

---

## User — 2026-08-05T05:35:03Z

本チャットの討議内容を、要約や編集をせずmarkdownファイルとして出力せよ。
但し、添付ファイルは名称のみ保持する形で問題ない。
