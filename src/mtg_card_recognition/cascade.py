"""Cascade API stub — deterministic Tier 8 gate fields for tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

GateStatus = str


def run_cascade(image_path: str | Path, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Run cascade tiers on an image against title-match candidates.

    MVP-4 stub: returns one proposal per candidate with deterministic
    ``gate_status`` and ``gate_fail_reason`` derived from path and rank.
    """
    image_key = str(image_path).lower().replace("\\", "/")
    proposals: list[dict[str, Any]] = []

    for index, candidate in enumerate(candidates):
        proposal = dict(candidate)
        if index == 0 and "verified" in image_key:
            proposal["gate_status"] = "verified"
            proposal["gate_fail_reason"] = None
        elif index == 0:
            proposal["gate_status"] = "proposed"
            proposal["gate_fail_reason"] = None
        else:
            proposal["gate_status"] = "blocked_at_gate"
            proposal["gate_fail_reason"] = "stub_secondary_candidate"
        proposals.append(proposal)

    return proposals
