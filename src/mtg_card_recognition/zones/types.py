"""Shared types for Tier-0 card region detection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CardRegion:
    """One detected card region on a listing photo."""

    obb: tuple[float, float, float, float, float, float, float, float]
    label: str
    confidence: float
    detector: str
    model_version: str | None = None

    @property
    def quad(self) -> list[float]:
        """Four corner points as flat x,y list (YOLO OBB order)."""
        return list(self.obb)
