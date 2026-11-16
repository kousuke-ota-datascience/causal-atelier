# 23_40_cli_library


---

## 7. CLI / Library Interface

現行実装のproduct script entry pointは次である。

```text
ariadne-discover
ariadne-estimate
ariadne-identify
ariadne-refute
ariadne-sensitivity
ariadne-api
ariadne-worker
```

scientific CLIの既存境界:

- `ariadne-discover`はstandalone discovery CLIであり、**Web/API Execution IDを作成しない**。
- `ariadne-identify` / `ariadne-refute` / `ariadne-sensitivity`は共通local scientific-stage implementationを利用し、`--config`でYAMLを読み、domain analysis-spec validation後に`ScientificCoreAdapter`を直接呼び出す。
- `ariadne-estimate`もlocal estimation commandとして提供される。
- CLIは実行manifest等のlocal outputを生成するが、browser route / sidebar stateを入力契約にしない。

したがってCurrent contractでは、存在しない次のようなgeneric Resource CLIをcurrent interfaceとして捏造しない。

```text
ariadne project list
ariadne execution submit
ariadne result show
```

将来generic product CLIを追加する場合は別scopeでinterface contractを設計する。Current mandatory contractでは、既存headless scientific CLIおよびPython/backend use caseへ`current_family` / `navigation_stage` / browser routeをrequired inputとして追加しない。

禁止例:

```text
ariadne-identify --navigation-stage identification --config ...
```

`AnalysisFamily` / `ExecutionOperation`等のdomain discriminatorと、UI Navigation Stageを区別する。

## 7.1. ENH-E11別Local CLI/Scientific Port契約

追加Local E11のCLI／Portのversion dispatch、Method/Estimand/Backend capability、typed scientific negative、exit分類は[23_41](23_41_e11_local_cli_scientific_ports.md)をInterface Authorityとする。Result/Graph/ManifestのSchema、privacy、atomic bundle publish/readbackは[23_42](23_42_e11_local_result_manifest_artifact.md)を参照。

E11は旧`ariadne-identify`等の`causal-analysis-spec/2`を再解釈せず、新しいCLI entrypointで明示的に分離する。新Interfaceのコード実装は別工程である。
