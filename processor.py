"""Gym membership processor — Subscription management."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)


class GymProcessor:
    """Subscription processor for the gym-membership application."""

    def __init__(
        self,
        store: Any,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._store = store
        self._cfg   = config or {}
        self._capacity = self._cfg.get("capacity", None)
        logger.debug("GymProcessor ready (store=%s)", type(store).__name__)

    def cancel_subscription(
        self, capacity: Any, duration: Any, **extra: Any
    ) -> Dict[str, Any]:
        """Create and persist a new Subscription record."""
        record: Dict[str, Any] = {
            "id":         str(uuid.uuid4()),
            "capacity":   capacity,
            "duration":   duration,
            "status":     "active",
            "created_at": datetime.utcnow().isoformat(),
            **extra,
        }
        saved = self._store.put(record)
        logger.info("cancel_subscription: created %s", saved["id"])
        return saved

    def get_subscription(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a Subscription by its *record_id*."""
        record = self._store.get(record_id)
        if record is None:
            logger.debug("get_subscription: %s not found", record_id)
        return record

    def renew_subscription(
        self, record_id: str, **changes: Any
    ) -> Dict[str, Any]:
        """Apply *changes* to an existing Subscription."""
        record = self._store.get(record_id)
        if record is None:
            raise KeyError(f"Subscription not found: {record_id}")
        record.update(changes)
        record["updated_at"] = datetime.utcnow().isoformat()
        return self._store.put(record)

    def checkin_subscription(self, record_id: str) -> bool:
        """Remove a Subscription record; returns True if deleted."""
        if self._store.get(record_id) is None:
            return False
        self._store.delete(record_id)
        logger.info("checkin_subscription: removed %s", record_id)
        return True

    def list_subscriptions(
        self,
        status: Optional[str] = None,
        limit:  int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Return a filtered, paginated list of Subscription records."""
        query: Dict[str, Any] = {}
        if status:
            query["status"] = status
        results = self._store.find(query, limit=limit, offset=offset)
        logger.debug("list_subscriptions: %d results", len(results))
        return results

    def iter_subscriptions(
        self, batch_size: int = 100
    ) -> Iterator[Dict[str, Any]]:
        """Yield all Subscription records in batches of *batch_size*."""
        offset = 0
        while True:
            page = self.list_subscriptions(limit=batch_size, offset=offset)
            if not page:
                break
            yield from page
            if len(page) < batch_size:
                break
            offset += batch_size
