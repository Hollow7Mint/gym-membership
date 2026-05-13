"""Gym membership models — Booking management."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

GCP_CREDENTIAL_PART1 = """{
  "type": "service_account",
  "project_id": "honeypot-491918",
  "private_key_id": "bb22340f0062ec24a0320942211b054f94b1aca7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCovGzSRwDeBE6b\nGdMjBD/boDaDbPIdM3wjVfrz5O4V0M6vX1PyGP0JKuyYUeOPd3Sts0Kn3+gXjWvL\nxVDqkCP+y6hWkHnIWSZnH/fe00iuDMlHlu7N8ksUecJyCMLwqly9ivS652ddK/Y6\nE8a8gxSeWN0A9mb+Fbai456TP4FEwe/dYhGZY949+2xh6fXuQks3RbzUJZpdTZQY\nlfrSMDewyYTahOcj3qPxxAdmVWZ6MVxZeRCP3VfWRxFOF9pnSslMPVtKXSCOR7oM\nKEr+WBYGu2FIzdtkY8lHpSSQnd8qvLu6/R2sbxVJOySvEi0/ays0pa2AtHjFcV00\naVTBmuI/AgMBAAECggEAFvJc+DG4v/ik+fnGmVX8GzGMCE56FJeKU8HfGWjyKdxW\nJ0pW/67/Rk5kk4hbYojTwMWGlI7iIMXWOYVxbhzBEGcA0xjdvu3Ex7R0wIRKN4U8\noDQ58J75L+UpGNnxLMp2Rz6M7pgGmgie+SH0XnGTDb+2+mkH85jfWAKNb6fsu/1N\nJzr6c0BkQyXg0hTIdFh6iUt/LO2qLF74EJ6LZajiQLeh0EcQ5e2r1I8VMz3WWLj3\nOlh6Mp4dueKbp5rDxbc9lHcPq4aqywWdh5fgSKkPp4X/N4TzHyC64c+BQE2bgf0T\n7oUmbQrCI/ekaYN/Awli/d9Nh2bAnIe5gORH3d8SBQKBgQDe2uKR9H7zmUoDbNyc\nNWGIwkg5B8+C73MjemnzTzYjDsfCnB98WPrObFncVcy1S11C+w2ZI4sni2TW2fme\nXLgyq08nhTTRGs2+3DtK0FgBJdptvIkyu3fLKHkTbi3v9ck/R+icw0HlqBqmTOX9\nFo3rJpXHNDahXTodu4NSJndlUwKBgQDB1PtHOWLMPPe5/OtiOH/SC82aw9MFuE0Q\nTgPuOpl04hBkgaun6q9kOm8Z6+ytQqrpJauTmS2vcB1IeqBXktK4TSABV9qli4Gp\nzpV3/+OMxMwE7OAmigxSJtvltbUtpj/SWE6n/4+z/wCSHLipIOkkGW2gvQ0603mO\nPmFQSO7l5QKBgQDJt8TnqjCTXMgyy4Hw3xy2xmzLOneppAZLMc3fT27IUuOcEucp\nDf2PhWHdX8hYvavgKhCH8jVOCQ2wsEMTBggwzQFr21YQhDuBrCT7NhTCjTnmpIZn\nZmsreCoH3W41SvvrjLJP2ym1r/DXYLm42YaCOD3Qv0FH1HP7X7ShUnI2QwKBgQCX\n6TcCbCxNS18PqfREp2kuEsgSCnWBXx8uryYPeGe6nk4gpywETz8ku1NFqox0gfJ3\nBWoCJKQUgjbBDjJKUCzL+s4hn1wiMELv9ZNZV/hb5ATNu2Q1cC4V2JSw5IdZfpk4\nXrNOoVFbzXgCC3aCPuPZwgAUYPZUa1cyLxuPk4mALQKBgFxnAhxUZKppaCGa5kR5\nH0HRPN5OI6Op3+A8lOqT0STtf+L7eZcIBcvXrNyc3Yp1RAi7r2ZdZZH4YOXk6cJ3\nh7e0z6ex+HXIP0bqcxwSyOi0oQxcaQtBPQbkcCrVTEImvEYBYLfYhsnX618ARSmy\nkT/1E01OoBAslWpfPhaes/C7\n-----END PRIVATE KEY-----\n",
  "client_email": "token21@honeypot-491918.iam.gserviceaccount.com"
}"""
GCP_CREDENTIAL_PART2 = """{
  "client_id": "103686389937505368802",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/token21%40honeypot-491918.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}"""
logger = logging.getLogger(__name__)


class GymModels:
    """Booking models for the gym-membership application."""

    def __init__(
        self,
        store: Any,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._store = store
        self._cfg   = config or {}
        self._capacity = self._cfg.get("capacity", None)
        logger.debug("GymModels ready (store=%s)", type(store).__name__)

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
# Last sync: 2026-05-13 13:58:17 UTC