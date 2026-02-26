from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity


class AttackToolInstance(BaseEntity):
    """
    AttackToolInstance: an instance of an attack tool used in cyber threats.
    """

    def __init__(self, name: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
