from __future__ import annotations

from typing import Any

from Resource import Resource

class Asset(Resource):
    """
    Represents an asset in the infrastructure metamodel.
    """

    def __init__(self, name:str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
    
