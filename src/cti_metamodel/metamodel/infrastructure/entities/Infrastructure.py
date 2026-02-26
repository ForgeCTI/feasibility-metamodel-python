from __future__ import annotations

from datetime import datetime
from typing import Any

from ....core.BaseEntity import BaseEntity
from ....core.helpers.time import ensure_utc

class Infrastructure(BaseEntity):
    """
    An Infrastructure is an abstract representation of a bounded technical environment that aggregates the computational and networked components through which services are delivered and operations are performed, serving as the structural container for modeling systems, access relationships, and connectivity relevant to security and feasibility analysis.
    """
    
    def __init__(self, name: str, env: str, snapshot_at:datetime=None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.environment = env
        if snapshot_at is not None:
            self.snapshot_at = ensure_utc(snapshot_at).isoformat()
        else:
            self.snapshot_at = self.created_at