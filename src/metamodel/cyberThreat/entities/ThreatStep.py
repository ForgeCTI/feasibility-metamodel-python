from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_int, require_optional_list_str, require_optional_str


class ThreatStep(BaseEntity):
    """Represents the ThreatStep entity from the metamodel."""

    _domain_attributes = ('sequence_index', 'phase', 'objective', 'preconditions', 'postconditions')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        sequence_index: int | None = None,
        phase: str | None = None,
        objective: str | None = None,
        preconditions: list[str] | None = None,
        postconditions: list[str] | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._sequence_index: int | None
        self._phase: str | None
        self._objective: str | None
        self._preconditions: list[str]
        self._postconditions: list[str]
        self.sequence_index = sequence_index
        self.phase = phase
        self.objective = objective
        self.preconditions = preconditions
        self.postconditions = postconditions

    @property
    def sequence_index(self) -> int | None:
        return self._sequence_index

    @sequence_index.setter
    def sequence_index(self, value: int | None) -> None:
        self._sequence_index = require_optional_int(value, "sequence_index", minimum=0, maximum=None)

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
        return self._preconditions

    @preconditions.setter
    def preconditions(self, value: list[str] | None) -> None:
        self._preconditions = require_optional_list_str(value, "preconditions")

    @property
    def postconditions(self) -> list[str]:
        return self._postconditions

    @postconditions.setter
    def postconditions(self, value: list[str] | None) -> None:
        self._postconditions = require_optional_list_str(value, "postconditions")

