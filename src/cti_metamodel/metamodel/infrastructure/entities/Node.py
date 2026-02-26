from __future__ import annotations

from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity
from NodeType import NodeType

class Node(BaseEntity):
    """
    A Node is a discrete computational or networked component within an environment, representing a single addressable unit (physical or virtual) that can host software resources and expose communication interfaces, and that functions as a fundamental locus for modeling deployment, connectivity, and attack surface in feasibility analysis.
    """

    def __init__(self, hostname: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.hostname = hostname
