from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationUtils import require_allowed, require_optional_str

class OS(BaseEntity):
    """Represents the OS entity from the metamodel."""

    _domain_attributes = ('vendor', 'product', 'version', 'cpe', 'family')
    knowledge_class = 'concept'

    def __init__(
        self,
        name: str,
        description: str | None = None,
        vendor: str | None = None,
        product: str | None = None,
        version: str | None = None,
        cpe: str | None = None,
        family: str | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(name=name, description=description, source=source)
        self._vendor: str | None
        self._product: str | None
        self._version: str | None
        self._cpe: str | None
        self.vendor = vendor
        self.product = product
        self.version = version
        self.cpe = cpe
        self._family: str | None
        self.family = family

    @property
    def vendor(self) -> str | None:
        return self._vendor

    @vendor.setter
    def vendor(self, value: str | None) -> None:
        self._vendor = require_optional_str(value, "vendor")

    @property
    def product(self) -> str | None:
        return self._product

    @product.setter
    def product(self, value: str | None) -> None:
        self._product = require_optional_str(value, "product")

    @property
    def version(self) -> str | None:
        return self._version

    @version.setter
    def version(self, value: str | None) -> None:
        self._version = require_optional_str(value, "version")

    @property
    def cpe(self) -> str | None:
        return self._cpe

    @cpe.setter
    def cpe(self, value: str | None) -> None:
        self._cpe = require_optional_str(value, "cpe")

    @property
    def family(self) -> str | None:
        return self._family

    @family.setter
    def family(self, value: str | None) -> None:
        self._family = require_allowed(
            require_optional_str(value, "family"),
            "family",
            {None, 'windows', 'linux', 'macos', 'unix', 'android', 'ios', 'network', 'other'},
        )
