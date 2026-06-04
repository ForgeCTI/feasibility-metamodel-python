from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization

model = Model()
model.add_entity(Organization(name="Organization without sector"))
report = model.validate()
for msg in report.messages:
    print(msg)
