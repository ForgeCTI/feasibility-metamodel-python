from __future__ import annotations

from typing import Any

from Process import Process

class ApplicationInstance(Process):
    """
    An ApplicationInstance represents a specific deployment or installation of an application within an infrastructure environment.
    """

    def __init__(self, name: str, version: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.version = version

   