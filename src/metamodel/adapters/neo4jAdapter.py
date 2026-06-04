from __future__ import annotations


def toCypherStatements(model) -> list[str]:
    """Create Cypher statements that can be executed against Neo4j."""
    statements = []
    for entity in model.entities:
        data = {k: v for k, v in entity.to_dict().items() if v is not None}
        statements.append(
            "MERGE (n:{label} {{id: $id}}) SET n += $props".format(label=entity.type)
        )
    for rel in model.relationships:
        statements.append(
            "MATCH (a {{id: $source_id}}), (b {{id: $target_id}}) "
            "MERGE (a)-[r:{rel_type} {{id: $id}}]->(b)".format(rel_type=rel.type)
        )
    return statements


def exportToNeo4j(model, uri: str, user: str, password: str) -> None:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise ImportError("neo4j is required. Install with: pip install cyber-feasibility-metamodel[neo4j]") from exc

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        for entity in model.entities:
            props = {k: v for k, v in entity.to_dict().items() if k not in {"id", "type"} and v is not None}
            session.run(
                f"MERGE (n:{entity.type} {{id: $id}}) SET n += $props",
                id=entity.id,
                props=props,
            )
        for rel in model.relationships:
            session.run(
                f"MATCH (a {{id: $source_id}}), (b {{id: $target_id}}) MERGE (a)-[r:{rel.type} {{id: $id}}]->(b)",
                source_id=rel.source_entity.id,
                target_id=rel.target_entity.id,
                id=rel.id,
            )
    driver.close()
