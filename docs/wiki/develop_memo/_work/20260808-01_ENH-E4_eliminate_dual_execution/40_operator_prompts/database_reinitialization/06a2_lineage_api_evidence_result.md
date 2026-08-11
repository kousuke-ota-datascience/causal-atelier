# 06a2 Lineage API Evidence Result

## Metadata

- Prompt: `06a2_lineage_api_evidence_prompt.md`
- Started at: `2026-08-08T07:15:58+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `ddf0a165b05727604700bf39b1d201d1d47d762f`
- Root result: `9203bd6d-abbc-47a4-9bc2-bc5ea061f98c`

> Read-only evidence capture. No Product state was modified.

## 06a2-01 Lineage API request

### Exit Code

````text
0
````
### Error Output

````text
````

## 06a2-02 Lineage API summary

````text
node_count=11
edge_count=13
node_type[Annotation]=1
node_type[Artifact]=3
node_type[DatasetVersion]=1
node_type[Execution]=2
node_type[GraphVersion]=1
node_type[Project]=1
node_type[Result]=2
required_node_types_present=true
missing_required_node_types=
````

## 06a2-03 Persisted LineageEdge count

````text
0
````

## 06a2-04 Golden Path lineage assertion

````python
        _require(client.post("/comparisons/query", json={
            "project_id": project_id,
            "result_ids": [result["result_id"] for result in estimation_results],
        }))
````

## Completion

- Finished at: `2026-08-08T07:15:59+00:00`
- Phase execution: `COMPLETED`
- Product state modified: `NO`
