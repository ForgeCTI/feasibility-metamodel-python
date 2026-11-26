"""metamodel inspect: print a summary of a scenario."""
from __future__ import annotations

import json
from collections import Counter

from metamodel.cli._common import add_input, load


def register(subparsers) -> None:
    parser = subparsers.add_parser("inspect", help="Print entity and relationship counts by type.")
    add_input(parser)
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("--entities", action="store_true", help="also list the entities")
    parser.set_defaults(handler=run)


def run(args) -> int:
    model = load(args)
    entity_counts = Counter(e.type for e in model.entities)
    rel_counts = Counter(r.type for r in model.relationships)
    if args.json:
        summary = {
            "metadata": model.metadata,
            "entities": len(model.entities),
            "relationships": len(model.relationships),
            "entity_types": dict(sorted(entity_counts.items())),
            "relationship_types": dict(sorted(rel_counts.items())),
        }
        if args.entities:
            summary["entity_list"] = [{"id": e.id, "type": e.type, "name": e.name} for e in model.entities]
        print(json.dumps(summary, indent=2))
        return 0
    if model.metadata.get("name"):
        print(f"Scenario: {model.metadata['name']}")
    print(f"Entities: {len(model.entities)}")
    for name, count in sorted(entity_counts.items()):
        print(f"  {name:28s} {count}")
    print(f"Relationships: {len(model.relationships)}")
    for name, count in sorted(rel_counts.items()):
        print(f"  {name:28s} {count}")
    if args.entities:
        print("Entity list:")
        for entity in sorted(model.entities, key=lambda e: (e.type, e.name)):
            print(f"  {entity.type:24s} {entity.id:38s} {entity.name}")
    return 0
