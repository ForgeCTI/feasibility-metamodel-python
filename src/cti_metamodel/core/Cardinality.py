from __future__ import annotations

from typing import Optional


class CardinalityViolation(ValueError):
    """Raised when an edge operation would violate a cardinality constraint."""

class Cardinality:
    """
    Cardinality constraints for one end of a relationship.

    @param min_count: minimum number of edges required (>= 0)
    @param max_count: maximum number of edges allowed; None means unbounded
    """
    def __init__(self, min_count: int = 0, max_count: Optional[int] = None) -> None:
        if min_count < 0:
            raise ValueError("min_count must be >= 0")
        if max_count is not None and max_count < min_count:
            raise ValueError("max_count must be >= min_count or None")
        self.min_count = min_count
        self.max_count = max_count

    def allows(self, n: int) -> bool:
        if n < self.min_count:
            return False
        if self.max_count is not None and n > self.max_count:
            return False
        return True

    def check_add(self, current: int, *, context: str) -> None:
        """
        Check whether adding one edge would violate max cardinality.
        """
        if self.max_count is not None and (current + 1) > self.max_count:
            raise CardinalityViolation(
                f"{context}: max cardinality exceeded "
                f"(current={current}, attempted={current + 1}, max={self.max_count})"
            )

    def check_remove(self, current: int, *, context: str) -> None:
        """
        Check whether removing one edge would violate min cardinality.
        """
        after = current - 1
        if after < self.min_count:
            raise CardinalityViolation(
                f"{context}: min cardinality violated "
                f"(current={current}, attempted={after}, min={self.min_count})"
            )
