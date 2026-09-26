# {{GATE_ID}} Implementation Evidence — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST for this Gate evidence namespace.

このdirectoryは1 Gateのunverified implementation ledgerとTrial evidenceを保存する。

- `{{ENHANCE_ID}}_{{GATE_ID}}_implementation_report_detail.md` — Gate全体の累積implementation ledger。
- `TrialNN/` — Trialごとのcandidate-generation evidence。

Rules:

- Package completion / READY_FOR_TESTをGate PASSと表現しない。
- Trialごとのcandidate evidenceを上書きしない。
- report本文にstatus / facts / rationaleを記載し、SHA / source / logはevidence参照として使う。
- final PASS後もhistorical implementation evidenceとして保持する。
