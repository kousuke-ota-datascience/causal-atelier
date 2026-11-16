# 23_40_cli_library

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

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
