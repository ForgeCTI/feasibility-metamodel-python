from __future__ import annotations
from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class AttackStepItem(BaseEntity):
    """
    Represents an attack step item in the cyber threat metamodel.
    """

    def __init__(self, name:str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
