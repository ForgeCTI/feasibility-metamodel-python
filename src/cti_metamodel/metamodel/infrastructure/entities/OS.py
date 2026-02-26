from __future__ import annotations

from typing import Any, Optional, Tuple

from Process import Process

class OS(Process):
    """
    OS represents an Operating System installed on a Node within an infrastructure environment.
    """

    def __init__(self, family: str, distro: str, version: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.family = family
        self.distro = distro
        self.version = version