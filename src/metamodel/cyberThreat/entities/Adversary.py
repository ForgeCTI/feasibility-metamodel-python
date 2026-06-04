from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Adversary(BaseEntity):
    """Represents the Adversary entity from the metamodel."""

    _domain_attributes = ('objective', 'intent', 'capability_level')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        objective: str | None = None,
        intent: str | None = None,
        capability_level: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._objective: str | None
        self._intent: str | None
        self._capability_level: str | None
        self.objective = objective
        self.intent = intent
        self.capability_level = capability_level

    @property
    def objective(self) -> str | None:
        return self._objective

    @objective.setter
    def objective(self, value: str | None) -> None:
        self._objective = require_optional_str(value, "objective")

    @property
    def intent(self) -> str | None:
        return self._intent

    @intent.setter
    def intent(self, value: str | None) -> None:
        self._intent = require_optional_str(value, "intent")

    @property
    def capability_level(self) -> str | None:
        return self._capability_level

    @capability_level.setter
    def capability_level(self, value: str | None) -> None:
        self._capability_level = require_allowed(require_optional_str(value, "capability_level"), "capability_level", {None, 'high', 'medium', 'advanced', 'unknown', 'low'})

