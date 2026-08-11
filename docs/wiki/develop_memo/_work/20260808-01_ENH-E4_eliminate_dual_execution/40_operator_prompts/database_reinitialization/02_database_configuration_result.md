# 02 Database Configuration Result

## Metadata

- Prompt: `02_database_configuration_prompt.md`
- Started at: `2026-08-08T06:13:50+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `ae7ae1246304bda91bdf7e1a102bdcc193043d3e`

> Command execution records only. No interpretation has been added.

## 02-01 Current branch

### Command

````bash
git branch --show-current
````

### Exit Code

````text
0
````

### Output

````text
refactor/ariadne_mvp_e4
````

## 02-02 Compose database and persistence configuration

### Command

````bash
sed -n "1,120p" compose.yaml
````

### Exit Code

````text
0
````

### Output

````text
services:
  database:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: ariadne
      POSTGRES_USER: ariadne
      POSTGRES_PASSWORD: ariadne
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ariadne"]
      interval: 5s
      timeout: 5s
      retries: 12
    volumes:
      - metadata-data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"

  migrate:
    build: .
    command: ["alembic", "-c", "alembic_product.ini", "upgrade", "head"]
    environment: &backend-environment
      ARIADNE_PRODUCT_DATABASE_URL: postgresql+psycopg://ariadne:ariadne@database:5432/ariadne
      ARIADNE_ARTIFACT_ROOT: /state/objects
    depends_on:
      database:
        condition: service_healthy

  api:
    build: .
    environment: *backend-environment
    depends_on:
      migrate:
        condition: service_completed_successfully
    ports:
      - "8000:8000"
    volumes:
      - artifact-data:/state
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/ready')"]
      interval: 10s
      timeout: 5s
      retries: 6

  worker:
    build: .
    command: ["ariadne-worker"]
    environment: *backend-environment
    depends_on:
      migrate:
        condition: service_completed_successfully
    volumes:
      - artifact-data:/state

  frontend:
    image: nginx:1.27-alpine
    depends_on:
      api:
        condition: service_healthy
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
      - ./deploy/nginx.conf:/etc/nginx/conf.d/default.conf:ro

volumes:
  metadata-data:
  artifact-data:
````

## 02-03 E1a Compose override

### Command

````bash
sed -n "1,120p" compose.e1a.yaml
````

### Exit Code

````text
0
````

### Output

````text
services:
  database:
    ports: !override
      - "127.0.0.1:15432:5432"
  api:
    ports: !override
      - "127.0.0.1:18000:8000"
  frontend:
    ports: !override
      - "127.0.0.1:18080:80"
  browser-e2e:
    build:
      context: .
      dockerfile: Dockerfile.browser-e2e
    image: ariadne-e1a-browser-e2e:playwright-1.62.0
    # The workspace is group-restricted and hosted on a root-squashed filesystem.
    user: "${ARIADNE_E2E_USER:-1000:1000}"
    profiles: ["e2e"]
    working_dir: /workspace
    environment:
      ARIADNE_E2E_WEB_URL: http://frontend
      ARIADNE_E2E_API_URL: http://api:8000/api/v1
      ARIADNE_E2E_OUTPUT_DIR: /evidence
      PLAYWRIGHT_BROWSERS_PATH: /ms-playwright
      PYTHONDONTWRITEBYTECODE: "1"
    volumes:
      - ./test-results/browser_e2e:/evidence
    depends_on:
      frontend:
        condition: service_started
````

## 02-04 Legacy Alembic configuration

### Command

````bash
grep -nE "script_location|sqlalchemy\.url" alembic.ini
````

### Exit Code

````text
0
````

### Output

````text
2:script_location = migrations
4:sqlalchemy.url = postgresql+psycopg://ariadne:ariadne@localhost:5432/ariadne
````

## 02-05 Product Alembic configuration

### Command

````bash
grep -nE "script_location|sqlalchemy\.url" alembic_product.ini
````

### Exit Code

````text
0
````

### Output

````text
2:script_location = product_migrations
4:sqlalchemy.url = postgresql+psycopg://ariadne:ariadne@localhost:5432/ariadne
````

## 02-06 Legacy Alembic runtime configuration

### Command

````bash
grep -nE "ARIADNE_DATABASE_URL|target_metadata|version_table|sqlalchemy\.url" migrations/env.py
````

### Exit Code

````text
0
````

### Output

````text
18:    "sqlalchemy.url",
19:    os.getenv("ARIADNE_DATABASE_URL", config.get_main_option("sqlalchemy.url")),
21:target_metadata = Base.metadata
26:        url=config.get_main_option("sqlalchemy.url"),
27:        target_metadata=target_metadata,
43:        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
````

## 02-07 Product Alembic runtime configuration

### Command

````bash
grep -nE "ARIADNE_PRODUCT_DATABASE_URL|target_metadata|version_table|sqlalchemy\.url" product_migrations/env.py
````

### Exit Code

````text
0
````

### Output

````text
16:database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
18:    raise RuntimeError("ARIADNE_PRODUCT_DATABASE_URL is required for Product migrations")
19:config.set_main_option("sqlalchemy.url", database_url)
20:target_metadata = ProductBase.metadata
25:        url=config.get_main_option("sqlalchemy.url"),
26:        target_metadata=target_metadata,
30:        version_table="alembic_version_product",
45:            target_metadata=target_metadata,
47:            version_table="alembic_version_product",
````

## 02-08 Web API database and artifact configuration

### Command

````bash
grep -nE "ARIADNE_PRODUCT_DATABASE_URL|ARIADNE_ARTIFACT_ROOT|create_engine" src/ariadne/interfaces/web_api/dependencies.py
````

### Exit Code

````text
0
````

### Output

````text
12:from sqlalchemy import create_engine
36:    database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
38:        raise RuntimeError("ARIADNE_PRODUCT_DATABASE_URL is required")
39:    engine = create_engine(database_url)
44:    root = Path(os.getenv("ARIADNE_ARTIFACT_ROOT", ".ariadne/objects"))
````

## 02-09 Worker database and artifact configuration

### Command

````bash
grep -nE "ARIADNE_PRODUCT_DATABASE_URL|ARIADNE_ARTIFACT_ROOT|create_engine" src/ariadne/interfaces/worker/runner.py
````

### Exit Code

````text
0
````

### Output

````text
38:    from sqlalchemy import create_engine
42:    engine = create_engine(database_url)
115:    database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
117:        raise RuntimeError("ARIADNE_PRODUCT_DATABASE_URL is required")
118:    artifact_root = Path(os.getenv("ARIADNE_ARTIFACT_ROOT", ".ariadne/objects"))
````

## 02-10 Legacy migration files

### Command

````bash
find migrations/versions -maxdepth 1 -type f -name "*.py" -print | sort
````

### Exit Code

````text
0
````

### Output

````text
migrations/versions/20260719_0001_initial_metadata.py
migrations/versions/20260720_0002_analysis_ready_mvp.py
migrations/versions/20260803_0003_rename_run_to_execution.py
migrations/versions/20260804_0004_mlflow_tracking_columns.py
````

## 02-11 Product migration files

### Command

````bash
find product_migrations/versions -maxdepth 1 -type f -name "*.py" -print | sort
````

### Exit Code

````text
0
````

### Output

````text
product_migrations/versions/20260805_product_0001_baseline.py
product_migrations/versions/20260806_product_0002_enh_e1.py
product_migrations/versions/20260806_product_0003_enh_e2.py
product_migrations/versions/20260807_product_0004_enh_e3_workspace.py
product_migrations/versions/20260807_product_0005_enh_e3_g4_predictive.py
product_migrations/versions/20260807_product_0006_enh_e3_g6_closure.py
````

## 02-12 Legacy migration revision chain

### Command

````bash
grep -HnE "^(revision|down_revision)[[:space:]]*=" migrations/versions/*.py || true
````

### Exit Code

````text
0
````

### Output

````text
migrations/versions/20260719_0001_initial_metadata.py:17:revision = "20260719_0001"
migrations/versions/20260719_0001_initial_metadata.py:18:down_revision = None
migrations/versions/20260720_0002_analysis_ready_mvp.py:18:revision = "20260720_0002"
migrations/versions/20260720_0002_analysis_ready_mvp.py:19:down_revision = "20260719_0001"
migrations/versions/20260803_0003_rename_run_to_execution.py:15:revision = "20260803_0003"
migrations/versions/20260803_0003_rename_run_to_execution.py:16:down_revision = "20260720_0002"
migrations/versions/20260804_0004_mlflow_tracking_columns.py:37:revision = "20260804_0004"
migrations/versions/20260804_0004_mlflow_tracking_columns.py:38:down_revision = "20260803_0003"
````

## 02-13 Product migration revision chain

### Command

````bash
grep -HnE "^(revision|down_revision)[[:space:]]*=" product_migrations/versions/*.py || true
````

### Exit Code

````text
0
````

### Output

````text
product_migrations/versions/20260805_product_0001_baseline.py:15:revision = "20260805_product_0001"
product_migrations/versions/20260805_product_0001_baseline.py:16:down_revision = None
product_migrations/versions/20260806_product_0002_enh_e1.py:12:revision = "20260806_product_0002"
product_migrations/versions/20260806_product_0002_enh_e1.py:13:down_revision = "20260805_product_0001"
product_migrations/versions/20260806_product_0003_enh_e2.py:12:revision = "20260806_product_0003"
product_migrations/versions/20260806_product_0003_enh_e2.py:13:down_revision = "20260806_product_0002"
product_migrations/versions/20260807_product_0004_enh_e3_workspace.py:12:revision = "20260807_product_0004"
product_migrations/versions/20260807_product_0004_enh_e3_workspace.py:13:down_revision = "20260806_product_0003"
product_migrations/versions/20260807_product_0005_enh_e3_g4_predictive.py:12:revision = "20260807_product_0005"
product_migrations/versions/20260807_product_0005_enh_e3_g4_predictive.py:13:down_revision = "20260807_product_0004"
product_migrations/versions/20260807_product_0006_enh_e3_g6_closure.py:12:revision = "20260807_product_0006"
product_migrations/versions/20260807_product_0006_enh_e3_g6_closure.py:13:down_revision = "20260807_product_0005"
````

## 02-14 DB-related shell environment variable names

### Command

````bash
env | sed "s/=.*//" | grep -E "^(ARIADNE_DATABASE_URL|ARIADNE_PRODUCT_DATABASE_URL|ARIADNE_PRODUCT_TEST_DATABASE_URL|ARIADNE_ARTIFACT_ROOT|ARIADNE_STATE_DIR)$" | sort || true
````

### Exit Code

````text
0
````

### Output

````text
````

## 02-15 Compose services

### Command

````bash
docker compose -f compose.yaml config --services
````

### Exit Code

````text
0
````

### Output

````text
database
migrate
api
frontend
worker
````

## 02-16 Compose volumes

### Command

````bash
docker compose -f compose.yaml config --volumes
````

### Exit Code

````text
0
````

### Output

````text
artifact-data
metadata-data
````

## 02-17 E1a merged Compose services

### Command

````bash
docker compose -f compose.yaml -f compose.e1a.yaml config --services
````

### Exit Code

````text
0
````

### Output

````text
database
migrate
api
frontend
worker
````

## 02-18 E1a merged Compose volumes

### Command

````bash
docker compose -f compose.yaml -f compose.e1a.yaml config --volumes
````

### Exit Code

````text
0
````

### Output

````text
metadata-data
artifact-data
````

## Completion

- Finished at: `2026-08-08T06:13:50+00:00`
- Phase execution: `COMPLETED`
