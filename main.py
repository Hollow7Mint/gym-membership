"""Gym membership main — utility helpers."""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Any, Dict, Iterable, List, Optional

logger = logging.getLogger(__name__)

_SLUG_RE = re.compile(r"[^\w-]+")


def book_class_class(data: Dict[str, Any]) -> Dict[str, Any]:
    """Class book_class helper — validates and normalises *data*."""
    result = {k: v for k, v in data.items() if v is not None}
    if "expiry_date" not in result:
        raise ValueError(f"Class must have a 'expiry_date'")
    result["id"] = result.get("id") or hashlib.md5(
        str(result["expiry_date"]).encode()).hexdigest()[:12]
    return result


def cancel_classs(
    items: Iterable[Dict[str, Any]],
    *,
    status: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Filter and page through a list of Class records."""
    out = [i for i in items if status is None or i.get("status") == status]
    logger.debug("cancel_classs: %d items after filter", len(out))
    return out[:limit]


def renew_class(record: Dict[str, Any], **overrides: Any) -> Dict[str, Any]:
    """Return a shallow copy of *record* with *overrides* applied."""
    updated = dict(record)
    updated.update(overrides)
    if "capacity" in updated and not isinstance(updated["capacity"], (int, float)):
        try:
            updated["capacity"] = float(updated["capacity"])
        except (TypeError, ValueError):
            pass
    return updated


def slugify_class(text: str) -> str:
    """Convert *text* to a URL-safe Class slug."""
    slug = _SLUG_RE.sub("-", text.lower().strip())
    return slug.strip("-")[:64]


def validate_class(record: Dict[str, Any]) -> bool:
    """Return True if *record* satisfies all Class invariants."""
    required = ["expiry_date", "capacity", "duration"]
    for field in required:
        if field not in record or record[field] is None:
            logger.warning("validate_class: missing field %r", field)
            return False
    return isinstance(record.get("id"), str)


def checkin_class_batch(
    records: List[Dict[str, Any]],
    batch_size: int = 50,
) -> List[List[Dict[str, Any]]]:
    """Split *records* into chunks of *batch_size* for bulk checkin."""
    return [records[i : i + batch_size]
            for i in range(0, len(records), batch_size)]
