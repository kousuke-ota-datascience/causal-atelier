# Ariadne ENH-E6 — Family / Stage Navigation Observable UI Bugfix

- Enhancement ID: `ENH-E6`
- Target branch: `bugfix/ariadne_mvp_e6`
- Planning baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Planning date: `2026-08-13`
- Source anomaly: `ENH-E5 / ANOM-E5-001 — Family Tab Observable UI Gap`
- Current state: `G01 CONTRACT FROZEN / READY_FOR_P01`
- Production code changes: `NOT STARTED`
- Gate contract status: `APPROVED / FROZEN`

## Objective

ENH-E5 で成立させる契約だった `EXPLORATORY / PREDICTIVE / CAUSAL` の Family tabs と Family-local Navigation Stage が、通常の画面遷移を含む実ユーザー導線で observable かつ URL / application state / selected Family / selected Stage / presentation surface と一貫して動作する状態へ修正する。

## Workflow position

本bundleは `agentic_enhancement_workflow_template` の次を実施した Planning artifact である。

1. Background / requirements / design の作成
2. Gate decomposition の決定
3. Current State Control Sheet の初期化
4. Gate 06 / 07 の draft 作成
5. Work Package mode と package decomposition の draft 作成

Human owner review、API READY clean baseline reproduction、既存 Playwright harness / canonical invocation pattern の確認を完了し、G01 06 / 07 は `APPROVED / FROZEN` とする。次の実行単位は P01 Coding Agent である。

## Directory

- `00_enhance_background/`: why / requirement / design / alignment / anomaly provenance
- `10_enhance_instruction/G01/`: Gate semantic contract, verification contract, Work Package draft
- `Current_State_Control_Sheet.md`: ENH-E6 開始時 verified state index

## Gate map

### G01 — Observable Family / Stage Navigation Integration

PASSすると、canonical Family/Stage navigation が通常導線・deep link・reload・back/forward・legacy compatibility entry の全てで同一 state transition authority を通り、Family tabs / Family-local Stage sidebar / presentation surface が同期して observable であることへ後続作業が依存できる。

Gate は UI部品・route・testを別Gateへ分割しない。これらは同一 semantic claim の成立条件であり、実装量による分割は Work Package で扱う。
