from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str, require_optional_taxonomy_ref


class Sector(BaseEntity):
    """Represents the Sector entity from the metamodel."""

    _domain_attributes = (
        'taxonomy_ref', 
        'sector_code', 
        'sector_standard', 
        'sector_standard_version'
    )

    def __init__(
        self,
        name: str,
        description: str | None = None,
        taxonomy_ref: str | None = None,
        sector_code: str | None = None,
        sector_standard: str | None = None,
        sector_standard_version: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._taxonomy_ref: str | None = None
        self._sector_code: str | None = None
        self._sector_standard: str | None = None
        self._sector_standard_version: str | None = None 
        self.taxonomy_ref = taxonomy_ref
        self.sector_standard = sector_standard
        self.sector_code = sector_code
        self.sector_standard_version = sector_standard_version

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

    @property
    def sector_code(self) -> str | None:
        return self._sector_code

    @sector_code.setter
    def sector_code(self, value: str | None) -> None:
        value = require_optional_str(value, "sector_code")
        if value is not None and self._sector_standard is None:
            raise ValueError(
                "sector_standard must be specified when sector_code is provided."
            )
        self._sector_code = value

    @property
    def sector_standard(self) -> str | None:
        return self._sector_standard

    @sector_standard.setter
    def sector_standard(self, value: str | None) -> None:
        value = require_optional_str(value, "sector_standard")
        if value is None and (
            self._sector_code is not None 
            or self._sector_standard_version is not None
        ):
            raise ValueError(
                "sector_standard cannot be removed while sector_code " 
                "or sector_standard_version is specified."
            )
        self._sector_standard = value

    @property
    def sector_standard_version(self) -> str | None:
        return self._sector_standard_version
    
    @sector_standard_version.setter
    def sector_standard_version(self, value: str | None) -> None:
        value = require_optional_str(value, "sector_standard_version")
        if value is not None and self._sector_standard is None:
            raise ValueError(
                "sector_standard must be specified when sector_standard_version is provided."
            )
        self._sector_standard_version = value