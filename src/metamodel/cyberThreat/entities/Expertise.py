from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class Expertise(BaseEntity):
    """Represents the Expertise entity from the metamodel."""

    _domain_attributes = ('level', 'domain')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        level: str | None = None,
        domain: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._level: str | None
        self._domain: str | None
        self.level = level
        self.domain = domain

    @property
    def level(self) -> str | None:
        return self._level

    @level.setter
    def level(self, value: str | None) -> None:
        self._level = require_optional_str(value, "level")

    @property
    def domain(self) -> str | None:
        return self._domain

    @domain.setter
    def domain(self, value: str | None) -> None:
        self._domain = require_optional_str(value, "domain")
