# 10 — ENH-E8 Gate / Work Package Contract

`06` はimplementation semantic authority、`07` はAcceptance Criteria authorityである。`Pxx` はimplementation executionを分解するが、Gate claimを弱めたり変更したりしない。

- G01 mode: `SINGLE_EXECUTION`
- G02 mode: `WORK_PACKAGE`
- G02 order: P01 -> P02 -> P03 -> Candidate Assembly -> Independent Verification

G01/G02の06/07およびG02 P00〜P03はHuman approvalにより `FROZEN`。08/09はformal FAILまたはsemantic amendment時まで`TEMPLATE`のままinactiveとする。
