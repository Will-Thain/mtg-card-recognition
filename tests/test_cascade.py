"""Tests for MVP-4 cascade stub API."""

from __future__ import annotations

from pathlib import Path

import pytest

from mtg_card_recognition import run_cascade

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_run_cascade_verified_first_candidate() -> None:
    """First candidate verifies when image path contains 'verified'."""
    image_path = FIXTURES / "images" / "verified.png"
    candidates = [
        {"printing_id": "aaa", "name": "Lightning Bolt", "set_code": "lea", "collector_number": "161"},
        {"printing_id": "bbb", "name": "Counterspell", "set_code": "lea", "collector_number": "54"},
    ]

    proposals = run_cascade(image_path, candidates)

    assert len(proposals) == 2
    assert proposals[0]["printing_id"] == "aaa"
    assert proposals[0]["gate_status"] == "verified"
    assert proposals[0]["gate_fail_reason"] is None
    assert proposals[1]["gate_status"] == "blocked_at_gate"
    assert proposals[1]["gate_fail_reason"] == "stub_secondary_candidate"


def test_run_cascade_proposed_when_not_verified_path() -> None:
    """Non-verified image paths keep the lead candidate at proposed status."""
    image_path = FIXTURES / "images" / "listing.jpg"
    candidates = [
        {"printing_id": "ccc", "name": "Sol Ring", "set_code": "c21", "collector_number": "263"},
    ]

    proposals = run_cascade(image_path, candidates)

    assert len(proposals) == 1
    assert proposals[0]["gate_status"] == "proposed"
    assert proposals[0]["gate_fail_reason"] is None


def test_run_cascade_is_deterministic() -> None:
    """Repeated runs with the same inputs return identical proposals."""
    image_path = "tests/fixtures/images/verified.png"
    candidates = [{"printing_id": "det", "name": "Test Card"}]

    first = run_cascade(image_path, candidates)
    second = run_cascade(image_path, candidates)

    assert first == second


@pytest.mark.parametrize(
    ("image_path", "expected_status"),
    [
        ("tests/fixtures/images/verified.png", "verified"),
        ("tests/fixtures/images/listing.jpg", "proposed"),
    ],
)
def test_run_cascade_gate_status_by_image_path(image_path: str, expected_status: str) -> None:
    """Gate status follows deterministic image-path rules."""
    proposals = run_cascade(image_path, [{"printing_id": "x", "name": "Card"}])

    assert proposals[0]["gate_status"] == expected_status
