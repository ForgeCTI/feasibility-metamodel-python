from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_optional_date_string,
    require_date_order,
    require_optional_str,
)


class Threat(BaseEntity):
    """Represents the Threat entity from the metamodel."""

    _domain_attributes = ('objective', 'first_seen', 'last_seen')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        objective: str | None = None,
        first_seen: str | None = None,
        last_seen: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)

        self._objective: str | None
        self._first_seen: str | None = None
        self._last_seen: str | None = None

        self.objective = objective
        self.first_seen = first_seen
        self.last_seen = last_seen

    @property
    def objective(self) -> str | None:
        return self._objective

    @objective.setter
    def objective(self, value: str | None) -> None:
        self._objective = require_optional_str(value, "objective")

    @property
    def first_seen(self) -> str | None:
        return self._first_seen

    @first_seen.setter
    def first_seen(self, value: str | None) -> None:
        value = require_optional_date_string(value, "first_seen")
        require_date_order(value, self._last_seen)
        self._first_seen = value

    @property
    def last_seen(self) -> str | None:
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value: str | None) -> None:
        value = require_optional_date_string(value, "last_seen")
        require_date_order(self._first_seen, value)
        self._last_seen = value
