```
echo '===== git ====='
git branch --show-current
git rev-parse HEAD
pwd

echo
echo '===== local frontend marker ====='
grep -nE 'Project Management|Project Overview|Project List' frontend/index.html

echo
echo '===== served frontend :18080 ====='
curl -sS http://127.0.0.1:18080/ \
  | grep -nE 'Project Management|Project Overview|Project List' \
  | head -20

echo
echo '===== served frontend :8080 ====='
curl -sS http://127.0.0.1:8080/ \
  | grep -nE 'Project Management|Project Overview|Project List' \
  | head -20

echo
echo '===== running compose containers ====='
docker compose ps

echo
echo '===== frontend mounts ====='
docker inspect "$(docker ps -q --filter publish=18080 | head -1)" \
  --format '{{range .Mounts}}{{println .Source " -> " .Destination}}{{end}}'

```

```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ echo '===== git ====='
git branch --show-current
git rev-parse HEAD
pwd

echo
echo '===== local frontend marker ====='
grep -nE 'Project Management|Project Overview|Project List' frontend/index.html

echo
echo '===== served frontend :18080 ====='
curl -sS http://127.0.0.1:18080/ \
  | grep -nE 'Project Management|Project Overview|Project List' \
  | head -20

echo
echo '===== served frontend :8080 ====='
curl -sS http://127.0.0.1:8080/ \
  | grep -nE 'Project Management|Project Overview|Project List' \
  | head -20

echo
echo '===== running compose containers ====='
docker compose ps

echo
echo '===== frontend mounts ====='
docker inspect "$(docker ps -q --filter publish=18080 | head -1)" \
  --format '{{range .Mounts}}{{println .Source " -> " .Destination}}{{end}}'
===== git =====
feature/ariadne_mvp_e7
b6953e8ec0e7d8f0a693bcbb31fb831f83ce4f5c
/loc0/bigbrother/repositories/causal-atelier

===== local frontend marker =====
14:        <button data-workspace="management" data-route="overview">Project Management</button>
41:        <h1>Project Overview</h1>
49:        <h1>Project List</h1>

===== served frontend :18080 =====
14:        <button data-workspace="management" data-route="overview">Project Management</button>
41:        <h1>Project Overview</h1>
49:        <h1>Project List</h1>

===== served frontend :8080 =====
14:        <button data-workspace="management" data-route="overview">Project Management</button>
41:        <h1>Project Overview</h1>
49:        <h1>Project List</h1>

===== running compose containers =====
NAME                        IMAGE                   COMMAND                  SERVICE    CREATED          STATUS                    PORTS
causal-atelier-api-1        causal-atelier-api      "uvicorn ariadne.int…"   api        10 minutes ago   Up 10 minutes (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
causal-atelier-database-1   postgres:17-alpine      "docker-entrypoint.s…"   database   10 minutes ago   Up 10 minutes (healthy)   127.0.0.1:5432->5432/tcp
causal-atelier-frontend-1   nginx:1.27-alpine       "/docker-entrypoint.…"   frontend   10 minutes ago   Up 10 minutes             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
causal-atelier-worker-1     causal-atelier-worker   "ariadne-worker"         worker     10 minutes ago   Up 10 minutes             8000/tcp

===== frontend mounts =====
/loc0/bigbrother/repositories/causal-atelier/deploy/nginx.conf  ->  /etc/nginx/conf.d/default.conf
/loc0/bigbrother/repositories/causal-atelier/frontend  ->  /usr/share/nginx/html

```