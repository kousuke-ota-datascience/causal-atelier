# Webサービス化プロトタイプ用ブランチ作成手順

## 諸元

| 項目 | 値 |
|---|---|
| Git root | `/loc0/bigbrother/repositories/ariadne` |
| Remote name | `ariadne` |
| Remote repository | `git@github.com:kousuke-ota-datascience/ariadne.git` |
| Base branch | `main` |
| Prototype branch | `prototype/web-service` |

## 1. リポジトリルートへ移動する

```bash
cd /loc0/bigbrother/repositories/ariadne
```

## 2. 現在のブランチと変更状態を確認する

```bash
git branch --show-current
git status
git remote -v
```

`git status` が次の状態であることを確認する。

```text
nothing to commit, working tree clean
```

未コミットの変更がある場合は、ブランチ作成前にその変更をどこへ含めるか決める。

現在の `main` に含める変更であれば、先にコミットする。

```bash
git add .
git diff --cached --stat
git diff --cached --check
git commit -m "Prepare baseline for web service prototype"
git push ariadne main
```

Webサービス化ブランチだけに含める変更であれば、コミットせず手順5でブランチを
作成してからコミットする。

## 3. リモートの最新状態を取得する

```bash
git fetch ariadne
```

ローカルとリモートの履歴を確認する。

```bash
git log --oneline --graph --decorate --all -20
```

## 4. `main` を最新状態にする

working treeがcleanであることを確認してから実行する。

```bash
git switch main
git pull --ff-only ariadne main
```

`--ff-only` により、意図しないマージコミットの作成を防止する。

## 5. プロトタイプ用ブランチを作成する

```bash
git switch -c prototype/web-service
```

作成結果を確認する。

```bash
git branch --show-current
git status
```

次のブランチ名が表示されることを確認する。

```text
prototype/web-service
```

## 6. ブランチをGitHubへ登録する

```bash
git push -u ariadne prototype/web-service
```

`-u` により、ローカルブランチの追跡先として
`ariadne/prototype/web-service` が設定される。

## 7. 追跡設定を確認する

```bash
git branch -vv
git status
```

期待する表示例は次のとおり。

```text
* prototype/web-service ... [ariadne/prototype/web-service]
```

## 8. Webサービス化の初期変更をコミットする

実装後、変更内容を確認する。

```bash
git status --short
git diff
```

ステージングとコミットを行う。

```bash
git add .
git diff --cached --stat
git diff --cached --check
git commit -m "Prototype web service interface"
```

GitHubへpushする。

```bash
git push
```

## 9. Pull Requestを作成する場合

GitHub上で次のブランチ間のPull Requestを作成する。

```text
base:    main
compare: prototype/web-service
```

GitHub CLIを使用できる場合は、次のコマンドでも作成できる。

```bash
gh pr create \
  --base main \
  --head prototype/web-service \
  --title "Prototype web service interface" \
  --body "Webサービス化に向けたプロトタイプ実装です。"
```

## 最短手順

working treeがcleanで、ローカル `main` を最新化してから分岐する場合は、以下の
コマンドで作成できる。

```bash
cd /loc0/bigbrother/repositories/ariadne
git fetch ariadne
git switch main
git pull --ff-only ariadne main
git switch -c prototype/web-service
git push -u ariadne prototype/web-service
git branch -vv
```

## 注意事項

- 未コミットの変更を残したまま `main` をpullしない。
- プロトタイプの変更を直接 `main` へコミットしない。
- `git push --force` と `git push --force-with-lease` は使用しない。
- リモート名がまだ `origin` の場合は、コマンド中の `ariadne` を `origin` に
  読み替える。
