# Single Execution Coding Agent Prompt

## 入力identity: 
GATE_ID=G01
TRIAL_NO=01

0. 対象エンハンスは `docs/wiki/develop_memo/_work/20260820_ENH-E8_analysis_stage_content_redesign/README.md` である 
1. normative implementation semanticsとして `10_enhance_instruction/G01/06_Ariadne_ENH-E8_G01_implementation_instruction.md` のみを読む。
2. 07、background、previous reportを使って06の不足を補完しない。
3. source code/testはimplementation fact確認のために調査してよい。
4. G01 scopeだけを実装し、focused self-checkを実行する。
5. implementation evidenceを `20_implementation_reports/G01/Trial<TRIAL_NO>/` に記録する。
6. candidate finalization前にGate PASSを宣言しない。
7. semantic ambiguityがある場合は推測せずcontract ambiguityとして停止する。
