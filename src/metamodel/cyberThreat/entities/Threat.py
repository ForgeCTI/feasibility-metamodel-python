from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_date_string, require_optional_str


class Threat(BaseEntity):
    """Represents the Threat entity from the metamodel."""

    _domain_attributes = ('objective', 'status', 'first_seen', 'last_seen')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        objective: str | None = None,
        status: str | None = None,
        first_seen: str | None = None,
        last_seen: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._objective: str | None
        self._status: str | None
        self._first_seen: str | None
        self._last_seen: str | None
        self.objective = objective
        self.status = status
        self.first_seen = first_seen
        self.last_seen = last_seen

    @property
    def objective(self) -> str | None:
        return self._objective

    @objective.setter
    def objective(self, value: str | None) -> None:
        self._objective = require_optional_str(value, "objective")

    @property
    def status(self) -> str | None:
        return self._status

    @status.setter
    def status(self, value: str | None) -> None:
        self._status = require_allowed(require_optional_str(value, "status"), "status", {None, 'observed', 'hypothetical', 'active', 'unknown', 'historical'})

    @property
    def first_seen(self) -> str | None:
        return self._first_seen

    @first_seen.setter
    def first_seen(self, value: str | None) -> None:
        self._first_seen = require_optional_date_string(value, "first_seen")

    @property
    def last_seen(self) -> str | None:
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value: str | None) -> None:
        self._last_seen = require_optional_date_string(value, "last_seen")

