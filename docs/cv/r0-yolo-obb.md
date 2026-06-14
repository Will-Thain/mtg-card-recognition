# R0 YOLO-OBB (YOLO-P1 foundation)

Greenfield **Tier-0** card region detection behind `REGION_DETECTOR=yolo_obb`.

## Behavior

| Setting | Default | Notes |
|---------|---------|-------|
| `region_detector` | `canny` | Rollback without code revert |
| `yolo_obb_model_path` | unset | Stub detector when unset |
| `yolo_obb_model_version` | `yolo_obb_stub_v0` | Persisted on cascade proposals |
| `image_allow_full_frame_fallback` | `true` | Set `false` with YOLO in production |

## Proof commands

```powershell
pytest tests/test_yolo_obb_regions.py tests/test_align_yolo.py -q
python scripts/compare_r0_detectors.py --detector yolo_obb --gate recall
```

## Operator blockers (full P1 PASS)

- **CHK-YOLO-P1-01** — ≥300 labeled train images (`verify_obb_train_manifest.py`)
- **CHK-YOLO-P1-06** — human GUI bbox pass on smoke control listings
