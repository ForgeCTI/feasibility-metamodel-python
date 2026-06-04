from metamodel.adapters.networkxAdapter import toNetworkx
from examples.organizationScenario import model

graph = toNetworkx(model)
print(graph.number_of_nodes(), graph.number_of_edges())
