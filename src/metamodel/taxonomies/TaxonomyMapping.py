from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaxonomyMapping:
    """Maps a metamodel entity type to a taxonomy id."""

    entity_type: str
    taxonomy_id: str
