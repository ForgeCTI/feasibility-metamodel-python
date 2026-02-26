from __future__ import annotations
from typing import Any
from ....core.BaseEntity import BaseEntity

class NodeType(BaseEntity):
    """
    A NodeType represents the classification or category of a Node, defining its characteristics, capabilities, and role within an infrastructure environment. Examples of NodeTypes include server, workstation, router, switch, firewall, virtual machine, container, and cloud instance. NodeTypes help in modeling the deployment, connectivity, and security aspects of Nodes in feasibility analysis.
    """
    def __init__(self, type: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.type = type
