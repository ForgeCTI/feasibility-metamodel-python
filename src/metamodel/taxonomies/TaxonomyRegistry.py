from __future__ import annotations

import json
from importlib.resources import files

from metamodel.taxonomies.Taxonomy import Taxonomy


class TaxonomyRegistry:
    """Registry for reusable controlled vocabularies."""

    def __init__(self) -> None:
        self.taxonomies: dict[str, Taxonomy] = {}

    def register(self, taxonomy: Taxonomy) -> Taxonomy:
        self.taxonomies[taxonomy.id] = taxonomy
        return taxonomy

    def get_taxonomy(self, taxonomy_id: str) -> Taxonomy | None:
        return self.taxonomies.get(taxonomy_id)

    def resolve(self, taxonomy_ref: str):
        if ":" not in taxonomy_ref:
            return None
        taxonomy_id, concept_id = taxonomy_ref.split(":", 1)
        taxonomy = self.get_taxonomy(taxonomy_id)
        if taxonomy is None:
            return None
        return taxonomy.get(concept_id)

    def contains(self, taxonomy_ref: str) -> bool:
        return self.resolve(taxonomy_ref) is not None

    @classmethod
    def load_default(cls) -> "TaxonomyRegistry":
        registry = cls()
        for package, filenames in DEFAULT_TAXONOMY_FILES.items():
            for filename in filenames:
                data = _load_yaml_resource(package, filename)
                registry.register(Taxonomy.from_dict(data))
        return registry


def _load_yaml_resource(package: str, filename: str) -> dict:
    text = (files(package) / filename).read_text(encoding="utf-8")
    try:
        import yaml
    except ImportError:
        # Minimal fallback for the bundled simple YAML files: convert through JSON-like subset is not supported.
        # Users who need taxonomy loading should install the yaml extra.
        raise ImportError("PyYAML is required to load taxonomy files. Install with: pip install cyber-feasibility-metamodel[yaml]")
    return yaml.safe_load(text)


DEFAULT_TAXONOMY_FILES = {
    "metamodel.taxonomies.attackTools": ["attackTools.yaml"],
    "metamodel.taxonomies.ttps": ["mitreAttackEnterprise.yaml"],
    "metamodel.taxonomies.vulnerabilities": ["cwe.yaml", "capec.yaml"],
    "metamodel.taxonomies.platforms": ["operatingSystems.yaml", "applications.yaml", "cloudServices.yaml"],
    "metamodel.taxonomies.infrastructure": ["nodeTypes.yaml", "userTypes.yaml", "informationTypes.yaml", "portTypes.yaml"],
    "metamodel.taxonomies.organization": ["sectors.yaml", "countries.yaml", "internationalBodies.yaml", "securityRequirements.yaml"],
}
