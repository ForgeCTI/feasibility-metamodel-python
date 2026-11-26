from __future__ import annotations

from metamodel.infrastructure.entities.Code import Code
from metamodel.core.ValidationUtils import (
    require_optional_str,
)


class OSInstance(Code):
    """Instance of an operating system running on a node."""

    _domain_attributes = Code._domain_attributes + ('build', 'patch_level', 'support_status')
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        build: str | None = None,
        patch_level: str | None = None,
        support_status: str | None = None,
        version: str | None = None,
        language: str | None = None,
        repository_url: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source, version=version, language=language, repository_url=repository_url)
        self._build: str | None
        self._patch_level: str | None
        self._support_status: str | None
        self.build = build
        self.patch_level = patch_level
        self.support_status = support_status


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
        self._support_status = require_optional_str(value, "support_status")
