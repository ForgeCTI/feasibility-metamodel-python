from __future__ import annotations
from typing import Any, Optional, Tuple

def norm_text(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s2 = str(s).strip()
    return s2 or None


def norm_iso2(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s2 = str(s).strip().upper()
    return s2 or None

def norm_acronym(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s2 = str(s).strip().upper()
    return s2 or None

def norm_lower(s: Optional[str]) -> Optional[str]:
    t = norm_text(s)
    return t.lower() if t else None

def norm_upper(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    t = str(s).strip().upper()
    return t or None