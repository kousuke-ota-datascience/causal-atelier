実行コマンド
```
docker compose down -v
docker compose up --build -d
```

```
docker compose exec api \
  alembic -c alembic_product.ini current

docker compose exec database \
  psql -U ariadne -d ariadne \
  -c "\dt product_project_membership"
```