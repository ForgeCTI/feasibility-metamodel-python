"""Taxonomy usage example."""

from pathlib import Path

from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.AttackTool import AttackTool

try:
    from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry
except ImportError:
    TaxonomyRegistry = None


BASE_DIR = Path(__file__).resolve().parent
TAXONOMY_FILE = BASE_DIR / "data" / "attack_tools.yaml"


def main() -> None:
    model = Model()

    tool = model.add_entity(
        AttackTool(
            name="Cobalt Strike",
            taxonomy_ref="attackTools:cobaltStrike",
            tool_type="command_and_control",
        )
    )

    print(f"Created {tool.type}: {tool.name}")
    print(f"Taxonomy reference: {tool.taxonomy_ref}")

    if TaxonomyRegistry is None:
        print("TaxonomyRegistry is not available in this package version.")
        print(f"Example taxonomy file: {TAXONOMY_FILE}")
        return

    registry = TaxonomyRegistry()
    registry.load_yaml(TAXONOMY_FILE)
    report = model.validate_taxonomies(registry)
    print(f"Taxonomy validation: {report.is_valid}")


if __name__ == "__main__":
    main()
