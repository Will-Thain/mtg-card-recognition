"""Zone crop extraction — fixed rects or optional zone YOLO (YOLO-P2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mtg_card_recognition.config import RecognitionSettings


@dataclass(frozen=True, slots=True)
class ZoneCrop:
    """One named zone crop on an aligned card image."""

    name: str
    bbox: tuple[float, float, float, float]
    detector: str
    confidence: float


DEFAULT_ZONE_RECTS: dict[str, tuple[float, float, float, float]] = {
    "bottom": (0.05, 0.78, 0.95, 0.98),
    "set_symbol": (0.78, 0.62, 0.95, 0.76),
    "title": (0.08, 0.08, 0.92, 0.22),
}


def extract_zone_crops(_aligned_image: Any, settings: RecognitionSettings) -> list[ZoneCrop]:
    """Return zone crops using fixed rects or optional zone YOLO detector."""
    if settings.zone_detector == "yolo":
        from mtg_card_recognition.zones.zone_yolo import detect_zone_boxes_yolo

        return detect_zone_boxes_yolo(_aligned_image, settings)

    return [
        ZoneCrop(name=name, bbox=bbox, detector="fixed_rect", confidence=1.0)
        for name, bbox in DEFAULT_ZONE_RECTS.items()
    ]
