from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Infrastructure(BaseEntity):
    """Represents the Infrastructure entity from the metamodel."""

    _domain_attributes = ('environment_type', 'scope')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        environment_type: str | None = None,
        scope: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._environment_type: str | None
        self._scope: str | None
        self.environment_type = environment_type
        self.scope = scope

    @property
    def environment_type(self) -> str | None:
        return self._environment_type

    @environment_type.setter
    def environment_type(self, value: str | None) -> None:
        self._environment_type = require_allowed(require_optional_str(value, "environment_type"), "environment_type", {None, 'test', 'staging', 'development', 'unknown', 'production', 'hybrid'})

    @property
    def scope(self) -> str | None:
        return self._scope

    @scope.setter
    def scope(self, value: str | None) -> None:
        self._scope = require_optional_str(value, "scope")

