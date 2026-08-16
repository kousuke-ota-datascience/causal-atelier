## 1. PRE-02

> docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/_work
これは除外したい以下の対応を願う。

`````
• _work 全体を検査対象から除外するなら、preflight の走査条件に追加します。対象は次のスクリプトです。

  docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py:38

  # Provenance and _work are not execution contracts.
  if rel.parts[:2] == ("00_enhance_background", "provenance") or rel.parts[:1] == ("_work",):
      continue

  現状の条件を上記に置換すればよいです。
`````

## 2. PRE-07 Pxx self-contained/isolation

以下のエラーで進まなくなった。対応せよ

`````
• 結論: BLOCKED_PRECHECK です。

  PRE-02 は解消済みですが、次が未解消です。

  - PRE-07 Pxx self-contained/isolation: 06_G01_P01_project_navigation_authority.md

  プロンプト規定により、P01 の契約書閲覧・実装には進んでいません。

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


› PRE-07 Pxx self-contained/isolation: 06_G01_P01_project_navigation_authority.md
  具体的に教えて


• PRE-07 の判定ロジックと、P01 文書内で実際に引っかかっている記述を確認します。これは実装には進まず、ブロック理由の説明だけを行います。

• Explored
  └ Read check_agent_execution_readiness.py
    Search PRE-07|self-contained|isolation|forbidden|06|07|P00|other Pxx|Gate in check_agent_execution_readiness.py
    Search self-containment|must not read|gate 06|gate 07|p00|other pxx in 06_G01_P01_project_navigation_authority.md
    Read 06_G01_P01_project_navigation_authority.md

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 結論: P01 の文書自体は、情報分離を明示しています。PRE-07 は検査スクリプトの文字列照合バグにより失敗しています。

  事実:

  - P01 には **Self-containment:** MUST がある（4行目）。
  - P01 には「parent 06 / 07 / P00 / other Pxx…読まない」（22行目）および「Gate 06 / Gate 07 / P00 / other Pxx…読まない」（88行目）がある。

  しかし、検査コードは次を要求しています。

  "must not read Gate 06" in pxx_text.lower()

  pxx_text.lower() は全小文字化されるため、右辺の Gate 06（大文字G）を含むことは構造上あり得ません。加えて P01 は日本語で「読まない」と書いており、英語の完全一致文字列もありません。

  つまり、P01 の契約不足ではなく PRE-07 の実装不備です。

  修正の最小案は、docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py:68 の比較値を小文字に揃える
  ことです。

  "must not read gate 06" in pxx_text.lower()

  ただし、現行 P01 は英語の must not read ... ではなく日本語なので、これだけでは PASS しません。実態に適合させるには、例えば明示的な日本語文言も許容します。

  pxx_ok = (
      "Self-containment:** MUST" in pxx_text
      and (
          "must not read gate 06" in pxx_text.lower()
          or "Gate 06 / Gate 07 / P00 / other Pxx / 00 / 20 / 30をpackage specification補完目的で読まない。" in pxx_text
      )
  )

  よりよい設計は、自然言語の完全一致ではなく、Pxx の必須メタデータ（例: **Information isolation:** MUST）を固定して検査することです。現状の文字列一致は、表現や言語の変更に壊れやすいです。

`````