from __future__ import annotations

from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class Port(BaseEntity):
    """
    Network port entity representing a communication endpoint within an infrastructure environment.
    """
    def __init__(self, number: int, protocol: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.number = number  # e.g., 80, 443
        self.protocol = protocol  # e.g., "TCP", "UDP"
    