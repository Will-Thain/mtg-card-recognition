"""Unified Tier-0 card region entry — dispatches by ``region_detector`` setting."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.canny import detect_card_regions_canny
from mtg_card_recognition.zones.types import CardRegion
from mtg_card_recognition.zones.yolo_obb import detect_card_regions_yolo_obb


def detect_card_regions(image_path: str | Path, settings: RecognitionSettings) -> list[CardRegion]:
    """Run R0 card region detection for one listing image."""
    path = Path(image_path)
    detector = (settings.region_detector or "canny").lower()

    if detector == "yolo_obb":
        regions = detect_card_regions_yolo_obb(path, settings)
    elif detector == "canny":
        regions = detect_card_regions_canny(path)
    else:
        msg = f"Unknown region_detector: {settings.region_detector!r}"
        raise ValueError(msg)

    min_score = settings.image_min_region_score
    return [region for region in regions if region.confidence >= min_score]
