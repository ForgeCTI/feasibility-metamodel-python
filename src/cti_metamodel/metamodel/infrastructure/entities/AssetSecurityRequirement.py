from __future__ import annotations
from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class AssetSecurityRequirement(BaseEntity):
    """
    Represents a security requirement associated with an asset.
    """
    def __init__(self, name:str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
    