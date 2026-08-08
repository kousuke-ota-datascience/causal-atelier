# 03b Host Pre-reset State Result

## Metadata

- Prompt: `03b_host_pre_reset_state_prompt.md`
- Started at: `2026-08-08T06:28:27+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `ca4fdfaca2a8574230d53320ad2cd996e58faeab`

> Host-side read-only inspection. No reset operation was performed.

## 03b-01 Current branch

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

## 03b-02 Working tree status

### Command

````bash
git status --short
````

### Exit Code

````text
0
````

### Output

````text
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03b_host_pre_reset_state_prompt.md
````

## 03b-03 Effective user

### Command

````bash
id
````

### Exit Code

````text
0
````

### Output

````text
uid=1000(bigbrother) gid=1000(bigbrother) groups=1000(bigbrother),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),101(lxd),988(docker)
````

## 03b-04 Docker daemon access

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

## 03b-05 Compose container state

### Command

````bash
docker compose -f compose.yaml ps -a
````

### Exit Code

````text
0
````

### Output

````text
NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS
````

## 03b-06 Compose container state JSON

### Command

````bash
docker compose -f compose.yaml ps -a --format json
````

### Exit Code

````text
0
````

### Output

````text
````

## 03b-07 Metadata volume candidates

### Command

````bash
docker volume ls --filter label=com.docker.compose.volume=metadata-data --format "{{.Name}}" | sort
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_metadata-data
causal-atelier_metadata-data
````

## 03b-08 Metadata volume details

### Command

````bash
for v in $(docker volume ls --filter label=com.docker.compose.volume=metadata-data -q | sort); do docker volume inspect "$v" --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Labels={{json .Labels}}"; done
````

### Exit Code

````text
0
````

### Output

````text
Name=ariadne-e1a_metadata-data Driver=local Mountpoint=/var/lib/docker/volumes/ariadne-e1a_metadata-data/_data Labels={"com.docker.compose.config-hash":"72932331346644bdc60b087dbe873ba706a9f18e103fb1ebd242e531203eee38","com.docker.compose.project":"ariadne-e1a","com.docker.compose.version":"5.3.1","com.docker.compose.volume":"metadata-data"}
Name=causal-atelier_metadata-data Driver=local Mountpoint=/var/lib/docker/volumes/causal-atelier_metadata-data/_data Labels={"com.docker.compose.config-hash":"edd182da074d6d3efb8b6014a37c4f090b40505d50b80784ef4a9949327347fd","com.docker.compose.project":"causal-atelier","com.docker.compose.version":"5.3.1","com.docker.compose.volume":"metadata-data"}
````

## 03b-09 Artifact volume candidates

### Command

````bash
docker volume ls --filter label=com.docker.compose.volume=artifact-data --format "{{.Name}}" | sort
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_artifact-data
causal-atelier_artifact-data
````

## 03b-10 Artifact volume details

### Command

````bash
for v in $(docker volume ls --filter label=com.docker.compose.volume=artifact-data -q | sort); do docker volume inspect "$v" --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Labels={{json .Labels}}"; done
````

### Exit Code

````text
0
````

### Output

````text
Name=ariadne-e1a_artifact-data Driver=local Mountpoint=/var/lib/docker/volumes/ariadne-e1a_artifact-data/_data Labels={"com.docker.compose.config-hash":"7b9bb2c48a4af276ce41d591bf47a8c14078f7a057ad20061e297b5f1f8ed4ed","com.docker.compose.project":"ariadne-e1a","com.docker.compose.version":"5.3.1","com.docker.compose.volume":"artifact-data"}
Name=causal-atelier_artifact-data Driver=local Mountpoint=/var/lib/docker/volumes/causal-atelier_artifact-data/_data Labels={"com.docker.compose.config-hash":"820ac23d41cc045aef5c8b4df34ef79d9413a862cecb05f92feecd33d57474fe","com.docker.compose.project":"causal-atelier","com.docker.compose.version":"5.3.1","com.docker.compose.volume":"artifact-data"}
````

## 03b-11 Database container mount mapping

### Command

````bash
CID="$(docker compose -f compose.yaml ps -aq database | head -n 1)"; if [ -n "$CID" ]; then docker inspect "$CID" --format "{{json .Mounts}}"; else printf "%s\n" "ABSENT: database container"; fi
````

### Exit Code

````text
0
````

### Output

````text
ABSENT: database container
````

## 03b-12 API container mount mapping

### Command

````bash
CID="$(docker compose -f compose.yaml ps -aq api | head -n 1)"; if [ -n "$CID" ]; then docker inspect "$CID" --format "{{json .Mounts}}"; else printf "%s\n" "ABSENT: api container"; fi
````

### Exit Code

````text
0
````

### Output

````text
ABSENT: api container
````

## 03b-13 Database service running state

### Command

````bash
if docker compose -f compose.yaml ps --status running --services | grep -qx "database"; then printf "%s\n" "RUNNING"; else printf "%s\n" "NOT_RUNNING"; fi
````

### Exit Code

````text
0
````

### Output

````text
NOT_RUNNING
````

## 03b-14 through 03b-20 Database inspection

### Status

````text
SKIPPED: database service was not running.
The database service was not started by this phase.
````

## 03b-21 Repository-local .ariadne tree

### Command

````bash
if [ -e .ariadne ]; then find .ariadne -maxdepth 4 -printf "%y %p\n" | sort; else printf "%s\n" "ABSENT: .ariadne"; fi
````

### Exit Code

````text
0
````

### Output

````text
d .ariadne
d .ariadne/objects
d .ariadne/workspaces
````

## 03b-22 Repository-local .ariadne size

### Command

````bash
if [ -e .ariadne ]; then du -sh .ariadne; else printf "%s\n" "ABSENT: .ariadne"; fi
````

### Exit Code

````text
0
````

### Output

````text
12K	.ariadne
````

## 03b-23 Repository-local .ariadne file count

### Command

````bash
if [ -e .ariadne ]; then find .ariadne -type f | wc -l; else printf "%s\n" "ABSENT: .ariadne"; fi
````

### Exit Code

````text
0
````

### Output

````text
0
````

## Completion

- Finished at: `2026-08-08T06:28:28+00:00`
- Phase execution: `COMPLETED`
