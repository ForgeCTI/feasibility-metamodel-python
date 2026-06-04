from metamodel.core.Model import Model
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.rels.madeBy import madeBy

model = Model()
infra = model.add_entity(Infrastructure(name="Corporate infrastructure", environment_type="production"))
node = model.add_entity(Node(name="web-01", hostname="web-01", ip_addresses=["10.0.0.10"]))
model.add_relationship(madeBy(infra, node))
print(model.to_dict())
