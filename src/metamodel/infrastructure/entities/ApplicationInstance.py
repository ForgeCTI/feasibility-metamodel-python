from __future__ import annotations

from metamodel.infrastructure.entities.Code import Code
from metamodel.core.ValidationUtils import (
    require_optional_str,
)


class ApplicationInstance(Code):
    """Instance of an Application running on a node."""

    _domain_attributes = Code._domain_attributes + ('runtime_state', 'role')
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        runtime_state: str | None = None,
        role: str | None = None,
        version: str | None = None,
        language: str | None = None,
        repository_url: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source, version=version, language=language, repository_url=repository_url)
        self._runtime_state: str | None
        self._role: str | None
        self.runtime_state = runtime_state
        self.role = role


    @property
    def runtime_state(self) -> str | None:
        return self._runtime_state

    @runtime_state.setter
    def runtime_state(self, value: str | None) -> None:
        self._runtime_state = require_optional_str(value, "runtime_state")

    @property
    def role(self) -> str | None:
        return self._role

    @role.setter
    def role(self, value: str | None) -> None:
        self._role = require_optional_str(value, "role")
