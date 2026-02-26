from __future__ import annotations
from typing import Any
from ....core.BaseEntity import BaseEntity


class AdversaryType(BaseEntity):
    """
    Represents types of adversaries in the cyber threat metamodel.
    """
    def __init__(self, type: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.type = type
