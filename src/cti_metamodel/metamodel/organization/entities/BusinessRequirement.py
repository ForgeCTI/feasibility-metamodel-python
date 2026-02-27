from __future__ import annotations

from typing import Any, Optional, Tuple

from ....core.BaseEntity import BaseEntity

class BusinessRequirement(BaseEntity):
    """
    A BusinessRequirement is an organization-level statement of business, regulatory, contractual, or operational need that drives security posture and prioritization within the metamodel. It captures why specific protections are required, independently of how those protections are implemented.
    
    @param name: The name of the business requirement.
    @param description: A detailed description of the business requirement.
    """

    def __init__(self, name: Optional[str] = None,
                 description: Optional[str] = None,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.description = description
