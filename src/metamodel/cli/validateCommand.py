"""metamodel validate: load a scenario and run model validation."""
from __future__ import annotations

import json

from metamodel.cli._common import add_input, load


def register(subparsers) -> None:
    parser = subparsers.add_parser("validate", help="Validate a scenario (references, types, multiplicities, semantic rules).")
    add_input(parser)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.set_defaults(handler=run)


def run(args) -> int:
    report = load(args).validate()
    failed = not report.is_valid or (args.strict and report.warnings)
    if args.json:
        print(json.dumps({
            "valid": not failed,
            "messages": [{"severity": m.severity, "validator": m.validator, "message": m.message} for m in report.messages],
        }, indent=2))
    else:
        for message in report.messages:
            print(f"[{message.severity}] {message.validator}: {message.message}")
        print(f"Valid: {not failed} ({len(report.errors)} error(s), {len(report.warnings)} warning(s))")
    return 1 if failed else 0
