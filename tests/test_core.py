from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn


def test_entity_id_is_generated():
    org = Organization(name="Example")
    assert org.id
    assert org.type == "Organization"


def test_relationship_type_checks_and_model():
    model = Model()
    org = model.add_entity(Organization(name="Example"))
    sector = model.add_entity(Sector(name="Finance"))
    rel = operatesIn(org, sector)
    model.add_relationship(rel)
    assert rel.type == "operatesIn"
    assert len(model.relationships) == 1
