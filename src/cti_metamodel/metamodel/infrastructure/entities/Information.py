from __future__ import annotations

from typing import Any, Optional

from Resource import Resource

class Information(Resource):
    """
    Information resource accessed by processes.
    """

    def __init__(self, name: Optional[str] = None, classification: str = None, info_type: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.info_type = info_type
        if classification:
            self.classification = classification