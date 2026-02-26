from __future__ import annotations

from typing import Any, Optional

from ....core.BaseEntity import BaseEntity

class User(BaseEntity):
    """
    A User represents an individual or entity that interacts with the system, typically possessing specific roles and responsibilities within an organization.
    """

    def __init__(self, name: str,  **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name