from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class Information(BaseEntity):
    """Represents the Information entity from the metamodel."""

    _domain_attributes = ('format',)

    def __init__(
        self,
        name: str,
        description: str | None = None,
        format: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._format: str | None
        self.format = format

    @property
    def format(self) -> str | None:
        return self._format

    @format.setter
    def format(self, value: str | None) -> None:
        self._format = require_optional_str(value, "format")
