from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_optional_str, require_optional_taxonomy_ref


class TTP(BaseEntity):
    """Represents the TTP entity from the metamodel."""

    _domain_attributes = ('taxonomy_ref', 'external_id', 'tactic', 'technique', 'subtechnique')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        taxonomy_ref: str | None = None,
        external_id: str | None = None,
        tactic: str | None = None,
        technique: str | None = None,
        subtechnique: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._taxonomy_ref: str | None
        self._external_id: str | None
        self._tactic: str | None
        self._technique: str | None
        self._subtechnique: str | None
        self.taxonomy_ref = taxonomy_ref
        self.external_id = external_id
        self.tactic = tactic
        self.technique = technique
        self.subtechnique = subtechnique

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

    @property
    def external_id(self) -> str | None:
        return self._external_id

    @external_id.setter
    def external_id(self, value: str | None) -> None:
        self._external_id = require_optional_str(value, "external_id")

    @property
    def tactic(self) -> str | None:
        return self._tactic

    @tactic.setter
    def tactic(self, value: str | None) -> None:
        self._tactic = require_optional_str(value, "tactic")

    @property
    def technique(self) -> str | None:
        return self._technique

    @technique.setter
    def technique(self, value: str | None) -> None:
        self._technique = require_optional_str(value, "technique")

    @property
    def subtechnique(self) -> str | None:
        return self._subtechnique

    @subtechnique.setter
    def subtechnique(self, value: str | None) -> None:
        self._subtechnique = require_optional_str(value, "subtechnique")

