from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Information(BaseEntity):
    """Represents the Information entity from the metamodel."""

    _domain_attributes = ('sensitivity', 'criticality', 'format')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        sensitivity: str | None = None,
        criticality: str | None = None,
        format: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._sensitivity: str | None
        self._criticality: str | None
        self._format: str | None
        self.sensitivity = sensitivity
        self.criticality = criticality
        self.format = format

    @property
    def sensitivity(self) -> str | None:
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value: str | None) -> None:
        self._sensitivity = require_allowed(
            require_optional_str(value, "sensitivity"),
            "sensitivity",
            {None, 'internal', 'confidential', 'secret', 'unknown', 'public', 'restricted'},
    )

    @property
    def criticality(self) -> str | None:
        return self._criticality

    @criticality.setter
    def criticality(self, value: str | None) -> None:
        self._criticality = require_allowed(
            require_optional_str(value, "criticality"),
            "criticality",
            {None, 'high', 'medium', 'low', 'critical'}
    )

    @property
    def format(self) -> str | None:
        return self._format

    @format.setter
    def format(self, value: str | None) -> None:
        self._format = require_optional_str(value, "format")

