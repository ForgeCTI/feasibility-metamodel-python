from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

model = Model()
org = model.add_entity(Organization(name="ExampleBank", organization_size="enterprise", criticality="critical"))
sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
model.add_relationship(operatesIn(org, sector))
print(model.to_dict())
