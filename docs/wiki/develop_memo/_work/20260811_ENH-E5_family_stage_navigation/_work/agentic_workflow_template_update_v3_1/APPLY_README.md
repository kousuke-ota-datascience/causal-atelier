# agentic_enhancement_workflow_template v3.1 反映手順

## 1. 結論

本packageは、v2で整理したoperational entry / candidate identity / formal FAIL remediation変更を維持したまま、追加handoffのBrowser E2E strategyを必要最小限の差分として反映する。

今回の主要追加点:

- Browser E2Eを廃止せず、Gate blocking canonical suiteを原則3〜5本程度のcritical user journeyへ縮小
- 各Gate 07はcanonical suiteからrelevant subsetだけを選択
- detailed correctnessをunit / API integration / frontend contract等のlower-level testへ配置
- Browser E2E environmentのhermetic化
- semantic synchronization / observable assertion
- Browser E2E failure evidence / classificationの標準化
- Test Agent / Coding Agent / Candidate Assembly / FAIL Reworkのfailure handling同期
- policy適用開始前に成立済みのfrozen contractへの非遡及適用

推奨手順:

```bash
./apply_agentic_enhancement_workflow_template_update_v3_1.sh --dry-run
./apply_agentic_enhancement_workflow_template_update_v3_1.sh
git diff --find-renames
```

スクリプトはcommit / pushを行わない。

## 2. Safety

- working treeがcleanでなければ停止する。
- payload invariantを実適用前に検査する。
- 既存promptは可能な場合`git mv`してから新canonical filenameへ差し替える。
- `--dry-run`はfileを変更せず、予定操作とpayload invariantを表示する。
- 実適用後にlegacy filename reference、主要invariant、`git diff --check`、`git status`、`git diff --stat --find-renames`を実行する。
- ENH-E5 / G04固有値がpayloadへ混入している場合は適用前に停止する。

## 3. Browser E2E policy authority

`40_operator_workflows/BROWSER_E2E_GATE_POLICY.md`はauthoring / operational policyであり、個別GateのAcceptance authorityではない。

Gate execution時のnormative verification authorityは従来通りfreeze済み07とする。したがって、Browser E2Eを使用するGateでは、critical journey / canonical command / environment / synchronization / assertion / evidence / decision semanticsを07本文へ具体化してfreezeする。

本template updateを理由に、適用時点ですでにfreeze済み、execution開始済み、または完了済みのcontract / Trial / enhancementへpolicyを遡及適用し、成立済みrequirementを削除・緩和してはならない。

## 4. MANIFEST

`MANIFEST.json`はpackage payloadへ固定値として同梱しない。

理由: payloadは変更対象だけを含むため、static manifestでは適用先に残るunchanged fileを完全に表現できない。またmanifest自身のhashを含めると自己参照になる。

実適用時に`regenerate_agentic_workflow_manifest.py`が適用先template全体を走査して最終`MANIFEST.json`を再生成する。`MANIFEST.json`自身はhash setから除外する。

## 5. Human review

実適用後、最低限以下を確認してからcommit / pushする。

```bash
git status --short
git diff --check
git diff --find-renames
git grep -n 'coding_agent_prompt\.md\|work_package_coding_agent_prompt\.md\|test_agent_prompt\.md'
```

特に以下を確認する。

- Work Package Coding Agentの`## 12. Final status`が保持されている。
- Test Agentの`## 13. Final status`が保持されている。
- `80_contract_amendment_log.md`と09 contract amendmentが相互trace可能である。
- formal FAIL後にnormal Pxx routeへ戻らない。
- Test Agentがcandidate identity不成立時にfail-closedする。
- `BROWSER_E2E_GATE_POLICY.md`が存在する。
- 07にprimary test layerとBrowser E2E critical journey selection ruleが存在する。
- Browser E2E failure classificationがTest Item / Gate Decision / Test Agentで整合する。
- test implementation / orchestration / environment defectがproduct FAILへ自動変換されない。
- frozen contractへのretroactive requirement緩和が記載されていない。
