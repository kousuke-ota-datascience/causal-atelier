# {{GATE_ID}} Trial {{TRIAL_NO}} Implementation Evidence — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST for one Trial evidence namespace.

このdirectoryは1 Trialのcandidate-generation transactionを保存する。

- `packages/` — WORK_PACKAGE modeのexecution status / checkpoint evidence。
- `*_implementation_completion_report.md` — Candidate AssemblyとFixed Trial Candidate identity。

Trial evidenceは、formal PASS / FAIL / BLOCKED後もimmutable historical evidenceとして保持する。Fixed Candidateを作り直す場合はCompletion Report内でidentityを明確にし、failed Trial evidenceを上書きしない。
