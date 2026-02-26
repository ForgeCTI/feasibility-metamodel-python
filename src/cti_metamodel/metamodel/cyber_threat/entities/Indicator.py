from __future__ import annotations

from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity


class Indicator(BaseEntity):
    """
    Indicator: an observable artifact that suggests a potential cyber threat.
    """

    def __init__(self, value: str, type:str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.value = value
        self.type = type
