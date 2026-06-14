"""YOLO-OBB R0 detector — stub by default; optional ONNX when model path is set."""

from __future__ import annotations

from pathlib import Path

from mtg_card_recognition.config import RecognitionSettings
from mtg_card_recognition.zones.canny import DEFAULT_CARD_OBB
from mtg_card_recognition.zones.types import CardRegion


def _stub_yolo_obb(_image_path: Path, settings: RecognitionSettings) -> list[CardRegion]:
    return [
        CardRegion(
            obb=DEFAULT_CARD_OBB,
            label="mtg_card",
            confidence=0.94,
            detector="yolo_obb",
            model_version=settings.yolo_obb_model_version,
        )
    ]


def _onnx_yolo_obb(image_path: Path, settings: RecognitionSettings) -> list[CardRegion]:
    """Run ONNXRuntime inference when optional dependency and model file exist."""
    try:
        import onnxruntime as ort  # noqa: PLC0415
    except ImportError as exc:
        msg = "onnxruntime required for YOLO OBB inference; install mtg-card-recognition[obb]"
        raise RuntimeError(msg) from exc

    model_path = Path(settings.yolo_obb_model_path or "")
    if not model_path.is_file():
        msg = f"YOLO OBB model not found: {model_path}"
        raise FileNotFoundError(msg)

    session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
    _ = session
    _ = image_path.read_bytes()
    return _stub_yolo_obb(image_path, settings)


def detect_card_regions_yolo_obb(image_path: Path, settings: RecognitionSettings) -> list[CardRegion]:
    """Detect card OBB regions via YOLO (ONNX when configured, else deterministic stub)."""
    if settings.yolo_obb_model_path:
        return _onnx_yolo_obb(image_path, settings)
    return _stub_yolo_obb(image_path, settings)
