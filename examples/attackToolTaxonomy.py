from metamodel.cyberThreat.entities.AttackTool import AttackTool

tool = AttackTool(name="Cobalt Strike", taxonomy_ref="attackTools:cobaltStrike")
print(tool.to_dict())
