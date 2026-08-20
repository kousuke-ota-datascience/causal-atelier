# Work Package Candidate Assembly Agent Prompt

入力identity: `GATE_ID=G02`, `TRIAL_NO`

1. required packageのcompletion evidenceを確認する。
2. packageを統合したrepository stateを確認し、unresolved conflict / blockerを解消または報告する。
3. Gate-level focused/protected regressionを実行する。
4. test implementationをacceptanceに合わせて恣意的に弱めない。
5. 1つのcommit SHAをFixed Trial Candidateとして固定する。
6. `20_implementation_reports/G02/Trial<TRIAL_NO>/` にImplementation Completion Reportを作成する。
7. `READY_FOR_TEST` はIndependent Verificationへ渡せる状態でありGate PASSではない。
