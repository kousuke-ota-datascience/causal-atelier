# G01 Implementation Evidence — 使用ガイド

G01のCoding execution / Package checkpoint / Candidate Assembly evidenceを保存する。

- Gate: `G01`
- Execution Mode: `WORK_PACKAGE`
- Active planned Trial: `Trial01`
- Package set: `P01, P02, P03`
- Gate acceptance authority: このdirectoryにはない。

Trialごとにimmutableなexecution historyを保持し、formal FAIL後も過去Trial reportを上書きしない。Gate-local detail ledgerは`ENH-E6_G01_implementation_report_detail.md`。
