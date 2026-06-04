from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TaxonomyConcept:
    id: str
    name: str
    description: str | None = None
    aliases: list[str] = field(default_factory=list)
    category: str | None = None
    external_references: list[dict] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    properties: dict = field(default_factory=dict)

    @property
    def ref_name(self) -> str:
        return self.id
