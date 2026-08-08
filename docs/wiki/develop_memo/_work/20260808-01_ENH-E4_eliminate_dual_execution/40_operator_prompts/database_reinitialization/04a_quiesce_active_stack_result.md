# 04a Quiesce Active Stack Result

## Metadata

- Prompt: `04a_quiesce_active_stack_prompt.md`
- Started at: `2026-08-08T06:42:10+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `e1c43797dc640a062ed7faeef93b27264bbb4eb6`
- Target branch: `refactor/ariadne_mvp_e4`
- Target Compose project: `ariadne-e1a`

> This phase stops the active stack only. Persistent volumes are not removed.

## 04a-01 Current branch precondition

### Command

````bash
CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"
````

### Exit Code

````text
0
````

### Output

````text
refactor/ariadne_mvp_e4
````

## 04a-02 Docker daemon access precondition

### Command

````bash
docker version --format "client={{.Client.Version}} server={{.Server.Version}}"
````

### Exit Code

````text
0
````

### Output

````text
client=29.6.2 server=29.6.2
````

## 04a-03 Active project container inventory before stop

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
26031e681c75   ariadne-e1a-frontend-1   Up 25 hours              frontend
df5f53878ef7   ariadne-e1a-database-1   Up 2 days (healthy)      database
````

## 04a-04 Database container project identity

### Command

````bash
test "$(docker inspect ariadne-e1a-database-1 --format "{{index .Config.Labels \"com.docker.compose.project\"}}")" = "ariadne-e1a"
````

### Exit Code

````text
0
````

### Output

````text
````

## 04a-05 Database volume mount precondition

### Command

````bash
test "$(docker inspect ariadne-e1a-database-1 --format "{{range .Mounts}}{{if eq .Destination \"/var/lib/postgresql/data\"}}{{.Name}}{{end}}{{end}}")" = "ariadne-e1a_metadata-data"
````

### Exit Code

````text
0
````

### Output

````text
````

## 04a-06 API artifact volume mount precondition

### Command

````bash
test "$(docker inspect ariadne-e1a-api-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")" = "ariadne-e1a_artifact-data"
````

### Exit Code

````text
0
````

### Output

````text
````

## 04a-07 Worker artifact volume mount precondition

### Command

````bash
test "$(docker inspect ariadne-e1a-worker-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")" = "ariadne-e1a_artifact-data"
````

### Exit Code

````text
0
````

### Output

````text
````

## 04a-08 Active volumes before stop

### Command

````bash
for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; done
````

### Exit Code

````text
0
````

### Output

````text
Name=ariadne-e1a_metadata-data Project=ariadne-e1a Volume=metadata-data
Name=ariadne-e1a_artifact-data Project=ariadne-e1a Volume=artifact-data
````

## 04a-09 Stop active Compose stack

### Command

````bash
docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml stop
````

### Exit Code

````text
0
````

### Output

````text
 Container ariadne-e1a-worker-1 Stopping 
 Container ariadne-e1a-frontend-1 Stopping 
 Container ariadne-e1a-frontend-1 Stopped 
 Container ariadne-e1a-api-1 Stopping 
 Container ariadne-e1a-api-1 Stopped 
 Container ariadne-e1a-worker-1 Stopped 
 Container ariadne-e1a-migrate-1 Stopping 
 Container ariadne-e1a-migrate-1 Stopped 
 Container ariadne-e1a-database-1 Stopping 
 Container ariadne-e1a-database-1 Stopped 
````

## 04a-10 Active project container inventory after stop

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
CONTAINER ID   NAMES                    STATUS                              service
51e57bcc7fb6   ariadne-e1a-api-1        Exited (0) 6 seconds ago            api
45888735054c   ariadne-e1a-migrate-1    Exited (0) 8 hours ago              migrate
f99a0d095a70   ariadne-e1a-worker-1     Exited (0) Less than a second ago   worker
26031e681c75   ariadne-e1a-frontend-1   Exited (0) 8 seconds ago            frontend
df5f53878ef7   ariadne-e1a-database-1   Exited (0) Less than a second ago   database
````

## 04a-11 Active volumes after stop

### Command

````bash
for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; done
````

### Exit Code

````text
0
````

### Output

````text
Name=ariadne-e1a_metadata-data Project=ariadne-e1a Volume=metadata-data
Name=ariadne-e1a_artifact-data Project=ariadne-e1a Volume=artifact-data
````

## Completion

- Finished at: `2026-08-08T06:42:20+00:00`
- Phase execution: `COMPLETED`
- Persistent volumes: `PRESERVED`
