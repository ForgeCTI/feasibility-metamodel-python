"""NetworkX export example."""

from pathlib import Path

from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.adapters.networkxAdapter import toNetworkx

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    model = Model()
    organization = model.add_entity(Organization(name="ExampleBank"))
    sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
    model.add_relationship(operatesIn(organization, sector))

    graph = toNetworkx(model)

    OUTPUT_DIR.mkdir(exist_ok=True)
    summary_file = OUTPUT_DIR / "networkx_summary.txt"
    summary_file.write_text(
        f"Nodes: {graph.number_of_nodes()}\nEdges: {graph.number_of_edges()}\n",
        encoding="utf-8",
    )

    print(summary_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
