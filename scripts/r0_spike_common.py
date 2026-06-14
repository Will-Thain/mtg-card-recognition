"""Shared paths and stub R0 detectors for YOLO-P0 spike scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "r0_spike"
MANIFEST_PATH = FIXTURE_DIR / "holdout_manifest.json"
ARTIFACT_DIR = ROOT / "artifacts" / "r0_spike"

DEFAULT_CARD_OBB = [4.0, 4.0, 28.0, 4.0, 28.0, 44.0, 4.0, 44.0]
CANNY_FP_OBB = [2.0, 2.0, 8.0, 2.0, 8.0, 8.0, 2.0, 8.0]


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    """Load holdout manifest JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def image_by_eval_id(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map eval_id to image record."""
    return {img["eval_id"]: img for img in manifest["images"]}


def default_card_detection(confidence: float = 0.92) -> dict[str, Any]:
    """Return a single card OBB detection."""
    return {"obb": list(DEFAULT_CARD_OBB), "label": "card", "confidence": confidence}


def stub_cardcaptor_obb(image_path: Path) -> list[dict[str, Any]]:
    """Stub CardCaptor/YOLO OBB detector — no ONNX required."""
    _ = image_path
    return [default_card_detection(confidence=0.88)]


def stub_canny_detector(_image_path: Path) -> list[dict[str, Any]]:
    """Stub Canny baseline — matches truth plus one spurious FP box."""
    return [
        default_card_detection(confidence=0.71),
        {"obb": list(CANNY_FP_OBB), "label": "card", "confidence": 0.55},
    ]


def stub_yolo_obb_detector(_image_path: Path) -> list[dict[str, Any]]:
    """Stub YOLO OBB detector — matches ground truth on compare set."""
    return [default_card_detection(confidence=0.94)]


def obb_match(a: list[float], b: list[float], tolerance: float = 2.0) -> bool:
    """True when all eight OBB coordinates are within tolerance."""
    if len(a) != 8 or len(b) != 8:
        return False
    return all(abs(x - y) <= tolerance for x, y in zip(a, b, strict=True))


def count_fp_fn(
    predictions: list[dict[str, Any]],
    ground_truth: list[dict[str, Any]],
) -> tuple[int, int]:
    """Greedy OBB match: unmatched preds are FP, unmatched truth are FN."""
    matched_truth: set[int] = set()
    false_positives = 0

    for pred in predictions:
        pred_obb = pred["obb"]
        found = False
        for idx, truth in enumerate(ground_truth):
            if idx in matched_truth:
                continue
            if obb_match(pred_obb, truth["obb"]):
                matched_truth.add(idx)
                found = True
                break
        if not found:
            false_positives += 1

    false_negatives = len(ground_truth) - len(matched_truth)
    return false_positives, false_negatives
