"""NetworkX export and import example (motivating example of the paper)."""

from pathlib import Path

from metamodel.adapters.graphmlAdapter import loadGraphML, saveGraphML
from metamodel.adapters.networkxAdapter import fromNetworkx, toNetworkx
from metamodel.io.yamlParser import loadYamlScenario

BASE_DIR = Path(__file__).resolve().parent
SCENARIO = BASE_DIR.parent / "13_motivating_example" / "data" / "scenario.yaml"
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    model = loadYamlScenario(SCENARIO)
    graph = toNetworkx(model)

    # Nodes carry the type hierarchy, edges the metamodel label.
    resources = [n for n, d in graph.nodes(data=True) if "Resource" in d["labels"]]
    grants = [(u, v, d.get("privilege_level")) for u, v, d in graph.edges(data=True) if d["label"] == "grantsAccessTo"]
    print(f"Nodes: {graph.number_of_nodes()}, edges: {graph.number_of_edges()}")
    print("Resources:", sorted(resources))
    print("Grants (account, resource, privilege level):", grants)

    # Round trip through NetworkX and GraphML.
    assert len(fromNetworkx(graph).entities) == len(model.entities)
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / "motivating_example.graphml"
    saveGraphML(model, str(path))
    print(f"GraphML written to {path}; re-imported entities: {len(loadGraphML(str(path)).entities)}")


if __name__ == "__main__":
    main()
