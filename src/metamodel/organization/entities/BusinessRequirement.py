from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class BusinessRequirement(BaseEntity):
    """Represents the BusinessRequirement entity from the metamodel."""

    _domain_attributes = ('priority',)

    def __init__(
        self,
        name: str,
        description: str | None = None,
        priority: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._priority: str | None
        self.priority = priority

    @property
    def priority(self) -> str | None:
        return self._priority

    @priority.setter
    def priority(self, value: str | None) -> None:
        self._priority = require_optional_str(value, "priority")
