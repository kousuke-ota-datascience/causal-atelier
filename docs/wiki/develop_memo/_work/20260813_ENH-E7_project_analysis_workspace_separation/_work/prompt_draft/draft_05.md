> docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/_work
これは除外したいんだが、どうすればいいか？

-----

以下のように、python3を指定していないか？

`````
## 1. Preflight first

Run:

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . --gate <GATE_ID> --package <PACKAGE_ID> --trial <TRIAL_NO>
```
`````

-----
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=G01
- PACKAGE_ID=P01
- TRIAL_NO=01

プロンプトの際の基本言語は日本語とする

-----

```
• 結論: BLOCKED_PRECHECK です。指定された preflight を実行しましたが、実行環境に python コマンドが存在しません。

  /bin/bash: line 1: python: command not found

  したがって、プロンプトの規定に従い P01 の契約書・実装には進んでいません。

  前提: preflight は指定どおり python で実行する必要があります。
  対応案: python を利用可能にした後、同じ G01 / P01 / Trial 01 で再実行してください。

```

本環境にインストールされているのはpython3であるため、python3を基本としたコマンドに書き換えること。
これは全ファイルを通して見直すこと。

-----
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=G01
- PACKAGE_ID=P01
- TRIAL_NO=01

プロンプトの際の基本言語は日本語とする
