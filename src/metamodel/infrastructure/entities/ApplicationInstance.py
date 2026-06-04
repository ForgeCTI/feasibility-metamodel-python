from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class ApplicationInstance(BaseEntity):
    """Represents the ApplicationInstance entity from the metamodel."""

    _domain_attributes = ('version', 'install_path', 'runtime_state', 'exposure')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        version: str | None = None,
        install_path: str | None = None,
        runtime_state: str | None = None,
        exposure: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._version: str | None
        self._install_path: str | None
        self._runtime_state: str | None
        self._exposure: str | None
        self.version = version
        self.install_path = install_path
        self.runtime_state = runtime_state
        self.exposure = exposure

    @property
    def version(self) -> str | None:
        return self._version

    @version.setter
    def version(self, value: str | None) -> None:
        self._version = require_optional_str(value, "version")

    @property
    def install_path(self) -> str | None:
        return self._install_path

    @install_path.setter
    def install_path(self, value: str | None) -> None:
        self._install_path = require_optional_str(value, "install_path")

    @property
    def runtime_state(self) -> str | None:
        return self._runtime_state

    @runtime_state.setter
    def runtime_state(self, value: str | None) -> None:
        self._runtime_state = require_allowed(require_optional_str(value, "runtime_state"), "runtime_state", {None, 'running', 'stopped', 'disabled', 'unknown'})

    @property
    def exposure(self) -> str | None:
        return self._exposure

    @exposure.setter
    def exposure(self, value: str | None) -> None:
        self._exposure = require_allowed(require_optional_str(value, "exposure"), "exposure", {None, 'dmz', 'external', 'internal', 'unknown'})

