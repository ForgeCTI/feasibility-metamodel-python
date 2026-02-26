from __future__ import annotations

from typing import Any

from ....core.BaseEntity import BaseEntity

class InformationType(BaseEntity):
    """
    An InformationType represents the classification or category of an Information resource
    """

    def __init__(self, type: str,  **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.type = type