# 03c Compose Project Inventory Result

## Metadata

- Prompt: `03c_compose_project_inventory_prompt.md`
- Started at: `2026-08-08T06:32:02+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `1f493aed49ffc18aab76de3c2cc89cb1dd3f5fbc`

> Read-only Compose project inventory. No container or volume was modified.

## 03c-01 causal-atelier Compose project containers

### Command

````bash
docker ps -a --filter label=com.docker.compose.project=causal-atelier --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES     STATUS    service
````

## 03c-02 ariadne-e1a Compose project containers

### Command

````bash
docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES                    STATUS                   service
51e57bcc7fb6   ariadne-e1a-api-1        Up 8 hours (healthy)     api
45888735054c   ariadne-e1a-migrate-1    Exited (0) 8 hours ago   migrate
f99a0d095a70   ariadne-e1a-worker-1     Up 19 hours              worker
26031e681c75   ariadne-e1a-frontend-1   Up 24 hours              frontend
df5f53878ef7   ariadne-e1a-database-1   Up 47 hours (healthy)    database
````

## 03c-03 causal-atelier Compose project volumes

### Command

````bash
docker volume ls --filter label=com.docker.compose.project=causal-atelier --format "{{.Name}}" | sort
````

### Exit Code

````text
0
````

### Output

````text
causal-atelier_artifact-data
causal-atelier_metadata-data
````

## 03c-04 ariadne-e1a Compose project volumes

### Command

````bash
docker volume ls --filter label=com.docker.compose.project=ariadne-e1a --format "{{.Name}}" | sort
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_artifact-data
ariadne-e1a_metadata-data
````

## 03c-05 causal-atelier metadata volume consumers

### Command

````bash
docker ps -a --filter volume=causal-atelier_metadata-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES     STATUS
````

## 03c-06 ariadne-e1a metadata volume consumers

### Command

````bash
docker ps -a --filter volume=ariadne-e1a_metadata-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES                    STATUS
df5f53878ef7   ariadne-e1a-database-1   Up 47 hours (healthy)
````

## 03c-07 causal-atelier artifact volume consumers

### Command

````bash
docker ps -a --filter volume=causal-atelier_artifact-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES     STATUS
````

## 03c-08 ariadne-e1a artifact volume consumers

### Command

````bash
docker ps -a --filter volume=ariadne-e1a_artifact-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES                  STATUS
51e57bcc7fb6   ariadne-e1a-api-1      Up 8 hours (healthy)
f99a0d095a70   ariadne-e1a-worker-1   Up 19 hours
````

## 03c-09 Target volume creation timestamps

### Command

````bash
for v in causal-atelier_metadata-data causal-atelier_artifact-data ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} CreatedAt={{.CreatedAt}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; done
````

### Exit Code

````text
0
````

### Output

````text
Name=causal-atelier_metadata-data CreatedAt=2026-08-05T13:15:20Z Project=causal-atelier Volume=metadata-data
Name=causal-atelier_artifact-data CreatedAt=2026-08-05T13:28:08Z Project=causal-atelier Volume=artifact-data
Name=ariadne-e1a_metadata-data CreatedAt=2026-08-06T07:07:20Z Project=ariadne-e1a Volume=metadata-data
Name=ariadne-e1a_artifact-data CreatedAt=2026-08-06T07:07:20Z Project=ariadne-e1a Volume=artifact-data
````

## Completion

- Finished at: `2026-08-08T06:32:02+00:00`
- Phase execution: `COMPLETED`
