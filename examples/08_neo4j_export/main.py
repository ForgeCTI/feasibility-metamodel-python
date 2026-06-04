"""Neo4j export example.

Start Neo4j first:
    docker compose -f examples/08_neo4j_export/docker-compose.yml up
"""

from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.adapters.neo4jAdapter import exportToNeo4j


def main() -> None:
    model = Model()
    organization = model.add_entity(Organization(name="ExampleBank"))
    sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
    model.add_relationship(operatesIn(organization, sector))

    exportToNeo4j(
        model,
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password",
    )

    print("Export completed. Open http://localhost:7474 and run queries/inspect_graph.cypher.")


if __name__ == "__main__":
    main()
