# 10 — ENH-E8 Gate / Work Package Contract

`06` はimplementation semantic authority、`07` はAcceptance Criteria authorityである。`Pxx` はimplementation executionを分解するが、Gate claimを弱めたり変更したりしない。

- G01 mode: `SINGLE_EXECUTION`
- G02 mode: `WORK_PACKAGE`
- G02 order: P01 -> P02 -> P03 -> Candidate Assembly -> Independent Verification
- G03 mode: `SINGLE_EXECUTION`
- G03 purpose: ENH-E8完了後に確認されたCausal Estimation submission regressionの後追い契約化・回帰防止

G01/G02の06/07およびG02 P00〜P03はHuman approvalにより `FROZEN`。08/09はformal FAILまたはsemantic amendment時まで`TEMPLATE`のままinactiveとする。

G03は、ENH-E8完了後に実装済みとなったbugfixを監査可能なEnhance Instructionとして残すための**retrospective reconstruction**である。G03の06/07は、実装前にfreezeされていたと遡及的に扱ってはならない。

G03 initial reconstruction後に追加bugfixが入り、handler bootstrap中のinteraction race、canonical frontend static asset delivery、およびhistorical regression testのstalenessが追加blocking conditionとして判明した。このため `G03-A01` Gate Contract Amendmentを`APPROVED/APPLIED`とし、G03の06/07を `RETROSPECTIVE_FROZEN / A01_APPLIED` としてre-baselineした。

G03のformal Independent Verificationは未実施であり、Trial01 Fixed Verification Candidateはまだ確定していない。G03の08はformal FAIL時までinactive、追加の09は新たなcontract defect / approved semantic amendmentが発生するまでinactiveとする。
