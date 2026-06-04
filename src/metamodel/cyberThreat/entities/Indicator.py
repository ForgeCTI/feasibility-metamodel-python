from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_date_string, require_optional_str


class Indicator(BaseEntity):
    """Represents the Indicator entity from the metamodel."""

    _domain_attributes = ('indicator_type', 'value', 'pattern', 'valid_from', 'valid_until')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        indicator_type: str | None = None,
        value: str | None = None,
        pattern: str | None = None,
        valid_from: str | None = None,
        valid_until: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._indicator_type: str | None
        self._value: str | None
        self._pattern: str | None
        self._valid_from: str | None
        self._valid_until: str | None
        self.indicator_type = indicator_type
        self.value = value
        self.pattern = pattern
        self.valid_from = valid_from
        self.valid_until = valid_until

    @property
    def indicator_type(self) -> str | None:
        return self._indicator_type

    @indicator_type.setter
    def indicator_type(self, value: str | None) -> None:
        self._indicator_type = require_allowed(require_optional_str(value, "indicator_type"), "indicator_type", {None, 'file', 'mutex', 'email', 'registry', 'url', 'ip', 'unknown', 'other', 'domain', 'hash'})

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, value: str | None) -> None:
        self._value = require_optional_str(value, "value")

    @property
    def pattern(self) -> str | None:
        return self._pattern

    @pattern.setter
    def pattern(self, value: str | None) -> None:
        self._pattern = require_optional_str(value, "pattern")

    @property
    def valid_from(self) -> str | None:
        return self._valid_from

    @valid_from.setter
    def valid_from(self, value: str | None) -> None:
        self._valid_from = require_optional_date_string(value, "valid_from")

    @property
    def valid_until(self) -> str | None:
        return self._valid_until

    @valid_until.setter
    def valid_until(self, value: str | None) -> None:
        self._valid_until = require_optional_date_string(value, "valid_until")

