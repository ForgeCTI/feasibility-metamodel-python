from __future__ import annotations

from datetime import date
from typing import Any


def require_optional_str(value: Any, field_name: str, *, allow_empty: bool = False) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string or None.")
    if not allow_empty and not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def require_str(value: Any, field_name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not allow_empty and not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def require_optional_bool(value: Any, field_name: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be a bool or None.")
    return value


def require_optional_int(value: Any, field_name: str, *, minimum: int | None = None, maximum: int | None = None) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be an integer or None.")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field_name} must be >= {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field_name} must be <= {maximum}.")
    return value


def require_optional_float(value: Any, field_name: str, *, minimum: float | None = None, maximum: float | None = None) -> float | None:
    if value is None:
        return None
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be a number or None.")
    value = float(value)
    if minimum is not None and value < minimum:
        raise ValueError(f"{field_name} must be >= {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field_name} must be <= {maximum}.")
    return value


def require_optional_list_str(value: Any, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError(f"{field_name} must be a list of strings.")
    if not all(isinstance(item, str) for item in value):
        raise TypeError(f"{field_name} must contain only strings.")
    return list(value)


def require_optional_dict(value: Any, field_name: str) -> dict:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a dictionary or None.")
    return dict(value)


def require_optional_date_string(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be an ISO date string or None.")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must use ISO date format YYYY-MM-DD.") from exc
    return value


def require_optional_taxonomy_ref(value: Any, field_name: str = "taxonomy_ref") -> str | None:
    value = require_optional_str(value, field_name)
    if value is not None and ":" not in value:
        raise ValueError(f"{field_name} must use '<taxonomy>:<concept>' format.")
    return value


def require_optional_email(value: Any, field_name: str) -> str | None:
    value = require_optional_str(value, field_name)
    if value is not None and "@" not in value:
        raise ValueError(f"{field_name} must look like an email address.")
    return value


def require_allowed(value: Any, field_name: str, allowed: set[Any]) -> Any:
    if value not in allowed:
        readable = ", ".join(str(item) for item in sorted(item for item in allowed if item is not None))
        raise ValueError(f"{field_name} must be one of: {readable}.")
    return value
