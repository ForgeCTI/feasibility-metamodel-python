from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class BusinessRequirement(BaseEntity):
    """Represents the BusinessRequirement entity from the metamodel."""

    _domain_attributes = ('priority', 'rationale', 'owner')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        priority: str | None = None,
        rationale: str | None = None,
        owner: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._priority: str | None
        self._rationale: str | None
        self._owner: str | None
        self.priority = priority
        self.rationale = rationale
        self.owner = owner

    @property
    def priority(self) -> str | None:
        return self._priority

    @priority.setter
    def priority(self, value: str | None) -> None:
        self._priority = require_allowed(require_optional_str(value, "priority"), "priority", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def rationale(self) -> str | None:
        return self._rationale

    @rationale.setter
    def rationale(self, value: str | None) -> None:
        self._rationale = require_optional_str(value, "rationale")

    @property
    def owner(self) -> str | None:
        return self._owner

    @owner.setter
    def owner(self, value: str | None) -> None:
        self._owner = require_optional_str(value, "owner")

