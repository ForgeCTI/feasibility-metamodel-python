from __future__ import annotations

from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class AttackTool(BaseEntity):
    """
    AttackTool: a tool used to carry out cyber attacks.
    """

    def __init__(self, name: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
