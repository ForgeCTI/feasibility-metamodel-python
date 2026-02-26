from __future__ import annotations

from typing import Any

from src.core.BaseEntity import BaseEntity


class Sector(BaseEntity):
    """
    A Sector is a categorical descriptor representing an economic or operational domain (e.g., finance, healthcare, energy) used to classify entities by their primary area of activity, enabling consistent grouping, comparison, and domain-specific reasoning across modeled scenarios.
    """

    def __init__(self, sector_name: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.sector_name = sector_name
