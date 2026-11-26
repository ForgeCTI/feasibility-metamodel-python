from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity


class Resource(BaseEntity):
    """Element hosted, processed, accessed, or acted upon within the infrastructure (abstract: specialized by Code, Data, and Asset)."""

    _domain_attributes = ()
    knowledge_class = 'system'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
