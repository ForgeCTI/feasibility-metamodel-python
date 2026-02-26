from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Tuple

from Resource import Resource

class Process(Resource):
    """
    A Process represents an executing instance of an application within a Node
    """

    def __init__(self, name: Optional[str] = None, privileges: Optional[str] = None,**kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.privileges = privileges