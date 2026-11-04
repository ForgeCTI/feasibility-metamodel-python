from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_str


class InternationalBody(BaseEntity):
    """Represents the InternationalBody entity from the metamodel."""

    _domain_attributes = ('acronym',)

    def __init__(
        self,
        name: str,
        acronym: str,
        description: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._acronym: str
        self.acronym = acronym

    @property
    def acronym(self) -> str:
        return self._acronym

    @acronym.setter
    def acronym(self, value: str) -> None:
        self._acronym = require_str(value, "acronym")
