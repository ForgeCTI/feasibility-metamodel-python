"""metamodel convert: convert a scenario between formats."""
from __future__ import annotations

import sys

from metamodel.cli._common import add_input, load
from metamodel.io.formats import FORMATS_OUT, detect_format, saveModel

STDOUT_FORMATS = ("json", "yaml", "cypher")


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "convert",
        help="Convert a scenario between json, yaml, csv, graphml, and cypher.",
        description="Without -o, json/yaml/cypher are printed to standard output.",
    )
    add_input(parser)
    parser.add_argument("-o", "--output", help="output file, or directory for csv")
    parser.add_argument("--to", dest="output_format", choices=FORMATS_OUT, help="output format (default: from -o, else json)")
    parser.set_defaults(handler=run)


def run(args) -> int:
    model = load(args)
    fmt = args.output_format or (detect_format(args.output) if args.output else "json")
    if args.output:
        saveModel(model, args.output, fmt)
        print(f"Wrote {len(model.entities)} entities and {len(model.relationships)} relationships to {args.output} ({fmt}).",
              file=sys.stderr)
        return 0
    if fmt not in STDOUT_FORMATS:
        print(f"error: format {fmt!r} requires -o/--output.", file=sys.stderr)
        return 2
    if fmt == "json":
        from metamodel.io.jsonSerializer import dumpsJsonScenario
        sys.stdout.write(dumpsJsonScenario(model) + "\n")
    elif fmt == "yaml":
        from metamodel.io.yamlSerializer import dumpsYamlScenario
        sys.stdout.write(dumpsYamlScenario(model))
    else:
        from metamodel.adapters.neo4jAdapter import toCypherScript
        sys.stdout.write(toCypherScript(model))
    return 0
