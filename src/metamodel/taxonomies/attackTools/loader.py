from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry


def load():
    registry = TaxonomyRegistry.load_default()
    return registry
