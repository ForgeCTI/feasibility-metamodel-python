from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str, require_optional_taxonomy_ref


class Expertise(BaseEntity):
    """Represents the Expertise entity from the metamodel."""

    _domain_attributes = ('level', 'domain', 'taxonomy_ref')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        level: str | None = None,
        domain: str | None = None,
        taxonomy_ref: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._level: str | None
        self._domain: str | None
        self._taxonomy_ref: str | None
        self.level = level
        self.domain = domain
        self.taxonomy_ref = taxonomy_ref

    @property
    def level(self) -> str | None:
        return self._level

    @level.setter
    def level(self, value: str | None) -> None:
        self._level = require_allowed(require_optional_str(value, "level"), "level", {None, 'high', 'medium', 'unknown', 'expert', 'low'})

    @property
    def domain(self) -> str | None:
        return self._domain

    @domain.setter
    def domain(self, value: str | None) -> None:
        self._domain = require_optional_str(value, "domain")

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

