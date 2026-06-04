from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class Asset(BaseEntity):
    """Represents the Asset entity from the metamodel."""

    _domain_attributes = ('asset_type', 'business_value', 'criticality', 'owner')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        asset_type: str | None = None,
        business_value: str | None = None,
        criticality: str | None = None,
        owner: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._asset_type: str | None
        self._business_value: str | None
        self._criticality: str | None
        self._owner: str | None
        self.asset_type = asset_type
        self.business_value = business_value
        self.criticality = criticality
        self.owner = owner

    @property
    def asset_type(self) -> str | None:
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value: str | None) -> None:
        self._asset_type = require_optional_str(value, "asset_type")

    @property
    def business_value(self) -> str | None:
        return self._business_value

    @business_value.setter
    def business_value(self, value: str | None) -> None:
        self._business_value = require_allowed(require_optional_str(value, "business_value"), "business_value", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def criticality(self) -> str | None:
        return self._criticality

    @criticality.setter
    def criticality(self, value: str | None) -> None:
        self._criticality = require_allowed(require_optional_str(value, "criticality"), "criticality", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def owner(self) -> str | None:
        return self._owner

    @owner.setter
    def owner(self, value: str | None) -> None:
        self._owner = require_optional_str(value, "owner")

