from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cardinality:
    """Represents a relationship cardinality such as 0..*, 1, or 1..*."""

    minimum: int
    maximum: int | None

    @classmethod
    def parse(cls, value: str | None) -> "Cardinality | None":
        if value is None:
            return None
        value = str(value).strip()
        if not value:
            return None
        if ".." in value:
            low, high = value.split("..", 1)
            minimum = int(low)
            maximum = None if high == "*" else int(high)
            return cls(minimum, maximum)
        exact = int(value)
        return cls(exact, exact)

    def contains(self, count: int) -> bool:
        if count < self.minimum:
            return False
        if self.maximum is not None and count > self.maximum:
            return False
        return True

    def __str__(self) -> str:
        if self.maximum is None:
            return f"{self.minimum}..*"
        if self.minimum == self.maximum:
            return str(self.minimum)
        return f"{self.minimum}..{self.maximum}"
