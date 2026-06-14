"""Stub Canny contour R0 detector for tests and rollback path."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.zones.types import CardRegion

DEFAULT_CARD_OBB = (4.0, 4.0, 28.0, 4.0, 28.0, 44.0, 4.0, 44.0)
CANNY_FP_OBB = (2.0, 2.0, 8.0, 2.0, 8.0, 8.0, 2.0, 8.0)


def detect_card_regions_canny(_image_path: Path) -> list[CardRegion]:
    """Return stub Canny detections (truth box + one spurious FP on compare fixtures)."""
    return [
        CardRegion(
            obb=DEFAULT_CARD_OBB,
            label="card",
            confidence=0.71,
            detector="canny",
            model_version="canny_stub_v0",
        ),
        CardRegion(
            obb=CANNY_FP_OBB,
            label="card",
            confidence=0.55,
            detector="canny",
            model_version="canny_stub_v0",
        ),
    ]
