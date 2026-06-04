from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str, require_optional_taxonomy_ref


class HomeCountry(BaseEntity):
    """Represents the HomeCountry entity from the metamodel."""

    _domain_attributes = ('iso2_code', 'iso3_code', 'region', 'taxonomy_ref')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        iso2_code: str | None = None,
        iso3_code: str | None = None,
        region: str | None = None,
        taxonomy_ref: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._iso2_code: str | None
        self._iso3_code: str | None
        self._region: str | None
        self._taxonomy_ref: str | None
        self.iso2_code = iso2_code
        self.iso3_code = iso3_code
        self.region = region
        self.taxonomy_ref = taxonomy_ref

    @property
    def iso2_code(self) -> str | None:
        return self._iso2_code

    @iso2_code.setter
    def iso2_code(self, value: str | None) -> None:
        self._iso2_code = require_optional_str(value, "iso2_code")

    @property
    def iso3_code(self) -> str | None:
        return self._iso3_code

    @iso3_code.setter
    def iso3_code(self, value: str | None) -> None:
        self._iso3_code = require_optional_str(value, "iso3_code")

    @property
    def region(self) -> str | None:
        return self._region

    @region.setter
    def region(self, value: str | None) -> None:
        self._region = require_optional_str(value, "region")

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

