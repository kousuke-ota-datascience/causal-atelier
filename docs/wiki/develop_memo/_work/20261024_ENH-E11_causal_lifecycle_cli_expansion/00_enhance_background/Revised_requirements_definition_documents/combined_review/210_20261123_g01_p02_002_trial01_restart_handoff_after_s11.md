# 210 — G01/P02 Trial01 Coding Agent restart handoff after AMD-E11-G01-P02-002 S11

**Date:** 2026-11-23 JST  
**Status:** `LIMITED_S11_APPROVED / CODING_AGENT_PREFLIGHT_PENDING`  
**Owner S11 authority:** `combined_review/209_20261123_g01_p02_002_limited_s11_owner_authorization.md`  
**Formal 09:** 205; **revised S10:** 207; **S11 decision docket:** 208  
**Frozen normative WHAT SHA:** `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`  
**Previous P01 PACKAGE_READY:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Repository / Branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`  
**uv.lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Prior Coding Agent byte SHA-256 for uv.lock (remeasure):** `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`

## 1. Exact execution

```text
以下の実行時変数で、指定されたWork Package Coding Agent Promptを実行せよ。

GATE_ID=G01
PACKAGE_ID=P02
TRIAL_NO=01

対象リポジトリ:
kousuke-ota-datascience/causal-atelier

作業ブランチ:
feature/ariadne_mvp_e11

実行対象Prompt:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md

凍結済み規範契約 full Git SHA:
0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492

承認記録:
00_enhance_background/Revised_requirements_definition_documents/combined_review/205_20261123_g01_p02_002_formal_09_owner_approved.md
00_enhance_background/Revised_requirements_definition_documents/combined_review/207_20261123_g01_p02_002_revised_provisional_s10_owner_refreeze.md
00_enhance_background/Revised_requirements_definition_documents/combined_review/209_20261123_g01_p02_002_limited_s11_owner_authorization.md

上記相対承認記録の基点:
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/

P01チェックポイント:
9bff61f0eae25236f95f31f2cd3e7c81291f0167

既存P01 PACKAGE_READYを維持して再実装しないこと。
最初に現在のHEAD/remote/branch/clean worktree、凍結SHAの祖先関係、
凍結後の許可済み管理文書のみの差分、uv.lockのblobと実測byte digest、
正式09/S10/新S11、Trial01/No FAIL・08、P02 checkpointなしを確認すること。

旧S11記録201のみに依存して再開しないこと。
以降、凍結SHA時点のG01/P02 06、関連P05 06、G01 07、
5階層の要件・設計書およびAMD-E11-G01-P02-002に従って
P02を実装し、focused testと実Linux FSのpublish/Readerを検証し、
実測したPackage公式Reportと有効なcheckpointを作成せよ。
未実施の検証結果をPASSと報告しないこと。

PrivacyDecisionの別インスタンスが全フィールド同値で、Publisher独立Policy
再評価も現在の実Study/root/UID/inventoryを許可する場合は受理する。
偽造拒否テストはフィールド不一致、信頼済みPolicy拒否、
検証迂回の試みを対象とし、object identityやissuer証明を要求しない。
Manifest/Marker/rename前にすべての拒否条件をfail closedすること。

新しい契約欠陥、未検証前提、実FS環境のBlockerがあれば停止し、
理由と証拠を記録すること。科学的/独立Gate999 PASSを自己宣言しないこと。
```

## 2. P02 acceptance and inter-package boundary

- P02's exact contract at frozen SHA: `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md`; P05's future caller contract: `06_G01_P05_cli_use_case_privacy.md`; G01 test instruction: `07_Ariadne_ENH-E11_G01_test_instruction.md`.
- All stock RD/LDD/BD/IF/DD in `00_enhance_background/Revised_requirements_definition_documents/` are the upper normative design authority. No direct rewrite of frozen documents.
- P01 remains implemented. P03/P04 scientific validity and P05 end-to-end integration are separate dependent packages. No fake graph-negative proof, row export or Product v2 rewrite.
- Positive equal-value-decision case, mismatch/denied cases, secure Linux trusted-root, atomic no-clobber, Marker/readback, cross-process crash failures must be independently distinguishable and measured. Developer test success cannot be promoted to G01_999.

## 3. What remains unexecuted

No Coding Agent execution, P02 code, P02 tests, actual Linux filesystem proof, P02 checkpoint or official Package report is claimed **by this control-plane handoff**. Trial01 preflight and real evidence remain responsibilities of the executable Agent.
