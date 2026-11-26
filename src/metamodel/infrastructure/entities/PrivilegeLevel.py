from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import (
    require_optional_int,
)


class PrivilegeLevel(BaseEntity):
    """Ordered privilege level (e.g. standard user < administrator < system); association class of grantsAccessTo."""

    _domain_attributes = ('rank',)
    knowledge_class = 'concept'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        rank: int | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._rank: int | None
        self.rank = rank


    @property
    def rank(self) -> int | None:
        return self._rank

    @rank.setter
    def rank(self, value: int | None) -> None:
        self._rank = require_optional_int(value, "rank", minimum=0)
