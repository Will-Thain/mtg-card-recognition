"""Smoke tests for YOLO-P0 R0 spike scaffolding."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "r0_spike"
SCRIPTS_DIR = ROOT / "scripts"
MANIFEST_PATH = FIXTURE_DIR / "holdout_manifest.json"


def _load_script_module(name: str):
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_holdout_manifest_lists_two_eval_ids() -> None:
    """Holdout manifest exposes exactly two eval-only IDs."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["holdout_eval_ids"] == ["r0_spike_001", "r0_spike_002"]


@pytest.mark.parametrize(
    "filename",
    ["holdout_001.jpg", "holdout_002.jpg", "train_001.jpg"],
)
def test_fixture_jpegs_exist_and_load(filename: str) -> None:
    """Synthetic fixture JPEGs exist and begin with JPEG magic bytes."""
    path = FIXTURE_DIR / filename
    assert path.is_file()
    data = path.read_bytes()
    assert data[:2] == b"\xff\xd8"
    assert len(data) > 100


def test_spike_scripts_importable() -> None:
    """Spike scripts load without requiring ONNX or legacy cache."""
    spike = _load_script_module("spike_cardcaptor_obb")
    compare = _load_script_module("compare_r0_detectors")
    common = _load_script_module("r0_spike_common")

    assert hasattr(spike, "main")
    assert hasattr(compare, "main")
    assert hasattr(common, "stub_cardcaptor_obb")
