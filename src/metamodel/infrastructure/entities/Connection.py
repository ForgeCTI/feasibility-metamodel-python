from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_bool, require_optional_str


class Connection(BaseEntity):
    """Represents the Connection entity from the metamodel."""

    _domain_attributes = ('protocol', 'direction', 'encrypted', 'allowed')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        protocol: str | None = None,
        direction: str | None = None,
        encrypted: bool | None = None,
        allowed: bool | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._protocol: str | None
        self._direction: str | None
        self._encrypted: bool | None
        self._allowed: bool | None
        self.protocol = protocol
        self.direction = direction
        self.encrypted = encrypted
        self.allowed = allowed

    @property
    def protocol(self) -> str | None:
        return self._protocol

    @protocol.setter
    def protocol(self, value: str | None) -> None:
        self._protocol = require_optional_str(value, "protocol")

    @property
    def direction(self) -> str | None:
        return self._direction

    @direction.setter
    def direction(self, value: str | None) -> None:
        self._direction = require_allowed(require_optional_str(value, "direction"), "direction", {None, 'outbound', 'inbound', 'unknown', 'bidirectional'})

    @property
    def encrypted(self) -> bool | None:
        return self._encrypted

    @encrypted.setter
    def encrypted(self, value: bool | None) -> None:
        self._encrypted = require_optional_bool(value, "encrypted")

    @property
    def allowed(self) -> bool | None:
        return self._allowed

    @allowed.setter
    def allowed(self, value: bool | None) -> None:
        self._allowed = require_optional_bool(value, "allowed")

