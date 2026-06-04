from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_int, require_optional_str


class Port(BaseEntity):
    """Represents the Port entity from the metamodel."""

    _domain_attributes = ('number', 'protocol', 'service_name', 'state', 'exposure')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        number: int | None = None,
        protocol: str | None = None,
        service_name: str | None = None,
        state: str | None = None,
        exposure: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._number: int | None
        self._protocol: str | None
        self._service_name: str | None
        self._state: str | None
        self._exposure: str | None
        self.number = number
        self.protocol = protocol
        self.service_name = service_name
        self.state = state
        self.exposure = exposure

    @property
    def number(self) -> int | None:
        return self._number

    @number.setter
    def number(self, value: int | None) -> None:
        self._number = require_optional_int(value, "number", minimum=0, maximum=65535)

    @property
    def protocol(self) -> str | None:
        return self._protocol

    @protocol.setter
    def protocol(self, value: str | None) -> None:
        self._protocol = require_allowed(require_optional_str(value, "protocol"), "protocol", {None, 'tcp', 'udp', 'sctp', 'unknown', 'icmp'})

    @property
    def service_name(self) -> str | None:
        return self._service_name

    @service_name.setter
    def service_name(self, value: str | None) -> None:
        self._service_name = require_optional_str(value, "service_name")

    @property
    def state(self) -> str | None:
        return self._state

    @state.setter
    def state(self, value: str | None) -> None:
        self._state = require_allowed(require_optional_str(value, "state"), "state", {None, 'open', 'unknown', 'closed', 'filtered'})

    @property
    def exposure(self) -> str | None:
        return self._exposure

    @exposure.setter
    def exposure(self, value: str | None) -> None:
        self._exposure = require_allowed(require_optional_str(value, "exposure"), "exposure", {None, 'dmz', 'external', 'internal', 'unknown'})

