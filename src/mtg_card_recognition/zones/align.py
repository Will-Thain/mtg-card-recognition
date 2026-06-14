"""Card alignment — accepts optional YOLO OBB quad; gates full-frame fallback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mtg_card_recognition.config import RecognitionSettings


@dataclass(frozen=True, slots=True)
class AlignResult:
    """Outcome of normalize_card_image."""

    ok: bool
    used_quad: bool
    reason: str | None = None
    quad: list[float] | None = None


def normalize_card_image(
    _image: Any,
    *,
    quad: list[float] | None = None,
    settings: RecognitionSettings,
) -> AlignResult:
    """Normalize a listing crop using an optional four-point OBB quad."""
    if quad is not None and len(quad) == 8:
        return AlignResult(ok=True, used_quad=True, quad=list(quad))

    if settings.region_detector == "yolo_obb" and not settings.image_allow_full_frame_fallback:
        return AlignResult(
            ok=False,
            used_quad=False,
            reason="full_frame_fallback_disabled_for_yolo_obb",
        )

    return AlignResult(ok=True, used_quad=False, reason="full_frame_fallback")
