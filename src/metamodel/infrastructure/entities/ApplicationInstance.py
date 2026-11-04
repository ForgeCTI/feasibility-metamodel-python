from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class ApplicationInstance(BaseEntity):
    """Represents the ApplicationInstance entity from the metamodel."""

    _domain_attributes = ('version', 'runtime_state')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        version: str | None = None,
        runtime_state: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._version: str | None
        self._runtime_state: str | None
        self.version = version
        self.runtime_state = runtime_state

    @property
    def version(self) -> str | None:
        return self._version

    @version.setter
    def version(self, value: str | None) -> None:
        self._version = require_optional_str(value, "version")

    @property
    def runtime_state(self) -> str | None:
        return self._runtime_state

    @runtime_state.setter
    def runtime_state(self, value: str | None) -> None:
        self._runtime_state = require_allowed(
            require_optional_str(value, "runtime_state"),
            "runtime_state",
            {None, 'running', 'stopped', 'disabled', 'unknown'},
        )
