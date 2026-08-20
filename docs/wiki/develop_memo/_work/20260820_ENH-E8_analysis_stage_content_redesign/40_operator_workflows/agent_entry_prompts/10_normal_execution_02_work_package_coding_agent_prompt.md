# Work Package Coding Agent Prompt

入力identity: `GATE_ID=G02`, `TRIAL_NO`, `PACKAGE_ID`

1. normative implementation semanticsとしてassigned `06_G02_<PACKAGE_ID>_*.md` **だけ**を読む。
2. Gate 06/07、P00、他Pxx、background、previous reportを使ってassigned contractを拡張・修復しない。
3. source code/testはfactual implementation contextとして調査してよい。
4. assigned packageだけを実装し、focused self-checkを実行する。
5. package status/checkpoint evidenceを `20_implementation_reports/G02/Trial<TRIAL_NO>/packages/` に記録する。
6. `PACKAGE_COMPLETE` はGate PASSではなく、Trial番号も増加させない。
7. semantic不足・ambiguityがある場合は停止し、contract ambiguityとして報告する。
