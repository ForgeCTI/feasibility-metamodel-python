from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity


class ThreatEvent(BaseEntity):
    """
    Represents a threat event in the cyber threat metamodel.
    """

    def __init__(self, name:str, date:datetime,**kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.date = date
