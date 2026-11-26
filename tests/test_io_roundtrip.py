import json

import pytest

from metamodel.core.Exceptions import ParseError
from metamodel.io import (
    loadCsvDirectory, loadJsonScenario, loadModel, parseScenario, parseScenarioWithReport,
    saveCsvDirectory, saveJsonScenario, saveModel,
)
from metamodel.io.serialization import model_to_data


def signature(model):
    """Order-independent description of a model, including ids and attributes."""
    return (
        sorted(json.dumps(e.to_dict(), sort_keys=True, default=str) for e in model.entities),
        sorted(json.dumps(r.to_dict(), sort_keys=True, default=str) for r in model.relationships),
        model.metadata,
    )


@pytest.mark.parametrize("fmt, name", [("json", "s.json"), ("yaml", "s.yaml"), ("csv", "csvdir"), ("graphml", "s.graphml")])
def test_roundtrip_preserves_everything(tmp_path, motivating_model, fmt, name):
    path = tmp_path / name
    saveModel(motivating_model, path, fmt)
    loaded = loadModel(path, fmt)
    assert signature(loaded) == signature(motivating_model)
    assert loaded.validate().is_valid


def test_ids_are_preserved(tmp_path, motivating_model):
    assert motivating_model.has_entity("mx")
    saveJsonScenario(motivating_model, tmp_path / "s.json")
    loaded = loadJsonScenario(tmp_path / "s.json")
    grant = loaded.get_relationships_by_type("grantsAccessToResource")[0]
    assert grant.get_attribute("privilege_level").id == "pl-standard"


def test_csv_types_are_coerced(tmp_path, motivating_model):
    saveCsvDirectory(motivating_model, tmp_path)
    header = (tmp_path / "entities.csv").read_text().splitlines()[0]
    assert header.startswith("id,type,name,description,source")
    loaded = loadCsvDirectory(tmp_path)
    assert loaded.get_entity("https").number == 443
    assert loaded.get_entity("pl-standard").rank == 1


def test_csv_lists_and_booleans(tmp_path):
    (tmp_path / "entities.csv").write_text(
        "id,type,name,ip_addresses,enabled,kind\n"
        "n1,Node,Mail server,10.0.0.1;10.0.0.2,,\n"
        'a1,Account,svc,,false,service\n')
    (tmp_path / "relationships.csv").write_text("id,type,source,target\n")
    model = loadCsvDirectory(tmp_path)
    assert model.get_entity("n1").ip_addresses == ["10.0.0.1", "10.0.0.2"]
    assert model.get_entity("a1").enabled is False


def test_labels_and_legacy_names():
    model = parseScenario({
        "entities": [
            {"id": "app", "type": "ApplicationInstance", "name": "nginx"},
            {"id": "p", "type": "Port", "name": "80", "number": 80},
            {"id": "d", "type": "Information", "name": "records"},
            {"id": "dt", "type": "InformationType", "name": "personal data"},
            {"id": "sc", "type": "SecurityControl", "name": "MFA"},
            {"id": "acc", "type": "Account", "name": "a"},
        ],
        "relationships": [
            {"type": "listensOn", "source": "app", "target": "p"},
            {"type": "hasInformationType", "source": "d", "target": "dt"},
            {"type": "protects", "source": "sc", "target": "acc"},
            {"type": "protects", "source": "sc", "target": "d"},
        ],
    })
    assert sorted(r.type for r in model.relationships) == ["hasDataType", "protectsAccount", "protectsResource", "uses"]
    assert model.get_entity("d").type == "Data"


def test_strict_and_lenient_parsing():
    data = {"entities": [{"id": "n", "type": "Node", "name": "n", "colour": "red"},
                         {"id": "x", "type": "Unknown", "name": "x"}],
            "relationships": [{"type": "hasNodeType", "source": "n", "target": "missing"}]}
    with pytest.raises(ParseError, match="colour"):
        parseScenario(data)
    result = parseScenarioWithReport(data)
    assert len(result.model.entities) == 1
    assert len(result.warnings) == 3


def test_invalid_attribute_value_is_reported_with_entity():
    with pytest.raises(ParseError, match="'p'.*number"):
        parseScenario({"entities": [{"id": "p", "type": "Port", "name": "p", "number": 70000}], "relationships": []})


def test_unknown_privilege_level_reference():
    data = {"entities": [{"id": "a", "type": "Account", "name": "a"}, {"id": "n", "type": "Node", "name": "n"}],
            "relationships": [{"type": "grantsAccessTo", "source": "a", "target": "n", "privilege_level": "nope"}]}
    with pytest.raises(ParseError, match="unknown entity"):
        parseScenario(data)


def test_model_to_data_omits_empty_values(motivating_model):
    data = model_to_data(motivating_model, include_none=False)
    assert all(None not in e.values() for e in data["entities"])
    assert data["metadata"]["name"].startswith("Motivating")
