"""Command-line interface: ``metamodel <command> ...`` (see ``metamodel --help``)."""
from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version

from metamodel.cli import convertCommand, inspectCommand, neo4jCommand, schemaCommand, validateCommand
from metamodel.cli._common import ERRORS, fail

COMMANDS = (validateCommand, inspectCommand, convertCommand, schemaCommand, neo4jCommand)


def _version() -> str:
    try:
        return version("cti-feasibility-metamodel")
    except PackageNotFoundError:
        return "unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="metamodel", description="CTI feasibility metamodel tools.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {_version()}")
    parser.add_argument("--traceback", action="store_true", help="show the full traceback on errors")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in COMMANDS:
        command.register(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except ERRORS as exc:
        if args.traceback:
            raise
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
