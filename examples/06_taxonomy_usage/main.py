"""Example 06: taxonomy usage.

This example loads a small local attack-tool taxonomy from YAML and uses a
taxonomy reference when creating an AttackTool entity.
"""

from pathlib import Path

import yaml

from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.AttackTool import AttackTool


BASE_DIR = Path(__file__).resolve().parent
TAXONOMY_FILE = BASE_DIR / "data" / "attack_tools.yaml"


def load_attack_tool_taxonomy(path: Path) -> dict:
    """Load the local attack-tool taxonomy file."""
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError("The taxonomy file must contain a YAML mapping.")

    if "taxonomy" not in data:
        raise ValueError("The taxonomy file must contain a 'taxonomy' section.")

    if "concepts" not in data:
        raise ValueError("The taxonomy file must contain a 'concepts' list.")

    return data


def main() -> None:
    taxonomy = load_attack_tool_taxonomy(TAXONOMY_FILE)

    cobalt_strike = next(
        concept for concept in taxonomy["concepts"]
        if concept["id"] == "cobaltStrike"
    )

    model = Model()

    attack_tool = model.add_entity(
        AttackTool(
            name=cobalt_strike["name"],
            description=cobalt_strike.get("description"),
            taxonomy_ref=f"{taxonomy['taxonomy']['id']}:{cobalt_strike['id']}",
            aliases=cobalt_strike.get("aliases", []),
            tool_type=cobalt_strike.get("category"),
            capabilities=cobalt_strike.get("capabilities", []),
            source=taxonomy["taxonomy"].get("source"),
        )
    )

    print("Loaded taxonomy:", taxonomy["taxonomy"]["id"])
    print("Created entity:", attack_tool.type)
    print("Name:", attack_tool.name)
    print("Taxonomy reference:", attack_tool.taxonomy_ref)


if __name__ == "__main__":
    main()