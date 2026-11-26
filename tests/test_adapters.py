import pytest

from metamodel.adapters.neo4jAdapter import (
    cypher_literal, exportToNeo4j, importFromNeo4j, toCypherScript, toCypherStatements,
)
from metamodel.adapters.networkxAdapter import fromNetworkx, toNetworkx

from test_io_roundtrip import signature

nx = pytest.importorskip("networkx")


def test_networkx_export(motivating_model):
    graph = toNetworkx(motivating_model)
    assert graph.number_of_nodes() == len(motivating_model.entities)
    assert graph.number_of_edges() == len(motivating_model.relationships)
    assert graph.nodes["exchange-1"]["labels"] == ["ApplicationInstance", "Code", "Resource"]
    edges = [d for _, _, d in graph.edges("mailbox-account", data=True)]
    assert edges[0]["label"] == "grantsAccessTo"
    assert edges[0]["privilege_level"] == "pl-standard"
    assert graph.graph["name"].startswith("Motivating")


def test_networkx_roundtrip(motivating_model):
    assert signature(fromNetworkx(toNetworkx(motivating_model))) == signature(motivating_model)


def test_networkx_import_with_labels_only():
    graph = nx.MultiDiGraph()
    graph.add_node("sc", type="SecurityControl", name="MFA")
    graph.add_node("acc", type="Account", name="a")
    graph.add_edge("sc", "acc", label="protects")
    model = fromNetworkx(graph)
    assert model.relationships[0].type == "protectsAccount"


def test_cypher_statements_are_batched_and_parameterized(motivating_model):
    statements = toCypherStatements(motivating_model, batch_size=1)
    assert statements[0][0].startswith("CREATE CONSTRAINT")
    queries = [q for q, _ in statements]
    assert any("SET n:`ApplicationInstance`:`Code`:`Resource`" in q for q in queries)
    assert any("[r:`grantsAccessTo`" in q for q in queries)
    assert sum(len(p.get("rows", [])) for _, p in statements) == len(motivating_model.entities) + len(motivating_model.relationships)


def test_neo4j_roundtrip_with_fake_driver(motivating_model, fake_neo4j):
    counts = exportToNeo4j(motivating_model, driver=fake_neo4j, clear=True, database="cti")
    assert counts == {"nodes": 34, "relationships": len(motivating_model.relationships)}
    grant = next(p for label, p, s, t in fake_neo4j.edges.values() if label == "grantsAccessTo")
    assert grant["privilege_level_rank"] == 1 and grant["class"] == "grantsAccessToResource"
    loaded = importFromNeo4j(driver=fake_neo4j)
    assert signature(loaded)[:2] == signature(motivating_model)[:2]


def test_cypher_script(motivating_model):
    script = toCypherScript(motivating_model)
    lines = script.strip().splitlines()
    assert lines[1].startswith("CREATE CONSTRAINT")
    assert len(lines) == 2 + len(motivating_model.entities) + len(motivating_model.relationships)
    assert all(line.endswith(";") for line in lines[1:])


@pytest.mark.parametrize("value, literal", [
    (None, "null"), (True, "true"), (3, "3"), (1.5, "1.5"), ("it's", "'it\\'s'"), (["a", 1], "['a', 1]"),
    ({"k": "v"}, "{`k`: 'v'}"),
])
def test_cypher_literal(value, literal):
    assert cypher_literal(value) == literal
