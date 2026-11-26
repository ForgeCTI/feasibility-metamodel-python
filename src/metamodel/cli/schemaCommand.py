"""metamodel schema: describe the entities and relationships of the metamodel."""
from __future__ import annotations

import json

from metamodel.core.Registry import Registry
from metamodel.core.Schema import describe_registry


def register(subparsers) -> None:
    parser = subparsers.add_parser("schema", help="List entity and relationship types of the metamodel.")
    parser.add_argument("name", nargs="?", help="show only this entity or relationship (class name or label)")
    parser.add_argument("--json", action="store_true", help="print the schema as JSON")
    parser.set_defaults(handler=run)


def run(args) -> int:
    schema = describe_registry(Registry.load_default())
    if args.name:
        schema = {
            "entities": [e for e in schema["entities"] if e["name"] == args.name],
            "relationships": [r for r in schema["relationships"]
                              if args.name in (r["name"], r["label"], r["source"], r["target"])],
        }
        if not schema["entities"] and not schema["relationships"]:
            print(f"error: unknown entity or relationship {args.name!r}.")
            return 2
    if args.json:
        print(json.dumps(schema, indent=2))
        return 0
    if schema["entities"]:
        print("Entities:")
        for e in schema["entities"]:
            sup = f" <: {e['superclass']}" if e["superclass"] else ""
            attrs = ", ".join(f"{k}: {v}" for k, v in e["attributes"].items())
            print(f"  {e['name']}{sup}  [{e['domain']}, {e['knowledge_class']}]")
            if attrs:
                print(f"      {attrs}")
    if schema["relationships"]:
        print("Relationships:")
        for r in schema["relationships"]:
            attrs = "".join(f" {{{k}: {v}}}" for k, v in r["attributes"].items())
            print(f"  {r['source']} [{r['source_cardinality']}] --{r['label']}--> [{r['target_cardinality']}] {r['target']}"
                  f"   ({r['name']}){attrs}")
    return 0
