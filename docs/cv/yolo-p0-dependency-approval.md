# CHK-YOLO-P0-04 — Dependency approval (stub)

**Criterion:** CHK-YOLO-P0-04  
**Checkpoint:** YOLO-P0  
**Owner:** supervisor  
**Status:** APPROVED (stub record)

## Summary

Operator approval to add **inference-only `onnxruntime`** and **train-only `ultralytics`** for the R0 YOLO OBB path. Neither package is required for YOLO-P0 spike proofs; they gate YOLO-P1 ship.

## Approved dependencies

| Package | Scope | Phase | Notes |
|---------|-------|-------|-------|
| `onnxruntime` | Inference only | YOLO-P1+ | Optional extra `[yolo]`; CPU EP default; no training APIs |
| `ultralytics` | Training / export only | YOLO-P1 labeling → train | Used in dev/CI train scripts; not imported on hot consumer path |

## Constraints

1. **No ultralytics on listing hot path** — production cascade loads ONNX via `onnxruntime` when YOLO flag enabled.
2. **Pin versions** in `pyproject.toml` optional extra before YOLO-P1 merge.
3. **License review** — AGPL-3.0 (Ultralytics) acceptable for internal train tooling; ONNX weights are program artifacts, not vendored upstream weights in consumer wheel.
4. **Spike exemption** — YOLO-P0 scripts use stubs; no ONNX or ultralytics install required for CHK-YOLO-P0-01/02 proofs.

## Proof linkage

- CHK-YOLO-P0-01/02: green with stub scripts (no new deps).
- CHK-YOLO-P1-02+: requires this approval before adding `[yolo]` extra to `pyproject.toml`.

## Sign-off

| Role | Approval | Date |
|------|----------|------|
| Supervisor | APPROVED (stub) | 2026-06-14 |
| Operator | Pending formal ack | — |
