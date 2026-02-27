from __future__ import annotations
from typing import Any

from ....core.BaseEntity import BaseEntity

class InternationalBody(BaseEntity):
    """
    An InternationalBody is a supranational or transnational entity that groups multiple HomeCountry jurisdictions under a shared political, legal, economic, or security framework, enabling the metamodel to represent country membership in higher-level structures that may influence organizational context and threat-campaign focus.
    """
    
    def __init__(self, international_body, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.international_body = international_body
