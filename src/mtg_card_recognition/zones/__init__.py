"""Tier-0 geometry: region detect, align, types."""

from mtg_card_recognition.zones.align import AlignResult, normalize_card_image
from mtg_card_recognition.zones.regions import detect_card_regions
from mtg_card_recognition.zones.types import CardRegion

__all__ = [
    "AlignResult",
    "CardRegion",
    "detect_card_regions",
    "normalize_card_image",
]
