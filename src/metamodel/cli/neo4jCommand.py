"""metamodel neo4j: export a scenario to Neo4j or import it back."""
from __future__ import annotations

import os
import sys

from metamodel.cli._common import add_input, load


def _connection(parser) -> None:
    parser.add_argument("--uri", default=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
                        help="Neo4j URI (default: $NEO4J_URI or bolt://localhost:7687)")
    parser.add_argument("--user", default=os.environ.get("NEO4J_USER", "neo4j"), help="user (default: $NEO4J_USER or neo4j)")
    parser.add_argument("--password", default=os.environ.get("NEO4J_PASSWORD"),
                        help="password (default: $NEO4J_PASSWORD)")
    parser.add_argument("--database", default=os.environ.get("NEO4J_DATABASE"), help="database name (default: server default)")


def register(subparsers) -> None:
    parser = subparsers.add_parser("neo4j", help="Export a scenario to Neo4j or import it from Neo4j.")
    actions = parser.add_subparsers(dest="neo4j_action", required=True)

    export = actions.add_parser("export", help="Write a scenario to Neo4j.")
    add_input(export)
    _connection(export)
    export.add_argument("--clear", action="store_true", help="delete all Entity nodes before writing")
    export.set_defaults(handler=run_export)

    imp = actions.add_parser("import", help="Read Entity nodes and their relationships into a scenario file.")
    _connection(imp)
    imp.add_argument("-o", "--output", required=True, help="output file or CSV directory")
    imp.add_argument("--to", dest="output_format", help="output format (default: from -o)")
    imp.set_defaults(handler=run_import)


def _password(args) -> str:
    if args.password is None:
        raise ValueError("no password: use --password or set NEO4J_PASSWORD.")
    return args.password


def run_export(args) -> int:
    from metamodel.adapters.neo4jAdapter import exportToNeo4j
    model = load(args)
    counts = exportToNeo4j(model, args.uri, args.user, _password(args), database=args.database, clear=args.clear)
    print(f"Exported {counts['nodes']} nodes and {counts['relationships']} relationships to {args.uri}.", file=sys.stderr)
    return 0


def run_import(args) -> int:
    from metamodel.adapters.neo4jAdapter import importFromNeo4j
    from metamodel.io.formats import saveModel
    model = importFromNeo4j(args.uri, args.user, _password(args), database=args.database)
    saveModel(model, args.output, args.output_format)
    print(f"Imported {len(model.entities)} entities and {len(model.relationships)} relationships into {args.output}.",
          file=sys.stderr)
    return 0
