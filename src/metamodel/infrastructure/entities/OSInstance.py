from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str


class OSInstance(BaseEntity):
    """Represents the OSInstance entity from the metamodel."""

    _domain_attributes = ('version', 'build', 'patch_level', 'support_status')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        version: str | None = None,
        build: str | None = None,
        patch_level: str | None = None,
        support_status: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._version: str | None
        self._build: str | None
        self._patch_level: str | None
        self._support_status: str | None
        self.version = version
        self.build = build
        self.patch_level = patch_level
        self.support_status = support_status

    @property
    def version(self) -> str | None:
        return self._version

    @version.setter
    def version(self, value: str | None) -> None:
        self._version = require_optional_str(value, "version")

    @property
    def build(self) -> str | None:
        return self._build

    @build.setter
    def build(self, value: str | None) -> None:
        self._build = require_optional_str(value, "build")

    @property
    def patch_level(self) -> str | None:
        return self._patch_level

    @patch_level.setter
    def patch_level(self, value: str | None) -> None:
        self._patch_level = require_optional_str(value, "patch_level")

    @property
    def support_status(self) -> str | None:
        return self._support_status

    @support_status.setter
    def support_status(self, value: str | None) -> None:
        self._support_status = require_allowed(require_optional_str(value, "support_status"), "support_status", {None, 'unknown', 'end_of_life', 'supported'})

