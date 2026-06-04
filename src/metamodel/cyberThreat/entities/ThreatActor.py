from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_list_str, require_optional_str, require_optional_taxonomy_ref


class ThreatActor(BaseEntity):
    """Represents the ThreatActor entity from the metamodel."""

    _domain_attributes = ('aliases', 'motivation', 'sophistication', 'country', 'taxonomy_ref')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        aliases: list[str] | None = None,
        motivation: str | None = None,
        sophistication: str | None = None,
        country: str | None = None,
        taxonomy_ref: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._aliases: list[str]
        self._motivation: str | None
        self._sophistication: str | None
        self._country: str | None
        self._taxonomy_ref: str | None
        self.aliases = aliases
        self.motivation = motivation
        self.sophistication = sophistication
        self.country = country
        self.taxonomy_ref = taxonomy_ref

    @property
    def aliases(self) -> list[str]:
        return self._aliases

    @aliases.setter
    def aliases(self, value: list[str] | None) -> None:
        self._aliases = require_optional_list_str(value, "aliases")

    @property
    def motivation(self) -> str | None:
        return self._motivation

    @motivation.setter
    def motivation(self, value: str | None) -> None:
        self._motivation = require_optional_str(value, "motivation")

    @property
    def sophistication(self) -> str | None:
        return self._sophistication

    @sophistication.setter
    def sophistication(self, value: str | None) -> None:
        self._sophistication = require_allowed(require_optional_str(value, "sophistication"), "sophistication", {None, 'high', 'medium', 'advanced', 'unknown', 'low'})

    @property
    def country(self) -> str | None:
        return self._country

    @country.setter
    def country(self, value: str | None) -> None:
        self._country = require_optional_str(value, "country")

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

