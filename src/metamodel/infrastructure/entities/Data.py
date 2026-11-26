from __future__ import annotations

from metamodel.infrastructure.entities.Resource import Resource
from metamodel.core.ValidationUtils import (
    require_optional_str,
)


class Data(Resource):
    """Digital content stored, processed, or transmitted within the infrastructure (formerly Information)."""

    _domain_attributes = Resource._domain_attributes + ('format',)
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        format: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._format: str | None
        self.format = format


    @property
    def format(self) -> str | None:
        return self._format

    @format.setter
    def format(self, value: str | None) -> None:
        self._format = require_optional_str(value, "format")
