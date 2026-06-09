from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PrintingRecord:
    """Framework-agnostic Scryfall printing row for catalog indexing and veto."""

    scryfall_id: str
    name: str
    set_code: str | None = None
    collector_number: str | None = None
    lang: str | None = None
    image_normal: str | None = None
    raw_payload_json: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, row: Any) -> PrintingRecord:
        """Build from any object or dict with Scryfall-like attributes."""
        if isinstance(row, dict):
            return cls(
                scryfall_id=str(row.get("id") or row.get("scryfall_id")),
                name=str(row.get("name") or ""),
                set_code=row.get("set_code") or row.get("set"),
                collector_number=row.get("collector_number"),
                lang=row.get("lang"),
                image_normal=row.get("image_normal"),
                raw_payload_json=dict(row.get("raw_payload_json") or row),
            )
        return cls(
            scryfall_id=str(getattr(row, "id")),
            name=str(getattr(row, "name")),
            set_code=getattr(row, "set_code", None),
            collector_number=getattr(row, "collector_number", None),
            lang=getattr(row, "lang", None),
            image_normal=getattr(row, "image_normal", None),
            raw_payload_json=dict(getattr(row, "raw_payload_json", None) or {}),
        )
