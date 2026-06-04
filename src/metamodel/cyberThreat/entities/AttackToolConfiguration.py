from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_bool, require_optional_dict, require_optional_str


class AttackToolConfiguration(BaseEntity):
    """Represents the AttackToolConfiguration entity from the metamodel."""

    _domain_attributes = ('configuration_type', 'parameters', 'persistence_enabled', 'stealth_level')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        configuration_type: str | None = None,
        parameters: dict | None = None,
        persistence_enabled: bool | None = None,
        stealth_level: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._configuration_type: str | None
        self._parameters: dict
        self._persistence_enabled: bool | None
        self._stealth_level: str | None
        self.configuration_type = configuration_type
        self.parameters = parameters
        self.persistence_enabled = persistence_enabled
        self.stealth_level = stealth_level

    @property
    def configuration_type(self) -> str | None:
        return self._configuration_type

    @configuration_type.setter
    def configuration_type(self, value: str | None) -> None:
        self._configuration_type = require_optional_str(value, "configuration_type")

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, value: dict | None) -> None:
        self._parameters = require_optional_dict(value, "parameters")

    @property
    def persistence_enabled(self) -> bool | None:
        return self._persistence_enabled

    @persistence_enabled.setter
    def persistence_enabled(self, value: bool | None) -> None:
        self._persistence_enabled = require_optional_bool(value, "persistence_enabled")

    @property
    def stealth_level(self) -> str | None:
        return self._stealth_level

    @stealth_level.setter
    def stealth_level(self, value: str | None) -> None:
        self._stealth_level = require_allowed(require_optional_str(value, "stealth_level"), "stealth_level", {None, 'high', 'medium', 'unknown', 'low'})

