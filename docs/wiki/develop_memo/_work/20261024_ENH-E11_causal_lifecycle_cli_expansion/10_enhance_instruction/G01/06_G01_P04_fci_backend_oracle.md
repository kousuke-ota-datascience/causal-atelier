# ENH-E11 G01 P04 — FCI Capability, Eligibility, Independent Graph Oracle

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P04
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P01,P03
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
FCI/PAG Adapterの技術的・科学的適格性を分離して実証する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope
`MethodCapabilityRegistry.describe/resolve/load_adapter`を実装し外部科学Engine importはload時のみ。`FciDiscoveryAdapter.preflight/execute`で`P1-M06`、fisherz/chisq/gsq、alpha/depth/max_path_length、BK required/forbidden、Data/scale/欠損/カテゴリsupportを検査。実効causal-learn APIとnode/endpoint accessorを照合しsilent fallback/自動離散化/欠損補完を禁止。独立DAG→MAG→同値類PAG ReferenceでGraph endpoint/adjacencyを検証し、2-node latentの一意識別主張・BK過剰確定を拒否する。

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01,P03の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation
`MethodCapabilityRegistry.describe/resolve/load_adapter`を実装し外部科学Engine importはload時のみ。`FciDiscoveryAdapter.preflight/execute`で`P1-M06`、fisherz/chisq/gsq、alpha/depth/max_path_length、BK required/forbidden、Data/scale/欠損/カテゴリsupportを検査。実効causal-learn APIとnode/endpoint accessorを照合しsilent fallback/自動離散化/欠損補完を禁止。独立DAG→MAG→同値類PAG ReferenceでGraph endpoint/adjacencyを検証し、2-node latentの一意識別主張・BK過剰確定を拒否する。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| G01-07-08/09/10；CAP01/04/05、DD-E11-METH-P106 | `uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01 -q` | Backend API/CI/BK invalid inputが拒否され、独立Oracle未完ならScience BLOCKEDを維持する。 |

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。G01受入境界は再審査待ちで、勝手にGate acceptanceを変更しない。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria
Backend API/CI/BK invalid inputが拒否され、独立Oracle未完ならScience BLOCKEDを維持する。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
