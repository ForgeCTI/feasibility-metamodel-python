from __future__ import annotations

from typing import Any, Optional

from ....core.BaseEntity import BaseEntity

class UserType(BaseEntity):
    """
    A UserType represents the classification or category of a User, defining its characteristics, capabilities, and role within an organization. 
    """

    def __init__(self, type: str,  **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.type = type