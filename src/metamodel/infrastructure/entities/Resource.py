from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Resource(BaseEntity):
    """Represents the Resource entity from the metamodel."""

    _domain_attributes = ('resource_type', 'criticality', 'sensitivity')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        resource_type: str | None = None,
        criticality: str | None = None,
        sensitivity: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._resource_type: str | None
        self._criticality: str | None
        self._sensitivity: str | None
        self.resource_type = resource_type
        self.criticality = criticality
        self.sensitivity = sensitivity

    @property
    def resource_type(self) -> str | None:
        return self._resource_type

    @resource_type.setter
    def resource_type(self, value: str | None) -> None:
        self._resource_type = require_optional_str(value, "resource_type")

    @property
    def criticality(self) -> str | None:
        return self._criticality

    @criticality.setter
    def criticality(self, value: str | None) -> None:
        self._criticality = require_allowed(require_optional_str(value, "criticality"), "criticality", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def sensitivity(self) -> str | None:
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value: str | None) -> None:
        self._sensitivity = require_allowed(require_optional_str(value, "sensitivity"), "sensitivity", {None, 'internal', 'confidential', 'secret', 'unknown', 'public', 'restricted'})

