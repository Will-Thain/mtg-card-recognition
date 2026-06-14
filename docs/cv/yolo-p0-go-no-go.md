# CHK-YOLO-P0-05 — R0 detector go / no-go

**Criterion:** CHK-YOLO-P0-05  
**Checkpoint:** YOLO-P0  
**Owner:** agent-python-recognition  
**Status:** GO (spike scaffolding)

## Decision

**Proceed with `yolo11n-obb` fine-tune** as the primary R0 card-detection path. Do not pursue CardCaptor ONNX fine-tune for production inference in this program.

## Evidence (spike stub)

| Path | Role |
|------|------|
| `scripts/spike_cardcaptor_obb.py --smoke-holdout` | Validates holdout smoke overlay export |
| `scripts/compare_r0_detectors.py --baseline canny` | FP/FN stub compare on non-holdout fixture |
| `tests/fixtures/r0_spike/holdout_manifest.json` | Two eval holdout IDs + one compare image |

Stub spike results on synthetic fixtures show the YOLO OBB stub matching ground truth (0 FP / 0 FN) while the Canny stub reports 1 FP / 0 FN on the compare image. This is sufficient to green-light **labeling + yolo11n-obb training** for YOLO-P1; real CardCaptor ONNX evaluation remains out of scope for P0.

## Rationale

1. **CardCaptor ONNX** — third-party weights, export friction, and unclear license/maintenance for our OBB labeling SOP.
2. **yolo11n-obb** — Ultralytics train path aligns with operator OBB labels, ONNX export for inference (YOLO-P1), and existing cascade Tier-0 integration plan.
3. **Holdout discipline** — smoke control listings stay eval-only per `holdout_manifest.json`; training manifests must exclude those IDs (CHK-YOLO-P0-03, workflows repo).

## Next steps (YOLO-P1)

- Label ≥300 train images (holdout excluded).
- Fine-tune `yolo11n-obb` from COCO-pretrained weights.
- Export ONNX for optional `onnxruntime` inference path.
- Replace stub detectors in `zones/yolo_obb.py` with real model dispatch.

## Sign-off

| Role | Decision | Date |
|------|----------|------|
| Recognition agent | GO — yolo11n-obb | 2026-06-14 |
| Supervisor | Pending independent proof | — |
