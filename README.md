# ariadne

ETL、分析用前処理、因果探索、因果推論を責務ごとに分離した分析基盤です。

実験は `experiments/<連番>_<サブテーマ>/`、対応するノートブックは
`notebooks/<連番>_<サブテーマ>/` で管理します。

## Webサービス

FastAPI control plane、PostgreSQL metadata DB、非同期worker、Local/S3/Azure Blob
Artifact Store、静的Frontendを含むMVP実装を提供します。既存CLIと数値実装は
そのまま残り、Web workerも同じDiscovery/Inference stage runnerを使用します。

最短の起動方法はDocker Composeです。

```bash
docker compose up --build
```

- Frontend: <http://localhost:8080>
- OpenAPI UI: <http://localhost:8000/docs>
- Readiness: <http://localhost:8000/health/ready>

開発用認証ではFrontendが `X-User-Subject` を送信します。本番では
`ARIADNE_AUTH_MODE=oidc` とし、issuer、audience、JWKS URLを設定して
Bearer tokenを検証してください。詳細な構成、resource登録からRun実行までの
流れ、environment variableは [Webサービス運用ガイド](docs/web_service.md) を参照してください。

ローカルでAPIとworkerを直接起動する場合は次のとおりです。

```bash
uv sync --all-groups
export ARIADNE_AUTO_CREATE_SCHEMA=true
uv run ariadne-api
# 別terminal
uv run ariadne-worker
```

テスト:

```bash
uv run pytest -q
```

本サービスは因果識別を自動証明しません。因果探索edgeはalgorithm依存の探索結果、
edge weightは探索的係数として表示し、treatment effectにはestimand、調整集合、
宣言された仮定、診断を併記します。

