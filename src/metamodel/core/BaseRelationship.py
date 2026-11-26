from __future__ import annotations

from typing import Any
from uuid import uuid4

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_str


class BaseRelationship:
    """Base class for all metamodel relationships.

    A relationship connects one source entity to one target entity.

    Class attributes:

    * ``label``: name of the association in the metamodel (e.g. ``implements``).
      Several classes may share a label when the association has several target
      types (e.g. ``protects``); the class name is then the unique identifier.
    * ``source_cardinality`` / ``target_cardinality``: multiplicities at the
      source and target ends (the target cardinality constrains outgoing
      relationships per source entity).
    * ``_domain_attributes``: names of relationship attributes, e.g. the
      association class ``PrivilegeLevel`` of ``grantsAccessTo``.
    * ``_entity_attributes``: subset of attributes whose value is an entity,
      mapped to the expected entity class.
    * ``cardinality_counts``: names of other relationship classes whose
      instances also count towards the cardinalities of this one (e.g. a node
      that runs an application instance also hosts it).
    """

    source_type: type[BaseEntity] | None = None
    target_type: type[BaseEntity] | None = None
    source_cardinality: str | None = None
    target_cardinality: str | None = None
    label: str | None = None
    _domain_attributes: tuple[str, ...] = ()
    _entity_attributes: dict[str, type[BaseEntity]] = {}
    cardinality_counts: tuple[str, ...] = ()

    def __init__(self, source_entity: BaseEntity, target_entity: BaseEntity, **attributes: Any) -> None:
        self._id = str(uuid4())
        self._source_entity = self._validate_endpoint(source_entity, self.source_type, "source")
        self._target_entity = self._validate_endpoint(target_entity, self.target_type, "target")
        self._attributes: dict[str, Any] = {name: None for name in self._domain_attributes}
        unknown = set(attributes) - set(self._domain_attributes)
        if unknown:
            raise TypeError(f"{self.type} got unexpected attribute(s): {', '.join(sorted(unknown))}")
        for name, value in attributes.items():
            self.set_attribute(name, value)

    @classmethod
    def get_label(cls) -> str:
        """Metamodel label of the association (defaults to the class name)."""
        return cls.label or cls.__name__

    @staticmethod
    def _validate_endpoint(
        entity: BaseEntity,
        expected_type: type[BaseEntity] | None,
        role: str
    ) -> BaseEntity:
        if expected_type is None:
            raise TypeError(f"{role}_type is not defined")
        if not isinstance(entity, expected_type):
            raise TypeError(f"{role}_entity must be an instance of {expected_type.__name__}")
        return entity

    def _update_endpoints(self, source_entity: BaseEntity, target_entity: BaseEntity) -> None:
        """Update relationship endpoints after validating their types."""

        source = self._validate_endpoint(source_entity, self.source_type, "source")
        target = self._validate_endpoint(target_entity, self.target_type, "target")
        self._source_entity = source
        self._target_entity = target

    def _restore_id(self, value: str) -> None:
        """Restore a persisted identifier (used by importers only)."""
        self._id = require_str(value, "id")

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def source_entity(self) -> BaseEntity:
        return self._source_entity

    @property
    def target_entity(self) -> BaseEntity:
        return self._target_entity

    @property
    def attributes(self) -> dict[str, Any]:
        """Relationship attributes (entity-valued attributes are entities)."""
        return dict(self._attributes)

    def get_attribute(self, name: str) -> Any:
        if name not in self._domain_attributes:
            raise AttributeError(f"{self.type} has no attribute {name!r}")
        return self._attributes[name]

    def set_attribute(self, name: str, value: Any) -> None:
        if name not in self._domain_attributes:
            raise AttributeError(f"{self.type} has no attribute {name!r}")
        expected = self._entity_attributes.get(name)
        if expected is not None and value is not None and not isinstance(value, expected):
            raise TypeError(f"{name} must be an instance of {expected.__name__} or None")
        self._attributes[name] = self._validate_attribute(name, value)

    def _validate_attribute(self, name: str, value: Any) -> Any:
        """Hook for subclasses to validate non-entity attributes."""
        return value

    def referenced_entities(self) -> list[BaseEntity]:
        """Entities referenced by entity-valued attributes."""
        return [v for k, v in self._attributes.items() if k in self._entity_attributes and v is not None]

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "type": self.type,
            "source": self.source_entity.id,
            "target": self.target_entity.id,
        }
        for name in self._domain_attributes:
            value = self._attributes[name]
            if isinstance(value, BaseEntity):
                value = value.id
            data[name] = value
        return data

    def __repr__(self) -> str:
        return f"{self.type}({self.source_entity!r} -> {self.target_entity!r})"
