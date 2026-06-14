"""YOLO-P0 spike: compare stub Canny baseline vs stub YOLO OBB on fixtures."""

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
    count_fp_fn,
    image_by_eval_id,
    stub_canny_detector,
    stub_yolo_obb_detector,
)

ROOT = Path(__file__).resolve().parent.parent


def run_compare(baseline: str, manifest_path: Path, output_path: Path) -> int:
    """Compare baseline vs YOLO stub on non-holdout fixture images."""
    if baseline != "canny":
        print(f"Unsupported baseline: {baseline}", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id = image_by_eval_id(manifest)
    compare_ids: list[str] = manifest.get("compare_eval_ids", [])
    ground_truth: dict[str, list[dict[str, Any]]] = manifest.get("ground_truth", {})

    per_image: list[dict[str, Any]] = []
    total_fp = 0
    total_fn = 0

    for eval_id in compare_ids:
        record = by_id[eval_id]
        image_path = FIXTURE_DIR / record["file"]
        if not image_path.is_file():
            print(f"Missing fixture image: {image_path}", file=sys.stderr)
            return 1

        truth = ground_truth.get(eval_id, [])
        canny_preds = stub_canny_detector(image_path)
        yolo_preds = stub_yolo_obb_detector(image_path)

        canny_fp, canny_fn = count_fp_fn(canny_preds, truth)
        yolo_fp, yolo_fn = count_fp_fn(yolo_preds, truth)

        per_image.append(
            {
                "eval_id": eval_id,
                "file": record["file"],
                "baseline": {
                    "detector": "canny_stub",
                    "false_positives": canny_fp,
                    "false_negatives": canny_fn,
                },
                "candidate": {
                    "detector": "yolo_obb_stub",
                    "false_positives": yolo_fp,
                    "false_negatives": yolo_fn,
                },
            }
        )
        total_fp += canny_fp
        total_fn += canny_fn

    report = {
        "baseline": baseline,
        "candidate_detector": "yolo_obb_stub",
        "eval_ids_compared": compare_ids,
        "false_positives": total_fp,
        "false_negatives": total_fn,
        "per_image": per_image,
        "note": "Stub spike report on synthetic fixtures; not production cache images.",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"false_positives": total_fp, "false_negatives": total_fn}))
    print(f"Wrote {output_path}")
    return 0


def run_yolo_gate(manifest_path: Path, gate: str) -> int:
    """Evaluate stub YOLO OBB against ground truth for P1 eval gates."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id = image_by_eval_id(manifest)
    compare_ids: list[str] = manifest.get("compare_eval_ids", [])
    ground_truth: dict[str, list[dict[str, Any]]] = manifest.get("ground_truth", {})

    total_fp = 0
    total_fn = 0
    images = max(len(compare_ids), 1)

    for eval_id in compare_ids:
        record = by_id[eval_id]
        image_path = FIXTURE_DIR / record["file"]
        truth = ground_truth.get(eval_id, [])
        preds = stub_yolo_obb_detector(image_path)
        fp, fn = count_fp_fn(preds, truth)
        total_fp += fp
        total_fn += fn

    recall = 1.0 - (total_fn / max(sum(len(ground_truth.get(i, [])) for i in compare_ids), 1))
    mean_fp = total_fp / images

    if gate == "recall" and recall < 0.95:
        print(json.dumps({"recall": recall, "status": "fail"}))
        return 1
    if gate == "fp" and mean_fp > 0.5:
        print(json.dumps({"mean_fp": mean_fp, "status": "fail"}))
        return 1

    print(json.dumps({"recall": recall, "mean_fp": mean_fp, "status": "pass"}))
    return 0


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        choices=["canny"],
        help="Baseline detector for comparison (CHK-YOLO-P0-02)",
    )
    parser.add_argument(
        "--detector",
        choices=["yolo_obb"],
        help="Candidate detector for eval gates (CHK-YOLO-P1-04/05)",
    )
    parser.add_argument(
        "--gate",
        choices=["recall", "fp"],
        help="Eval gate to enforce on stub fixtures",
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
        default=ARTIFACT_DIR / "compare_report.json",
        help="Output compare report JSON path",
    )
    args = parser.parse_args()

    if args.detector == "yolo_obb" and args.gate:
        return run_yolo_gate(args.manifest, args.gate)

    if args.baseline is None:
        print("Specify --baseline canny", file=sys.stderr)
        return 2

    return run_compare(args.baseline, args.manifest, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
