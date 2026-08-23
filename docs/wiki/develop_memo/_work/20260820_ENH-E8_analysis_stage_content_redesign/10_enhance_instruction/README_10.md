# 10 — ENH-E8 Gate / Work Package Contract

`06` はimplementation semantic authority、`07` はAcceptance Criteria authorityである。`Pxx` はimplementation executionを分解するが、Gate claimを弱めたり変更したりしない。

- G01 mode: `SINGLE_EXECUTION`
- G02 mode: `WORK_PACKAGE`
- G02 order: P01 -> P02 -> P03 -> Candidate Assembly -> Independent Verification
- G03 mode: `SINGLE_EXECUTION`
- G03 purpose: ENH-E8完了後に確認されたCausal Estimation submission regressionの後追い契約化・回帰防止

G01/G02の06/07およびG02 P00〜P03はHuman approvalにより `FROZEN`。08/09はformal FAILまたはsemantic amendment時まで`TEMPLATE`のままinactiveとする。

G03は、ENH-E8完了後に実装済みとなったbugfixを監査可能なEnhance Instructionとして残すための**retrospective reconstruction**である。G03の06/07は、実装前にfreezeされていたと遡及的に扱ってはならない。文書化時点で観測できる実装事実と回帰条件を `RETROSPECTIVE_FROZEN` として固定し、今後のregression protection authorityとして使用する。G03の08/09は他Gateと同様、formal FAILまたはcontract defectが発生するまで`TEMPLATE`としてinactiveとする。
