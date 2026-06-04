"""Generic STIX model elements.

These classes allow the parser to preserve STIX objects and relationships even
when the CTI Feasibility Metamodel does not yet have a native semantic class for
them.
"""

from __future__ import annotations

from typing import Any

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.BaseRelationship import BaseRelationship


class GenericStixObject(BaseEntity):
    """Generic entity preserving an arbitrary STIX object.

    Use this for STIX objects that are valid CTI objects but do not have a
    direct CTI Feasibility Metamodel entity mapping yet.
    """

    def __init__(
        self,
        stix_type: str,
        stix_id: str,
        name: str,
        description: str | None = None,
        raw: dict[str, Any] | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)

        self._stix_type: str
        self._stix_id: str
        self._raw: dict[str, Any]

        self.stix_type = stix_type
        self.stix_id = stix_id
        self.raw = raw or {}

    @property
    def stix_type(self) -> str:
        return self._stix_type

    @stix_type.setter
    def stix_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("stix_type must be a string.")
        if not value.strip():
            raise ValueError("stix_type cannot be empty.")
        self._stix_type = value

    @property
    def stix_id(self) -> str:
        return self._stix_id

    @stix_id.setter
    def stix_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("stix_id must be a string.")
        if not value.strip():
            raise ValueError("stix_id cannot be empty.")
        self._stix_id = value

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

    @raw.setter
    def raw(self, value: dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("raw must be a dictionary.")
        self._raw = value


class GenericStixRelationship(BaseRelationship):
    """Generic relationship preserving an arbitrary STIX relationship object."""

    def __init__(
        self,
        source_entity,
        target_entity,
        stix_relationship_type: str,
        stix_id: str | None = None,
        raw: dict[str, Any] | None = None,
    ) -> None:
        self._stix_relationship_type: str
        self._stix_id: str | None
        self._raw: dict[str, Any]

        self.stix_relationship_type = stix_relationship_type
        self.stix_id = stix_id
        self.raw = raw or {}

        super().__init__(
            source_entity=source_entity,
            target_entity=target_entity,
        )

    @property
    def stix_relationship_type(self) -> str:
        return self._stix_relationship_type

    @stix_relationship_type.setter
    def stix_relationship_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("stix_relationship_type must be a string.")
        if not value.strip():
            raise ValueError("stix_relationship_type cannot be empty.")
        self._stix_relationship_type = value

    @property
    def stix_id(self) -> str | None:
        return self._stix_id

    @stix_id.setter
    def stix_id(self, value: str | None) -> None:
        if value is not None and not isinstance(value, str):
            raise TypeError("stix_id must be a string or None.")
        self._stix_id = value

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

    @raw.setter
    def raw(self, value: dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("raw must be a dictionary.")
        self._raw = value

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["stix_relationship_type"] = self.stix_relationship_type
        data["stix_id"] = self.stix_id
        return data
