from __future__ import annotations

from uuid import uuid4

from metamodel.core.ValidationUtils import require_optional_str, require_str


class BaseEntity:
    """Base class for all metamodel entities.

    The internal id is generated automatically at instantiation time and is read-only.
    Entity type is derived from the class name, which must match the metamodel entity name.
    """

    _domain_attributes: tuple[str, ...] = ()

    def __init__(self, name: str, description: str | None = None, source: str | None = None) -> None:
        self._id = str(uuid4())
        self._name: str
        self._description: str | None
        self._source: str | None
        self.name = name
        self.description = description
        self.source = source

    @property
    def id(self) -> str:
        """Internal automatically generated identifier."""
        return self._id

    @property
    def type(self) -> str:
        """Entity type, derived from the class name."""
        return self.__class__.__name__

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = require_str(value, "name")

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        self._description = require_optional_str(value, "description")

    @property
    def source(self) -> str | None:
        return self._source

    @source.setter
    def source(self, value: str | None) -> None:
        self._source = require_optional_str(value, "source")

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "source": self.source,
        }
        for attr in self._domain_attributes:
            data[attr] = getattr(self, attr)
        return data

    def __repr__(self) -> str:
        return f"{self.type}(id={self.id!r}, name={self.name!r})"
