from metamodel.io.jsonParser import parseScenario


def test_parse_scenario():
    model = parseScenario({
        "entities": [
            {"id": "org", "type": "Organization", "name": "Example"},
            {"id": "sec", "type": "Sector", "name": "Finance"},
        ],
        "relationships": [
            {"type": "operatesIn", "source": "org", "target": "sec"},
        ],
    })
    assert len(model.entities) == 2
    assert len(model.relationships) == 1
