from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_allowed,
    require_optional_str,
)


class SecurityRequirement(BaseEntity):
    """Represents a security requirement based on the CIA triad."""

    _domain_attributes = (
        'requirement_type',
    )

    def __init__(
        self,
        name: str,
        description: str | None = None,
        requirement_type: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._requirement_type: str | None
        self.requirement_type = requirement_type

    @property
    def requirement_type(self) -> str | None:
        return self._requirement_type

    @requirement_type.setter
    def requirement_type(self, value: str | None) -> None:
        self._requirement_type = require_allowed(
            require_optional_str(value, "requirement_type"),
            "requirement_type",
            {None, "confidentiality", "integrity", "availability"}
        )
