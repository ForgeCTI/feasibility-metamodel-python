from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from Cardinality import Cardinality
from BaseEntity import BaseEntity

class RelationshipError(Exception):
    """Base exception for relationship/schema errors."""

class UnknownRelationship(RelationshipError):
    pass

class TypeViolation(RelationshipError, TypeError):
    pass

class BaseRelationship:
    """
    Base relationship definition

    @param uid: Unique identifier for the relationship
    @param name: Name of the relationship
    @param src_type: Source entity type (BaseEntity subclass)
    @param dst_type: Destination entity type (BaseEntity subclass)
    @param cardinality: Cardinality constraints
    @param edge_attr_schema: Optional schema for edge attributes (dict of attr name to type)
    @param description: Optional human-readable description
    """

    def __init__(self, name: str,
                 src_type: BaseEntity,
                 dst_type: BaseEntity,
                 src: str,
                 dst: str,
                 cardinality: Cardinality = Cardinality(0, None),
                 edge_attr_schema: Optional[Dict[str, type]] = None,
                 description: Optional[str] = None) -> None:
        self.name = name
        
        self.src_type = src_type
        self.dst_type = dst_type
        self.src = src
        self.dst = dst
        self.cardinality = cardinality

        if self._validate_edge_attrs(edge_attr_schema):
            self.edge_attr_schema = edge_attr_schema
        else:
            self.edge_attr_schema = None

        self.description = description
        self.uid = str(uuid4())

    # ----------------------------
    # Enforcement helpers
    # ----------------------------

    def _validate_edge_attrs(self, attrs: Optional[Dict[str, Any]]) -> None:
        if attrs is None:
            return
        if not isinstance(attrs, dict):
            raise TypeViolation(f"{self.name}: edge attributes must be a dict or None")

        if self.edge_attr_schema is None:
            return

        for k, v in attrs.items():
            if k not in self.edge_attr_schema:
                raise RelationshipError(f"{self.name}: unexpected edge attribute '{k}'")
            expected_t = self.edge_attr_schema[k]
            if v is not None and not isinstance(v, expected_t):
                raise TypeViolation(
                    f"{self.name}: edge attribute '{k}' must be {expected_t.__name__}, got {type(v).__name__}"
                )

    def check_add(self, *, out_degree: int, src_id: str) -> None:
        self.cardinality.check_add(out_degree, context=f"{self.name} per-src [{src_id}]")

    def check_remove(self, *, out_degree: int, src_id: str) -> None:
        self.cardinality.check_remove(out_degree, context=f"{self.name} per-src [{src_id}]")

    @property
    def kind(self) -> str:
        return self.name
        
    
    def __hash__(self) -> int:
        return hash(self.uid)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseRelationship) and self.uid == other.uid
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "src": self.src,
            "dst": self.dst,
            "cardinality": {
                "min": self.cardinality.min_count,
                "max": self.cardinality.max_count,
            },
            "edge_attr_schema": {k: v.__name__ for k, v in self.edge_attr_schema.items()} if self.edge_attr_schema else None,
            "description": self.description,
        }