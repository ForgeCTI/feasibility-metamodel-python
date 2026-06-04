from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.rels.toolInstanceOf import toolInstanceOf

model = Model()
tool = model.add_entity(AttackTool(name="Cobalt Strike", taxonomy_ref="attackTools:cobaltStrike", tool_type="command_and_control"))
instance = model.add_entity(AttackToolInstance(name="Observed beacon"))
model.add_relationship(toolInstanceOf(instance, tool))
print(model.to_dict())
