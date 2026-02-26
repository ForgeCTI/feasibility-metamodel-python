from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Mapping, Optional, Set, Tuple
from uuid import uuid4

from ..core.helpers.time import dt_from_iso, utcnow

class BaseEntity:
    """
    Root class for all entities in the metamodel.

    @param uid: Unique identifier for the entity
    @param description: Optional human-readable description
    @param external_ids: Optional mapping of external system IDs
    @param tags: Optional set of tags for categorization
    @param meta: Optional arbitrary metadata
    @param created_at: Timestamp of entity creation
    @param updated_at: Timestamp of last entity update
    """

    def __init__(self, description: Optional[str] = None,
                 external_ids: Optional[Dict[str, str]] = None,
                 tags: Optional[Dict[str]] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        self.uid = str(uuid4())
        self.description = description

        self.external_ids = external_ids if external_ids is not None else {}
        self.tags = tags if tags is not None else dict()
        self.meta = meta if meta is not None else {}

        self.created_at = created_at if created_at is not None else utcnow().isoformat()
        self.updated_at = updated_at if updated_at is not None else utcnow().isoformat()

    @property
    def kind(self) -> str:
        return self.__class__.__name__

    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseEntity) and self.uid == other.uid

    def touch(self) -> None:
        self.updated_at = utcnow()

    # ----------------------------
    # Merge support
    # ----------------------------

    def merge_from(self, other: BaseEntity, *, prefer: str = "self") -> None:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot merge {type(other).__name__} into {type(self).__name__}")

        if prefer not in {"self", "other"}:
            raise ValueError("prefer must be 'self' or 'other'")
        overwrite = (prefer == "other")

        def choose(a: Any, b: Any) -> Any:
            if a is None:
                return b
            if b is None:
                return a
            return b if overwrite else a

        self.label = choose(self.label, other.label)
        self.description = choose(self.description, other.description)

        self.tags |= set(other.tags)
        self.external_ids.update(other.external_ids)
        self.meta.update(other.meta)

        self.touch()

    # ----------------------------
    # Serialization
    # ----------------------------

    def to_dict(self) -> Dict[str, Any]:
        d = self.__dict__
        d['class'] = self.kind
        return d

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> BaseEntity:
        return cls(
            uid=str(d.get("uid", str(uuid4()))),
            description=d.get("description"),
            external_ids=dict(d.get("external_ids", {}) or {}),
            tags=set(d.get("tags", {}) or []),
            meta=dict(d.get("meta", {}) or {}),
            created_at=dt_from_iso(d.get("created_at")) or utcnow().isoformat(),
            updated_at=dt_from_iso(d.get("updated_at")) or utcnow().isoformat(),
        )


Entity = BaseEntity
