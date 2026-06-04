from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str


class Code(BaseEntity):
    """Represents the Code entity from the metamodel."""

    _domain_attributes = ('language', 'version', 'repository_url', 'hash')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        language: str | None = None,
        version: str | None = None,
        repository_url: str | None = None,
        hash: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._language: str | None
        self._version: str | None
        self._repository_url: str | None
        self._hash: str | None
        self.language = language
        self.version = version
        self.repository_url = repository_url
        self.hash = hash

    @property
    def language(self) -> str | None:
        return self._language

    @language.setter
    def language(self, value: str | None) -> None:
        self._language = require_optional_str(value, "language")

    @property
    def version(self) -> str | None:
        return self._version

    @version.setter
    def version(self, value: str | None) -> None:
        self._version = require_optional_str(value, "version")

    @property
    def repository_url(self) -> str | None:
        return self._repository_url

    @repository_url.setter
    def repository_url(self, value: str | None) -> None:
        self._repository_url = require_optional_str(value, "repository_url")

    @property
    def hash(self) -> str | None:
        return self._hash

    @hash.setter
    def hash(self, value: str | None) -> None:
        self._hash = require_optional_str(value, "hash")

