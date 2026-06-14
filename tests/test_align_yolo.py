"""Align behavior with YOLO OBB quad (CHK-YOLO-P1-03)."""

from __future__ import annotations

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.align import normalize_card_image


def test_align_accepts_obb_quad() -> None:
    quad = [4.0, 4.0, 28.0, 4.0, 28.0, 44.0, 4.0, 44.0]
    result = normalize_card_image(
        None,
        quad=quad,
        settings=RecognitionSettings(region_detector="yolo_obb", image_allow_full_frame_fallback=False),
    )
    assert result.ok is True
    assert result.used_quad is True
    assert result.quad == quad


def test_yolo_obb_disables_full_frame_fallback_when_configured() -> None:
    result = normalize_card_image(
        None,
        quad=None,
        settings=RecognitionSettings(region_detector="yolo_obb", image_allow_full_frame_fallback=False),
    )
    assert result.ok is False
    assert result.reason == "full_frame_fallback_disabled_for_yolo_obb"


def test_canny_allows_full_frame_fallback() -> None:
    result = normalize_card_image(
        None,
        quad=None,
        settings=RecognitionSettings(region_detector="canny", image_allow_full_frame_fallback=True),
    )
    assert result.ok is True
    assert result.used_quad is False
