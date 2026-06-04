from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_list_str, require_optional_str, require_optional_taxonomy_ref


class AttackTool(BaseEntity):
    """Represents the AttackTool entity from the metamodel."""

    _domain_attributes = ('taxonomy_ref', 'aliases', 'tool_type', 'capabilities')

    def __init__(
        self,
        name: str,
        description: str | None = None,
        taxonomy_ref: str | None = None,
        aliases: list[str] | None = None,
        tool_type: str | None = None,
        capabilities: list[str] | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._taxonomy_ref: str | None
        self._aliases: list[str]
        self._tool_type: str | None
        self._capabilities: list[str]
        self.taxonomy_ref = taxonomy_ref
        self.aliases = aliases
        self.tool_type = tool_type
        self.capabilities = capabilities

    @property
    def taxonomy_ref(self) -> str | None:
        return self._taxonomy_ref

    @taxonomy_ref.setter
    def taxonomy_ref(self, value: str | None) -> None:
        self._taxonomy_ref = require_optional_taxonomy_ref(value, "taxonomy_ref")

    @property
    def aliases(self) -> list[str]:
        return self._aliases

    @aliases.setter
    def aliases(self, value: list[str] | None) -> None:
        self._aliases = require_optional_list_str(value, "aliases")

    @property
    def tool_type(self) -> str | None:
        return self._tool_type

    @tool_type.setter
    def tool_type(self, value: str | None) -> None:
        self._tool_type = require_allowed(require_optional_str(value, "tool_type"), "tool_type", {None, 'scanner', 'living_off_the_land', 'malware', 'exploit_kit', 'custom_tool', 'unknown', 'credential_tool', 'command_and_control'})

    @property
    def capabilities(self) -> list[str]:
        return self._capabilities

    @capabilities.setter
    def capabilities(self, value: list[str] | None) -> None:
        self._capabilities = require_optional_list_str(value, "capabilities")

