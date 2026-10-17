import pytest
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.core.Cardinality import Cardinality
from metamodel.core.Registry import Registry
from metamodel.core.Exceptions import RegistryError


# Entities tests


def test_entity_id_is_generated():
    org = Organization(name="Example")
    assert org.id
    assert org.type == "Organization"


def test_valid_add_entity():
    model = Model()
    org = Organization(name="Example")
    result = model.add_entity(org)
    assert result is org
    assert org in model.entities


def test_duplicate_entity_id():
    model = Model()
    org = Organization(name="Example")
    model.add_entity(org)
    with pytest.raises(ValueError):
        model.add_entity(org)


def test_invalid_entity_type():
    model = Model()
    with pytest.raises(TypeError):
        model.add_entity("ciao")


def test_valid_get_entity():
    model = Model()
    org = Organization(name="Example")
    model.add_entity(org)
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
    model.add_entity(org1)
    model.add_entity(org2)
    result = model.get_entities_by_type("Organization")
    assert len(result) == 2
    assert org1 in result
    assert org2 in result 


def test_entities_list_missing_type():
    model = Model()
    org1 = Organization(name="Example1")
    model.add_entity(org1)
    result = model.get_entities_by_type("Sector")
    assert result == []

    
# Relationships tests


def test_relationship_type_checks_and_model():
    model = Model()
    org = model.add_entity(Organization(name="Example"))
    sector = model.add_entity(Sector(name="Finance"))
    rel = operatesIn(org, sector)
    result = model.add_relationship(rel)
    assert result is rel
    assert rel.type == "operatesIn"
    assert rel in model.relationships
    assert len(model.relationships) == 1


def test_invalid_relationship_type():
    model = Model()
    with pytest.raises(TypeError):
        model.add_relationship("ciao")


def test_source_entity_not_added():
    model = Model()
    org = Organization(name="Example")
    sector = model.add_entity(Sector(name="Finance"))
    rel = operatesIn(org, sector)
    with pytest.raises(ValueError):
        model.add_relationship(rel)
        

def test_target_entity_not_added():
    model = Model()
    org = model.add_entity(Organization(name="Example"))
    sector = Sector(name="Finance")
    rel = operatesIn(org, sector)
    with pytest.raises(ValueError):
        model.add_relationship(rel)
        

def test_relationships_list_type():
    model = Model()
    org = Organization(name="Example")
    sec = Sector(name="Finance")
    rel = operatesIn(org, sec)
    model.add_entity(org)
    model.add_entity(sec)
    model.add_relationship(rel)
    result = model.get_relationships_by_type("operatesIn")
    assert len(result) == 1
    assert rel in result


def test_relationships_list_missing_type():
    model = Model()
    org = Organization(name="Example")
    sec = Sector(name="Finance")
    rel = operatesIn(org, sec)
    model.add_entity(org)
    model.add_entity(sec)
    model.add_relationship(rel)
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
    model.add_entity(organization)
    model.add_entity(sector)
    relationship = operatesIn(organization, sector)
    model.add_relationship(relationship)
    model.remove_relationship(relationship)
    assert relationship not in model.relationships


def test_remove_relationship_wrong_type():
    model = Model()
    with pytest.raises(TypeError):
        model.remove_relationship("not a relationship")


def test_remove_relationship_not_in_model():
    organization = Organization(name="Example organization")
    sector = Sector(name="Example sector")
    relationship = operatesIn(organization, sector)
    model = Model()
    with pytest.raises(ValueError):
        model.remove_relationship(relationship)


def test_model_to_dict():
    model = Model()
    org = Organization(name="Example")
    sec = Sector(name="Finance")
    rel = operatesIn(org, sec)
    model.add_entity(org)
    model.add_entity(sec)
    model.add_relationship(rel)
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