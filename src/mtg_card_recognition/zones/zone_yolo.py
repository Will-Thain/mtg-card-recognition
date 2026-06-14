"""Zone YOLO detector on aligned card crops (YOLO-P2 stub)."""

from __future__ import annotations

from typing import Any

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.crops import DEFAULT_ZONE_RECTS, ZoneCrop


def detect_zone_boxes_yolo(_aligned_image: Any, settings: RecognitionSettings) -> list[ZoneCrop]:
    """Stub zone YOLO — returns fixed rects with yolo detector tag until model ships."""
    _ = settings.yolo_zone_model_path
    return [
        ZoneCrop(name=name, bbox=bbox, detector="zone_yolo_stub", confidence=0.9)
        for name, bbox in DEFAULT_ZONE_RECTS.items()
    ]
