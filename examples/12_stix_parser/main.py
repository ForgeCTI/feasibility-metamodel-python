"""Example 12: STIX parser."""

from pathlib import Path
from collections import Counter

from metamodel.io.stixParser import StixParser


BASE_DIR = Path(__file__).resolve().parent
BUNDLE_FILE = BASE_DIR / "data" / "bundle.json"


def main() -> None:
    parser = StixParser()
    result = parser.load_file(BUNDLE_FILE)
    model = result.model

    entity_counts = Counter(entity.type for entity in model.entities)
    relationship_counts = Counter(
        getattr(relationship, "stix_relationship_type", relationship.type)
        for relationship in model.relationships
    )

    print("STIX parser example")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")

    print("\nEntity counts:")
    for entity_type, count in sorted(entity_counts.items()):
        print(f"- {entity_type}: {count}")

    print("\nRelationship counts:")
    for relationship_type, count in sorted(relationship_counts.items()):
        print(f"- {relationship_type}: {count}")

    print("\nParsed entities:")
    for entity in model.entities:
        stix_type = getattr(entity, "stix_type", None)
        suffix = f" [{stix_type}]" if stix_type else ""
        print(f"- {entity.type}: {entity.name}{suffix}")

    print(f"\nSkipped objects: {len(result.skipped_objects)}")
    for skipped in result.skipped_objects:
        print(f"- {skipped}")

    print(f"\nSkipped relationships: {len(result.skipped_relationships)}")
    for skipped in result.skipped_relationships:
        print(f"- {skipped}")


if __name__ == "__main__":
    main()
