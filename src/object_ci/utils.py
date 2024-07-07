import os
from typing import TypeVar

_T = TypeVar("_T")


def getenv_or_raise(key: str, default: _T | None = None) -> str | _T:
    value = os.getenv(key, default)
    if value is None:
        raise KeyError(f"Environment variable not set: {key}")
    return value
