from __future__ import annotations

import sys

from metamodel.core.Exceptions import MetamodelError
from metamodel.io.formats import FORMATS_IN, loadModel


def add_input(parser, *, name: str = "path") -> None:
    parser.add_argument(name, help="scenario file (json, yaml, graphml, STIX bundle, draw.io) or CSV directory")
    parser.add_argument("--from", dest="input_format", choices=FORMATS_IN, help="input format (default: from the extension)")
    parser.add_argument("--lenient", action="store_true", help="skip unknown types and attributes instead of failing")


def load(args):
    return loadModel(args.path, args.input_format, strict=not args.lenient)


def fail(message: str, code: int = 2) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


ERRORS = (MetamodelError, OSError, ValueError, TypeError, ImportError, KeyError)
