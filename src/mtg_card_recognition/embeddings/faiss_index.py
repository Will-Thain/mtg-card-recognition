from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import numpy as np

from ..catalog.printing import PrintingRecord
from ..config import RecognitionSettings
from ..zones.layouts import extract_art_zone_from_card_image, layout_from_scryfall_payload
from .openclip import embed_image_file, embed_image_paths

ProgressCallback = Callable[[int, int, str], None]


@dataclass(slots=True)
class EmbeddingMatch:
    scryfall_id: str
    card_name: str | None
    score: float


_FAISS_INDEX_CACHE: dict[str, tuple[Any, dict[str, Any]]] = {}


def clear_faiss_index_cache() -> None:
    _FAISS_INDEX_CACHE.clear()


def _meta_path(index_path: str) -> Path:
    return Path(f"{index_path}.meta.json")


def index_exists(index_path: str) -> bool:
    return Path(index_path).exists() and _meta_path(index_path).exists()


def load_index_meta(index_path: str) -> dict[str, Any] | None:
    meta_file = _meta_path(index_path)
    if not meta_file.exists():
        return None
    return json.loads(meta_file.read_text(encoding="utf-8"))


def indexed_scryfall_ids(index_path: str) -> set[str]:
    meta = load_index_meta(index_path)
    if not meta:
        return set()
    return {str(card_id) for card_id in meta.get("scryfall_ids", [])}


def skipped_scryfall_ids(index_path: str) -> set[str]:
    meta = load_index_meta(index_path)
    if not meta:
        return set()
    return {str(card_id) for card_id in meta.get("skipped_scryfall_ids", [])}


def excluded_scryfall_ids(index_path: str) -> set[str]:
    return indexed_scryfall_ids(index_path) | skipped_scryfall_ids(index_path)


def append_skipped_ids(index_path: Path, card_ids: list[str]) -> None:
    if not card_ids:
        return
    meta_file = _meta_path(str(index_path))
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
    skipped = {str(card_id) for card_id in meta.get("skipped_scryfall_ids", [])}
    skipped.update(card_ids)
    meta["skipped_scryfall_ids"] = sorted(skipped)
    meta_file.write_text(json.dumps(meta), encoding="utf-8")


def _load_faiss_index(index_path: str) -> tuple[Any, dict[str, Any]] | None:
    import faiss  # type: ignore[import-not-found]

    resolved = str(Path(index_path).resolve())
    if resolved in _FAISS_INDEX_CACHE:
        return _FAISS_INDEX_CACHE[resolved]

    if not index_exists(resolved):
        return None

    index = faiss.read_index(resolved)
    meta = json.loads(_meta_path(resolved).read_text(encoding="utf-8"))
    _FAISS_INDEX_CACHE[resolved] = (index, meta)
    return index, meta


def faiss_index_crop_mode(settings: RecognitionSettings) -> str:
    if settings.faiss_index_use_art_zone and settings.card_zone_faiss_enabled:
        return "art_zone"
    return "full_card"


def _download_art(url: str, dest: Path, timeout_ms: int) -> bool:
    try:
        with httpx.Client(timeout=timeout_ms / 1000) as client:
            response = client.get(url)
            response.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(response.content)
        return True
    except (httpx.HTTPError, OSError):
        return False


def prepare_art_paths(
    printings: list[PrintingRecord],
    settings: RecognitionSettings,
) -> tuple[list[str], list[str], list[str], int]:
    art_dir = Path(settings.image_cache_dir) / "scryfall_art"
    art_zone_dir = Path(settings.image_cache_dir) / "scryfall_art_zones"
    use_art_zone = faiss_index_crop_mode(settings) == "art_zone"
    pending_paths: list[str] = []
    card_ids: list[str] = []
    card_names: list[str] = []
    downloaded = 0

    for printing in printings:
        if not printing.image_normal:
            continue
        art_path = art_dir / f"{printing.scryfall_id}.jpg"
        if not art_path.exists():
            ok = _download_art(printing.image_normal, art_path, settings.image_download_timeout_ms)
            if ok:
                downloaded += 1
            time.sleep(0.05)
        if not art_path.exists():
            continue

        embed_path = art_path
        if use_art_zone:
            zone_path = art_zone_dir / f"{printing.scryfall_id}_art.jpg"
            if not zone_path.is_file():
                layout_hint = layout_from_scryfall_payload(printing.raw_payload_json)
                extracted = extract_art_zone_from_card_image(
                    str(art_path),
                    str(zone_path),
                    align_enabled=settings.card_zone_align_enabled,
                    scryfall_layout=layout_hint,
                )
                if not extracted:
                    continue
            embed_path = zone_path

        pending_paths.append(str(embed_path))
        card_ids.append(printing.scryfall_id)
        card_names.append(printing.name)

    return pending_paths, card_ids, card_names, downloaded


def embed_art_paths(
    pending_paths: list[str],
    card_ids: list[str],
    card_names: list[str],
    settings: RecognitionSettings,
    *,
    on_progress: ProgressCallback | None = None,
) -> tuple[list[np.ndarray], list[str], list[str]]:
    batch_size = max(1, settings.embedding_batch_size)
    matrix_rows: list[np.ndarray] = []
    indexed_ids: list[str] = []
    indexed_names: list[str] = []
    total_paths = len(pending_paths)

    if total_paths and on_progress is not None:
        on_progress(0, total_paths, "embeddings")

    for start in range(0, len(pending_paths), batch_size):
        chunk_paths = pending_paths[start : start + batch_size]
        chunk_ids = card_ids[start : start + batch_size]
        chunk_names = card_names[start : start + batch_size]
        try:
            vectors = embed_image_paths(chunk_paths, settings)
            for vector, card_id, card_name in zip(vectors, chunk_ids, chunk_names, strict=True):
                matrix_rows.append(vector)
                indexed_ids.append(card_id)
                indexed_names.append(card_name)
        except Exception:  # noqa: BLE001
            for path, card_id, card_name in zip(chunk_paths, chunk_ids, chunk_names, strict=True):
                try:
                    vector = embed_image_file(path, settings)
                except Exception:  # noqa: BLE001
                    continue
                matrix_rows.append(vector[0])
                indexed_ids.append(card_id)
                indexed_names.append(card_name)

        done = min(start + len(chunk_paths), total_paths)
        if on_progress is not None and (done % (batch_size * 5) == 0 or done == total_paths):
            on_progress(done, total_paths, "embeddings")

    return matrix_rows, indexed_ids, indexed_names


def write_faiss_index(
    index_path: Path,
    matrix_rows: list[np.ndarray],
    indexed_ids: list[str],
    indexed_names: list[str],
    settings: RecognitionSettings,
    *,
    append: bool,
) -> int:
    import faiss  # type: ignore[import-not-found]

    if not matrix_rows:
        return 0

    matrix = np.vstack(matrix_rows).astype(np.float32)
    dimension = matrix.shape[1]
    index_path.parent.mkdir(parents=True, exist_ok=True)

    if append and index_exists(str(index_path)):
        index = faiss.read_index(str(index_path))
        meta = load_index_meta(str(index_path)) or {}
        if int(index.d) != dimension:
            raise ValueError(
                f"FAISS dimension mismatch: index has {index.d}, new vectors have {dimension}"
            )
        existing_ids = [str(card_id) for card_id in meta.get("scryfall_ids", [])]
        existing_names = [str(name) for name in meta.get("card_names", [])]
        index.add(matrix)
        indexed_ids = existing_ids + indexed_ids
        indexed_names = existing_names + indexed_names
    else:
        index = faiss.IndexFlatIP(dimension)
        index.add(matrix)

    faiss.write_index(index, str(index_path))
    crop_mode = faiss_index_crop_mode(settings)
    _meta_path(str(index_path)).write_text(
        json.dumps(
            {
                "model_name": settings.openclip_model_name,
                "torch_device": settings.torch_device,
                "dimension": dimension,
                "index_crop_mode": crop_mode,
                "scryfall_ids": indexed_ids,
                "card_names": indexed_names,
            }
        ),
        encoding="utf-8",
    )
    clear_faiss_index_cache()
    return len(matrix_rows)


def search_similar_cards(
    image_path: str,
    settings: RecognitionSettings,
    top_k: int = 5,
) -> list[EmbeddingMatch]:
    index_path = settings.faiss_index_path
    loaded = _load_faiss_index(index_path)
    if loaded is None:
        return []

    index, meta = loaded
    ids: list[str] = meta.get("scryfall_ids", [])
    names: list[str] = meta.get("card_names", [])
    if not ids:
        return []

    query = embed_image_file(image_path, settings)
    k = min(top_k, len(ids))
    scores, indices = index.search(query, k)

    matches: list[EmbeddingMatch] = []
    for score, idx in zip(scores[0], indices[0], strict=False):
        if idx < 0 or idx >= len(ids):
            continue
        matches.append(
            EmbeddingMatch(
                scryfall_id=ids[idx],
                card_name=names[idx] if idx < len(names) else None,
                score=float(score),
            )
        )
    return matches


def build_index_from_printings(
    printings: list[PrintingRecord],
    settings: RecognitionSettings,
    *,
    append: bool = False,
    on_progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    """Download art, embed, and write a FAISS index from catalog printings."""
    pending_paths, card_ids, card_names, downloaded = prepare_art_paths(printings, settings)
    if not pending_paths:
        raise ValueError("Could not prepare any Scryfall art images for FAISS index.")

    matrix_rows, indexed_ids, indexed_names = embed_art_paths(
        pending_paths,
        card_ids,
        card_names,
        settings,
        on_progress=on_progress,
    )
    if not matrix_rows:
        raise ValueError("Could not embed any Scryfall art images for FAISS index.")

    index_path = Path(settings.faiss_index_path)
    vectors_indexed = write_faiss_index(
        index_path,
        matrix_rows,
        indexed_ids,
        indexed_names,
        settings,
        append=append,
    )
    return {
        "cards_considered": len(printings),
        "images_downloaded": downloaded,
        "vectors_indexed": vectors_indexed,
        "index_path": str(index_path),
        "torch_device": settings.torch_device,
        "embedding_batch_size": settings.embedding_batch_size,
    }
