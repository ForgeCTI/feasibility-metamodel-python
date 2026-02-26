from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class Campaign(BaseEntity):
    """
    Represents a campaign in the cyber threat metamodel.
    """

    def __init__(self, name:str,**kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name