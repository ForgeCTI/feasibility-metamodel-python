from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_allowed,
    require_optional_bool,
    require_optional_str,
)


class Account(BaseEntity):
    """Identity through which a user authenticates; it grants access to nodes and resources."""

    _domain_attributes = ('kind', 'username', 'enabled')
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        kind: str | None = None,
        username: str | None = None,
        enabled: bool | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._kind: str | None
        self._username: str | None
        self._enabled: bool | None
        self.kind = kind
        self.username = username
        self.enabled = enabled


    @property
    def kind(self) -> str | None:
        return self._kind

    @kind.setter
    def kind(self, value: str | None) -> None:
        self._kind = require_allowed(
            require_optional_str(value, "kind"),
            "kind",
            {None, 'local', 'domain', 'cloud', 'service', 'other'},
        )

    @property
    def username(self) -> str | None:
        return self._username

    @username.setter
    def username(self, value: str | None) -> None:
        self._username = require_optional_str(value, "username")

    @property
    def enabled(self) -> bool | None:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        self._enabled = require_optional_bool(value, "enabled")
