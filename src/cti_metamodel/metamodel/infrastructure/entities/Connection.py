from __future__ import annotations

from typing import Any

from ....core.BaseEntity import BaseEntity

class Connection(BaseEntity):
    """
    A Connection represents a network connection between Nodes within an infrastructure environment.
    """

    def __init__(self, protocol: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.protocol = protocol
