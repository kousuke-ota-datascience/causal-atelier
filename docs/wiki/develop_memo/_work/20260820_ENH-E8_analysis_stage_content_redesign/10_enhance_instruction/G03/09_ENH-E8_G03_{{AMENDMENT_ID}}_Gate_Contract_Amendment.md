# ENH-E8 G03 Gate Contract Amendment

- Document class: Gate Contract Amendment
- Status: `TEMPLATE`
- Gate: `G03`
- Amendment ID: `{{AMENDMENT_ID}}`

## 目的

`RETROSPECTIVE_FROZEN` としたG03の06 / 07について、semantic claim、scope、Acceptance Criteriaそのものに欠陥またはHuman-approved changeがあり、元contractのまま今後のverification / regression protectionへ使用できない場合に使用する。

## 必須記録

- amendment理由
- affected 06/07 section
- old contract semantics
- new contract semantics
- ENH-E8 G01/G02 protected contractへのimpact
- historical bugfix evidenceへのimpact
- Trial / candidate handling
- Human approval
- required re-baseline artifacts

`08` remediationでcontract defectを隠して修正してはならない。

G03がretrospective reconstructionであること自体を理由に、過去のworkflow実行事実を遡及的に書き換えてはならない。
