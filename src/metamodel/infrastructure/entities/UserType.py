from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class UserType(BaseEntity):
    """Represents the UserType entity from the metamodel."""

    _domain_attributes = ('privilege_level',)

    def __init__(
        self,
        name: str,
        description: str | None = None,
        privilege_level: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._privilege_level: str | None
        self.privilege_level = privilege_level

    @property
    def privilege_level(self) -> str | None:
        return self._privilege_level

    @privilege_level.setter
    def privilege_level(self, value: str | None) -> None:
        self._privilege_level = require_optional_str(value, "privilege_level")
