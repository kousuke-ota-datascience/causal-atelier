# 20_implementation_reports — ENH-E5

文書区分: Evidence Artifact Guide（実装evidence資料ガイド）

planning時点ではimplementation evidenceは存在しない。架空のcheckpoint SHA、candidate SHA、completion status、implementation observationを事前生成してはならない。

Trial開始時に`{GATE_ID}/Trial{TRIAL_NO}/`を作成し、以下を記録する:
- Work Package GateのPackage status/checkpoint report;
- implementation report detail;
- exact Fixed Trial Candidate SHAを含むimplementation completion report。
