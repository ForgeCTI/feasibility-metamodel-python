"""Extensible registries for STIX object and relationship mappers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


ObjectMapper = Callable[[dict[str, Any], "StixParserContext"], Any]
RelationshipMapper = Callable[[dict[str, Any], "StixParserContext"], list[Any]]


class StixObjectMapperRegistry:
    """Registry mapping STIX object type names to mapper functions."""

    def __init__(self) -> None:
        self._mappers: dict[str, ObjectMapper] = {}

    def register(self, stix_type: str, mapper: ObjectMapper) -> None:
        if not isinstance(stix_type, str) or not stix_type.strip():
            raise ValueError("stix_type must be a non-empty string.")
        if not callable(mapper):
            raise TypeError("mapper must be callable.")
        self._mappers[stix_type] = mapper

    def get(self, stix_type: str) -> ObjectMapper | None:
        return self._mappers.get(stix_type)

    def has(self, stix_type: str) -> bool:
        return stix_type in self._mappers

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self._mappers))


class StixRelationshipMapperRegistry:
    """Registry mapping STIX SRO types to mapper functions.

    The key is the STIX object type, for example `relationship` or `sighting`.
    Specific `relationship_type` values are preserved by the generic mapper and
    can be handled with custom mappers if needed.
    """

    def __init__(self) -> None:
        self._mappers: dict[str, RelationshipMapper] = {}

    def register(self, sro_type: str, mapper: RelationshipMapper) -> None:
        if not isinstance(sro_type, str) or not sro_type.strip():
            raise ValueError("sro_type must be a non-empty string.")
        if not callable(mapper):
            raise TypeError("mapper must be callable.")
        self._mappers[sro_type] = mapper

    def get(self, sro_type: str) -> RelationshipMapper | None:
        return self._mappers.get(sro_type)

    def has(self, sro_type: str) -> bool:
        return sro_type in self._mappers

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self._mappers))


class StixParserContext:
    """Mutable parser context passed to STIX mapper functions."""

    def __init__(self, model) -> None:
        self.model = model
        self.stix_to_entity: dict[str, Any] = {}
        self.stix_to_entity_id: dict[str, str] = {}
        self.skipped_objects: list[dict[str, str]] = []
        self.skipped_relationships: list[dict[str, str]] = []
