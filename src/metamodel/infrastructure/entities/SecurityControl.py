from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_allowed,
    require_optional_str,
)


class SecurityControl(BaseEntity):
    """Deployed defensive measure, e.g. the MFA enforced on the mailbox accounts."""

    _domain_attributes = ('status',)
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        status: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._status: str | None
        self.status = status


    @property
    def status(self) -> str | None:
        return self._status

    @status.setter
    def status(self, value: str | None) -> None:
        self._status = require_allowed(
            require_optional_str(value, "status"),
            "status",
            {None, 'enforced', 'audit', 'disabled', 'unknown'},
        )
