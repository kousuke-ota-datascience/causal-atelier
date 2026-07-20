title: データモデル定義書指摘事項

# 0. overview 

本文書は、以下のドキュメントに対する指摘事項である。

- /loc0/bigbrother/repositories/causal-atelier/_work/20260718_requirements_of_web_service/
    - 02_data_model_definition_v1.1.md

必要に応じて、バージョンをインクリメントして新しい版を作成、データモデル定義書を修正せよ

以下、簡略化のため修正対象の文書を[v1.1]と呼ぶこととする


# 1. 全般

## 1.1. 見出しの構成

文書名として、見出し1 '#' で[causal-atelier Webサービス データモデル定義書]としているが、
この文書がデータモデルであることは自明である。
見出しは章立ての構成に使用すること

また、混乱を避けるため見出しレイヤを以下のように定義する

- #: 章 / chapter / チャプター
- ##: 節 / section / セクション
- ###: 項 / subsection / サブセクション
- ####: 目 / subsubsection / サブサブセクション
- （以降はこの段階では定義していない。必要に応じて定義すること）


## 1.2. 記載内容の量/密度

例えば、以下の用に記載されているが記載内容が足りず人間が読んでも理解不能になっている
例示した箇所以外にも、多数該当する部分があるので全般修正せよ。
このままだと意味が通らない


例(1)
```
## 3. 設計原則

### 3.1. 不変Resource

次は確定またはpublish後に内容を更新しない。

- Dataset Version / Dataset Table Version
- Published Configuration Version
- Published Causal Graph Version
- Pipeline Definition Version
- Execution Plan
- Artifact content
- Manifest
- Run Event
- Stage Attempt履歴
- Result projectionが参照する入力Version snapshot
```

例(2)
```
## 4. 集約

1. Identity / Authorization
2. Project
3. Data Catalog / Dataset Source
4. Configuration Catalog / Feature Semantics / Causal Design
5. Experiment
6. Pipeline Definition
7. Run Execution / Input Preparation
8. Artifact / Manifest / Lineage
9. Discovery Result Projection
10. Saved Causal Graph
11. Inference Result Projection
12. Validation / Audit / Outbox
13. Visualization（既存互換）
```

例(3)
```
# 7. Data Catalog変更

## 7.1. `dataset`

既存schemaを維持する。

`dataset_kind`:

- RAW
- INTERIM
- PROCESSED
- DISCOVERY_FEATURE
- INFERENCE_FEATURE

MVP WebはPROCESSED、DISCOVERY_FEATURE、INFERENCE_FEATUREを主に使用するが、RAW/INTERIMを削除しない。

## 7.2. `dataset_version`

既存columnとsource typeを維持する。

`source_type`:

- UPLOAD
- OBJECT_REFERENCE
- ETL
- FEATURE_BUILD
- IMPORT
- EXTERNAL_REFERENCE（MVP後）

```

# 2. 文書情報を表現するチャプター

## 2.1. 文書情報チャプターの構成

データモデル定義の中身に関係しないものは、 # 0. の文書情報に記載すること
'# 0. ' のタイトルは、文書のメタ情報 / 文書そのものの情報 / OVERVIEW であることがわかるようにする

例
```
documet title: causal-atelier Webサービス データモデル定義書

# 0. 文書情報

## 0.1. 改定履歴

## 0.1. 本文章の目的

## 0.1. 本版の変更原則

```

## 2.2. 記載内容

v1.1内の冒頭で、以下のように記載があったがリストアップされている情報の粒度/レイヤ/対象がバラバラである。
文章版と基準リポジトリを同列に扱うのは記載する情報の粒度の観点から違和感がある。
文書に関する情報飲みを  # 0. に集約し、リポジトリや対象DBMS等は他のチャプターに記載すること


# 3. v1.0 への依存の解決

記載内容が、v1.0（02_data_model_definition.md）に依存しているように見える

 例えば、以下の章が該当する。
 ```
 # 6. 既存集約の維持

次のtableは原版v1.0および現行SQLAlchemy modelを維持する。本版に追加記載がないcolumn・constraintを削除しない。

```
v1.0を維持する、ではなく、具体的にどのような仕様にするかを記載すること

言い換えるならば、読者がこのv1.1 **のみ** を参照し、データモデル定義を理解できるように修正すること

ただし、[## 2. v1.0からの変更サマリー]に記載されている内容は決して無駄ではない。
[# 0.] のセクション/サブセクションに記載すれば良いので、章立てを変更すること


# 4. 章の構成

'# 5. 概念ER' のあとに、 '# 6. 既存集約の維持' がいきなり来ている。
テーブル間の集約の話だろうがいきなり集約の話をされても読者は頭に入ってこない。

章立てとして、以下の順序にすること。

- ER図 / エンティティ一覧
- 各エンティティ詳細
- エンティティ間の関係
    - 集約の情報
    - [etc...]



# 5. 記載内容

例えば、以下の章について

```
## 3. 設計原則

### 3.1. 不変Resource

次は確定またはpublish後に内容を更新しない。
```

このように記載されても、何を対象としている話なのかが伝わりづらい。
おそらくは対象エンティティのレコードに対して、createはできてもdeleteやupdateができないことを表しているのだろうが、
それならばcrudのほうが素直である。

