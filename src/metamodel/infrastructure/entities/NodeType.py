from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str, require_optional_taxonomy_ref


class NodeType(BaseEntity):
    """Represents the NodeType entity from the metamodel."""

    _domain_attributes = ('taxonomy_ref', 'category')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        taxonomy_ref: str | None = None,
        category: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._taxonomy_ref: str | None
        self._category: str | None
        self.taxonomy_ref = taxonomy_ref
        self.category = category

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

    @property
    def category(self) -> str | None:
        return self._category

    @category.setter
    def category(self, value: str | None) -> None:
        self._category = require_optional_str(value, "category")

