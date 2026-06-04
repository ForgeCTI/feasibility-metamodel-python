from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_list_str, require_optional_str


class Node(BaseEntity):
    """Represents the Node entity from the metamodel."""

    _domain_attributes = ('hostname', 'ip_addresses', 'mac_addresses', 'fqdn', 'location', 'criticality', 'exposure')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        hostname: str | None = None,
        ip_addresses: list[str] | None = None,
        mac_addresses: list[str] | None = None,
        fqdn: str | None = None,
        location: str | None = None,
        criticality: str | None = None,
        exposure: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._hostname: str | None
        self._ip_addresses: list[str]
        self._mac_addresses: list[str]
        self._fqdn: str | None
        self._location: str | None
        self._criticality: str | None
        self._exposure: str | None
        self.hostname = hostname
        self.ip_addresses = ip_addresses
        self.mac_addresses = mac_addresses
        self.fqdn = fqdn
        self.location = location
        self.criticality = criticality
        self.exposure = exposure

    @property
    def hostname(self) -> str | None:
        return self._hostname

    @hostname.setter
    def hostname(self, value: str | None) -> None:
        self._hostname = require_optional_str(value, "hostname")

    @property
    def ip_addresses(self) -> list[str]:
        return self._ip_addresses

    @ip_addresses.setter
    def ip_addresses(self, value: list[str] | None) -> None:
        self._ip_addresses = require_optional_list_str(value, "ip_addresses")

    @property
    def mac_addresses(self) -> list[str]:
        return self._mac_addresses

    @mac_addresses.setter
    def mac_addresses(self, value: list[str] | None) -> None:
        self._mac_addresses = require_optional_list_str(value, "mac_addresses")

    @property
    def fqdn(self) -> str | None:
        return self._fqdn

    @fqdn.setter
    def fqdn(self, value: str | None) -> None:
        self._fqdn = require_optional_str(value, "fqdn")

    @property
    def location(self) -> str | None:
        return self._location

    @location.setter
    def location(self, value: str | None) -> None:
        self._location = require_optional_str(value, "location")

    @property
    def criticality(self) -> str | None:
        return self._criticality

    @criticality.setter
    def criticality(self, value: str | None) -> None:
        self._criticality = require_allowed(require_optional_str(value, "criticality"), "criticality", {None, 'high', 'medium', 'low', 'critical'})

    @property
    def exposure(self) -> str | None:
        return self._exposure

    @exposure.setter
    def exposure(self, value: str | None) -> None:
        self._exposure = require_allowed(require_optional_str(value, "exposure"), "exposure", {None, 'dmz', 'external', 'internal', 'unknown'})

