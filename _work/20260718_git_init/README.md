# causal-atelier Git初期登録手順

## 諸元

| 項目 | 値 |
|---|---|
| Git root | `/loc0/bigbrother/repositories/causal-atelier` |
| GitHub repository | `git@github.com:kousuke-ota-datascience/causal-atelier.git` |
| Default branch | `main` |

## 1. リポジトリルートへ移動する

```bash
cd /loc0/bigbrother/repositories/causal-atelier
```

## 2. 現在のGit管理状態を確認する

```bash
ls -la .git
git rev-parse --is-inside-work-tree
```

`not a git repository` と表示され、既存の `.git` が空かつ書き込み不可の場合は、
所有者の書き込み権限を戻す。

```bash
chmod u+rwx .git
```

## 3. データファイルをGit管理対象外にする

`.gitignore` に以下が含まれていることを確認する。

```gitignore
data/00_raw/**
data/10_interim/**
data/20_processed/**

!data/00_raw/README_data.md
```

実データをGitHubへ登録する必要がある場合は、通常のGitへ直接追加せず、
Git LFSまたは外部ストレージの利用を検討する。

## 4. Gitリポジトリを初期化する

```bash
git init -b main
```

初期化結果を確認する。

```bash
git branch --show-current
git status --short
```

## 5. 巨大ファイルと機密情報を確認する

90 MBを超えるファイルを確認する。

```bash
find . -type f -size +90M -not -path './.git/*' -print
```

環境変数ファイルや秘密鍵などが含まれていないことも確認する。

```bash
find . -type f \
  \( -name '.env' -o -name '*.pem' -o -name '*.key' \) \
  -not -path './.git/*' -print
```

意図しないファイルが見つかった場合は、コミット前に `.gitignore` へ追加する。

## 6. コミットユーザーを設定する

すでにGitのグローバル設定がある場合、この手順は省略できる。

```bash
git config user.name "kousuke-ota-datascience"
git config user.email "GitHubに登録しているメールアドレス"
```

設定結果を確認する。

```bash
git config user.name
git config user.email
```

## 7. ファイルをステージングする

```bash
git add .
```

コミット対象を確認する。

```bash
git status
git diff --cached --stat
git diff --cached --check
```

`data/` 配下の実データ、ログ、仮想環境、キャッシュ、生成artifactが含まれていない
ことを確認する。

## 8. 初回コミットを作成する

```bash
git commit -m "Initial commit: restructure causal atelier"
```

コミットを確認する。

```bash
git log --oneline --decorate -1
```

## 9. GitHubへのSSH接続を確認する

```bash
ssh -T git@github.com
```

初回接続時はホスト鍵の確認が表示される。GitHubアカウントが正しく認識されることを
確認する。

## 10. リモートリポジトリを登録する

```bash
git remote add origin git@github.com:kousuke-ota-datascience/causal-atelier.git
git remote -v
```

すでに `origin` が存在する場合は、追加ではなくURLを更新する。

```bash
git remote set-url origin git@github.com:kousuke-ota-datascience/causal-atelier.git
git remote -v
```

## 11. リモートの状態を確認する

```bash
git fetch origin
git log --oneline --graph --all --decorate
```

GitHub側が空のリポジトリであることを確認できた場合は、次へ進む。

GitHub側にREADMEなどの既存コミットがある場合は、強制pushせず、履歴を統合する
方針を決める。

## 12. `main` ブランチをpushする

```bash
git push -u origin main
```

## 13. 登録結果を確認する

```bash
git status
git branch -vv
git remote -v
```

期待する状態は以下のとおり。

- working treeがcleanである
- ローカルの `main` が `origin/main` を追跡している
- GitHub上にソースコード、設定、テスト、ドキュメントが表示される
- 実データ、ログ、仮想環境、キャッシュ、生成artifactが登録されていない

## 注意事項

- `git push --force` および `git push --force-with-lease` は初回登録では使用しない。
- 認証エラーの場合は、GitHubに登録したSSH公開鍵と `ssh-agent` の状態を確認する。
- 100 MBを超えるファイルはGitHubの通常リポジトリへpushできない。
