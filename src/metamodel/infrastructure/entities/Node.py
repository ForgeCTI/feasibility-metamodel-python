from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_optional_str,
    require_optional_ip_addresses,
    require_optional_mac_addresses,
)

class Node(BaseEntity):
    """Represents the Node entity from the metamodel."""

    _domain_attributes = (
        'hostname',
        'ip_addresses',
        'mac_addresses',
        'fqdn',
    )

    def __init__(
        self,
        name: str,
        description: str | None = None,
        hostname: str | None = None,
        ip_addresses: list[str] | None = None,
        mac_addresses: list[str] | None = None,
        fqdn: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._hostname: str | None
        self._ip_addresses: list[str]
        self._mac_addresses: list[str]
        self._fqdn: str | None
        self.hostname = hostname
        self.ip_addresses = ip_addresses
        self.mac_addresses = mac_addresses
        self.fqdn = fqdn

    @property
    def hostname(self) -> str | None:
        return self._hostname

    @hostname.setter
    def hostname(self, value: str | None) -> None:
        self._hostname = require_optional_str(value, "hostname")

    @property
    def ip_addresses(self) -> list[str]:
        return list(self._ip_addresses)

    @ip_addresses.setter
    def ip_addresses(self, value: list[str] | None) -> None:
        self._ip_addresses = require_optional_ip_addresses(
            value, "ip_addresses"
        )

    @property
    def mac_addresses(self) -> list[str]:
        return list(self._mac_addresses)

    @mac_addresses.setter
    def mac_addresses(self, value: list[str] | None) -> None:
        self._mac_addresses = require_optional_mac_addresses(
            value, "mac_addresses"
        )

    @property
    def fqdn(self) -> str | None:
        return self._fqdn

    @fqdn.setter
    def fqdn(self, value: str | None) -> None:
        self._fqdn = require_optional_str(value, "fqdn")
