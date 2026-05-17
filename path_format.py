from __future__ import annotations

import re
from datetime import datetime


_DATE_PATTERN = re.compile(r"%date:([^%]+)%")


def _format_date_pattern(pattern: str, now: datetime | None = None) -> str:
    now = now or datetime.now()
    replacements = {
        "yyyy": f"{now.year:04d}",
        "yy": f"{now.year % 100:02d}",
        "MM": f"{now.month:02d}",
        "M": str(now.month),
        "dd": f"{now.day:02d}",
        "d": str(now.day),
        "HH": f"{now.hour:02d}",
        "H": str(now.hour),
        "hh": f"{(now.hour % 12) or 12:02d}",
        "h": str((now.hour % 12) or 12),
        "mm": f"{now.minute:02d}",
        "m": str(now.minute),
        "ss": f"{now.second:02d}",
        "s": str(now.second),
        "SSS": f"{now.microsecond // 1000:03d}",
        "a": "AM" if now.hour < 12 else "PM",
    }

    output = []
    index = 0
    tokens = sorted(replacements, key=len, reverse=True)
    while index < len(pattern):
        for token in tokens:
            if pattern.startswith(token, index):
                output.append(replacements[token])
                index += len(token)
                break
        else:
            output.append(pattern[index])
            index += 1

    return "".join(output)


def expand_date_tokens(path_template: str) -> str:
    return _DATE_PATTERN.sub(lambda match: _format_date_pattern(match.group(1)), path_template or "")


def format_path(path_template: str) -> str:
    return expand_date_tokens(path_template)
