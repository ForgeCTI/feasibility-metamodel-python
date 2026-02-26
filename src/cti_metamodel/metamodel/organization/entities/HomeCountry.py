from __future__ import annotations
from typing import Any
from src.core.BaseEntity import BaseEntity

class HomeCountry(BaseEntity):
    """
    A HomeCountry is a jurisdictional descriptor representing a specific nation-state used to capture the national legal and geopolitical context associated with an entity, enabling consistent representation of country-level identity and jurisdictional grounding within modeled scenarios.
    """

    def __init__(self, country, **kwargs: Any) -> None:
        self.country = country
        super().__init__(**kwargs)
