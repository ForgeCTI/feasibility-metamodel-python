from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_list_str, require_optional_str


class ThreatStep(BaseEntity):
    """Represents the ThreatStep entity from the metamodel."""

    _domain_attributes = (
        'phase',
        'objective',
        'preconditions',
        'postconditions', 'join')
    knowledge_class = 'posteriori'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        phase: str | None = None,
        objective: str | None = None,
        preconditions: list[str] | None = None,
        postconditions: list[str] | None = None,
        join: str = 'AND',
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._phase: str | None
        self._objective: str | None
        self._preconditions: list[str]
        self._postconditions: list[str]
        self.phase = phase
        self.objective = objective
        self.preconditions = preconditions
        self.postconditions = postconditions
        self._join: str
        self.join = join

    @property
    def phase(self) -> str | None:
        return self._phase

    @phase.setter
    def phase(self, value: str | None) -> None:
        self._phase = require_optional_str(value, "phase")

    @property
    def objective(self) -> str | None:
        return self._objective

    @objective.setter
    def objective(self, value: str | None) -> None:
        self._objective = require_optional_str(value, "objective")

    @property
    def preconditions(self) -> list[str]:
        return list(self._preconditions)

    @preconditions.setter
    def preconditions(self, value: list[str] | None) -> None:
        self._preconditions = require_optional_list_str(value, "preconditions")

    @property
    def postconditions(self) -> list[str]:
        return list(self._postconditions)

    @postconditions.setter
    def postconditions(self, value: list[str] | None) -> None:
        self._postconditions = require_optional_list_str(value, "postconditions")

    @property
    def join(self) -> str:
        return self._join

    @join.setter
    def join(self, value: str) -> None:
        self._join = require_allowed(value, "join", {'AND', 'OR'})
