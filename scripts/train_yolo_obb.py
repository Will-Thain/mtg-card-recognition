#!/usr/bin/env python3
"""Train or export yolo11n-obb when ultralytics is available (YOLO-P1)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = REPO_ROOT.parent / "mtg-ebay-workflows" / ".cache" / "training" / "obb-v1" / "data.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.data.is_file():
        print(
            "train_yolo_obb: create data.yaml via labeling pack + operator labels first",
            file=sys.stderr,
        )
        print(f"  expected: {args.data}", file=sys.stderr)
        return 1

    command = f"yolo obb train data={args.data} model=yolo11n-obb.pt epochs={args.epochs}"
    if args.dry_run:
        print(f"train_yolo_obb: dry-run command: {command}")
        return 0

    try:
        from ultralytics import YOLO
    except ImportError:
        print("train_yolo_obb: install ultralytics in training venv (train-only, not runtime)", file=sys.stderr)
        print(f"  then run: {command}", file=sys.stderr)
        return 1

    model = YOLO("yolo11n-obb.pt")
    model.train(data=str(args.data), epochs=args.epochs)
    print("train_yolo_obb: training complete — export ONNX per runbooks/training-yolo-obb-v1.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
