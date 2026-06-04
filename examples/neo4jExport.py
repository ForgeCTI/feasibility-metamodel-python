from metamodel.adapters.neo4jAdapter import toCypherStatements
from examples.organizationScenario import model

for statement in toCypherStatements(model):
    print(statement)
