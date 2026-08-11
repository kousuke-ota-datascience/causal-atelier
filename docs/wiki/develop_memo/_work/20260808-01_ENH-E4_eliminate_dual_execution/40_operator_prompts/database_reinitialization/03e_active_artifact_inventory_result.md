# 03e Active Artifact Inventory Result

## Metadata

- Prompt: `03e_active_artifact_inventory_prompt.md`
- Started at: `2026-08-08T06:38:46+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `79fea02077e7d4b5d991e307687d61b8326f8b73`
- Target container: `ariadne-e1a-api-1`
- Target volume: `ariadne-e1a_artifact-data`
- Target path: `/state`

> Read-only artifact inventory. File contents were not inspected.

## 03e-01 API container state

### Command

````bash
docker ps --filter name="^/ariadne-e1a-api-1$" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES               STATUS
51e57bcc7fb6   ariadne-e1a-api-1   Up 8 hours (healthy)
````

## 03e-02 API container mount mapping

### Command

````bash
docker inspect ariadne-e1a-api-1 --format "{{json .Mounts}}"
````

### Exit Code

````text
0
````

### Output

````text
[{"Type":"volume","Name":"ariadne-e1a_artifact-data","Source":"/var/lib/docker/volumes/ariadne-e1a_artifact-data/_data","Destination":"/state","Driver":"local","Mode":"rw","RW":true,"Propagation":""}]
````

## 03e-03 Artifact volume metadata

### Command

````bash
docker volume inspect ariadne-e1a_artifact-data --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"
````

### Exit Code

````text
0
````

### Output

````text
Name=ariadne-e1a_artifact-data Driver=local Mountpoint=/var/lib/docker/volumes/ariadne-e1a_artifact-data/_data Project=ariadne-e1a Volume=artifact-data
````

## 03e-04 State directory presence

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; test -d /state; printf "%s\n" "PRESENT: /state"; if [ -d /state/objects ]; then printf "%s\n" "PRESENT: /state/objects"; else printf "%s\n" "ABSENT: /state/objects"; fi'
````

### Exit Code

````text
0
````

### Output

````text
PRESENT: /state
PRESENT: /state/objects
````

## 03e-05 State storage usage

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; du -sh /state; if [ -d /state/objects ]; then du -sh /state/objects; fi'
````

### Exit Code

````text
0
````

### Output

````text
4.6M	/state
4.6M	/state/objects
````

## 03e-06 State file count

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; find /state -type f | wc -l'
````

### Exit Code

````text
0
````

### Output

````text
458
````

## 03e-07 Artifact object file count

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; if [ -d /state/objects ]; then find /state/objects -type f | wc -l; else printf "%s\n" "ABSENT: /state/objects"; fi'
````

### Exit Code

````text
0
````

### Output

````text
458
````

## 03e-08 State directory count

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; find /state -type d | wc -l'
````

### Exit Code

````text
0
````

### Output

````text
700
````

## 03e-09 Shallow state tree

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; find /state -mindepth 1 -maxdepth 2 -print | sort'
````

### Exit Code

````text
0
````

### Output

````text
/state/objects
/state/objects/projects
/state/workspaces
````

## Completion

- Finished at: `2026-08-08T06:38:47+00:00`
- Phase execution: `COMPLETED`
