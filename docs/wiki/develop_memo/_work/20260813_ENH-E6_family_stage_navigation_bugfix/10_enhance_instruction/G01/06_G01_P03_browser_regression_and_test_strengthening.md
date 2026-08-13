# ENH-E6 G01 P03 — Browser Regression and Test Strengthening

- Status: `DRAFT`

## Outcome

ANOM-E5-001を再発させないobservable acceptance evidenceを実装する。

## Required browser coverage

- normal analysis entry immediately shows actual Family tabs
- actual Family tab click -> default Stage
- actual Stage click -> Family retained
- Causal discovery/inference presentation binding
- legacy shortcut canonical targets
- direct canonical route
- reload
- back/forward

## Existing source-inspection tests

`analysis-family-tabs` stringや`catalog.families.map` stringの検査はsupplemental static protectionとして残してよい。ただしreal-browser blocking proofの代替として扱わない。

## Anti-patterns

- test中にrendererを直接呼んでnormal entry defectを回避
- forced reload before first assertion
- hidden elementのtext existenceだけをvisible扱い
