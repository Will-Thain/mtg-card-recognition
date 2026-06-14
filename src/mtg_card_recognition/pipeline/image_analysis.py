"""Public listing image analysis — R0 detect, align, cascade tiers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mtg_card_recognition.cascade import run_cascade
from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.align import normalize_card_image
from mtg_card_recognition.zones.regions import detect_card_regions


def analyze_listing_image(
    image_path: str | Path,
    candidates: list[dict[str, Any]],
    settings: RecognitionSettings | None = None,
) -> list[dict[str, Any]]:
    """Analyze one listing image against title-match candidates."""
    loaded = settings or RecognitionSettings()
    path = Path(image_path)
    regions = detect_card_regions(path, loaded)

    primary_quad: list[float] | None = None
    model_version: str | None = None
    if regions:
        best = max(regions, key=lambda region: region.confidence)
        primary_quad = best.quad
        model_version = best.model_version

    align = normalize_card_image(None, quad=primary_quad, settings=loaded)
    if not align.ok:
        return [
            {
                **candidate,
                "gate_status": "blocked_at_gate",
                "gate_fail_reason": align.reason or "align_failed",
                "region_detector": loaded.region_detector,
            }
            for candidate in candidates
        ]

    proposals = run_cascade(str(path), candidates)
    for proposal in proposals:
        proposal["region_detector"] = loaded.region_detector
        if loaded.region_detector == "yolo_obb" and model_version:
            proposal["model_version"] = model_version
        if primary_quad is not None:
            proposal["card_obb"] = primary_quad
    return proposals
