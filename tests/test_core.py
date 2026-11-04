import pytest
import importlib
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.core.Cardinality import Cardinality
from metamodel.core.Registry import Registry
from metamodel.core.Exceptions import RegistryError
from metamodel.core.ValidationReport import ValidationMessage
from metamodel.core.ValidationUtils import(
    require_optional_taxonomy_ref,
    require_optional_email,
    require_optional_float,
)


# Entities tests


def test_entity_id_is_generated():
    org = Organization(name="Example")
    assert org.id
    assert org.type == "Organization"


def test_valid_add_entity():
    model = Model()
    org = Organization(name="Example")
    result = model.add(org)
    assert result is org
    assert org in model.entities


def test_duplicate_entity_id():
    model = Model()
    org = Organization(name="Example")
    model.add(org)
    with pytest.raises(ValueError):
        model.add(org)


def test_valid_get_entity():
    model = Model()
    org = Organization(name="Example")
    model.add(org)
    assert model.get_entity(org.id) is org


def test_missing_get_entity():
    model = Model()
    org = Organization(name="Example")
    with pytest.raises(KeyError):
        model.get_entity(org.id)


def test_entities_list_type():
    model = Model()
    org1 = Organization(name="Example1")
    org2 = Organization(name="Example2")
    model.add(org1)
    model.add(org2)
    result = model.get_entities_by_type("Organization")
    assert len(result) == 2
    assert org1 in result
    assert org2 in result


def test_entities_list_missing_type():
    model = Model()
    org1 = Organization(name="Example1")
    model.add(org1)
    result = model.get_entities_by_type("Sector")
    assert result == []


def test_remove_isolated_entity():
    model = Model()
    org = model.add(Organization(name="Example"))
    model.remove(org)
    assert org not in model.entities
    with pytest.raises(KeyError):
        model.get_entity(org.id)


def test_remove_entity_with_incident_relationship():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    rel = model.add(operatesIn(org, sector))
    with pytest.raises(ValueError):
        model.remove(org)
    with pytest.raises(ValueError):
        model.remove(sector)
    assert org in model.entities
    assert sector in model.entities
    assert model.relationships == [rel]


def test_remove_relationship_then_entities():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    rel = model.add(operatesIn(org, sector))
    model.remove(rel)
    assert model.relationships == []
    model.remove(org)
    model.remove(sector)
    assert model.entities == []
    assert model.relationships == []


def test_remove_missing_entity():
    model = Model()
    org = model.add(Organization(name="Organization 1"))
    external_org = Organization(name="External organization")
    with pytest.raises(ValueError):
        model.remove(external_org)
    assert model.entities == [org]
    assert model.relationships == []


# Relationships tests


def test_relationship_type_checks_and_model():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    rel = operatesIn(org, sector)
    result = model.add(rel)
    assert result is rel
    assert rel.type == "operatesIn"
    assert rel in model.relationships
    assert len(model.relationships) == 1


def test_invalid_add_type():
    model = Model()
    with pytest.raises(TypeError):
        model.add("ciao")


def test_add_duplicate_relationship():
    model = Model()
    organization = Organization(name="Example organization")
    sector = Sector(name="Example sector")
    model.add(organization)
    model.add(sector)
    relationship = operatesIn(organization, sector)
    model.add(relationship)
    with pytest.raises(ValueError):
        model.add(relationship)


def test_add_duplicate_relationship_same_endpoints():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    rel1 = operatesIn(org, sector)
    rel2 = operatesIn(org, sector)
    assert rel1.id != rel2.id
    model.add(rel1)
    with pytest.raises(ValueError):
        model.add(rel2)
    assert model.relationships == [rel1]


def test_source_entity_not_added():
    model = Model()
    org = Organization(name="Example")
    sector = model.add(Sector(name="Finance"))
    rel = operatesIn(org, sector)
    with pytest.raises(ValueError):
        model.add(rel)


def test_target_entity_not_added():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = Sector(name="Finance")
    rel = operatesIn(org, sector)
    with pytest.raises(ValueError):
        model.add(rel)


def test_relationships_list_type():
    model = Model()
    org = Organization(name="Example")
    sec = Sector(name="Finance")
    rel = operatesIn(org, sec)
    model.add(org)
    model.add(sec)
    model.add(rel)
    result = model.get_relationships_by_type("operatesIn")
    assert len(result) == 1
    assert rel in result


def test_relationships_list_missing_type():
    model = Model()
    org = Organization(name="Example")
    sec = Sector(name="Finance")
    rel = operatesIn(org, sec)
    model.add(org)
    model.add(sec)
    model.add(rel)
    result = model.get_relationships_by_type("altraRelazione")
    assert result == []


def test_relationship_wrong_source_type():
    sec1 = Sector(name="Finance")
    sec2 = Sector(name="Other")

    with pytest.raises(TypeError):
        operatesIn(sec1, sec2)


def test_relationship_wrong_target_type():
    org1 = Organization(name="Example1")
    org2 = Organization(name="Example2")

    with pytest.raises(TypeError):
        operatesIn(org1, org2)


def test_relationship_source_entity_is_read_only():
    organization = Organization(name="Example organization")
    sector = Sector(name="Example sector")
    other_organization = Organization(name="Other organization")
    relationship = operatesIn(organization, sector)
    with pytest.raises(AttributeError):
        relationship.source_entity = other_organization


def test_relationship_target_entity_is_read_only():
    organization = Organization(name="Example organization")
    sector = Sector(name="Example sector")
    other_sector = Sector(name="Other sector")
    relationship = operatesIn(organization, sector)
    with pytest.raises(AttributeError):
        relationship.target_entity = other_sector


def test_remove_relationship():
    model = Model()
    organization = Organization(name="Example organization")
    sector = Sector(name="Example sector")
    model.add(organization)
    model.add(sector)
    relationship = operatesIn(organization, sector)
    model.add(relationship)
    model.remove(relationship)
    assert relationship not in model.relationships


def test_remove_relationship_wrong_type():
    model = Model()
    with pytest.raises(TypeError):
        model.remove("not a relationship")


def test_remove_relationship_not_in_model():
    organization = Organization(name="Example organization")
    sector = Sector(name="Example sector")
    relationship = operatesIn(organization, sector)
    model = Model()
    with pytest.raises(ValueError):
        model.remove(relationship)


def test_update_relationship_source():
    model = Model()
    org1 = model.add(Organization(name="Organization 1"))
    org2 = model.add(Organization(name="Organization 2"))
    sector = model.add(Sector(name="Finance"))
    rel = model.add(operatesIn(org1, sector))
    model.update_relationship(rel, source_entity=org2)
    assert rel.source_entity is org2
    assert rel.target_entity is sector
    assert rel in model.relationships


def test_update_relationship_both_endpoints():
    model = Model()
    org1 = model.add(Organization(name="Organization 1"))
    org2 = model.add(Organization(name="Organization 2"))
    sector1 = model.add(Sector(name="Finance"))
    sector2 = model.add(Sector(name="Technology"))
    rel = model.add(operatesIn(org1, sector1))
    model.update_relationship(
        rel,
        source_entity=org2,
        target_entity=sector2,
    )
    assert rel.source_entity is org2
    assert rel.target_entity is sector2
    assert rel in model.relationships


def test_update_relationship_wrong_source_type():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    other_sector = model.add(Sector(name="Technology"))
    rel = model.add(operatesIn(org, sector))
    with pytest.raises(TypeError):
        model.update_relationship(rel, source_entity=other_sector)
    assert rel.source_entity is org
    assert rel.target_entity is sector


def test_update_relationship_rejects_duplicate():
    model = Model()
    org1 = model.add(Organization(name="Organization 1"))
    org2 = model.add(Organization(name="Organization 2"))
    sector = model.add(Sector(name="Finance"))
    rel1 = model.add(operatesIn(org1, sector))
    rel2 = model.add(operatesIn(org2, sector))
    with pytest.raises(ValueError):
        model.update_relationship(rel2, source_entity=org1)
    assert rel2.source_entity is org2
    assert rel2.target_entity is sector
    assert model.relationships == [rel1, rel2]


def test_update_relationship_rejects_missing_entity():
    model = Model()
    org = model.add(Organization(name="Organization 1"))
    sector = model.add(Sector(name="Finance"))

    other_org = Organization(name="External organization")
    rel = model.add(operatesIn(org, sector))

    with pytest.raises(ValueError):
        model.update_relationship(rel, source_entity=other_org)

    assert rel.source_entity is org
    assert rel.target_entity is sector
    assert model.relationships == [rel]


def test_update_relationship_rejects_missing_relationship():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    other_org = model.add(Organization(name="Other organization"))

    rel = operatesIn(org, sector)

    with pytest.raises(ValueError):
        model.update_relationship(rel, source_entity=other_org)

    assert rel.source_entity is org
    assert rel.target_entity is sector
    assert model.relationships == []


def test_model_to_dict():
    model = Model()
    org = Organization(name="Example")
    sec = Sector(name="Finance")
    rel = operatesIn(org, sec)
    model.add(org)
    model.add(sec)
    model.add(rel)
    result = model.to_dict()
    assert "entities" in result
    assert "relationships" in result
    assert len(result["entities"]) == 2
    assert len(result["relationships"]) == 1
    assert org.to_dict() in result["entities"]
    assert sec.to_dict() in result["entities"]
    assert rel.to_dict() in result["relationships"]


# Cardinality tests


def test_cardinality_exact():
    cardinality = Cardinality.parse("1")
    assert cardinality.minimum == 1
    assert cardinality.maximum == 1
    assert cardinality.contains(1)
    assert not cardinality.contains(0)
    assert not cardinality.contains(2)


def test_cardinality_range():
    cardinality = Cardinality.parse("1..3")
    assert cardinality.minimum == 1
    assert cardinality.maximum == 3
    assert cardinality.contains(1)
    assert cardinality.contains(2)
    assert cardinality.contains(3)
    assert not cardinality.contains(0)
    assert not cardinality.contains(4)


def test_cardinality_unbounded():
    cardinality = Cardinality.parse("0..*")
    assert cardinality.minimum == 0
    assert cardinality.maximum is None
    assert cardinality.contains(0)
    assert cardinality.contains(100)


def test_invalid_cardinality():
    with pytest.raises(ValueError):
        Cardinality.parse("ciao")


def test_cardinality_rejects_negative_minimum():
    with pytest.raises(ValueError):
        Cardinality(-1, 5)


def test_cardinality_rejects_maximum_lower_than_minimum():
    with pytest.raises(ValueError):
        Cardinality(5, 2)


def test_cardinality_parse_rejects_negative_minimum():
    with pytest.raises(ValueError):
        Cardinality.parse("-1..5")


def test_cardinality_parse_rejects_maximum_lower_than_minimum():
    with pytest.raises(ValueError):
        Cardinality.parse("5..2")


def test_cardinality_rejects_non_integer_minimum():
    with pytest.raises(TypeError):
        Cardinality(1.5, 5)


def test_cardinality_rejects_non_integer_maximum():
    with pytest.raises(TypeError):
        Cardinality(1, 5.5)


def test_cardinality_rejects_boolean_values():
    with pytest.raises(TypeError):
        Cardinality(True, 5)


# Registry tests


def test_registry_get_entity_class():
    registry = Registry.load_default()
    result = registry.get_entity_class("Organization")
    assert result is Organization


def test_registry_get_relationship_class():
    registry = Registry.load_default()
    result = registry.get_relationship_class("operatesIn")
    assert result is operatesIn


def test_registry_missing_entity_class():
    registry = Registry.load_default()
    with pytest.raises(RegistryError):
        registry.get_entity_class("NonEsiste")


def test_registry_missing_relationship_class():
    registry = Registry.load_default()
    with pytest.raises(RegistryError):
        registry.get_relationship_class("NonEsiste")


def test_registry_rejects_invalid_entity_class(monkeypatch):
    registry_module = importlib.import_module("metamodel.core.Registry")
    monkeypatch.setattr(registry_module, "ENTITY_IMPORTS", [("InvalidEntity", "builtins", "str")])
    with pytest.raises(RegistryError):
        Registry.load_default()


def test_registry_rejects_invalid_relationship_class(monkeypatch):
    registry_module = importlib.import_module("metamodel.core.Registry")
    monkeypatch.setattr(registry_module, "RELATIONSHIP_IMPORTS", [("InvalidRelationship", "builtins", "str")])
    with pytest.raises(RegistryError):
        Registry.load_default()


# ValidationUtils tests


def test_optional_taxonomy_ref_valid():
    assert require_optional_taxonomy_ref("sectors:finance", "taxonomy_ref") == "sectors:finance"


def test_optional_taxonomy_ref_none():
    assert require_optional_taxonomy_ref(None, "taxonomy_ref") is None


@pytest.mark.parametrize(
    "value",
    [
        ":",
        "sectors:",
        ":finance",
        "sectors:finance:extra",
        " sectors:finance",
        "sectors :finance",
        "sectors: finance",
        "sectors:finance ",
    ],
)
def test_optional_taxonomy_ref_invalid_format(value):
    with pytest.raises(ValueError):
        require_optional_taxonomy_ref(value, "taxonomy_ref")


def test_optional_email_valid():
    assert require_optional_email("name@example.com", "email") == "name@example.com"


@pytest.mark.parametrize(
    "value",
    [
        "@",
        "a@",
        "@b",
        "a@@b.com",
        "a@example",
        "a b@example.com",
    ],
)
def test_optional_email_invalid(value):
    with pytest.raises(ValueError):
        require_optional_email(value, "email")


def test_optional_email_none():
    assert require_optional_email(None, "email") is None


@pytest.mark.parametrize("value", [
    float("nan"),
    float("inf"),
    float("-inf"),
])
def test_optional_float_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        require_optional_float(
            value,
            "cvss_score",
            minimum=0,
            maximum=10,
        )


# ValidationReport tests


def test_validation_message_rejects_invalid_severity():
    with pytest.raises(ValueError):
        ValidationMessage(validator="test", message="Test message", severity="banana")


def test_validation_message_is_immutable():
    message = ValidationMessage(validator="test", message="Test message", severity="error")

    with pytest.raises(AttributeError):
        message.severity = "warning"