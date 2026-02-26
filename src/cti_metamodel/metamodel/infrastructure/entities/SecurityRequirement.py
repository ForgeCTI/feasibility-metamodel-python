from __future__ import annotations
from ....core.BaseEntity import BaseEntity

class SecurityRequirement(BaseEntity):
    """
    Represents a security requirement in the infrastructure metamodel.
    """

    def __init__(self, label:str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.label = label
