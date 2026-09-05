# ENH-E8 G03 Gate Contract Amendment

- Document class: Gate Contract Amendment
- Status: `TEMPLATE`
- Gate: `G03`
- Amendment ID: `{{AMENDMENT_ID}}`

## 目的

`RETROSPECTIVE_FROZEN` としたG03の06 / 07について、semantic claim、scope、Acceptance Criteriaそのものに欠陥またはHuman-approved changeがあり、元contractのまま今後のverification / regression protectionへ使用できない場合に使用する。

G03では、agentic enhancement workflowを経由せずCHAT上でsource codeを直接変更したhistorical exceptionが存在する。そのため、source history再監査で06/07のcontract incompletenessが判明した場合も09の対象とする。

## 必須記録

- amendment理由
- affected 06/07 section
- old contract semantics
- new contract semantics
- ENH-E8 G01/G02 protected contractへのimpact
- historical bugfix / CHAT-direct source evidenceへのimpact
- relevant source commit SHA / document baseline SHA
- historical commit labelとeffective ENH-E8 classificationの関係
- known incomplete implementation stateをPASS扱いしていないこと
- Trial / candidate handling
- Human approval
- required re-baseline artifacts

## CHAT-direct history rule

source変更がCHAT上で直接実施され、formal Gate FAIL / active 08 / Coding Agent executionを経ていない場合:

1. 当該source commitをformal Trial remediationへ遡及変換しない。
2. 08にはnon-canonical historical exception recordとして残してよい。
3. source auditによりsemantic claim / Acceptance Criteria不足が判明した場合は09でexplicit amendmentを作成する。
4. historical commit messageのEnhancement ID表記を後付けで改変せずprovenanceとして保持する。
5. Human ownerによるeffective classificationがhistorical labelと異なる場合、その両方を明記する。
6. source file存在とruntime integration成立を同一視しない。

## 禁止事項

`08` remediationでcontract defectを隠して修正してはならない。

G03がretrospective reconstructionであること自体を理由に、過去のworkflow実行事実、Trial、Fixed Candidate、Independent Verification、Gate PASSを遡及的に捏造してはならない。

過去source commitを記録するために既存のapproved 09 amendmentをsilent rewriteしない。追加のcontract changeは新しいAmendment IDでappendする。
