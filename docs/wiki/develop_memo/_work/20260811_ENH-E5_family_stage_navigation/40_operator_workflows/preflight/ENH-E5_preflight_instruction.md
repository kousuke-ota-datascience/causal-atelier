# ENH-E5 Preflight Instruction

文書区分: Operator Artifact（運用資料）

## 目的

planning上のUNKNOWNを解消し、G00 contract freeze前にrepository/test baselineを証明する。

## 実行command

```bash
set -euo pipefail

git branch --show-current
git rev-parse HEAD
git status --short

git log -1 --oneline
uv run pytest -q
```

full suiteがenvironment依存で実行困難な場合は、blockerを正確に記録し、repositoryで文書化されたfocused smoke/readiness pathを実行する。evidenceなしにPASSを主張しない。

## 必須確認項目

1. branchが`feature/ariadne_mvp_e5`であること。
2. local full SHAがpin済みplanning baseline `46122c68333df03680b97c253a7b5d32bf9393e7`と一致すること。
3. 想定外の未commit production/test/migration変更が存在しない、または明示的に説明されていること。
4. current test baselineが判明していること。
5. architecture discoveryの観測事項を、その正確なSHAに対して再確認すること。
6. 既存navigation descriptor/APIにより提案G00設計が重複実装にならないこと。

## 結果の扱い

- すべての前提成立 → 観測したlocal/test/migration/runtime factでControl Sheetを更新し、HumanはG00をfreezeしてよい。
- branch/SHAが曖昧 → `BLOCKED_BASELINE_IDENTITY`。
- architecture上の矛盾 → `BLOCKED_ARCHITECTURE_REVIEW`。
- environmentによりbaseline test不能 → `BLOCKED_PREFLIGHT_ENVIRONMENT`。product FAILとはしない。
