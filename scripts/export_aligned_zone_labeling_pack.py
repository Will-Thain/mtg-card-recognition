#!/usr/bin/env python3
"""Export aligned crop images for zone YOLO labeling (YOLO-P2)."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / ".cache" / "training" / "zone-v1"


def export_pack(*, out_dir: Path, source_dir: Path | None = None) -> int:
    """Copy aligned crop JPGs into a labeling pack directory."""
    source = source_dir or (REPO_ROOT / "tests" / "fixtures" / "r0_spike")
    if not source.is_dir():
        print(f"export_aligned_zone_labeling_pack: missing source {source}", file=sys.stderr)
        return 1

    images_dir = out_dir / "images"
    labels_dir = out_dir / "labels"
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, str]] = []
    for index, image_path in enumerate(sorted(source.glob("*.jpg")), start=1):
        dest = images_dir / f"aligned_{index:04d}{image_path.suffix.lower()}"
        shutil.copy2(image_path, dest)
        label_path = labels_dir / f"{dest.stem}.txt"
        label_path.write_text("", encoding="utf-8")
        entries.append(
            {
                "image_path": dest.relative_to(out_dir).as_posix(),
                "label_path": label_path.relative_to(out_dir).as_posix(),
            }
        )

    manifest = {
        "version": 1,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "entries": entries,
        "classes": ["bottom", "set_symbol", "title"],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"export_aligned_zone_labeling_pack: OK entries={len(entries)} out={out_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--source", type=Path, default=None)
    args = parser.parse_args()
    out_dir = args.out if args.out.is_absolute() else (REPO_ROOT / args.out).resolve()
    return export_pack(out_dir=out_dir, source_dir=args.source)


if __name__ == "__main__":
    raise SystemExit(main())
