# ENH-E11 G01 P05 — Local CLI, UseCase, Privacy, Legacy Regression

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P05
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P02,P03,P04
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
DISCOVER-only CLIの全経路を統合し、Product v2を回帰保護する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope
`LocalCausalUseCase.preflight/run(spec,context)`（`LocalRunContext`はTrustedRoot・Principal・CLI row flagを保持）、`LocalPrivacyPolicy.assert_export_allowed`、`interfaces.cli.local_causal.command.main`を実装。CLIのcheck-onlyは実科学計算/Publishともゼロ。`DISCOVER+P1-M06`でQuestion/Design/Dataset→FCI PAG→Graph/Study/Status→Publisher→Reader、Effect Resultなし。Study行要求かCLI row flagならG01ではexit3で拒否、暗黙aggregate fallback禁止。Schema exit2、input/Privacy exit3、Backend exit4、publication/readback exit5。旧Product CLI/Result/Manifest/DB/Web/Workerは改変せず既存テストを回帰実行する。

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P02,P03,P04の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation
`LocalCausalUseCase.preflight/run(spec,context)`（`LocalRunContext`はTrustedRoot・Principal・CLI row flagを保持）、`LocalPrivacyPolicy.assert_export_allowed`、`interfaces.cli.local_causal.command.main`を実装。CLIのcheck-onlyは実科学計算/Publishともゼロ。`DISCOVER+P1-M06`でQuestion/Design/Dataset→FCI PAG→Graph/Study/Status→Publisher→Reader、Effect Resultなし。Study行要求かCLI row flagならG01ではexit3で拒否、暗黙aggregate fallback禁止。Schema exit2、input/Privacy exit3、Backend exit4、publication/readback exit5。旧Product CLI/Result/Manifest/DB/Web/Workerは改変せず既存テストを回帰実行する。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| G01-07-07/11/12；RUN01/03/04/06/07、PRIV01〜06、PUB10/MAN04〜06/READ06 | `uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01 -q` | strict CLI envelope、no row/secret leakage、old Product v2 regression、no false COMMITTED/Science PASS。 |

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
strict CLI envelope、no row/secret leakage、old Product v2 regression、no false COMMITTED/Science PASS。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
