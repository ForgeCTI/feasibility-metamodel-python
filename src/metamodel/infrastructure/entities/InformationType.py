from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class InformationType(BaseEntity):
    """Represents the InformationType entity from the metamodel."""

    _domain_attributes = ('category',)

    def __init__(
        self,
        name: str,
        description: str | None = None,
        category: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._category: str | None
        self.category = category

    @property
    def category(self) -> str | None:
        return self._category

    @category.setter
    def category(self, value: str | None) -> None:
        self._category = require_optional_str(value, "category")

