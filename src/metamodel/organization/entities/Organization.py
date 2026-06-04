from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Organization(BaseEntity):
    """Represents the Organization entity from the metamodel."""

    _domain_attributes = ('legal_name', 'short_name', 'website', 'organization_size', 'criticality', 'maturity_level')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        legal_name: str | None = None,
        short_name: str | None = None,
        website: str | None = None,
        organization_size: str | None = None,
        criticality: str | None = None,
        maturity_level: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._legal_name: str | None
        self._short_name: str | None
        self._website: str | None
        self._organization_size: str | None
        self._criticality: str | None
        self._maturity_level: str | None
        self.legal_name = legal_name
        self.short_name = short_name
        self.website = website
        self.organization_size = organization_size
        self.criticality = criticality
        self.maturity_level = maturity_level

    @property
    def legal_name(self) -> str | None:
        return self._legal_name

    @legal_name.setter
    def legal_name(self, value: str | None) -> None:
        self._legal_name = require_optional_str(value, "legal_name")

    @property
    def short_name(self) -> str | None:
        return self._short_name

    @short_name.setter
    def short_name(self, value: str | None) -> None:
        self._short_name = require_optional_str(value, "short_name")

    @property
    def website(self) -> str | None:
        return self._website

    @website.setter
    def website(self, value: str | None) -> None:
        self._website = require_optional_str(value, "website")

    @property
    def organization_size(self) -> str | None:
        return self._organization_size

    @organization_size.setter
    def organization_size(self, value: str | None) -> None:
        self._organization_size = require_allowed(require_optional_str(value, "organization_size"), "organization_size", {None, 'medium', 'enterprise', 'small', 'micro', 'large'})

    @property
    def criticality(self) -> str | None:
        return self._criticality

    @criticality.setter
    def criticality(self, value: str | None) -> None:
        self._criticality = require_allowed(require_optional_str(value, "criticality"), "criticality", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def maturity_level(self) -> str | None:
        return self._maturity_level

    @maturity_level.setter
    def maturity_level(self, value: str | None) -> None:
        self._maturity_level = require_allowed(require_optional_str(value, "maturity_level"), "maturity_level", {None, 'defined', 'optimized', 'quantitatively_managed', 'managed', 'initial'})

