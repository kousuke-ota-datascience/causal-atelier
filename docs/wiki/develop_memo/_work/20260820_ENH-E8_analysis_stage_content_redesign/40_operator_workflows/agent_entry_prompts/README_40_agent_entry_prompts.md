# 40 — Agent Entry Prompt

このdirectoryはHuman operatorが各Agentを起動するためのprompt templateを置く。

原則:

- Coding Agentには必要最小限のnormative contractだけを渡す。
- Test Agentにはfrozen `07` とFixed Trial Candidate identityを渡す。
- Agentに不足仕様をworkflow treeから探索させない。
- `PACKAGE_COMPLETE`, `READY_FOR_TEST`, `PASS` を混同しない。
- formal FAIL前にTrial番号を増やさない。
