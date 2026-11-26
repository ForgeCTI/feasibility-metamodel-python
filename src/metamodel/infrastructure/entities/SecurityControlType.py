from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_optional_str,
)


class SecurityControlType(BaseEntity):
    """Generic type of defensive measure, e.g. phishing-resistant MFA (from D3FEND or NIST SP 800-53)."""

    _domain_attributes = ('external_id', 'catalogue')
    knowledge_class = 'concept'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        external_id: str | None = None,
        catalogue: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._external_id: str | None
        self._catalogue: str | None
        self.external_id = external_id
        self.catalogue = catalogue


    @property
    def external_id(self) -> str | None:
        return self._external_id

    @external_id.setter
    def external_id(self, value: str | None) -> None:
        self._external_id = require_optional_str(value, "external_id")

    @property
    def catalogue(self) -> str | None:
        return self._catalogue

    @catalogue.setter
    def catalogue(self, value: str | None) -> None:
        self._catalogue = require_optional_str(value, "catalogue")
