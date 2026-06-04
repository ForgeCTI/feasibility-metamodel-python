from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str, require_optional_taxonomy_ref


class SecurityRequirement(BaseEntity):
    """Represents the SecurityRequirement entity from the metamodel."""

    _domain_attributes = ('requirement_type', 'taxonomy_ref', 'control_family')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        requirement_type: str | None = None,
        taxonomy_ref: str | None = None,
        control_family: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._requirement_type: str | None
        self._taxonomy_ref: str | None
        self._control_family: str | None
        self.requirement_type = requirement_type
        self.taxonomy_ref = taxonomy_ref
        self.control_family = control_family

    @property
    def requirement_type(self) -> str | None:
        return self._requirement_type

    @requirement_type.setter
    def requirement_type(self, value: str | None) -> None:
        self._requirement_type = require_optional_str(value, "requirement_type")

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

    @property
    def control_family(self) -> str | None:
        return self._control_family

    @control_family.setter
    def control_family(self, value: str | None) -> None:
        self._control_family = require_optional_str(value, "control_family")

