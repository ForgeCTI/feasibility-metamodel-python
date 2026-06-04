from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class AssetSecurityRequirement(BaseEntity):
    """Represents the AssetSecurityRequirement entity from the metamodel."""

    _domain_attributes = ('priority', 'status', 'rationale')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        rationale: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._priority: str | None
        self._status: str | None
        self._rationale: str | None
        self.rationale = rationale

    @property
    def priority(self) -> str | None:
        return self._priority

    @priority.setter
    def priority(self, value: str | None) -> None:
        self._priority = require_allowed(require_optional_str(value, "priority"), "priority", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def status(self) -> str | None:
        return self._status

    @status.setter
    def status(self, value: str | None) -> None:
        self._status = require_allowed(require_optional_str(value, "status"), "status", {None, 'implemented', 'partially_implemented', 'unknown', 'not_implemented', 'planned'})

    @property
    def rationale(self) -> str | None:
        return self._rationale

    @rationale.setter
    def rationale(self, value: str | None) -> None:
        self._rationale = require_optional_str(value, "rationale")

