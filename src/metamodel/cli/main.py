from __future__ import annotations

import argparse
import json

from metamodel.io.jsonParser import loadJsonScenario
from metamodel.io.yamlParser import loadYamlScenario


def _load(path: str):
    if path.endswith((".yaml", ".yml")):
        return loadYamlScenario(path)
    return loadJsonScenario(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="metamodel")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate a scenario file.")
    validate.add_argument("path")

    inspect = sub.add_parser("inspect", help="Print scenario summary.")
    inspect.add_argument("path")

    convert = sub.add_parser("convert", help="Convert scenario to JSON.")
    convert.add_argument("path")

    args = parser.parse_args(argv)
    model = _load(args.path)

    if args.command == "validate":
        report = model.validate()
        for message in report.messages:
            print(f"[{message.severity}] {message.validator}: {message.message}")
        return 0 if report.is_valid else 1

    if args.command == "inspect":
        print(f"Entities: {len(model.entities)}")
        print(f"Relationships: {len(model.relationships)}")
        return 0

    if args.command == "convert":
        print(json.dumps(model.to_dict(), indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
