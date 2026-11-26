"""Neo4j export and import example (motivating example of the paper).

Start Neo4j first:
    docker compose -f examples/08_neo4j_export/docker-compose.yml up -d
then run:
    NEO4J_PASSWORD=password python examples/08_neo4j_export/main.py
Without a running server, the script only writes the Cypher script.
"""

import os
from pathlib import Path

from metamodel.adapters.neo4jAdapter import exportToNeo4j, importFromNeo4j, toCypherScript
from metamodel.io.yamlParser import loadYamlScenario

BASE_DIR = Path(__file__).resolve().parent
SCENARIO = BASE_DIR.parent / "13_motivating_example" / "data" / "scenario.yaml"


def main() -> None:
    model = loadYamlScenario(SCENARIO)

    (BASE_DIR / "output").mkdir(exist_ok=True)
    script = BASE_DIR / "output" / "load_motivating_example.cypher"
    script.write_text(toCypherScript(model, clear=True), encoding="utf-8")
    print(f"Cypher script written to {script} (cypher-shell -f {script.name}).")

    password = os.environ.get("NEO4J_PASSWORD")
    if not password:
        print("NEO4J_PASSWORD not set: skipping the live export.")
        return
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    counts = exportToNeo4j(model, uri, os.environ.get("NEO4J_USER", "neo4j"), password, clear=True)
    print(f"Exported {counts['nodes']} nodes and {counts['relationships']} relationships to {uri}.")
    back = importFromNeo4j(uri, os.environ.get("NEO4J_USER", "neo4j"), password)
    print(f"Re-imported {len(back.entities)} entities and {len(back.relationships)} relationships.")
    print("Open http://localhost:7474 and run queries/inspect_graph.cypher or queries/ts3_precondition.cypher.")


if __name__ == "__main__":
    main()
