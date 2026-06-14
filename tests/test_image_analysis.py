"""Image analysis flag matrix (canny vs yolo_obb)."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.pipeline.image_analysis import analyze_listing_image

FIXTURE = Path(__file__).parent / "fixtures" / "r0_spike" / "train_001.jpg"


def test_analyze_listing_image_flag_matrix() -> None:
    candidates = [{"scryfall_id": "x", "printing_id": "x", "rank_order": 1}]
    canny = analyze_listing_image(
        FIXTURE,
        candidates,
        settings=RecognitionSettings(region_detector="canny"),
    )
    yolo = analyze_listing_image(
        FIXTURE,
        candidates,
        settings=RecognitionSettings(region_detector="yolo_obb"),
    )
    assert canny[0]["region_detector"] == "canny"
    assert yolo[0]["region_detector"] == "yolo_obb"
    assert yolo[0].get("model_version")
