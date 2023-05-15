import re
from typing import *


def get_multiple(d: dict[Any, Any], *keys: Iterable[Any]) -> dict[Any, Any]:
    return {key: d.get(key) for key in keys}


def normalize_whitespace(s: str) -> str:
    RE_WHITESPACE = re.compile("\s+")
    s = re.sub(RE_WHITESPACE, " ", s)
    return s.strip()


def quote_value(value: str, quote: str = "`") -> str:
    if re.match(re.compile(quote + "(.*)" + quote), value) is not None:
        return value
    else:
        return f"{quote}{value}{quote}"
