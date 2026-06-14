"""YOLO OBB region detection tests (CHK-YOLO-P1-02)."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.pipeline.image_analysis import analyze_listing_image
from mtg_card_recognition.zones.regions import detect_card_regions

FIXTURE = Path(__file__).parent / "fixtures" / "r0_spike" / "train_001.jpg"


def test_yolo_obb_detector_returns_one_region() -> None:
    settings = RecognitionSettings(region_detector="yolo_obb")
    regions = detect_card_regions(FIXTURE, settings)
    assert len(regions) == 1
    assert regions[0].detector == "yolo_obb"
    assert regions[0].model_version == "yolo_obb_stub_v0"


def test_analyze_listing_image_with_yolo_obb_sets_model_version() -> None:
    settings = RecognitionSettings(region_detector="yolo_obb")
    candidates = [{"scryfall_id": "abc", "printing_id": "abc", "rank_order": 1}]
    proposals = analyze_listing_image(FIXTURE, candidates, settings=settings)
    assert proposals[0]["model_version"] == "yolo_obb_stub_v0"
    assert proposals[0]["region_detector"] == "yolo_obb"
    assert "card_obb" in proposals[0]
