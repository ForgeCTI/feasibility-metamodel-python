from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MOTIVATING = ROOT / "examples" / "13_motivating_example" / "data" / "scenario.yaml"


@pytest.fixture
def motivating_model():
    from metamodel.io.yamlParser import loadYamlScenario
    return loadYamlScenario(MOTIVATING)


class FakeResult(list):
    def consume(self):
        return None


class FakeNeo4j:
    """In-memory stand-in for the Neo4j driver that understands the adapter's statements."""

    def __init__(self):
        self.nodes = {}   # id -> (labels, props)
        self.edges = {}   # id -> (label, props, source, target)
        self.queries = []

    # driver API
    def session(self, database=None):
        self.database = database
        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def close(self):
        pass

    def run(self, query, params=None):
        import re
        params = params or {}
        self.queries.append((query, params))
        if query.startswith("MATCH (n:Entity) DETACH DELETE"):
            self.nodes.clear(); self.edges.clear()
            return FakeResult()
        if query.startswith("CREATE CONSTRAINT"):
            return FakeResult()
        if query.startswith("UNWIND $rows AS row MERGE (n:Entity"):
            labels = re.findall(r"`([A-Za-z]+)`", query.split("SET n:")[1].split(" SET")[0])
            for row in params["rows"]:
                props = dict(row["props"]); props["id"] = row["id"]
                self.nodes[row["id"]] = (labels, props)
            return FakeResult()
        if query.startswith("UNWIND $rows AS row MATCH"):
            label = re.search(r"\[r:`([A-Za-z]+)`", query).group(1)
            for row in params["rows"]:
                assert row["source"] in self.nodes and row["target"] in self.nodes
                props = dict(row["props"]); props["id"] = row["id"]
                self.edges[row["id"]] = (label, props, row["source"], row["target"])
            return FakeResult()
        if query.startswith("MATCH (n:Entity) RETURN"):
            return FakeResult({"props": props} for _, props in self.nodes.values())
        if query.startswith("MATCH (a:Entity)-[r]->(b:Entity)"):
            return FakeResult({"label": l, "props": p, "source": s, "target": t} for l, p, s, t in self.edges.values())
        raise AssertionError(f"unexpected query: {query}")


@pytest.fixture
def fake_neo4j():
    return FakeNeo4j()
