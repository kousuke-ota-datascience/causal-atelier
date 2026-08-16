# Package Evidence — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST for package evidence creation.

WORK_PACKAGE modeで、各Pxx/Rxxについて次を記録する。

- `*_in_progress.md` — 1 Agent executionの完了 / 中断 / blocker status。
- `*_implementation_checkpoint_report.md` — package-local checkpoint evidence。

各reportはstatus / completed work / remaining work / verification / relevant SHA / next actionを本文に持つ。source / command output / diffは外部evidenceとして参照してよい。

Package evidenceはGate acceptance authorityを持たない。
