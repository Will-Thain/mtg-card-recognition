"""Recognition settings consumed by workflow adapters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RecognitionSettings:
    """Library-facing recognition configuration."""

    faiss_index_path: str = "./.cache/faiss/index.bin"
    faiss_top_k: int = 5
    image_min_region_score: float = 0.55
    image_allow_full_frame_fallback: bool = True
    verify_name_hard_min: float = 0.75
    verify_name_strong_min: float = 0.88
    verify_symbol_strong_min: float = 0.55
    image_evidence_min_ocr_similarity: float = 0.60
    image_evidence_min_faiss_score: float = 0.55
    image_evidence_min_mana_confidence: float = 0.30
    card_zone_ocr_enabled: bool = True
    card_zone_faiss_enabled: bool = True
    card_zone_align_enabled: bool = True
    card_set_symbol_match_enabled: bool = True
    card_set_symbol_min_score: float = 0.45
    card_mana_cost_enabled: bool = True
    align_min_confidence: float = 0.35
    faiss_propose_candidates: bool = True
    ocr_engine: str = "pytesseract"
    tesseract_cmd: str | None = None
    torch_device: str = "cpu"
    openclip_model_name: str = "ViT-B-32"
    embedding_batch_size: int = 32
    region_detector: str = "canny"
    yolo_obb_model_path: str | None = None
    yolo_obb_model_version: str = "yolo_obb_stub_v0"
    zone_detector: str = "fixed_rect"
    yolo_zone_model_path: str | None = None
