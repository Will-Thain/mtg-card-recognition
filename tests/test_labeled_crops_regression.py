"""Labeled-crops regression placeholder — cascade unchanged under YOLO R0 (CHK-YOLO-P1-07)."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.pipeline.image_analysis import analyze_listing_image

FIXTURE = Path(__file__).parent / "fixtures" / "r0_spike" / "train_001.jpg"


def test_cascade_gate_matrix_unchanged_for_yolo_flag() -> None:
    candidates = [
        {"scryfall_id": "a", "printing_id": "a", "rank_order": 1},
        {"scryfall_id": "b", "printing_id": "b", "rank_order": 2},
    ]
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
    assert [row["gate_status"] for row in canny] == [row["gate_status"] for row in yolo]
