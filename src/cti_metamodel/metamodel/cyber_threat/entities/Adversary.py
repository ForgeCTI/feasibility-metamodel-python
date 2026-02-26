from __future__ import annotations

from typing import Any

from ....core.BaseEntity import BaseEntity

class Adversary(BaseEntity):
    """
    Represents an adversary in the cyber threat metamodel.
    """

    def __init__(self, name:str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name

    
