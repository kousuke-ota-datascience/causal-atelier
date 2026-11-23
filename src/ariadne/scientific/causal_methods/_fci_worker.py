"""Private subprocess boundary for importing and fitting the selected Backend."""
import hashlib
import inspect
import json
import os
import sys
import tempfile
from importlib.metadata import version


def _run(request):
    from causallearn.graph.Edge import Edge
    from causallearn.graph.GeneralGraph import GeneralGraph
    from causallearn.graph.GraphNode import GraphNode
    from causallearn.search.ConstraintBased.FCI import fci
    import numpy as np

    observed = version("causal-learn")
    signature = inspect.signature(fci)
    expected = (
        "dataset", "independence_test_method", "alpha", "depth", "max_path_length", "verbose",
        "background_knowledge", "show_progress", "node_names", "kwargs",
    )
    accessors = ((Edge, ("get_node1", "get_node2", "get_endpoint1", "get_endpoint2")),
                 (GeneralGraph, ("get_nodes", "get_graph_edges")), (GraphNode, ("get_name",)))
    fingerprint = hashlib.sha256(str(signature).encode()).hexdigest()
    if (
        sys.version_info[:2] != (3, 12) or observed != "0.1.4.8"
        or tuple(signature.parameters) != expected
        or not all(callable(getattr(cls, name, None)) for cls, names in accessors for name in names)
    ):
        return {"error": "BACKEND_API_MISMATCH"}
    if request["action"] == "probe":
        return {"version": observed, "api_signature_hash": fingerprint}
    if request["api_signature_hash"] != fingerprint or request["version"] != observed:
        return {"error": "BACKEND_API_MISMATCH"}
    settings = request["config"]
    if settings["background_knowledge"] is not None:
        return {"error": "BACKEND_SEMANTICS_UNVERIFIED"}
    profile = settings["indep_test"]
    data = np.asarray(request["rows"], dtype=np.float64 if profile == "fisherz" else np.int64)
    result = fci(
        dataset=data, independence_test_method=profile, alpha=settings["alpha"], depth=settings["depth"],
        max_path_length=settings["max_path_length"], background_knowledge=None,
        show_progress=False, verbose=False, node_names=request["columns"],
    )
    if type(result) is not tuple or len(result) != 2 or type(result[1]) is not list:
        return {"error": "BACKEND_API_MISMATCH"}
    graph, edges = result
    if not isinstance(graph, GeneralGraph):
        return {"error": "BACKEND_API_MISMATCH"}

    def edge_values(edge):
        return {
            "source": edge.get_node1().get_name(), "target": edge.get_node2().get_name(),
            "source_mark": edge.get_endpoint1().name, "target_mark": edge.get_endpoint2().name, "lag": None,
        }

    edges_wire = [edge_values(edge) for edge in edges]
    structural = [edge_values(edge) for edge in graph.get_graph_edges()]

    def oriented_key(edge):
        s, t = edge["source"], edge["target"]
        left, right = edge["source_mark"], edge["target_mark"]
        return (s, t, left, right) if s < t else (t, s, right, left)

    if sorted(map(oriented_key, edges_wire)) != sorted(map(oriented_key, structural)):
        return {"error": "BACKEND_API_MISMATCH"}
    return {"nodes": [node.get_name() for node in graph.get_nodes()], "edges": edges_wire}


def main():
    request = json.load(sys.stdin)
    # Keep a private control descriptor. Backend output never enters the control stream.
    with os.fdopen(os.dup(1), "w", encoding="utf-8") as control:
        with open(os.devnull, "wb") as discard, tempfile.TemporaryDirectory() as cache:
            os.dup2(discard.fileno(), 1)
            os.dup2(discard.fileno(), 2)
            os.environ["MPLCONFIGDIR"] = cache
            try:
                response = _run(request)
            except ImportError:
                response = {"error": "BACKEND_UNAVAILABLE"}
            except Exception:
                response = {"error": "BACKEND_EXECUTION_FAILED"}
            json.dump(response, control, allow_nan=False)


if __name__ == "__main__":
    main()
