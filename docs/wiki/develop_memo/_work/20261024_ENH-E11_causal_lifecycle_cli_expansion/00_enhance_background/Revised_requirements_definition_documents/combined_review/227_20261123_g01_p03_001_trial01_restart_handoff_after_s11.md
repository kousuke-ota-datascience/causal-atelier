# 227 — G01/P03/Trial01 authorized Coding Agent restart handoff

**Date:** 2026-11-23 JST  
**Status:** `LIMITED_S11_AUTHORIZED / ACTUAL_AGENT_PREFLIGHT_PENDING`  
**Frozen WHAT SHA:** `52e5c60176d6b72c91f839ef267f46657bd380b5`  
**Valid sequential Owner authority:** formal 09 record **222**, provisional S10 reFreeze record **224**, distinct limited S11 record **226**; completed P02 Reader compatibility approval **221**  
**P01 checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**P02 checkpoint:** `3a76a0aa1698037354b284ba7b5a875300473ce6`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**uv.lock tracked Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`

## Invocation

```text
以下の実行時変数で、指定のWork Package Coding Agent Promptを実行せよ。

GATE_ID=G01
PACKAGE_ID=P03
TRIAL_NO=01

対象リポジトリ:
kousuke-ota-datascience/causal-atelier

作業ブランチ:
feature/ariadne_mvp_e11

実行対象Prompt:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md

凍結規範契約 full Git SHA:
52e5c60176d6b72c91f839ef267f46657bd380b5

正式09 Owner承認:
00_enhance_background/Revised_requirements_definition_documents/combined_review/222_20261123_g01_p03_001_formal_09_owner_approved.md

S10 Owner再Freeze:
00_enhance_background/Revised_requirements_definition_documents/combined_review/224_20261123_g01_p03_001_s10_owner_refreeze.md

新S11 Owner承認:
00_enhance_background/Revised_requirements_definition_documents/combined_review/226_20261123_g01_p03_001_limited_s11_owner_authorization.md

完了済みP02 Reader限定改修Owner承認:
00_enhance_background/Revised_requirements_definition_documents/combined_review/221_20261123_g01_p03_p02_reader_compat_owner_approved.md

承認記録の共通相対path起点:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/

P01 PACKAGE_READY checkpoint:
9bff61f0eae25236f95f31f2cd3e7c81291f0167

P02 PACKAGE_READY checkpoint:
3a76a0aa1698037354b284ba7b5a875300473ce6

最初に実リポジトリのremote、branch、HEAD、clean worktree、
Frozen SHA ancestor、凍結後の管理記録だけの差分、uv.lockの
blobと実ファイルSHA-256、P01/P02 checkpoint祖先・公式状態、
P03 checkpoint不存在・Trial01のGate FAIL/08不存在、
正式09=222、再Freeze S10=224、新S11=226を照合せよ。

G01/P03の凍結06、G01の凍結07、上位RD/LDD/BD/IF/DD/Graph Schema、
AMD-E11-G01-P03-001の規範契約に従い実装すること。
承認221の範囲でのみ完了済みP02 ReaderのGraphProvenance
検証を限定的に強化し、そのテストと既存P02/P01回帰を実施する。
P01/P02の旧PACKAGE_READYチェックポイントを再作成・上書きしない。
限定範囲の外へのコード修正が必要ならSTOPしOwnerへ報告せよ。

Graph provenanceはtyped six-field構造、Method/Backend/CI、
SourceRefsとStudy/Manifestの完全一致、実ContentRef bytes hash、
null first-parent、internal semantic hashと外部byte hashの分離を検証。
PAG circle/arrow/bidirectedをDAGへ勝手に変換せず、実P04科学的
referenceなしにscientific PASSを宣言しないこと。

実環境でfocused test・Graph契約・Reader・回帰を実行し、
実測記録に基づき公式Package Reportと有効な新checkpointを作成せよ。
新しい契約欠陥は、コード側で推測修正せずBLOCKEDとして報告せよ。
```

## Remaining unperformed work

Issuing S11 and this handoff does not itself run the Coding Agent, edit any executable source or test, assert actual Linux readback, create a P03 checkpoint, or certify G01 07/999 and independent science. Such evidence is required separately after actual execution.
