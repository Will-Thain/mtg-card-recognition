# mtg-card-recognition

Standalone Python library for Magic: The Gathering card recognition from listing photos:

- OpenCV region detection, alignment, and zone crops (name, art, bottom, symbol, mana)
- Tesseract zone OCR and set-symbol template matching
- OpenCLIP art embeddings + FAISS nearest-neighbor search
- Strict **propose-then-confirm** evidence gate (set+collector / symbol+name)
- Framework-agnostic `RecognitionSettings` and `PrintingRecord` catalog types

## Install

```bash
pip install mtg-card-recognition
```

Development (from this repo):

```bash
pip install -e ".[dev]"
```

## Quick start

```python
from mtg_card_recognition import RecognitionSettings
from mtg_card_recognition.zones.signals import extract_card_zone_signals
from mtg_card_recognition.embeddings import search_similar_cards

settings = RecognitionSettings(
    image_cache_dir="./.cache/images",
    faiss_index_path="./.cache/faiss/index.bin",
)

fields, crops, evidence = extract_card_zone_signals(
    "path/to/region.jpg",
    zone_dir="./.cache/images/crops/zones",
    settings=settings,
)

matches = search_similar_cards(crops.art_path or "path/to/region.jpg", settings, top_k=5)
```

## Public API

| Symbol | Module |
|--------|--------|
| `RecognitionSettings` | `mtg_card_recognition.config` |
| `PrintingRecord` | `mtg_card_recognition.catalog` |
| `extract_card_zone_signals` | `mtg_card_recognition.zones.signals` |
| `search_similar_cards`, `build_index_from_printings` | `mtg_card_recognition.embeddings` |
| `apply_per_listing_verification_gates` | `mtg_card_recognition.evidence` |

## Tests

```bash
pytest
```

Labeled crop fixtures live under `tests/fixtures/labeled_crops/`.

## Consumers

- **[EbayWorkflows](https://github.com/your-org/EbayWorkflows)** — eBay ingest, pricing, GUI (depends on this package)
- Other marketplace / scanner apps can reuse the same gate and FAISS stack

## License

Proprietary — see repository LICENSE.
