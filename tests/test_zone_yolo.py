"""Zone YOLO stub tests (CHK-YOLO-P2-02/03)."""

from __future__ import annotations

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.crops import extract_zone_crops


def test_zone_yolo_flag_returns_stub_crops() -> None:
    settings = RecognitionSettings(zone_detector="yolo")
    crops = extract_zone_crops(None, settings)
    assert len(crops) >= 2
    assert all(crop.detector == "zone_yolo_stub" for crop in crops)


def test_fixed_rect_default_unchanged_with_p1_flag() -> None:
    crops = extract_zone_crops(None, RecognitionSettings(zone_detector="fixed_rect"))
    assert crops[0].detector == "fixed_rect"
