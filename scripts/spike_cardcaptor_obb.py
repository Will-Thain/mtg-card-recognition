"""YOLO-P0 spike: stub CardCaptor OBB on smoke holdout fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from r0_spike_common import (
    ARTIFACT_DIR,
    FIXTURE_DIR,
    MANIFEST_PATH,
    image_by_eval_id,
    stub_cardcaptor_obb,
)

ROOT = Path(__file__).resolve().parent.parent


def run_smoke_holdout(manifest_path: Path, output_path: Path) -> int:
    """Run stub OBB on holdout images and write overlays.json."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id = image_by_eval_id(manifest)
    holdout_ids: list[str] = manifest["holdout_eval_ids"]

    overlays: list[dict[str, Any]] = []
    for eval_id in holdout_ids:
        record = by_id[eval_id]
        image_path = FIXTURE_DIR / record["file"]
        if not image_path.is_file():
            print(f"Missing fixture image: {image_path}", file=sys.stderr)
            return 1

        detections = stub_cardcaptor_obb(image_path)
        overlays.append(
            {
                "eval_id": eval_id,
                "file": record["file"],
                "holdout": True,
                "detector": "cardcaptor_obb_stub",
                "detections": detections,
            }
        )

    payload = {
        "mode": "smoke-holdout",
        "detector": "cardcaptor_obb_stub",
        "holdout_eval_ids": holdout_ids,
        "images_processed": len(overlays),
        "overlays": overlays,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {output_path} ({len(overlays)} holdout images)")
    return 0


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--smoke-holdout",
        action="store_true",
        help="Run stub OBB on holdout fixture images (CHK-YOLO-P0-01)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_PATH,
        help="Path to holdout_manifest.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ARTIFACT_DIR / "overlays.json",
        help="Output overlays JSON path",
    )
    args = parser.parse_args()

    if not args.smoke_holdout:
        print("Specify --smoke-holdout", file=sys.stderr)
        return 2

    return run_smoke_holdout(args.manifest, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
