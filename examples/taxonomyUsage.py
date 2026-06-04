from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry

registry = TaxonomyRegistry.load_default()
concept = registry.resolve("attackTools:cobaltStrike")
print(concept)
