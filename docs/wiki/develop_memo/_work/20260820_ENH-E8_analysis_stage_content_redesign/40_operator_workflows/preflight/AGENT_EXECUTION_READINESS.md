# ENH-E8 Agent Execution Readiness

Current documentation state: `APPROVED/FROZEN`

## Common document freeze

- [x] baseline commit `386521d18e9c5cc4d42fb99c97c212430908afc3` をbaseline authorityとして固定
- [x] Humanが00 planning/design basisをAPPROVED
- [x] G01/G02 06/07をFROZEN
- [x] G02 P00/P01/P02/P03をFROZEN
- [x] Browser E2E canonical command/environmentを07でFROZEN
- [x] revised design snapshotをAPPROVED composite snapshotとしてFROZEN

## G01 execution-time preflight

- [ ] actual implementation worktree/branch identityを確認
- [ ] worktreeがCoding Agent開始に適したcontrolled stateである
- [ ] required local tooling / Docker / Compose / Playwright image build pathが利用可能
- [ ] frozen G01 contractとtarget repository SHAをAgent起動時に再確認

**G01 routing:** document/contract上は実行可能。上記execution-time preflightをHuman/operatorが実repository上で確認してからCoding Agentを起動する。

## G02 dependency / execution-time preflight

- [ ] canonical G01 999 decision = PASS
- [ ] G01 PASS candidateを含むaccepted baseline/worktree identityを確認
- [ ] required local tooling / Docker / Compose / Browser E2E pathが利用可能
- [ ] frozen G02 package contractとtarget repository SHAをAgent起動時に再確認

**G02 routing:** contractsはFROZENだが、canonical G01 `999 PASS` が記録されるまでdependency-blocked。
