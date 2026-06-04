from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_date_string, require_optional_list_str, require_optional_str


class AttackToolInstance(BaseEntity):
    """Represents the AttackToolInstance entity from the metamodel."""

    _domain_attributes = ('observed_version', 'hashes', 'first_seen', 'last_seen')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        observed_version: str | None = None,
        hashes: list[str] | None = None,
        first_seen: str | None = None,
        last_seen: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._observed_version: str | None
        self._hashes: list[str]
        self._first_seen: str | None
        self._last_seen: str | None
        self.observed_version = observed_version
        self.hashes = hashes
        self.first_seen = first_seen
        self.last_seen = last_seen

    @property
    def observed_version(self) -> str | None:
        return self._observed_version

    @observed_version.setter
    def observed_version(self, value: str | None) -> None:
        self._observed_version = require_optional_str(value, "observed_version")

    @property
    def hashes(self) -> list[str]:
        return self._hashes

    @hashes.setter
    def hashes(self, value: list[str] | None) -> None:
        self._hashes = require_optional_list_str(value, "hashes")

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

