from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class AttackToolConfiguration(BaseEntity):
    """
    AttackToolConfiguration: configuration details for an attack tool instance.
    """

    def __init__(self, parameters: Dict[str, Any], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.parameters = parameters
