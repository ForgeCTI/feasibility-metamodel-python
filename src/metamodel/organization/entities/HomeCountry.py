from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class HomeCountry(BaseEntity):
    """Represents the HomeCountry entity from the metamodel."""

    _domain_attributes = ('iso2_code', 'iso3_code', 'region')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        iso2_code: str | None = None,
        iso3_code: str | None = None,
        region: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._iso2_code: str | None
        self._iso3_code: str | None
        self._region: str | None
        self.iso2_code = iso2_code
        self.iso3_code = iso3_code
        self.region = region

    @staticmethod
    def _validate_iso_code(value: str | None, field_name: str, length: int) -> str | None:
        value = require_optional_str(value, field_name)
        if value is not None and (
            len(value) != length
            or not value.isalpha()
            or not value.isupper()
        ):
            raise ValueError(f"{field_name} must contain exactly {length} uppercase letters.")
        return value

    @property
    def iso2_code(self) -> str | None:
        return self._iso2_code

    @iso2_code.setter
    def iso2_code(self, value: str | None) -> None:
        self._iso2_code = self._validate_iso_code(value, "iso2_code", 2)

    @property
    def iso3_code(self) -> str | None:
        return self._iso3_code

    @iso3_code.setter
    def iso3_code(self, value: str | None) -> None:
        self._iso3_code = self._validate_iso_code(value, "iso3_code", 3)

    @property
    def region(self) -> str | None:
        return self._region

    @region.setter
    def region(self, value: str | None) -> None:
        self._region = require_optional_str(value, "region")
