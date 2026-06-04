from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.rels.manages import manages
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor

model = Model()
org = model.add_entity(Organization(name="ExampleBank"))
sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
infra = model.add_entity(Infrastructure(name="ExampleBank infrastructure"))
actor = model.add_entity(ThreatActor(name="Example threat actor", sophistication="advanced"))
model.add_relationship(operatesIn(org, sector))
model.add_relationship(manages(org, infra))
print(model.to_dict())
