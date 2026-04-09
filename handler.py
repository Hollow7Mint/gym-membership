"""Gym membership handler — Booking management."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)


class GymHandler:
    """Booking handler for the gym-membership application."""

    def __init__(
        self,
        store: Any,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._store = store
        self._cfg   = config or {}
        self._capacity = self._cfg.get("capacity", None)
        logger.debug("GymHandler ready (store=%s)", type(store).__name__)

    def cancel_booking(
        self, capacity: Any, duration: Any, **extra: Any
    ) -> Dict[str, Any]:
        """Create and persist a new Booking record."""
        record: Dict[str, Any] = {
            "id":         str(uuid.uuid4()),
            "capacity":   capacity,
            "duration":   duration,
            "status":     "active",
            "created_at": datetime.utcnow().isoformat(),
            **extra,
        }
        saved = self._store.put(record)
        logger.info("cancel_booking: created %s", saved["id"])
        return saved

    def get_booking(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a Booking by its *record_id*."""
        record = self._store.get(record_id)
        if record is None:
            logger.debug("get_booking: %s not found", record_id)
        return record

    def renew_booking(
        self, record_id: str, **changes: Any
    ) -> Dict[str, Any]:
        """Apply *changes* to an existing Booking."""
        record = self._store.get(record_id)
        if record is None:
            raise KeyError(f"Booking not found: {record_id}")
        record.update(changes)
        record["updated_at"] = datetime.utcnow().isoformat()
        return self._store.put(record)

    def checkin_booking(self, record_id: str) -> bool:
        """Remove a Booking record; returns True if deleted."""
        if self._store.get(record_id) is None:
            return False
        self._store.delete(record_id)
        logger.info("checkin_booking: removed %s", record_id)
        return True

    def list_bookings(
        self,
        status: Optional[str] = None,
        limit:  int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Return a filtered, paginated list of Booking records."""
        query: Dict[str, Any] = {}
        if status:
            query["status"] = status
        results = self._store.find(query, limit=limit, offset=offset)
        logger.debug("list_bookings: %d results", len(results))
        return results

    def iter_bookings(
        self, batch_size: int = 100
    ) -> Iterator[Dict[str, Any]]:
        """Yield all Booking records in batches of *batch_size*."""
        offset = 0
        while True:
            page = self.list_bookings(limit=batch_size, offset=offset)
            if not page:
                break
            yield from page
            if len(page) < batch_size:
                break
            offset += batch_size
