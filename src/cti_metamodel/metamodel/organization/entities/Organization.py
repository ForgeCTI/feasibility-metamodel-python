from __future__ import annotations

from typing import Any, Optional, Set, Tuple

from src.core.BaseEntity import BaseEntity

class Organization(BaseEntity):
    """
    An Organization is a uniquely identifiable institutional entity—such as a private company, public-sector body, non-profit organization, or other structured collective—modeled as a top-level subject of analysis to capture its stable identity, scope of responsibility, and contextual characteristics relevant to assessing operational and security-related scenarios.
    
    @param legal_name: The official registered legal name of the organization.
    """

    def __init__(self, legal_name: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.legal_name = legal_name
    
    def __hash__(self):
        return super().__hash__()
