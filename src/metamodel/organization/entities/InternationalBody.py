from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str, require_optional_taxonomy_ref


class InternationalBody(BaseEntity):
    """Represents the InternationalBody entity from the metamodel."""

    _domain_attributes = ('acronym', 'taxonomy_ref')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        acronym: str | None = None,
        taxonomy_ref: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._acronym: str | None
        self._taxonomy_ref: str | None
        self.acronym = acronym
        self.taxonomy_ref = taxonomy_ref

    @property
    def acronym(self) -> str | None:
        return self._acronym

    @acronym.setter
    def acronym(self, value: str | None) -> None:
        self._acronym = require_optional_str(value, "acronym")

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

