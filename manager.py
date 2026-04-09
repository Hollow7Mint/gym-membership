"""Gym membership manager — Class management."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)


class GymManager:
    """Class manager for the gym-membership application."""

    def __init__(
        self,
        store: Any,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._store = store
        self._cfg   = config or {}
        self._location = self._cfg.get("location", None)
        logger.debug("GymManager ready (store=%s)", type(store).__name__)

    def assign_trainer_class(
        self, location: Any, plan_type: Any, **extra: Any
    ) -> Dict[str, Any]:
        """Create and persist a new Class record."""
        record: Dict[str, Any] = {
            "id":         str(uuid.uuid4()),
            "location":   location,
            "plan_type":   plan_type,
            "status":     "active",
            "created_at": datetime.utcnow().isoformat(),
            **extra,
        }
        saved = self._store.put(record)
        logger.info("assign_trainer_class: created %s", saved["id"])
        return saved

    def get_class(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a Class by its *record_id*."""
        record = self._store.get(record_id)
        if record is None:
            logger.debug("get_class: %s not found", record_id)
        return record

    def enroll_class(
        self, record_id: str, **changes: Any
    ) -> Dict[str, Any]:
        """Apply *changes* to an existing Class."""
        record = self._store.get(record_id)
        if record is None:
            raise KeyError(f"Class not found: {record_id}")
        record.update(changes)
        record["updated_at"] = datetime.utcnow().isoformat()
        return self._store.put(record)

    def book_class_class(self, record_id: str) -> bool:
        """Remove a Class record; returns True if deleted."""
        if self._store.get(record_id) is None:
            return False
        self._store.delete(record_id)
        logger.info("book_class_class: removed %s", record_id)
        return True

    def list_classs(
        self,
        status: Optional[str] = None,
        limit:  int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Return a filtered, paginated list of Class records."""
        query: Dict[str, Any] = {}
        if status:
            query["status"] = status
        results = self._store.find(query, limit=limit, offset=offset)
        logger.debug("list_classs: %d results", len(results))
        return results

    def iter_classs(
        self, batch_size: int = 100
    ) -> Iterator[Dict[str, Any]]:
        """Yield all Class records in batches of *batch_size*."""
        offset = 0
        while True:
            page = self.list_classs(limit=batch_size, offset=offset)
            if not page:
                break
            yield from page
            if len(page) < batch_size:
                break
            offset += batch_size
