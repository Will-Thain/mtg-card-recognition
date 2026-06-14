"""Build a minimal FAISS index from sample fixture embeddings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import faiss
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "faiss" / "cards.json"
DEFAULT_OUTPUT = ROOT / ".cache" / "faiss" / "index.bin"


def load_cards(fixture_path: Path) -> list[dict[str, Any]]:
    """Load card records with embeddings from a JSON fixture."""
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    cards = payload.get("cards", [])
    if not isinstance(cards, list):
        msg = f"Expected 'cards' list in {fixture_path}"
        raise ValueError(msg)
    return cards


def build_index(fixture_path: Path, output_path: Path) -> int:
    """Write a FAISS index and sidecar metadata from fixture embeddings."""
    cards = load_cards(fixture_path)
    if not cards:
        print(f"No cards found in {fixture_path}", file=sys.stderr)
        return 1

    embeddings = [card["embedding"] for card in cards]
    vectors = np.array(embeddings, dtype=np.float32)
    dimension = int(vectors.shape[1])

    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_path))

    resolved_fixture = fixture_path.resolve()
    try:
        source_fixture = str(resolved_fixture.relative_to(ROOT.resolve()))
    except ValueError:
        source_fixture = str(resolved_fixture)

    meta = {
        "printing_ids": [str(card["printing_id"]) for card in cards],
        "dim": dimension,
        "count": len(cards),
        "source_fixture": source_fixture,
    }
    meta_path = Path(f"{output_path}.meta.json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {output_path} ({len(cards)} vectors, dim={dimension})")
    return 0


def main() -> int:
    """CLI entrypoint for building the sample FAISS index."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Path to cards.json fixture with embeddings",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output path for the FAISS index file",
    )
    args = parser.parse_args()
    return build_index(args.fixture, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
