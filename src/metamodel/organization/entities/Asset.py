from __future__ import annotations

from metamodel.infrastructure.entities.Resource import Resource


class Asset(Resource):
    """Resource with an associated asset security requirement."""

    _domain_attributes = Resource._domain_attributes
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
