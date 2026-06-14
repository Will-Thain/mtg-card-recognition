"""Tier-0 geometry gate — unified R0 entry before alignment."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.regions import detect_card_regions
from mtg_card_recognition.zones.types import CardRegion


def run_tier0_geometry(image_path: str | Path, settings: RecognitionSettings) -> list[CardRegion]:
    """Detect card regions for one listing image (R0)."""
    return detect_card_regions(image_path, settings)
