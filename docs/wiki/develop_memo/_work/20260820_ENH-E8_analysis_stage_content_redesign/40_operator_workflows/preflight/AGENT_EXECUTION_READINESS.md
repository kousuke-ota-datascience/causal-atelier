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

- [x] actual implementation worktree/branch identityを確認

```
commit 7f846fd305b767ac93224a27c980e5dec8499729 (HEAD -> feature/ariadne_mvp_e8, causal-atelier/prototype/ariadne_mvp, prototype/ariadne_mvp)
Author: kousuke-ota-datascience <kousuke.ota.datascience@gmail.com>
Date:   Thu Aug 20 21:09:15 2026 +0000

    add 20260820_docs
```

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
