from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Information(BaseEntity):
    """Represents the Information entity from the metamodel."""

    _domain_attributes = ('classification', 'sensitivity', 'format')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        classification: str | None = None,
        sensitivity: str | None = None,
        format: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._classification: str | None
        self._sensitivity: str | None
        self._format: str | None
        self.classification = classification
        self.sensitivity = sensitivity
        self.format = format

    @property
    def classification(self) -> str | None:
        return self._classification

    @classification.setter
    def classification(self, value: str | None) -> None:
        self._classification = require_allowed(require_optional_str(value, "classification"), "classification", {None, 'internal', 'confidential', 'secret', 'unknown', 'public', 'restricted'})

    @property
    def sensitivity(self) -> str | None:
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value: str | None) -> None:
        self._sensitivity = require_allowed(require_optional_str(value, "sensitivity"), "sensitivity", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def format(self) -> str | None:
        return self._format

    @format.setter
    def format(self, value: str | None) -> None:
        self._format = require_optional_str(value, "format")

