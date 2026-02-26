from __future__ import annotations
from ....core.BaseEntity import BaseEntity


class ApplicationType(BaseEntity):
    """
    An ApplicationType represents a specific category or classification of an application within an infrastructure environment.
    """
    def __init__(self, type: str, **kwargs: dict) -> None:
        super().__init__(**kwargs)
        self.type = type