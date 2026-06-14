"""MTG card recognition library — greenfield MVP-4 cascade stub."""

from mtg_card_recognition.cascade import run_cascade
from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.pipeline.image_analysis import analyze_listing_image

__version__ = "0.4.0"

__all__ = [
    "__version__",
    "RecognitionSettings",
    "analyze_listing_image",
    "run_cascade",
]
