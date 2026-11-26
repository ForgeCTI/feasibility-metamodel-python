from __future__ import annotations

import json
from pathlib import Path

from metamodel.core.Factory import Factory
from metamodel.core.Model import Model
from metamodel.io.serialization import ParseResult, data_to_model


def parseScenario(data: dict, *, factory: Factory | None = None, strict: bool = True) -> Model:
    """Build a Model from scenario data (see ``metamodel.io.serialization``)."""
    return data_to_model(data, factory=factory, strict=strict).model


def parseScenarioWithReport(data: dict, *, factory: Factory | None = None, strict: bool = False) -> ParseResult:
    """Like ``parseScenario`` but returns the warnings collected while parsing."""
    return data_to_model(data, factory=factory, strict=strict)


def loadsJsonScenario(text: str, *, strict: bool = True) -> Model:
    return parseScenario(json.loads(text), strict=strict)


def loadJsonScenario(path: str | Path, *, strict: bool = True) -> Model:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return parseScenario(data, strict=strict)
