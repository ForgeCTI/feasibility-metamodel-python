from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional


def utcnow() -> datetime:
    """
    Canonical clock for KB lifecycle timestamps.
    Always returns a tz-aware UTC datetime.
    """
    return datetime.now(timezone.utc)


def dt_to_iso(dt: Optional[datetime]) -> Optional[str]:
    """
    Convert tz-aware (or naive) datetime to ISO-8601 string in UTC.
    Returns None if dt is None.
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def dt_from_iso(s: Optional[str]) -> Optional[datetime]:
    """
    Parse ISO-8601 string to tz-aware datetime.
    If the parsed datetime is naive, it is assumed UTC.
    Returns None if s is None/empty.
    """
    if not s:
        return None
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def ensure_utc(dt: datetime) -> datetime:
    """
    Ensure dt is tz-aware and normalized to UTC.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
