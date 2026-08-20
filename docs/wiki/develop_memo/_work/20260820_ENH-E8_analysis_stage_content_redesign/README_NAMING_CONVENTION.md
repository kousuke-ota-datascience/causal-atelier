# README Naming Convention

## 1. Rule

Enhancement work root / workflow template rootのtop-level READMEだけを無印 `README.md` とする。

nested directoryのlocal READMEは、directory pathから機械的に導出した `PATH_ID` をpostfixとして付与する。

```text
README filename = deterministic function(directory path)
```

```text
root/
  README.md

root/00_enhance_background/
  README_00.md

root/20_implementation_reports/G01/Trial01/
  README_20_G01_Trial01.md

root/40_operator_workflows/agent_entry_prompts/
  README_40_agent_entry_prompts.md
```

## 2. PATH_ID generation

Enhancement/template rootからREADME配置directoryまでのrelative pathを左から処理する。

1. `NN_<semantic_name>` 形式のworkflow namespace directoryは `NN` に短縮する。
2. `G01`, `P01`, `Trial01` 等のruntime identity directoryはそのまま保持する。
3. `agent_entry_prompts`, `preflight` 等の非numbered semantic directoryは名前を保持する。
4. tokenを `_` で連結する。
5. `README_<PATH_ID>.md` とする。

例:

```text
00_enhance_background
  -> 00
  -> README_00.md

20_implementation_reports/G01/Trial01
  -> 20_G01_Trial01
  -> README_20_G01_Trial01.md

40_operator_workflows/agent_entry_prompts
  -> 40_agent_entry_prompts
  -> README_40_agent_entry_prompts.md
```

## 3. Invariants

- root以外に無印 `README.md` を置いてはならない。
- 同一directoryに複数のlocal READMEを置いてはならない。
- 手作業でpostfixを決めてはならない。必ずpath-derived naming functionを使用する。
- rename時はMarkdown links、plain path references、operator prompts、structure/manifest、validator/instantiation toolingを同時更新する。
- target filename collisionが発生した場合は自動上書きせず `BLOCKED_README_NAMING_COLLISION` とする。

## 4. Canonical implementation

canonical naming functionは以下とする。

```text
40_operator_workflows/tools/readme_naming.py
```

Template migration/apply tooling、instantiation tooling、validatorは同一規則を使用し、別々の命名ロジックを持たない。
